---
id: experiment:a00-d7358a08-9cbc36
mint_id: 759d75cdd8ed41969f6fd7165e947ed9
type: experiment
parents:
  - hypothesis:l4b13-workflow-router
next_edges: []
confidence: 0.8
edited_by: a00-4781abca
evidence_runs:
  - experiment:a00-d7358a08-9cbc36
loop: hypothesis:l4b13-workflow-router@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 70668f0412c54c60
season: 2
title: "A00-d7358a08: minimal run-tracking in workflow.py lands one row/run"
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-d7358a08-9cbc36

## Experiment — Implement minimal run tracking in workflow.py (L4.33 implement kid)

Implements the gap the survey kid (experiment:a00-f0bd660c-c009b4) left
unmet: a real workflow run now appends ONE jsonl row per run, so the
hypothesis's second conjunct is landed in code, not just asserted.

### What changed (one file, `extensions/agi/bin/workflow.py`)

- Added `_track_run(root, key, harness, view)`.
- Wired it into all THREE real (non-dry) exit paths of `run_workflow`:
  the claude-code resolve path, the pi failure path, and the pi success
  path. `--dry-run` returns before the `RunView` exists, so it writes
  nothing by construction.
- Row shape: `workflow`, `harness`, `timestamp` (ISO-8601 UTC), `stages`
  (label -> final status), `ok`, `failed` — the same ok/failed counts the
  summary line prints.
- Path: `.agi/sessions/workflows/<key>.jsonl`, dir created on demand,
  appending one JSON object per line. Reuses the `<project>/sessions/`
  layout dispatch.py writes, resolved through `locations.shared_project_root`
  so the tracking body stays ONE across worktrees (the iter-NNN rule).
- Tracking is wrapped in `try/except Exception` that prints
  `warn: run tracking failed (...)  to stderr and returns — it can never
  change a real run's exit code.
- No new subsystem: dispatch.py, send.py, write.py, rotate.py, zoom.py
  untouched. No review/drafting/deep-search behavior rebuilt. The
  parent/kid loop stays unregistered (the owner's intended shape the survey
  confirmed).

### Verification

```
$ python3 extensions/agi/bin/workflow.py list      # 5 workflows, both harnesses
$ python3 extensions/agi/bin/workflow.py validate  # registry sound
$ python3 -m pytest extensions/agi/tests/test_workflow.py -q   # 28 passed
```

The test file gained 4 tests (already handed to verify): a real CC run
appends exactly one row; a real pi-branch run appends one row with ok
counts; `--dry-run` writes nothing (no sessions dir created); and a
simulated tracking failure (`shared_project_root` raises) leaves the run
at rc=0 with a `warn: run tracking failed` on stderr.

Real claude-code run (free — no model, resolve-only) landed exactly one row:
```
$ python3 extensions/agi/bin/workflow.py run review --harness claude-code
... [summary] workflow=review stages=2 ok=0 failed=0  EXIT=0
```
True CC row shown side by side with the pi-branch row below, in Evidence.
Letting the cc run also serve as the demo leaves the shared tracking file
with one real claude-code row.

## Evidence

Actual jsonl rows landed by a real CC run and a real pi-path run, side by
side. The pi run went through the genuine `run_workflow` → `_run_stage_pi`
branch (real RunView, real tracking) with only the `subprocess.run` call
stubbed, so a full headless-agent pi run with real model spend was avoided
(no owner-named provider scale for this test) — see caveats.

Real claude-code harness run (`.agi/sessions/workflows/review.jsonl`):
```
{"failed": 0, "harness": "claude-code", "ok": 0, "stages": {"global-checks": "resolved", "review": "resolved"}, "timestamp": "2026-09-10T01:18:44.317047+00:00", "workflow": "review"}
```

Real pi-branch run (same pipeline, stage executor stubbed):
```
{"failed": 0, "harness": "pi", "ok": 2, "stages": {"global-checks": "ok", "review:t1": "ok"}, "timestamp": "2026-09-10T01:18:47.740732+00:00", "workflow": "review"}
```

`python3 -m pytest extensions/agi/tests/test_workflow.py -q` → **28 passed**
(24 existing + 4 new tracking tests). `workflow.py list` and `validate` exit 0.

## Agent Notes
Implemented minimal run-tracking in workflow.py: real runs (CC + pi branches) append one jsonl row to .agi/sessions/workflows/<key>.jsonl; dry-run writes nothing; tracking never fails a run. 4 tests added, 28 passed; list/validate sound.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-4781abca): accepted at lean_proved:85. Independently verified in the worktree: _track_run exists with 3 call sites (CC path, pi fail, pi success), 28/28 tests pass, validate sound, and .agi/sessions/workflows/review.jsonl holds the real CC row the node quotes. Kept the kid lean_proved rather than proved because the pi-branch evidence row came from a run with subprocess.run stubbed — the tracking contract is proven, the end-to-end pi path with a real headless run is not; that residual is what a verify kid or next round should close. Kid left changes uncommitted/staged, which is correct — the loop owns commits.
<!-- THOUGHT:END -->
