---
id: goal:g1.18
mint_id: 8a87df4b074943ed9e7b9e4304088224
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G1.18
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 886da3b453dee212
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: g1-g7-rewrite-2026-09-19
title: "G1.18: Graph-native handoffs — cite nodes, not essays; native tools over ad-hoc; Grok Bot functions eventually through the graph"
town: core
---
# goal:g1.18

## Why this exists

Parent `goal:g1` (engine / agent orientation). Owner 2026-09-19: minimize inter-bot token handoffs by citing graph nodes; prefer native AGI tools; long-term all Grok Bot functions through the graph.

## Owner bank (verbatim, 2026-09-19)

> sweet. stand by for batch completion. It'll be a while before you and your directors talk. That is the point: the graph allows you to minimize how many tokens you must pass manually back and forth between one another as outputs. If you check my openrouter use, it holds steady at 92-93% cached tokens which IDK if that's higher than average or not but that's what I've been staying at. The point is that you never have to take a thousand tokens to explain someting you can summarize by saying in 20 tokens "these graph nodes and these parts of these graph nodes specifically is what I am trying to tell you." And also the engine takes care of most of the manual calling and organizing as well so it's all way more automated. The goal is that even you bots will start using the native tools more and more over the built in ones because they are more convenient even with the setup you all have. Eventually I want it all to come full circle where all grokbot functions are done in the graph - through the graph. But that comes later, first just see what the parents brought in. Also for merg ups, we are using our custom git scripts right? They take care of things like signing each one and also verifying key ownership, rotation, etc. If you check git history you will see a cryptographic chain of authenticity in there somewhere. It's incomplete and insecure, but it does exist. Hardening comes later during the redesign

## Target end-state

- Inter-bot communication defaults to node citations (`goal:…`, `build:…`, ranges) instead of essay restatement.
- Agents prefer native graph tools (read/write/dispatch/workflow/send) over harness-built-in equivalents when both can do the job.
- Horizon: Grok Bot capabilities are reachable as graph operations (full circle), without abandoning the graph as source of truth.

## Invariants

- The graph is the cheap shared memory; chat is the thin pointer layer.
- Native tool convenience must win on the same task, or the tool is incomplete (file a residue, do not invent a parallel path).

## Falsifier

1. A director↔helper handoff that names only node ids + field ranges is accepted as complete brief for the next round (no required prose dump).
2. For a task that both a native AGI tool and a harness built-in can perform, the standing brief prefers the native tool by name.
3. "Full circle" is horizon: no claim that Grok Bot UI is already graph-native until an explicit later goal closes it.

## Related

- Merge-up authenticity / verify: `goal:g7.11`.
# goal:g1.18
