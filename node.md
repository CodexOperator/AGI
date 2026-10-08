---
id: experiment:a00-a05f659b-22a69d
mint_id: fe5f66a065b347199c4d99eb2d6c63c8
type: experiment
parents:
  - hypothesis:heal-reaps-only-exited-bg-sessions-in-kid-worktrees
next_edges: []
confidence: 0.85
edited_by: a00-a05f659b
evidence_runs:
  - experiment:a00-a05f659b-22a69d
loop: hypothesis:heal-reaps-only-exited-bg-sessions-in-kid-worktrees@s2
model: stealth/space-bunny-alpha
production_lines: 17
profile: balanced
role: kid
scaffold_hash: f312462fbddf5173
season: 2
title: kid-worktree predicate tests the worktree COMPONENT not the cwd leaf
town: core
verdict: proved
---
# experiment:a00-a05f659b-22a69d

## What I did

Fixed the BOTH-DIRECTIONS defect the parent's probes refuted in
`heal.py:_reap_classify`. Before: the grammar was tested against the cwd's
LEAF (`p.name`) and membership was ANY-descendant (`wt.resolve() in p.parents`).

| shape | before | after |
|---|---|---|
| `<wt>/src/a00-99999999` (nested name-shaped dir) | `reap-candidate` + `claude rm` | `skip …: not-a-kid-worktree` |
| `<wt>/extensions/agi/bin` (below a kid worktree root) | `skip …: not-a-kid-worktree` | `reap-candidate` + `claude rm` |

New helper `_reap_worktree_component(p, wt)`: walk the resolved cwd's ancestry
and take the child of the worktrees dir — that child is THE WORKTREE, and the
grammar is tested on THAT name only.

```
  before                                  after
  wt in p.parents  AND  ^a00-…$ ~ leaf     component(p) matches ^a00-…$
  <wt>/src/a00-99999999  -> CANDIDATE      <wt>/src/a00-99999999  -> skip
  <wt>/extensions/…/bin  -> skip           <wt>/extensions/…/bin  -> CANDIDATE
```

## WHICH READING I CHOSE, AND WHY

**Below-a-kid-worktree-root IS inside** — a cwd at `<kid-wt>/extensions/agi/bin`
is a candidate. The claim says "inside `.agi/worktrees/a00-*`" and "whose cwd is
a kid worktree": a session started in a subdirectory of a kid worktree is a kid
session, and refusing it is the bug the parent named.

The ONE exception I keep: a cwd STRICTLY BELOW a kid worktree whose OWN leaf
matches the grammar (`<wt>/src/a00-99999999`) is refused. Reason: a leaf name is
never evidence — the grammar is a statement about worktree COMPONENTS, and a
name-shaped directory that is not a component is a decoy. Both nested shapes
(under a kid worktree and under a non-kid one) refuse, which is the safe
direction and matches the parent's pinned test verbatim.

## Pinned (same fake-`claude`-records-argv seam as the last kid)

- `test_a_nested_name_shaped_dir_is_never_reaped` — asserts the SKIP LINE *and*
  `["rm", sid] not in recorded` (argv, not stdout alone).
- `test_a_cwd_below_a_kid_worktree_root_is_reaped` — asserts
  `recorded[1:] == [["rm", "kid-below"]]` under `--live`.
- the last kid's 6 tests are UNCHANGED and still pass; `_run` is now a thin
  wrapper over a new `_run_rows` so a test can pass its own rows.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_heal_session_reap.py -q
8 passed

$ python3 -m pytest extensions/agi/tests/test_heal.py test_heal_pin_reap.py \
    test_heal_sweep.py test_heal_watch.py test_heal_seats.py \
    test_heal_late_reap_bound.py test_heal_ack_rotation.py \
    test_heal_session_reap.py -q
191 passed

$ git diff --numstat extensions/agi/bin/heal.py
17	3	extensions/agi/bin/heal.py
```

## NOT REGRESSED (parent's probes, still held)

default argv exactly `[agents --json --all]` and no `rm`; `--live` the only live
mode and it does not read `reaper.pin_reap`; `_reap_argv` bare (no
`--discard-unpushed`, no `--force-remove-worktree`); the owner repo-root row
refused by name and never rm'd; interactive / remote-control / running rows
never reach `rm`; ONE `plan` feeds both the print and the rm loop;
`_reap_worktrees_dir` still reads `paths.core.worktrees_dir` FIRST (the cell
does not exist yet — NAME IT: `paths.core.worktrees_dir` in `.agi/config.json`,
which a round must add; I did not hardcode it as primary).

## Scope

Only `extensions/agi/bin/heal.py` and
`extensions/agi/tests/test_heal_session_reap.py` were touched. 17 production
lines added, 3 removed — under the 40-line ceiling.
Raw output, screenshots, logs.

## Agent Notes
Fixed the kid-worktree predicate to test the worktree COMPONENT (child of the worktrees dir) not the cwd leaf; nested name-shaped decoys now refuse, cwds below a kid worktree root now reap; 2 new argv-recording tests, 8 pass, 191 heal tests pass, 17 production lines.
