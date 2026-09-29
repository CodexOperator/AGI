---
id: doc:council-loop
mint_id: 0e5025a7e24f4e459c30e50d82b8060e
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: e99976c6c09553f9
season: 2
title: Council loop
town: core
---
# doc:council-loop

# doc:council-loop — the council loop (goal:g7.16.1): one protocol for every post in it

Seated 09-29 by belam-S2-L5-XV on the owner's word (goal:g7.16.1 holds it verbatim). Local-town · town local-maxxing · MAIN `/data/work/agi` on `local-maxxing/season2/main` · every post claude-code, Opus 5.5, effort high.

## Posts
| post | owns |
|---|---|
| alive · all-is-one · self-perpetuating (council) | check + modify each bundle after discussion (group chat); review the completed bundle: batched mur in chunks, then ONE manual review through YOUR vision node only, never the other two |
| director-general-1 | goals + hypotheses (skill agi-goal: nest leaves under the bundle's goal) |
| director-general-2 | experiments + verdicts, and the tests they need (skill agi-verify) |
| director-general-3 | MVPs + build nodes + tests; a build node may take the [goal, idea] parent set to shortcut chain growth |
| sanctuary-master | review each finished bundle: standard mur (agi-merge-up-review) on claude-code, model claude-opus-5-5, effort high; residues back until clean |
| belam (Prime) | merges into season2/main (PASS); reviews season 2's result through the five morals |

## The loop
```
council: check + modify the bundle (group chat) ─► DG1 goals+hypotheses ─► DG2 experiments+verdicts ─► DG3 MVPs+builds+tests
   ▲                                                                                               │
   │                                residues ◄── sanctuary-master: mur on CC Opus 5.5 high ◄───────┘   (until clean)
   └── council: batched mur in chunks + one lens review each ─► the next bundle (simplify · refine)
```

## Order of work (owner 09-29)
1. The current town bundle (town:local-maxxing board) — first.
2. Grok's work on `core/season2/main` and `core/main` ("probably way overbuilt on core"): simplify.
3. ONLY when nothing is left to simplify in 1 and 2: close season 2 — grow the graph out to the nodes overview nodes need (outcomes → bigger outcomes → overviews) and hand them to the Prime.
What this formation lacks (formations as template build nodes under goal:g7.16, one call that activates one template and deactivates the rest, the rest of the council-loop machinery) is bundle work, built by the directors in dependency order.

## Handoff (lean on Claude Code messaging, owner 09-29)
- `ListAgents` → `SendMessage` to the next post (it wakes that session) + ONE room line for the record:
  `python3 extensions/agi/bin/send.py --from <you> send --room council-loop '[handoff] bundle <n> · <stage> done · <node ids> · tests <n passed>'`
- A post acts only on a handoff addressed to it; one director works a bundle at a time.
- Council group chat: SendMessage to the other two council posts; the room carries the agreed bundle.

## Rules
- Nodes only through write.py (skills agi-node-write, agi-goal); commit by exact path in MAIN; never switch branches; never commit another post's edits; no MAIN commit while `.agi/sessions/verify-suite.lock` exists.
- No parent/kid dispatch in this mode (dispatch.py stays unused).
- Measure (owner: "Does the council materially improve the results"): per loop ONE numbers-only line on the town board — bundle · nodes grown · SM residues · what the council changed · better or not.
- Stop around noon ET 09-29 (16:00Z): finish the atomic step, write the card whole, commit, idle.
- Rotation at the meter line: skill agi-rotate. Post mechanics: skill agi-post.
