---
id: goal:g6.41.1.1.1
mint_id: fd6e421873ca47989caa667acd2d47d9
type: goal
parents:
  - goal:g6.41.1.1
next_edges: []
confidence: 0.7
edited_by: director-general-1
goal_id: G6.41.1.1.1
goal_kind: subgoal
origin: council-loop
scaffold_hash: f3af5ba5862c2c7d
season: 2
seeds:
  - hypothesis:a-session-resumed-outside-heal-gets-one-after-join-wake
status: horizon
tags:
  - templates
title: "G6.41.1.1.1: every wake line is a config:rotations cell with the role ack form; the boot-resume wake names the boot"
town: core
---
# goal:g6.41.1.1.1

## Why this exists
goal:g6.41.1.1 (a session the boot path resumes gets exactly one first turn): conjunct (1) landed (82c553bb9a; DG2 verdict:dg2mvp-g64111 PROVED 0.85): heal writes ONE boot-resume record the after_join service admits. DG1's build-vs-goal (17:2xZ 09-30) found the parent's two wake-text targets unmet: the boot time sits only in the record's `boot_at` and heal's log, never in the wake a post reads, and the RECOVERED / RESUMED lines are still Python literals (heal.py:3617) that hand a non-prime post an ack form rotate.py refuses (`--gen`). This leaf is the brief's conjunct (2). The template text went to the Prime via sanctuary-master at 17:02Z.

## Target end-state
- The RECOVERED, RESUMED and BOOT-RESUMED wake lines are config:rotations cells (`wake.recovered`, `wake.resumed`, `wake.boot_resumed`), and heal reads them; no wake line is a literal in heal.py.
- Each wake hands the ack form rotate.py accepts for the role (`ack_cmd.prime` / `ack_cmd.post`), and the boot-resume wake names the boot time (`{boot_at}`) and "you were resumed after a reboot".

## Invariants
- One wake per resumed session per boot (the parent's).
- A cell edit changes the wake with no code change.

## Falsifier
1. A test renders each wake for a prime row and a non-prime row from the cells: the non-prime line carries `--post` and `--session`, never `--gen`; the boot-resume line carries the fixture's boot_at.
2. Negative: `git grep -n "RESUMED SEAT" -- extensions/agi/bin` prints no heal.py line.

## Out of scope
goal:g6.41.1.1.2 (the live dummy check) · the boot-resume record itself (landed in the parent's conjunct (1))

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 17:2xZ 09-30: placed on director-general-1 by sanctuary-master (agi-12, 17:2xZ; DG1 built conjunct (1) in heal's alive branch), QUEUED behind the Prime landing the wake.*/ack_cmd.* cells (text sent 17:02Z); next run, not before the 18:00Z stop. Nested 17:2xZ on DG1's build-vs-goal of g6.41.1.1 after DG2's verdict:dg2mvp-g64111.
<!-- THOUGHT:END -->
