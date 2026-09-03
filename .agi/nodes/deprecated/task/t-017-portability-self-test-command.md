---
id: task:t-017
mint_id: aa96b648a8714befa5e4f5f2b860cd00
type: task
parents:
  - hyp:graph-core-r9
acceptance_criteria:
  - R9.4 (self-test command verifies portability by reloading from temporary copy and comparing node counts and ids)
blocked_by:
  - task:t-016
cavekit_req: graph-core/R9
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-017: Portability self-test command"
---
**Description:** Implement `agi-tree self-test portability` CLI subcommand. Copies `context/` to a tempdir, loads from there, compares node counts and id lists with the original. Exit code 0 on match, non-zero with diff on mismatch.

**Files:** `agi-tree/src/graph_core/cli/self_test.py`, `agi-tree/tests/graph_core/test_self_test_portability.py`

**Test Strategy:** Invoke the subcommand on a fixture context dir; assert exit 0 and a "portable: yes" line in stdout.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R9` under `hyp:graph-core-r9`, whose disposition is disposition CLOSE-BY-SMALL-EXPERIMENT, not run: no dedicated portability self-test exists (no `test_portability.py`); the small experiment is an absolute-path audit plus copying `.agi/` to a tempdir and reloading it through the real loader -- hours, not architecture.
<!-- THOUGHT:END -->
