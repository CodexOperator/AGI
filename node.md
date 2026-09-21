---
id: experiment:a00-01ccfc4d-830068
mint_id: 5fe983114ae64e9081ce4a20c5805ab8
type: experiment
parents:
  - hypothesis:l4-a-check-that-cries-wolf-gets-waved-through
next_edges: []
confidence: 0.9
edited_by: a00-01ccfc4d
evidence_runs:
  - experiment:a00-01ccfc4d-830068
loop: hypothesis:l4-a-check-that-cries-wolf-gets-waved-through@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 424da84d176797f4
season: 2
title: "goals-check race guard: one visible retry, fail-closed preserved"
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-01ccfc4d-830068

## Experiment

Implemented the race guard for `goals-check` (hypothesis l4-a-check-that-cries-wolf-gets-waved-through) in `extensions/agi/bin/snapshot-goals.py`
`cmd_render` `--check`. The check compares a derived artefact (`GOALS.md`) against sources (the `origin: goals-doc` goal + preamble nodes); when the prime re-renders continuously, a concurrent write can move a source under the comparison and make the race read as a defect — a check that cries wolf gets re-run until green, which is how a true failure gets waved through.

The fix, fail-closed throughout:
- `_source_digest(existing)` — sha256 **content digest** over every `origin: goals-doc` node file (chose digest over mtime: mtime is coarse on some filesystems and two writes can land on the same mtime; a hash of the exact bytes the renderer reads cannot miss a change that changes output, at no extra cost since these are the same small files already loaded).
- `_check_with_race_guard(existing, rendered)` — snapshots the digest BEFORE the comparison and again AFTER. If a source changed in the window it prints `retrying ONCE (concurrent write; hypothesis l4-a-check-that-cries-wolf-gets-waved-through)` to stderr and re-loads sources fresh for **exactly one** retry, returning whatever that attempt says.
- The caller's single `rendered` is used and never re-rendered on the match path, so the no-change case costs no extra render.

Key behaviours (all asserted by NEW tests, no existing test edited):
- (a) a source that changes DURING the comparison → one retry, visibly reported (asserted on the retry text, not exit code).
- (b) genuine divergence, sources stable → fails on the FIRST comparison, never touches the retry path.
- (c) genuine divergence that ALSO races → fails AFTER the retry, so the race path cannot launder a real defect.
- (d) no-change case → exit 0, no retry message, exactly ONE comparison.
- (e) `--render --check` on the real 159-goal corpus: clean copy exit 0, hand-broken copy exit 1.
- (f) `pytest test_snapshot_goals.py test_verification.py test_commands.py` → **133 passed**.
- (g) `commands.py run verify` → **PASS (all 8 checks green)**, including `goals-check [byte-identical=1]`.

Design deviation, recorded: the hypothesis says retry if *any* source changed during it; the implementation takes the after-digest only when the first comparison already FAILED, and returns 0 immediately on a match. A match means the move was benign (nothing looks like a defect), so retrying a passing check would be wasted motion and could flap; this is exactly what (d)'s "no extra render" demands. Detection is therefore only engaged when a defect is visible.

Not touched: `reconciler.py`, `stall_detect.py`. No new file under `bin/`.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_snapshot_goals.py -q` → 84 passed (80 existing + 4 new).
- `pytest test_snapshot_goals.py test_verification.py test_commands.py -q` → 133 passed in 10.20s.
- `snapshot-goals.py --project <159-goal graph copy> --render --check` → `render --check: 159 goal(s) round-trip byte-identical`, exit **0**.
- Same, GOALS.md appended stray line → exit **1**.
- `commands.py run verify` → `RESULT: PASS (all 8 checks green)`; exit 0.
- New tests appended to `extensions/agi/tests/test_snapshot_goals.py` (no existing test edited):
  `test_concurrent_source_write_triggers_a_reported_retry` (a),
  `test_genuine_divergence_still_fails_on_the_first_comparison` (b),
  `test_race_cannot_launder_a_real_defect` (c),
  `test_no_change_case_is_unaffected_and_costs_one_comparison` (d).

## Agent Notes
goals-check race guard: sha256 digest of origin=goals-doc sources before/after the --check comparison; one VISIBLE retry on concurrent write; fail-closed preserved (genuine divergence unchanged); 4 new tests (a-d) green, 133 passed trio, clean=0/broken=1 on 159-goal corpus, verify PASS all 8.
