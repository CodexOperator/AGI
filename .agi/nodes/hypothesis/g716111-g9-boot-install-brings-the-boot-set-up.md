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
