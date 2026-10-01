---
id: doc:g716111-capsule-build
mint_id: ce7c1b733a984160bdc7ee2d09cedb00
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-3
scaffold_hash: 98861062cd223672
season: 2
tags:
  - doc
  - capsule
  - g7.16.1.11
title: "g7.16.1.11 CAPSULE build phase A: capsule-pop (O.2 + a +136 B patch) / capsule-login (O.5 + P11) / pre-receive delta / interim custody / pqwrap, dry-tested, 10 root acts listed (none run)"
town: core
---
# doc:g716111-capsule-build

The CAPSULE build, PHASE A (goal:g7.16.1.11; owner BUILD GO 05:45Z + custody O.8 released by belam 06:01Z; source design doc:radically-simple-engine §O/§P @1daf2888a). Built by an Opus 5.5 subagent of director-general-3, NO root, nothing installed, nothing run against a live key/ref/hook; dry tests re-run by DG3 (rc 0, 89 case lines, same results). The pieces below are byte-exact (sha256 in pieces.sha256 order); off-graph copy /tmp/agi-capsule/. ROOT ACTS: 10 listed in the plan, NONE run -- R1-R9 on belam's word, R10 (seal the owner's real plain key) on the OWNER's go.

## Council picks banked (DG3 recommends the first option of each)
- **O.2 capsule-pop: patched (+136 B) vs byte-exact.** The byte-exact O.2 (1,194 B) has three holes the dry test reproduces: H1 T given as a ref NAME pops twice (replay); H2 a failing commit-tree runs L while the tip never moves (replayable); H3 R.L swapped mid-pop runs an UNSIGNED launch cell with the credential. capsule-pop.patched (1,330 B) refuses H1 and H2 and runs only the signed cell on H3. Recommend: patched.
- **O.5 capsule-login: the doc version, given a symlinked pane, wipes the ledger and leaves the login code IN it.** The built capsule-login (932 B) requires the pane to be a FIFO owned by the ask's creator and writes the ledger line only after the code is typed (L1-L10).
- **Interim custody ring:** capsule ok holds the posts at weight 1, k = ALL posts, owner NOT in the ring (a lost phone stays recoverable); the price: all posts together can recover the owner's plain key, but only into a destination they all sign, and the ledger names them.
- **§P.6 finding:** 'the kernel alone guards refs/capsule' does not hold -- git pack-refs moves refs into the single packed-refs file.

## Engine byte delta (config:engine is v4c 16,384 B, cap 20,480 while needed): re-add pre-receive +568 -> 16,952 · capsule delta +480 -> 17,432 · agi-post@ pane-group line +75 -> 17,507 (2,973 B under the cap). Not applied: an engine edit is a Prime landing (N2).

## Custody seam (named, NOT built): I1 the app's Secure Enclave key emitting SSH signatures · I2 the iMessage extension sharing that keychain · the device-side 2-of-2 inner seal (se-wrap) · how a recovered key reaches a new phone.

## Dry-test results (DG3 re-run 06:3xZ)
~~~~~text
== test forms vs pieces/ (lines differing): capsule-pop 1 (systemd-run --user, LoadCredential plain, no DynamicUser) · capsule-pop.patched 1 (same) · capsule-seal 1 (cat for systemd-creds encrypt: the test cred is PLAIN) · pre-receive 1 (group name) · capsule-ok 0 · capsule-login 0
== capsule-seal (test form) -- create-only, secret on stdin
S1 seal c1 (plain 2-of-3)                        | ok, files: cred k ring/p1 ring/p2 ring/p3 
S1 seal pc (POSTS' capsule: owner@4, posts @1, k=6) | ok, ring: owner@4 p1 p2 p3 
S1 seal oc (OWNER's capsule: all @1, k=4)          | ok
S1 seal ok (INTERIM CUSTODY: the owner's plain key, posts @1, k=3) | ok, cred = 387 B
S2 a second seal of c1                              | rc=128 (create-only: the first tip stands)
S3 a holder with no key at HEAD                     | rc=128
S4 k = 0                                            | rc=1
S5 a malformed weight p1@2@3                        | rc=2 · refs/capsule/c9 exists: no
== capsule-pop: pieces/capsule-pop = doc O.2 BYTE-EXACT (1,194 B, cmp-identical to doc:radically-simple-engine @1daf2888a and @HEAD)
T1 plain 2-of-3: 1 signer                           | rc=1 | tip 3d73c7a -> 3d73c7a | L ran 0x
T2 one holder signing twice                         | rc=1 | tip 3d73c7a -> 3d73c7a | L ran 0x
T3 a holder + an outsider                           | rc=1 | tip 3d73c7a -> 3d73c7a | L ran 0x
T4 2 signers, then R.L swapped (H mismatch)         | rc=1 | tip 3d73c7a -> 3d73c7a | L ran 0x
T4b 2 signers, then T in R edited                   | rc=2 | tip 3d73c7a -> 3d73c7a | L ran 0x
T5 plain 2-of-3: 2 distinct signers                 | rc=0 | tip 3d73c7a -> 27efa4a | L ran 1x, read 19 B
T6 replay: the same R + signatures                  | rc=128 | tip 27efa4a -> 27efa4a | L ran 0x
Q1 posts' capsule: all 3 posts, no owner (3<6)      | rc=1 | tip a1a4ef5 -> a1a4ef5 | L ran 0x
Q2 posts' capsule: owner + 1 post (5<6)             | rc=1 | tip a1a4ef5 -> a1a4ef5 | L ran 0x
Q4 posts': p1+p2, worktree ring p1@9 and k=1        | rc=1 | tip a1a4ef5 -> a1a4ef5 | L ran 0x
Q3 posts' capsule: owner + 2 posts (6>=6)           | rc=0 | tip a1a4ef5 -> 367ecc5 | L ran 1x, read 19 B
Q5 owner's capsule: owner + 2 posts (3<4)           | rc=1 | tip 0f7b032 -> 0f7b032 | L ran 0x
Q6 owner's capsule: owner + all 3 posts             | rc=0 | tip 0f7b032 -> 5466fb7 | L ran 1x, read 19 B
== capsule-pop: pieces/capsule-pop.patched (O.2 + the 3-part patch, +136 B)
T1 plain 2-of-3: 1 signer                           | rc=1 | tip 3d73c7a -> 3d73c7a | L ran 0x
T2 one holder signing twice                         | rc=1 | tip 3d73c7a -> 3d73c7a | L ran 0x
T3 a holder + an outsider                           | rc=1 | tip 3d73c7a -> 3d73c7a | L ran 0x
T4 2 signers, then R.L swapped (H mismatch)         | rc=1 | tip 3d73c7a -> 3d73c7a | L ran 0x
T4b 2 signers, then T in R edited                   | rc=2 | tip 3d73c7a -> 3d73c7a | L ran 0x
T5 plain 2-of-3: 2 distinct signers                 | rc=0 | tip 3d73c7a -> 0ced077 | L ran 1x, read 19 B
T6 replay: the same R + signatures                  | rc=128 | tip 0ced077 -> 0ced077 | L ran 0x
Q1 posts' capsule: all 3 posts, no owner (3<6)      | rc=1 | tip a1a4ef5 -> a1a4ef5 | L ran 0x
Q2 posts' capsule: owner + 1 post (5<6)             | rc=1 | tip a1a4ef5 -> a1a4ef5 | L ran 0x
Q4 posts': p1+p2, worktree ring p1@9 and k=1        | rc=1 | tip a1a4ef5 -> a1a4ef5 | L ran 0x
Q3 posts' capsule: owner + 2 posts (6>=6)           | rc=0 | tip a1a4ef5 -> 685f1f2 | L ran 1x, read 19 B
Q5 owner's capsule: owner + 2 posts (3<4)           | rc=1 | tip 0f7b032 -> 0f7b032 | L ran 0x
Q6 owner's capsule: owner + all 3 posts             | rc=0 | tip 0f7b032 -> bf13f73 | L ran 1x, read 19 B
== the holes in O.2 as written, and the patch
H1 capsule-pop         T = a ref NAME, 2 signers   | rc=0 | tip 3d73c7a -> d2d6a56 | L ran 1x, read 19 B
H1 capsule-pop         the SAME R + sigs again      | rc=0 | tip d2d6a56 -> f926ad4 | L ran 1x, read 19 B
H2 capsule-pop         commit-tree fails (no identity) | rc=0 | tip f926ad4 -> f926ad4 | L ran 1x, read 19 B
H2 capsule-pop         the SAME R + sigs again      | rc=0 | tip f926ad4 -> f926ad4 | L ran 1x, read 19 B
H3 capsule-pop         R.L swapped mid-pop (race)   | rc=0 | tip f926ad4 -> acb3ab3 | L ran 1x, read SWAPPED-unsigned-cell-read-19 B
H1 capsule-pop.patched T = a ref NAME, 2 signers   | rc=1 | tip acb3ab3 -> acb3ab3 | L ran 0x
H1 capsule-pop.patched the SAME R + sigs again      | rc=1 | tip acb3ab3 -> acb3ab3 | L ran 0x
H2 capsule-pop.patched commit-tree fails (no identity) | rc=128 | tip acb3ab3 -> acb3ab3 | L ran 0x
H2 capsule-pop.patched the SAME R + sigs again      | rc=128 | tip acb3ab3 -> acb3ab3 | L ran 0x
H3 capsule-pop.patched R.L swapped mid-pop (race)   | rc=0 | tip acb3ab3 -> ff52f3c | L ran 1x, read 19 B
   out (the destinations' own log): 1 line(s) written by an UNSIGNED run cell
== interim custody: the owner's plain key in capsule 'ok' (ring p1 p2 p3, k=3); the recovery destination signs a posts'-capsule ask with it
K1 the owner's own signature (not in this ring)      | rc=1 | tip 6f68186 -> 6f68186 | L ran 0x
K2 two of three posts (2<3)                         | rc=1 | tip 6f68186 -> 6f68186 | L ran 0x
K3 all three posts: the recovery pop                | rc=0 | tip 6f68186 -> f4c8136 | L ran 1x, read 387 B
   the destination held the owner's exact key: yes
K4 posts' capsule: RECOVERED owner sig + 2 posts    | rc=0 | tip a1a4ef5 -> 97a6e3b | L ran 1x, read 19 B
== pre-receive = engine piece (last carried @50eda68b1, 435 B) + the capsule delta; bare origin, refs/capsule/* seeded before the hook
B0 a ledger commit of O.2 AS WRITTEN (no signatures in it) | rc=1 | remote: capsule: refs/capsule/c1 declined 
B1 a patched pop's ledger commit (2-of-3)            | rc=0 | 3d73c7a..8b5fd7a 
B6 replay: the same R + sigs re-committed on T       | rc=1 | remote: capsule: refs/capsule/c1 declined 
B2 forged: right shape, 1 signature                  | rc=1 | remote: capsule: refs/capsule/c1 declined 
B3 2 valid signatures, the TREE changed              | rc=1 | remote: capsule: refs/capsule/c1 declined 
B3b 2 valid signatures, two parents                  | rc=1 | remote: capsule: refs/capsule/c1 declined 
B3c 2 valid signatures over an R naming another T    | rc=1 | remote: capsule: refs/capsule/c1 declined 
B10 posts' capsule: 3 posts, no owner (3<6)          | rc=1 | remote: capsule: refs/capsule/pc declined 
B11 posts' capsule: owner + 2 posts                  | rc=0 | a1a4ef5..a56b01e 
B4 delete refs/capsule/c1                            | rc=1 | remote: capsule: refs/capsule/c1 declined 
B5 create refs/capsule/c2 (a seal by push)           | rc=1 | remote: capsule: refs/capsule/c2 declined 
B7 pieces/pre-receive AS SHIPPED (group agi-capsule) | rc=1 | remote: capsule: refs/capsule/c1 declined 
B8 base path unchanged: a branch the pusher owns     | rc=0 | [new branch] 
B9 base path unchanged: a path of another group      | rc=1 | declined 
== capsule-login (pieces/, unmodified) as an authorized_keys forced command of a scratch sshd (own user, 127.0.0.1 only, throwaway host key; the owner key = the iPhone's plain key)
L1 owner key, open ask, code#state          | rc=0 | pane +18 B | stderr 0 B | ledger 1 lines
   pane got exactly code+CR: yes · ledger fields: login post id time 4 fields
L2 any other key, open ask                  | rc=255 | pane +0 B | stderr 0 B | ledger 1 lines
L3 the used id again                        | rc=3 | pane +0 B | stderr 0 B | ledger 1 lines
L3' an unknown id                           | rc=3 | pane +0 B | stderr 0 B | ledger 1 lines
L4 a shell (no command)                     | rc=2 | pane +0 B | stderr 0 B | ledger 1 lines
L4' another command (ls;id)                 | rc=2 | pane +0 B | stderr 0 B | ledger 1 lines
L5 path traversal id ../../x                | rc=2 | pane +0 B | stderr 0 B | ledger 1 lines
L6 P11 pin: SP     line                  | rc=4 | pane +0 B | stderr 0 B | ledger 1 lines
L6 P11 pin: QT     line                  | rc=4 | pane +0 B | stderr 0 B | ledger 1 lines
L6 P11 pin: ESC    line                  | rc=4 | pane +0 B | stderr 0 B | ledger 1 lines
L6 P11 pin: 513    line                  | rc=4 | pane +0 B | stderr 0 B | ledger 1 lines
L6 P11 pin: EMPTY  line                  | rc=4 | pane +0 B | stderr 0 B | ledger 1 lines
L6' P11 pin: exactly 512 chars             | rc=0 | pane +513 B | stderr 0 B | ledger 2 lines
L7 pane i = a symlink (to the ledger)       | rc=5 | pane +0 B | stderr 0 B | ledger 2 lines
   ledger unchanged: yes
L7' pane i = a regular file                | rc=5 | pane +0 B | stderr 0 B | ledger 2 lines
   file still empty: yes
L8 two logins of ONE ask at once            | rc=0,3 | pane +18 B | ledger 3 lines
L9 the code at rest: spool + ledger + sshd log: 0 files
L10 the pane not reading (named limit)     | rc=124 (124 = the client blocked on the FIFO until timeout) | ask spent: yes
   scratch sshd stopped: yes · reader stopped: yes
== the doc's O.5 capsule-login (692 B, byte-exact) vs pieces/capsule-login, the pane i swapped for a symlink to the ledger (run directly, no sshd)
L7 capsule-login.O5  | rc=0 | ledger's first line kept: 0 · the code at rest in the ledger: 1
L7 capsule-login     | rc=5 | ledger's first line kept: 1 · the code at rest in the ledger: 0
== pqwrap (V-L1 as a piece: hybrid X25519 + ML-KEM-768 share wrap, node v24.21.0, bundled OpenSSL 3.5.8)
V0 keygen: x.pub 113 B  k.pub 1686 B  · key modes: 600 600 
V1 wrap 32 B to holder a | envelope 1180 B (32+1088+12+16+32) | share bytes inside it: False
V2 open with a's two keys            | rc=0 | byte-exact: yes
V3 open with b's keys               | rc=1
V4 a's X25519 + b's ML-KEM (F30)    | rc=1
V5 b's X25519 + a's ML-KEM (F30)    | rc=1
V6 one byte changed @5              | rc=1
V6 one byte changed @600            | rc=1
V6 one byte changed @1125           | rc=1
V6 one byte changed @1140           | rc=1
V6 one byte changed @1160           | rc=1
~~~~~

## PLAN (root acts one by one, each command · UNDO · PROOF; teardown T1-T8)

Built unprivileged by an Opus 5.5 subagent of DG3, 06:0x-06:2xZ 10-01, under the owner's GO of 05:45Z and the custody scope added at 06:01Z.
Inputs: `pieces/` (below), `test.txt` (the dry run, pasted from `dry-test.sh`). No key, ref, hook, authorized_keys or graph node was touched.

### Pieces (bytes on disk)
| piece | B | job |
|---|---|---|
| capsule-pop | 1194 | doc O.2, BYTE-EXACT (cmp-identical @1daf2888a and @HEAD): weighted k-of-n, one CAS, L runs with C as its only credential |
| capsule-pop.patched | 1330 | O.2 + a 3-part patch (+136 B, `capsule-pop.diff`): T must be 40 hex · inputs copied before use · commit-tree output assigned first, and the signatures go into the ledger |
| capsule-ok | 836 | the O.2 weighted check as one call (ring, weights and k read FROM T; k >= 1). The pre-receive uses it |
| capsule-seal | 1074 | O.1 SEAL (root): secret on stdin -> systemd-creds -> one commit = HEAD tree + .agi/capsule/C/{cred,k,ring/<h>[@w]} -> refs/capsule/C, create-only |
| capsule-login | 932 | O.5 + P11 (692 -> 932 B): the pane must be a FIFO, not a symlink, owned by the ask's creator; the ledger line is written only after the code is typed |
| pre-receive | 915 | the engine piece as last carried (@50eda68b1, 435 B) + `capsule.pre-receive.delta` (480 B) |
| capsule-pop.path / .service | 70 / 345 | O.2's "unbuilt, named" trigger: the sticky spool /var/spool/agi/pop, one `<C>.R` per capsule; a refused pop leaves R waiting for more signatures |
| capsule.sysusers · authorized_keys.shape | 65 · 132 | the agi-capsule user · `restrict,command="/opt/agi/capsule/capsule-login" <owner device key>` |
| pqwrap | 2101 | V-L1 as a piece (P.7 escrow share wrap): X25519 + ML-KEM-768 hybrid with HKDF-SHA256 and ChaCha20-Poly1305, node:crypto only |

### Why a patch to O.2 (each one is shown failing on O.2 as written in test.txt H1-H3, and passing on the patched piece)
- **H1 · replay through a ref name.** `git update-ref NEW OLD` resolves OLD as a revision, so with T = `refs/capsule/C` the CAS always matches. k signatures over "C H refs/capsule/C" popped TWICE.
- **H2 · CAS skipped when commit-tree fails** (for example, no git identity in the unit). `$(...)` is empty, so `update-ref ref T` sets the ref to its own value with no CAS, and L runs. The same R popped twice with the tip unmoved.
- **H3 · TOCTOU in a shared spool.** O.2 reads R and R.L again after the hash and signature checks, so swapping R.L during a pop (150 junk .sig files widen the window) ran an UNSIGNED run cell with the credential. The patch copies R, R.L and R.sig.* into its private temp first.
- **For the pre-receive:** the ledger commit must carry the signatures, or a receiving repo cannot re-check a pop (B0: an O.2 ledger commit is refused).

### Engine delta (config:engine = 16,384 B now; cap 20,480 B while needed)
The live engine (v4c, e1e0dbaaf) carries NO pre-receive piece; the last version that did was 50eda68b1 (435 B).
| change | +B | engine |
|---|---|---|
| re-add `### pre-receive` (the 435 B piece + its table row) | +568 | 16,952 |
| + the capsule delta inside it (480 B: one `case $r in refs/capsule/*)` branch at the top of the loop, so a delete or create of a capsule ref never reaches the base's delete-skip) | +480 | 17,432 |
| + agi-post@.service: `ExecStartPre=+sh -c 'chgrp agi-capsule %t/agi-%i/i&&chmod 620 %t/agi-%i/i'` (O.5's "price, named") | +75 | **17,507** (headroom 2,973) |
What the delta checks: no create or delete · exactly one parent, = old · same tree as old · line 1 of the message = "C H old" with C = the ref's name · the pusher is in group agi-capsule · capsule-ok(old, C, line 1, the message's SSHSIG blocks) passes. It calls `${0%/*}/capsule-ok`, so capsule-ok sits beside the hook.

### Pre-flight (no root; each must print the expected value, else STOP). Measured 06:2xZ
- `getent passwd agi-capsule | wc -l` ; `getent group agi-capsule | wc -l` -> 0 ; 0
- `ls -d /opt/agi/capsule /var/spool/agi /var/lib/agi-capsule /var/lib/agi/capsule-rehearsal.git 2>/dev/null | wc -l` -> 0 (/opt/agi/{bin,pi} and an empty /var/lib/agi pre-exist: never touched)
- `grep -rhiE '^\s*(AllowUsers|AllowGroups|DenyUsers|DenyGroups|Match|AuthorizedKeysFile)' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/ | wc -l` -> 0 (so NO sshd_config edit is needed; a root-owned authorized_keys passes StrictModes)
- `for f in /tmp/agi-capsule/pieces/*; do sh -n $f 2>/dev/null; done; (cd /tmp/agi-capsule/pieces && sha256sum -c ../pieces.sha256)` -> all OK
- memory / disk per skill agi-memory-guard

### Root acts (9 + 1 gated), in order. Each: command · UNDO · PROOF. Rehearsal = throwaway holder keys r1-r3 in /tmp/agi-capsule-rehearsal/k + the owner's PUBLIC device key
- **R1** user: `sudo systemd-sysusers --inline 'u agi-capsule - "agi capsule-login" /var/lib/agi-capsule /bin/sh'` (NOT in group agi: no polkit start rights)
  - UNDO: T6 · PROOF: `getent passwd agi-capsule | cut -d: -f6,7` = /var/lib/agi-capsule:/bin/sh; `sudo passwd -S agi-capsule | cut -d' ' -f2` = L; `id -nG agi-capsule` = agi-capsule
- **R2** pieces: `sudo sh -c 'install -d -m 755 /opt/agi/capsule && cd /tmp/agi-capsule/pieces && install -m 755 capsule-ok capsule-login capsule-seal /opt/agi/capsule/ && install -m 755 capsule-pop.patched /opt/agi/capsule/capsule-pop'` (after N1, extract from config:capsule @REV instead; BANKED: patched vs byte-exact)
  - UNDO: T7 · PROOF: `cmp /opt/agi/capsule/capsule-pop /tmp/agi-capsule/pieces/capsule-pop.patched` silent (and the same for the other 3); `stat -c '%a %U' /opt/agi/capsule/*` = 755 root ×4
- **R3** [KEY: public only] `sudo sh -c 'install -d -m 755 /var/lib/agi-capsule /var/lib/agi-capsule/.ssh && umask 022 && printf "restrict,command=\"/opt/agi/capsule/capsule-login\" %s\n" "<owner device public key>" > /var/lib/agi-capsule/.ssh/authorized_keys'` (the owner reads the PUBLIC line off the phone; never a private key)
  - UNDO: T5 · PROOF: `sudo ssh-keygen -lf /var/lib/agi-capsule/.ssh/authorized_keys | wc -l` = 1 and the fingerprint = the one the phone shows; `sudo stat -c '%a %U' /var/lib/agi-capsule /var/lib/agi-capsule/.ssh /var/lib/agi-capsule/.ssh/authorized_keys` = 755 root, 755 root, 644 root
- **R4** spool: `sudo sh -c 'install -d -m 755 /var/spool/agi && install -d -o agi-capsule -g <posts group> -m 1730 /var/spool/agi/ask && install -d -o agi-capsule -g agi-capsule -m 700 /var/spool/agi/used && install -o agi-capsule -g agi-capsule -m 600 /dev/null /var/spool/agi/ledger && install -d -o root -g <posts group> -m 1770 /var/spool/agi/pop'` (posts group = agi from stage 3; in the rehearsal, the agi-rp group from R8)
  - UNDO: T4 · PROOF: `stat -c '%n %a %U %G' /var/spool/agi/*` = ask 1730 agi-capsule · ledger 600 agi-capsule · pop 1770 root · used 700 agi-capsule
- **R5** rehearsal repo: `sudo sh -c 'git clone -q --bare /tmp/agi-capsule-rehearsal/seed.bundle /var/lib/agi/capsule-rehearsal.git && git -C /var/lib/agi/capsule-rehearsal.git symbolic-ref HEAD refs/heads/trunk'` (seed built unprivileged: one commit with .agi/keys/{owner,r1,r2,r3}, all public)
  - UNDO: T3 · PROOF: `sudo git -C /var/lib/agi/capsule-rehearsal.git ls-tree --name-only trunk .agi/keys/` = owner r1 r2 r3
- **R6** hook: `sudo sh -c 'cd /var/lib/agi/capsule-rehearsal.git && install -m 755 /tmp/agi-capsule/pieces/pre-receive /tmp/agi-capsule/pieces/capsule-ok hooks/'` (at stage 3, into origin.git with the old hook kept as hooks/pre-receive.pre-capsule; source = engine `sect pre-receive` after N2)
  - UNDO: T3 (origin: `sudo mv hooks/pre-receive.pre-capsule hooks/pre-receive; sudo rm hooks/capsule-ok`) · PROOF: `sudo cmp hooks/pre-receive /tmp/agi-capsule/pieces/pre-receive` silent; after R7, a push of a forged `refs/capsule/d1` from an unprivileged clone = "capsule: refs/capsule/d1" (B2)
- **R7** [KEY: dummy] SEAL a dummy: `printf dummy-secret-19-byt | sudo sh -c 'cd /var/lib/agi/capsule-rehearsal.git && /opt/agi/capsule/capsule-seal d1 2 r1 r2 r3'` (then `pc` with owner@4 r1 r2 r3 k=6, the same way)
  - UNDO: T3 · PROOF: `sudo git -C … ls-tree -r --name-only refs/capsule/d1 .agi/capsule` = cred k ring/r1 ring/r2 ring/r3; `sudo git -C … cat-file blob refs/capsule/d1:.agi/capsule/d1/cred | grep -c dummy` = 0; **C9b** `sudo -u agi-capsule systemd-creds decrypt …` fails
- **R8** [SHARED: daemon-reload] units + a rehearsal post: `sudo sh -c 'systemd-sysusers --inline "u agi-rp - - /var/lib/agi-rp"; install -m 644 /tmp/agi-capsule/pieces/capsule-pop.service /tmp/agi-capsule/pieces/capsule-pop.path /run/systemd/system/ && mkdir -p /run/systemd/system/capsule-pop.service.d && printf "[Service]\nWorkingDirectory=/var/lib/agi/capsule-rehearsal.git\n" > /run/systemd/system/capsule-pop.service.d/r.conf && systemctl daemon-reload && systemctl start capsule-pop.path'`
  - UNDO: T1 + T6 · PROOF (**C9/C11**): as agi-rp, drop d1.R + d1.R.L (run cell `wc -c < ${CREDENTIALS_DIRECTORY}/s > /tmp/c9`) + ONE signature -> the tip is unmoved and R waits; drop the 2nd -> the tip moves ONCE, /tmp/c9 = 19, the ledger message = R + names + 2 SSHSIG blocks; the same R again -> refused; `journalctl -u capsule-pop | grep -c dummy` = 0
- **R9** login rehearsal (the owner, from the phone): `sudo install -d -o agi-rp -m 755 /run/agi-rp && sudo -u agi-rp mkfifo -m 600 /run/agi-rp/i && sudo chgrp agi-capsule /run/agi-rp/i && sudo chmod 620 /run/agi-rp/i`; agi-rp writes an ask `rp <url>` into /var/spool/agi/ask/<18 hex>; the reader is `sudo -u agi-rp cat /run/agi-rp/i | od -c`
  - UNDO: T1b · PROOF: phone `ssh agi-capsule@<box> <id>` with a dummy code -> the reader shows code + \r once; the ledger gets 1 line without the code; any other key -> refused (P2); no id -> rc 2 (P4). **P8** (a real Claude Code login) waits for a stage-3 post
- **R10 GATED (owner's go, after R1-R9 pass)** [KEY: the owner's plain key] interim custody: the owner pipes the phone's exported PRIVATE key into `ssh <owner admin>@<box> 'cd <capsule repo> && sudo /opt/agi/capsule/capsule-seal ok <n> <post>…'` (stdin only: never argv, never plain on disk; `.agi/keys/owner` and the posts' keys must be at HEAD, N3)
  - UNDO: none clean (append-only): rotate = a new phone key + a new ok, retire the old ref by a pop · PROOF: K1-K3 replayed with the real posts: owner alone and n-1 posts refused, all n posts pop

### Teardown (back to zero; the stage-2 two system units and /opt/agi/{bin,pi} untouched)
- **T1** `sudo sh -c 'systemctl stop capsule-pop.path capsule-pop.service; rm -rf /run/systemd/system/capsule-pop.path /run/systemd/system/capsule-pop.service /run/systemd/system/capsule-pop.service.d; systemctl daemon-reload; systemctl reset-failed capsule-pop.service 2>/dev/null; :'` · PROOF: `systemctl list-units --all --no-legend 'capsule-pop*' | wc -l` = 0
- **T1b** `sudo rm -rf /run/agi-rp` · PROOF: `ls -d /run/agi-rp 2>/dev/null | wc -l` = 0
- **T3** `sudo rm -rf /var/lib/agi/capsule-rehearsal.git` · PROOF: `ls /var/lib/agi | wc -l` = 0
- **T4** `sudo rm -rf /var/spool/agi` · PROOF: absent
- **T5** `sudo rm -rf /var/lib/agi-capsule /var/lib/agi-rp` · PROOF: absent
- **T6** `sudo sh -c 'userdel agi-rp; userdel agi-capsule; for g in agi-rp agi-capsule; do getent group $g >/dev/null && groupdel $g; done; :'` · PROOF: `getent passwd agi-capsule agi-rp | wc -l` = 0; same for groups
- **T7** `sudo rm -rf /opt/agi/capsule` · PROOF: `ls /opt/agi` = bin pi
- **T8** (no root) `rm -rf /tmp/agi-capsule-rehearsal` (the throwaway r1-r3 keys) · PROOF: absent
Leftovers by design: journal lines for capsule-pop / sshd.

### Non-root acts (graph and engine; DG3 / council, not this subagent)
- **N1** `config:capsule` (write.py create): the pieces above, the seal line and the units. BANKED: capsule-pop byte-exact O.2 or patched (recommendation: patched; without it H1-H3 stand and the pre-receive refuses every pop, B0)
- **N2** config:engine: re-add `pre-receive` with the capsule delta + the agi-post@ pane line = +1,123 B -> 17,507 B
- **N3** `.agi/keys/owner` = the phone's PUBLIC key, committed; the rings point at it (`ring/owner@<n+1>` in the posts' capsules, `ring/owner` in the owner's)
- **N4** doc fold: O.2 patch, O.5 bytes (692 -> 932), and P.6 "0 B, the kernel" corrected: `git pack-refs` moves refs into ONE packed-refs file, so ownership of the refs/capsule/ directory does not pin a capsule ref; the pre-receive does, for pushes
- **N5 (seam)** the ask writer: a post's login wrapper writes `/var/spool/agi/ask/<18 hex>` = `<post> <url>` (mode 644, create-only); and the `asks` listing for carrier (a), which the owner banked

### Open points §O/§P leave undecided: my pick and why
| point | pick | why |
|---|---|---|
| where refs/capsule/* live | the origin bare repo (root-owned); pop = local update-ref as root | a pop never needs a push; mirrors push through the pre-receive |
| who may push refs/capsule/* | group agi-capsule AND the full check | if any reader of the spool could push a valid ledger commit, it could spend a pop before the unit runs L (a denial) |
| ledger contents | R + signer names + the SSHSIG blocks | the pop becomes re-verifiable anywhere, and the pre-receive can check it |
| T format | 40 hex (SHA-1 repo) | blocks H1; a SHA-256 repo needs 64 (named) |
| seal commit | no parent; tree = HEAD + the capsule dir | the ring symlinks resolve inside T; `git log refs/capsule/C` = this capsule's events only |
| k = 0 | refused by capsule-seal and capsule-ok | O.2 pops on 0 signatures if k = 0 (named; guarded at the seal) |
| capsule-login's pane | FIFO + not a symlink + the same uid as the ask file | O.5 as written truncates the ledger and leaves the code in it when a post points i at it (test.txt L7) |
| pane not reading | not fixed: the session blocks, the ask is spent (L10) | a timeout would need a child process carrying the code in its argv |
| asks/<id>/used ref | not built: the spool rename is the claim | the smallest form; the rename is atomic (L8) |
| agi-capsule groups | its own group only, never agi | agi carries the polkit start rights; ask files are 644 (under PKCE the URL is not secret) |
| interim custody ring | capsule `ok`: the posts @1, k = n, the owner NOT in the ring | a lost phone cannot sign its own recovery. The price, named: all n posts together can recover the owner's key, but only into a destination they all sign, and the ledger names them (K3/K4) |
| pqwrap | standalone; `esc` still wraps X25519-only | wiring it into esc is §P's call; it reaches parity with esc's construction |

### Custody seam (NAMED, NOT BUILT)
The owner app's Secure Enclave key emitting SSHSIG (**I1**) · the iMessage extension sharing its keychain group (**I2**) · se-wrap's device side / the 2-of-2 inner seal (O.7) · how a recovered key reaches a NEW phone (K3's destination: in the test it signed inside the unit; the real one must deliver to a new-device public key that is pinned in R.L and signed by the posts: the app or a Terminus import path, VERIFY).
What the box offers that seam: `.agi/keys/owner` (public) · the ring entries `owner@w` · the authorized_keys line · capsule `ok`. Moving the owner from the plain key to the SE key = a new keys/owner + a ring change, which is itself a pop (P.6).


## PIECES (byte-exact)

### authorized_keys.shape (132 B, sha256 093197c3a25a5d06)
~~~~~
restrict,command="/opt/agi/capsule/capsule-login" <owner device key: ssh-ed25519|ecdsa-sha2-nistp256 AAAA..., the public half only>
~~~~~

### capsule-login (932 B, sha256 69c922e2b5032977)
~~~~~
#!/bin/sh
# capsule-login, run ONLY as authorized_keys `restrict,command="/opt/agi/capsule/capsule-login" <owner device key>` (sshd checking that key IS the
# approval, k=1): ssh agi-capsule@<box> <ask-id>, ONE code line on stdin -> the asking post's pane i. The claim is one atomic rename (a used or racing
# id loses); P11: the code is pinned to a URL-safe line <= 512 B; the pane must be a FIFO owned by the ask's own creator; the code is never at rest
d=${AGI_SPOOL:-/var/spool/agi};i=$SSH_ORIGINAL_COMMAND;case $i in ''|*[!a-z0-9]*)exit 2;;esac;mv $d/ask/$i $d/used/$i 2>/dev/null||exit 3
read -r p u<$d/used/$i;case $p in ''|*[!a-z0-9-]*)exit 2;;esac;f=${AGI_RUN:-/run}/agi-$p/i;[ -p $f ]&&[ ! -h $f ]&&[ $(stat -c %u $f) = $(stat -c %u $d/used/$i) ]||exit 5
IFS= read -r c;case $c in ''|*[!A-Za-z0-9._~#-]*)exit 4;;esac;[ ${#c} -le 512 ]||exit 4;printf '%s\r' "$c">$f||exit 5;echo "login $p $i $(date -u +%FT%TZ)">>$d/ledger
~~~~~

### capsule-ok (836 B, sha256 ef6cc083c49a86b0)
~~~~~
#!/bin/sh
# capsule-ok T C R SIG..: exit 0 iff the weights (ring/<holder>@<w>, w=1 if absent) of the distinct ring principals AT T that signed R (namespace
# capsule) sum to >= k >= 1; ring, weights and k are read FROM T (capsule-pop's one formula); prints the signers. Used by the pre-receive delta
t=$1 x=.agi/capsule/$2 R=$3;shift 3;a=$(mktemp);trap 'rm -f $a' EXIT;k=$(git cat-file blob $t:$x/k)||exit 1;case $k in ''|*[!0-9]*)exit 1;;esac
git ls-tree --name-only $t $x/ring/|while read f;do echo "${f##*/} namespaces=\"capsule\" $(echo "$t:$f"|git cat-file --batch --follow-symlinks|tail -n+2)";done>$a
for s;do p=$(ssh-keygen -Y find-principals -s "$s" -f $a 2>/dev/null)&&ssh-keygen -Y verify -f $a -I "$p" -n capsule -s "$s"<"$R">/dev/null 2>&1&&echo "$p";done|sort -u|awk -F@ -v k=$k '1;{s+=NF>1?$NF:1}END{exit !(k>=1&&s>=k)}'
~~~~~

### capsule-pop (1194 B, sha256 e9e07c9cecfd9128)
~~~~~
#!/bin/sh
# capsule-pop R: R = "C H T" (capsule, hash of the launch vector R.L, ledger tip). The ring, k and the sealed bytes are read FROM T, so the
# signatures pin all of them; the WEIGHTS of distinct ring signers (ring/<holder>@<w>, w=1 if absent) summing to k move refs/capsule/C T->new (one CAS: a replay loses), then L runs with C as its only credential
set -e;read -r c h t<"$1";x=.agi/capsule/$c;r=$(mktemp);trap 'rm -f $r $r.ok $r.c' EXIT;[ "$(git hash-object "$1.L")" = "$h" ]
g(){ echo "$t:$1"|git cat-file --batch --follow-symlinks|tail -n+2;};git ls-tree --name-only $t $x/ring/|while read f;do echo "${f##*/} namespaces=\"capsule\" $(g $f)";done>$r
for s in "$1".sig.*;do p=$(ssh-keygen -Y find-principals -s "$s" -f $r)&&ssh-keygen -Y verify -f $r -I "$p" -n capsule -s "$s"<"$1">/dev/null 2>&1&&echo "$p";done|sort -u>$r.ok
[ $(awk -F@ '{s+=NF>1?$NF:1}END{print s+0}' $r.ok) -ge $(git cat-file blob $t:$x/k) ];git update-ref refs/capsule/$c $(cat "$1" $r.ok|git commit-tree $t^{tree} -p $t) $t;git cat-file blob $t:$x/cred>$r.c
systemd-run -q --wait -p LoadCredentialEncrypted=s:$r.c -p DynamicUser=yes -p StandardOutput=null -p StandardError=null sh -c "$(jq -r .run "$1.L")"
~~~~~

### capsule-pop.diff (826 B, sha256 26aa83d12f65db5b)
~~~~~
4c4,5
< set -e;read -r c h t<"$1";x=.agi/capsule/$c;r=$(mktemp);trap 'rm -f $r $r.ok $r.c' EXIT;[ "$(git hash-object "$1.L")" = "$h" ]
---
> set -e;r=$(mktemp);trap 'rm -f $r $r.ok $r.c $r.R*' EXIT;for f in "$1" "$1".L "$1".sig.*;do cp "$f" $r.R${f#"$1"};done;set -- $r.R
> read -r c h t<"$1";x=.agi/capsule/$c;expr "$t" : '[0-9a-f]\{40\}$'>/dev/null;[ "$(git hash-object "$1.L")" = "$h" ]
7c8
< [ $(awk -F@ '{s+=NF>1?$NF:1}END{print s+0}' $r.ok) -ge $(git cat-file blob $t:$x/k) ];git update-ref refs/capsule/$c $(cat "$1" $r.ok|git commit-tree $t^{tree} -p $t) $t;git cat-file blob $t:$x/cred>$r.c
---
> [ $(awk -F@ '{s+=NF>1?$NF:1}END{print s+0}' $r.ok) -ge $(git cat-file blob $t:$x/k) ];n=$(cat "$1" $r.ok "$1".sig.*|git commit-tree $t^{tree} -p $t);git update-ref refs/capsule/$c $n $t;git cat-file blob $t:$x/cred>$r.c
~~~~~

### capsule-pop.patched (1330 B, sha256 2f0ec19a4d494ded)
~~~~~
#!/bin/sh
# capsule-pop R: R = "C H T" (capsule, hash of the launch vector R.L, ledger tip). The ring, k and the sealed bytes are read FROM T, so the
# signatures pin all of them; the WEIGHTS of distinct ring signers (ring/<holder>@<w>, w=1 if absent) summing to k move refs/capsule/C T->new (one CAS: a replay loses), then L runs with C as its only credential
set -e;r=$(mktemp);trap 'rm -f $r $r.ok $r.c $r.R*' EXIT;for f in "$1" "$1".L "$1".sig.*;do cp "$f" $r.R${f#"$1"};done;set -- $r.R
read -r c h t<"$1";x=.agi/capsule/$c;expr "$t" : '[0-9a-f]\{40\}$'>/dev/null;[ "$(git hash-object "$1.L")" = "$h" ]
g(){ echo "$t:$1"|git cat-file --batch --follow-symlinks|tail -n+2;};git ls-tree --name-only $t $x/ring/|while read f;do echo "${f##*/} namespaces=\"capsule\" $(g $f)";done>$r
for s in "$1".sig.*;do p=$(ssh-keygen -Y find-principals -s "$s" -f $r)&&ssh-keygen -Y verify -f $r -I "$p" -n capsule -s "$s"<"$1">/dev/null 2>&1&&echo "$p";done|sort -u>$r.ok
[ $(awk -F@ '{s+=NF>1?$NF:1}END{print s+0}' $r.ok) -ge $(git cat-file blob $t:$x/k) ];n=$(cat "$1" $r.ok "$1".sig.*|git commit-tree $t^{tree} -p $t);git update-ref refs/capsule/$c $n $t;git cat-file blob $t:$x/cred>$r.c
systemd-run -q --wait -p LoadCredentialEncrypted=s:$r.c -p DynamicUser=yes -p StandardOutput=null -p StandardError=null sh -c "$(jq -r .run "$1.L")"
~~~~~

### capsule-pop.path (70 B, sha256 837f46d052f82c4e)
~~~~~
[Path]
PathChanged=/var/spool/agi/pop
[Install]
WantedBy=paths.target
~~~~~

### capsule-pop.service (345 B, sha256 25dc37d0393f9151)
~~~~~
[Service]
Type=oneshot
WorkingDirectory=/var/lib/agi/origin.git
Environment=PATH=/opt/agi/capsule:/usr/bin:/bin GIT_AUTHOR_NAME=capsule-pop GIT_AUTHOR_EMAIL=capsule@agi GIT_COMMITTER_NAME=capsule-pop GIT_COMMITTER_EMAIL=capsule@agi
ExecStart=sh -c 'for R in /var/spool/agi/pop/*.R;do [ -f "$$R" ]&&capsule-pop "$$R"&&rm -f "$$R" "$$R".*;done;:'
~~~~~

### capsule-seal (1074 B, sha256 9ad072d2554b19a3)
~~~~~
#!/bin/sh
# capsule-seal C K HOLDER[@W].. <secret -- root, once per capsule (O.1 SEAL): the secret on STDIN only (never argv, never plain on disk) -> systemd-creds
# encrypt (host key) -> ONE commit = HEAD's tree + .agi/capsule/C/{cred, k, ring/<holder>[@w] -> ../../../keys/<holder>} -> refs/capsule/C, create-only
set -e;c=$1 k=$2;shift 2;x=.agi/capsule/$c;i=$(mktemp);trap 'rm -f $i $i.c' EXIT;expr "$c" : '[a-z0-9][a-z0-9-]*$'>/dev/null;expr "$k" : '[1-9][0-9]*$'>/dev/null
a(){ GIT_INDEX_FILE=$i git update-index --add --cacheinfo $1,$2,$3;};rm $i;GIT_INDEX_FILE=$i git read-tree HEAD;systemd-creds encrypt --name=s - $i.c
a 100644 $(git hash-object -w $i.c) $x/cred;a 100644 $(echo $k|git hash-object -w --stdin) $x/k;for h;do case $h in *[!a-z0-9@-]*|@*|*@*@*|*@)exit 2;;esac
git cat-file -e HEAD:.agi/keys/${h%@*};a 120000 $(printf ../../../keys/${h%@*}|git hash-object -w --stdin) $x/ring/$h;done
n=$(GIT_INDEX_FILE=$i git write-tree);n=$(echo "SEAL $c k=$k $*"|git commit-tree $n);git update-ref refs/capsule/$c $n 0000000000000000000000000000000000000000;echo $n
~~~~~

### capsule.pre-receive.delta (480 B, sha256 7634e8e4fe2b078e)
~~~~~
case $r in refs/capsule/*)m=$(mktemp -d);git cat-file commit $n|sed '1,/^$/d'>$m/m;head -1 $m/m>$m/R;awk -v d=$m '/^-----BEGIN SSH SIG/{f=d"/s"++i}f{print>f}/^-----END SSH SIG/{f=""}' $m/m;read -r c h t<$m/R
[ "$c $t $(git rev-parse $n^@)" = "${r#refs/capsule/} $o $o" ]&&[ $(git rev-parse $n^{tree}) = $(git rev-parse $o^{tree}) ]&&id -nG|grep -qw agi-capsule&&${0%/*}/capsule-ok $o $c $m/R $m/s*>/dev/null;v=$?;rm -rf $m;[ $v = 0 ]||{ echo "capsule: $r";exit 1;};continue;;esac
~~~~~

### capsule.sysusers (65 B, sha256 7c875d1c3759e72c)
~~~~~
u agi-capsule - "agi capsule-login" /var/lib/agi-capsule /bin/sh
~~~~~

### pqwrap (2101 B, sha256 e2e5e22ea069550e)
~~~~~
#!/usr/bin/env node
// pqwrap keygen DIR | wrap DIR <share >env | open DIR <env >share -- the §P.7 escrow share wrap (V-L1): hybrid X25519 + ML-KEM-768, both must break.
// HKDF-SHA256(ss_kem||ss_x||ct||eph||rcpt_x, info "agi-escrow-hybrid-v1") -> ChaCha20-Poly1305; env = eph32||ct1088||nonce12||tag16||body.
// DIR: x.pub k.pub (public, committable) + x.key k.key (the holder's own, mode 600). node:crypto only; never shell openssl (3.0 has no ML-KEM)
import c from'node:crypto';import f from'node:fs';const[v,D]=process.argv.slice(2),L=Buffer.from('agi-escrow-hybrid-v1'),r=n=>f.readFileSync(D+'/'+n)
const X=k=>Buffer.from(k.export({format:'jwk'}).x,'base64url'),H=(s,x,ct,e,p)=>Buffer.from(c.hkdfSync('sha256',Buffer.concat([s,x,ct,e,p]),Buffer.alloc(0),L,32))
const a=(k,n,d)=>(d?c.createDecipheriv:c.createCipheriv)('chacha20-poly1305',k,n,{authTagLength:16}),o=b=>process.stdout.write(b)
if(v=='keygen')for(const[t,n]of[['x25519','x'],['ml-kem-768','k']]){const p=c.generateKeyPairSync(t);f.writeFileSync(`${D}/${n}.pub`,p.publicKey.export({type:'spki',format:'pem'}));f.writeFileSync(`${D}/${n}.key`,p.privateKey.export({type:'pkcs8',format:'pem'}),{mode:0o600})}
if(v=='wrap'){const q=c.createPublicKey(r('x.pub')),e=c.generateKeyPairSync('x25519'),E=X(e.publicKey),{sharedKey:s,ciphertext:ct}=c.encapsulate(c.createPublicKey(r('k.pub')))
 const n=c.randomBytes(12),z=a(H(s,c.diffieHellman({privateKey:e.privateKey,publicKey:q}),ct,E,X(q)),n);z.setAAD(Buffer.concat([L,E,ct]));const b=Buffer.concat([z.update(f.readFileSync(0)),z.final()]);o(Buffer.concat([E,ct,n,z.getAuthTag(),b]))}
if(v=='open'){const m=f.readFileSync(0),E=m.subarray(0,32),ct=m.subarray(32,1120),q=c.createPublicKey(r('x.pub')),e=c.createPublicKey({key:{kty:'OKP',crv:'X25519',x:E.toString('base64url')},format:'jwk'})
 const z=a(H(c.decapsulate(c.createPrivateKey(r('k.key')),ct),c.diffieHellman({privateKey:c.createPrivateKey(r('x.key')),publicKey:e}),ct,E,X(q)),m.subarray(1120,1132),1)
 z.setAAD(Buffer.concat([L,E,ct]));z.setAuthTag(m.subarray(1132,1148));o(Buffer.concat([z.update(m.subarray(1148)),z.final()]))}
~~~~~

### pre-receive (915 B, sha256 8d19baf96bbbffc8)
~~~~~
#!/bin/sh
e=$(git hash-object -t tree /dev/null)
while read o n r;do case $r in refs/capsule/*)m=$(mktemp -d);git cat-file commit $n|sed '1,/^$/d'>$m/m;head -1 $m/m>$m/R;awk -v d=$m '/^-----BEGIN SSH SIG/{f=d"/s"++i}f{print>f}/^-----END SSH SIG/{f=""}' $m/m;read -r c h t<$m/R
[ "$c $t $(git rev-parse $n^@)" = "${r#refs/capsule/} $o $o" ]&&[ $(git rev-parse $n^{tree}) = $(git rev-parse $o^{tree}) ]&&id -nG|grep -qw agi-capsule&&${0%/*}/capsule-ok $o $c $m/R $m/s*>/dev/null;v=$?;rm -rf $m;[ $v = 0 ]||{ echo "capsule: $r";exit 1;};continue;;esac
case $n in *[!0]*);;*)continue;;esac;[ $r = refs/heads/trunk ]&&{ agi-gate $n||{ echo "gate: $n";exit 1;};continue;};case $o in *[!0]*);;*)o=$(git merge-base HEAD $n 2>/dev/null||echo $e);;esac
f=$(git diff --name-only $o $n)||exit 1;for p in $f;do g=$(git check-attr --source=$n owner -- "$p"|cut -d' ' -f3);id -nG|grep -qw "$g"||{ echo "$p: $g";exit 1;};done;done
~~~~~

### pre-receive.base (435 B, sha256 f5cd2eb8d22e1301)
~~~~~
#!/bin/sh
e=$(git hash-object -t tree /dev/null)
while read o n r;do case $n in *[!0]*);;*)continue;;esac;[ $r = refs/heads/trunk ]&&{ agi-gate $n||{ echo "gate: $n";exit 1;};continue;};case $o in *[!0]*);;*)o=$(git merge-base HEAD $n 2>/dev/null||echo $e);;esac
f=$(git diff --name-only $o $n)||exit 1;for p in $f;do g=$(git check-attr --source=$n owner -- "$p"|cut -d' ' -f3);id -nG|grep -qw "$g"||{ echo "$p: $g";exit 1;};done;done
~~~~~

## REHEARSAL RUN R1-R9 + the STAND-IN phone key (owner night plan 06:5xZ items 2 + 5; 07:1xZ-07:3xZ)
Executed by an Opus 5.5 subagent of director-general-3; spot-checked by DG3 (users, units, cmp of the 4 installed scripts, fingerprints, ledger, refs). R10 (the owner's REAL key) NOT run: owner's go.
| act | result |
|---|---|
| pre-flight | PASS (the sshd grep needs sudo: one sshd_config.d file is root-only; 0 restricting lines) |
| R1 agi-capsule user | PASS (home /var/lib/agi-capsule, locked, groups agi-capsule only) |
| R2 pieces | PASS: /opt/agi/capsule/{capsule-ok,capsule-login,capsule-seal} + capsule-pop = capsule-pop.patched (council pick banked), 755 root, cmp silent |
| R3 authorized_keys | PASS: ONE line, restrict,command="/opt/agi/capsule/capsule-login" + the STAND-IN key (SHA256:Is+B34WMLlFbC5eAF6pSdRLl+pQQ0hRnxecXCH+JOdY, ed25519, owner-user-only, dir 700 / key 600; delete when the real phone key lands) |
| R4 spool | PASS (ask 1730 agi-capsule · ledger 600 · pop 1770 root · used 700) |
| R5 rehearsal repo | PASS (/var/lib/agi/capsule-rehearsal.git, keys owner r1 r2 r3, all public) |
| R6 hook | PASS: a forged refs/capsule/d1 (one signature, k=2) refused "capsule: refs/capsule/d1", tip unmoved |
| R7 seal d1 + pc | PASS: cred/k/ring present, the secret absent in plain (grep 0); decrypt as agi-capsule = Permission denied (C9b) |
| R8 pop units | PASS (C9/C11): 1 signature -> tip unmoved, R waits; the 2nd -> tip moves ONCE, the cell read 19 B, ledger = R + names + 2 SSHSIG; the same R again refused; journal grep dummy = 0 |
| R9 login over LOOPBACK (the passkey-code route, stand-in key) | PASS: code + CR typed into the pane ONCE · ledger 1 line without the code, ask moved to used · another key rc 255 · no id rc 2 · used id rc 3 · any other command rc 2 |
Deviations: D1 R4 needs the agi-rp group R8 creates -> R8's user line ran first, unchanged · D2 root has no git identity -> capsule-seal ran with author/committer capsule-seal (as capsule-pop.service sets) -> fold into capsule-seal (N4) · D3 the run cell's /tmp is private under DynamicUser -> the byte count went to the journal (logger -t agi-c9).
BANKED F1: sealing CREATED the box's host credential key /var/lib/systemd/credential.secret (absent before R7); removing it at teardown is optional and left commented in the undo script -- the owner's / belam's call.
Left installed for the night: users agi-capsule + agi-rp; /opt/agi/capsule; /var/lib/agi-capsule/.ssh/authorized_keys; /var/spool/agi; the rehearsal repo (refs/capsule/d1 popped once, refs/capsule/pc); capsule-pop.path active from /run (gone at reboot); the /run/agi-rp/i pane; rehearsal keys under /tmp; the stand-in key. UNDO: /tmp/agi-capsule/undo.sh (700, not run): T1 T1b T3-T8; T9 (delete the stand-in key) and T10 (credential.secret) commented.
