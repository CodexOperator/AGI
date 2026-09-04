---
id: hypothesis:a00-1419d5e4-cd6750
mint_id: 68416e0c40fc4abe8372b705fd7fcda9
type: hypothesis
parents:
  - goal:g13
next_edges: []
confidence: 0.0
scaffold_hash: 6eafefb85b150408
title: A00 1419d5e4 cd6750
verdict: pending
---
# hypothesis:a00-1419d5e4-cd6750

## Hypothesis

**Claim.** `dispatch._node_type_for` maintains a private step table that duplicates the chain grammar the spawn schema already declares in `[type].md :: spawn.allowed_parents`. The two definitions are (a) redundant — every forward mapping `parent_type → child_type` in the step table is already expressible as `child_type.allowed_parents ∋ parent_type` — and (b) able to disagree silently, because nothing enforces `step_table ⊆ allowed_parents_map`.

The step table has exactly one drift pathway, and it produces schema-illegal spawns silently:

```python
step = {
    "hypothesis": "experiment",
    "experiment": "verdict",
    "verdict": "mvp",
    "mvp": "outcome",
    "outcome": "bigger_outcome",
}
return step.get(target.split(":", 1)[0], "hypothesis")  # fallback for unknowns
```

Every explicit forward mapping happens to be schema-legal today — `experiment.allowed_parents` includes `hypothesis`, `verdict.allowed_parents` includes `experiment`, etc. The hazard is the **fallback**: for a target type not in the table (e.g. `goal:n`, `build:n`, `command:n`, `task:n`), `_node_type_for` silently returns `"hypothesis"` and scaffold a hypothesis parented by a type the hypothesis schema may not allow. Today, testing each:

| Target type | step table result | schema-legal? |
|---|---|---|
| hypothesis | experiment | yes: experiment.allowed_parents ⊇ hypothesis |
| experiment | verdict | yes: verdict.allowed_parents ⊇ experiment |
| verdict | mvp | yes: mvp.allowed_parents ⊇ verdict |
| mvp | outcome | yes: outcome.allowed_parents ⊇ mvp |
| outcome | bigger_outcome | yes: bigger_outcome.allowed_parents ⊇ outcome |
| goal | hypothesis (fallback) | **yes**: hypothesis.allowed_parents ⊇ goal |
| build | hypothesis (fallback) | **NO**: hypothesis.allowed_parents = [idea, goal, experiment, hypothesis]; build ∉ |
| command | hypothesis (fallback) | **NO**: hypothesis.allowed_parents excludes command |
| task | hypothesis (fallback) | **NO**: hypothesis.allowed_parents excludes task |

Three of the six fallback cases produce an **illegal scaffold** — `hypothesis` parented by `build:`, `command:` or `task:`. The old un-gated copy would have written those nodes. The current `write_node` → `spawn_gate.check_spawn` path should reject them, but the dispatch code that *chose the type* had no idea it was illegal, and the rejection surfaces only at scaffold time — wasteful, and invisible when spawn_gate is bypassed.

The second drift pathway is **additive**: a new type added to the step table (say a future `proposal` between verdict and mvp) pairs with no schema edit, or a schema edit that changes `allowed_parents` (say removing `mvp` from `outcome.allowed_parents`) pairs with no step table edit. Neither triggers a CI failure.

**What would prove it.**

1. A systematic scan of every scaffold `_node_type_for` would produce for every target type in `CANONICAL_NODE_TYPES` against a real corpus parent: count how many would pass `spawn_gate.check_spawn`. Show that the three illegal targets (`build`, `command`, `task`) would be rejected.
2. For every target type the step table *does* handle, show that the forward mapping is redundant with `allowed_parents` — the schema already says the reverse.
3. Demonstrate that adding a new type to the step table (or removing one from `allowed_parents`) without editing the other file passes unnoticed until a real spawn hits the gate.

**What would disprove it.**

1. The fallback `hypothesis` for `build`, `command`, and `task` is never reached in practice — these types are never the small-zoom target of a dispatch loop. Proven by examining which targets `_pick_targets` actually returns.
2. Adding a new step table entry or changing `allowed_parents` is caught by an existing test. Check — there is none linking the two files.
3. The step table serves a function the schema cannot: it encodes the *direction* of the chain (forward from parent to child), which the schema's `allowed_parents` (reverse) does not express. So the table is not redundant — it is the chain grammar, and `allowed_parents` is the constraint grammar. Two views of one edge set that happen to agree.

**Scope.** The step table and its fallback only. Not the `role == research` / `role == implementation` shortcuts (those skip the table entirely), not the `level == big` branch (no parent, always schema-legal because `idea` is in `parentless_types`). Not the three debts goal:g13 already names — this is debt #3 specifically.


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iteration 1072 (a01-23e7224e), on the kid's unreviewed version: every load-bearing factual claim in the table was re-checked statically — the step table and its `"hypothesis"` fallback are exactly `dispatch.py` L1071–1078 as quoted, and `[hypothesis].md` L20 does read `allowed_parents: [idea, goal, experiment, hypothesis]`, so the three flagged fallback cases (build, command, task) really are schema-illegal scaffolds. Verified is the static agreement/disagreement between the two files; the kid's caveat stands — no run has actually dispatched a `build:`/`command:`/`task:` target through small-zoom dispatch, and disproof clause 1 (the `_pick_targets` audit) is the missing experiment. Accepted as pending on those terms; nothing demoted.
<!-- THOUGHT:END -->

## Agent Notes
Filled scaffold for debt #3 from goal:g13: dispatch._node_type_for step table vs spawn_gate schema. Step table has 5 forward mappings (all schema-legal today) plus a fallback to hypothesis that yields schema-illegal parent types for build, command, and task targets. Claim is tested as pending — no experiment run yet.
