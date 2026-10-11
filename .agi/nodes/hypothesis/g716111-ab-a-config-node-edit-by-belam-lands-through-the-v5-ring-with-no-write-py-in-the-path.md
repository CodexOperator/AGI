---
id: hypothesis:g716111-ab-a-config-node-edit-by-belam-lands-through-the-v5-ring-with-no-write-py-in-the-path
mint_id: 6200f3e42ba6427cb0b7d933ee7cc2d5
type: hypothesis
parents:
  - goal:g7.16.1.11.17
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) belam writes the FIRST ring version as ONE signed single-file commit, one line per post per column, and the ring-gate admits it under the bootstrap rule (the ring path has never existed in the tip's history); (b) after it, a commit that edits a [config] node and is signed by belam's current ring line lands through grow-gate, with write.py absent from the process (the test environment has no write.py on PATH); (c) the same edit signed by a DG or by SM is ruled by the node's ruler as the ring hypothesis defines it (a ring: cell, else any ring signer: the named limit R6 until belam chooses) and the test pins the verdict that build gives, it does not invent a stricter one; (d) belam's edit signed by a RETIRED generation key, or by a key not in the ring, is refused; (e) the only-owner-and-prime_director-write-config rule of goal .17 stays true by the ruler cells, not by a role gate in code."
title: "belam-on-v5 (3): a config-node edit signed by belam lands through the v5 ring with no write.py in the path, and belam's first ring commit is the bootstrap that makes the ring exist"
town: core
---
# hypothesis:g716111-ab-a-config-node-edit-by-belam-lands-through-the-v5-ring-with-no-write-py-in-the-path

## Measured
- self-perpetuating's ruling 06:02Z from the LANDED text (trunk 5d9182afb, doc:radically-simple-engine section AB + section AA2 'Before the capsule + owner app exist'): (3) the config ring IS section AB's ring (a trunk node, one line per post x algorithm column, belam writes the first line); (4) the anchor signer is OPTION B: belam's generation key IS the anchor signer, the rules cell = belam, today's trust level with no owner tap; option A (capsule + owner app) is the later upgrade = one ring line. Goal g7.16.1.11.17 (3) and (4) are DESIGNED; these are their builds, mine to place.
- section AB table cases C1, C2, C4, C7-C13 (a post's current key, hand-off, re-vouch by the parent, ringed nodes) already cover the ring half; what is NEW here is the first-version bootstrap by belam and the absence of write.py. The ring node does not exist on the trunk yet (belam writes v1; no owner lines under option B).
- Today a CHANGED node gets no signer check at all; R6 (a node with no ring: cell is ruled by any ring signer) is the named limit in the ring hypothesis and belam's decision (a / b / c) is open.

## CLAIM
(a) belam writes the FIRST ring version as ONE signed single-file commit, one line per post per column, and the ring-gate admits it under the bootstrap rule (the ring path has never existed in the tip's history); (b) after it, a commit that edits a [config] node and is signed by belam's current ring line lands through grow-gate, with write.py absent from the process (the test environment has no write.py on PATH); (c) the same edit signed by a DG or by SM is ruled by the node's ruler as the ring hypothesis defines it (a ring: cell, else any ring signer: the named limit R6 until belam chooses) and the test pins the verdict that build gives, it does not invent a stricter one; (d) belam's edit signed by a RETIRED generation key, or by a key not in the ring, is refused; (e) the only-owner-and-prime_director-write-config rule of goal .17 stays true by the ruler cells, not by a role gate in code.

## Dispatch line
config-max: the rules cell (belam, option B) / template-max: none / code: none of its own: it is a TEST on the ring build (grow-gate-ab and the ring-gate pieces) plus the first-ring procedure written as belam's own commit.

## FALSIFIERS
1. In a scratch repo with no ring in history, a single-file commit adding .agi/nodes/.geometry/ring (one canonical line per post per column) signed by belam lands; the same commit unsigned, signed by a DG, or touching a second file is refused.
2. With that ring, a commit that edits a [config] node signed by belam's current key lands, rc 0, and `command -v write.py` fails in the test's PATH.
3. The same edit signed by belam's RETIRED generation key (after a hand-off), and by a key absent from the ring, is refused.
4. The same edit signed by dg1 gets exactly the verdict the ring build gives a node with no ring: cell (pinned, with R6 named in the test header), and by sm likewise.
5. Mutations RED: the bootstrap never opens (1 RED), the signer check dropped (3 RED), a write.py call added to the path (2 RED).

## TESTS
Shell, the grow-gate-ab.t.sh harness (scratch repo borrowing objects, run-time keys). Scratch keys generated at run time, no armoured block in any file (spell the header with dots), nothing pushed, every ROOT act is belam's own GO.

## FILE SCOPE
One new test file; no engine change. Depends on: the ring build (RING.4) landing and belam writing the first ring.

## HELD (named, not built)
The real first ring commit is belam's own act (his key, his GO). R6's choice is belam's [decision] (open).

## CEILING
1 parent - kids <= 1 - 0 B on the engine - 1 new test file - 0 USD - regular review.
