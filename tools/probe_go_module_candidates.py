from __future__ import annotations

import json
import shutil
import subprocess
import textwrap
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "data" / "verification" / "go_module_probe"


@dataclass(frozen=True)
class Candidate:
    slug: str
    module: str
    old: str
    new: str
    source: str
    main_go: str


CANDIDATES = [
    Candidate(
        slug="go-masterminds-semver-prerelease-range",
        module="github.com/Masterminds/semver/v3",
        old="v3.3.1",
        new="v3.4.0",
        source="https://github.com/Masterminds/semver/releases/tag/v3.4.0",
        main_go=r'''
package main

import (
	"encoding/json"
	"fmt"

	semver "github.com/Masterminds/semver/v3"
)

func main() {
	constraint, err := semver.NewConstraint(">1.0.0-beta.1 <2")
	if err != nil {
		panic(err)
	}
	version := semver.MustParse("1.0.0-beta.2")
	payload := map[string]any{
		"check": constraint.Check(version),
	}
	out, err := json.Marshal(payload)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(out))
}
''',
    ),
    Candidate(
        slug="go-jsoniter-map-key-text-marshaler",
        module="github.com/json-iterator/go",
        old="v1.1.9",
        new="v1.1.10",
        source="https://github.com/json-iterator/go/releases/tag/v1.1.10",
        main_go=r'''
package main

import (
	"encoding/json"
	"fmt"

	jsoniter "github.com/json-iterator/go"
)

type Key string

func (k Key) MarshalText() ([]byte, error) {
	return []byte("key_" + string(k)), nil
}

func main() {
	text, err := jsoniter.Marshal(map[Key]int{"a": 1})
	payload := map[string]any{"text": string(text)}
	if err != nil {
		payload["err"] = err.Error()
	}
	out, err := json.Marshal(payload)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(out))
}
''',
    ),
    Candidate(
        slug="go-pelletier-toml-omitzero-tag",
        module="github.com/pelletier/go-toml/v2",
        old="v2.2.4",
        new="v2.3.0",
        source="https://github.com/pelletier/go-toml/releases/tag/v2.3.0",
        main_go=r'''
package main

import (
	"encoding/json"
	"fmt"

	"github.com/pelletier/go-toml/v2"
)

type Config struct {
	Count int `toml:"count,omitzero"`
}

func main() {
	text, err := toml.Marshal(Config{})
	payload := map[string]any{"toml": string(text)}
	if err != nil {
		payload["err"] = err.Error()
	}
	out, err := json.Marshal(payload)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(out))
}
''',
    ),
    Candidate(
        slug="go-goccy-yaml-text-marshaler-string",
        module="github.com/goccy/go-yaml",
        old="v1.17.1",
        new="v1.18.0",
        source="https://github.com/goccy/go-yaml/releases/tag/v1.18.0",
        main_go=r'''
package main

import (
	"encoding/json"
	"fmt"

	"github.com/goccy/go-yaml"
)

type Value struct{}

func (Value) MarshalText() ([]byte, error) {
	return []byte("a: b"), nil
}

func main() {
	text, err := yaml.Marshal(map[string]Value{"v": {}})
	payload := map[string]any{"yaml": string(text)}
	if err != nil {
		payload["err"] = err.Error()
	}
	out, err := json.Marshal(payload)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(out))
}
''',
    ),
]


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)

    results = []
    for candidate in CANDIDATES:
        result = run_candidate(candidate)
        results.append(result)
        print(json.dumps(result, sort_keys=True), flush=True)

    kept = [item for item in results if item["old_exit"] == 0 and item["new_exit"] == 0 and item["old_stdout"] != item["new_stdout"] and not item["old_stderr"] and not item["new_stderr"]]
    print(json.dumps({"kept": [item["slug"] for item in kept], "kept_count": len(kept)}, sort_keys=True), flush=True)
    return 0


def run_candidate(candidate: Candidate) -> dict[str, object]:
    old = run_side(candidate, "old", candidate.old)
    new = run_side(candidate, "new", candidate.new)
    return {
        "slug": candidate.slug,
        "module": candidate.module,
        "old": candidate.old,
        "new": candidate.new,
        "source": candidate.source,
        "old_exit": old.returncode,
        "new_exit": new.returncode,
        "old_stdout": old.stdout.strip(),
        "new_stdout": new.stdout.strip(),
        "old_stderr": old.stderr.strip(),
        "new_stderr": new.stderr.strip(),
    }


def run_side(candidate: Candidate, label: str, version: str) -> subprocess.CompletedProcess[str]:
    case_dir = WORK / candidate.slug / label
    case_dir.mkdir(parents=True)
    (case_dir / "go.mod").write_text(f"module probe\n\ngo 1.23\n\nrequire {candidate.module} {version}\n", encoding="utf-8")
    (case_dir / "main.go").write_text(textwrap.dedent(candidate.main_go).strip() + "\n", encoding="utf-8")
    subprocess.run(["go", "mod", "tidy"], cwd=case_dir, capture_output=True, text=True, check=False, timeout=180)
    return subprocess.run(["go", "run", "."], cwd=case_dir, capture_output=True, text=True, check=False, timeout=180)


if __name__ == "__main__":
    raise SystemExit(main())
