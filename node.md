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

## OWNER 2026-09-29 23:3xZ, verbatim (Prime pane) -- answers to the Prime's three design points (override order · recursion guard · atomic swap)
"1. Agreed. Makes it compatible with users, security groups, domain controller infra.
2. Sounds good. Walk only across a max of say 5 steps. If it took more than that the template/.geometry formation graph likely got too complicated or templates got too complicated and need to be simplified again.
3. Yup that works.
Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further."
Settled: (1) nearest wins -- post customizations over the harness template over the model default (the locations.py rule); (2) a link walk stops at 5 hops with a cycle guard, and needing more is itself a finding: simplify the templates; (3) a config switch writes beside the old file and swaps the symlink by one rename.

## OWNER 2026-09-30 00:0xZ, verbatim (Prime pane) -- the first turn is a render tool call
"One more simplification I wanted to add to the new rotation spawn route is that instead of doing some kind of weird hook thing to manually post all that text from the various like templates and docs into the first turn of the conversation, we should just instead have all of that be posted in at the first turn still, but instead of a chat turn, it's a tool call turn if possible. And the tool call is a render call that returns the graph slice that is all the docs that need to be put into context first thing. basically Instead of a first turn in the pane, we get to just run the tool call or the render call, and the results of that get posted in to the, if possible, tool call results as first thing. And I keep mentioning turning all these engine function clis into tools slash MCPs, same diff, but that's not needed right now. I'm not sure that seems like that's like a lot of extra setup. We should just first make sure the internals work properly. But yeah, I want more engine functions to rest on the render pipeline as well. And the render pipeline itself should have different display modes like a more graphical display mode but then also an inline display mode that just kind of shows everything in one big block like the way fresh rotations get their docs now. Also let's make it so the context docs are also linked into the posts. plus are the guard scripts and the guard dot env in the graph as a build node and a .geometry node respectively."
Prime's answer to the last question, measured 00:0xZ: NO. guard-init.sh, sanctuary-health and sanctuary-watch live outside the repo in a directory that is not under git at all (the 09-29 option (b) change is versioned only by .bak copies); nodes only mention them. guard.env keys 5 settings by the host name, so its .geometry node must key them by box class (anonymize) before it can be committed.
## Why this exists
goal:g7.16.1 (the council loop): the owner's next bundle after bundle 4 (goal:g7.16.1.4), minted by the Prime so the council places it whole. It stands on bundle 4: link rows are mint ids (goal:g4.18.6), a template is addressable by row (goal:g4.18.5 W1a), and every template version is a per-node grid commit (goal:g7.16.1.6). Today the same facts are copied across config:posts cells, config:brief parts, per-harness templates (pi-free vs pi local) and rotate.py / heal.py launch paths.

## Target end-state
- ONE post row per role holds everything live for it: session id, pid, tmux pane id, and mint-id links (never copies) to its renderer and its harness config (the model is part of the harness config).
- A formation is a TEMPLATE whose link rows point at null. Activating it writes the formation into .geometry, and standing a post up fills each link row: post template + customizations -> harness template -> model template(s). Nested, recursive, dynamically linked templates built on the existing graph machinery, with no duplicated template text.
- ONE pi harness template: its rows are JSON objects (model + thinking level, extendable to other harness settings), covering the internal aliases already in use; exactly one row carries the default marker, and any row can be chosen at stand-up or changed on the fly. No separate pi-free / pi-local templates.
- A harness adapter ships with a template mapping that harness's actions and hooks onto the engine's graph functions (Claude Code, pi, and later third parties).
- Spawn and rotate are self-activated in the background: the owner or the Prime activates a formation template and chains a harness template; nothing else is typed.
- A post's config switch-over is atomic: the new config is written beside the old one and the symlink is swapped in one rename, with no window in which a reader sees neither.
- The first turn of a spawn or rotation is a TOOL-CALL turn, not a chat turn: a render call returns the graph slice of every doc the post needs (its linked context docs), posted as the tool result; no hook pastes template text. Turning engine CLIs into tools / MCP is later; the internals first.
- The render pipeline has display modes: a graphical mode and an inline mode (one big block, the way fresh rotations get their docs today); more engine functions rest on it.
- A post row links its context docs by mint id, beside its harness and renderer links.
- The guard is in the graph: guard-init.sh, sanctuary-health and sanctuary-watch as build nodes; guard.env as a .geometry config node keyed by box class, never by host name.
- Seat claiming needs no model act: heal assigns the post's keys from a key template (kind and forgiving in season 2; stricter templates and per-post accounts with custom write permissions are season 3).

## Invariants
- A template field lives in one node; everything else links to it by mint id.
- A live post is never left without a readable config (the swap is atomic) or without a key it can sign with.

## Falsifier
1. Standing up a post from a formation template takes one activation command, and the post row afterwards holds the session id, pid and pane id plus mint-id links (not copies) to its harness and model templates.
2. Switching a live post's model is one row change in the harness template (or one post-row link change) plus the atomic swap, with no restart of any other post.
3. Negative: zero pi-free / pi-local template pairs remain, and zero model or effort literals remain in rotate.py / heal.py launch paths.

## Out of scope
goal:g7.16.1.4 (bundle 4) · goal:g7.16.1.6 · the messaging-system redesign (its own bundle: goal:g7.32.6, after goal:g7.16.1.6; its wake is an adapter verb, so it joins this line's harness templates) · the magic pane system (after this bundle: tmux is linked to posts) · season-3 key templates and per-post user accounts.
Inputs to absorb or retire BY NAME at placement, never duplicate: goal:g4.20.1 (one harness source) · goal:g1.9 + goal:g1.9.2 (one brief, the first turn is the render) · goal:g6.36 (rotate driven) · goal:g6.41.1 P2-P4 (one launcher, resume) · goal:g6.43 · goal:g6.46 · goal:g7.25 (third-party harness adapter) · goal:g1.11 (per-spawn keys) · the key-row trunk pattern (the Prime 23:5xZ, measured tonight: SM gen 7's re-mint 4f0bdf6e5 landed on season2/main only, conflicted posts.md on local-maxxing and blocked EVERY rotate until the Prime synced 93f4567b5) -- when heal assigns keys, a key row lands on the post's own trunk too, never on one trunk alone · goal:g7.16.1.2.9 (row F: the formation line printed at wake from config:rotations first_turn; MOVED UNBUILT from bundle 2, council 23:5xZ, self-perpetuating + alive). SPLIT BY DEPENDENCY (all-is-one lens 23:5xZ, council agrees): 7a NOW (DG5) = ONE stand-up verb for spawn, rotate, heal recover and hand restart (absorbs goal:g6.41.1 P2-P4 and heal's launcher copy) · heal assigns keys · ONE pi template with JSON model rows; 7b AFTER goal:g7.16.1.6 + goal:g4.18.6 = the formation -> post -> harness -> model link rows, the walk, the atomic swap. Long-horizon guards: an override EQUAL to what it inherits is REFUSED (customizations never accrete); the harness adapter map IS the spine (every harness maps onto the same engine verbs: write · send · render · stand-up; never a harness-only verb). PLACEMENT (council, alive 23:4xZ, on belam XVIII's resume + owner 23:4xZ): the SPAWN line, side by side with bundle 4 NOW; it never waits on goal:g7.16.1.6 -- write.py is the one writer, so this line's writes take the new write form automatically when it lands. Also absorbs, by name, the launch-path half of the old bundle-5 list on goal:g7.16.1.4: C3 one scope-argv builder through mem_cap · B1 one launcher (heal._launch_recovered -> rotate._launch_window) · B4 one config reader · the R2 alert (N deferred recoveries -> ONE [red]) · SM's rotate candidates (_launch_window ensure_tmux_session without root; same-second unit names; the rotation announcement's absolute handoff path). Shape conditions (self-perpetuating lens 23:5xZ): the walk limit (5 hops) is a CONFIG CELL, and a walk that exceeds it names the chain in ONE finding (a simplify leaf or a [red]), never a silent error; COLD-START falsifier: a fresh clone + ONE formation activation = a running formation, nothing else typed. Keep "absorb or retire BY NAME" for every input: duplicates breed at nine. OUTCOME test through vision:alive: a recovered or rotated post's brief IS its live card, every time (09-29 17:33Z: the recovery brief was rendered from a stale 09-18 file).

## Agent Notes
Assigned to **the council** (placement).
