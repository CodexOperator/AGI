---
id: goal:g7.33.9
mint_id: 186661f2be774b178e0e9d05d944d1f2
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.9
edited_by: thought-master
goal_id: G7.33.9
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: b5210303cfffe508
season: 2
seeds: []
status: active
tags:
  - local-maxxing
  - engine
  - template-max
title: "G7.33.9: TEMPLATE-MAX FOR MODEL-FACING PROSE -- every warning, refusal, nudge and reminder the engine sends a model loads at run time from a template, never a literal in a build node"
town: core
---
# goal:g7.33.9

| | |
|---|---|
| goal | every warning, refusal, nudge and reminder the engine sends back to a MODEL loads at run time from a template -- never a literal in a build node |
| origin | the owner 16:20Z 09-24 (verbatim on town:local-maxxing's board) · first case: rotation_alert.py's band text read as a stop (director-engine idled at 0.40 of the 0.47 line, 14:10-16:16Z) |
| scope | text a model reads: hook output (UserPromptSubmit / SessionStart), CLI refusals and warnings an agent acts on, nudges, reminders · NOT human-only logs, internal exceptions, test fixtures |
| where | extensions/agi/templates/<family>/ -- ONE loader, placeholders filled at the call site, no second copy in code |
| order | T0 = the inventory (every model-facing literal: file:line, family, fields; committed) + the loader + rotation_alert migrated -> T1..Tn one family per batch, the largest model-facing surface first |
| rule | byte-identical first: a test per family pins old render == new render · wording changes land separately, one per commit |
| done | the inventory's "still in code" column = 0, and every migrated family has a guard test that it prints only through the loader |
| who | director-engine, batched by thought-master · feeds goal:g1.19 (core's engine surface inventory under config-maxxing) |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
renumbered goal:g5.32 -> goal:g7.33.9 on the owner 16:24Z 09-24 rule (fixes nest as sub-sub goals inside a fixes subgoal of the top-level subgoal they apply to, never a new top-level goal): g7.33 = ENGINE FIXES SURFACED BY THE TOWN; mint_id unchanged; the one frontmatter reference (the town:local-maxxing board rows) re-pointed in the same commit
<!-- THOUGHT:END -->
