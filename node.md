---
id: hypothesis:g716111-g9-boot-install-brings-the-boot-set-up
mint_id: 11ec0aa84c9145818470ead84bff1ecf
type: hypothesis
parents:
  - goal:g7.16.1.11.10
next_edges: []
edited_by: director-general-3
scaffold_hash: bff9a8a3a86c71ee
season: 2
testable_claim: after a reboot agi-boot.service re-applies the agi-ram ACLs, projects the local trunk, and starts only the boot-flagged v5 rows one at a time behind the load and io gate
title: "G9: one root boot unit brings the boot-set v5 posts up after a reboot with no hand act"
town: core
---
# hypothesis:g716111-g9-boot-install-brings-the-boot-set-up

## Measured
- OWNER 17:5xZ 10-01 (verbatim on goal:g7.16.1.11 @bd53e5b0e): boot = local-trunk projection now (the signed seed waits for the iPhone app); auto-start ONLY belam (fresh, v5) + the core council (alive, all-is-one, self-perpetuating) + thought-master-new + director-thought-1 + sanctuary-master + director-general-1; a Proxmox mock restart FIRST, then ONE real reboot with the old belam resumed on the old setup as the look-over.
- belam -> DG3 18:1xZ (direct session message): ROUND G9 = the boot install; install only after G7 (pi start fix) lands.
- Today every reboot (14:42Z) needed hand acts: /run wiped (unit template, drop-ins, wants dir), the /mnt/agi-ram ACLs gone, then one hand start per post behind the load / io gate (DG3 card traps: reboot wipes, start gate).
- agi-ram-main.service (/etc, oneshot, RemainAfterExit) brings the RAM tier up; engine-root.md:22 already orders agi-post@ After= it.
## CLAIM
One root unit agi-boot.service (its text a section in engine-root.md, installed once into /etc/systemd/system, After= + Requires= agi-ram-main.service) brings every boot-set v5 post up after a reboot with NO hand act: it re-applies the /mnt/agi-ram ACL pair, projects the engine from MAIN's LOCAL trunk into /run/systemd/system, daemon-reloads, then starts ONLY the projected rows whose config:posts boot cell is true, ONE at a time behind the gate (load1 < 16 AND io PSI some avg60 < 50).
## Dispatch line
Kid answers FIRST: which existing pieces it reuses (the agi-project section and the gate numbers -- where do they live as cells?), how the start loop waits on the gate without busy-spinning and with a bound, and how a row that is projected but not boot-flagged stays down.
## FALSIFIERS
- F1 after a (mock) reboot a boot-set v5 post is not active with no hand act.
- F2 an agi-* user cannot reach /mnt/agi-ram/worktrees (g:agi x on /mnt/agi-ram) or CAN read /mnt/agi-ram/state (g:agi --- there).
- F3 a projected row without boot: true is started, or two starts overlap, or a start fires while load1 >= 16 or io PSI some avg60 >= 50.
- F4 the unit text lives anywhere but one geometry section (a second copy in a script or a doc).
## TESTS
rows that run the extracted boot piece under sh with fakes on PATH (setfacl, systemctl, cat of /proc/loadavg and /proc/pressure/io via env-pointed files): the ACL pair is applied; projection runs from the local trunk ref; only boot-true rows get one start each, in order, never two at once; a high load or io reading delays the next start and a bound gives up by name; the unit text carries After= + Requires= agi-ram-main.service and Type=oneshot. No real systemd, no real reboot in CI.
## FILE SCOPE
.agi/nodes/.geometry/engine-root.md (### agi-boot.service + ### agi-boot sections) · .agi/nodes/.geometry/posts.md (a boot cell on the owner's boot-set rows ONLY) · the gate numbers as cells (config.json or engine.md, one place) · one test file · this node.
## CEILING
production +25 lines (two sections + cells) · tests +80 · Sonnet 5.5 subagent · 0 USD. INSTALL (sudo, /etc) is the director's act after G7 lands and belam's GO; Proxmox mock first.

## RESULT G9 (kid afcd4e53d + trunk merge 6017fcbc6, director record)
engine-root.md gains ### agi-boot.service + ### agi-boot; posts.md boot:true on the owner's 8 rows; config cell values.local_maxxing.agi_boot {poll_s, wait_max_s}; gate numbers read from de_live_parents.ceiling_if. NUMSTAT 0e28707f3..afcd4e53d: config.json 1/0 · engine-root.md 31/0 · posts.md 8/8 · test_agi_boot.py 87/0 (production +32 vs +25: disclosed override, the 8 row flags). Trunk merged in (posts.md resolved = trunk rows + the 8 flags, diff-verified). 27 passed. mur-de-base-g9: review accept_with_residue · verify DEMOTE.
RULING (belam 18:2xZ): boot projects only engine.v==4 rows; old-setup rows come back via heal until their own move; the flags stay on all 8 -- the verify's 'boot set cannot start' is the designed state, but the skip must be NAMED and tested.

## CORRECTIVE G9.2 -- closes mur-de-base-g9 g9-code (verify D1 D2 D4 + missed a b + config_max; D3 refuted; D5 = the record above)
BASE      CUT FROM de-base-G9 tip (6017fcbc6 + this node write). No merge. Never rebase.
1. (D1) the gate is fail-OPEN on an unreadable/empty loadavg (l empty -> awk 0). TRUE WHEN a missing or empty load reading keeps the gate CLOSED exactly like io; a row proves it.
2. (D2) test_high_reading_delays_next_start flakes (5 of 8): the fixture's wait_max_s=1 vs the integer-second bound. TRUE WHEN the row is deterministic (bound and poll chosen so the delay is observed and the start still happens, e.g. flip the reading file mid-wait or use a bound far above the poll); run the file 8x, 8 green.
3. (D4) setfacl and daemon-reload failures are silent. TRUE WHEN each failure prints a named stderr line, boot CONTINUES (posts still start), and the unit's final exit is non-zero so systemd shows the boot as failed; a row with a failing fake setfacl asserts the line, the starts, and the exit.
4. (missed a+b) a boot-flagged row with no projected wants link is skipped with a NAMED stderr line ('agi-boot: <p> not projected (engine v4 row absent), skipped'); a fixture row WITHOUT engine.v==4 proves the line and that it is not started.
5. (config_max) drop the AGI_TRUNK literal from the unit: the piece and its config are read from MAIN's checked-out HEAD (MAIN never switches branches; it IS the local trunk). WorkingDirectory stays the one install-time literal (systemd needs it; it is written at install from the agi-project service's own toplevel). The shell's test-override defaults stay.
DEMOTED   D3 refuted by verify (the wants dir is /run tmpfs, wiped at boot) · a dedicated boot ceiling cell vs reusing de_live_parents.ceiling_if: kept shared, one source, the owner's numbers are the same.
FILE SCOPE .agi/nodes/.geometry/engine-root.md (the two agi-boot sections) · extensions/agi/tests/test_agi_boot.py.  CEILING production net +4 · tests +40 · Sonnet 5.5 subagent · 0 USD.

## RESULT G9.2 (kid 79f05922f, director record)
loadavg fail-closed (l reset each pass) · deterministic delay row (fake sleep flips the reading; 8 runs, 0 fails) · setfacl / daemon-reload failures named, boot continues, exit non-zero · a named skip for a boot row with no projected wants link · no AGI_TRUNK literal (ExecStart reads HEAD of MAIN). NUMSTAT a3e1f655e..79f05922f: engine-root.md 9/8 · test_agi_boot.py 35/11. 11 passed x3 (director), x8 (verify). mur-de-base-g9b: review + verify accept_with_residue.

## CORRECTIVE G9.3 -- closes mur-de-base-g9b g9b-code (D1 + verify missed a b; D4 D5)
BASE      CUT FROM de-base-G9 tip (79f05922f + this node write). No merge. Never rebase.
1. (D1 + missed b) the start loop is a piped while (a subshell): a failed systemctl start AND a gate give-up both print a named line but cannot set e, so the unit exits 0. TRUE WHEN the boot rows are collected first (rows=$(...)) and iterated in the MAIN shell (for p in $rows -- names carry no spaces), so a failed start or a give-up sets e and the final exit is non-zero; rows: a failing fake start -> named line + exit non-zero + the next row still started; a give-up -> exit non-zero.
2. (missed a) a SECOND loadavg read that fails after a good first read must not reuse the stale value: a row whose load file is valid-low on the first ok() call and then removed/emptied asserts the gate stays CLOSED (the start is skipped by name at the bound).
3. (D4) the fake systemctl regains a start duration (e.g. sleep 0.1 inside start) so the no-overlap order row means something.
4. (D5) drop the dead imports.
DEMOTED   path defaults /mnt/agi-ram and /run/systemd/system = env-overridable defaults of a root unit, read nowhere else (no second source) · WorkingDirectory fidelity = an install-time check (the director installs from the projection and reads it back) · 'MAIN never switches branches' = a standing rule (the HEAD) not a code property · RESULT + THOUGHT = the director's (above; engine-root THOUGHT rewritten with this write).
FILE SCOPE .agi/nodes/.geometry/engine-root.md (### agi-boot) · extensions/agi/tests/test_agi_boot.py.  CEILING production net +2 · tests +30 · Sonnet 5.5 subagent · 0 USD.

## RESULT G9.3 (kid 69e9cd1d9 + trunk merge 7172cc8ff, director record)
Start loop in the MAIN shell (rows collected first): a failed start or a gate give-up sets e, exit non-zero, the next row still tried · a second failed load read keeps the gate closed (row) · the fake start has a duration again · dead imports gone · engine-root THOUGHT rewritten IN THE KID'S COMMIT (write.py refuses a director THOUGHT on config:*). NUMSTAT 5df4b9203..69e9cd1d9: engine-root.md 5/6 · test_agi_boot.py 17/3. 13 passed x8 (kid), x2 (director); trunk merged (posts.md = trunk + the 8 boot cells, diff-verified), merge-tree rc 0. mur-de-base-g9c: review + verify accept_with_residue.

## CORRECTIVE G9.4 -- closes mur-de-base-g9c g9c-code (D1)
BASE      CUT FROM de-base-G9 tip (7172cc8ff + this node write). No merge. Never rebase.
1. (D1) rows=$(git show ...posts.md|sed|jq) is unchecked: a missing posts.md at the ref, a sed miss or a jq error starts nothing and exits 0. TRUE WHEN a failed extraction OR an empty boot list prints a named stderr line ('agi-boot: no boot rows read from <ref>') and sets e=1 (the unit exits non-zero); rows: posts.md absent at the ref -> the line + exit non-zero; a posts.md with no boot:true row -> the line + exit non-zero.
DEMOTED   unquoted for p in $rows: post names are [a-z0-9-] (the posts schema), no whitespace or glob can occur · the round outcome as a verdict + evidence_runs = the merge pass / the director's RESULT records (this node's convention).
FILE SCOPE .agi/nodes/.geometry/engine-root.md (### agi-boot) · extensions/agi/tests/test_agi_boot.py.  CEILING production net +1 · tests +15 · Sonnet 5.5 subagent · 0 USD.

## RESULT G9.4 (kid 51642395e + trunk merge 42538e87b, director record) -- G9 residues 0
An unreadable or empty boot-row list is named ('agi-boot: no boot rows read from <ref>') and sets e=1. NUMSTAT 66618dd1c..51642395e: engine-root.md 3/3 (rows line, size header, THOUGHT line) · test_agi_boot.py 10/0. 15 passed (kid x5); trunk merged again (posts.md = trunk + the 8 boot cells, diff-verified), 33 passed, merge-tree rc 0. mur-de-base-g9d: review + verify accept_with_residue, the clause confirmed sound by mutation.
DEMOTED by reason: a boot where every flagged row is unprojected exits 0 = belam's ruling (flags stay on all 8 until each move; every skip is named and tested) · zero boot flags failing the unit = not a legal state under the owner's boot set, so loud is right · no 'boot continues after an empty list' row = the ACL pair and the projection run BEFORE the row read, nothing follows it to continue.
CHAIN: G9 afcd4e53d -> G9.2 79f05922f -> G9.3 69e9cd1d9 -> G9.4 51642395e; murs g9 (demote) -> g9b -> g9c -> g9d accept_with_residue, closed in-loop. INSTALL = the director's act after belam's GO + the owner's Proxmox location; Proxmox mock FIRST.

## RESULT G9 MOCK (belam GO 20:3xZ 10-01; director record) -- a systemd container, NO Proxmox (host = Ubuntu 24.04, SVM disabled by BIOS: no KVM)
```
CONTAINER  privileged docker, ubuntu:24.04 + systemd as PID 1, memory 1.5 GB (swap 0 extra), --network none, its OWN tmpfs /run + /mnt/agi-ram,
           a depth-1 clone of the trunk at eb0247358 (contains G9 0b8f086a5) bound READ-ONLY at /data/work/agi; never MAIN, the real /mnt/agi-ram or /etc
           packages via a host-network SETUP container committed to a local image (the docker bridge has no outbound: apt hung 2x)
INSIDE     /etc: agi-boot.service = the ONE engine-root.md section extracted at HEAD (F4) · a MOCK agi-ram-main (host modes 710/755/775, no ACLs)
           · FAKES (labelled): /opt/agi/bin/pi (the projection needs a pi on the unit PATH while a pi row is on the box) · agi-post@ drop-in
           ExecStart = sleep (no claude), the key/worktree ExecStartPre dropped (trunk is ro), the memory-PSI ExecStartPre kept · users agi-<p> in g:agi 984
BEFORE     reboot: projected 0 · active 0 · /mnt/agi-ram empty · gate at start: load1 1.98, io avg60 2.83
REBOOT     docker restart 20:58:48Z -> agi-boot Finished 20:58:49Z, Result success, exit 0
F1 HOLDS   6/6 projected boot rows active, no hand act: all-is-one · self-perpetuating · alive · director-general-1 · thought-master-new · director-thought-1
F2 HOLDS   /mnt/agi-ram g:agi --x · state g:agi --- (re-applied after the wipe) · agi-alive: cd worktrees OK · ls state DENIED · ls /mnt/agi-ram DENIED
F3 HOLDS   5/5 projected NON-boot rows inactive (director-general-2 -4 -5, director-thought-2, stream-master) · 2 named skips: belam, sanctuary-master
           ('not projected (engine v4 row absent)') · starts sequential in posts.md order, ~13 ms apart · gate open throughout (cells 16/50)
RESIDUE    the gate reads load1 + io avg60, which cannot see a start 13 ms old: 6 REAL claude posts would boot inside ~0.1 s (the 12:58Z trap: 4 starts
           3-4 min apart already drove io PSI 88) -> a spacing cell between starts (findings row 89) · the projection also links every projected post
           + agi-project.path into multi-user.target.wants under /run: harmless at boot (the transaction is already built), but an isolate / target
           restart after boot would start the NON-boot rows (row 89)
TEARDOWN   container + setup container removed · images agi-g9-mock-img:local + ubuntu:24.04 removed · clone removed · host: docker images 5 = 5,
           containers 4 = 4, volumes 2 = 2, networks 3 = 3, systemd-container not installed, lxd snap 0, /etc agi-boot 0 -- after == before
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
G9 MOCK version (belam GO 20:3xZ 10-01). OWNER 20:2xZ verbatim: "You can install proxmox on this box yourself as needed". MEASURED by belam 20:2xZ: host = Ubuntu 24.04 (Proxmox VE installs on Debian only), SVM DISABLED BY BIOS (no KVM). OWNER CHOICE 20:3xZ verbatim (asked with 4 options): "systemd container mock" -- no Proxmox. So the CLAIM was exercised in a privileged docker container with systemd as PID 1 instead of a Proxmox VM: same agi-boot.service bytes (extracted from the one engine-root section at the trunk tip), a mock agi-ram-main, and sleep-faked posts. F1 F2 F3 held on the first mock reboot. Near miss: the docker bridge has no outbound, so packages came from a separate host-network setup container committed to a local image, and the mock itself ran with --network none. Not yet proven: real claude posts behind the gate (the ~13 ms start spacing is the open residue). The real /etc install and the ONE real reboot each wait for a separate belam GO.
<!-- THOUGHT:END -->
