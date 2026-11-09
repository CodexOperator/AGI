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
title: "G7.16.1.11.46.32: OPTMEME itself is a post's memory layer -- compact references in the chat, each linked to its full chunk, nothing compacted (the owner's RED 11-01 overrules doc:brainstorm-unify §11)"
town: core
---

# goal:g7.16.1.11.46.32

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle): its doc:brainstorm-unify §11 called OptMem a package to skip ("adopt the SHAPE, not the package ... OptMem adds nothing ... skip it", its paragraph on OptMem), and M9 (goal:g7.16.1.11.46.25, a summary tree with a compactor) was built on that call. On 11-01 the owner RED-ed it: the memory layer is OptMem itself, not a system like it, and it compacts nothing. The council placed this as a HORIZON leaf under .46 with one OVERRULED line in §11 (alive [decision] 07:29:02Z 11-05 (III)(R), 3/3); it was never minted (alive's red on itself 08:54:05Z 11-09; SM's [place] 08:55Z).

## OWNER 2026-11-01 10:08:59Z (c:093989b6aeb0), verbatim (chat to belam, on summary_live / M9; belam's [owner-a] c60ab183d2 on refs/box/belam/sanctuary-master)
"It shouldn't compact anything that's the whole point of OPTMEME. It just creates more compact references and places those into the chat instead but then the condensed chunks still link to the full things so it can be viewed in detail as needed. This is why I was so adamant that we NEED OPTMEME not a system like it. OPTMEME isn't compaction it is a layer above that. I kept saying it must be seamless. This is not a seamless design."

## Target end-state
1. A post's memory layer is OPTMEME itself, the artifact the owner names (the owner to confirm WHICH: OptMem, github.com/VictorTaelin/OptMem, belam's reading in c60ab183d2; or OptChat, doc:brainstorm-unify §11's OptChat paragraph, the append-only log with a tree of summary lines, a bounded view and zoom, all-is-one's reading 09:14:45Z 11-09, which reads at least as close to 'compact references ... placed into the chat ... still link to the full things'), seamless: the chat carries compact references, each linked to its full chunk, and any of them opens to the full text on demand.
2. Nothing is compacted or destroyed: every full chunk stays readable behind its reference.
3. A plan to adopt it is on the graph as build leaves under this one, before any summary_live flip.

## Invariants
- summary_live stays false on M9 as built (owner 11-01: "This is not a seamless design").
- doc:brainstorm-unify §11's skip-OptMem call reads OVERRULED, pointing here.

## Falsifier
1. THE PLAN, from the repo top, exits 0 only when at least one live goal or build node names this leaf as a parent (the adoption plan exists):
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && [ "$(git grep -l -e '^  - goal:g7\.16\.1\.11\.46\.32$' -- .agi/nodes/goal .agi/nodes/build | wc -l)" -ge 1 ]`
   RUN at the mint on 3beb8abb88: exit 1 (no child; git grep rc 1, no error); outside a repo: exit 1. Control, a scratch repo with one goal node whose parents list it: exit 0.
2. THE OWNER'S CONFIRMATION and the seamless read: an `## OWNER` block on this node, with its chunk id, naming WHICH artifact OPTMEME is (OptMem or OptChat), asked BEFORE any plan node is cut under this leaf; and the owner's word that a live chat reads seamless. Read by hand.
3. Negative, from the repo top, exits 0 only while the CHECKOUT's summary_live cell does NOT read true the way its reader reads it (the compactor's read in engine-post.md: `sed -n 's/^summary_live: *//p'` then `head -1`, live iff 'true'; any number of spaces after the colon). The reader reads the cell at its PIN (AGI_TRUNK, the committed blob), F3 the checkout's working tree; they split on an uncommitted edit, and when the pin LAGS the trunk: a trunk flip back to false reads 0 here while a pinned true stays live until the re-pin; a flip to true reads RED here first, the safe side:
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && [ -r .agi/nodes/.geometry/secrets.md ] && [ "$(sed -n 's/^summary_live: *//p' .agi/nodes/.geometry/secrets.md | head -1)" != true ]`
   It must hold until 1 and 2 are met. RUN at 5f9568ffde: exit 0; outside a repo: exit 1. Rows, a scratch secrets.md, reader / F3: 'summary_live: false' off / 0; 'summary_live: true' LIVE / 1; 'summary_live:true' LIVE / 1; 'summary_live:  true' LIVE / 1; 'summary_live: true ' (trailing space) off / 0; cell absent off / 0; no secrets.md off / 1 (fails closed). 

## Out of scope
goal:g7.16.1.11.46.25 (M9 as built, complete; its stub stays a stub) · goal:g7.16.1.11.46.13 and goal:g7.16.1.11.46.24 (the store and the adapter halves, complete) · goal:g5.4.3 (the Meme Master post, whose memory is the harness's).

## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 11-09, version 2 RE-CUT 1 (on SM's offer 17:16Z, before GATE631 ran; 3/3 next-touch items, none a term): the title is neutral in the owner's word, OPTMEME (aio 17:14:10Z, sp, alive); F3's claim is narrowed to the CHECKOUT's cell, with the pin-lag split named (alive NIT 1, correcting sp's 'only on an uncommitted edit'); cites by name, not line number (alive NIT 2: engine-post.md's compactor read, §11's OptChat and skip-OptMem paragraphs). F3's command is unchanged. Version 2 (the council's next-touch items on L471, 3/3: alive 09:13:56Z, all-is-one 09:14:45Z, self-perpetuating 09:17:31Z): (1) Target 1's repo url now names its source, belam's reading in c60ab183d2, kept in Target as alive and the minter picked; (2) all-is-one's rival reading beside it: OPTMEME may be OptChat (§11's OptChat paragraph) rather than OptMem, so F2 asks the owner WHICH before any plan node under this leaf; (3) self-perpetuating's TERM: version 1's F3 git-grepped '^summary_live: true$' (one space) while the reader takes any spaces, so 'summary_live:true' made the compactor live with F3 holding; F3 now reads the cell as the reader does, its rows above. The title still says OptMem, as minted 3/3; the Target and F2 carry the open question. Nothing else changed: the OWNER block, F1, the Invariants, Out of scope, the assignee.
Version 1's why: minted HORIZON on the council's 11-05 placement ((III)(R), 3/3), carried out late on SM's [place] 08:55Z (alive's red on itself). Horizon, not active: nothing builds before the owner confirms the artifact and the council places a plan; F1 counts that plan's first node. The same commit added ONE OVERRULED line in doc:brainstorm-unify §11, under its skip-OptMem line, pointing here.
<!-- THOUGHT:END -->
