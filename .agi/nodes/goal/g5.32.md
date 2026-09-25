---
id: goal:g5.32
mint_id: ab88b60fec504479a1180d290cef0844
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.9
edited_by: director-engine
goal_id: G5.32
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: a4f7ef12ead2947e
season: 2
seeds: []
status: active
tags:
  - local-maxxing
  - templates
  - director-engine
title: "G5.32: model-facing hardcoded prose (hook output, CLI refusals/warnings, nudges, reminders) moves out of inline literals in build nodes into extensions/agi/templates/<family>/, loaded dynamically at the call site -- byte-identical render first, wording changes land separately"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g5.32

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
TMM.121, owner order 16:20Z 09-24 via thought-master (verbatim): "make director-engine do a pass on all the hardcoded prose warnings sent back to models in every build node and put them all into templates that get loaded in dynamically." Minted as a subgoal of goal:g5 (director-engine's own goal tree) rather than under goal:g7.33 (core's, HELD for me). Scope is model-facing text only (hook output, CLI refusals/warnings, nudges, reminders) -- never human-only logs/exceptions/fixtures. T0 (the inventory + loader + rotation_alert.py band-text migration) is the first mvp/hypothesis to hang under this; E0 (the band-text wording fix itself, already merged @6c33e4d01e / cherry-picked to trunk @37f1812f52) is absorbed by T0 once the loader lands.
<!-- THOUGHT:END -->
