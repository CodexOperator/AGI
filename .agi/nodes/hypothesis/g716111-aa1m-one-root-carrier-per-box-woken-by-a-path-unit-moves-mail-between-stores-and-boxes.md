---
id: hypothesis:g716111-aa1m-one-root-carrier-per-box-woken-by-a-path-unit-moves-mail-between-stores-and-boxes
mint_id: 8629e41201d942b995827239f53eaae1
type: hypothesis
parents:
  - goal:g7.16.1.11.11.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: f5dd822fae1bd12f
season: 2
testable_claim: "(M2) ONE carrier per box (root) reads the post rows' LOCATION cells (box, store): for a recipient Q on this box it moves P's `refs/box/P/Q` into Q's store through a runuser pipe (AA2's agi-carry, 454 B), for Q on another box it pushes `refs/box/P/*` to the remote head and Q's box carrier fetches it; it is woken by a path unit watching each store's `refs/box` (PathChanged, no polling cron) plus ONE timer for remote fetches; a message sent by P reaches Q's store within one wake with no shared file written and no worktree touched."
title: "AA1.M carrier: ONE root carrier per box, woken by a path unit on each store's refs/box (no polling cron) plus one timer for remote fetches, reads the rows' location cells and moves mail store-to-store on a box (runuser pipe, agi-carry) or box-to-box (push / fetch of the remote head)"
town: core
---
# hypothesis:g716111-aa1m-one-root-carrier-per-box-woken-by-a-path-unit-moves-mail-between-stores-and-boxes

## Measured
- doc:rse-aa1-boxes section AA1.M (alive, posts/alive; belam [owner] 18:16Z item M1; designed and scratch-tested by alive 18:1xZ); belam ACCEPTED as designed ([decision] 18:2xZ, owner 18:2xZ GO). The numbers are alive's scratch measurements, not re-run by me. HORIZON: the build is not dispatched; each host act is belam's own GO.
- Bytes (expansion, 0 B in the zygote): the carrier = agi-carry 454 B + one rows-reading line ~200 B + a path unit ~60 B.
- HOST ACT 1 RESULT (belam, as root, 18:27:58Z, script read whole, sha256 OK, rolled back; doc:rse-aa1-boxes AA1.M on posts/alive): rc 0, `CARRIED hello-m1 U`, `BARRIER HOLDS`: the two-uid runuser carry WORKS and the 0700 barrier holds, but the receiver printed U (does not trust the sender's key), not G. Cause measured by alive 18:3xZ: each post's ~/.signers = the trunk's `.agi/keys/*` (3 keys: DT-1, DT-2, TM-new) + its own key, so all-is-one's lacked alive's; and a row's `pubkey` cell is NOT the git signing key (two keys per post).
- SIGNERS FIX (alive 18:29Z, REVISED 18:3xZ on self-perpetuating's objection, INCLUDED in this lane by belam [rule] 18:5xZ): at unit start root (ExecStartPre=+) reads ~<post>/.ssh/id_ed25519.pub and appends `<post>@agi namespaces="git" valid-after=<now> <pub>` to ONE root-owned allowed_signers, only when the key changed, stamping `valid-before` on that post's previous line (old generations still verify at their own dates); `.agi/keys/` stops being a source; the row hex `pubkey` stays send.py's seatsig and retires with it. Cross-box: the allowed_signers file itself TRAVELS as a commit signed by the box's root key (AA2 'keys: Source and travel', refs/agi/ring/BOX in the commons); a receiving box accepts it only if it verifies against the ring.
- NOT MEASURED (alive: needs root): runuser between two real post uids, the path unit firing on a store write, a remote head on a second box. belam: each of the THREE is its OWN HOST ACT = its own GO, ONE line per act with the exact command, the before-state and the one-command rollback; he GOes it the same hour.

## CLAIM
(M2) ONE carrier per box (root) reads the post rows' LOCATION cells (box, store): for a recipient Q on this box it moves P's `refs/box/P/Q` into Q's store through a runuser pipe (AA2's agi-carry, 454 B), for Q on another box it pushes `refs/box/P/*` to the remote head and Q's box carrier fetches it; it is woken by a path unit watching each store's `refs/box` (PathChanged, no polling cron) plus ONE timer for remote fetches; a message sent by P reaches Q's store within one wake with no shared file written and no worktree touched.

## Dispatch line
config-max: the path unit + the one timer (root-installed; host acts) / template-max: none / code: the carrier's rows-reading line. NOT dispatched: HORIZON; the three host acts below are the build's steps and each needs belam's GO first.

## FALSIFIERS
HOST ACT 1 (RUN once, belam 18:27:58Z: CARRIED U + BARRIER HOLDS, rolled back; RE-RUN after the signers fix must read `CARRIED hello-m1 G`, not U, with BARRIER HOLDS; before-state: /tmp/m1 absent, no live store touched; rollback: `rm -rf /tmp/m1`; each re-run is a fresh belam GO) a root `runuser -u <Q uid>` pipe from P's store to Q's store delivers one ref between two REAL post uids · HOST ACT 2: the path unit fires the carrier on a write to a store's `refs/box` and not otherwise (before-state: unit absent; rollback: `systemctl disable --now` the unit + remove the file) · HOST ACT 3: a push to a remote head on a SECOND box is fetched by that box's carrier and the reply returns (before-state: one box; rollback: remove the remote + the timer) · negative: no `cron` entry or polling loop exists for local delivery.

## TESTS
scratch first (alive's two-repo fixture), then each host act on the real box ONLY after belam's GO; each act's result recorded on its experiment node with the before-state it started from.

## FILE SCOPE
the carrier script + the path unit + one timer unit (root files: belam's GO per act) · its own experiment nodes. NEVER an inbox file.

## CEILING
3 host acts, one at a time, each its own belam GO · 1 parent · kids <= 1 · regular review. HORIZON.

## Placement (DG1 inner loop, 10-02 19:16Z, on DG2's return)
(M2) as WRITTEN is DISPROVED on its wake conjunct (verdict:dg2-aa1m-m2, 0.8): a watch on `refs/box` fires only on a sender's FIRST send (inotify is not recursive; the ref is `refs/box/P/Q`, two levels down). The corrective is hypothesis:g716111-aa1m-every-send-wakes-the-carrier-through-a-per-sender-path-watch (a template path unit per sender on `refs/box/P`, the per-row dir pre-created by root): ACCEPTED, and its HOST ACT 2 package (doc:dg2-aa1m-host-act-2) went to belam as ONE line for his GO; HOST ACT 2 RAN 19:32:46Z (belam, root) and was rolled back: per-sender fires on every send (3/3), refs/box on the first only (1/3), the unit RE-ARMS after pack-refs (5/5, no gc mitigation), a ghost row waits, pid 1 inotify +1 per unit; GHOST-after was untested (script flaw) and then MET by HOST ACT 2b (belam, root, 19:39:48Z: a waiting unit attaches when its dir appears: fired=1, then 2 on a 2nd write): host act 2 is 8 of 8, and the live unit may use the default shape (paths.target at boot), no ordering after the post unit. Details on the corrective hypothesis. Host acts 1 (re-run after the signers fix, must read G) and 3 (a second box) are unchanged and each its own GO. The signers fix above stays part of this hypothesis.

## BUILD (director-general-3, 10-02 19:39Z)
Built, scratch only (one uid, AGI_RUN=none; no root act run). Pieces in config:engine-root, map lines in config:engine: box-carry (1784 B: P's refs/box/P/* -> each recipient's store on this box by pack-objects | unpack-objects --strict + update-ref CAS, ff-only, run as the post's own uid; a recipient on another box -> pushed from a ROOT-OWNED staging repo, never from a post's store, so a post's repo config never runs as root; --fetch = the timer: the hub's refs/box/*/Q -> Q's store) · agi-signers (698 B, alive's 18:29Z fix: root appends one generation line per key change to ONE allowed_signers, stamps valid-before on the old line; option syntax namespaces="git",valid-after="..." comma-separated, NOT space-separated) · agi-carry@.path (PathChanged on the SENDER's own refs/box/<P>, DG2's host act 2 result), agi-carry@.service, agi-carry-fetch.timer + .service (systemd-analyze verify: only 'box-carry not installed').
Test extensions/agi/tests/box-carry.t.sh (reads the pieces from the nodes): k1 deliver + read from the recipient's own store · k2 idempotent, once · k3 only the sender's own channels, k3b a planted foreign channel is not forwarded · k4 diverged recipient tip refused loud, k4b sender-rewritten tip refused by the ff check · k5 box A -> hub -> box B and the reply back · k6 no hub = nothing pushed · k7 no inbox file, worktree clean · s1-s4 signers: once, rotation stamps valid-before, OLD key verifies at its own date and is refused after valid-before, NEW key verifies · n1-n3 no python / cron / inbox path / sleep loop. 24 ok at first cut, 33 ok after the two reviews (k3c k3d k3e s5 s7 s8 s9 s10 added); mutations caught: ff check removed (k4b), own-prefix removed (k3b + k5), valid-before stamp removed (s2 s3).
NOT BUILT, host side (each its own belam GO): (1) install of the four units + box-carry + agi-signers under /opt/agi/bin and /etc/agi/carry.env (AGI_BOX AGI_REPO AGI_HUB cells) · (2) the post unit delta: ExecStartPre=+/opt/agi/bin/agi-signers %i ONLY (belam host act 2b 19:39Z: a waiting per-sender path unit attaches when its dir appears later, so NO per-row mkdir and NO ordering after the post unit; the units take the default paths.target shape) · (3) host act 1 re-run (expects CARRIED G now) · (4) a 2nd box. The per-post stores (g.git) do not exist on the box yet (AA2, goal:g7.16.1.11.12): the carrier needs them. 32 rows = 32 path instances (+32 inotify of 128; belam 19:32Z).

## REVIEW (director-general-3, 10-02 20:03Z)
Sonnet review 1 REJECT (2 critical: a ref name spliced into sh -c as the recipient or root; a post-owned pub file copied whole into the root allowed_signers; + as() re-running as root when the post-uid command failed) -> fixed 742432512, re-review ACCEPT_WITH_RESIDUE (criticals closed; mutation-checked). Residues closed in the next commit: agi-signers reads <= 400 B and needs the exact ed25519 blob shape (a 2 MB line is refused), lock on $F.lock (sed -i swaps the inode), AGI_RUN other than runuser|none refused, a name starting with - refused, fetch exit code 0 on a clean run. Open LOW: a hub-bound ref is not checked against the matrix for its recipient (a post can push a channel name to the hub that no one reads) · the symlinked-key probe needs two real uids (HOST ACT 1) · StartLimit on the path unit's own trigger limit untested (needs root). NOT closed: config_max (AGI_BOX / AGI_HUB / AGI_REPO live in /etc/agi/carry.env, to be generated from graph cells by the install).

## SECURITY MUR CORRECTIVE (director-general-3, 10-02 20:46Z; mur dg3aa1m-m2 accept_with_residue, 6 stood)
| # | residue | closed by |
|---|---|---|
| 1 | root read the matrix from a post-writable repo HEAD (refs/replace honoured) | box-carry needs a PINNED 40-hex AGI_TRUNK (refuses a ref or HEAD), exports GIT_NO_REPLACE_OBJECTS=1, reads posts.md and box's a() at that sha (k0, k0b); the fixture HEAD sits PAST the pin with flipped cells and a deny-all a(), so reading HEAD instead turns k0c k5 etc. red (re-mur #1) |
| 2 | root git on a foreign-owned repo, no safe.directory | the units carry GIT_CONFIG_COUNT/KEY_0 and carry.env the VALUE_0 = box.root (the agi-boot pattern, never global) |
| 3 | hub-bound and hub-sourced refs not matrix-checked | box's own a() (sect box at the pinned sha, so the level rule flows in with no copy) gates local, hub-bound and hub-sourced refs (k5c, k5d) |
| 4 | a send during the oneshot is coalesced | the carrier re-scans P's tips until they stop moving (max 5), k4c; still moving after pass 5 = exit 75 + Restart=on-failure, k4d |
| 5 | config_max | the cells below |
| 6 | untested guards | s0 (a held lock blocks), k3f (unknown run mode), k0, k0b, k5c, k5d, k4c: each turned red by removing its guard; the symlinked key file is read AS the post by runuser: it needs two real uids = HOST ACT 1's probe, stated, not tested here |
Missed items closed: TimeoutStartSec=120 on both services · k7 now asserts the matrix repo's files and status are untouched and no path named *inbox* exists · k3d asserts the runuser path was tried (a runuser shim logs agi-belam) · the old-key date window is a stated BOUND (agi-signers comment): git checks a signature at the commit's own date, which its signer writes · engine.md piece count refreshed.
## CELLS (config_max: /etc/agi/carry.env is derived at install, never typed; re-mur dg3aa1m-m2c, 21:03Z)
| env in carry.env | exact source |
|---|---|
| AGI_REPO | .agi/config.json `box.repo` = "/data/work/agi" (belam 12e8065cc; NOT box.root, which stays a [box].md leak-scanner field) |
| GIT_CONFIG_VALUE_0 (safe.directory) | the same cell `box.repo`: the install writes it into carry.env; the units carry only GIT_CONFIG_COUNT and GIT_CONFIG_KEY_0, the literal `*` is gone |
| AGI_STORES | the post units' StateDirectory root (agi-post@.service `StateDirectory=agi/%i`, default /var/lib/agi): no cell |
| AGI_BOX | .agi/config.json `box.alias` = "local-town" (belam 059414660), equal to the `box` value its post rows carry |
| AGI_HUB | .agi/config.json `box.hub` = "" (belam 059414660; empty = no remote: a remote recipient stays in the sender's store) |
| AGI_TRUNK | no cell: the 40-hex sha of the town trunk ref, written into carry.env by the install and the tick (root-owned file; never a post-writable ref) |
## BOUNDS (stated, not hidden)
- Re-scan tail: the carrier re-scans a sender's tips up to 5 passes; tips still moving after the last pass = exit 75 and the service restarts (Restart=on-failure, RestartSec=5): case k4d. What stays UNMEASURED is how systemd coalesces PathChanged events that fire while the oneshot runs (one re-trigger or none): a HOST probe with belam's GO, in the same act as the install.
- Old-key date window: a rotated-out key still verifies a commit it dates inside its own window (git checks a signature at the commit's own date, which its signer writes).
- Symlinked key file: read AS the post by runuser, so it cannot reach a root-only file: needs two real uids (host act 1).
- Pieces: engine.md maps 37 pieces; 40 `###` blocks exist in engine*.md (agi-boot, agi-boot.service and matrix are not in the map).
