---
id: doc:g716111-encryption-town-move
mint_id: 301f75cf757447e38d833fe66e3dfded
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
tags:
  - doc
  - encryption-town
  - g7.16.1.11
model: claude-sonnet-5-5
role: director
scaffold_hash: 7c779e010b6829cd
season: 2
title: "g7.16.1.11 encryption-town: the host act (step 0 + rollback), the NO-RAM-disk shape, the per-post move steps and how mail reaches a moved post tonight (owner 21:2xZ, belam 21:4xZ)"
town: core
---

# doc:g716111-encryption-town-move

Owner 2026-10-08 21:2xZ via belam [order] 21:4xZ: ALL 12 posts move to encryption-town (E) TONIGHT; E's internal drive, NO RAM disk; nothing in flight is cut. Base: doc:g716111-crossbox-plan (§5 root acts, §7 rollback, traps X1-X6). The act is `extensions/agi/guard/host-act-encryption-town.sh`; its lane is `extensions/agi/tests/host-act-encryption-town.t.sh` (the rehearsal under ROOT=<scratch>: no systemd, no root).

## 1 The host act (root on E, ONE command, step 0 first)
`PIN=$(git -C /data/work/agi rev-parse 7b0dd78c7) sh extensions/agi/guard/host-act-encryption-town.sh act` (sudo). Step 0 is the shape of experiment:g141-a1b-host-act-before-state-and-rollback: it copies the before-state of every path it will write aside (`cp -a --parents`, modes and owners kept), snapshots every agi-* path under /run/systemd/system, and writes ONE rollback command (`sh /var/backups/agi-act-<stamp>/rollback.sh`, printed). The act, in the order of the local-town act (vstore file first): /usr/local/libexec/agi-vstore · /etc/agi/carry.env (AGI_BOX=encryption-town, AGI_HUB empty, AGI_REPO=/data/work/agi, AGI_TRUNK=PIN, GIT_CONFIG_VALUE_0=/data/work/agi) · /opt/agi/bin/{sect,box,box-carry,agi-signers} · the four carry units and agi-boot.service · the E drop-in · the polkit rule · agi.slice · daemon-reload · `enable --now agi-carry-fetch.timer` · `enable` + `start agi-boot.service`. Every piece is the pinned commit's section byte for byte (`sect` over the geometry at PIN, never the moving checkout) and its sha256 is printed so belam can compare with L.
**PREREQUISITES the act checks and does not install** (it refuses by name, writing nothing): `pi` at /opt/agi/bin/pi (agi-project exits 3 without it while a pi row has box E; E has no pi: stream L's reviewed tree per crossbox-plan XR2, 207 MiB), claude readable by the agi-* users for the claude rows (crossbox-plan R3), group agi and the agi-<post> users (belam: they exist), setfacl, the clone holding PIN.
**The agi.slice is typed in the script** (config:guard has no E line): MemoryHigh 5G, MemoryMax 6G, oomd kill at 40% on a 7.8 GB box. Each post unit carries MemoryHigh=4G, so 12 posts are capped by the slice, not by their own units: belam confirms the numbers or sets E_MEM_HIGH / E_MEM_MAX / E_OOM_LIMIT before the act.

## 2 The NO-RAM-disk shape (E only, local-town untouched)
agi-boot.service is the pinned text (After= and Requires=agi-ram-main.service stay in the engine bytes). On E a drop-in `/etc/systemd/system/agi-boot.service.d/encryption-town.conf` holds an empty `After=` and an empty `Requires=` (a list setting reset), so the unit starts without agi-ram-main.service, which does not exist on E. agi-boot's two `setfacl` calls target `${AGI_RAM:-/mnt/agi-ram}`: the act creates /mnt/agi-ram and /mnt/agi-ram/state as PLAIN directories on E's drive (no mount, no tmpfs). The post unit's `After=agi-ram-main.service` is ordering only and harmless on a missing unit (crossbox-plan X6). MAIN (/data/work/agi) is the plain clone. No engine byte, no cell, no unit text changes: the rehearsal lane pins that agi-boot.service keeps its Requires line and that MAIN stays clean.

## 3 The per-post move steps (one post at a time, at the post's own [ready])
1. belam, on L: flip the post's row `box` to encryption-town in posts.md (write.py, dry-run first), commit, push the trunk; the post's card is current (its [ready]).
2. On L: `systemctl stop agi-post@P` (ExecStopPost runs agi-flush: the drop, the last turn, the trunk merge); nothing in flight is cut.
3. On E: `git -C /data/work/agi fetch origin local-maxxing/season2/main && git -C /data/work/agi merge --ff-only FETCH_HEAD`, then `PIN=$(git -C /data/work/agi rev-parse HEAD) sh host-act-encryption-town.sh move P` (sudo). It refuses unless the row is box E with engine.v 4 AT the pin; bumps the AGI_TRUNK cell (the old carry.env is kept as carry.env.before-P); starts agi-project.service (the projection); requires the projected wants link and the user; `enable --now agi-carry@<post>.path`; `start agi-post@P`; prints is-active and the ControlGroup.
4. The owner logs the post in (the /login relay); the post resumes from its card. The next post repeats from step 1; a pin bump re-projects every row at once, so the second post onward only re-runs step 3.
Rollback of ONE post: flip its row back, stop it on E (`systemctl stop agi-post@P`, flush runs), start it on L. Rollback of the act: `sh /var/backups/agi-act-<stamp>/rollback.sh`.

## 4 How mail reaches a moved post tonight (belam asked for ONE answer)
FACTS (read from the pieces): a v5 post's mail is the BOX primitive (refs/box/<from>/<to>, carried by root's box-carry between the stores of ONE box, and to another box only through AGI_HUB); belam's carry.env order says AGI_HUB EMPTY, so box mail does NOT cross between L and E tonight. `send.py send` writes the inbox file under the SENDER's MAIN (`.agi/sessions/inbox/<post>.md`, gitignored, per MAIN), and `send.py read --box-local` (the mail_poll reader) skips a foreign-box row by name. `send.py dm` channels are tracked files under .agi/comms and ride the branches (already public on GitHub, like every tracked file).
RECOMMENDATION (GitHub fetch + box read, DMs only): a mail to a post on the OTHER box goes by `send.py dm <post>`; each side runs `git fetch origin && git merge --ff-only` of the comms branch it reads, then `send.py read --box-local --peek` / the post's own `send.py read`; the cost is one push + one fetch of latency, the same as any DM today. Inbox nudges (`send.py send`) and box mail to a post on the other box are NOT delivered tonight and are not queued: the sender sees no ack. Posts that stay on one box keep the local paths unchanged.
ALTERNATIVE (one MAIN only): keep every post's mail on L's MAIN and let E's posts reach it by ssh: refused here, because the only route is L -> E (the mesh key); E has no route to L (GitHub over ssh is refused and E holds no L key), so an E post could not write or read L's MAIN. BANKED for belam: a [decision] if he wants an L-side forwarder instead (a minute loop copying new inbox bytes both ways over the L -> E route), which is a new piece this commit does not build.

## 5 Not covered / UNRUN
systemd itself (the unit verify, the drop-in reset of After= and Requires=, PathChanged on carry.env, enable --now): the rehearsal runs with ROOT= and none of them; `systemd-analyze verify` runs in the real act and refuses with the rollback line. The /login relay and each post's first turn on E. E's pi and claude installs (prerequisites). The slice numbers (belam). A crontab on E: none is written (the owner's scrub note).
