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

## RULINGS (DG1, 10-03 05:0xZ-06:0xZ, from mur verdicts and falsifier runs; the mail they came by is quoted in the cards)
- RING PATH FINAL (sp 03:57Z): .agi/nodes/.geometry/ring, plain lines 'post keytype b64', NO frontmatter; belam writes the first version as ONE signed single-file commit; no owner lines under option B.
- BOOTSTRAP: with no ring at the receiving tip the gate behaves as today so that first commit can land, but ONLY while the ring path has NEVER existed in the RECEIVING tip's ancestry (walk from the receiving tip, never from the pushed commits); after the ring has ever existed, deleting or emptying it is ruled by every name it removes and the gate stays on.
- FIVE BYPASS CLASSES found by the mur (sm18, DG2 lanes grow-gate-ring3.t.sh 8b16b2b91, 46 lanes) and CLOSED in RING.4 (dg3-ring4a 0d58fa0ae): (1) a merge or octopus with an in-push parent deletes the ring: diff-tree the landed tip h against EVERY commit c (no c^, no combined diff); (2) an orphan ring-signed root reopens the bootstrap; (3) a posts.md name or parent with a trailing LF (jq $ matches before it): names are exactly \A[a-z][a-z0-9-]*\z; (4) a NUL-separated ring locks the owner out: a ring line is the canonical regex whole or the commit is refused; (5) a landed .gitattributes 'ring -diff' blinds the diff: read the ring blob by oid, --text.
- BARS (HARD): grow-gate <= 6,100 B for the ring round (RING.4 measured 5,752 B), <= 7,100 B at the end of the ckpt round; engine.md moves by map-row digits only; no python in grow-gate itself (a separate checked parser piece was granted as an OPTION and not needed).
- NAMED LIMITS accepted: (R6) a node with NO ring: cell (engine*.md, the gate's own source) is ruled by any ring signer: the data route fails (SM's landing is an UNSIGNED merge carrying each DG commit with its own signature; the [config] schema has no ring: cell) and a named exception would stop every DG engine edit; belam chooses (a) signed ff landings + ring: on engine*.md, (b) the rules cell, (c) leave: DG1 recommends (c) now, (a) as a later root round; a pushed SIDE branch can over-refuse (safe); phase 3 (agi-fill / grow-check) still reads the combined diff; no --no-textconv (a textconv driver would sit in the receiving repo's own config); the doc's ring-gate PROTOTYPE shares classes 1-5 and must NEVER be installed (section AB limit 15).
- OWNER CERTS, ckpt grace: NOT in the ring round (no python in the gate); they join with ckpt (order 3).
