---
id: goal:g7.16.1.11.13
mint_id: 0d5e0a34405d4ec0aab3c608edee9433
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.13
goal_kind: subgoal
origin: goal
scaffold_hash: c6b17011fb0f9e1d
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - design
  - g7.16.1.11
  - aa3
  - land
  - trunk
title: "G7.16.1.11.13: AA3 land -- a land is mail one parent edge up; root ff-lands a post's range on the trunk after edge + ring-signer + grow-gate + agi-gate checks; the trunk has ONE writer"
town: core
---
# goal:g7.16.1.11.13

## Why this exists
goal:g7.16.1.11: the council's AA3 section (doc:rse-aa3-land on posts/all-is-one, measured on a scratch repo borrowing MAIN's objects, 11 lanes, 0 shared refs written) answers the owner's 'things could only go where they must go' for the merge path: today the master's hand-gated merge-up (skill agi-master-gate's landing) and the hub's pre-receive are the only gates. It found three byte defects that make today's gates read nothing (AA3.4) and, after belam's ruling 1efd017e6 (members <- council), a fail-closed rule for council authority (AA3.8: a name in the council row's `members` cell, absent = nobody; belam wrote the cell, faabf9b7a). The author's follow-up: the three byte fixes come BEFORE agi-land, or its checks read nothing.

## OWNER 2026-10-01 23:0xZ + 23:2xZ, verbatim (via the council bundle)
"We just need to allow each post to have a will box which they already do, an inbox and a holding box or an outbox or something."
"This is why protocol needs to be a mathematical matrix rotation or projection. So things could only go where they must go."
"Remember the graph can hold as much as you want just the engine itself needs to be tiny. It can lead on the graph via templates we have so much recursion and linking built in."
Skills line (owner 23:4xZ via belam 23:49Z): "update the other skills to reflect the way the new system works"


## Target end-state
- agi-land (<= 1,503 B, root-side, in config:engine-root, 0 B in the zygote) ff-lands <post>'s <sha> on the trunk iff ALL hold at the RECEIVING tip $o: EDGE sender = parent(post) on the parent cells (council authority = the council row's `members` cell, fail-closed; a post whose parent is owner lands itself), SIGNERS every commit in $o..$sha verifies on root's ring as the sender or a post under <post>, GROWTH grow-gate over $o..$sha, BODY agi-gate $sha, FF $o is an ancestor and the move is compare-and-swap (in MAIN the last step is `git merge --ff-only`).
- The request travels as AA1 mail to root: refs/box/<sender>/root, body `land <post> <sha>`; no master role, no human gate step.
- Three byte fixes land FIRST (AA3.4): (1) the signers principal `<post>@agi`; (2) grow-gate `rev-list $n --not ${AGI_NOT:---all}` (+12 B); (3) grow-gate's signer sed strips `@agi` (+7 B).
- The trunk reflog shows ONLY root as the trunk writer after the switch.

## Invariants
- A land is ff-only and compare-and-swap: a not-ff is refused (the child merges the trunk and re-requests), never merged by root.
- Root runs no suite on the land path (small and synchronous); the parent's judgment (suites on tmpfs, reds attributed) happens BEFORE it mails `land`.
- A forged commit (a key outside the subtree) moves nothing; SM cannot land alive; DG1 cannot land itself.
- SIZE BAR (the bundle's statement of the owner's line): the base install stays under 8 KB (config:engine <= 8,192 B), unfolded from a 1 KB seed (1,023 B); boxes, the lap and the land check are EXPANSION read by `sect`, 0 B in the zygote; nothing model-manual that could be automated; reuse an existing piece before adding one.

## Falsifier
1. All 11 lanes of doc:rse-aa3-land AA3.3 reproduce on a scratch clone against the real ring + real trunk cells (never MAIN): the harness is AA3.9 of doc:rse-aa3-land (3,283 B, self-contained, alternates, 0 shared refs written; extract + run: `sed -n '/^## AA3.9/,$p' .agi/nodes/doc/rse-aa3-land.md | sed -n '/^```sh/,/^```$/{//!p}' > /tmp/lanes.sh; sh /tmp/lanes.sh`) and prints 11 lines `ok`. TODAY (trunk faabf9b7a+): 10 ok + `FAIL 4v` (the real grow-gate is vacuous at a land); the AA3.4 byte fixes flip 4v, so the blocking order is a test that fails now and passes when they land.
2. Negative: after the switch `git reflog <trunk>` shows no writer other than root, and `git grep -n 'refs/heads/trunk' -- <post-writable scripts>` returns zero hits.

## Out of scope
goal:g7.16.1.11.11 (the box root reads) · goal:g7.16.1.11.12 (the ring) · goal:g7.16.1.11.14 (skill deltas) · the agi-land build until the three byte fixes land.

## Agent Notes
Assigned to **director-general-1**.
