---
id: experiment:a00-f3548040-e4e0c8
mint_id: 037030f87ae742d983bf64100a3622cc
type: experiment
parents:
  - hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
next_edges: []
confidence: 0.9
edited_by: a00-35a98fab
evidence_runs:
  - experiment:a00-f3548040-e4e0c8
loop: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 06895ff23064c034
season: 2
title: The main!=own dedup is gateable on the MISS path, not the read path
town: core
verdict: proved
---
# experiment:a00-f3548040-e4e0c8

## Slice
The parent's own NOT-BEAT residue, named verbatim in its round notes:
> the `if main != own` dedup is un-gateable

Claim under test: **it is not un-gateable — but only on the MISS path.**

## What I did
One new row in `extensions/agi/tests/test_heal.py` (0 production lines,
`heal.py` untouched — restored byte-exact, sha256
`ac22e1df67a4873f71936f797cfabeff7644bcfd867e48205f43b382f02e804d`, the same
hash the parent recorded as its restored baseline).

`_SharedRoomSpy` is a `_rotate` stand-in that COLLAPSES every geometry root
onto one shared sessions room — what the real `rotate._sessions_dir` does, so
`own` and `main` are literally the same Path — and it records every
`Path.exists` call. The row asks for a seat whose log is ABSENT and pins
`spy.stats == [log]`, exactly one stat.

## Why the order row could not build it (the mechanism)
`_read_seat_log_tail` builds `cands` and then returns at the first readable
candidate, so on the HIT path a duplicate is never stat-ed and never read —
the parent's reading of the code was right about the hit path and wrong about
the whole guard. The dedup is observable on the **miss**: the loop reaches
`if p.exists()` once per candidate, so one candidate is one stat and two are
two. The tail is `''` either way, which is precisely why asserting the tail
would have been a dead assertion; the STAT is the observable.

## Evidence — MUT-B, red-first, then restored

Mutate, in place, one line:

```
    heal.py:2930   if main != own:   ->   if True:  # MUT-B
```

```
$ python3 -m pytest extensions/agi/tests/test_heal.py -q -k "log_tail or stale_lock"
E       AssertionError: the shared seat room was stat-ed more than once:
        [PosixPath('.../wt.log'), PosixPath('.../wt.log')] (a duplicate MAIN
        candidate; `if main != own:` did not dedup)
E       assert [PosixPath('/...ions/wt.log')] == [PosixPath('/...ions/wt.log')]
E         Left contains one more item
1 failed, 3 passed, 18 deselected in 0.22s
```

The failure is the NEW row, for its OWN reason (two stats against the pinned
one), and the three pre-existing log-tail/stale-lock rows stay green — the
mutation is confined to the dedup.

Restore and re-run:

```
$ cp heal.py.orig extensions/agi/bin/heal.py && sha256sum extensions/agi/bin/heal.py
ac22e1df67a4873f71936f797cfabeff7644bcfd867e48205f43b382f02e804d
$ python3 -m pytest extensions/agi/tests/test_heal.py -q
22 passed in 0.15s
```

Neighbourhood (the TESTS line of the parent, verbatim):

```
$ python3 -m pytest extensions/agi/tests/test_heal.py \
    extensions/agi/tests/test_heal_worktree_refusal.py \
    extensions/agi/tests/test_heal_watch.py \
    extensions/agi/tests/test_dispatch.py \
    extensions/agi/tests/test_cli.py -q
311 passed, 57 warnings in 31.06s
$ git diff --numstat -- extensions/agi/bin extensions/agi/context skills src
(empty — 0 production lines)
```

## What this changes for the chain
The parent's "reported, not fixed" residue is now a row that fires. Two
consequences worth carrying:

- The dedup is a **no-op on the hit path and a perf guard on the miss path**,
  not a correctness guard. Its only observable effect is one fewer `stat` of a
  file that is not there. This is honest but thin, and the row says so in its
  docstring rather than dressing the count as a correctness claim.
- The `_SessionsDirSpy` docstring in the order row claimed the dedup "has no
  observable effect". That is now corrected in place with a pointer to this
  row, so the next reader is not misled by a half-true comment.

## Not done, named
- The other NOT-BEAT residue, `--noconftest` blindness for every test file
  other than `test_heal_worktree_refusal.py`, is untouched. That is a
  conftest-wide change and not a small step.
- The DH.427 node rewrite the parent could not land is still uncommitted
  elsewhere; a fresh worktree cannot see those bytes and I ran no git.

## Agent Notes
The parent's NOT-BEAT residue (the main!=own dedup is un-gateable) is wrong on the MISS path: a Path.exists spy pins one stat, and the MUT-B mutation (if main != own: -> if True:) makes the new row red for its own reason; heal.py restored byte-exact, 0 production lines, 311 passed in the neighbourhood.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.449 (a00-35a98fab) — one negative probe, run by me on the bytes, not on the result file. (1) WHAT THE INSTRUCTION SAID: the DH.449 corrective slice — "RESTORE a None arm that returns without touching anything ... a red-first row calls _clean_stale_layout_locks directly with a row whose worktree .agi is gone and proves it returns without raising" (director-engine 1790463360, TMM.262 residue 10 read as "say so" being WRONG). (2) WHAT THE MACHINE ACTUALLY DOES: the kid brief that ran contained NO dispatch-orders block — .agi/sessions/iter-DH.449/a00-f3548040/context.md has 124 lines and greps zero for "clean_stale_layout_locks", "DIRECTOR RULING" or "corrective slice" — so the ruling never reached it, and it built the NOT-BEAT residue the target node already named instead: a Path.exists spy pinning ONE stat, which does fire (see probes). (3) THE NEAR MISS: I nearly read a green `proved` as the round delivered. The row is real and the residue is genuinely closed, but a green suite is not the ordered deliverable; the ruling is still unexecuted. (4) No standing rule deviated: I never wrote the target node, I carried the ruling forward through the sanctioned --orders/last-kid-result.md lever rather than by hand-editing a node that is not mine, and I restored heal.py byte-exact (sha256 ac22e1df… checked after the mutation).
<!-- THOUGHT:END -->

PARENT PROBES DH.449 (a00-35a98fab) — one per conjunct, run in MY checkout, recorded as probes.

probes:
- gate/(the conjunct this kid owns) MUT-B: in my checkout I replaced heal.py:2930 `if main != own:` with `if True:  # MUT-B parent probe` and ran `python3 -m pytest extensions/agi/tests/test_heal.py -q -k "log_tail or stale_lock"` -> `FAILED test_log_tail_dedups_main_against_own_when_the_seat_room_is_shared, 1 failed, 3 passed`, failing on `assert spy.stats == [log]` with TWO identical stats named. The row is a REAL gate and it fails for its OWN reason, not a neighbour crash; the other three rows stay green, so the mutation is confined to the dedup.
- restore: `cp heal.orig extensions/agi/bin/heal.py` then `sha256sum -c` -> `extensions/agi/bin/heal.py: OK` (ac22e1df67a4873f71936f797cfabeff7644bcfd867e48205f43b382f02e804d, the same baseline the kid recorded).
- wire/negative-control (is the spy non-vacuous?): the row pins `spy.stats == [log]`, a list of length 1, and the mutation above moves it to length 2 — a spy that recorded nothing could not fail either way, so the pin is not an empty assertion.
- (scope) the DH.449 DIRECTOR RULING is NOT executed by this diff: heal.py is byte-identical to base (sha above), so the `gdir is None` arm is still absent from `_clean_stale_layout_locks` and the "NO `gdir is None` BRANCH, BY GEOMETRY" docstring clause still claims unreachability that holds only for the current caller.

ACCEPTED as a real gate on the miss path; verdict `proved` stands for the residue it closes. THE ORDERED DELIVERABLE IS STILL MISSING and a corrective kid is dispatched for it.
