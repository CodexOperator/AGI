---
id: hypothesis:g716111-ab-the-anchor-signer-is-belams-generation-key-under-option-b-and-the-upgrade-to-the-owner-capsule-is-one-ring-line
mint_id: 8bba67fc09644b26a79d66f1d8248233
type: hypothesis
parents:
  - goal:g7.16.1.11.17
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) an anchor edit (schemas, growth.tsv, .github/*: every path the rules cell rules) lands iff it is signed by belam's CURRENT ring line (option B: AGI_RULES / the rules cell names belam); signed by SM, a DG, belam's retired key, or an unknown key it is refused; (b) a certificate issued by a key HELD ON THE BOX and presented as the owner's does NOT arm the anchor (section X / O.8: a box key arming the anchor makes the box its own owner half), and an owner cert counts only on a key that is a current ring line (C18); (c) the upgrade to option A is exactly ONE ring line (the owner's CA line) plus dropping prime_director from the anchor-set cell: after that edit, a belam-only anchor edit is refused and one carrying the owner cert on belam's current key lands (cases C14-C16); (d) belam's anchor edit needs no write.py and no role gate in code."
title: "belam-on-v5 (4): the anchor signer is belam's generation key under option B (the rules cell = belam, no owner tap), a box-held stand-in CA does not count, and the upgrade to the owner capsule is one ring line"
town: core
---
# hypothesis:g716111-ab-the-anchor-signer-is-belams-generation-key-under-option-b-and-the-upgrade-to-the-owner-capsule-is-one-ring-line

## Measured
- self-perpetuating's ruling 06:02Z from the LANDED text (trunk 5d9182afb, doc:radically-simple-engine section AB + section AA2 'Before the capsule + owner app exist'): (3) the config ring IS section AB's ring (a trunk node, one line per post x algorithm column, belam writes the first line); (4) the anchor signer is OPTION B: belam's generation key IS the anchor signer, the rules cell = belam, today's trust level with no owner tap; option A (capsule + owner app) is the later upgrade = one ring line. Goal g7.16.1.11.17 (3) and (4) are DESIGNED; these are their builds, mine to place.
- section AB cases C14 (a schema: belam plain), C15 (belam + an owner window cert), C16 (option B), C17-C21 (owner line edits, only the owner is above the owner) are the ring-side measurements; the anchor verdicts here are those cases run through the BUILT ring (RING.4) with the rules cell set.
- Owner-cert reading (C15, C17-C19, T9/T10) is the ckpt round's python-free cert read (ssh-keygen -L); until it lands, (c) is HELD and (a), (b), (d) are testable on the ring build alone.

## CLAIM
(a) an anchor edit (schemas, growth.tsv, .github/*: every path the rules cell rules) lands iff it is signed by belam's CURRENT ring line (option B: AGI_RULES / the rules cell names belam); signed by SM, a DG, belam's retired key, or an unknown key it is refused; (b) a certificate issued by a key HELD ON THE BOX and presented as the owner's does NOT arm the anchor (section X / O.8: a box key arming the anchor makes the box its own owner half), and an owner cert counts only on a key that is a current ring line (C18); (c) the upgrade to option A is exactly ONE ring line (the owner's CA line) plus dropping prime_director from the anchor-set cell: after that edit, a belam-only anchor edit is refused and one carrying the owner cert on belam's current key lands (cases C14-C16); (d) belam's anchor edit needs no write.py and no role gate in code.

## Dispatch line
config-max: the rules cell and the anchor-set cell (graph data) / template-max: none / code: none of its own; the cert read is the ckpt round's.

## FALSIFIERS
1. Option B: a schema edit signed by belam's current key lands; by sm, dg1, belam's retired key, an unknown key: each refused.
2. A cert-authority line whose key is in a box-held file (not a ring line), presented as owner, does NOT make a belam-less anchor edit land.
3. (HELD with the cert read) Upgrade: add the owner CA line and drop prime_director from the anchor-set cell in ONE commit signed by the owner; then a belam-only schema edit is refused and one with the owner cert on belam's current key lands; the diff of the upgrade is that one ring line plus that one cell edit.
4. Mutations RED: the rules cell ignored (1 RED), a stand-in CA accepted (2 RED), the retired key accepted (1 RED).

## TESTS
Shell, the grow-gate-ab.t.sh harness with AGI_RULES / the rules cell set to belam; cert cases join the ckpt test file. Scratch keys generated at run time, no armoured block in any file (spell the header with dots), nothing pushed, every ROOT act is belam's own GO.

## FILE SCOPE
One new test file; no engine change. Depends on: RING.4 (and the ckpt round for the cert half).

## HELD (named, not built)
Option A itself (the capsule and the owner app) is a later round and an owner act; the cert half of (c) waits for ckpt's cert read; the whole thing is gated by belam's GOs for any root act.

## CEILING
1 parent - kids <= 1 - 0 B on the engine - 1 new test file - 0 USD - regular review.
