---
id: goal:g7.16.1.11.31
mint_id: 7ae23e7148e74e49b1da350bb999696c
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.31
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 0e66e1a15d521992
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - v5
  - tests
  - baseline
  - g7.16.1.11
title: "G7.16.1.11.31: the engine FULL suite on E has a baseline -- 0 collection errors and a named owner for each remaining red (98 ids at trunk ce5b24d726)"
town: core
---
# goal:g7.16.1.11.31

## Why this exists
goal:g7.16.1.11: SM's gates now run on E (pytest 7.4.4), where the engine FULL suite at trunk ce5b24d726 gives 90 failed + 8 errors, the SAME 98 ids on a trunk tree and on the .13.2 range (SM's measure, mur wf_a4658ad9-02f; I have not rerun it): test_workflow* 82, test_grid_writers 5, test_agi_wt_archive 8 setup errors (TypeError 'module' / str: an order-dependent same-name module collision), test_commands::test_a_bare_first_word_runs_a_declared_command, test_schema_round1_empty_lists[doc-card-alive], test_rotate_prepare::test_rotate_self_pushes_only_unpushed_blocker_and_continues. And extensions/agi/tests/embeddings and extensions/agi/tests/renderers cannot be COLLECTED in a full run (SM: they collide with src/embeddings and src/renderers; alone they pass, 24 and 41). A gate that diffs "no new red against the trunk" has therefore been comparing against a baseline of 98 failures nobody owns.

## Target end-state
- The FULL suite on E reaches 0 collection errors: the two same-name collisions are resolved (rename or package the colliding directories; the mechanism is the implementing round's).
- Every one of the remaining reds has a NAMED owner and a one-line cause in a baseline node, or is fixed; none is "the baseline".
- The baseline node is the thing a gate diffs against, with the trunk sha and the pytest version it was measured at.

## Invariants
- No test is deleted or skipped to reach the count; a red either gets fixed, gets an owner, or is retired with its reason in the baseline node.
- The suite lock and the single-file discipline of the gate (agi-verify) stay as they are.
- A red that only reproduces on E is recorded as E-only with the pytest version, not fixed on another box.

## Falsifier
The deciding checks are pytest runs on E, not repo greps, so the first backticked command here is deliberately not harvest-eligible (agi-frontier reads it as mute, not met).
1. `python3 -m pytest extensions/agi/tests -q --co 2>&1 | tail -3` on E shows no `error` count (0 collection errors; today the embeddings and renderers directories error).
2. Every remaining red id in the FULL run appears in the baseline node with an owner (a lane or a script diffs the two id lists; empty difference = done).
3. Negative: `python3 -m pytest extensions/agi/tests/embeddings extensions/agi/tests/renderers -q` still passes alone (24 and 41 per SM), so the fix did not trade a collision for a loss.

## Out of scope
Fixing the 82 test_workflow reds themselves (each gets an owner here, a fix is its own round) · the engine's code under test · other boxes' baselines · SM's saved report (ask SM by box for it).

## RULE SM placement 09:5xZ 10-09, from belam [decision] 09:5xZ (SM's relay text; every number in it is SM's measure on E)
"(C) E FULL-SUITE BASELINE TRIAGE: on E (pytest 7.4.4) the engine FULL at trunk ce5b24d726 = 90 failed + 8 errors, the same 98 ids on a trunk tree and on .13.2: test_workflow* 82, test_grid_writers 5, test_agi_wt_archive 8 setup errors (TypeError 'module' / str: an order-dependent same-name module collision), test_commands::test_a_bare_first_word_runs_a_declared_command, test_schema_round1_empty_lists[doc-card-alive], test_rotate_prepare::test_rotate_self_pushes_only_unpushed_blocker_and_continues; and tests/embeddings + tests/renderers cannot be COLLECTED in a full run (they collide with src/embeddings, src/renderers; alone 24 + 41 pass). Falsifier: the FULL on E reaches 0 collection errors and a named owner per remaining red. My saved report: ask me by box."

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-09 06:5xZ: filed on SM placement 09:5xZ. HORIZON. Every number is SM measure on E (pytest 7.4.4, mur wf_a4658ad9-02f); I have NOT rerun the FULL. The deciding checks are pytest runs on E so the first backticked command is deliberately not harvest-eligible (mute, not met). No prior version.
<!-- THOUGHT:END -->
