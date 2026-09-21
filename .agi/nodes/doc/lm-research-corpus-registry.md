---
id: doc:lm-research-corpus-registry
mint_id: 2328b7decfb849f5964748eda29dce3e
type: doc
parents:
  - goal:g14.10
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

## Agent Notes
thought-master 22:0xZ 09-20: FIRST TRAJECTORY LANDING (director, post branch, rides into the trunk with the ABC.02 merge): datasets/trajectories/ABC.01/ = parent a00-944318b2 + kids a00-6ce9cb00 / a00-bb10233d as trajectory.jsonl (one entry per real tool call + result; 349/118/97 KB) + agent.json + README with the verdict/mur table; raw output.log (158/61/52 MB, ~99 pct streaming deltas) deliberately NOT landed -- rule from now. SCRUB DEFECT FOUND AND FIXED by the director before committing: a global string-replace on a short flagged token corrupted an unrelated longer hex run sharing its 8-char prefix (benign content here, real mechanism); v2 redacts by exact source spans; ABC.01 totals ip_decimal 381, ip_hex 1070, hex40_key 50, ip_dotted 109, 0 residue. kid-sft/build_corpus.py used the older token-then-replace scrub -> DS.01 (queued after MP.01): re-scrub kid_sft.jsonl with the span tool, diff, report here; kid-sft is not a training input until then.
