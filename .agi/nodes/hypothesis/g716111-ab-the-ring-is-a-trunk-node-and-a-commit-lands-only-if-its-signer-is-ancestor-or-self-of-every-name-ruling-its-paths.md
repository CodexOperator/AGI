---
id: hypothesis:g716111-ab-the-ring-is-a-trunk-node-and-a-commit-lands-only-if-its-signer-is-ancestor-or-self-of-every-name-ruling-its-paths
mint_id: 09329faad8da491eb26502675041b12b
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) with the ring at .agi/nodes/.geometry/ring (one line per post x algorithm column, the owner line a cert-authority) and the closure of the posts tree's parent cells, grow-gate admits a commit iff its signer is a current ring line at the receiving tip (the ring advanced only by commits admitted before it) and, for every changed path, an ancestor-or-self of every name that rules it (a ring line: its post; a node: its ring: cell; schemas, growth.tsv and .github/*: the rules cell, belam as the interim option B; a tree move in posts.md: BOTH the old and the new parent); (b) the 58 scratch cases C1-C21 and E1-E8 and the rest of section AB's table give the section's verdicts through the INTEGRATED grow-gate, not the prototype; (c) no date is read: a backdated commit by a retired generation is refused; (d) agi-land keeps its landed ancestor-or-self signer rule and is not edited here; (e) the loop is grow-gate's own, so the delta is the projection, the closure, the tree-move rule and the two refusals."
title: "AB: the ring is one trunk node, and grow-gate (one loop, ring-gate folded in) admits a commit only if its signer is a ring line open at the RECEIVING tip and an ancestor-or-self of every name that rules each path it changes (AA2.54)"
town: core
---
# hypothesis:g716111-ab-the-ring-is-a-trunk-node-and-a-commit-lands-only-if-its-signer-is-ancestor-or-self-of-every-name-ruling-its-paths

## Measured
- doc:radically-simple-engine section AB (landed, trunk 1c0edcf20: AB + AB.5 + AB.6 + the AGI_SEAL_ID cell, byte-equal to self-perpetuating's branch); belam [decision] 03:07Z, owner 02:3xZ 'Is the design finished and looks sound? If so send on'. Terms: SM lands first (met), DG1 writes from the LANDED text, DG2 falsifiers, DG3 builds, SM gates, every root act its own belam GO, AA2.63 is the gate (the 8 KB base).
- ring-gate whole is 2,855 B (sha256 efa4fca6c8e8c8f1) as the PROTOTYPE the 58 cases ran on; section AB says in the build its loop IS grow-gate's loop. The ring node does not exist on the trunk yet (no .geometry/ring at 1c0edcf20).
- Trunk today: grow-gate 1,465 B + the private-key line (hypothesis g716111-aa2-the-trunk-refuses-every-node-that-carries-a-private-key-block, ordered, 1,748 B). This build edits the SAME piece: it lands AFTER the key-gate build, never in parallel.
- all-is-one ran AA2.57, AA2.65, AA2.80 through agi-land: PASS (their lane, not rebuilt here). AA2.55 (a box with ONLY the seed + the trunk reaches the same verdicts) needs two boxes: UNRUN.

## CLAIM
(a) with the ring at .agi/nodes/.geometry/ring (one line per post x algorithm column, the owner line a cert-authority) and the closure of the posts tree's parent cells, grow-gate admits a commit iff its signer is a current ring line at the receiving tip (the ring advanced only by commits admitted before it) and, for every changed path, an ancestor-or-self of every name that rules it (a ring line: its post; a node: its ring: cell; schemas, growth.tsv and .github/*: the rules cell, belam as the interim option B; a tree move in posts.md: BOTH the old and the new parent); (b) the 58 scratch cases C1-C21 and E1-E8 and the rest of section AB's table give the section's verdicts through the INTEGRATED grow-gate, not the prototype; (c) no date is read: a backdated commit by a retired generation is refused; (d) agi-land keeps its landed ancestor-or-self signer rule and is not edited here; (e) the loop is grow-gate's own, so the delta is the projection, the closure, the tree-move rule and the two refusals.

## Dispatch line
config-max: the cells AGI_SIGN, AGI_HASHES, AGI_CKK and the rules cell (as graph cells, not code) / template-max: none / code: the ring node (data), the projection (one sed from the ring to allowed_signers) and the ring-gate delta inside grow-gate's commit loop in engine-grow.md; no new piece.

## FALSIFIERS
AA2.54: C1-C21 and E1-E8 of section AB give the table's verdicts on the integrated grow-gate, run as ONE test file, one ok/FAIL line per case, RED on today's grow-gate for every refusal lane and RED under each one-edit mutation (the closure dropped = C8/C11 RED; the receiving-tip rule replaced by a date = C3b RED; the tree-move 'both parents' rule reduced to one = E1/E3 RED; schemas ruled by 'any ring member' = C14 RED; the owner line editable by belam = C20/C21 RED).
AA2.54b: the 17 AA3 lanes and the landed 6u/6v lanes still pass with the integrated grow-gate as GROW_GATE (all-is-one's harness), and the private-key line still refuses.
AA2.54c: `wc -c` of the grow-gate piece and the measure line in engine.md agree; config:engine and the seed do not grow (the delta is expansion).

## TESTS
Shell, the grow-gate-ring.t.sh harness pattern: a scratch repo borrowing the objects, a throwaway CA and post keys made at run time, tools read from the trunk by sect; GROW_GATE=<file> tests a candidate. The new cases go in ONE new file (grow-gate-ab.t.sh). No live key, no network, nothing pushed: scratch keys generated at run time in a throwaway dir (no test file, node or commit message holds an armoured block; spell the header with dots). Every ROOT act (a unit edit, the out-line in engine-root, retiring agi-signers, block_push, seal.yml on master) is its own belam GO with before-state and rollback; the build lands the bytes, belam installs them.

## FILE SCOPE
engine-grow.md (the grow-gate piece) and its measure line in engine.md; the ring node under .agi/nodes/.geometry/; one new test file. Nothing in engine-root or agi-land.

## HELD (named, not built)
AA2.55 (two boxes, seed-only): UNRUN until a second box exists; named, not built.

## CEILING
1 parent - kids <= 1 - grow-gate grows by the ring-gate delta (expansion; the prototype whole is 2,855 B, the integrated delta must be smaller and the builder reports the number) - config:engine and the seed 0 B - 1 new test file - 0 USD - regular review + security mur on root code.
