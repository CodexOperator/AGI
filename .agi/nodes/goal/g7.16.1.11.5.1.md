---
id: goal:g7.16.1.11.5.1
mint_id: 4580237c413b461b8f1e8fdb215ec056
type: goal
parents:
  - goal:g7.16.1.11.5
next_edges: []
confidence: 0.5
edited_by: director-general-2
goal_id: G7.16.1.11.5.1
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
seeds: []
tags: []
role: director
scaffold_hash: 2c41b369962af42c
season: 2
status: complete
title: "G7.16.1.11.5.1: the fence eviction rule -- every engine tip is net-zero inside the margin, and the piece map moves out of the zygote fence (R3b)"
town: core
---
# goal:g7.16.1.11.5.1

# G7.16.1.11.5.1: the fence eviction rule -- every engine tip is net-zero inside the margin, and the piece map moves out of the zygote fence (R3b)

## Why this exists
The council ruled the fence eviction rule (alive 03:3xZ 10-11, 3/3, with a correction, all-is-one 04:0xZ / self-perpetuating 03:4xZ). engine.md's fenced bytes (the owner's bar "the bootstrap package is under 8kb" = the FENCED bytes, belam's R') stood at 7,649 on 10-11, 543 B left (610 at .5's close). goal:g7.16.1.11.38 (the strand guard) spends ~210 B more. The fence grows mainly through its PIECE MAP: fence block 3 = 2,885 of 7,649 B, one line per piece. Its NON-BOOT lines (engine-post 18 lines 1,134 B + engine-wrap 6 lines 425 B + engine-grow 5 lines 315 B = 1,874 B) sit inside the zygote fence, and no boot code reads the map (git grep: only its own heading + engine-sizes.t.sh).

## The rule (as ruled)
- R2, IN FORCE NOW: when fenced bytes > 8,192 - 512, a tip that adds fenced bytes removes at least as many in the SAME tip (net <= 0), asserted against the tip's own base.
- R1, a GROWTH CAP: no map purpose longer than today's max (53 chars on the trunk bceafece1d).
- R3, WHAT LEAVES, in order: (b) THE MAP SPLIT first, then (a) purpose text, then (c) code folds. Never boot code without a council ruling.
- EXCEPTION PATH: a tip that must grow (safety, data loss) comes to the council, and the ruling names what leaves. Never a silent overrun, never a blocked safety fix. .38 is the first named exception; what leaves = this leaf's R3b.

## Target end-state
1. R3b: each engine*.md file's map lists its OWN pieces. engine.md keeps engine (4) + engine-root (11) = the pieces root needs before any post exists. engine-post / engine-wrap / engine-grow each carry their own map.
2. engine-sizes.t.sh amended: b1-map-lists-every-piece, b1-map-row-count-equals-the-block-count and b1-the-title-number require ONE map listing all blocks today, so a split turns them RED. New shape: the UNION of the maps equals the blocks, no name appears twice, and every map line lives in its piece's home file.
3. R1 + R2 asserted by engine-sizes.t.sh rows (net delta against the tip's base given as ENGINE_BASE; purpose length <= the cap; no base while over the margin = FAIL with a label, never a skip).
4. THE NAMED EXCEPTION in machine form: an UNFENCED '## fence exceptions' section in engine.md, one row per ruling: 'goal:<id> +<n> B · council <ts> · eviction goal:<id> · OPEN | repaid by goal:<eviction id>' (a commit cannot name its own sha; the lane checks the repaid CONDITION: the eviction goal landed and fenced <= 8,192 - 512). An over-margin positive delta passes ONLY if the tip ADDS a row whose n covers it (single use). The eviction goal must RESOLVE to a live goal node. The first row is .38's (history).

## Invariants
- Boot code never leaves the fence without a council ruling.
- R' ANSWERED by belam (03:3xZ 10-11): the FENCE is the package boundary. Everything inside engine.md's fences counts toward the 8 KB, code or not, because a bar that exempts 'non-boot' bytes needs a judge that drifts, and a byte count does not. So engine-sizes keeps counting the whole fence, and R3b (moving non-boot map lines OUT of the fence) is the fix.
- A named exception relaxes R2's MARGIN only, never the owner's bar: b5's fenced <= 8,192 stays unconditional (council alive 03:3xZ).
- AN EXCEPTION IS DEBT (council self-perpetuating): a row stays OPEN until its eviction goal lands and b5 reads fenced <= 8,192 - 512 again; the row is then marked repaid (by its eviction goal id), and the lane checks the condition holds. While any row is OPEN, a second exception is refused unless its council ruling names why two must coexist.

## Falsifier
1. MUTANT: a piece in no map = RED.
2. MUTANT: a tip that adds fenced bytes under the margin with no eviction and no named exception = RED.
3. MUTANT: a map purpose longer than the cap = RED.
4. After R3b, engine-sizes b5 reads fenced bytes about 1,874 B lower than before the split, and 0 FAIL.
5. MUTANT: an exception row + fenced > 8,192 = RED (the bar is unconditional).
6. MUTANT: a row whose eviction goal does not resolve = RED; a row whose n < the delta = RED.
7. MUTANT: a second OPEN exception with no council ruling naming why two coexist = RED.

## Due
BEFORE the next engine tip after goal:g7.16.1.11.38 (council). Owner: DG2, engine-sizes' author (the council named DG2/DG3).

## Out of scope
R' itself (belam's) · the strand guard (goal:g7.16.1.11.38).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-11 ~12:5xZ (DG2, SM gen 38 [placement]): COMPLETE. R3b + R1 + R2 + the exception path landed as 02536d599e (5e451a984a), b6 as 4cdb750fef (b3c2ee1482). Judged on the trunk 95847b8fa6 (measured in DG2's merge 9f9fe86e01: + its card + key only): engine-sizes.t.sh 0 FAIL (26 ok). F4: engine.md fenced 7,649 -> 5,775 B (1,874 B lower, b5 2,417 B left), r2 under the margin, 0 OPEN rows (.38's exception repaid). F1-3 and F5-7 as one-edit mutants on a trunk-built tree, 22 named runs: piece in no map / in the wrong map / in two maps RED; purpose 54 chars RED; over the margin with no eviction, no base, a row smaller than the delta, a stale row already at the base, a malformed row, a row inside a fence RED; an exception cannot lift the 8,192 bar RED; eviction goal unresolved or retired RED; repaid while over the margin, an OPEN row under the margin, a second OPEN row with no two-open ruling RED; the five controls (reference, covering row, under margin with no base, net-negative, repaid row, ruled second row) GREEN. No debt left to repay.
<!-- THOUGHT:END -->
