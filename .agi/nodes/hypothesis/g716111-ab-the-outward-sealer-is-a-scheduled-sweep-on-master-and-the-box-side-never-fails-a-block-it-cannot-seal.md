---
id: hypothesis:g716111-ab-the-outward-sealer-is-a-scheduled-sweep-on-master-and-the-box-side-never-fails-a-block-it-cannot-seal
mint_id: c69c75aec990420ba8b75f89a9a7ebd5
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) AGI_SUBJECT is ONE cell read by both sides: sha256 over the sorted 'sha256(file) path' lines of a block's tree (tip, time, hash, every signature), no tar, so it does not depend on tar.umask (cases G6/G7) nor on the repo's sha1 object ids; the box's gate fact and seal.yml carry the same line, byte-equal; (b) the whole-block subject binds WHICH quorum (G2), where the signed payload's digest does not (G1); (c) block_push is `for i in 1 2 4 8;do git push -q origin 'refs/agi/block/*:refs/agi/block/*'&&break;sleep $((i*60));done;:` and always exits 0: with origin unreachable the block still HOLDS on the box and reads 'unsealed externally'; (d) refs/revoked is not under the pushed pattern; 'block' is a reserved town name; (e) the identity is ONE literal cell AGI_SEAL_ID = https://github.com/OWNER/REPO/.github/workflows/seal.yml@refs/heads/master, written once, never derived from `git remote get-url origin` (that URL ends in .git); (f) `.github/*` on the trunk is ruled by the rules cell (W1 refused for a DG, W2 admitted for the owner)."
title: "AB.6: the outward sealer is GitHub Actions - a scheduled sweep on master attests each block's whole-block digest (AGI_SUBJECT) - and the box side (block_push with backoff) exits 0 so an unreachable origin leaves a block UNSEALED-EXTERNALLY, never failed (AA2.74, AA2.77, AA2.79; the outward ones HELD)"
town: core
---
# hypothesis:g716111-ab-the-outward-sealer-is-a-scheduled-sweep-on-master-and-the-box-side-never-fails-a-block-it-cannot-seal

## Measured
- doc:radically-simple-engine section AB (landed, trunk 1c0edcf20: AB + AB.5 + AB.6 + the AGI_SEAL_ID cell, byte-equal to self-perpetuating's branch); belam [decision] 03:07Z, owner 02:3xZ 'Is the design finished and looks sound? If so send on'. Terms: SM lands first (met), DG1 writes from the LANDED text, DG2 falsifiers, DG3 builds, SM gates, every root act its own belam GO, AA2.63 is the gate (the 8 KB base).
- AB.6 (owner 03:25Z): the external anchor is a scheduled sweep on master (the default branch; GitHub runs schedule and dispatch only from it), 0 bytes on the trunk; seal.yml is 1,489 B (sha256 686368aa896cb1e8) and lives on master, whose writer is belam's call.
- NOT run and not buildable without belam's GO (outward): the workflow on GitHub, an attestation, `gh attestation verify`, the push of block refs to origin.

## CLAIM
(a) AGI_SUBJECT is ONE cell read by both sides: sha256 over the sorted 'sha256(file) path' lines of a block's tree (tip, time, hash, every signature), no tar, so it does not depend on tar.umask (cases G6/G7) nor on the repo's sha1 object ids; the box's gate fact and seal.yml carry the same line, byte-equal; (b) the whole-block subject binds WHICH quorum (G2), where the signed payload's digest does not (G1); (c) block_push is `for i in 1 2 4 8;do git push -q origin 'refs/agi/block/*:refs/agi/block/*'&&break;sleep $((i*60));done;:` and always exits 0: with origin unreachable the block still HOLDS on the box and reads 'unsealed externally'; (d) refs/revoked is not under the pushed pattern; 'block' is a reserved town name; (e) the identity is ONE literal cell AGI_SEAL_ID = https://github.com/OWNER/REPO/.github/workflows/seal.yml@refs/heads/master, written once, never derived from `git remote get-url origin` (that URL ends in .git); (f) `.github/*` on the trunk is ruled by the rules cell (W1 refused for a DG, W2 admitted for the owner).

## Dispatch line
config-max: AGI_SUBJECT, AGI_SEAL_ID (cells), the allowed-paths row for .github/* (the rules cell; belam at landing) / template-max: none / code: block_push as a crons.md job cell (belam's GO to enable), the AGI_SUBJECT line in the gate fact, seal.yml as a FILE for master (not committed to the trunk).

## FALSIFIERS
AA2.74: G1-G5 PASS scratch (council); DG2 re-runs G6/G7 only: the AGI_SUBJECT recipe under three tar.umask values and in a fresh clone gives ONE digest, 9/9 blocks distinct.
AA2.77: with origin unreachable (a bad URL), block_push exits 0 within its backoff bound (the test shortens the sleeps by a cell), the block still holds under ckpt and the status line reads unsealed externally.
AA2.79 (box side): the AGI_SUBJECT line in seal.yml and in the gate fact are byte-equal (cmp).
AA2.80: W1/W2 through agi-land is all-is-one's lane.
Workflow file: seal.yml parses (pyyaml), triggers are schedule and workflow_dispatch only, permissions are contents read, id-token write, attestations write.

## TESTS
Shell, scratch repos and a bad-URL origin; no network, nothing pushed; pyyaml for the parse. No live key, no network, nothing pushed: scratch keys generated at run time in a throwaway dir (no test file, node or commit message holds an armoured block; spell the header with dots). Every ROOT act (a unit edit, the out-line in engine-root, retiring agi-signers, block_push, seal.yml on master) is its own belam GO with before-state and rollback; the build lands the bytes, belam installs them.

## FILE SCOPE
engine*.md (the AGI_SUBJECT fact, AGI_SEAL_ID cell), crons.md (the block_push job, disabled until belam's GO), seal.yml delivered as a file under the graph for belam to place on master, one new test file.

## HELD (named, not built)
AA2.75 (a block pushed at t is attested within two sweep intervals and `gh attestation verify` on its rebuilt listing passes for an outside reader), AA2.76 (a second sweep creates 0 attestations) and AA2.78 (`git ls-remote origin` lists refs/agi/block/* and NO refs/revoked): UNRUN, OUTWARD, each needs belam's GO for block_push, seal.yml on master and the first push. Limits 12-14: the schedule is best-effort; the anchor is GitHub plus Sigstore, trustless of the sanctuary, not of them.

## CEILING
1 parent - kids <= 1 - block_push about 110 B - seal.yml 1,489 B (a file, not a piece) - 1 new test file - 0 USD - regular review.
