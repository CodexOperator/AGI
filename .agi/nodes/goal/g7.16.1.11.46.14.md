---
id: goal:g7.16.1.11.46.14
mint_id: ad644af8042d482c9da6433f7ef65230
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: belam
goal_id: G7.16.1.11.46.14
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - M7
season: 3
status: active
title: "G7.16.1.11.46.14: M7 -- every chunk names its atom (a card row id, none or ?), the card's chunks: lists are derived, agi-atom where answers from the chain with no model, and a reply to an ask that names no atom id is a red at the next turn"
town: local-maxxing
---
# goal:g7.16.1.11.46.14

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1 addendum): the council cut this leaf from hypothesis:g7161146-w1b-full-memory-beside-the-atoms (alive's [decision] 14:0xZ 10-24, 3/3 with all-is-one and self-perpetuating, read at trunk ebc2942b74; author belam YES via SM on S1-S4). Doc §40, §39, §12 (M7). Prerequisites: goal:g7.16.1.11.46.13 (M6, the store) and goal:g7.16.1.11.46.3 (M2, the atomizer, whose stub stands in until C1-C3). The card's real row ids are `<n>.<m>` and `a<n>` (doc:card-belam §7), so the id grammar must resolve both (R1).

## OWNER 2026-10-24, verbatim (doc:brainstorm-unify §40 quotes it)
> "one post can say on you asked to get X done this day at this time and it is recorded here in the graph and is being
> worked on or it didn't get transferred yet but I'll mark it for the spiders." · "every optmem/optchat little chunk is
> marked to an atom as needed, with multiple chunks able to map to a single atom as one chunk would be user doing it the
> other would be the agent acknowledging."

## OWNER atoms placed here (doc:card-belam §7 rows; they close to leaf:goal:g7.16.1.11.46.14 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 10.2 | every chunk is marked to an atom; several chunks map to one atom (the owner asking, the agent acknowledging) | target:§40 M7 |
| 10.4 | the post can say: you asked X at this day/time; recorded here, being worked on / not transferred yet, marked for the spiders | target:§40 M7 agi-atom where |
| 10.6 (tier-1 part) | classifiers via openrouter or our own; otherwise cheap haiku/sonnet | target:§40 tier 1 rides M2 (tiers 2-3 season 4) |

## Target end-state
- R1 each chunk carries `atom: <id>|none|?`, and the id grammar resolves the card's real row ids, `<n>.<m>` and `a<n>`.
- R2 a card row's `chunks:` list is DERIVED from the chunks, never hand-kept; a hand edit is overwritten or reported on the next derive.
- R3 `agi-atom where <words>` = regex over chunks -> atom -> exit -> leaf status, with no model; no hit prints `no chunk` with rc 1, never a nearest guess.
- R4 tier 0 (ids named, MANIFEST kinds) runs first; until C1-C3, M2's stub labels owner chunks `?`, never `none`.
- R5 the front post runs walk checks 1-2 on its new chunks each turn (an ask chunk with no atom is cut; an atom with no ack chunk is listed first); a post reply to a `kind: ask` chunk that names no atom id is a red at the next turn: it counts in M4's intake red cell (goal:g7.16.1.11.46.5) plus one notice line with its own bracket and an 8-hex token.

## Invariants
- The edge lives on the many side (the chunk names the atom); the atom's list is only ever derived.
- `where` never guesses: a miss is rc 1.
- Spend: tier 1 rides M2's credits lane (a stub until C1-C3); no openrouter key.

## Falsifier
1. `sh extensions/agi/tests/atom-edge.t.sh` exits 0 with one lane per row R1-R5, and each MUTANT reads RED: (R1) `atom: 10.2` does not resolve · (R2) a hand edit of a `chunks:` list survives the next derive unreported · (R3) a planted chunk does not return chunk id, atom id, exit and status; unknown words return rc 0 or a guess · (R4) the stub returns `none` for an owner chunk · (R5) a planted ask + a reply naming no id reads green at the next turn, or a reply naming the id reads red.
2. (a) the derive lane asserts >= 1 ask+ack row on a PLANTED store under the gate's own uid (a hand-labelled `kind: ask` chunk + an ack chunk naming its id); mutant: zero `chunks:` fields -> RED. (b) the live run, AS the facing uid, prints `done-when(4): <k> rows ask+ack, <q> owner chunks ?`: an OPEN line while M2's stub stands in (it writes `?`, and `kind: ask` is a tier-1 label, so no live ask+ack row can exist yet), and RED once C1-C3's atomizer has landed (the turn-over point: goal:g7.16.1.11.46.3's live leg) and k = 0. (c) Negative, live, as the facing uid: every chunk id listed in a `chunks:` field of doc:card-belam §7 resolves to a chunk whose `atom:` names that row; the zero-field case prints `chunks: 0 listed`, never a bare ok (mutant: one hand-added chunk id that no chunk names -> RED).

## Out of scope
goal:g7.16.1.11.46.13 (M6, the store) · goal:g7.16.1.11.46.3 (M2, the atomizer itself) · M8 the per-lap walk and the batched relay (wave 3) · tiers 2-3 classifiers (season 4).

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 (director-general-2 10-24, council [decision] 19:0xZ 3/3, rows A + R + W + two small ones; the node's rows are unchanged): the live check showed the label grammar still counted a bare a<n> (belam's prose listed rows bare, so a1/a2 linked three chunks): an id now counts only MARKED, a<n> and a dotted id alike (`atom a1` | `atoms: a1 10.2` | `[a1, 10.2]`), after the same strip. The recompute has ONE owner: `agi-mem label --all` = a redo over every live post chunk (mem/<date>/, not retired), then `agi-atom derive`, printing `relabelled k/m post chunks` (rc 1 unless k = m; `mem: unread`, rc 1, on a store it cannot read). `nested` RETIRES its `fix` (it was a second recompute, and a redo before A re-linked a1/a2): it stays a REPORT-only diagnostic (`nested-fence chunks: N`), so the small row 'nested fix passes the rc through' has no verb to apply to. `label --redo` on an OWNER chunk prints `label --redo: c:ID is an owner chunk` and exits 1 (was a silent rc 0). W: one line in skills/agi-send: ack with `atom <id>` as plain text, never in backticks or quotes. Named for the close (F3): the fail-closed cases (an odd " eats a prose ack; a post's own ack in backticks) are a loud false [unnamed-reply] red, beside the 4-space indented block that is out of scope.
v2 (belam 14:2xZ 10-24, council [decision] 14:1xZ 3/3 G2 with sp's amendment, node-text correction; rows unchanged): falsifier 2 as written could not run (the store is 0700 under the facing uid, R1 of .46.13) and passed on zero `chunks:` fields; it is now (a) a planted-store derive lane under the gate's uid, (b) a live done-when(4) line that is open while the stub stands in and red after C1-C3 with k = 0, (c) the live resolve negative with an explicit `chunks: 0 listed`. M7 is not held to C1-C3.
v1 (belam 10-24 14:0xZ, minted by the brief's author on the council's word: "belam writes the two leaves (.46.13 M6, .46.14 M7) on the trunk; DG2 is the Assigned director of both"): rows R1-R5 are the council's decision in substance, each turned into a target line and a mutant lane. The R5 notice's bracket name is left to DG2 (the council fixed only its shape: own bracket + 8-hex token).
<!-- THOUGHT:END -->
