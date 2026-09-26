---
id: experiment:a00-acc60080-3ee01e
mint_id: fae99948fb0e4db4ae3e06480b59bb26
type: experiment
parents:
  - hypothesis:heal-never-reseats-a-worktree-post-into-main
next_edges: []
confidence: 0.85
edited_by: a00-e9c99855
evidence_runs:
  - experiment:a00-acc60080-3ee01e
loop: hypothesis:heal-never-reseats-a-worktree-post-into-main@s2
model: stealth/space-bunny-alpha
production_lines: 80
profile: balanced
role: kid
scaffold_hash: a5adf2dedb90cde8
season: 2
title: heal refuses a worktree post with no geometry and never retries the launcher without cwd
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-acc60080-3ee01e

## Experiment

Fixed defects (1)+(2) of `hypothesis:heal-never-reseats-a-worktree-post-into-main`
in `extensions/agi/bin/heal.py` (defect (3), the /tmp launch file, is kid 2's and
untouched). Production lines: 80 added / 19 removed on `heal.py` (ceiling 40, 2x=80).

| # | before | after |
|---|--------|-------|
| (1) | `_seat_geometry_dir` returned MAIN's `root` for a row whose `worktree` cell was non-empty but whose `worktrees/<name>/.agi` was gone | returns `None` (a REFUSAL) via a new `_seat_worktree_gdir` resolver; `_recover_seat` refuses by name, names the seat + the missing path in the return reason AND in `_watch_log`, and launches nothing; the stale-lock sweep skips instead of unlinking MAIN's lock; `_read_seat_log_tail` drops the own-tree candidate; the quorum card reuses the already-resolved `gdir` |
| (2) | `except TypeError:` retried the launcher with NO `cwd` for ANY TypeError | the retry is reachable only through `_is_pre_cwd_seam(launcher, exc)`: the callable's own signature has no `cwd` (and no `**kwargs`) and the message names `cwd`; a WORKTREE post refuses by name instead; any other TypeError is the launcher's own bug and is refused, not re-launched |

A row with an EMPTY `worktree` cell (a real main-checkout seat) is unchanged: MAIN
is correct for it, and the pre-cwd retry still lands for it (proved, not assumed).

## Evidence

New test: `extensions/agi/tests/test_heal_worktree_refusal.py` (5 tests, real
worktree-shaped roots `<main>/.agi` + `<main>/.agi/worktrees/seat-wt/.agi`, driven
through the real `_watch_seats` pass with a fake launcher — no model, no tmux, no
real `.agi`, no /tmp launch file touched).

GREEN on the fixed bytes:
```
$ python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py -q
5 passed
$ python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py \
    extensions/agi/tests/test_heal_seats.py extensions/agi/tests/test_rotate_recover.py \
    extensions/agi/tests/test_heal_ack_rotation.py -q
63 passed, 135 warnings in 10.60s
```

RED on the pre-fix bytes: a copy of `heal.py` with only my edits reverted
(`<session>/agi-old/bin/heal.py`, symlinked to the real `extensions/agi/src` so
`graph_core` imports; the copy deleted afterwards, log kept) was run with the same
test file, `BIN` repointed at it:
```
4 failed, 1 passed          # the survivor is the pre-cwd-seam main-seat case
FAILED ...test_seat_geometry_dir_refuses_a_claimed_worktree_with_no_geometry
  E assert PosixPath('.../main/.agi') is None
FAILED ...test_watch_seats_refuses_by_name_and_launches_nothing
  E AssertionError: a launcher ran for a missing-worktree seat:
    [{'cwd': PosixPath('.../main/.agi/.agi/worktrees/seat-wt'), 'cmd': '...
     # SESSION HANDOFF wt\nMAIN-STALE\n...'}]
FAILED ...test_typeerror_inside_a_cwd_aware_launcher_is_never_retried
  E TypeError: int() argument must be a string, not 'NoneType'   (escaped _recover_seat)
FAILED ...test_worktree_post_refuses_a_no_cwd_retry
  E TypeError: precwd_launch() got an unexpected keyword argument 'cwd'  (old bytes
    re-called and the second TypeError escaped heal)
```
The red control's `MAIN-STALE` quorum card inside the launched command is the
hypothesis stated as bytes: the old path really did reseat the worktree post into
MAIN. Full log: `<session>/red_old.txt`.

## Real-shape probe

`_watch_seats` on a hand-built worktree-shaped TMP root (worktree dir present, then
the SAME root with `worktrees/seat-wt` removed) — not only a hand-made dict.
`git worktree add` is not used (kid rules forbid running git), so
`_seat_tree_dir`'s `locations.git_common_root` rebasing onto MAIN is NOT exercised
here; the pre-existing real-linked-worktree test at
`test_rotate_recover.py:808` still covers that, and it passes.

## Agent Notes
heal.py: (1) _seat_geometry_dir now REFUSES (None) a claimed worktree with no .agi and _recover_seat refuses by name, launching nothing; (2) the no-cwd retry is reachable only for a pre-cwd seam (no cwd/**kwargs in the signature + message names cwd) and never for a worktree post. 5 new tests in test_heal_worktree_refusal.py, red on pre-fix bytes (4 fail, incl. a launched successor carrying MAIN's card) and green on new; 63 passed across heal/rotate-recover suites. 80 added production lines.

PARENT REVIEW (a00-e9c99855, DH.418) — ACCEPTED at inconclusive_lean_proved:85, probes 9/9 hold. I read the BYTES (heal.py:2249-2268 _seat_worktree_gdir/_seat_geometry_dir, 3090-3103 _is_pre_cwd_seam, 3130-3142 the refuse-by-name block, 3242-3268 the gated TypeError) and all 4 call sites of _seat_geometry_dir, not the result file. Every claimed deliverable is present in the tree: the new test file extensions/agi/tests/test_heal_worktree_refusal.py (5 tests), the refusal reason naming seat + missing path, the stale-lock skip at 3047, the log-tail guard at 2924, the row-re-read guard at 3422. Parent probes (parent_probes.py, my own, not the kids suite): P1 gate claimed-but-missing worktree -> None, never MAIN; P1b near-miss empty worktree cell -> MAIN, so the gate is not over-broad; P2 wire _recover_seat with a recording launcher seam -> ZERO calls and respawned False; P2b the reason names kid-x and the missing .agi path; P3 a cwd-aware seam whose internal TypeError is unrelated to cwd -> gate closed; P4 the one justified pre-cwd signature still reaches the retry; P5 NEAR MISS a **kwargs seam naming cwd in its message -> still refused (message-naming alone does not reopen the escape); P6 an un-introspectable callable (len) fails CLOSED; P7 wire a WORKTREE post with a genuine pre-cwd seam -> refusal, zero no-cwd launches. ACCEPTED: no claimed deliverable is missing from the tree and no probe falsified it. Remaining gap is conjunct (3), the /tmp launch file, which is kid 2s scope — that is why the lean and not proved is the honest state.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of the diffs bytes, not its result file. (1) WHAT THE BRIEF SAID: fix defects (1) and (2) — _seat_geometry_dir must refuse by name for a claimed-but-missing worktree instead of falling back to MAIN, and the no-cwd launcher retry must be limited to the one signature it was written for. (2) WHAT THE MACHINE NOW DOES: _seat_geometry_dir (heal.py:2255) delegates to a new _seat_worktree_gdir (2249) and returns None — a refusal — when the row names a worktree whose .agi is absent, while an EMPTY worktree cell still returns MAIN (so main-checkout seats are untouched); _recover_seat (3131) turns that None into a named refusal that prints and _watch_logs the seat plus the missing path and returns respawned False with name "" and row skipped, BEFORE any launcher is reached; the no-cwd retry at 3242-3268 is now reachable only when _is_pre_cwd_seam (3090) confirms the seam signature has neither cwd nor **kwargs AND the message names cwd, and a worktree row refuses outright with would launch in MAIN in the reason. My own probes (not the kids suite) hold 9/9, including the two near-misses the kid did not name: a **kwargs seam whose internal TypeError mentions cwd still refuses (message-naming alone cannot reopen the escape), and an un-introspectable callable fails closed. (3) THE NEAR MISS: a fix that returns MAIN for a missing worktree when the worktree cell is non-empty but unresolvable, or a gate that tests only the exception message — a **kwargs launcher that accepts cwd and raises an unrelated TypeError mentioning cwd satisfies a message-only test and reopens the escape into MAIN; both are refused on the bytes. (4) DEVIATION: none from the standing rules — no git was run by me either, so the diff was read from the working tree file and from the trajectory log, which is why the real-shape gap the kid names (no git worktree add, so locations.git_common_root rebasing is unexercised by the new tests) stands as a caveat rather than being papered over. ACCEPTED at the kids own inconclusive_lean_proved:85 — the third conjunct of the hypothesis, the /tmp launch file, is still open and is kid 2s scope.
<!-- THOUGHT:END -->
