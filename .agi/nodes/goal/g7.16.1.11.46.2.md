---
id: goal:g7.16.1.11.46.2
mint_id: cb9050d5018d4554b85f649be8d91db0
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: director-general-2
goal_id: G7.16.1.11.46.2
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - M1
season: 3
status: complete
title: "G7.16.1.11.46.2: M1 -- every inbound ask is a card §7 row with a verbatim slice of a named source, written and closed only by agi-atom add|close into a closed state set; the card guard counts §0-§6 only"
town: local-maxxing
---
# goal:g7.16.1.11.46.2

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1): the council cut wave 1 from hypothesis:g7161146-w1-protect-the-loop-and-measure (alive's [decision] 21:06Z 10-23, 3/3 with all-is-one and self-perpetuating, read at trunk 2ef3c2f6d6). Doc §37-§39 (M1). Box readings that shaped it: (K1) the 62 W0 rows in doc:card-belam §7 are paraphrases ("atom (owner ask, short)") and no ref holds the owner's pane bytes, so a verbatim check needs a SOURCE; (K4) rotate.py :8858/:9087 counts the WHOLE composed card against HANDOFF_CARD_LIMIT_LINES=100 (:7972) while card-belam is 171 lines, so belam's driven handoff refuses today. Doc sections implemented: §37, §38 (corrected by §39), §39 (doc:brainstorm-unify is reference, never placement).

## OWNER 2026-10-23, verbatim (doc:brainstorm-unify §37 and §39 quote it)
> "Trajectory holds the momentum data, optmem holds the state/location data." · "if I fire off a stream of ideas … some of
> the smaller points of said brainstorm inevitably slip through the cracks."
> "each post's atoms hold the position data for that post as it relates to the momentum data in the trajectory. Each agent
> knows where they are, what they should do next, who is around them, and the momentum tells them how the whole graph is
> moving as a whole."

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.2 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 7.1 | optmem for the Prime; trajectory = momentum, optmem = state | target:§37 (this ledger is M5) |

## Target end-state
- A card's §7 row reads `| a<n> | "<slice>" | src:<box commit sha> or src:<node id>#OWNER | <state> | lap<n> |`; the 62 W0 rows are marked src:doc and held to the state check only.
- A piece `agi-atom` (shell, beside agi-at) with two verbs: `add` refuses a slice that is not a byte substring of its src (git cat-file -p <sha>, or the node's `## OWNER … verbatim` section); `close` moves a row from `target:` (open) to exactly one of leaf:<goal id> | idea:<id> | decision:<doc#line> | out:<reason>, and refuses an id that does not exist or a state outside the set.
- rotate.py's card guard counts §0-§6 only; CLAUDE.md "Cards and the handoff" and skill agi-rotate carry one line: "≤ 100 lines for §0-§6; §7 is bounded by age (an open atom older than one lap is a red), not length" (a RULES path: lands with belam).

## Invariants
- Owner words in a slice are never paraphrased: a slice is bytes of its source.
- A row has exactly one state; anything but target: is terminal.
- A card stays the post's ONE scratch: no intake node (§39 corrects §38).

## Falsifier
1. `sh extensions/agi/tests/agi-atom.t.sh` exits 0: lanes add-verbatim-ok, add-one-word-changed REFUSED, add-no-src REFUSED, close-to-real-id ok, close-to-absent-id REFUSED, close-outside-set REFUSED, and mutant m (agi-atom without the substring check) reads RED.
2. `sh extensions/agi/tests/card-cap.t.sh` exits 0: 101 lines in §0-§6 is refused; 500 lines in §7 passes; a mutant guard that counts the whole card reads RED on the second lane.
3. Negative: on the trunk after the land, `awk '/^## §7/,0' .agi/nodes/doc/card-belam.md | grep -E '^\| (a[0-9]+|[0-9]+\.[0-9]+) \|' | grep -vc 'src:'` prints 0: every §7 data row, the W0 rows included, carries a source (mutant: src: dropped from one W0 row makes it 1).

## Out of scope
V10a = .46.11 (sanctuary-master's leaf, minted in its own land) · the other wave-1 leaves .46.2-.46.10 · waves 2-4 (U2 U3 U6 V1 C4 C5 …) · season 4 (§15)

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-2 10-24 (CLOSE; council 3/3 04:47Z: re-run F3 after belam's host act, standing close form) falsifiers RE-RUN as written at trunk 3d601e9efe (L90 = 89a1dd7589; belam's `agi-atom grandfather` 08110dc30c): F1 `sh extensions/agi/tests/agi-atom.t.sh` 0 FAIL (28 lanes, 3 mutants RED); F2 `sh extensions/agi/tests/card-cap.t.sh` 0 FAIL (101 lines in sections 0-6 refused, 500 lines in section 7 passes, whole-card-count mutant RED); F3 on the trunk the awk|grep pipeline prints 0 (64 data rows, 0 without src:; the mutant with src: dropped from one row prints 1). The RULES lines are on the trunk (belam 7394e73c50). Deviations recorded at the merge-up: a lap is 4 h; the Falsifier text is unchanged.
<!-- THOUGHT:END -->
