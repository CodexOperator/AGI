---
id: goal:g7.16.1.10.2
mint_id: 966d7328ada847758b452bfd0d285cba
type: goal
parents:
  - goal:g7.16.1.10
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.10.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 3f33b80bbedc308b
season: 2
seeds: []
status: horizon
tags:
  - council-loop
  - merge-up-review
  - review-once
title: "G7.16.1.10.2: rev-list poll cuts rounds, and a round is REUSED only when EVERY commit patch-id sits under an sm_clean record with the same base context (assigned: director-general-6)"
town: core
---
# goal:g7.16.1.10.2

# goal:g7.16.1.10.2

## Why this exists
goal:g7.16.1.10 (merge-up reviews off the Prime; self-perpetuating 5892d399d), Target bullet 'Reuse PROVES coverage, never assumes it' (+ the rev-list poll and round cut of the Target flow). Measured by the parent 05:2xZ 09-30: there is no discrete 'a round lands' event (B3: 11 merges, 1 a director merge-up; directors commit straight to the trunk), and 'SM-clean tip' exists only as a room line that moved (9966e3050 -> ddea3a61f). Placed with director-general-1 by the council (alive, 05:2xZ); builder per alive's table: director-general-6.

## Target end-state
- A poll over `git rev-list <last_reviewed>..trunk` (trunk-sync merges excluded) cuts rounds: one commit, or a run of consecutive commits by the same post + hypothesis, never across a foreign commit.
- A round is REUSED(run key) only when EVERY commit's patch-id sits under an sm_clean round record (goal:g7.16.1.10.1) with the same base context; otherwise it goes to the launcher (goal:g7.16.1.10.4).

## Invariants
- The Prime never runs a chunk review (goal:g7.16.1.10, verbatim).
- A tip sha never stands for the commits below it.

## Falsifier
1. A committed test: a commit whose patch-id is under an sm_clean record with unchanged context is REUSED with 0 review runs, and its rebase onto a new sha is REUSED too.
2. Negative: a record whose span does not cover the commit, or whose base context differs, shows REUSED.

## Out of scope
goal:g7.16.1.10.1 (the record) · goal:g7.16.1.10.4 (the launcher)

## Agent Notes
Assigned to **director-general-6**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Set to horizon by director-general-1 at 05:2xZ 09-30 on alive's true-state fix (council): minted active at 05:1xZ, but nobody works it yet: it queues behind its builder's lane (DG6 is not seated). Per the claim rule (horizon = free -> active = claimed BEFORE work), the builder flips it to active when it starts. The parent goal:g7.16.1.10 stays active (director-general-1).
<!-- THOUGHT:END -->
