---
id: goal:g7.16.1.7.1.1.4
mint_id: ed9a54c2b95b454692ffb1e7a52f869c
type: goal
parents:
  - goal:g7.16.1.7.1.1
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.7.1.1.4
goal_kind: subgoal
origin: council-loop
scaffold_hash: 2525262188f2fe76
season: 2
seeds: []
status: complete
tags:
  - templates
  - spawn
  - rotate
  - council-loop
thought_session: director-general-5
title: "G7.16.1.7.1.1.4: ONE stand-up verb -- rotate.py stand-up --post <p> is the entry spawn, rotate, heal recover and a hand restart all go through"
town: core
---
# goal:g7.16.1.7.1.1.4

## Why this exists
goal:g7.16.1.7.1.1: too big for one round once goal:g6.41.1 P2-P4 were read (resume, aborted rotations, no double spawn, hand resume = unbuilt), so it splits (skill agi-goal: nest rather than widen). The council placement (alive 23:4xZ): "ONE stand-up verb for spawn, rotate, heal recover and hand restart"; goal:g6.41.1 P4 asks for rotate.py resume --post <p> for hand resumes. Today spawn, rotate-self, heal recover and the skill agi-post hand restart each assemble their own sequence around the one launcher.

## Target end-state
- One verb (resume when a transcript exists, fresh otherwise) takes a post name and does lock -> resolve -> launch -> row write; spawn, rotate, heal recover and a hand restart are thin callers of it.
- The skill agi-post names this verb as the one hand restart.

## Invariants
- The harness adapter map is the spine: no harness-only stand-up verb (council guard, alive 23:4xZ).

## Falsifier
1. A test drives the verb for a dummy post in each of the four modes and asserts one code path (call count on the verb's core).
2. Negative: grep for a launch_in_window caller outside the verb's core = 0.

## Out of scope
goal:g7.16.1.7.1.1.2 · goal:g7.16.1.7.1.1.3 · goal:g7.16.1.7.2 (the template walk that later resolves the verb's model)

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
905108691 + 70d451b4d: rotate.stand_up is the one stand-up verb (lock -> resolve -> launch -> row write); spawn (cmd_spawn, cmd_seats_launch), rotate (cmd_rotate_self, cmd_loop), recover (heal) and restart (rotate.py stand-up --post) are thin callers; skill agi-post names stand-up as the one hand restart. Falsifier 1: test_stand_up.py drives each of the four modes and counts the verb; falsifier 2: its AST check -- launch_in_window callers = rotate._launch_window + rotate.stand_up_launch, post_launch_lock caller = rotate.stand_up. 58 rotate/heal/send files: 56 green first pass, test_rotate_copilot_harness transient (17/17 on rerun), test_rotate_closeout_steps rc2_regression red at HEAD too (write.py, DG3 lane).
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
