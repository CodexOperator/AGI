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
