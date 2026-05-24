# Paper Readiness Audit — SilentDriftBench + DriftRL

**Audited:** 2026-05-23  
**Auditor:** Read-only inspection of `benchmark3-upload-work` and `beachmark4silentdrift`  
**Scope:** EMNLP/AAAI artifact readiness. No code was modified. No data was invented.

---

## 1. Repository Map

| Repo | Local path | Role in paper claim |
|---|---|---|
| `benchmark3-upload-work` | `bench2/benchmark3-upload-work/` | Case factory (older generation; largely superseded) |
| `beachmark4silentdrift` | `bench2/shishan/worktree/beachmark4silentdrift/` | Canonical case bank, eval-pack generator, grading schema |
| `neobenchmark4silentdrift` | `bench2/neobenchmark4silentdrift/` | Near-empty stub (2 JS triage docs only; not usable as artifact) |

The canonical repo for paper purposes is `beachmark4silentdrift`. `benchmark3-upload-work` contains overlapping and older data; its 15 cases in `cases/` are a subset of the 160 in the canonical bank.

---

## 2. Case Count — Current State

### 2.1 Total case entries in `docs/case-bank/cases/`

| Status | Count | Notes |
|---|---:|---|
| `verified_keep` | **65** | Both public + hidden oracle present |
| `rejected_cluster_duplicate` | 38 | Verified reproductions but deduplicated out of benchmark |
| `blocked_dependency` | 27 | Cannot reproduce: language runtime pair not cached |
| `blocked_runtime` | 15 | Cannot reproduce offline: requires live API credential |
| `needs_source` | 8 | Evidence too weak to include |
| `rejected_no_diff` | 7 | Reproduced but old/new behavior identical |
| **Total** | **160** | All have `metadata.json`; all have `client/` |

### 2.2 verified_keep breakdown

| Sub-cohort | Count | Determinism |
|---|---:|---|
| Main batch (seq-30, rev-50, old-15, extra) | 46 | local-deterministic or runtime-pair |
| Strict Python (PY-STRICT-*, PY-HOL-*) | 19 | local-deterministic |
| **Total verified_keep** | **65** | |

Of the 65 `verified_keep`:
- **60 are `local-deterministic`** (offline, no network, reproducible with pinned package versions)
- **5 are `runtime-pair`** (require a specific runtime environment pair to run the probe)

All 65 have `hidden/expected.json` and `hidden/oracle.md`. All 65 have `client/`.

### 2.3 Cases that cannot be counted as offline-reproducible benchmark entries

| Group | Count | Reason |
|---|---:|---|
| NEW-20260520-* (ecommerce platform) | 10 | `blocked_runtime` / `requires-live-credential` |
| SEED-20260520-* (ecommerce seed) | 8 | `blocked_runtime` / `needs_source` / `requires-live-credential` |
| `rejected_cluster_duplicate` PY-HOL | 38 | Valid reproductions, but curation decision removed them as redundant cluster |
| `blocked_dependency` | 27 | Could not install runtime pair in available environment |
| `rejected_no_diff` | 7 | No behavioral difference confirmed |

**Claimable offline-reproducible benchmark size: 60 cases** (the `local-deterministic` verified_keep subset).

---

## 3. Ecosystem Coverage (verified_keep only)

| Ecosystem | Count |
|---|---:|
| python | 31 |
| js | 9 |
| go | 6 |
| jvm | 6 |
| php | 6 |
| ruby | 4 |
| dotnet | 3 |

Drift type coverage (drift_patterns field, 13 possible values, all represented at least once in verified_keep).

Scenario coverage: all 10 primary_scenarios represented in verified_keep.

---

## 4. Existing Functional Components

### 4.1 What works and is tested

| Component | Location | Status |
|---|---|---|
| Metadata schema validation | `silent_drift_miner/src/case_bank/schema.py` | Working; enforces enum values, required fields, provenance |
| Case bank validation | `silent_drift_miner/src/case_bank/validation.py` | Working; checks file layout, oracle presence for verified cases |
| Eval-pack generator | `silent_drift_miner/src/case_bank/pack.py` | Working; strips `hidden/` directory before output |
| Pack leak check | `silent_drift_miner/src/case_bank/pack.py::validate_case_bank_eval_package` | Working; asserts no oracle content in output |
| Index generation | `silent_drift_miner/src/case_bank/index.py` | Working; 5 Markdown index files (by-status, by-language, by-scenario, etc.) |
| CLI entry | `python -m case_bank {index,pack,validate}` | Working |
| Test suite | `silent_drift_miner/tests/` (26 test files) | Unit tests for adapter, oracle, pack, validation, bench-audit |
| Existing eval package | `artifacts/eval_package_full_v20260522_091724/` | Snapshot from 2026-05-22, 88 cases, no hidden material |

### 4.2 Reproduction harness (benchmark3 / bench4 shared tool)

| Capability | Status |
|---|---|
| Python venv-based reproduction | Working; uses `silent-drift-miner reproduce run` |
| Ecosystem adapters | Python: working. Go, JS, JVM, .NET, Ruby, PHP: functional but minimally tested |
| Old/new stdout diff comparison | Working; structured comparison with JSON-field ignore list |
| Case-bank writer | Working; produces full case folder from reproduction result |
| LLM-assisted extraction | Exists (`extractors/llm.py`); requires `ANTHROPIC_API_KEY`; not validated at scale |

### 4.3 Oracle schema

Each `hidden/expected.json` uses schema_version 1:
```json
{
  "schema_version": 1,
  "case_id": "...",
  "assertions": [
    { "name": "...", "field": "...", "old": "...", "new": "..." }
  ]
}
```

This is a **field-equality oracle**: it asserts that a named field in the probe output changed from value `old` to value `new` across the version boundary. It is not a rubric, not a scoring function, and not an LLM judge. It is suitable for automated pass/fail scoring of deterministic probes.

---

## 5. What Is Only Smoke / Toy Level

| Item | Reality |
|---|---|
| Non-Python ecosystem adapters (Go, JS, JVM, .NET, Ruby, PHP) | Functional for toy-drift cases; not systematically verified across all 65 cases |
| The 5 `old15-*_toy_drift` cases | Synthetic toy drifts created for adapter testing; not real-world behavioral drift |
| Old `benchmark3-upload-work/cases/` directory | 15 legacy cases; only 9 Python ones have real probe clients; toy_drift entries are stubs |
| `eval_package_old15_check/` | Temporary validation artifact; not a releasable benchmark |
| `data/curated/*.yaml` | 5 old-format curated cases; superseded by case-bank format |

---

## 6. What Cannot Be Claimed in a Paper

The following cannot be stated as contributions without additional work:

1. **"160-case benchmark"**: The auditable, claimable, offline-reproducible core is **60 cases** (local-deterministic verified_keep). The remaining 100 entries are either blocked, deduplicated, or require live credentials.

2. **"Multi-ecosystem benchmark with 7 languages"**: Coverage exists but depth is uneven. Python has 31 verified cases; .NET has 3. A paper must report per-ecosystem counts honestly and not present the tail as equivalent to the head.

3. **"AgenticRL environment" / "DriftRL"**: No RL code exists in either repository. There is no gym/environment interface, no reward function, no mock replay mechanism, no agent interaction trace, and no agentic_rl_adapter. This is a paper idea not yet implemented.

4. **"Ecommerce API drift as offline-reproducible cases"**: All 10 NEW-20260520 cases (Douyin, Amazon, Walmart, Adobe Commerce, BigCommerce, Mercado Libre, etc.) and all 8 SEED cases are `blocked_runtime` or `needs_source`. They are documented leads, not packaged offline benchmark entries.

5. **"Curated with human verification"**: The claim is partially supported. The 65 verified_keep cases have human-checked provenance and reproduction results. The 38 rejected_cluster_duplicate PY-HOL cases were verified but then deduplicated by curation decision — they cannot be counted as independent benchmark entries.

6. **"Oracle measures what the agent predicts"**: The current oracle only checks whether a probe program emits a changed value. There is no mechanism that measures whether an LLM agent *predicts* the behavioral change or *diagnoses* its root cause. The oracle is a ground-truth label, not an evaluation rubric.

---

## 7. Minimum Missing Artifacts for EMNLP/AAAI Submission

Roughly in dependency order:

### 7.1 Dataset card (blocking)
No dataset card exists. Required fields for any NLP/ML benchmark submission:
- Task definition with formal notation
- Data collection methodology and provenance
- Per-split statistics (size, ecosystem distribution, drift-pattern distribution)
- Known limitations and exclusion criteria
- License statement for each case's source evidence

### 7.2 Canonical split manifest (blocking)
No train/dev/test split exists. A benchmark paper must define which cases are the evaluation set. Currently all 65 verified_keep cases are in a single pool with no held-out test split. Required:
- `splits/eval.json` — the public eval set (IDs + slugs)
- Justified exclusions (e.g., runtime-pair cases excluded from the main leaderboard)

### 7.3 Baseline runner (blocking)
No code runs an LLM against the benchmark and produces a score. Required minimum:
- A script that, given an eval package and a model, runs each probe with the model replacing the client, compares output to `expected.json`, and reports per-case pass/fail and aggregate accuracy.
- At least one baseline result (e.g., GPT-4, Claude Sonnet, zero-shot).

### 7.4 Scoring schema beyond field equality (important)
The current oracle is binary: old-field-value matches or does not. For a paper, reviewers will ask:
- What fraction of cases have multi-assertion oracles?
- How is partial credit handled?
- How is the score normalized across ecosystems?

Currently all 65 verified_keep cases have single-assertion oracles. This is defensible but must be stated explicitly.

### 7.5 Experiment results table (blocking)
No experiment has been run. A benchmark paper without baseline numbers is a dataset paper at best, and a dataset paper still needs a task definition and at least one evaluation result.

### 7.6 DriftRL / AgenticRL environment (stated goal, does not exist)
If the paper claims a new RL environment:
- Gymnasium-compatible `DriftEnv` with `step()`, `reset()`, `observation_space`, `action_space`
- Mock replay of old/new version pair responses so the agent can probe without live binaries
- Reward function tied to the oracle assertions
- At least one rollout trace with a baseline agent

None of this exists. Building it requires non-trivial engineering before it can support a paper claim.

---

## 8. Summary Table

| Artifact | Exists | Quality | Paper-claimable |
|---|---|---|---|
| Case bank with 160 metadata entries | Yes | Production-grade schema | No — must report 60 claimable |
| 65 verified_keep cases with oracle | Yes | Solid | Yes, with honest per-ecosystem breakdown |
| 60 local-deterministic offline cases | Yes | Strong | Yes |
| Eval-pack generator (strips hidden/) | Yes | Tested, leak-checked | Yes |
| Metadata schema + validation | Yes | Tested | Yes |
| Ecosystem adapters (7 languages) | Yes | Mixed depth | Yes, with caveat |
| Dataset card | No | — | Blocking |
| Split manifest | No | — | Blocking |
| Baseline runner | No | — | Blocking |
| Experiment results | No | — | Blocking |
| Scoring schema beyond field equality | No | — | Important |
| AgenticRL / DriftRL environment | No | — | Not yet claimable |
| Mock replay mechanism | No | — | Not yet claimable |
| Ecommerce cases as offline benchmark | No | Documented leads | Not claimable offline |

---

## 9. Recommended Minimum Path to Submission

Given what exists, the minimum credible EMNLP/AAAI artifact path is:

1. **Declare scope honestly**: SilentDriftBench = 60 locally reproducible, multi-ecosystem, real-world library behavioral drift cases. Do not inflate with blocked or ecommerce cases.

2. **Write the dataset card** covering those 60 cases: collection method, provenance chain, per-ecosystem counts, oracle schema, known limitations.

3. **Define and freeze the eval split**: Pick 40–50 of the 60 as the held evaluation set; keep the rest as development/illustration. Write `splits/eval.json`.

4. **Implement a baseline runner** that takes an eval package folder, runs each `client/probe.{ext}` with a target LLM substituting some logic, compares to `expected.json`, and reports accuracy. Run at least one model.

5. **Report baseline numbers** (even if low; that is the point of a hard benchmark).

6. **DriftRL**: Either implement a minimal Gymnasium wrapper backed by the 60-case oracle, or drop it from the paper title and treat the paper as a benchmark-only paper. A paper claiming a new RL environment without any RL experiment will not survive review.

---

*This audit reports what can be independently verified from the committed codebase and case-bank metadata. It does not assess whether blocked cases could eventually be reproduced, whether the ecommerce leads have research value, or whether the task definition is novel. Those are separate questions for the authors.*
