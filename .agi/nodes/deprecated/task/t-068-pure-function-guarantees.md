---
id: task:t-068
mint_id: fe9e86d6b4d748ae94fece581dc0842a
type: task
parents:
  - hyp:renderers-r8
acceptance_criteria:
  - R8.1 (renderer invoked twice with same representation → equal outputs)
  - R8.2 (input representation unchanged after call)
  - R8.3 (no renderer reads env vars/files/network during render)
  - R8.4 (no renderer writes file or process state during render)
blocked_by:
  - task:t-067
cavekit_req: renderers/R8
edited_by: season.py
effort: M
origin: build-site
season: 1
status: deprecated
tags:
  - M
  - tier--1
thought_session: season
tier: -1
title: "T-068: Pure-function guarantees"
---
**Description:** Add a property-based test that runs each registered renderer twice on the same representation and asserts equal output. Snapshot the representation before and after to assert immutability. Use `unittest.mock` to patch `open`, `os.environ.__getitem__`, and `socket.socket` and assert no calls.

**Files:** `agi-tree/tests/renderers/test_purity.py`

**Test Strategy:** Cover all four criteria via a single test fixture run across all registered renderers.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `renderers/R8` under `hyp:renderers-r8`, whose disposition is disposition CLOSE-BY-SMALL-EXPERIMENT, not run: testable against the three existing renderers with no new code: call twice and assert equal, mock `open`/env/socket and assert no calls.
<!-- THOUGHT:END -->