---
id: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
mint_id: 0c4b7c466b1b4226ab2d601cb17d23e2
type: hypothesis
parents:
  - hypothesis:a00-1ff9316d-177aae
next_edges: []
edited_by: director-engine
scaffold_hash: 2b76fd5380d914b6
season: 2
testable_claim: "mem_cap.resolve_tasks_max reads spawn.tasks_max (150 on the live config, TMM.263 (2)) and values.memcap.tasks_max is read nowhere; absent or bad cell falls back to the fail-closed 96; AGI_TASKS_MAX still overrides (assigned: director-engine)"
title: Per spawn tasks max reads the spawn tasks max cell
town: core
---
# hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell

## Measured
- TMM.263 (2), OWNER 19:5xZ via the Prime 20:13Z: the per-spawn scope's TasksMax is the cell `spawn.tasks_max` = 150, beside `spawn.memory_max` (2G). Committed by the director at 684a83a3a (.agi/config.json spawn.tasks_max: 150).
- PRE-FIX STATE, measured before this hypothesis's kid (DH.495 re-dates this row from the bytes: the reader itself is now correct): extensions/agi/bin/mem_cap.py `resolve_tasks_max` read `values.memcap.tasks_max` (absent on the live config) -> the shipped default 96 applied, not the owner's 150. The reader now reads `spawn.tasks_max`; DH.488 touched NO production line and did not re-measure this row.

## CLAIM
`resolve_tasks_max(cfg)` reads `spawn.tasks_max` (one cell, the one `resolve_memory_cap` sits beside), so on the live config every per-spawn scope carries TasksMax=150; `values.memcap.tasks_max` is read nowhere; an absent/non-numeric/<1 cell still falls back to the fail-closed default 96; AGI_TASKS_MAX still overrides for tests.

## Dispatch line
config-max: the value is the cell spawn.tasks_max (already committed; READ it, never write config.json) / template-max: none / code: the reader's key path + its docstring/comment.

## FALSIFIERS
- `grep -rn "memcap.*tasks_max\|\"memcap\").*tasks_max" extensions/agi/bin` hits a reader;
- `resolve_tasks_max(json.load(open('.agi/config.json')))` != 150;
- a cfg with spawn.tasks_max absent returns anything but 96.

## TESTS
extensions/agi/tests/test_mem_cap_tasks_max.py (rows on spawn.tasks_max + a live-config row = 150) + neighbourhood test_launch_memory_cap.py test_heal_mem_cap.py test_dispatch.py. Every pytest under `timeout 600`, --basetemp under /tmp. No test in this family launches a real systemd scope (DH.453 removed the DH.421 spawn rows).

## FILE SCOPE
extensions/agi/bin/mem_cap.py · extensions/agi/tests/test_mem_cap_tasks_max.py. Never .agi/config.json.

## CEILING
1 kid · <= 12 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude.

## ROUND EG.1 -- the post-branch RED between two merged chains (director-engine, first round of the EG series: belam [decision] 00:0xZ 09-28 reset the DH counter)
Measured   post branch bf2430484: test_boxkit_probe.py::test_spawn_rows_target_the_config_and_the_resolvers_not_a_literal FAILS (1 failed, 365 passed over the 23 touched test files): assert (150, 150, 'ok') == (150, 96, 'DRIFT'). The fixture drives the drift through values.memcap.tasks_max (test:85, :550) while this node's chain (merged 1ee2340c3) made mem_cap.resolve_tasks_max read spawn.tasks_max (mem_cap.py:73-82) -- two merged chains disagree on which cell the resolver reads.
CLAIM      the boxkit probe's spawn.tasks_max row and its test agree with the ONE cell this node names (spawn.tasks_max via mem_cap.resolve_tasks_max): a resolver/cell disagreement is still reported as DRIFT, driven through a path production can take (e.g. the resolver's env override), and no test or probe reads values.memcap.tasks_max as the tasks bound.
Dispatch line  config-max: spawn.tasks_max is the one cell (no new cell) · template-max: none · code: the probe row / test fixture follow the resolver; never bring back a second cell
FALSIFIERS the named test still fails · any probe/test path still sets or reads values.memcap.tasks_max as the bound · the DRIFT case is removed rather than re-driven
TESTS      test_boxkit_probe.py test_mem_cap*.py (if present) + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE)
FILE SCOPE extensions/agi/tests/test_boxkit_probe.py · extensions/agi/boxkit/probe.py (the spawn.tasks_max row only) · the kid's own node
CEILING    HARD CAP: 1 kid · <= 8 production lines net · <= 30 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT     paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.1 (first round of the reset EG series, belam [decision] 00:0xZ 09-28): the post branch carries a red between this chain (merged 1ee2340c3: resolve_tasks_max reads spawn.tasks_max) and the boxkit probe test that still drives values.memcap.tasks_max; found by the merge-up run over the 23 touched test files, declared in the merge-up, fixed here rather than by hand (a director writes no engine code).
<!-- THOUGHT:END -->
