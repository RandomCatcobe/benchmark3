from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRATCH = ROOT / "data" / "verification" / "ruby_new_probe"
BUNDLE = str(Path.home() / "scoop" / "apps" / "ruby" / "current" / "bin" / "bundle.bat")


@dataclass(frozen=True)
class Candidate:
    slug: str
    old: str
    new: str
    source: str
    gemfile_template: str
    client: str


CANDIDATES = [
    Candidate(
        slug="ruby-public-suffix-pages-gay-domain",
        old="5.0.4",
        new="5.0.5",
        source="https://github.com/weppos/publicsuffix-ruby/blob/main/CHANGELOG.md",
        gemfile_template='source "https://rubygems.org"\ngem "public_suffix", "{version}"\n',
        client=r'''require "json"
require "public_suffix"

puts JSON.generate({ domain: PublicSuffix.domain("foo.pages.gay") })
''',
    ),
    Candidate(
        slug="ruby-mime-types-data-parquet-type",
        old="3.2025.0924",
        new="3.2026.0317",
        source="https://github.com/mime-types/mime-types-data/blob/main/CHANGELOG.md",
        gemfile_template='source "https://rubygems.org"\ngem "mime-types", "3.6.0"\ngem "mime-types-data", "{version}"\n',
        client=r'''require "json"
require "mime/types"

type = MIME::Types.type_for("x.parquet").first
puts JSON.generate({ content_type: type&.content_type })
''',
    ),
]


def main() -> int:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir(parents=True)
    kept: list[str] = []
    for candidate in CANDIDATES:
        result = probe(candidate)
        print(json.dumps(result, sort_keys=True), flush=True)
        if (
            result["old_exit"] == 0
            and result["new_exit"] == 0
            and result["old_stderr"] == ""
            and result["new_stderr"] == ""
            and result["old_stdout"] != result["new_stdout"]
        ):
            kept.append(candidate.slug)
    print(json.dumps({"kept": kept, "kept_count": len(kept)}, sort_keys=True), flush=True)
    return 0


def probe(candidate: Candidate) -> dict[str, object]:
    result: dict[str, object] = {
        "slug": candidate.slug,
        "old": candidate.old,
        "new": candidate.new,
        "source": candidate.source,
    }
    for side, version in (("old", candidate.old), ("new", candidate.new)):
        work = SCRATCH / candidate.slug / side
        work.mkdir(parents=True, exist_ok=True)
        (work / "Gemfile").write_text(candidate.gemfile_template.format(version=version), encoding="utf-8")
        (work / "probe.rb").write_text(candidate.client, encoding="utf-8")
        config = subprocess.run(
            [BUNDLE, "config", "set", "path", "vendor/bundle"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        if config.returncode != 0:
            result[f"{side}_exit"] = config.returncode
            result[f"{side}_stdout"] = config.stdout.strip()
            result[f"{side}_stderr"] = config.stderr.strip()
            continue
        install = subprocess.run(
            [BUNDLE, "install", "--quiet"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            timeout=240,
        )
        if install.returncode != 0:
            result[f"{side}_exit"] = install.returncode
            result[f"{side}_stdout"] = install.stdout.strip()
            result[f"{side}_stderr"] = install.stderr.strip()
            continue
        run = subprocess.run(
            [BUNDLE, "exec", "ruby", "probe.rb"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        result[f"{side}_exit"] = run.returncode
        result[f"{side}_stdout"] = run.stdout.strip()
        result[f"{side}_stderr"] = run.stderr.strip()
    return result


if __name__ == "__main__":
    raise SystemExit(main())
