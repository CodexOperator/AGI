---
id: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
mint_id: 0c4b7c466b1b4226ab2d601cb17d23e2
type: hypothesis
parents:
  - hypothesis:a00-1ff9316d-177aae
next_edges: []
edited_by: a00-394a4440
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
- TEST ROW LIST AS OF 24e16666d (restored by DH.495 from the bytes into `## Measured`, not `## TESTS`: it records the pre-fix measurement, not a plan). extensions/agi/tests/test_mem_cap_tasks_max.py (rows moved onto spawn.tasks_max + a live-config row = 150) + neighbourhood test_launch_memory_cap.py test_heal_mem_cap.py test_dispatch.py. Every pytest under `timeout 600`, --basetemp under /tmp. DROPPED CLAUSE: the original ended "No NEW test launches a real systemd scope (the pre-existing DH.421 row in test_mem_cap_tasks_max.py does, under its own cap -- mur-director-engine-5 DH.429-k2 caught the director brief overstating this)" — withdrawn, the fan-out rows NEVER SPAWN since DH.453.

## CLAIM
`resolve_tasks_max(cfg)` reads `spawn.tasks_max` (one cell, the one `resolve_memory_cap` sits beside), so on the live config every per-spawn scope carries TasksMax=150; `values.memcap.tasks_max` is read nowhere; an absent/non-numeric/<1 cell still falls back to the fail-closed default 96; AGI_TASKS_MAX still overrides for tests.

## Dispatch line
config-max: the value is the cell spawn.tasks_max (already committed; READ it, never write config.json) / template-max: none / code: the reader's key path + its docstring/comment.

## FALSIFIERS
- `grep -rn "memcap.*tasks_max\|\"memcap\").*tasks_max" extensions/agi/bin` hits a reader;
- `resolve_tasks_max(json.load(open('.agi/config.json')))` != 150;
- a cfg with spawn.tasks_max absent returns anything but 96.

## TESTS
- PRE-FIX STATE, measured before this hypothesis's kid (still the text as of 2026-09-27's DH.488 re-read; the reader itself is now correct): extensions/agi/bin/mem_cap.py `resolve_tasks_max` read `values.memcap.tasks_max` (absent on the live config) -> the shipped default 96 applied, not the owner's 150. The reader now reads `spawn.tasks_max`; DH.488 touched NO production line and did not re-measure this row.

## FILE SCOPE
extensions/agi/bin/mem_cap.py · extensions/agi/tests/test_mem_cap_tasks_max.py. Never .agi/config.json.

## CEILING
1 kid · <= 12 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
mur-director-engine-5 DH.429-k2: the director-authored TESTS line claimed no test launches a real systemd scope; test_mem_cap_tasks_max.py already does (DH.421). Corrected the brief text by the director; the code residues ride DH.443.
<!-- THOUGHT:END -->
