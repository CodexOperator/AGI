---
id: hypothesis:heal-crash-respawn-writes-the-new-pid-into-the-row
mint_id: d052c815ee174faaa801bac91302289e
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-general-3
scaffold_hash: 36ece904d0c94192
season: 2
testable_claim: After a crash-respawn heal writes the new session pid into the seat's config:posts pid cell, so a second sweep pass over the same seat finds it alive and does not respawn again
title: "heal crash-respawn writes the new pid into the row: one dead process, one respawn"
town: core
---
# hypothesis:heal-crash-respawn-writes-the-new-pid-into-the-row

## Measured
- inbox:sanctuary-master, from heal: `[crash-recovery] all-is-one pid 2871680 dead at 2026-10-01T18:46:21Z (remote-control-disconnect); respawned all-is-one gen 4 @id @13` then `[crash-recovery] all-is-one pid 2871680 dead at 2026-10-01T19:00:18Z (unknown); respawned all-is-one gen 4 @id @14` -- the SAME dead pid twice: the 18:46 respawn never wrote its new pid into the config:posts row, so the next sweep re-judged the old pid dead and respawned a second session.
- heal.py `_write_crash_recovery` records `pred_pids` + the outcome pid in the rotation record; the row's `pid` cell is the one the sweep reads.
- Ordered by belam 19:0xZ 10-01 (direct message, relayed on doc:card-sanctuary-master §1).

## CLAIM
After a crash-respawn, heal writes the NEW session's pid into the seat's config:posts `pid` cell (into the working-tree row through rotate._successor_row_write / write.submit, which the next sweep reads; heal commits no row write anywhere -- DH.2 correction, mur-heal-respawn-pid-2), so one dead process yields exactly one respawn: a second sweep pass over the same seat finds the new pid alive and does nothing.

## Dispatch line
config-max: none expected (the pid cell already exists) / template-max: none / code: the respawn path that does not write the outcome pid back to the row.

## FALSIFIERS
- One simulated crash (fake seam, no real tmux/claude), two sweep passes: a second respawn on pass 2, or the row's pid still the dead one after pass 1.
- More than one live session for the seat after the two passes.

## TESTS
A committed test in extensions/agi/tests/test_heal*.py driving one respawn + two sweep passes through fakes only (never a real pi / claude / tmux); the existing heal crash-recovery tests stay green.

## FILE SCOPE
extensions/agi/bin/heal.py (the respawn path only) · its test file · this node.

## CEILING
1 pi-free parent, 0 kids beyond its own · <= 12 production lines · 0 USD.

## RESULT (kid d7a541b94, director record)
NUMSTAT 14e06f47b..d7a541b94: heal.py 5/1 · test_heal_respawn_pid.py 90/0. 26 passed (kid). mur-heal-respawn-pid (pi-free, extra signal): review accept_with_residue (C1-C5 + C7 MET, C6 UNVERIFIED), verify unstructured (residue 1 confirmed; pane == parent of the agent cmd, dies with it: rotate.py ~2013, mem_cap.py ~356-358). The gating claude-code mur follows the corrective.

## CORRECTIVE DH.1 -- closes mur-heal-respawn-pid heal-pid-code (accept_with_residue)
BASE      CUT FROM heal-respawn-pid tip d7a541b94 (worktree /mnt/agi-ram/worktrees/heal-respawn-pid). No merge. Never rebase.
1. the pane lookup is unguarded after the launch -- heal.py ~3717 (seam read ~2455-2459) -- TRUE WHEN an exception from the pane lookup can never abort the sweep between the launch and the row write: it yields None (the row as before) and the reason reaches stderr + _watch_log; one test with a raising seam.
2. the pane pid stands in for the agent pid (C6 UNVERIFIED) -- heal.py ~3717, the liveness gate ~3886 -- TRUE WHEN a test proves the pane pid is dead at the next sweep once its agent dies on the launcher this path uses (pane == parent of the agent cmd), OR, for a launcher where the pane can outlive the agent, the row keeps None there; name which in the commit.
3. the comment says 'pid-free' -- heal.py ~3718 -- TRUE WHEN it says what None does (rotate.py ~9999 keeps the prior pid).
4. missing pins -- test_heal_respawn_pid.py -- TRUE WHEN a test proves a real launcher pid wins with NO pane probe, and a falsy window_id makes NO lookup.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE extensions/agi/bin/heal.py (the respawn path only) · extensions/agi/tests/test_heal_respawn_pid.py · this node (director)
CEILING   HARD CAP: 1 Sonnet 5.5 kid · <= 10 production lines · <= 80 test lines · 0 USD -- over it = the round is cut

## CORRECTIVE DH.2 -- closes mur-heal-respawn-pid-2 heal-pid-code (accept_with_residue; gating, claude-code)
BASE      CUT FROM heal-respawn-pid tip 3de303583 (worktree /mnt/agi-ram/worktrees/heal-respawn-pid). No merge. Never rebase.
1. the row pid can now be a PANE pid while other readers compare it to a registry session pid (UNVERIFIED in the mur) -- heal.py ~3910-3925 (_alive_via_pin, the stale-row arm) -- TRUE WHEN a fixture sweep with row pid = a live pane pid and a registry session of a DIFFERENT pid proves no stale-row misfire and no second respawn (or the reader is fixed so it holds); one test.
2. the unknown-pane fallback keeps the dead pid, so a later sweep could respawn again -- test_an_unknown_pane_pid_leaves_the_row_pid_alone -- TRUE WHEN a test proves the repeat is bounded (the once-guard SEAT_DEAD_WINDOW_S, or a value written to the row that stops it), and the unknown-pane case is named on stderr + _watch_log.
DEMOTED   respawn_outcome.pid None (refuted: nothing reads it, rotate.py ~7937-7956) · 'committed by exact path' = node prose, corrected by the director (heal commits no row write; write.submit lands the working tree the sweep reads) · experiment node = the director's record (RESULT) · the reviewer ran no test (tree not at the tip) = a mur-runner note.
ANON      no user name, home or repo path value, host or IP
FILE SCOPE extensions/agi/bin/heal.py (respawn path + the reader in item 1 only if it must change) · extensions/agi/tests/test_heal_respawn_pid.py
CEILING   HARD CAP: 1 Sonnet 5.5 kid · <= 8 production lines · <= 70 test lines · 0 USD

## CORRECTIVE DH.3 -- the INTEGRATION gap with hypothesis:heal-ack-line-comes-from-config-rotations-by-role (director, 21:2xZ 10-01; DH.2 = mur-heal-respawn-pid-heal-ack-by-role accept/accept)
BASE      CUT FROM heal-respawn-pid tip 3f4f6cb54 (worktree /mnt/agi-ram/worktrees/heal-respawn-pid). No merge. Never rebase.
MEASURED  trunk 5ac25bf7b + heal-respawn-pid + heal-ack-by-role (merge-tree clean): the heal family = 8 failed / 323 passed -- ALL 8 in test_heal_respawn_pid.py: its fixture root has no config:rotations, so the ack round's _recover_seat refuses by name ('recovery_ack[director] unusable ... FileNotFoundError'); trunk alone 314 passed.
1. TRUE WHEN test_heal_respawn_pid.py's fixture seeds the config:rotations recovery_ack cell (the suite idiom: a per-module seed helper, as the 6 neighbour tests of the ack round do) and the file passes BOTH alone on this branch AND on the combined tree (trunk + both rounds). Test-only.
FILE SCOPE extensions/agi/tests/test_heal_respawn_pid.py
CEILING   HARD CAP: 1 Sonnet 5.5 kid · 0 production lines · <= 20 test lines · 0 USD
