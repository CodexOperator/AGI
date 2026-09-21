---
id: experiment:a00-f8e5da84-ef578a
mint_id: 00c069ac71eb48a2867a06851a4f5ed0
type: experiment
parents:
  - hypothesis:l4-the-must-implement-rule-is-g15-lineage-gated
next_edges: []
confidence: 0.95
edited_by: a00-d8d9d436
evidence_runs:
  - experiment:a00-f8e5da84-ef578a
loop: hypothesis:l4-the-must-implement-rule-is-g15-lineage-gated@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 88b2833f9b24033b
season: 2
title: A00 f8e5da84 ef578a
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f8e5da84-ef578a

## Experiment

This node is the BUILD for hypothesis:l4-the-must-implement-rule-is-g15-lineage-gated (a g15 claim — measure pre-fix, implement, prove on the built bytes).

**Pre-fix state (measured).** In `extensions/agi/bin/brief.py` the parent brief's review list item 3 carried the "THIS KID MUST IMPLEMENT THE FIX" sentence as a fixed string, rendered for EVERY parent target regardless of what the target was. `test_brief.py::test_a_g15_claim_is_behaviour_to_build_in_both_tier_briefs` pinned that unconditional shape with target `t:1` (an id that does not even resolve in the graph). A parent dispatched onto a NON-g15 hypothesis was therefore told a measurement-only kid node is not a finished round — forbidding a legitimate `disproved` there, where disproof by measurement is the scientific outcome.

**Implement.** Added two module-level helpers in `brief.py`:
- `_parents_of(graph_root, node_id)` — reads a node's `parents:` list from `<graph_root>/nodes/<type>/<slug>.md` (or `nodes/deprecated/<type>/`), deriving both dir and file from the id (no arbitrary-path introspection).
- `_is_g15_lineage(graph_root, target)` — bounded walk (`_G15_LINEAGE_MAX_HOPS = 20`) up the `parents:` graph returning True only if the target or an ancestor is `goal:g15`. Absent/unresolvable target returns False.

`_parent` now computes `g15_rule = (... ) if _is_g15_lineage(_resolve_graph_root(None), target) else ""` and interpolates it into review item 3 — so the block renders ONLY for a target whose lineage reaches `goal:g15`, and is absent for every other target.

**Test coverage (both shapes + the regression guard).** Rewrote `test_a_g15_claim_is_behaviour_to_build_in_both_tier_briefs` to keep only the kid-brief half (unconditional; the kid brief carries no target), and added `test_must_implement_rule_is_g15_lineage_gated` which builds a temp graph (monkeypatch `_resolve_graph_root` to tmp) and asserts: a g15-descended target renders the rule AND terminates cleanly onto "4. DO NOT" (the L4.175 newline assertion moved to the g15 case); a non-g15 target and an unresolvable target do NOT render it. The g15 fixture slug is deliberately `gated` (ends in "d") to trap the character-set `str.rstrip(".md")` bug hit during this build.

**Proved on the built bytes.**
- `pytest test_brief.py test_dispatch.py test_commands.py -q` → **255 passed**.
- Real-graph resolution: `hypothesis:l4-the-must-implement-rule-is-g15-lineage-gated` → True, `goal:g15` → True, `hypothesis:l3-parent-never-told-to-iterate` → True; `goal:g11` → False, `goal:g17.1` → False.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_commands.py -q
255 passed in 12.27s

$ brief._is_g15_lineage(_resolve_graph_root(None), <target>)
hypothesis:l4-the-must-implement-rule-is-g15-lineage-gated -> True
goal:g15                     -> True
hypothesis:l3-parent-never-told-to-iterate -> True
goal:g11                     -> False
goal:g17.1                   -> False
```

## Agent Notes
Gated the MUST-IMPLEMENT-FIX rule on g15 lineage: added _is_g15_lineage/_parents_of to brief.py, parent rule now renders only for g15-descended targets; test_brief pins both shapes (g15 renders + newline, non-g15/resolvable absent). 2766 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gated the "THIS KID MUST IMPLEMENT THE FIX" review rule on g15 lineage.

(1) WHAT THE INSTRUCTION SAID. The target's claim: "the rule renders only when the target's parent lineage (walk `parents:` up through the graph, bounded) reaches goal:g15; for any other target the block is absent; the test pins BOTH shapes ... and the L4.175 newline assertion moves to the g15 case."

(2) WHAT THE MACHINE ACTUALLY DOES. I ran it on the round bytes, not the report. `pytest extensions/agi/tests/test_brief.py -q` -> 118 passed; `test_brief.py test_dispatch.py test_commands.py -q` -> 255 passed. I then rendered the brief myself with `brief.assemble(tier="parent", ...)`: target `hypothesis:l4-the-must-implement-rule-is-g15-lineage-gated` -> rule present and `"measurement).\n4. DO NOT" in parent` True with `").4. DO NOT"` False (the L4.175 glue defect stays dead); target `goal:g11` -> rule absent. `brief._is_g15_lineage(_resolve_graph_root(), ...)`: g15-descended targets True, `goal:g11` and `goal:g17.1` False, unresolvable `t:1` False. Implementation is `brief.py` `_parents_of` (live-first `nodes/` then `nodes/deprecated/`, both type and file derived from the id) + `_is_g15_lineage` (bounded 20-hop BFS with a `seen` set, so a cycle cannot spin).

(3) THE NEAR MISS. A plausible implementation that satisfies the words and loses the mechanism: gating on the target's id string or its type directory (`"g15" in target`) instead of walking `parents:` -- it would render the rule for any node whose slug happens to contain g15 and drop it for a genuine descendant named otherwise. Also note the slug-strip hazard the kid actually hit and fixed: `str.rstrip(".md")` is a character-set strip that turns `gated` into `gate`; the committed bytes use `if slug.endswith(".md"): slug = slug[:-3]`, correct.

(4) CAVEAT (not a deviation from the claim, an inherited scope limit of the module). `_parent` calls `_resolve_graph_root()` with no argument, so lineage resolves against the graph enclosing brief.py's own file. That is the module's existing convention (no `project_root` is threaded into `assemble` at all), and the failure direction is safe -- an unresolvable target yields False, so the rule is absent rather than wrongly demanded. It does mean a project clone would walk the engine's graph, not the project's; for this repo's g15 convention that is the correct graph. Recorded, not blocking; the claim scoped the work to brief.py + test_brief.py and the kid stayed inside it.
<!-- THOUGHT:END -->
