---
id: hypothesis:g716111-ab-a-block-holds-only-with-k-current-pairwise-level-adjacent-signers-and-grace-ends-when-the-lowest-block-seals-the-hand-off
mint_id: c63a3fa7f89b4a1f91e81b3f026b32dc
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) cases L1-L8 give the section's verdicts: DG1+DG2 (level 3) hold; SM+DG1 sealing a level-3 block hold; alive+all-is-one+SM sealing level 2 hold; belam+DG1 (levels 1 and 3), owner+alive (levels 0 and 2) and a single signer with k = 2 do not hold; the owner CA key plus belam is the anchor block and holds; (b) grace and sealing T1-T10: a retired key signs inside its grace window before any holding block contains its hand-off, is refused once the LOWEST block seals the hand-off at any date, a backdated commit is refused, a block over an OLDER tip than a block it seals does not hold, an owner cert expired before the newest holding block's time is refused; (c) the hybrid cell H1-H5: a block holds only when EVERY algorithm of AGI_SIGN verifies (an ed25519-only block does not hold under a two-column cell, a missing column fails), a block naming a hash outside AGI_HASHES does not hold; (d) a block's tree is ONLY tip, time, hash, sigs/<post>.<n> (an extra file such as 'evil name' makes it not hold, cases B1/B2), so every path the AGI_SUBJECT recipe reads is plain ASCII; (e) AA2.62's composite gpg.ssh.program is NOT built: AB.5 retires it for blocks (the nest lives in the block's one signature blob); commits stay classical."
title: "AB: ckpt (the calendar) - a block under refs/agi/block/* holds iff its tree is only tip, time, hash, sigs/<post>.<n>, every signer is current at its tip in every AGI_SIGN column, the signers are pairwise level-adjacent and at least k, and a ring change no holding block contains keeps the closed line verifying until the lowest block seals it (AA2.57, AA2.58, AA2.59)"
town: core
---
# hypothesis:g716111-ab-a-block-holds-only-with-k-current-pairwise-level-adjacent-signers-and-grace-ends-when-the-lowest-block-seals-the-hand-off

## Measured
- doc:radically-simple-engine section AB (landed, trunk 1c0edcf20: AB + AB.5 + AB.6 + the AGI_SEAL_ID cell, byte-equal to self-perpetuating's branch); belam [decision] 03:07Z, owner 02:3xZ 'Is the design finished and looks sound? If so send on'. Terms: SM lands first (met), DG1 writes from the LANDED text, DG2 falsifiers, DG3 builds, SM gates, every root act its own belam GO, AA2.63 is the gate (the 8 KB base).
- ckpt whole is 2,666 B (sha256 9ce7cd418feb4c90), the prototype the L, H and T cases ran on; AGI_CKK is the k per level cell ('0:2 1:2 2:2 3:2', default 2). The 2nd algorithm column was ECDSA P-256 as a STAND-IN: OpenSSH 9.6 has no PQ signature type, and the AND is algorithm-blind.
- Base: ckpt is one map line, about +62 B (section AB bytes table); AA2.63 decides whether it fits.

## CLAIM
(a) cases L1-L8 give the section's verdicts: DG1+DG2 (level 3) hold; SM+DG1 sealing a level-3 block hold; alive+all-is-one+SM sealing level 2 hold; belam+DG1 (levels 1 and 3), owner+alive (levels 0 and 2) and a single signer with k = 2 do not hold; the owner CA key plus belam is the anchor block and holds; (b) grace and sealing T1-T10: a retired key signs inside its grace window before any holding block contains its hand-off, is refused once the LOWEST block seals the hand-off at any date, a backdated commit is refused, a block over an OLDER tip than a block it seals does not hold, an owner cert expired before the newest holding block's time is refused; (c) the hybrid cell H1-H5: a block holds only when EVERY algorithm of AGI_SIGN verifies (an ed25519-only block does not hold under a two-column cell, a missing column fails), a block naming a hash outside AGI_HASHES does not hold; (d) a block's tree is ONLY tip, time, hash, sigs/<post>.<n> (an extra file such as 'evil name' makes it not hold, cases B1/B2), so every path the AGI_SUBJECT recipe reads is plain ASCII; (e) AA2.62's composite gpg.ssh.program is NOT built: AB.5 retires it for blocks (the nest lives in the block's one signature blob); commits stay classical.

## Dispatch line
config-max: AGI_SIGN, AGI_HASHES, AGI_CKK cells (data) / template-max: none / code: the ckpt piece (a new engine PIECE, sign and check) and its map line.

## FALSIFIERS
AA2.58: L1-L8 and AA2.57's T1-T10 as the section tabulates them, RED on a tree without ckpt, RED under one-edit mutations (k ignored = L8 RED; level adjacency dropped = L4/L7 RED; the lowest-block seal dropped = T5 RED; the ring read at the commit date = T3b RED; the hash name unchecked = H4/H5 RED).
AA2.59: H1-H5 under a two-column AGI_SIGN (ed25519 AND the stand-in), with the column read from the key type ssh-keygen prints.
AA2.57b: the same T lanes through agi-land with the integrated grow-gate as GROW_GATE are all-is-one's lane (PASS reported at 03:5xZ); DG2 does not rebuild them.
AA2.58b: B1/B2, the tree-only rule.

## TESTS
Shell with a throwaway CA and post keys generated at run time; blocks written as the section's fixture recipe says (ckpt sign, a tree of tip/time/hash/sigs, git commit-tree with -p per sealed block, update-ref refs/agi/block/<name>). No live key, no network, nothing pushed: scratch keys generated at run time in a throwaway dir (no test file, node or commit message holds an armoured block; spell the header with dots). Every ROOT act (a unit edit, the out-line in engine-root, retiring agi-signers, block_push, seal.yml on master) is its own belam GO with before-state and rollback; the build lands the bytes, belam installs them.

## FILE SCOPE
The ckpt piece in engine.md's piece list (a new section of the right engine*.md file), its map line, one new test file. The ring node comes from the ring hypothesis.

## CEILING
1 parent - kids <= 1 - ckpt <= 2,666 B whole and about +62 B on the base map - 1 new test file - 0 USD - regular review + security mur on root code. Depends on: the ring-is-a-trunk-node hypothesis.

## RULINGS (DG1, 10-03 05:0xZ-06:0xZ, from mur verdicts and falsifier runs; the mail they came by is quoted in the cards)
- ROUND GATE (DG1): the ckpt round adds to grow-gate the ckpt GRACE wiring (AGI_CKPT) and a python-free owner-cert expiry read (ssh-keygen -L, or its own piece, measured); grow-gate <= 7,100 B HARD at the end of the round (ring 6,100 + the delta). DG2's file ckpt.t.sh 7e74b8c07 (32 lanes): RED on the trunk ('FAIL no ckpt piece', exit 99); the doc's ckpt + the ring build as the gate = 30 ok / 2 FAIL (t2 grace wiring, t10 cert read) = exactly the ckpt round's scope. Starting text = the landed 2,666 B; report the exact bytes and the map-row delta; both rail tiers reported.
