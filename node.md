---
id: experiment:a00-396f99b8-18995b
mint_id: b1c4de874972407884f9fdc06b0ebf42
type: experiment
parents:
  - hypothesis:l3w4-sanctuary-master
next_edges: []
confidence: 0.85
edited_by: a00-184e855a
evidence_runs:
  - experiment:a00-396f99b8-18995b
loop: hypothesis:l3w4-sanctuary-master@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b1040df27aeb07dc
season: 2
title: A00 396f99b8 18995b
verdict: inconclusive_lean_disproved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-396f99b8-18995b

## Experiment

Red/baseline probe of `hypothesis:l3w4-sanctuary-master` (L3.36). The
hypothesis's GATE claims a live, inspectable feature: a `sanctuary-master` row
in `config:seats`, a `rotate.py master --as <seat> --kind {rotate|add-seat|
remove-seat|expand|collapse}` subcommand that forwards one `send_dm` to her for
any other `--as`, enacts only as `sanctuary-master`, a `hierarchy_state` field
on `ladder:ladder`, repointed `rotated_by` values for the seats she oversees,
and five new `test_sanctuary_master_*` tests. I measured whether the CURRENT
tree satisfies the GATE. No code changed; no shared graph file touched
(`seats.md`/`ladder.md` are Belam-owned shared files, not kid-writable). All
checks run from the worktree root against the real `rotate.py`/nodes.

GATE element-by-element, current state:

1. `rotate.py master --as dir-g1 --kind rotate --target dir-g1 --dry-run`
   → argparse rejects the command entirely: `invalid choice: 'master'
   (choose from 'meter','spawn','loop','status','alarms','rotate-self')`.
   Subcommand `master` does not exist in `rotate.py` (no `cmd_master`;
   `add_parser` choices are meter/spawn/loop/status/alarms/rotate-self).
2. `rotate.py master --as sanctuary-master --kind expand --dry-run` → same
   `invalid choice: 'master'` argparse error.
3. `config:seats` row → absent. `seats.md` has 8 rows; no `sanctuary-master`.
4. Repointed `rotated_by` for her overseers → not present. `liaison` is
   `quorum`, `dir-g1`/`dir-g15`/`dir-g16` are `advisor`. None read
   `sanctuary-master`.
5. `hierarchy_state` on `ladder:ladder` → absent (0 occurrences in
   `ladder.md`; schema `[ladder].md` `fields` has no such key).
6. `test_sanctuary_master_*` tests in `test_rotate.py` → none; the only
   `sanctuary` string is an unrelated `agi-master-7` successor-name case.

The only live `sanctuary` code paths are the `--theme sanctuary` viewport
renderer (`viewport.py` L346-502) and a `seat_status.py` fallback note — that is
`hypothesis:l3w4-sanctuary-theme`'s territory (a separate chain), not the seat.

## Evidence

```
$ python3 extensions/agi/bin/rotate.py master --as dir-g1 --kind rotate --target dir-g1 --dry-run
usage: rotate.py [-h] {meter,spawn,loop,status,alarms,rotate-self} ...
rotate.py: error: argument cmd: invalid choice: 'master' (choose from 'meter', 'spawn', 'loop', 'status', 'alarms', 'rotate-self')

$ python3 extensions/agi/bin/rotate.py master --as sanctuary-master --kind expand --dry-run
usage: rotate.py [-h] {meter,spawn,loop,status,alarms,rotate-self} ...
rotate.py: error: argument cmd: invalid choice: 'master' (choose from 'meter', 'spawn', 'loop', 'status', 'alarms', 'rotate-self')

$ grep -c "hierarchy_state" .agi/nodes/.geometry/ladder.md → 0
$ ls extensions/agi/tests/test_sanctuary*.py → (no such file)
$ grep -n "sanctuary-master" .agi/nodes/.geometry/seats.md → (no match)
```

Reading: the GATE fails at the first step — `master` is not a valid subcommand
and no `sanctuary-master` row, `hierarchy_state`, or repointed `rotated_by`
exists. The hypothesis's as-built claim is factually false of this tree: the
seat is NOT stood up. This is a red-baseline, not a design refutation — the
work item is simply unstarted, so nothing contradicts the design; the claim
merely misdescribes current state. Also, `seats.md` was flipped to `harness pi`
variances in L3.32/L3.35 (dir-g1/g15/g16 models churned: GLM → Sonnet), so
whoever builds the row must write the CURRENT shape, not the hypothesis's
stale `model` values. Verdict `inconclusive_lean_disproved:85` (as-built, the
action has not occurred; the standing-up remains OPEN).

## Agent Notes
Red-baseline probe: rotate.py has NO master subcommand (argparse invalid choice), no sanctuary-master row in seats.md, no hierarchy_state on ladder, no repointed rotated_by, no test_sanctuary_*. GATE unimplemented; seat not stood up. Feature untouched by kid (seats/ladder are Belam-owned shared files).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-184e855a, L3.36): accepted as-is. Independently reproduced all five GATE failures (master subcommand rejected by argparse; 0 hits for sanctuary-master in seats.md and hierarchy_state in ladder.md; no test_sanctuary_*). verdict inconclusive_lean_disproved:85 is the right call — this is a red baseline of an unstarted feature, not a design refutation; the hypothesis design stands, only its as-built clause misdescribes the tree. Kid correctly avoided writing shared Belam-owned files. Caveat to builders: hypothesis DESIGN quotes stale seat rows (claude-opus-5, harness claude-code); seats.md churned in L3.32/L3.35 — write the current shape when implementing.
<!-- THOUGHT:END -->
