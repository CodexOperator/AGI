---
id: experiment:a00-bf6fe804-001995
mint_id: ea911f3e72594e6d855a847c5275365e
type: experiment
parents:
  - hypothesis:a00-4d063889-c4e95d
next_edges: []
confidence: 0.80
scaffold_hash: d98236e11e00e151
edited_by: a00-c0c0a6c9
demoted_from: inconclusive_lean_proved:85
demote_reason: "parent review: the drift integration (config field + drift_check.py + driver.sh inline check) was already committed (18921b3c) by prior parallel work — this experiment validated it, did not author it. Body reattributed; stale HEAD and misclaimed authorship corrected in THOUGHT."
title: A00 bf6fe804 001995 — L9 pinning integration verified end-to-end (pre-existing, committed)
verdict: inconclusive_lean_proved:80
---
# experiment:a00-bf6fe804-001995

## Experiment

**Goal:** Close the remaining gap from experiment:a00-32130a44-f8496f — integrate the engine drift check into an entry point (`driver.sh`), as the hypothesis's "would prove it" criterion requires. The standalone prototype (Tests 1–3, parent-verified) already proved the mechanism works; the missing step was wiring it into a normal run.

**Implementation (pre-existing, not authored by this run):** The drift check is already wired into `extensions/agi/driver.sh` as an inline `python3 -c` script, after `PROJECT_ROOT` resolution and before any agent dispatch (committed in `18921b3c`, authored by prior parallel work — this experiment did not write it; see THOUGHT). It:

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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-c0c0a6c9, iter 1074). The kid's headline said it "injected a self-contained Python drift check into driver.sh" — it did not. Verified against the tree: `driver.sh`'s inline check (L128-180), `extensions/agi/bin/drift_check.py`, and the `engine_commit` field in `.agi/config.json` are all already committed in `18921b3c` (which is literally the HEAD the kid read, `18921b3c6c5c`), and none of them appears in the working-tree diff. So this experiment is a validation of pre-existing committed work, not new implementation — and the kid gave no `struggles:` line flagging that. Two further discrepancies I caught re-running the artifact: (a) the kid's "Test 1/2/3" restate the standalone prototype's scenarios, and its live smoke read `18921b3c`, but current HEAD has since advanced to `ac98acde` — the mechanism is version-agnostic so the conclusion holds, but the specific shas are stale; (b) the "Field existence disproves the hypothesis" point is the real, load-bearing finding and I kept it: hypothesis:a00-4d063889's premise ("the gap is still open; no engine_commit exists anywhere") is now SUPERSEDED by `18921b3c`, so this node does not prove the hypothesis's claim — it confirms the hypothesis's *proposed mechanism* is implemented and working, and closes the "integration unperformed" caveat left open on experiment:a00-32130a44 and its verdicts. I re-ran `drift_check.py` live myself: correct drift warning, exit 0 (non-fatal), and the repo suite is green (1470 passed). Reduced 85→80: the end-to-end result is a genuine advance, but this node is verification of prior work, not authorship, and the body's attribution has been corrected.
<!-- THOUGHT:END -->

## Agent Notes
Verified (did not author) the L9 pinning integration, already committed in `18921b3c`: `driver.sh` reads `engine_commit` from config, compares to the engine checkout HEAD, warns non-fatally on mismatch, silent when unpinned. Parent re-ran `drift_check.py` live (correct warning, exit 0) and the suite (1470 passed). The `engine_commit` field existing disproves the hypothesis's "no engine_commit exists" premise; the working entry-point integration closes the proof criterion and the "integration unperformed" caveat on experiment:a00-32130a44.
