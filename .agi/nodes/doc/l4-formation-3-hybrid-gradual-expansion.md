---
id: doc:l4-formation-3-hybrid-gradual-expansion
mint_id: 6d67d8c4c0e847dc8f82a61d89fcd579
type: doc
parents:
  - goal:g6.21
next_edges: []
edited_by: belam
origin: doc-version
scaffold_hash: 7a160090971d18df
season: 2
tags:
  - formation
  - sanctuary
  - owner-verbatim
thought_session: dissolve-legacy-2026-09-19
title: Formation 3 — hybrid survival with gradual expansion (the figure-eight)
town: core
---
<!-- BODY:BEGIN -->
# doc:l4-formation-3-hybrid-gradual-expansion

## Owner text (the verbatim quotes that define this formation)

> "Usually receives assignments from Master Sensei but can also receive them for you in this now lightest version of a hybrid mode, somewhere between survival and full operation."
(doc:l4-owner-decisions L729)

> "Overall, structural clarification for hybrid survival mode. What we do is instead of running directors, uh, doing point for each specific long term goal, instead, we only activate the keep. Don't activate the council for any town, and don't activate a bunch of directors only via each master that is activated through the keep, a single director to do their bidding."
(doc:l4-owner-decisions L765)

> "I don't know if you noticed, but it naturally felt into a place that the masters tell the directors what to do. And then the directors, when they're done, circle around in a figure eight towards you, reporting their completion status and all these things, and then you circle around to the masters telling them to continuing, like, what to do next. So it is like a smaller, more tight knit figure eight loop, and it seems to be working really well. Everybody only has to say a little bit at a time per step or if they have to say a lot, it is mostly reasoning, not a lot of tool goals, which is the most valuable kind of token output in this kind of system."
(doc:l4-owner-decisions L765)

> "So the operating structure right now is you have the sanctuary master and their free floating director attached to them, and beside the sanctuary master, you have the master Sensei because they're both kinda equal level in the keep. And then under both of them, you have the stream master running the streaming town, and you have the local master that you're about to spin up running the local maxing town."
(doc:l4-owner-decisions L767)

> "But as I said for now, we are not pulling up those masters. We are just strictly pulling up the structure required to initiate this. As far as masters online, we just keep the exact same set and the exact same set of directors. We just add one other master that presides over the local Maxxing town. This is, by the way, how we will organize breaking out long term g goals into their own towns as needed. over time to allow the structure of the graph to recurse upon itself as needed to increase in scope gradually and in a controlled fashion."
(doc:l4-owner-decisions L767)

> "The StreamMaster is running in hardcore survival mode. We're not standing up the full thing. We're just letting it run the actual live stream right now and act as a liaison instead of its actual kinda, like, master role."
(doc:l4-owner-decisions L767)

> "Prime resides over core town himself directly during hybrid survival mode. Sanctuary town is overseen by Sanctuary Master and Master Sensei as we described. You have core town, and Thought Master will oversee local town with his director."
(doc:l4-owner-decisions L773)

> "Sensei shouldn't need a director, he's responsible for template/config changes and brief/doc updates only for various roles."
(doc:l4-owner-decisions L745)

## The formation

Prime/SM reading: the keep is active, no council is, and every activated master gets exactly one director. Towns are the unit of expansion — a master per town, one town per long-term G goal as it is broken out. Role words are the owner's (16:4xZ); post names in parentheses are what config:posts carries today.

```
owner
  │
belam (Prime) ── presides over CORE town DIRECTLY · suite-window grant · circles "what next" back to the masters
  ├─ director-point   (post sanctuary-director, sonnet max)  the Prime's own director
  ├─ director-review  (post sanctuary-helper,   sonnet max)  runs the mur reviews the Prime names
  │
  THE KEEP — SANCTUARY town, equals:   sanctuary-master ══ master-sensei
  │    SM ──► director-sanctuary (post sensei-director, sonnet max; free-floating, g15 usual)
  │    Sensei: templates / config / briefs / role docs only — NO director; every other task ──► SM
  │
  town masters under the keep:
  ├─ stream-master  (STREAMING town; hardcore survival: runs the stream, liaison only, no director)
  └─ thought-master (LOCAL town, opus) ──► his own director (goal:g14)
  NOT pulled up: any council · web-app master · encryption master

figure eight:  masters ──tell──► directors ──done──► Prime ──what next──► masters
```

Prime/SM reading of the loop: a director speaks to the master above it; the master hands completion to the Prime; the Prime hands direction back to the masters. Short turns, reasoning over tool calls.

## What it bootstraps in the next

Next: doc:l4-formation-4-full-activation. Prime/SM reading of what F3 proves that F4 stands on:

- **The keep as the routing layer.** SM + Sensei already carry task intake, planning and review by name; F4 adds councils on top of a keep that has been running, not one stood up cold.
- **Town-per-master as the recursion unit.** stream and local towns each have a master before they have a council; the council rows (council-core, council-streaming-suite, council-web-app-suite, council-local-maxxing in config:posts) exist unfilled and are what F4 fills. The web-app and encryption masters follow the same pattern when pulled up.
- **director-review as the council placeholder.** The Prime's mur after every merge-up stays

> "until the Council exists"
(doc:l4-owner-decisions L757) — the owner's own framing of merge review: "Since the directors usually hand off all their merges to you or later the council eventually through the Master review process anyway." (doc:l4-owner-decisions L757). F4's council inherits a review workflow that already runs.
- **Per-post tool access by template + key** (rungs 5-8, next season, doc:l4-owner-decisions L739) is the gate F4 needs before many posts run at once.

## Status

Running now. Entered 2026-09-12 22:2xZ (Sanctuary Master stood up, seated 23:37Z; director-sanctuary moved under her), named as the lightest hybrid at 23:0xZ (L729) and as hybrid survival mode with the figure-eight at 2026-09-13 23:32Z (L765-767); the sanctuary/core/local town split at 2026-09-14 01:06Z (L773). thought-master row live (window @366, goal:g14); his director not yet on a row. Councils, web-app and encryption masters: not activated.

## Sources

- doc:l4-owner-decisions L725-731 (SM stood up, director-sanctuary free-floating, lightest hybrid), L745 (Sensei has no director), L757 (council review), L763-767 (thought master, keep-only, figure-eight, town masters), L773-775 (town split, formation order)
- goal:g7.16 L24-28 (the preceding formation, doc:l4-formation-2-texas-two-step)
- config:posts (live rows: names, models, windows)
- sanctuary-master card §0.5-§0.6 (formation diagrams this one is built from)
<!-- BODY:END -->
