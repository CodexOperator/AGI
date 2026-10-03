---
id: hypothesis:g716111-ab-a-nested-post-quantum-inner-signature-must-verify-and-a-generation-cannot-sign-past-its-leaves
mint_id: 44eac3a55c774246b357dd01db7ab1a5
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) cases P1-P3 and N1-N4: the Winternitz-Merkle prototype (w = 16, 67 chains, h = 8) signs and verifies, a tampered message and another generation's root fail, an honest nested blob verifies on both layers, a forger with the OUTER key who changes the payload fails the inner (outer yes, inner no), an invented inner fails, stripping the outer and forging only the inner fails; (b) ckpt verifies a NESTED blob (outer ed25519 against the ring, inner against the ring's pq column) and refuses a block whose inner fails; (c) the leaf index is the number of blocks already carrying this post's signature under this root (the DAG is the counter), a generation that exhausts its 2^h leaves cannot sign another block and its successor can; (d) the post writes a block before it signs another, so a block signed and never written cannot repeat an index; (e) the inner on EVERY commit (a 2,404 B trailer) is a cell, OFF by default."
title: "AB.5: the block signature blob is OUTER over payload plus INNER, the inner is a hash-only signature against the ring's PQ column, a forger holding only the OUTER key still fails the inner, and a generation that has used its 2^h leaves cannot sign another block (AA2.67, AA2.70, AA2.73)"
town: core
---
# hypothesis:g716111-ab-a-nested-post-quantum-inner-signature-must-verify-and-a-generation-cannot-sign-past-its-leaves

## Measured
- doc:radically-simple-engine section AB (landed, trunk 1c0edcf20: AB + AB.5 + AB.6 + the AGI_SEAL_ID cell, byte-equal to self-perpetuating's branch); belam [decision] 03:07Z, owner 02:3xZ 'Is the design finished and looks sound? If so send on'. Terms: SM lands first (met), DG1 writes from the LANDED text, DG2 falsifiers, DG3 builds, SM gates, every root act its own belam GO, AA2.63 is the gate (the 8 KB base).
- AB.5 measured: keygen 0.19 s for 256 signatures, sign and verify under 1 ms, signature 2,404 B, ring column 32 B; no PQ library exists on this box (no oqs, no pyspx, no ML-DSA in cryptography 41 or OpenSSL 3.0).
- pq.py whole is 1,509 B (sha256 d0e37a478bc590a8), a PROTOTYPE: plain Winternitz with no bitmasks, weaker than WOTS+, XMSS or SLH-DSA, STATEFUL (a leaf must never sign twice). It measures the nesting and the sizes, not a production PQ scheme (limits 8, 9, 10).

## CLAIM
(a) cases P1-P3 and N1-N4: the Winternitz-Merkle prototype (w = 16, 67 chains, h = 8) signs and verifies, a tampered message and another generation's root fail, an honest nested blob verifies on both layers, a forger with the OUTER key who changes the payload fails the inner (outer yes, inner no), an invented inner fails, stripping the outer and forging only the inner fails; (b) ckpt verifies a NESTED blob (outer ed25519 against the ring, inner against the ring's pq column) and refuses a block whose inner fails; (c) the leaf index is the number of blocks already carrying this post's signature under this root (the DAG is the counter), a generation that exhausts its 2^h leaves cannot sign another block and its successor can; (d) the post writes a block before it signs another, so a block signed and never written cannot repeat an index; (e) the inner on EVERY commit (a 2,404 B trailer) is a cell, OFF by default.

## Dispatch line
config-max: the leaf-count cell (h) and the inner-on-commits cell (off) / template-max: none / code: the pq piece (a new engine PIECE) and the ckpt delta that checks the inner; base map +~58 B for pq.

## FALSIFIERS
AA2.67: P1-P3 and N1-N4 in a shell test that calls pq.py through python3 (cryptography is not needed: sha256 only).
AA2.70: ckpt holds a block with a valid nested blob and refuses the same block with a wrong inner (the outer still good).
AA2.73: a scratch generation built with h = 2 (4 leaves): the 5th block signature is refused by the signer, the next generation's first signature is accepted, and the index equals the count of blocks already carrying the post's signature under the root.
Mutations RED: inner not checked (N2/N3 RED), leaf index taken from a local counter (AA2.73 RED), the root read from the wrong generation (P3 RED).

## TESTS
Shell plus python3 for pq.py; throwaway keys at run time; small h for the exhaustion case. No live key, no network, nothing pushed: scratch keys generated at run time in a throwaway dir (no test file, node or commit message holds an armoured block; spell the header with dots). Every ROOT act (a unit edit, the out-line in engine-root, retiring agi-signers, block_push, seal.yml on master) is its own belam GO with before-state and rollback; the build lands the bytes, belam installs them.

## FILE SCOPE
The pq piece (engine*.md piece list + map line), the ckpt delta, one new test file.

## HELD (named, not built)
AA2.61 (a real PQ column, ML-DSA or SLH-DSA, under the hybrid cell): UNRUN until a verifier exists on the box; the PQ column is one more column value the day it does. Limit 8: the prototype is not a production scheme.

## CEILING
1 parent - kids <= 1 - pq <= 1,509 B whole - the inner is a cell, off for commits - 1 new test file - 0 USD - regular review + security mur on root code. Depends on: the ckpt hypothesis.

## RULINGS (DG1, 10-03 05:0xZ-06:0xZ, from mur verdicts and falsifier runs; the mail they came by is quoted in the cards)
- RULINGS on DG2's pq-nest.t.sh 55b9a0c78 (24 lanes; with the doc's pq.py + un-nested ckpt 18 ok / 6 FAIL = k2 k3 k4 e2 e3 d1, the build's scope): (d) AA2.73(d) is pinned: ckpt sign (nested) records its signed leaf index in the post's own state and REFUSES a second signature while that index's block is not yet visible in the DAG (d1 back to back refused, d2 fresh leaf once a block carrying the first is visible); (e) the inner-on-commits cell is pinned DEFAULT-OFF only (a signed commit with the cell absent carries no pq trailer, < 1,500 B); the ON state is HELD. SEAMS: AGI_PQSEED = a file with b64 of 32 B, AGI_PQH default 8, the ring line 'post pq-sha256 b64root' with pub = the post's name; a missing or wrong inner under a pq column is not counted; no column = outer-only.
