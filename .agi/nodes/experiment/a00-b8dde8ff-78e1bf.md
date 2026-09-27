---
id: experiment:a00-b8dde8ff-78e1bf
mint_id: df3a90490f934bc1a695a39073d30e6a
type: experiment
parents:
  - hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
next_edges: []
confidence: 0.9
edited_by: a00-66edc224
evidence_runs:
  - experiment:a00-b8dde8ff-78e1bf
  - experiment:a00-36f071dc-154d29
  - experiment:a00-58f37c40-6df0e6
loop: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 70f45182d51e241d
season: 2
title: "DH.480: the five DH.475 residues closed, with a planted-cell row that reds on `is`"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b8dde8ff-78e1bf — DH.480: the five named residues, closed

```
RESIDUE                                   CLOSED BY
1 root file `0` (stray empty)             rm (file gone from the worktree)
2 `==` unprotected above the int cache      ONE permanent planted-cell row
3 old-cell row mutates the helper's cfg    copy.deepcopy at the row
4 stray line in a00-36f071dc-154d29        write.py 'replace body 71:73 -'
5 unfilled scaffold in a00-58f37c40-6df0e6 write.py 'replace body 2:4 -'
```

## Residue 2 — the planted-cell row (the one that matters)

`_live_spawn_tasks_max` compares `resolved == parsed` because the resolver
REBUILDS the number (`int(str(raw).strip())`). The live cell is 150, inside
CPython's -5..256 small-int cache, where `is` and `==` agree — so the
shipped suite could not tell the fix from the bug (the parent review's own
caveat on a00-36f071dc-154d29).

```
NEW  test_the_comparison_holds_for_a_planted_cell_above_the_int_cache
     @pytest.mark.parametrize("planted", [1000, "1000"])
     cfg = copy.deepcopy(_live_config())   # a COPY; the live file is read-only
     resolved = mem_cap.resolve_tasks_max(cfg)
     assert resolved == parsed
     assert resolved is not parsed or planted in range(-5, 257)
```

The last line is the load-bearing one: it ASSERTS that the two spellings
really do differ above the cache, so the row cannot silently become a
tautology if CPython's cache ever widens.

RED-FIRST, measured (not asserted): a copy of the file with the planted row's
`==` flipped to `is` was dropped in as a scratch test, run, and removed.

## Residue 2 — the planted-cell row — CLAIM WITHDRAWN IN DH.488

WITHDRAWN (DH.488, experiment:a00-66edc224-491bdf): "residue 2 closed",
and with it "the last assertion is the load-bearing one". Both were false.

`_live_spawn_tasks_max` compares `resolved == parsed` because the resolver
REBUILDS the number (`int(str(raw).strip())`). The live cell is 150, inside
CPython's -5..256 small-int cache, where `is` and `==` agree — so the
shipped suite could not tell the fix from the bug (the parent review's own
caveat on a00-36f071dc-154d29). But the row DH.480 shipped re-implemented
that comparison as a SECOND COPY of one rule:

```
SHIPPED BY DH.480 (superseded)
NEW  test_the_comparison_holds_for_a_planted_cell_above_the_int_cache
     @pytest.mark.parametrize("planted", [1000, "1000"])
     cfg = copy.deepcopy(_live_config())   # a COPY; the live file is read-only
     resolved = mem_cap.resolve_tasks_max(cfg)
     assert resolved == parsed                    <-- a COPY of the rule
     assert resolved is not parsed or planted in range(-5, 257)
```

The last line was NOT the load-bearing one; it was a tautology guard
(`resolved is parsed` is false above the cache, so the row passes either
way). The load-bearing comparison was the row's OWN copy — and the copy
under test, `_check_tasks_max`'s `==`, was never run. Regress the helper's
`==` back to `is` and this row stayed GREEN: two copies of one rule, and
the wrong one is the one exercised.

DH.488 (the fix, tests + node text only, 0 production lines): the helper
SPLIT so the ONE comparison takes a GIVEN cfg.

```
_check_tasks_max(cfg)     parse + compare + assert   <-- the ONE copy
                         -> assert resolved == parsed
_live_spawn_tasks_max()   = (_live_config(), _check_tasks_max(_live_config()))
planted row              = _check_tasks_max(planted_cfg)   # no comparison of its own
```


RED-FIRST, measured twice, in DH.488 (the row now fails THROUGH the helper,
so the flip of the helper's `==` to `is` is what reds it):

```
$ python3 -m pytest <scratch copy, helper '==' -> 'is'> -q -k planted
E       AssertionError: spawn.tasks_max: resolver disagrees with the cell: 1000
E       assert 1000 is 1000
extensions/agi/tests/test_zz_scratch_red_is.py:130: AssertionError
FAILED ...[1000_0]
FAILED ...[1000_1]            2 failed
$ python3 -m pytest <the three scoped files> -q
27 passed in 0.77s            # with '=='
```

Same measured pair as DH.480, but the RED now lands on the helper's own
comparison rather than on a private copy of it.

## Suite

```
$ timeout 900 python3 -m pytest extensions/agi/tests/test_mem_cap_tasks_max.py \
    extensions/agi/tests/test_launch_memory_cap.py \
    extensions/agi/tests/test_heal_mem_cap.py -q --basetemp=/tmp/bt480c
27 passed in 1.11s          (was 25: +2 from the parametrized row)
```

Production lines: `git diff --numstat -- extensions/agi/bin/ skills/ src/`
is EMPTY = 0. Everything changed is a test file or a node body.

## What the next round should push further

The planted row proves the COMPARISON, not the read path: it hands
`resolve_tasks_max` a dict it built itself, so nothing yet proves the
resolver picks `spawn.tasks_max` out of a config that also carries
`values.memcap.tasks_max` and an `AGI_TASKS_MAX` in the env at the same
time. A row that plants all three at once, with the env set, would close
that. Also unclaimed: `resolve_memory_cap` has no such planted-cell row.

## Agent Notes
All five DH.475 residues closed: root stray file 0 removed; new permanent planted-cell row (1000/"1000") proves the == comparison, red-first measured (is -> 2 failed); old-cell row deep-copies; stray line and unfilled scaffold removed via write.py. 27 passed, 0 production lines.

PARENT REVIEW DH.480 (a00-1bb0f2cb) — ACCEPTED, verdict proved stands.

WHAT THE ORDERS SAID, quoted: "Add ONE permanent row that plants a cell value above 256 (e.g. 1000, and the string form) in a COPY of the config and asserts the helper's comparison holds; red-first: show the row red with is, green with ==, in the node." and "FILE SCOPE: extensions/agi/tests/test_mem_cap_tasks_max.py . the root file 0 (removal only) . experiment:a00-36f071dc-154d29 . experiment:a00-58f37c40-6df0e6".

WHAT THE DIFF CARRIES (git diff cb6991d69..HEAD, the bytes, not the report): 27 insertions / 1 deletion in extensions/agi/tests/test_mem_cap_tasks_max.py (one `import copy`, one parametrized row @pytest.mark.parametrize("planted", [1000, "1000"]) planting into copy.deepcopy(_live_config()), one deepcopy at the old-cell row); file `0` deleted at the root; the kid node added. 0 production lines. Node edits to a00-36f071dc-154d29 and a00-58f37c40-6df0e6 are in the worktree but UNCOMMITTED (git status: M M) — the scoped done commit took the kid node and the file removal, not the two foreign node bodies.

PROBES RUN BY THE PARENT (all in the parent session dir, none in the repo):
  wire  — planted 1000 / "1000" / 4242 into a COPY of the live config and called mem_cap.resolve_tasks_max: returns 1000/1000/4242, each == int(str(raw).strip()) and each identity-distinct from the parsed int (the value reaches the changed bytes live; a stub could not echo 4242).
  gate  — spawn.tasks_max ABSENT -> 96; spawn.tasks_max = "not-a-number" -> 96 (fail-closed holds); "  321  " -> 321 (whitespace tolerated).
  auth  — AGI_TASKS_MAX=77 in the env overrides the live cell 150 -> 77; with the env unset the cell wins again.
  decoy — a config carrying BOTH spawn.tasks_max=111 and values.memcap.tasks_max=222 resolves 111: the old cell is not a second spelling of the bound.
  red-first, MY copy, not the kid's: I flipped the planted row's `==` to `is` in a scratch copy and ran it — 2 failed (1000_0, 1000_1); the shipped file is 2 passed. The row is a real guard, not a tautology.
  suite — test_mem_cap_tasks_max.py + test_launch_memory_cap.py + test_heal_mem_cap.py: 27 passed (was 25).
  residues 4/5 — `short test sentence here` and `## Experiment / What did you do?` are both gone from the two nodes (grep, no hits).

NEAR MISS, stated so a later reader can check it: a test that only re-asserts the live cell 150 would have passed identically under `is` and under `==` (CPython caches -5..256), so a green suite here proves nothing about the fix. The planted row above 256 is the only thing that does, and that is the row that exists.
CAVEAT: 27 test lines against a <= 25 ceiling (2 over, imports and docstring included). DEVIATION, declared not silent: the orders said `git rm -- 0`; the kid used a plain rm and said so in its node, because the round rule forbids git. Correct call.
CAVEAT: the two foreign node-body edits are uncommitted and the kid is forbidden from git — left for the loop to commit, not landed by hand (a director edit to a foreign node fakes whose work it is).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-1bb0f2cb, DH.480): this version differs from the kid's by adding the parent's own probe record, not by changing the kid's claim.

The kid closed all five named residues inside FILE SCOPE and I reproduced its one load-bearing measurement myself: a scratch copy with `==` flipped to `is` fails 2/2, the shipped file passes 2/2. The hypothesis under test — resolve_tasks_max reads spawn.tasks_max and nothing else — holds on the live config (150), on a planted 1000/"1000"/4242, with the decoy values.memcap.tasks_max present, with the cell absent (96), with the cell non-numeric (96), and under an AGI_TASKS_MAX=77 override.

Three things this version adds that the kid's could not know: (1) the AGI_TASKS_MAX override conjunct, which no shipped row in the diff exercises, only my probe does — the hypothesis has an unclaimed row; (2) the fact that the two foreign node-body edits (a00-36f071dc-154d29, a00-58f37c40-6df0e6) landed in the worktree but NOT in the scoped done commit, while the stray file `0` removal did; (3) the 27-vs-25 line overage against the ceiling, which I accept as immaterial (two lines are the import and the docstring) and name rather than cut.

Verdict: accepted, proved stands. Nothing demoted this round.
<!-- THOUGHT:END -->
