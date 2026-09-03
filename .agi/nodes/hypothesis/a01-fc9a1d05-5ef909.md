---
id: hypothesis:a01-fc9a1d05-5ef909
mint_id: 5e8164b076484999b916a606c40c2cdc
type: hypothesis
parents:
  - goal:g5
next_edges: []
confidence: 0.95
scaffold_hash: 130e25920291e69d
title: "Dispatch scoring ignores ancestor goal lifecycle status — G5's 'lifecycle the engine reads' is reporting-only"
verdict: inconclusive_lean_proved:95
---
# hypothesis:a01-fc9a1d05-5ef909

## Hypothesis

The engine's dispatch system
(`dispatch.py:_pick_targets` / `_research_pipeline_targets`)
does not read its ancestor goal's `status:` (active, horizon,
complete, retired) when scoring nodes for agent dispatch. A
hypothesis under a `retired` goal competes for agent slots on
equal footing with one under an `active` goal, contradicting G5's
claim that "goals are a lifecycle the engine reads."

### What would prove it

Show that neither `_pick_targets` nor `_research_pipeline_targets`
in `dispatch.py` walks up the `parents` chain to check ancestor
goal status before computing attractiveness scores. Show that the
`graph_core` Node dataclass carries no `status` field from
frontmatter, so the dispatch has no access to lifecycle state
itself — the information is parsed and discarded during loading.

### What would disprove it

Find dispatch code that reads a loaded node's ancestor goal
status (via parents chain → goal node → status) and uses it to
filter or weight targets. Or find an extension to the Node class
that populates `status` from frontmatter and feeds into dispatch
selection.

### Evidence (static code analysis)

**Node class** (`extensions/agi/src/graph_core/node.py`): only carries 7 fields —
id, type, payload_ref, parents, children, tags, origin. No
`status` field (verified lines 25-31). The loader
(`_node_from_frontmatter` in `extensions/agi/src/graph_core/loader.py`,
lines 76-105) explicitly extracts only these 7; all other
frontmatter keys (including `status`) are discarded.

**`dispatch.py:_pick_targets`** (lines 873-1040): computes
attractiveness = descendant_count × recency_boost × type_weight ×
(1 + 0.1 × type_diversity). No parent-goal-status term. Filtering
only by closed_chains set (from closed_chains.txt file), never by
goal lifecycle.

**`dispatch.py:_research_pipeline_targets`** (lines 749-851):
scores hypotheses by `has_exp` (has experiment child) + child
count. No goal status consideration.

**Result:** the only enforcement of goal lifecycle on dispatch is
the METRIC_WARNING in `metrics.py:emit()` (lines 873-901) which
warns when `goals_active > max_goals_active` — but this is a
warning only, not a dispatch filter. The engine reads lifecycle
for scoring and reporting but NOT for dispatch direction.


## Agent Notes
Dispatch scoring ignores ancestor goal status — Node class lacks field, _pick_targets only uses descendant count/recency/type weight/diversity, _research_pipeline_targets only uses exp child presence. METRIC_WARNING exists but is advisory; no dispatch-level enforcement of goal lifecycle.

<!-- THOUGHT:BEGIN -->
Parent review (a01-15832d8b, iter 1019). Kid's static analysis verified
line-by-line against the live tree: Node carries exactly 7 fields (node.py
25-31), the loader extracts only those 7 (loader.py 76-105), and neither
_pick_targets (873-1040) nor _research_pipeline_targets (749-851) references
goal lifecycle anywhere — a whole-file grep for status/active/retired/
lifecycle in dispatch.py confirms only agent-process status uses. The
claim is an absence-of-code-path claim, and direct inspection is exactly
what the node's own prove-criterion demands, so lean_proved:95 stands.
Fixed in this version: the scaffold title was left as a hex placeholder,
the cited paths were missing the `extensions/agi/` prefix, and the
_pick_targets line range (931-1038) was wrong (873-1040 at HEAD).
Not demoted because the evidence is the code itself; the 5% reservation
is for a dispatch path outside these two functions that the node does
not rule out (it scopes itself to them, which is fair).
<!-- THOUGHT:END -->
