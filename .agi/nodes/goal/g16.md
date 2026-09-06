---
id: goal:g16
mint_id: 407ea8deeb4645a0bf0f89d99a5d97fc
type: goal
parents: []
next_edges: []
confidence: 1.0
edited_by: director
goal_id: G16
goal_kind: long-term
heading_level: 2
origin: goals-doc
scaffold_hash: b8d304fcfbc73ec9
seeds: []
status: active
tags:
  - goal
thought_session: agi-master-2026-09-06
title: "G16: Telemetry per node, propagated up the ladder"
---
# goal:g16

## Agent Notes
Per node at done and per session: model, harness, profile, tokens_in, tokens_out, cost_usd, accepted diff bytes (node plus payload, review-accepted only). Roll-up is a descendant sum along parents: outcome is its loop, bigger_outcome the LT goal, overview the season. Ratios: bytes per token and bytes per dollar, always beside aligned-outcome count; cost per aligned outcome is the ranking number. Secondary only, never a target, never read by an agent choosing what to do; it tunes the model lattice, goal:g14. Cost source is OpenRouter's per-generation endpoint through the per-spawn key, to be verified first. Design: .agi/context/season-ladder-and-morals-brief.md section 5. Horizon until L2 wave 2.