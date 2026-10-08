---
id: hypothesis:g716111-aa2-a-key-is-fresh-per-generation-and-the-root-ring-appends-once
mint_id: 86cf986d7ab44cf783ec4656f4faed95
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: a32c37d35930e0ba
season: 2
testable_claim: "(a) a crash restart (no `.fresh`) keeps the key and appends 0 ring lines; an out-line (`.fresh`) drops the key before keygen and root appends exactly 1 line `<post>@agi namespaces='git' valid-after=<now> <pubkey>`, stamping valid-before on the previous line; (b) a commit by generation g's key dated after g+1's start fails `git verify-commit`; (c) the principal form is `<post>@agi` everywhere (unit committer email, ring, signers), so verify-commit no longer says No principal matched."
title: "AA2: the signing key is fresh per GENERATION, root's allowed-signers ring appends exactly one line per generation (none on a crash restart), and a commit dated after generation g+1 starts fails verify under g's key"
town: core
---
# hypothesis:g716111-aa2-a-key-is-fresh-per-generation-and-the-root-ring-appends-once

## Measured
- doc:radically-simple-engine §AA2 'Keys': engine-root:33 makes the key ONCE (`[ -f .ssh/id_ed25519 ]||ssh-keygen`) and Restart=always (:38) resumes the same session after a crash (DG5 restarted 15 times on 10-01), so a generation is `.fresh`, not a unit start.
- doc:rse-aa3-land AA3.4(1): `verify-commit` says No principal matched on EVERY v5 commit today (HEAD of posts/all-is-one: signed, unverifiable; `<post>@agi` reads Good); the trunk's signers = 3 keys (director-thought-1, director-thought-2, thought-master-new).
- Owner answer on keys (AA1): no requests; root mints the post's capped key at unit start into a root-written EnvironmentFile; mail never carries a secret.
- RELEASED 10-03 for the ONE-BOX half (belam gen 27 [decision] 02:3xZ; owner 02:3xZ: "if [finished and sound] send on"): the 21:3xZ hold no longer covers claims (a), (b) and (c) on one box: `~/.fresh` drops `.ssh/id_ed25519*` before keygen; a crash restart appends 0 ring lines; the ring append and the valid-before stamp are agi-signers, INSTALLED at host act A2 (belam ran A1 A2 A4 A5). Route: DG2 falsifier -> DG3 build -> SM gate; the unit edit is its own root GO (belam).
- NOT released, back to the council for another pass (owner verbatim sent to alive): the CROSS-BOX half: ring travel between boxes, the anchor signer, X11a/b, the [config] ring. Nothing here covers them.
- Claim (c), the principal form `<post>@agi`, is met by agi-signers + A3 (goal:g7.16.1.11.11.1.1 retires the `signers` piece), NOT by an edit of that piece: skipped by the council's ruling (alive 22:1xZ via SM 22:4xZ).

## CLAIM
(a) a crash restart (no `.fresh`) keeps the key and appends 0 ring lines; an out-line (`.fresh`) drops the key before keygen and root appends exactly 1 line `<post>@agi namespaces="git" valid-after=<now> <pubkey>`, stamping valid-before on the previous line; (b) a commit by generation g's key dated after g+1's start fails `git verify-commit`; (c) the principal form is `<post>@agi` everywhere (unit committer email, ring, signers), so verify-commit no longer says No principal matched.

## BUILT AND PINNED (DG1 10-08 17:4xZ, found by DG4's audit; corrects 'NOT dispatched' below)
The ONE-BOX half is on the trunk (8aaf41d5d1): engine-root.md:35 ExecStartPre #1 = `[ .fresh -nt .ssh/id_ed25519 -a ! -f t/.agi/nodes/.geometry/ring ]&&rm -f .ssh/id_ed25519*;[ -f .ssh/id_ed25519 ]||ssh-keygen ...` (the `.fresh -nt` test is the retry-idempotence guard, the `! -f ring` clause is AB(2) 00ffbe04cc) and agi-signers writes the ring line. extensions/agi/tests/agi-fresh.t.sh (23 ok, 0 FAIL, env -i, the REAL unit line extracted) pins claims (a) crash keeps the key and appends 0 ring lines, out-line = a new key + exactly 1 ring line + valid-before stamped, retry x2 = 1 line, and (b) generation g's key dated after g+1 fails verify-commit; (c) the principal form is `<post>@agi`. DG4's mutation audit (9 mutants of the REAL pieces: drop after keygen, on a crash, pub key only, whenever .fresh, ring append twice, no idempotence guard, no valid-before, no valid-after, principal form) killed 9/9; five survivors (the `! -f ring` clause, `rm -rf .ssh/*`, ring chmod 666, the one-line pubkey check, the key-pattern check) get lane rows (test-only). No build remains for the one-box half; the cross-box half stays with the council.

## Dispatch line
config-max: none new (the ring path is the unit's) / template-max: none / code: ~35 B in the post's ExecStartPre (drop `.ssh/id_ed25519*` when ~/.fresh exists); the ring append is agi-signers (built, installed A2), unchanged. Build lane: DG3 after DG2's falsifier; NOT dispatched until handed. The unit edit's install = its own belam GO (command, before-state, one-command rollback).

## FALSIFIERS
AA2.7 a commit by generation g's key dated after g+1's start fails verify-commit · AA2.8 a crash restart keeps the key and appends 0 ring lines; an out-line appends exactly 1 · every v4 commit verifies as `<post>@agi` (git log --show-signature count of 'No principal matched' = 0).

## TESTS
scratch ring tests (OpenSSH 9.6 allowed_signers valid-after/valid-before); a unit-file test for the ExecStartPre line; no live key is touched.

## FILE SCOPE
engine-root (the unit's ExecStartPre) · agi-signers is the ring writer (unchanged) · the principal form is A3's (the `signers` piece retires, never edited here). One-box half only; the cross-box half stays with the council. No live key is touched by the build or its tests.

## CEILING
1 parent · kids <= 1 · +35 B in the post unit · one-box half released 10-03 (belam 02:3xZ; owner 02:3xZ) · regular review.
