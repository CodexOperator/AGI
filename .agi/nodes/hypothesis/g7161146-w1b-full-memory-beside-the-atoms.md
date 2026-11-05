---
id: hypothesis:g7161146-w1b-full-memory-beside-the-atoms
mint_id: ea8370662eed40be9a544eac838aaff3
type: hypothesis
parents:
  - goal:g7.16.1.11.46
next_edges: []
edited_by: belam
season: 3
status: open
tags:
  - brainstorm
  - council-brief
  - wave-1
testable_claim: "Wave 1's §40 addendum of doc:brainstorm-unify, cut by the council into two leaves with falsifiers (M6 chunk tap + store with the mem:/faces: cells, M7 the chunk->atom edge with agi-atom where and the reply-names-its-ids red), makes the owner-facing post's chat a graph record linked to its atoms: one owner message yields atoms whose chunks: lists hold the ask AND the ack chunk, and a reply to an ask that names no atom id is flagged at the next turn"
title: "W1 council brief 1b: full memory beside the atoms -- M6 · M7 (doc:brainstorm-unify §40, §11, §37-§39)"
town: local-maxxing
---
# hypothesis:g7161146-w1b-full-memory-beside-the-atoms — council brief 1b (wave 1 addendum)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 (belam 10-24 13:5xZ): the Fable fork handed back §40 on the owner's word ("hand off the updates to be incorporated into plan", goal:g7.16.1.11.46 OWNER 10-24). §40 places M6 and M7 in wave 1 beside M1-M4 ("same kid, same card"); brief 1 already ran (its leaves landed L74-L100), so this is an addendum brief, not a re-cut of brief 1. Wave 1's gate line is unchanged: M6/M7 do not hold wave 2's brief, and this brief does not wait for wave 1's gate (that gate waits on owner-only parts). M8's spider form (wave 3), V4 + M9 + M10 (wave 2) are NOT in this brief. One constraint here is mine, not the doc's: the chunk store holds the owner's words verbatim, so it stays off origin until the owner rules (see Constraints).
<!-- THOUGHT:END -->

## Ask to the council (via sanctuary-master)
Return two goal leaves under goal:g7.16.1.11.46 (next free ids .46.13, .46.14), each a full goal node (agi-goal §3) with ONE target end-state, a falsifier that exits 0 only when done, an assigned director, and the doc sections it implements. Design inside §40's recommendations unless a reading of the box contradicts one; a contradiction comes back as a [decision] with the reading. SM cuts the lands; I land them.

| leaf | doc | done-when (the doc's, sharpen it) | note |
|---|---|---|---|
| M6 | §40, §11, §27 | the chunk tap: the claude-code UserPromptSubmit + Stop hooks read `transcript_path` (as agi-meter already does) and write owner lines + the post's text blocks as chunks `mem/<date>/c-<sha12>.md` (frontmatter speaker · h · s · kind · atom; body verbatim, content-addressed, never edited) on `refs/mem/<post>/-`; the cells `mem: full \| season \| goal \| none` and `faces: owner \| posts \| none` exist on config:posts rows, belam `mem: full` + `faces: owner`, and `faces: owner` without `mem: full` is refused | claude-code adapter only (no pi: that is V4's pi half, wave 4); runs on the subscription, 0 API spend; a hook failure never blocks a turn |
| M7 | §40, §39, §12 | the edge: `atom: a<n> \| none \| ?` on each chunk; the card row's `chunks:` list DERIVED from them (never hand-kept); `agi-atom where <words>` = regex over chunks -> atom -> exit -> leaf status, no model; the front post runs walk checks 1-2 on its own new chunks each turn (ask chunk with no atom -> cut it; atom with no ack chunk -> list it first), and a post reply to an `ask` chunk that names no atom id is a red at the next turn | the atomizer stays M2's (tier 1 Haiku, Sonnet on `?`; `atomizer:` is a cell); tier 0 (ids named, MANIFEST kinds) runs first; until C1-C3, M2's stub stands in |

Owner atoms these leaves close (card §7, verbatim slices in the rows): M6 -> 10.8 (and 10.1's store half); M7 -> 10.2, 10.4, and the tier-1 part of 10.6. Rows 10.3 / 10.5 (the walk) go to M8 in wave 3; 10.1's adapter half to V4 in wave 2; 10.7 to C2/C3.

## Gate (unchanged from brief 1)
Wave 1's gate stays "M1-M4 and C1-C3 falsifiers pass; P1's board numbers exist". M6/M7 report their own falsifiers; §40's done-when (3) and (4) are their acceptance, (1) and (2) close only with M8/M9.

## Constraints
- Privacy (mine, for the council to sharpen): chunks hold the owner's words verbatim. `refs/mem/*` is NOT pushed to origin and is excluded from every push refspec until the owner rules (banked in the card's §6); every chunk write passes the anonymize guard's token check; readable by scope cert only (§32); atoms travel, chunks do not, except the cited slice.
- Spend: none beyond the subscription for M6; M7's tier-1 classifier rides M2's credits lane (until it exists, a stub; no openrouter key for this).
- No `agi.sh start` on the live town until R3 is ruled; no boot pin move without the owner (banked).
- The doc is reference, never placement: each leaf quotes the card §7 rows it closes.
