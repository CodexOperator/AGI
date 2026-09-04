---
id: goal:g14
mint_id: c721e86dd1c545f0abfcbcac486919c3
type: goal
parents: []
next_edges: []
confidence: 1.0
edited_by: director
goal_id: G14
goal_kind: long-term
heading_level: 2
origin: goals-doc
scaffold_hash: 7bceacd8528266d8
seeds: []
status: horizon
tags:
  - goal
  - root
thought_session: L1.13
title: "G14: Local-maxxing: the smallest model that can do the job, everywhere"
---
# goal:g14

## Agent Notes
**Owner goal, 2026-09-04: local-maxxing.** Use the smallest, fastest, most open
model that can do each job, everywhere it can be done — and make the graph itself
the thing that decides which model that is.

The shape:

- **Mechanistic tagging at creation.** Classifiers, encoders, or small tuned
  models assign a node its tags the moment it is minted, rather than a large
  model being asked to introspect (`goal:g5.2`, `goal:g1.12`).
- **Tags route the model.** Which model writes the next node is a function of the
  requested node's type, flavor tag and grain, given the node it follows in the
  chain. That is config, declared in the graph (`goal:g1`), never improvised per
  spawn.
- **Specialists get sharper over time.** Every routed call is training data for
  the model that serves that slot, so models become hyper-specialised per
  granularity, per loop flavor, per harness piece — narrow capability, tiny
  prompt, tiny output.
- **A lattice, not a ladder.** Many hyper-tuned models each doing one subtask,
  with classifiers and encoders breaking a goal into optimal sub-goals and the
  results stitched back together live at every zoom level — the way DNA is
  stitched during replication, or proteins working inside a cell. No single large
  model in the middle of the loop.

**Why it is a goal rather than an optimisation:** the director's context is the
scarce resource (measured across loop L1) and provider spend is the other. Both
fall out of the same fix — put the smallest competent model at every node and let
the graph, not a human, decide what competent means here.

Related: `goal:g4` (right model at the right grain), `goal:g4.2` (a
reasoning-effort dial), `goal:g4.4` (a web of specialists, each owning a region),
`goal:g2.4` and `goal:s32` (the embeddings pipeline this needs).
