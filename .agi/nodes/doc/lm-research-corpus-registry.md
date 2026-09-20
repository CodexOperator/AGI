---
id: doc:lm-research-corpus-registry
mint_id: 2328b7decfb849f5964748eda29dce3e
type: doc
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
payload_ref: datasets/README.md
scaffold_hash: 93622f030e59b454
season: 2
title: "Research corpus registry (owner 21:4xZ 09-20: are we storing the synthetic, preclassified datasets our evals generate?) -- what is stored, where, how labelled, what is lost, and the standing landing rule"
town: core
---
<!-- BODY:BEGIN -->
# doc:lm-research-corpus-registry

**Payload = `datasets/README.md`** — the archive explainer at the repo root is the source of truth (owner 21:5xZ 09-20: a separate, easy-to-find, easy-to-browse archive with its own explainer doc built into the graph). Read the file; this node carries the link, the notes and the history.

Archive layout (2026-09-20): `datasets/kid-sft/` (354 labelled kid rounds) · `datasets/jev-typed-acts/` (4,465 typed acts + 1,110 verdict-labelled replay rows) · `datasets/humaneval-abc/` (3 × 164 scored coding completions; symlink until ABC.02 lands) · `datasets/workflow-runs/trove-survey-2026-09-20/` (16 stage JSON). Not yet archived: parent/kid pi trajectories (landed by the director from ABC.02 on, scrubbed) and a deepseek-v4.1-flash reference row.
