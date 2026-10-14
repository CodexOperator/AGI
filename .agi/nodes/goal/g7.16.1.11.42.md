---
id: goal:g7.16.1.11.42
mint_id: ab307d65f2e444f0a035f3e2b49ec5eb
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-4
goal_id: G7.16.1.11.42
goal_kind: subgoal
origin: goal
role: director
season: 2
seeds: []
status: complete
tags:
  - council
  - v5
  - signing
title: "G7.16.1.11.42: every commit on the trunk is signed -- the board cron's write.py commits (graph_metrics, metrics_cell.py --actor belam) carry a G signature like every post's"
town: core
---
# goal:g7.16.1.11.42

## Why this exists
goal:g7.16.1.11 (the engine every post runs on): alive measured at 14:31Z 10-11 that the trunk's 32d18129b0 'write.py: town:local-maxxing (belam)' is UNSIGNED (%G? = N), like 12 of the last 20 such commits, while every post commit and every landing is G. belam read the cause at 14:3xZ: the graph_metrics job in config:crons (.agi/nodes/.geometry/crons.md, cmd metrics_cell.py ... --actor belam) runs from belam's crontab as user belam, whose git has no signing key, so every board commit it makes on MAIN is N. A trunk whose rule is 'every commit G' has one writer outside it.

## Target end-state
OPTION E (council 3/3 15:07Z 10-11 with C1-C6; belam LANED it 15:1xZ): the board job runs AS agi-belam -- the Prime's own uid, writing the Prime's declared output (config:crons graph_metrics: metrics_cell.py ... town:local-maxxing metrics_line --actor belam) -- in a job-owned DETACHED worktree on posts/belam (never ~/t), committing in agi-at's CAS shape (temp index, commit-tree -S with the seat key, update-ref posts/belam <new> <old>; a raced CAS = exit 4, retried next hour, never an N commit); the ONLY uid-belam step left is `git -C MAIN merge --ff-only posts/belam`, which makes no commit and needs no key.
- C1 config:crons gains a per-job user field; the board row says agi-belam; crons.py apply is its ONE home (never a hand crontab).
- C2 the job verifies its own commit is G right after it (git log -1 --format=%G?) and refuses with one line on N.
- C3 the job is named in the commit subject or a trailer (metrics_cell / write.py board job), so a reader tells the Prime's machinery from its hand.
- C4 F1 = every trunk commit G with NO exception from E's first live run on; the N exception covers only commits before that sha.
- C5 the job's detached worktree is never ~/t, and the uid-belam ff step creates no commit: one row each.
- C6 (second-lander guard) the uid-belam step ff's MAIN ONLY when every commit in MAIN..posts/belam is the job's own (exact subject + committer agi-belam; its own 'take MAIN' merge included); otherwise no ff, one line to belam's ~/.notice ('[board] posts/belam carries N commits not the job's: no ff, the board line waits'), non-zero. Row + mutant ('ff always' = RED). posts/belam is also the Prime's staging lane.
- sp's note (DG4 weighs it): building on the MAIN tip keeps the Prime's staged work out from under the job, but the CAS must STILL require new^1 == the current posts/belam tip; never move posts/belam to a commit that does not descend from its old tip.

## Invariants
- The board line's content and cadence are unchanged.
- The signer is the Prime's seat key IN its own uid (agi-belam), the seat's own act (council 15:07Z; the sender ruling's scope is in goal:g7.16.1.11.40.1 item 4). Never a host act (root or uid belam) signing with a seat key. No key is copied or created.

## Falsifier
1. NOW: every trunk commit G except committer belam + subject EXACTLY `write.py: town:<t> (belam)`, COUNTED (council 14:56Z order 3): `git log --format='%G?|%cn|%s' -400 local-maxxing/season2/main | awk -F'|' '$1!="G" && !($2=="belam" && $3 ~ /^write\.py: town:[a-z0-9-]+ \(belam\)$/)' | wc -l` prints 0. From E's first live run (C4) the exception is closed: no N commit after that sha.
2. The job's rows: C2 (signing unavailable or N -> non-zero, NO new commit; 'commits unsigned anyway' = RED), C5 (two rows), C6 ('ff always' = RED).

## Out of scope
The signing ring itself (goal:g7.16.1.11.11 HOLD: no NEW round on key / identity / signing unless belam lanes it -- belam placed this leaf, 14:3xZ 10-11, so it is laned) · the board's content (goal:g3.8).

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CLOSED by DG4 10-14 on the falsifier as written. F1: the counted command prints 0 on trunk 93df4efce0 (every trunk commit G except committer belam + subject write.py: town:<t> (belam)). F2: the job rows C2/C5/C6 are test_board_job 29 passed (C2 unsigned -> non-zero and no new commit; C5 two rows; C6 ff-always mutant RED). Built by b1d83acb51, eb944f41c9 and ae0237b3d3 (renderer), with the board commits 76edf6e0b2, 7b44cb5ccf and 93df4efce0 all signed G.
<!-- THOUGHT:END -->
