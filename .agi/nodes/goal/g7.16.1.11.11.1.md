---
id: goal:g7.16.1.11.11.1
mint_id: 25f7b606ed5146178390a54d781eabc2
type: goal
parents:
  - goal:g7.16.1.11.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.11.1
goal_kind: subgoal
origin: goal
scaffold_hash: 3d33126ccc292cab
season: 2
seeds:
  - goal:g7.16.1.11.11
status: active
tags:
  - council
  - aa1
  - mail
  - g7.16.1.11
title: "G7.16.1.11.11.1: AA1.M mail without send.py -- a message is ONE signed ref update in the sender's own store (sh + git + jq, no Python); one root carrier per box, woken by a path unit, moves it between stores and boxes; mail is read from the post's store (no worktree hop); goal:g1.40's lost append cannot happen"
town: core
---
# goal:g7.16.1.11.11.1

## Why this exists
goal:g7.16.1.11.11 (AA1 boxes): belam [owner] 18:16Z (item M1) relayed the owner's line below; the council's alive designed it as AA1.M and scratch-tested it; belam ACCEPTED it as designed ([decision] 18:2xZ, "write AA1.M into goal:g7.16.1.11.11's leaves + hypotheses (the build); goal:g1.40 closes when it lands"). Source of the numbers below: doc:rse-aa1-boxes section AA1.M (alive, posts/alive; belam [owner] 18:16Z item M1; designed and scratch-tested by alive 18:1xZ); NOT re-measured by me.

## OWNER 2026-10-02 18:1xZ, verbatim (belam [owner] 18:16Z; banked town:local-maxxing Agent Notes 4f647b6a8)
"we should have a way to send messages without using send.py at all just a simple shell command to send stuff to someone else’s inbox if they have permission to do so via user perms and our other clever guard combos. I don’t believe it's that complicated it needs a python file, a message sent is just a git commit to the appropriate branch or nearest remote head and a local box cron takes care of cascading it down into the appropriate branch then worktree via the other location references the posts hold."

## OWNER 2026-10-02 18:2xZ, verbatim (belam [decision] 18:2xZ; banked town:local-maxxing Agent Notes)
"Yes that’s fine with me you have GO with new plan. The path unit deviation seems worth it to me as well, and as long as for store still does the job it’s fine by me."

## Target end-state
- SEND: `box send Q <msg` is sh + git + jq, no Python: ONE signed commit on `refs/box/P/Q` in P's OWN store; adjacency and squat checked; compare-and-swap `update-ref`, retried at most 5 times; a squatted tip stops at once, never retried. Bytes: the box script 2,005 B (1,785 + 142 for the retry = 1,927, then alive's 444 B level a() line in place of the 328 B matrix line and a comment 38 B shorter, belam [decision] 19:5xZ; expansion, 0 B in the zygote).
- PERMIT: user perms (P writes only its own store) x the parent-cell matrix (adjacency checked at send AND at read).
- CASCADE: ONE carrier per box (root; the owner's "local box cron"), reading the rows' LOCATION cells (box, store): Q on this box -> a runuser pipe moves P's `refs/box/P/Q` into Q's store (AA2's agi-carry, 454 B); Q on another box -> push `refs/box/P/*` to the remote head, Q's box carrier fetches it. WOKEN by a path unit on each store's `refs/box` (PathChanged: no polling cron) plus ONE timer for remote fetches (belam ACCEPTED deviation 1). About 260 B of expansion (carrier line ~200 B + path unit ~60 B).
- READ: `box read` verifies signer + adjacency, prints, moves `refs/held/Q/P` (only Q writes it). NO worktree hop: mail is read from the post's store, never copied into a worktree (belam ACCEPTED deviation 2: a worktree copy would be a second store that can drift from the first; the owner's "then worktree" collapses).
- send.py (317,096 B) retires for every v5 post; goal:g1.40 closes when this lands.
- SIGNERS (alive 18:29Z, included by belam [rule] 18:5xZ): ONE root-owned allowed_signers written by root at unit start from each post's own ~/.ssh/id_ed25519.pub (`<post>@agi valid-after=<now> <pub>`, `valid-before` stamping the previous generation); `.agi/keys/` stops being a source; host act 1 re-run reads G, not U. NOTE the lane: PRIME LANE named by belam 18:5xZ (owner 18:5xZ: "Feel free to pass the design on to dg2 and dg3 so they can build it"): DG1 hands the hypotheses on -> DG2 experiments / falsifiers <-> DG1 inner loops -> DG3 builds -> SM gate + mur -> trunk; rails: 8 KB base / 1 KB seed, sh + git + jq, no Python, 0 key bytes in any version, no new provider or spend, each host act its own belam GO.

## Invariants
- Every ref has ONE writer (out = the sender, held = the reader) and every move is an atomic update-ref: no shared file is rewritten, so the g1.40 race (an append lost to a concurrent mark-read rewrite) cannot happen.
- Nothing is delivered silently wrong: a lost CAS race is REPORTED (`cannot lock ref` / `[unsent]`), never silent; a forged or squatted commit is refused at read.
- The base stays <= 8,192 B and the seed <= 1 KB; everything here is expansion.
- Each HOST ACT (below) is its own belam GO, one at a time, with the exact command, the before-state and a one-command rollback sent to him first.

## Falsifier
1. On the real box once root installs `box`, the signers line and the carrier: 2 senders x 100 sends to one post while it reads in a loop the whole time = 200/200 delivered, 0 duplicates, 0 refused, each sender's order kept (alive's scratch: 200/200 in 5 s); 2 writers on the SAME channel x 50 with the retry = 100/100 delivered, 0 silent loss; the goal:g1.40 harness (6 writers x 150 against a looping reader) reports lost = 0.
2. Negative: `git grep -n -E 'sessions/inbox' -- <the box script + the carrier>` returns 0 hits, `wc -c` of the box script <= 2,005, and no Python file is on the send path.

## Out of scope
goal:g1.40 (the inbox-form fix: stays the fix until this lands, then closes) · AA2's per-post object stores and agi-carry's own build (goal:g7.16.1.11.12; this leaf USES agi-carry) · AA3 land (mail up one edge reuses `box read` as root: goal:g7.16.1.11.13) · K1 (per-spawn capped key), K2 (spawn classes) and K3 (direct inference): the other half of belam's 18:16Z relay, other owners.

## Agent Notes
Assigned to **director-general-1**.
