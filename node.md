---
id: goal:g14.10.2
mint_id: 4bee9811f20e4d7ba3cf3c54989435ff
type: goal
parents:
  - goal:g14.10
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G14.10.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: f6779e03a26a53a5
season: 2
status: active
tags:
  - local-maxxing
  - datasets
  - corpus
  - sessions
title: "G14.10.2: THE SESSION-DATA TRUNK + CLASSIFIER PASS -- every role's session data (pi parents/kids, claude-code masters/directors/Prime) scrubbed into datasets/sessions/, pre-labelled from the graph, then a jev classifier pass over all data trunks calibrated on a 200-record hand-checked slice (owner 02:1xZ 09-21)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.10.2
## Agent Notes
**Owner source (2026-09-21 02:1xZ, verbatim on goal:g14, relayed via goal:g14.10's thought-master program block):** "Use all session data all parents kids and all other roles generate and find a way to pre-label it or even use jev to do an in-depth classifier pass on all the data trunks including things like model, harness, provider etc."

**Commits to.** Capture EVERY role's session data: pi parents + kids (already land under `datasets/trajectories/` via the standing landing rule) AND claude-code roles -- masters, directors, the Prime -- whose session jsonl lives under the harness dir today and nowhere in the archive. All of it lands under `datasets/sessions/<role>/<session>/` through the ONE scrub (`datasets/tools/scrub.py`), never a second redactor. The claude-code capture HOOK itself (the mechanism that copies a harness session dir into the landing path) is `G14.14.8`, director-engine's engine round -- this node commits to the data-trunk shape and the labelling, not the hook.

**Invariants.** Pre-label every record from what the graph ALREADY knows before any classifier runs: model · harness · provider · role · post · town · round id · verdict · mur residue class · spend · wall · box. Only THEN does a jev classifier pass add classes the graph does not carry: act type, reasoning shape (prose vs diagram-maxed), refusal, tool-error, rebrief -- calibrated against a 200-record hand-checked slice, never trusted unvalidated. CPU/API only, no GPU (thought-master's own order line). Nothing lands unscrubbed; a leak hit blocks the commit (G14.10 rule); the index (`datasets/README.md`) updates in the same merge that adds a trunk (G14.10 rule).

**Falsifiers.** Same as `goal:g14.10`'s own falsifier (b): if a re-scrub or label audit finds > 1 pct of records with a wrong or missing label, the affected trunk is quarantined under `datasets/quarantine/` until relabelled -- the classifier's calibration slice is exactly what this audit re-checks against.

**Done when.** One index exists -- a `datasets/README.md` row plus a `labels.jsonl` per trunk -- that `goal:g14.7.2`'s training arms can read directly with no further transform.

**First chunk.** None minted yet -- ordered explicitly by thought-master: DS.01 first (the one scrub, already queued), THEN this node's own capture chunk, THEN the jev classifier pass as its own batched rounds. Both later steps queue behind DS.01 landing.
