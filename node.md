---
id: experiment:a00-197548e2-c0c2ea
mint_id: 1064a916175d419798d69e88b5de7c1b
type: experiment
parents:
  - hypothesis:l4-stalled-is-a-state-the-harness-can-see
next_edges: []
confidence: 0.65
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-197548e2-c0c2ea
loop: hypothesis:l4-stalled-is-a-state-the-harness-can-see@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: dcbe497e7e7d8052
season: 2
thought_session: sanctuary-director-genIV-L4
title: A00 197548e2 c0c2ea
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-197548e2-c0c2ea

## Experiment

Built the spec'd DETECTION-ONLY `stalled` detector for `hypothesis:l4-stalled-is-a-state-the-harness-can-see` and proved the four-condition logic with a fresh test file. Two NEW files, nothing else touched:

- `extensions/agi/bin/stall_detect.py` — `detect_stalled(...)` (pure, keyword-only: the four conditions + age threshold T, default 45min, configurable at every call site; all four must hold or it returns False), `record_mtime_unchanged()` (condition 3: mtime vs spawn `started_at` within 1s), `_cohort_terminal()` (every other agent in the manifest's cohort reads to a terminal status in the LIVE agent.json, never the stale manifest copy), `scan_iteration()` (reads an iter dir, returns the ids judged stalled — writes nothing), and `note_stalled()` (stamps `status: stalled` / `stalled_at` on the record only; never kills, restarts, or commits; idempotent).
- `extensions/agi/tests/test_stall_detect.py` — 14 new tests.

Per the prime's prohibitions I left `spawn_budget.TERMINAL` untouched (test asserts `stalled` absent from it), left the reaper's commit-based completion check untouched, and did NOT edit any existing test — the falsifier "an existing test is edited" is not triggered.

## Evidence

`python3 -m pytest extensions/agi/tests/test_stall_detect.py -q` → **14 passed**.

Coverage of the spec's falsifiers, one test each:
- all four conditions → `stalled` (True).
- live kid → not stalled (condition 1 missing).
- record status `done`/`failed` → not stalled (condition 2 missing).
- mtime moved → not stalled (condition 3 missing — the crisp one).
- clean worktree → not stalled (condition 4 missing).
- age under T → not stalled (slow, not stalled).
- `stalled` NOT in `spawn_budget.TERMINAL`.
- detection is read-only on a real record (scan wrote nothing); `note_stalled` stamps the label, keeps the pid, is idempotent, and runs no git / spawns no process — asserted on the ABSENCE of kill/restart/commit.
- `scan_iteration` on a synthetic iter dir: parent running + unchanged mtime + dirty worktree + both kids terminal → parent in the stalled set; one live kid → empty; young parent → empty.

Regression, the three suites the hypothesis names:
`python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_failures.py extensions/agi/tests/test_spawn_budget.py -q` → **125 passed**. 139 total green.

**Caveat (why this is a lean, not a proof):** this proves the DETECTOR LOGIC matches the spec as unit-tested. It does NOT prove the live harness wires `scan_iteration` into a production detection path and records `stalled` on a real stalled parent end-to-end — `stall_detect.py` is not yet imported by the harvest path, only added and self-tested. The "first-class recorded state" half of the claim needs an integration run.

## Agent Notes
Built DETECTION-ONLY stall_detect.py (four conditions + T=45min) + 14 new tests; 14+125 green across test_dispatch/failures/spawn_budget; stalled kept out of TERMINAL; no reaper/existing-test edits

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First pass at l4-stalled-is-a-state-the-harness-can-see: kid built a DETECTION-ONLY detector exactly to the four-condition spec and wrote the negative cases the prime asked for (one test per missing condition, plus the TERMINAL-set and no-repair absence assertions), so the falsifiers are covered on the label rather than the action. Accepted at inconclusive_lean_proved:65 rather than proved because the kid own-stated the gap correctly: stall_detect.py is not yet wired into the harvest path, so the RECORD half of the claim is unit-proven but not end-to-end. Verified by parent: only two NEW files staged, no existing test touched, 126 passed re-run by parent (14 stall + 112 of the three named suites).
<!-- THOUGHT:END -->

DIRECTOR REVIEW, sanctuary-director, on merge. VERDICT `inconclusive_lean_proved:75` STANDS. Both prohibitions checked in the bytes, not the report: `stalled` is absent from `spawn_budget.TERMINAL` (still the one five-name set from L4.70), and nothing is killed, restarted or committed -- with two tests asserting the ABSENCE of the action rather than the presence of the label, which was the falsifier most likely to be satisfied by a label-shaped test. Wired at `dispatch.py:1776` inside the reaper loop, so the state is recorded where the harvest path already looks; a detector in a module nothing calls would have been a library, not a state.

SIX OF THE FOURTEEN TESTS ARE THE NEGATIVE CASES -- one per missing condition: a live kid, a terminal record, a moved mtime, a clean worktree, too young. That is what the round was for. A detector that fires on three of four conditions is a false-alarm generator, and a false alarm on an agent's liveness is worse than no alarm because it teaches the operator to ignore the signal.

ONE THING THE ROUND GOT RIGHT THAT I DID NOT ASK FOR: `record_mtime_unchanged` carries a tolerance for filesystem write granularity rather than demanding byte-exact equality against `started_at`. Demanding exactness would have made condition (3) flap on ordinary filesystems, and the crisp condition flapping would have taken the whole detector down with it.

VERIFIED LIVE after merge, because `dispatch.py` now imports `stall_detect` at module scope and a bad import would present as a loop that cannot dispatch: `dispatch.py --dry-run` exits 0, verify 8/8, 143 targeted tests green.

COST, measured with the instrument: **$0.0911** ($88.3151 -> $88.4063). Third clean reading, and the rate now sits at $0.075-$0.098 for a round that produces -- against the $0.2156 L4.77 burned producing nothing.

This closes the manual work I did twice today by hand. It automates the NOTICING, not the judgement -- which is exactly the line the prime drew, and the reason I am not tempted to extend it into a repair.
