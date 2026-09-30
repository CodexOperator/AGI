---
id: goal:g7.16.1.7
mint_id: 2364abb35c3c446d84a79f1ce50941cd
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.7
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: a7b1e7dbb0f986b4
season: 2
seeds: []
status: horizon
tags:
  - templates
  - spawn
  - rotate
  - formation
  - council-loop
title: "G7.16.1.7: spawn/rotate unification on recursive linkable templates -- formation -> post -> harness -> model, one post row holds the live role"
town: core
---
# goal:g7.16.1.7

## OWNER 2026-09-29 23:1xZ, verbatim (Prime pane)
"Okay sweet. That looks good so far. We're redesigning the messaging system and the rotate/spawn unification next, so we could have director-generals 3,4 tackle both bundles side by side, with one creating the machinery that accepts the new write form as the other fills it in. Then as 3 completes the write portion they move on to the rotate/spawn unification. If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining. Ideally the post holds everything for that role: session id, pid, tmux pane id, renderer nested inside it but actually a mint id link: harness config (includes model type)."
"Formations become templates, harness adapters become accompanied by templates mapping other harnesses' actions and hooks to general graph engine functions as best possible."
"Also we need to figure out a more elegant way to claim a seat. Like the heal script should just automatically assign keys so no model has to do it. For now we can keep it very kind and forgiving via a template. But over time we will pop in more and more stringent key creation templates. Especially as we work on per-post user accounts with custom write permissions. But that is season3 work first we need to wrap up season 2."
"The minimal requirement for rotate/spawn is that it's all self-activated in the background. All I or you need is to activate the right formation template and chain the appropriate harness template and modify its configuration as needed. No more templates for pi free vs pi local. Just standard pi template that lists all the different model + thinking level + extendable to other harness settings as rows containing jsons. So it includes the other models+internal aliases we added and can be used. One row will have a default tag or marker. The rest are available and can be used during stand up or modified on the fly."
"Add a way to smoothly switch the symlink over to the new config settings."
"So formations are templates containing empty link rows pointing to "null" that are set as part of formation activation, which writes the template into .geometry while filling in the link rows dynamically at stand up using a post template + customizations, which itself links a harness template, which can link various model templates. All graph based reusing existing graph machinery for the most part. We are basically implementing recursive dynamically linkable templates during the spawn rotate unification so we can leave all this template duplication behind in favor of nested templates."
"Does that make sense? Then we can bring in the magic pane system as well since tmux is linked to posts."

## Why this exists
goal:g7.16.1 (the council loop): the owner's next bundle after bundle 4 (goal:g7.16.1.4), minted by the Prime so the council places it whole. It stands on bundle 4: link rows are mint ids (goal:g4.18.6), a template is addressable by row (goal:g4.18.5 W1a), and every template version is a per-node grid commit (goal:g7.16.1.6). Today the same facts are copied across config:posts cells, config:brief parts, per-harness templates (pi-free vs pi local) and rotate.py / heal.py launch paths.

## Target end-state
- ONE post row per role holds everything live for it: session id, pid, tmux pane id, and mint-id links (never copies) to its renderer and its harness config (the model is part of the harness config).
- A formation is a TEMPLATE whose link rows point at null. Activating it writes the formation into .geometry, and standing a post up fills each link row: post template + customizations -> harness template -> model template(s). Nested, recursive, dynamically linked templates built on the existing graph machinery, with no duplicated template text.
- ONE pi harness template: its rows are JSON objects (model + thinking level, extendable to other harness settings), covering the internal aliases already in use; exactly one row carries the default marker, and any row can be chosen at stand-up or changed on the fly. No separate pi-free / pi-local templates.
- A harness adapter ships with a template mapping that harness's actions and hooks onto the engine's graph functions (Claude Code, pi, and later third parties).
- Spawn and rotate are self-activated in the background: the owner or the Prime activates a formation template and chains a harness template; nothing else is typed.
- A post's config switch-over is atomic: the new config is written beside the old one and the symlink is swapped in one rename, with no window in which a reader sees neither.
- Seat claiming needs no model act: heal assigns the post's keys from a key template (kind and forgiving in season 2; stricter templates and per-post accounts with custom write permissions are season 3).

## Invariants
- A template field lives in one node; everything else links to it by mint id.
- A live post is never left without a readable config (the swap is atomic) or without a key it can sign with.

## Falsifier
1. Standing up a post from a formation template takes one activation command, and the post row afterwards holds the session id, pid and pane id plus mint-id links (not copies) to its harness and model templates.
2. Switching a live post's model is one row change in the harness template (or one post-row link change) plus the atomic swap, with no restart of any other post.
3. Negative: zero pi-free / pi-local template pairs remain, and zero model or effort literals remain in rotate.py / heal.py launch paths.

## Out of scope
goal:g7.16.1.4 (bundle 4) · goal:g7.16.1.6 · the messaging-system redesign (its own bundle) · the magic pane system (after this bundle: tmux is linked to posts) · season-3 key templates and per-post user accounts.
Inputs to absorb or retire BY NAME at placement, never duplicate: goal:g4.20.1 (one harness source) · goal:g1.9 + goal:g1.9.2 (one brief, the first turn is the render) · goal:g6.36 (rotate driven) · goal:g6.41.1 P2-P4 (one launcher, resume) · goal:g6.43 · goal:g6.46 · goal:g7.25 (third-party harness adapter) · goal:g1.11 (per-spawn keys).

## Agent Notes
Assigned to **the council** (placement).
