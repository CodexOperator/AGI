---
acceptance_criteria:
  - R8.1 (renderer invoked twice with same representation → equal outputs)
  - R8.2 (input representation unchanged after call)
  - R8.3 (no renderer reads env vars/files/network during render)
  - R8.4 (no renderer writes file or process state during render)
blocked_by:
  - task:t-067
cavekit_req: renderers/R8
effort: M
id: "task:t-068"
mint_id: fe9e86d6b4d748ae94fece581dc0842a
origin: build-site
parents:
  - hyp:renderers-r8
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-068: Pure-function guarantees"
type: task
---

**Description:** Add a property-based test that runs each registered renderer twice on the same representation and asserts equal output. Snapshot the representation before and after to assert immutability. Use `unittest.mock` to patch `open`, `os.environ.__getitem__`, and `socket.socket` and assert no calls.

**Files:** `agi-tree/tests/renderers/test_purity.py`

**Test Strategy:** Cover all four criteria via a single test fixture run across all registered renderers.
