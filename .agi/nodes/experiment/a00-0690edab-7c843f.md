---
id: experiment:a00-0690edab-7c843f
mint_id: 3d5d6490f7874dc4a8e893317db937fe
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.8
edited_by: season.py
scaffold_hash: 776239a4e382c4c3
season: 1
thought_session: season
title: A00 0690edab 7c843f
verdict: inconclusive_lean_disproved:80
---
# experiment:a00-0690edab-7c843f

## Experiment

Four prior experiments under this hypothesis (a00-ed477860-8f3343, a00-dc51bea8-loop-scoped-ids-not-end-to-end, a01-7a49270a-a6b875, and 11+ others) all performed static code reading — no one ran the actual falsifier test the hypothesis describes. This experiment adds DYNAMIC empirical evidence to confirm and extend the static findings.

Ran a custom Python script (`/tmp/exp-clobber-test.py`) that simulates the driver.sh scenario:

**Test 1 — Manifest merge (goal:s28)**
Two dispatches into the same iter dir, each writing a different agent. `_merge_manifest` reads existing manifest, merges by agent id, writes back.
→ PASS: both agents survive (2 agents in final manifest). The goal:s28 guard works.

**Test 2 — iter-NNN-graph.json is unguarded**
Write an initial graph.json with 3 nodes, then overwrite it with 1 node (simulating a second driver.sh run targeting the same iter dir).
→ PASS: graph.json is a plain overwrite — original data lost, only 1 node remains. NO merge protection exists for graph.json, as the static reads predicted but never tested.

**Test 3 — sesssions/iter-001 on disk**
Confirmed `.agi/sessions/iter-001` holds real historical data (1 agent in manifest, 330KB graph.json). A fresh `driver.sh --max-iters 1` run would target this exact directory — nothing in `driver.sh`'s `seq 1 "$MAX_ITERS"` loop checks for existing content before writing.

### Verdict on the hypothesis

Two claims bundled, resolved:

1. **"A fresh driver.sh run cannot overwrite an existing .agi/sessions manifest"** — Partially disproved in scope: `manifest.json`'s `agents` list IS protected by `_merge_manifest` (goal:s28), but `iter-NNN-graph.json` IS a plain overwrite. The hypothesis claimed the protection came from loop-scoped ids; the real protection comes from the merge discipline, which is narrower than "cannot clobber".

2. **"Iteration ids are loop-scoped (L<loop>.<nn>) end to end"** — Disproved. No code path formats or parses this scheme. `driver.sh:239` still does `seq 1 "$MAX_ITERS"`, restarting at 1 every run. The `L1.01..L1.09` labels exist only as hand-typed commit subjects and 3 ad-hoc directory names.

This experiment builds on and confirms the prior findings. The only new empirical contribution is Test 2 (graph.json overwrite confirmed dynamically).

## Evidence

Script: `/tmp/exp-clobber-test.py` — all 3 tests pass.

```
TEST1 PASS: manifest merge protects agent entries across dispatches (2 agents)
TEST2 PASS: iter-NNN-graph.json IS an unguarded plain overwrite (confirmed)
TEST3: iter-001 has 1 agents — real historical data, not a stub
TEST3: iter-001-graph.json exists (330134 bytes) — would be plain-overwritten
TEST3 PASS: confirmed .agi/sessions/iter-001 is populated and would be targeted by a fresh driver.sh run
```

Supporting evidence:
- `extensions/agi/driver.sh:239` — `for i in $(seq 1 "$MAX_ITERS")` — no allocator, no next-free-id check.
- `extensions/agi/bin/dispatch.py:335-354` — the real guard (goal:s28 merge).
- `extensions/agi/tests/test_dispatch.py` — 34 tests, all pass, including `test_merge_preserves_the_parent_when_a_kid_dispatches_into_the_same_iter`.
- `.agi/sessions/iter-001/` — populated manifest + 330KB graph.json, real historical data.
- Full test suite: 1454 passed.

## Agent Notes
Dynamic falsifier: all 3 tests pass. Confirms prior static findings: manifest merge works (goal:s28, agents list protected) but graph.json IS unguarded plain overwrite. driver.sh seq 1..MAX_ITERS never checks for existing sessions dir. 1454 tests pass.