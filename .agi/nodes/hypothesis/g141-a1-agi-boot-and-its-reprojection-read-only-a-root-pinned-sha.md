---
id: hypothesis:g141-a1-agi-boot-and-its-reprojection-read-only-a-root-pinned-sha
mint_id: 648ac855d1324abfa30597a89e501465
type: hypothesis
parents:
  - goal:g1.41
next_edges: []
confidence: 0.75
edited_by: director-general-1
scaffold_hash: 76171befa0582e8b
season: 2
testable_claim: "(A1) root's boot chain reads ONLY a 40-hex trunk sha pinned in /etc/agi/carry.env (AGI_TRUNK), never HEAD: (c1) agi-boot.service loads EnvironmentFile=/etc/agi/carry.env and its ExecStart extracts the agi-boot section from $AGI_TRUNK:engine-root.md, the word HEAD in no ExecStart; (c2) agi-boot starts with t=${AGI_TRUNK:?} and exits 1 before any git read, any ACL change and any start unless the value is exactly 40 chars of [0-9a-f]; (c3) with the pin set, moving HEAD's branch to a commit whose posts.md carries an extra boot:true row changes nothing: the projected units, the started posts and the baked agi-project.service are byte-identical to a boot before the move, and that service's ExecStart has 0 HEAD"
title: "G1.41 A1 (RED -> DG, owner 19:0xZ 'Leave it, fix via DG only'): agi-boot and the agi-project re-projection it installs read only a root-pinned 40-hex sha from /etc/agi/carry.env, never HEAD; engine-root.md only, engine.md untouched"
town: core
---
# hypothesis:g141-a1-agi-boot-and-its-reprojection-read-only-a-root-pinned-sha

## Measured
- engine-root.md agi-boot.service ExecStart (:63): `echo HEAD:.agi/nodes/.geometry/engine-root.md|git cat-file --batch ...|sh -s` runs, as ROOT, bytes read from HEAD of WorkingDirectory=/data/work/agi. agi-boot (:71,:74) takes `t=${AGI_TRUNK:-HEAD}` and reads config.json, engine.md (agi-project) and posts.md at $t; the unit sets no AGI_TRUNK, so $t is HEAD.
- Scratch run of the real agi-project block (engine.md ### agi-project, 2,242 B) against trunk 86d234fcd1, 10-07 20:5xZ: with r=HEAD the baked agi-project.service carries `echo HEAD:` (1 HEAD in the ExecStart) and agi-project.path watches logs/HEAD, so root RE-PROJECTS from the live ref on every trunk move, not only at boot. With r = a 40-hex sha: 0 HEAD in the ExecStart, the sha baked, the path unit degenerates to `PathChanged=<gitdir>/logs/` (no ref to watch; a re-run re-projects the same pinned tree, idempotent). So the pin needs NO engine.md edit.
- Writability, mode bits read as director-general-1 (agi group), nothing written: /data/work/agi/.git and HEAD not writable; refs/heads, refs/heads/local-maxxing, refs and objects WRITABLE. HEAD is the symbolic ref refs/heads/local-maxxing/season2/main, so a replaced loose ref (lockfile + rename in a writable dir) moves what root runs. /etc/agi is root:root 755, carry.env root:root 644 (a root-held home exists).
- The pattern exists: box-carry (engine-root.md:91) refuses AGI_TRUNK unless it is 40 chars of [0-9a-f]; doc:dg3-aa1m-install-packages F2 says the pin is set at install and a landing does not move it (STEP=pieces with the new T refreshes it). The INSTALLED pin is f024955299bc1763db6ce76cb316539b838f0d13, 457 commits behind origin/local-maxxing/season2/main.
- Bytes: engine-root.md is expansion (13,419 B whole, no rail); engine.md fenced 7,435 / 8,192 and whole 9,307 / 12,288 at trunk 86d234fcd1 (the .20 re-cut adds +21 each): this round touches neither. SM lane A1 (f2f6c06010): DG3 builds first; engine.md only after .20 lands, which this round does not need.

## CLAIM
(A1) root's boot chain reads ONLY a 40-hex trunk sha pinned in /etc/agi/carry.env (AGI_TRUNK), never HEAD: (c1) agi-boot.service loads EnvironmentFile=/etc/agi/carry.env and its ExecStart extracts the agi-boot section from $AGI_TRUNK:engine-root.md, the word HEAD in no ExecStart; (c2) agi-boot starts with t=${AGI_TRUNK:?} and exits 1 before any git read, any ACL change and any start unless the value is exactly 40 chars of [0-9a-f]; (c3) with the pin set, moving HEAD's branch to a commit whose posts.md carries an extra boot:true row changes nothing: the projected units, the started posts and the baked agi-project.service are byte-identical to a boot before the move, and that service's ExecStart has 0 HEAD.

## Dispatch line
config-max: the pin VALUE is a cell in /etc/agi/carry.env, host-held, written by belam's STEP=pieces act, never by this round / template-max: the unit's EnvironmentFile line + its ExecStart (two lines) / code: the 40-hex gate in agi-boot (copy of engine-root.md:91, 2 lines) and `t=${AGI_TRUNK:?}`.

## FALSIFIERS
In a mktemp repo with fakes on PATH (the test_agi_boot.py shape: setfacl / systemctl stubs, AGI_RAM, AGI_BOOT_OUT): pin = good sha, HEAD advanced to a commit with an extra boot row `evil` -> projected rows and starts are the good tree's, no agi-post@evil, agi-project.service ExecStart 0 HEAD · pin unset -> rc 1, a stub git that logs argv shows 0 reads, 0 setfacl, 0 start · pin short (7), 41 chars, uppercase hex, non-hex, empty, trailing newline -> rc 1 each, same 0 · the unit text: EnvironmentFile=/etc/agi/carry.env present, HEAD in no ExecStart · the ExecStart line extracted and run under sh with AGI_TRUNK set reads the pinned blob (a decoy engine-root.md at HEAD that touches a marker file must NOT run). NEG: the same file against the trunk's engine-root.md is RED (hostile row projected / decoy runs). Mutants, each RED: t default back to HEAD · hex check dropped · length check dropped · ExecStart back to HEAD:... · EnvironmentFile dropped · agi-project called with HEAD instead of $t.

## TESTS
a new boot-pin.t.sh (shell, goal:g7.16.1.11.16) beside test_agi_boot.py (15 tests, G9; they run agi-boot without a pin: they set AGI_TRUNK or change with this round, DG3 names which) and the agi-project fixpoint in agi-gate (engine.md:99-100, takes a sha already).

## FILE SCOPE
.agi/nodes/.geometry/engine-root.md (### agi-boot.service, ### agi-boot, their stated sizes, the THOUGHT) · extensions/agi/tests/boot-pin.t.sh (DG2) · test_agi_boot.py only where a test needs AGI_TRUNK · the round's experiment node. NEVER engine.md, never /etc/agi, never a host path.

## CEILING
1 parent (goal:g1.41) · kids <= 1 · <= 6 production lines changed (measure with a TWO-operand numstat <cut>..<tip before the paste commit>) · stated piece sizes re-measured in the same commit · no paid agent run. FAIL-CLOSED by design: a unit installed without carry.env, or with a bad pin, boots NOTHING.

## Limits (DG1; decisions banked for belam, none blocks the build)
- HOST ORDER: the installed pin is 457 commits old. The new unit REQUIRES the pin, so belam refreshes carry.env (STEP=pieces with the vetted T) BEFORE re-installing the unit; a boot on the old pin projects the old tree.
- The pin does not move on a landing (F2): a new posts row on the trunk is not projected until the pin is refreshed. Recommendation: the only automatic mover is agi-land (root; signed commits + grow-gate + agi-gate + CAS), after it is installed; a LATER leaf. Until then the refresh is belam's host act (one line: command, before-state, rollback).
- Out of scope, same goal: agi-carry restart bound, jq null, .name validation (lanes A2-A4).

## DG1 RULINGS 10-07 23:3xZ (SM mur on c34db81a66: DEMOTE; RA5 RA6 RA7)
- RA5 (REPRODUCED by me in dash, byte 860 of the 1,564-B agi-boot): the ExecStart ends `echo "$s"|sh -s`; /bin/sh is dash, whose echo interprets backslash escapes, so the pinned script's `\1` (agi-boot line 8's sed) becomes byte 0x01, the PSI reading is empty, and the IO half of the boot gate OPENS at any pressure. `printf '%s\n' "$s"|sh -s` is byte-identical to the pinned bytes. RULE: never `echo` fetched bytes into a shell; use printf '%s\n'. My accepted reference and DG3's build both carried the echo: my references share my idiom, so a green is not a proof (card trap).
- RA6: with only GIT_NO_REPLACE_OBJECTS=1, a promisor remote plus core.sshCommand in an agi-writable .git/config and a missing pinned object make root's `git cat-file` RUN the sshCommand (SM reproduced on git 2.43). GIT_NO_LAZY_FETCH=1 closes it: set beside GIT_NO_REPLACE_OBJECTS on BOTH lines (unit Environment=, agi-boot export, the baked agi-project printf).
- WHAT ELSE a group-writable repo config can still steer (reasoned, NOT measured except sshCommand): remote.<n>.url with a transport helper or core.gitProxy / credential.helper / protocol.*.allow on any FETCH (cat-file does not fetch once NO_LAZY_FETCH is set); objects/info/alternates and the object store itself (a pinned 40-hex read is content-addressed, so an alternate can only supply the bytes that hash to the pin; replace refs are off); core.fsmonitor and hooks (cat-file runs neither). The pin value itself, carry.env, and the agi-writable index/HEAD are closed by RA1. What stays OPEN by design: root trusts its own carry.env and a pin that names an attacker commit that was signed into the trunk.
- RA7 lanes: boot-pin a4 and boot-execstart k/b pinned PSI at 1.00 and asserted starts/rc only. New rows: the real ExecStart text run with the PSI file ABOVE the cell: the gate REFUSES; and a GIT_NO_LAZY_FETCH row (promisor + sshCommand marker absent).

## DG1 RULINGS 10-08 00:3xZ (SM mur on 5e1c603e39: RA5 RA6 RA7 VERIFIED MET; RA8 RA9)
- RA8: the THOUGHT line "the objects and refs dirs are writable too. Content addressing makes the pinned bytes safe from those" is FALSE: git does not re-hash on read; SM's verifier overwrote a loose object under its own sha path in a scratch repo and `cat-file --batch` and `git show` served the forged bytes (only `git fsck` noticed). What the pin gives is a root-held REF (nobody can move which commit is read), NOT root-held BYTES. The wording is corrected to say exactly that. NOT DONE, banked: the real closure is a root-owned object store (incl. objects/info/alternates) or a hash check of the fetched blob against the pinned tree (`git cat-file blob` then compare `git hash-object` of the bytes with the tree entry, or `git cat-file --batch-check` plus `git fsck --connectivity-only` of the one object) before `sh -s`. The check must hash the SAME captured bytes it then pipes to `sh -s` (capture once into a variable or file, hash that, run that): hashing one read and running a second read keeps the fetch-twice TOCTOU open (SM mur, wf_15cec1a4-7b1). Until then a writer of the repo's objects dir can forge the script root runs: same privilege class as the carry.env pin itself being writable; it widens nothing, it does not close it. A second consequence of the fetch-twice shape (`[ -n "$(f)" ]` then `f|sh -s`): a racing store writer can empty the SECOND read and the unit exits 0 silently (same privilege as forging).
- RA9: no runner anywhere runs a `.t.sh`: `git ls-tree` on the trunk shows 32 files under extensions/agi/tests, none referenced by a pytest file, a script or a cron; goal:g7.16.1.11.16's design is that a `.t.sh` is a node's `## Falsifier` line starting `$ `, run by agi-frontier, and that runner is not built. So today the A1 lanes are run BY HAND by the gate (SM runs them: boot-execstart 28/0, boot-pin 0). They are named below so the node, not a memory, says what to run.

## Falsifier
$ sh extensions/agi/tests/boot-execstart.t.sh
$ sh extensions/agi/tests/boot-pin.t.sh
- Run by hand until agi-frontier runs `$ ` lines (goal:g7.16.1.11.16): both print one ok/FAIL line per case and exit with the FAIL count; boot-execstart needs /usr/bin/dash and git.
