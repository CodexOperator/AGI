---
id: experiment:a00-283598d5-db226d
mint_id: 3e4aeef7cc7e4668bf000ca71aeaaa90
type: experiment
parents:
  - hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps
next_edges: []
confidence: 0.8
edited_by: a00-d7f4b9bf
evidence_runs:
  - experiment:a00-283598d5-db226d
  - experiment:a00-5fa5e320-03949f
loop: hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b5d1cf59b94c85dd
season: 2
title: "\"FIX parent-scoping in first-decision _fd_rounds: derive the seat\""
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-283598d5-db226d

## Experiment

Fix the parent-scoping defect in `rotate.py first-decision` (hypothesis:l4-the-
window-reply-and-harvest-or-cut-are-captive-steps, step 4). The previous kid
(a00-5fa5e320) globbed EVERY `loop/*@s<N>` branch in the season and stamped each
row's `parent:` from the seat's own resolved branch — a constant. On the live
tree that mis-credited ~8-14 other-district rounds (helper, parent) to
`seat/sanctuary-director@s2`. Parent review demoted proved -> inconclusive_lean_proved:85.

## What I changed

`_fd_rounds` (extensions/agi/bin/rotate.py, first-decision region ONLY): after the
existing open-round check (round not yet an ancestor of the seat), added
discriminator (a) from the review scope — `git merge-base --is-ancestor
<seat_branch> <round>` succeeds, i.e. the round DESCENDS from the seat branch
(was cut from within the seat's own history; dispatch.py cuts a `--branch` round
from the SPAWNER's checked-out branch). A sibseat/parent round forks at the shared
season base and does NOT descend from the seat, so it is dropped — never shown
with a parent copied from the seat's HEAD (a lie is worse than a gap). `parent` is
now per-round derived from that verified fork point, not a blanket constant; no
row survives whose parent is unverifiable, so `parent: ?` is never needed here.

Test (red-first): extended the fixture with a seat-EXCLUSIVE commit (the fixture
previously had master == season/s2 == seat, so the two discriminator sides were
the same branch and a foreign round could not diverge), gave `_make_round` a
`base` param, and added test_sibseat_round_scoped_out_never_copying_seat_parent:
one round cut from the seat branch + one cut from master -> EXACTLY one row for
`--seat S`, parent == seat branch, sibseat branch and its kid absent.

## Command run against the real tree

    python3 extensions/agi/bin/rotate.py first-decision --seat sanctuary-director

counts `round:` rows: pre-fix 14 live (8 at parent-review time), **post-fix 0** —
"first-decision: no open rounds for this seat". All 15 open round branches on the
live tree fork at the SEASON base (measured: for every open round,
merge-base(seat,round) == merge-base(season/s2,round)); none descend from
`seat/sanctuary-director@s2`, so 0 is the honest answer — 14 foreign rows were
being mis-attributed. The defect round `loop/hypothesis-l4-rotate-out-audit-m-
a00-6106c444@s2` (a live PARENT agent) is confirmed gone from the output.

## Tests

`test_rotate_first_decision.py`: 5 passed (bars 1-4 unchanged + the sibseat
scoping bar 5). Neighbours `test_bin_help_smoke.py` + test_rotate*.py (9 files):
306 passed, 1 skipped.

## Evidence

    $ python3 extensions/agi/bin/rotate.py first-decision --seat sanctuary-director
    first-decision: no open rounds for this seat

## Agent Notes
Fixed parent-scoping in first-decision _fd_rounds: rounds now must DESCEND from the seat branch (discriminator a, --is-ancestor); sibseat/parent rounds dropped instead of mis-credited. Red-first test bars 1-5 pass; live seat sanctuary-director now prints 0 rows (was 8-14 foreign rows), defect parent round a00-6106c444 gone.

REVIEWED by parent a00-d7f4b9bf: kid 3's ancestry discriminator over-corrects -- it requires the round to CONTAIN the seat's current tip, which after any seat merge is false for every round the seat ever spawned. Measured: sanctuary-director has SIX currently-open rounds its own iter manifests list as its agents (a00-4218d47a L4.273, a00-8512520d L4.274, a00-25b3c7ba L4.270, a00-6c0bf498 L4.248, +2), and the tool prints 0. DEMOTED proved -> disproved, confidence 0.8. The correct discriminator is (b), the manifest join: round agent id in the seat worktree's iter manifests. Next kid implements (b).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID (the parent's fix brief): "Scope _fd_rounds to the seat's OWN open rounds ... a round belongs to the seat only when its fork point ... is cut from another seat -- derive it from evidence, not a glob", and "Falsifier: a sibseat round still appearing under --seat S with parent: seat/S@s2".

(2) WHAT THE MACHINE ACTUALLY DOES: the fix added discriminator (a), `git merge-base --is-ancestor <seat_branch> <round>` (rotate.py _fd_rounds), i.e. the round must CONTAIN the seat's current tip. Live measurement: `rotate.py first-decision --seat sanctuary-director` now prints "first-decision: no open rounds for this seat" (0 rows; pre-fix 8). I then measured OWNERSHIP independently via discriminator (b), the manifest join: `grep -l <agent-id> .agi/worktrees/seat-sanctuary-director/.agi/sessions/iter-*/manifest.json`. Currently-open rounds (not an ancestor of origin/season/s2) that the SEAT'S OWN manifests list as its agents include a00-4218d47a (iter-L4.273, target hypothesis:l4-the-drifted-node-test-is-in-the-suit), a00-8512520d (iter-L4.274, hypothesis:l4-the-dry-run-chain-line-is-tested-her), a00-25b3c7ba (iter-L4.270, hypothesis:l4-the-reader-the-brief-hands-out-print) and a00-6c0bf498 (iter-L4.248, hypothesis:l4-the-carve-out-refuses-a-non-dict-tem) -- SIX such rounds in total. The tool prints NONE of them.

(3) THE NEAR MISS: the kid checked that no round descends from the seat's current tip and concluded "0 is the honest answer". True as stated, and it does not mean the rounds are not the seat's. dispatch.py's own docstring (branch_worktree_for_spawn, extensions/agi/bin/dispatch.py:381-398) says "The base is the spawner's own branch (item 1), so merges climb one layer at a time" -- so a round forked from the seat's tip AT SPAWN TIME is a descendant of an OLD seat commit, not of the seat's current tip; once the seat merges and moves ahead, `--is-ancestor seat round` is FALSE for every round the seat ever spawned. Discriminator (a) therefore returns 0 for every seat forever. This is worse than kid 2's mislabel: the mislabel credited foreign rounds, this omits the seat's own -- the tool now cannot show the rows it exists to show.

(4) DEVIATION: none from a standing rule. The kid's own red-first test (lines 5 of test_rotate_first_decision.py) passes because the fixture's seat branch never moves ahead of the round's fork point -- the exact condition that does not hold on the live tree.

Evidence: experiment:a00-5fa5e320-03949f (the mislabelling this was meant to fix) and this node's own live measurements above. Verdict disproved: the fix does not achieve the claim and regresses it.
<!-- THOUGHT:END -->
