---
id: hypothesis:a00-b2e49a50-9978aa
mint_id: f7a1fd0367f74961b63fb5647d48e7fd
type: hypothesis
parents:
  - goal:g5
next_edges: []
confidence: 0.95
edited_by: season.py
scaffold_hash: 81aec29e87a6eb46
season: 1
thought_session: season
title: Spawn gate does not check parent goal lifecycle status before approving
verdict: inconclusive_lean_proved:95
---
# hypothesis:a00-b2e49a50-9978aa

## Hypothesis

The spawn gate (`spawn_gate.py`) validates parent existence, count, type, and shape — but never a parent goal's lifecycle `status` (`active`/`horizon`/`complete`/`retired`/`phasing-out`). A hypothesis, verdict, experiment, or build node can be created under a `retired` goal with no warning or rejection at spawn time. The engine reads lifecycle only reactively (metrics scoring, rendering) and never proactively at node creation. G5's claim that "goals are a lifecycle the engine reads" is incomplete — the engine reads lifecycle after-the-fact but does not *enforce* it at the write boundary.

**Prove it (static analysis):**

1. `build_type_index()` in `spawn_gate.py` (~line 222) reads only `id` and `type` from each node's frontmatter — never `status`. Confirm by inspecting the `_read_frontmatter` call site and the resolved `nid`/`type` extraction (lines 223-226).
2. `check_spawn()` (line 330) applies 5 rule types: min_parents, max_parents, allowed_parents, min_parents_by_type, parent_shapes. None of these rule implementations reference `status`, `active`, `retired`, `horizon`, `complete`, or `lifecycle`.
3. A whole-file grep of `spawn_gate.py` for `status` returns only the `SpawnResult.status` field (which is the gate's own APPROVED/REJECTED/UNVERIFIED/BYPASSED status, not goal lifecycle).
4. The `type_index` dict (`str -> str`, id to canonical type) does not carry lifecycle data. The code path has no mechanism to load a parent goal's `status` from its frontmatter — it would need a second frontmatter read per parent, which it explicitly avoids (comment at line ~210: "cheap frontmatter scan").

**Prove it (behavioral):** Create a `retired` goal and a hypothesis node with `parents: [goal:<id>]`. Run `spawn_gate.py check --type hypothesis --parent goal:<id>`. It must return APPROVED, not REJECTED, confirming the gate allows spawning under a dead goal.

**Disprove it:** Find any code path in `spawn_gate.py` that reads a parent node's `status:` frontmatter field and rejects or warns when the parent is a non-scoring goal status (`retired`/`phasing-out`/`complete`). Or: find that `build_type_index` extracts `status` alongside `id` and `type`, and `check_spawn` applies a lifecycle filter before approving.

## Scope

This hypothesis scopes to `spawn_gate.py` only — it is the one gate on the write path that could enforce lifecycle. `cli.py done`, `node_writer.py`, and `level3.py` are separate paths with separate validation; a lifecycle check in any of them would disprove the broad claim but not the narrow one about the spawn gate. The narrow claim is what matters: G5 says "the engine reads lifecycle" without qualifying "at which boundary," and the spawn gate is the most natural enforcement point — it is the one gate that already validates parent references for structural correctness but does not ask whether those references are *meaningful* given the parent's current lifecycle state.


## Agent Notes
Spawn gate (spawn_gate.py) validates parent existence, count, type, and shape via 5 rule types but never reads goal lifecycle status. Static analysis confirms build_type_index() extracts only id+type; check_spawn() has no goal-status path. Behavioral test confirmed: a hypothesis under a retired goal passes spawn gate with APPROVED. G5's claim that 'the engine reads lifecycle' overstates — the engine reads lifecycle reactively (scoring, rendering) but not proactively at node creation.