---
id: hypothesis:g716111-ab-the-out-line-writes-three-ring-lines-per-generation-and-none-on-a-crash-restart
mint_id: 2c2c6c4e24554c0e838334e30c77ad48
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) one `.fresh` writes exactly ONE ring commit (three lines: SIGN ssh-ed25519, PQ pq-sha256 root, SEAL x25519) over the post's own lines, signed by the CURRENT sign key (that commit IS the self-revocation statement), then lands, then `touch ~/.fresh`; a crash restart (no `.fresh`) writes 0 ring commits; (b) a crash BEFORE the land leaves the old line in force, a crash AFTER it leaves a line whose key is lost and the parent re-vouches it (case C7), one recovery rule; (c) the capsule shares are re-wrapped to the next SEAL key at hand-off, the next generation's SEAL opens the re-wrap, the retired generation's SEAL does not open the new one, another post's does not; (d) the retired SIGN key, even PUBLISHED, does not open any wrap (cases S1-S4), because SEAL is a separate key that is deleted at its out-line and never published; (e) the unit line stays within the revised ceiling and writes no ring text itself beyond that one signed commit."
title: "AB: the out-line (the generation shift) commits the post's three new ring lines over its own, signed by the CURRENT sign key, and a crash restart commits none; the SEAL key is its own column, deleted and never published (AA2.56, AA2.68)"
town: core
---
# hypothesis:g716111-ab-the-out-line-writes-three-ring-lines-per-generation-and-none-on-a-crash-restart

## Measured
- doc:radically-simple-engine section AB (landed, trunk 1c0edcf20: AB + AB.5 + AB.6 + the AGI_SEAL_ID cell, byte-equal to self-perpetuating's branch); belam [decision] 03:07Z, owner 02:3xZ 'Is the design finished and looks sound? If so send on'. Terms: SM lands first (met), DG1 writes from the LANDED text, DG2 falsifiers, DG3 builds, SM gates, every root act its own belam GO, AA2.63 is the gate (the 8 KB base).
- AB.5 (c) conflict 1: section AB's folded design wrapped the share to the SIGN key's X25519, so a published sign key opens it (S3: the conflict is real); the separate SEAL column closes it (S1, S2, S4).
- Replaces AA2's ~35 B `.fresh` key drop (the A3.3 build now at SM, guard `[ .fresh -nt .ssh/id_ed25519 ]`) with the revised out-line, ~90 B in engine-root. That A3.3 hypothesis (g716111-aa2-a-key-is-fresh-per-generation-and-the-root-ring-appends-once) stays true for the ONE-BOX half until this lands; this one supersedes its (a) when built.
- Conflict 3 (owner 03:15Z): the proof of concept runs on ROOT-READABLE keys on this box (undoable); the iPhone secure signer is a later round.

## CLAIM
(a) one `.fresh` writes exactly ONE ring commit (three lines: SIGN ssh-ed25519, PQ pq-sha256 root, SEAL x25519) over the post's own lines, signed by the CURRENT sign key (that commit IS the self-revocation statement), then lands, then `touch ~/.fresh`; a crash restart (no `.fresh`) writes 0 ring commits; (b) a crash BEFORE the land leaves the old line in force, a crash AFTER it leaves a line whose key is lost and the parent re-vouches it (case C7), one recovery rule; (c) the capsule shares are re-wrapped to the next SEAL key at hand-off, the next generation's SEAL opens the re-wrap, the retired generation's SEAL does not open the new one, another post's does not; (d) the retired SIGN key, even PUBLISHED, does not open any wrap (cases S1-S4), because SEAL is a separate key that is deleted at its out-line and never published; (e) the unit line stays within the revised ceiling and writes no ring text itself beyond that one signed commit.

## Dispatch line
config-max: none new (the ring columns are ring-node data) / template-max: none / code: the out-line is its OWN piece, `agi-out`, in engine-post.md (expansion: only its map row touches engine.md); the unit's ExecStartPre line only CALLS it and touches `.fresh` (<= 95 B over today's). `agi-out` calls `pq` (keys, inner) and `esc` (wrap) by sect name, commits the three ring lines over the post's own, and NEVER lands them (the post's flush does); the capsule re-wrap uses the existing systemd-creds path. (DG1 ruling 04:1xZ to DG2 and DG3: a ~90 B unit line cannot hold keygen, three ring lines, the commit and the re-wrap by itself.)

## FALSIFIERS
AA2.56: on a scratch post unit, one `.fresh` yields exactly one ring commit holding the three lines, signed by the current key; a crash restart yields none; three restarts yield none; the commit verifies against the ring at the receiving tip.
AA2.56b (C7): a crash after the land and before the key is installed leaves the parent able to re-vouch with one commit, and that commit is admitted.
AA2.68: S1 the SEAL key opens its share, S2 the PUBLISHED retired sign key does NOT, S4 the next generation's SEAL opens the re-wrap and its ring seal column is 32 B raw, X3/X4 the retired SEAL and another post do not.
AA2.56c: the unit's ExecStartPre line <= 95 B over today's; the agi-fresh.t.sh cases still pass for the one-box behaviour (crash keeps the key and appends 0).

## TESTS
Shell, the agi-fresh.t.sh pattern (the REAL unit lines extracted from engine-root.md, a scratch HOME and a scratch repo, a stub systemctl); real ssh-keygen for the sign key; the PQ and SEAL keys from the pq piece and the existing X25519 fold; capsule wraps against a scratch directory. No live key, no network, nothing pushed: scratch keys generated at run time in a throwaway dir (no test file, node or commit message holds an armoured block; spell the header with dots). Every ROOT act (a unit edit, the out-line in engine-root, retiring agi-signers, block_push, seal.yml on master) is its own belam GO with before-state and rollback; the build lands the bytes, belam installs them.

## FILE SCOPE
engine-post.md (the agi-out piece and its map row in engine.md), engine-root.md (the one ExecStartPre line that calls it), the ring node data, one new test file. The root '+' install of the unit is belam's own GO.

## CEILING
1 parent - kids <= 1 - <= +95 B in the post unit line (the revised out-line is ~90 B) - 1 new test file - 0 USD - regular review + security mur on root code.

## RULINGS (DG1, 10-03 05:0xZ-06:0xZ, from mur verdicts and falsifier runs; the mail they came by is quoted in the cards)
- THE PIECE: agi-out in engine-post.md; OUT.2 49a5e9917 (agi-out 2,738 B; engine.md 9,214 B; fenced 7,440 B) with DG2's agi-outline.t.sh de-base-dg2-16 592f186da (37 lanes, hermetic: GIT_CONFIG_GLOBAL and SYSTEM = /dev/null except inside the unit's own steps).
- D1 (mur sm17): the first cut swapped the key AFTER the root agi-signers step, so the g+1 key was missing from allowed_signers; lane d1a (a commit signed by the NEW sign key verifies as post@agi after the ONE start that swapped it, against the box file the unit's own agi-signers step writes) is RED on that cut (36 ok / 1 FAIL) and green on OUT.2 (37 / 0); d1b-d1d keep the old key and the later restarts. The unit steps run in FILE ORDER; a post whose worktree holds NO ring node keeps today's behaviour; agi-fresh.t.sh's CEIL is 840 (745 + the 95 B call) and the unit's sh -c lines stay <= 790 B.
- Lands AFTER the ring (RING.4).
