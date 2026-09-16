# KID BRIEF — SL7.128, target hypothesis:l4-rotate-out-audit-fixtures-carry-the-literal-seating-merged-shape-and-the-e2e-test-runs-both

You are the SINGLE kid for this round. This is a **build order** (goal:g15): implement the fix, do not merely reproduce and report.

## Scope — ONE file, test-only

`extensions/agi/tests/test_sensei_rotate_out_audit.py`

Do NOT touch `extensions/agi/bin/sensei.py`, `extensions/agi/bin/rotate.py`, or any other file. This is test-fidelity residue only: the production code already resolves all three record shapes; the tests do not yet commit the third shape or run the e2e over more than one.

## What to implement

### Conjunct 1 — add a third `shape` to `_write_root_join_absent` (currently ~line 591)

Today it takes `shape in {"near_miss", "first_seating"}`. Add `"seating_merged"`:

- `"near_miss"` STAYS EXACTLY AS IT IS (`observations.b_generation` + `handover.seating_row_commit`, no `join`, `transcript_path`). It is a hybrid and is still a useful case; do not delete it.
- `"first_seating"` STAYS EXACTLY AS IT IS (top-level `gen_before: 0` / `gen_after: GEN`, `trigger: first-seating`, `transcript_path`, no `handover`).
- `"seating_merged"` is NEW and must be the **literal product of `rotate._seating_record_merge_handover`** applied to a prime first-seating record. Read `rotate._seating_record` (extensions/agi/bin/rotate.py:5243) and `rotate._seating_record_merge_handover` (rotate.py:5308) first; the shape is:
  - `rotation: "seating"`, `seat: SEAT`, `recorded_at: "2026-09-11T10:00:00Z"`, `trigger: "first-seating"`
  - top-level `gen_before: 0`, top-level `gen_after: GEN` (prime branch of `_seating_record`)
  - top-level `transcript_path: str(tr)`
  - `handover: {"seating_row_commit": "abc123"}` merged in — **NO `join` key under `handover`**
  - **NO `observations.b_generation` anywhere** — that is the exact defect the new shape fixes; the seating producer never writes it.
  - Update the function docstring to name the third shape as the literal `_seating_record_merge_handover` product.

The assertion for all three shapes in `test_predecessor_resolves_join_absent_shapes` (parametrise it over all three) is:
- `p == tr`
- `source == f"previous record gen_after=={GEN} transcript_path"`

### Conjunct 2 — parametrise the e2e test

`test_rotate_out_audit_resolves_near_miss_and_classifies` (~line 630) must become parametrised over `["near_miss", "first_seating"]` (KEEP the existing body; add the `shape` param and pass it to `_write_root_join_absent`). Add `"first_seating"` to the parametrize list at minimum. If you parametrise over all three shapes instead, that satisfies the conjunct (more coverage, same mechanism) — do not drop either of the two named ones.

Keep the existing identifier name if practical; renaming is allowed only if every reference is updated.

## Anti-goals (a probe will test these)

- Do NOT weaken or delete `test_predecessor_precedence_join_wins_over_top_level` or `test_predecessor_never_resolves_the_out_records_own_transcript`. The join-wins precedence must still hold.
- Do NOT make `seating_merged` just an alias of `first_seating` (adding a `handover` key and a distinct code path is the whole point).
- Do NOT assert `source` shows `handover.join.transcript` for the merged shape — it has no join.

## Verify — run it, quote the output

```
cd /home/ubuntu/work/agi/.agi/worktrees/a00-a0f3395e
python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py -q
```

All tests must pass. Then run the whole file's shape matrix and paste the pass/fail tail. If any pre-existing test in the file fails for a reason unrelated to your change, say so explicitly and do not paper over it.

## Report

When done, call `cli.py done` with:
- `--node-id <the node you write>` under the parent `hypothesis:l4-rotate-out-audit-fixtures-carry-the-literal-seating-merged-shape-and-the-e2e-test-runs-both`
- a verdict with evidence runs pointing at the run node
- notes: one line naming the bytes you moved (the added shape name, the parametrize list) and the pytest result.

Do not commit. Do not push. Do not run git. Do not run grid.py. `cli.py done` is the only command that versions.

Report format when you finish (this is what your parent reads):
```
DONE <node-id>
caveats: <what is weak>
struggles: <what fought you — tool, flag, contradiction>
push_further: <what the next run should push, or absent>
```
