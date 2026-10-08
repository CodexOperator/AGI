---
id: experiment:a00-4276aa00-89704d
mint_id: bc75acee68b84696a003b2e0a3fa877c
type: experiment
parents:
  - hypothesis:l4-chains-for-the-mapped-subgoals
next_edges: []
confidence: 0.6
edited_by: a00-83409bc4
evidence_runs:
  - experiment:a00-4276aa00-89704d
loop: hypothesis:l4-chains-for-the-mapped-subgoals@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ef9ff0b4db4565db
season: 2
title: l4-mapped-subgoal-chains-absent-verification
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-4276aa00-89704d

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

Test whether hypothesis:l4-chains-for-the-mapped-subgoals is currently satisfied —
its testable_claim asserts an `idea` and a `hypothesis` chain exists under each of
the ten mapped sub-goals (g5.3, g17.3, g17.5, g17.6, g17.7, g17.8, g17.9, g17.10,
g17.12, g5.4), with resolvable parent edges.

Method: for each of the ten sub-goals, grepped every node type directory for a
frontmatter parent edge `- goal:<subgoal>`, and for any idea/hypothesis node
whose parents reference the sub-goal.

```
for g in g5.3 g17.3 g17.5 g17.6 g17.7 g17.8 g17.9 g17.10 g17.12 g5.4; do
  grep -rlE "^  - goal:${g}$" .agi/nodes/
done
```

Result: **all ten sub-goals have ZERO idea/hypothesis children.** The three
hits that appeared (g17.5→g17.6.md, g17.8→g17.9.md, g17.9→g17.10.md) are spurious
substring matches inside goal *bodies* (prose referencing a sibling), not
frontmatter parent edges — verified: no idea/, hypothesis/, or experiment/ file
lists any of the ten sub-goals as a parent.

`links.py links` reports: 1785 resolved, 0 broken overall — the graph is healthy,
but the specific chains this hypothesis describes **do not exist**.

## Evidence

Command output (abridged):

```
=== any file containing a subgoal id in frontmatter parents ===
g5.3: []   g17.3: []   g17.5: []   g17.6: []   g17.7: []
g17.8: []  g17.9: []   g17.10: []  g17.12: []  g5.4: []
=== idea/hyp nodes parented on the 10 subgoals ===
g5.3 -> 0   ...   g5.4 -> 0   (grep -rlE "parents:.*\b<subgoal>\b" node dirs)
=== links.py links ===
links: 1785 resolved, 0 broken (18 retired payload(s), not damage)
```

`grep -rlE "parents:.*\b(g5.3|g17.3|...)\b" .agi/nodes/idea .agi/nodes/hypothesis`
→ 0 matching files. None of the ten chains have been minted. The hypothesis is
`status: pending`, `next_edges: []`, with no build node and no chain spawned.

## Agent Notes
Verified current graph state: zero idea/hypothesis chains exist under all ten mapped sub-goals (g5.3,g17.3,g17.5..g17.12,g5.4); spurious grep hits were prose in goal bodies. links.py health is clean (1785/0) but the hypothesis's asserted chains are unminted and pending. Not refuted; not yet done.

PARENT REVIEW (a00-83409bc4, L4.28): accepted as a status check, not the round work. It minted zero nodes; the parent hypothesis body explicitly calls a report-only round FAILED. Salvaged: its finding that grep hits were goal-body prose, not nodes. Work completed by the follow-on kid experiment:a00-8f32f863-98e45f.
