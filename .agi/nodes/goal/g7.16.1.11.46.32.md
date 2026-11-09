---
id: goal:g7.16.1.11.46.32
mint_id: c7997be3d655449782c8ee58f94acda3
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.46.32
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 3b13d8dade315dcb
season: 3
seeds: []
status: horizon
tags: []
title: "G7.16.1.11.46.32: OptMem ITSELF is a post's memory layer -- compact references in the chat, each linked to its full chunk, nothing compacted (the owner's RED 11-01 overrules doc:brainstorm-unify §11)"
town: core
---

# goal:g7.16.1.11.46.32

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle): its doc:brainstorm-unify §11 called OptMem a package to skip ("adopt the SHAPE, not the package ... OptMem adds nothing ... skip it", :363-365), and M9 (goal:g7.16.1.11.46.25, a summary tree with a compactor) was built on that call. On 11-01 the owner RED-ed it: the memory layer is OptMem itself, not a system like it, and it compacts nothing. The council placed this as a HORIZON leaf under .46 with one OVERRULED line in §11 (alive [decision] 07:29:02Z 11-05 (III)(R), 3/3); it was never minted (alive's red on itself 08:54:05Z 11-09; SM's [place] 08:55Z).

## OWNER 2026-11-01 10:08:59Z (c:093989b6aeb0), verbatim (chat to belam, on summary_live / M9; belam's [owner-a] c60ab183d2 on refs/box/belam/sanctuary-master)
"It shouldn't compact anything that's the whole point of OPTMEME. It just creates more compact references and places those into the chat instead but then the condensed chunks still link to the full things so it can be viewed in detail as needed. This is why I was so adamant that we NEED OPTMEME not a system like it. OPTMEME isn't compaction it is a layer above that. I kept saying it must be seamless. This is not a seamless design."

## Target end-state
1. A post's memory layer is OptMem itself (the owner to confirm OPTMEME = github.com/VictorTaelin/OptMem), seamless: the chat carries compact references, each linked to its full chunk, and any of them opens to the full text on demand.
2. Nothing is compacted or destroyed: every full chunk stays readable behind its reference.
3. A plan to adopt it is on the graph as build leaves under this one, before any summary_live flip.

## Invariants
- summary_live stays false on M9 as built (owner 11-01: "This is not a seamless design").
- doc:brainstorm-unify §11's skip-OptMem call reads OVERRULED, pointing here.

## Falsifier
1. THE PLAN, from the repo top, exits 0 only when at least one live goal or build node names this leaf as a parent (the adoption plan exists):
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && [ "$(git grep -l -e '^  - goal:g7\.16\.1\.11\.46\.32$' -- .agi/nodes/goal .agi/nodes/build | wc -l)" -ge 1 ]`
   RUN at the mint on 3beb8abb88: exit 1 (no child; git grep rc 1, no error); outside a repo: exit 1. Control, a scratch repo with one goal node whose parents list it: exit 0.
2. THE OWNER'S CONFIRMATION and the seamless read: an `## OWNER` block on this node, with its chunk id, confirming the OptMem repo, and the owner's word that a live chat reads seamless. Read by hand.
3. Negative, from the repo top, exits 0 only while summary_live reads false (git grep -q's rc 1 = no line saying true):
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && { git grep -q -e '^summary_live: true$' -- .agi/nodes/.geometry/secrets.md; [ $? = 1 ]; }`
   It must hold until 1 and 2 are met. RUN at the mint on 3beb8abb88: exit 0; outside a repo: exit 1. Mutant, secrets.md with 'summary_live: true': exit 1.

## Out of scope
goal:g7.16.1.11.46.25 (M9 as built, complete; its stub stays a stub) · goal:g7.16.1.11.46.13 and goal:g7.16.1.11.46.24 (the store and the adapter halves, complete) · goal:g5.4.3 (the Meme Master post, whose memory is the harness's).

## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 11-09: minted HORIZON on the council's 11-05 placement ((III)(R), 3/3), carried out late on SM's [place] 08:55Z (alive's red on itself). Horizon, not active: nothing builds before the owner confirms the repo and the council places a plan; F1 counts that plan's first node. The same commit adds ONE OVERRULED line in doc:brainstorm-unify §11 under :365, pointing here; :365 itself stays as written (a version is the grid's).
<!-- THOUGHT:END -->
