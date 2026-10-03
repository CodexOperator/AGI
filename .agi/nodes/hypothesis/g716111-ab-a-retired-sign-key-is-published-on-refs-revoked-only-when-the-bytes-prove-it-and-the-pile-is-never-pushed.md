---
id: hypothesis:g716111-ab-a-retired-sign-key-is-published-on-refs-revoked-only-when-the-bytes-prove-it-and-the-pile-is-never-pushed
mint_id: b695727fa215422592bb2b3dbbd8648f
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) cases R1-R7: DG1's gen1 key published after the level-3 block sealed its hand-off HOLDS ('revoked <post> <fp> closed <c> sealed'); a LIVE key, a key that was never the post's, and the post's retired key under ANOTHER post's name are refused; alive's gen1 handed off with NO block sealing it (grace) is refused and holds after a level-2 block seals it; a commit signed with a published key at any date is refused by the ring rule (T5); a passphrase-ENCRYPTED key on the pile is refused at once with no prompt and no hang (`ssh-keygen -y -P ''` against no tty); (b) `git ls-remote origin | grep -c refs/revoked` is 0 after a day of publications, because refs/revoked is under no pushed pattern (branch_push, grid_sync, the town mirror's refs/agi/<town>/*); (c) the trunk keeps refusing ANY private key block (the key-gate hypothesis), so a publication lives only on refs/revoked; (d) published keys stay OFF every remote until the owner names the outward act (belam [decision] 03:2xZ)."
title: "AB.5: revoke - a retired SIGN key may sit on refs/revoked only if its public half was the post's CLOSED ring line, the commit that closed it was signed by that same key, and a holding block seals that commit; the pile is pushed by no job (AA2.69, AA2.72)"
town: core
---
# hypothesis:g716111-ab-a-retired-sign-key-is-published-on-refs-revoked-only-when-the-bytes-prove-it-and-the-pile-is-never-pushed

## Measured
- doc:radically-simple-engine section AB (landed, trunk 1c0edcf20: AB + AB.5 + AB.6 + the AGI_SEAL_ID cell, byte-equal to self-perpetuating's branch); belam [decision] 03:07Z, owner 02:3xZ 'Is the design finished and looks sound? If so send on'. Terms: SM lands first (met), DG1 writes from the LANDED text, DG2 falsifiers, DG3 builds, SM gates, every root act its own belam GO, AA2.63 is the gate (the 8 KB base).
- revoke whole is 1,390 B as the prototype (sha256 32c9d51d3295ff1b); the LANDED piece is 1,588 B (e1301b5f, trunk 558e77664), which verifies against the ring at the closing commit's PARENT; it derives the public half with -P '' because a bare `ssh-keygen -y` prompts on an encrypted key and would stall a land (alive, R7).
- Origin is PUBLIC-READABLE (alive 03:1xZ, read-only GitHub API) and a landed v5 commit reads verified:false, reason no_user on GitHub: the rule for plain-git readers is 'only ring-gate's verdict counts' (the council places it in section AB and the agi-verify skill, one place each).

## CLAIM
(a) cases R1-R7: DG1's gen1 key published after the level-3 block sealed its hand-off HOLDS ('revoked <post> <fp> closed <c> sealed'); a LIVE key, a key that was never the post's, and the post's retired key under ANOTHER post's name are refused; alive's gen1 handed off with NO block sealing it (grace) is refused and holds after a level-2 block seals it; a commit signed with a published key at any date is refused by the ring rule (T5); a passphrase-ENCRYPTED key on the pile is refused at once with no prompt and no hang (`ssh-keygen -y -P ''` against no tty); (b) `git ls-remote origin | grep -c refs/revoked` is 0 after a day of publications, because refs/revoked is under no pushed pattern (branch_push, grid_sync, the town mirror's refs/agi/<town>/*); (c) the trunk keeps refusing ANY private key block (the key-gate hypothesis), so a publication lives only on refs/revoked; (d) published keys stay OFF every remote until the owner names the outward act (belam [decision] 03:2xZ).

## Dispatch line
config-max: none / template-max: none / code: the revoke piece (a new engine PIECE), its map line, and the successor's publish step in the out-line (commit the old SIGN key to refs/revoked when the lowest block seals the hand-off, then delete it from the capsule).

## FALSIFIERS
AA2.69: R1-R7 in a shell test with a throwaway CA, post keys and blocks; R7 under `timeout 20` (a hang is the failure).
AA2.72: a scratch origin (a bare repo) after a simulated day of publications and every cron job's push pattern replayed: `git ls-remote` of it lists 0 refs/revoked (read-only check, nothing outward).
Mutations RED: the closing-commit-signer check dropped (R2/R3 RED), the seal check dropped (R4 RED), the post-name check dropped (R3b RED), -P '' dropped (R7 hangs, caught by the timeout).

## TESTS
Shell, scratch repos and a scratch bare origin only; no key leaves the scratch dir. No live key, no network, nothing pushed: scratch keys generated at run time in a throwaway dir (no test file, node or commit message holds an armoured block; spell the header with dots). Every ROOT act (a unit edit, the out-line in engine-root, retiring agi-signers, block_push, seal.yml on master) is its own belam GO with before-state and rollback; the build lands the bytes, belam installs them.

## FILE SCOPE
The revoke piece, its map line, the out-line's publish step, one new test file.

## CEILING
1 parent - kids <= 1 - revoke <= 1,588 B whole (the landed piece; the prototype was 1,390 B), about +58 B on the base map - 1 new test file - 0 USD - regular review + security mur on root code. Depends on: the ckpt hypothesis and the out-line hypothesis.

## RULINGS (DG1, 10-03 05:0xZ-06:0xZ, from mur verdicts and falsifier runs; the mail they came by is quoted in the cards)
- MUTATION LINE CORRECTED (DG2, measured): dropping the signer check of the closing commit goes RED only on R8 (a line closed by SM's RE-VOUCH, not signed by the key, is refused although a block seals it); R2 and R3 are refused earlier by the CLOSED-line test, so they do not isolate that check.
- The LANDED piece is 1,588 B (e1301b5f); DG2's falsifier revoke.t.sh e6092b9aa runs 18 lanes (R1-R11b + AA2.72), 18 ok / 0 FAIL on the landed text + the doc's ckpt + the ring build. Git itself keeps a one-level refs/revoked off a stock remote, but the lanes pin the PUSH PATTERNS, not git.
