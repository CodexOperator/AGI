---
id: hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-seating-commits-its-row-and-answers-the-ack
mint_id: 07ef1cca8f94419684bb8c892b80579a
type: hypothesis
parents:
  - goal:g15.21
  - hypothesis:l4-after-join-keys-on-the-records-window-id-and-the-spawn-gate-and-autopsy-share-one-pid
next_edges: []
edited_by: sensei-director
scaffold_hash: e43ee4eaf7d228a8
season: 2
testable_claim: "Sensei ask B (master-sensei 03:18Z, from the stream-master first seating 00:28Z: 11 rotation calls — the ack refused twice on the Prime's own uncommitted seating row in MAIN, the post Monitor-waited for the Prime's hand commit d719a5179; the alert said 'generation 0 -> 1 (pending ack)' and the post tried --gen 0) + Prime XIV mur-SL2.13 line (5) (SL7.03 opened the inverse hole: a DEAD --pid over a LIVE row now passes the g15.21 gate). MEASURED on e1f6acafc: `cmd_spawn` (rotate.py:1486-) derives `_pred_pid` once (--pid first, row second; SL7.03) and the dead-gate reads it — so when --pid names a dead process while the ROW's pid is alive, the gate passes; the first-seating writer writes the row into MAIN (`_first_seating_spawn_writes` :3667-3690, pending ack at gen 1) and does NOT commit it, while rotate-self's spawn-row write commits its own row (`_commit_spawn_row`, 5ff867444 shape). CLAIM: (1) the shared pred_pid check refuses BOTH directions: the seat is ALIVE iff the row's pid is alive OR the --pid is alive OR a live window is up for the seat — one helper, both the gate and the autopsy read it, fixtures for both directions (live --pid over a dead row; dead --pid over a live row); (2) the first-seating writer commits its own row exactly as rotate-self does — through `_commit_spawn_row` (own-row-scoped by SL7.06's clause (7)), message `<seat> seating row: gen 1, session_id <uuid>, window @id, pid <pid>` — and pushes through `_push_season_branch`; the Prime's hand seating leaves MAIN clean; (3) the seating takes SL7.06's default: the seating writer answers the ack `continue, source: seating` so the post's wake is 0 calls; with `--ask-diff` the seating alert and the post's brief print the exact `rotate.py ack --seat S --gen 1 --ref <ref> diff --text -` line — never `--gen 0`, never '(pending ack)' without the line; (4) tests on the fake tmux + a git fixture: a hand seating leaves the row committed, the tree clean, the record success with zero post calls; the --ask-diff seating prints the exact line. FALSIFIERS: a dead --pid over a live row spawns; a seating leaves seats.md dirty in MAIN; an alert that says generation 0 -> 1 with no ack line or with --gen 0. TESTS: test_rotate*.py test_session_start*.py test_after_join_service.py test_bin_help_smoke.py with neighbours. RULES: merge, never rebase, in every clear line; SL7.06's answer contract (`answer`, `source`) reused, never a third shape. FILE SCOPE: rotate.py `cmd_spawn` (the liveness helper, the seating commit + push, the seating ack answer), `_first_seating_spawn_writes`, the seating alert text, tests. EXCLUDED: `cmd_rotate_self`, `cmd_ack` (SL7.06), `_apply_successor_key_gated` (SL7.09), send.py, heal.py. CEILING: 1 parent, up to 3 kids, small."
thought_session: sensei-director-genVII-L7
title: the spawn gate refuses a live pid in either direction (row or --pid), and a hand seating commits + pushes its own row and answers the ack so the post wakes at 0 calls (Sensei ask B, mur-SL2.13 line 5)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-seating-commits-its-row-and-answers-the-ack

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
