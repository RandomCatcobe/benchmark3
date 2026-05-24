from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRATCH = ROOT / "data" / "verification" / "php_new_probe"
COMPOSER = str(Path.home() / "scoop" / "shims" / "composer.cmd")


@dataclass(frozen=True)
class Candidate:
    slug: str
    package: str
    old: str
    new: str
    source: str
    client: str


CANDIDATES = [
    Candidate(
        slug="php-doctrine-inflector-axis-brownies",
        package="doctrine/inflector",
        old="2.0.8",
        new="2.0.9",
        source="https://github.com/doctrine/inflector/releases/tag/2.0.9",
        client=r'''<?php
require __DIR__ . "/vendor/autoload.php";

$inflector = Doctrine\Inflector\InflectorFactory::create()->build();
echo json_encode([
  "axis_plural" => $inflector->pluralize("axis"),
  "brownies_singular" => $inflector->singularize("brownies"),
], JSON_UNESCAPED_SLASHES), PHP_EOL;
''',
    ),
    Candidate(
        slug="php-guzzle-psr7-uri-userinfo-encoding",
        package="guzzlehttp/psr7",
        old="1.5.2",
        new="1.6.0",
        source="https://github.com/guzzle/psr7/releases/tag/1.6.0",
        client=r'''<?php
require __DIR__ . "/vendor/autoload.php";

$uri = (string) (new GuzzleHttp\Psr7\Uri("https://example.com"))->withUserInfo("al ice", "p@ss");
echo json_encode(["uri" => $uri], JSON_UNESCAPED_SLASHES), PHP_EOL;
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
        "package": candidate.package,
        "old": candidate.old,
        "new": candidate.new,
        "source": candidate.source,
    }
    for side, version in (("old", candidate.old), ("new", candidate.new)):
        work = SCRATCH / candidate.slug / side
        work.mkdir(parents=True, exist_ok=True)
        (work / "composer.json").write_text(
            json.dumps(
                {
                    "require": {candidate.package: version},
                    "config": {
                        "disable-tls": True,
                        "secure-http": False,
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (work / "probe.php").write_text(candidate.client, encoding="utf-8")
        install = subprocess.run(
            [COMPOSER, "install", "--no-interaction", "--no-progress", "--quiet"],
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
            ["php", "probe.php"],
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
