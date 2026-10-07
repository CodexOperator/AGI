---
id: hypothesis:g716111-ab-a-flow-rotation-run-cuts-one-block-per-phase-transition-signed-by-its-parties-only
mint_id: 974f4f81d19046feaf4db27169c4f4b3
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) a FLOW ROTATION run cuts exactly one block per phase transition; (b) each block is signed by that phase's parties only (the level-3 pair for a DG phase, SM plus a DG for a block sealing level 3, and so on up the layers) and holds under ckpt; (c) the block DAG, read from refs/agi/block/*, has the same shape as the run's phase tree: a sub-phase's block is a git parent of the block that seals it; (d) a phase that is skipped or fails cuts NO block, and a phase's block never names a signer outside the phase's parties."
title: "AB: a workflow phase transition is a block signed by the phase's parties over the phase's done commit, its sub-transitions are the blocks it seals, and the run's phase tree equals its block DAG (AA2.66)"
town: core
---
# hypothesis:g716111-ab-a-flow-rotation-run-cuts-one-block-per-phase-transition-signed-by-its-parties-only

## Measured
- doc:radically-simple-engine section AB (landed, trunk 1c0edcf20: AB + AB.5 + AB.6 + the AGI_SEAL_ID cell, byte-equal to self-perpetuating's branch); belam [decision] 03:07Z, owner 02:3xZ 'Is the design finished and looks sound? If so send on'. Terms: SM lands first (met), DG1 writes from the LANDED text, DG2 falsifiers, DG3 builds, SM gates, every root act its own belam GO, AA2.63 is the gate (the 8 KB base).
- section AB 'A workflow phase transition ... The block DAG IS the phase tree, signed.' Layers: DG1+DG2 often; SM+DG1 sealing L3; council+SM sealing L2+3; belam+council the rare top; owner(CA)+belam the anchor block.
- Depends on the FLOW ROTATION phase tree of AA2 (the engine's workflow runner, still being retired into agi-kid by the W phase).

## CLAIM
(a) a FLOW ROTATION run cuts exactly one block per phase transition; (b) each block is signed by that phase's parties only (the level-3 pair for a DG phase, SM plus a DG for a block sealing level 3, and so on up the layers) and holds under ckpt; (c) the block DAG, read from refs/agi/block/*, has the same shape as the run's phase tree: a sub-phase's block is a git parent of the block that seals it; (d) a phase that is skipped or fails cuts NO block, and a phase's block never names a signer outside the phase's parties.

## Dispatch line
config-max: none / template-max: none / code: one block-cut call at each phase transition in the flow runner (agi-kid -m after W-1) using ckpt sign.

## FALSIFIERS
AA2.66: a scripted FLOW ROTATION run with three phases (one with a sub-phase) cuts 3 + 1 blocks, each holds under ckpt, the DAG edges equal the phase tree edges, a failed phase cuts none, and a block signed by a non-party does not hold.
Mutations RED: a block cut per COMMIT instead of per phase (count), the sub-phase block not a parent (DAG shape), a non-party signature accepted (party set).

## TESTS
Shell, the agi-kid-flow.t.sh harness (a scratch invoker repo, stub pi, a manifest of three phases), throwaway keys. No live key, no network, nothing pushed: scratch keys generated at run time in a throwaway dir (no test file, node or commit message holds an armoured block; spell the header with dots). Every ROOT act (a unit edit, the out-line in engine-root, retiring agi-signers, block_push, seal.yml on master) is its own belam GO with before-state and rollback; the build lands the bytes, belam installs them.

## FILE SCOPE
The flow runner (engine-wrap.md agi-kid) call site and one new test file; blocks come from ckpt.

## CEILING
1 parent - kids <= 1 - <= +120 B in agi-kid (the runner is at its 1,856 B ceiling after W-1: the builder says what moves, or the call lives in ckpt) - 1 new test file - 0 USD - regular review. Depends on: the ckpt hypothesis and the W-1 re-cut landing.

## RULINGS (DG1, 10-03 05:0xZ-06:0xZ, from mur verdicts and falsifier runs; the mail they came by is quoted in the cards)
- THE CUT (DG1 05:1xZ): not per phase in the runner; the runner makes ONE call at the END of an agi-kid -m run, `ckpt cut MANIFEST HASH`, which walks the phases the run COMPLETED in tree order and cuts one block per completed phase with that phase's parties (each sub-phase block a git parent of the block that seals it); a failed or pending phase cuts none, a resumed run cuts only the rest, once, a re-run of a finished flow changes no block ref. Runner ceiling in this round 2,130 B HARD (W-1 re-cut 2,100 + the call).
- COLLECTION PATH RULED (self-perpetuating 05:1xZ): MAIL, no agents. The cutter is one of the block's own parties; it fixes the payload (tip time hash digest) and box-mails it to each other party as a [sign] request; each party runs ckpt sign with its OWN key (nested PQ inner included) and mails the blob back as [sig] BLOCK POST; the cutter writes sigs/POST.N and cuts when k is met, verifying each blob through ckpt check first (a bad blob is dropped, never fatal). It stays ON the mail matrix (signers are pairwise level-adjacent, the rule a() uses for who may mail whom); no relay, no cross-uid agent socket. 2 mails per party per block; a party that never answers = the block WAITS, the phase is NOT failed. EXCEPTION (HELD): the anchor block (the owner has no mail row): belam as cutter gets the owner's signature through the armed CA window, not mail.
- ROUND A: DG2's flow-rotation.t.sh 4cd39cc19 (scratch keys in $AGI_BLOCK_KEYS; 1 ok / 14 FAIL on W-1.11 + the doc's ckpt). ROUND B: the mail collection, a new file flow-collect.t.sh (cutter sends one [sign] to each OTHER party, verifies each [sig], a forged blob is dropped, a silent party = no block and no failure, a late [sig] cuts it, a non-party [sig] ignored, anchor never asks the owner by mail). HELD limit on the collection path is DROPPED.
