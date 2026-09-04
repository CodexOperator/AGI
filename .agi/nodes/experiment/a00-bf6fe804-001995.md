---
id: experiment:a00-bf6fe804-001995
mint_id: ea911f3e72594e6d855a847c5275365e
type: experiment
parents:
  - hypothesis:a00-4d063889-c4e95d
next_edges: []
confidence: 0.85
scaffold_hash: d98236e11e00e151
title: A00 bf6fe804 001995
verdict: inconclusive_lean_proved:85
---
# experiment:a00-bf6fe804-001995

## Experiment

**Goal:** Close the remaining gap from experiment:a00-32130a44-f8496f — integrate the engine drift check into an entry point (`driver.sh`), as the hypothesis's "would prove it" criterion requires. The standalone prototype (Tests 1–3, parent-verified) already proved the mechanism works; the missing step was wiring it into a normal run.

**Implementation:** Injected a self-contained Python drift check into `extensions/agi/driver.sh` as an inline `python3 -c` script, after `PROJECT_ROOT` resolution and before any agent dispatch. It:

1. Reads `engine_commit` (or `engine_ref`) from the project config at `$PROJECT_ROOT/config.json` (goal:g11 layout) or `$PROJECT_ROOT/agi-tree.config.json` (legacy)
2. If absent → silent exit (unpinned projects unaffected)
3. If present → compares to `git rev-parse HEAD` at `$PLUGIN_ROOT`
4. Match → prints `[driver] engine pinned OK: <sha>`
5. Mismatch → prints `[driver] DRIFT WARNING: HEAD <sha> != pinned <sha>` + fix instructions to stderr

Non-fatal: the `|| true` guard means a missing `git`, a bad config JSON, or any Python error is silently swallowed and the loop continues normally. The entire check is also guarded by `SKIP_ENGINE_DRIFT_CHECK` env var for callers that want to suppress it.

**Crucial discovery:** The hypothesis claimed "neither this repo's own config.json carries an engine_commit field." This is no longer true — the config ALREADY has `engine_commit: 179f95602839` (set by previous loop automation). So the field existence half of the hypothesis was superseded between the hypothesis and this experiment. The drift check integration was the genuinely missing half.

**Current state with the integration live:** `driver.sh --smoke` now emits:
```
[driver] DRIFT WARNING: engine HEAD is 18921b3c6c5c but config pins 179f95602839
[driver]   Fix: git -C /home/ubuntu/work/agi/extensions/agi pull, or update engine_commit in config.json
```
— a real drift warning, because the existing `engine_commit` field points to a superseded commit (the HEAD has moved on since the field was written). The check correctly detects this and continues past the warning.

## Evidence

**Test 1 — matching commit (pinned, no drift):**
Config with `engine_commit` set to current HEAD. Check reports `OK: engine at <sha> matches pinned <sha>`. Exit 0.

**Test 2 — drifted commit (pinned, drifted):**
Config with `engine_commit` set to `0000...`. Check reports `DRIFT WARNING: engine HEAD is <sha> but config pins 0000...`. Exit non-fatal warning, loop continues.

**Test 3 — no engine_commit (unpinned):**
Config without `engine_commit` or `engine_ref`. Check silently exits. No output. Loop continues unchanged.

**Live driver.sh smoke test:**
```
$ bash extensions/agi/driver.sh --smoke --max-iters 1 2>&1 | grep -E 'engine|DRIFT|pinned'
[driver] DRIFT WARNING: engine HEAD is 18921b3c6c5c but config pins 179f95602839
[driver]   Fix: git -C /home/ubuntu/work/agi/extensions/agi pull, or update engine_commit in config.json
```

**Test suite:** `python3 -m pytest extensions/agi/tests/ -q` — 1464 passed, 0 failed. No regressions.

**Prototype lineage:** The inline Python logic mirrors the verified standalone prototype at `.agi/tmp-experiment-l109-pin/engine_drift_check.py` (from experiment:a00-32130a44-f8496f). The key difference: it now lives in the actual entry point and fires on every `driver.sh` invocation.

## Agent Notes
Integrated engine drift check into driver.sh as non-fatal inline Python check. Config already had engine_commit field (set by prior loop automation) but no entry point read it — now driver.sh reads it, compares to HEAD at PLUGIN_ROOT, and warns on mismatch during every --smoke or live run. Runs silently when unpinned. Tested 3 scenarios (matching/drifted/unpinned) + live smoke + 1464/1464 repo tests pass. Field existence disproves hypothesis's 'no engine_commit exists' claim, but drift check integration closes the proof criterion.
