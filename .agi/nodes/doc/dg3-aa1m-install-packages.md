---
id: doc:dg3-aa1m-install-packages
mint_id: d18ff1d70e814e3383b58a515b21a1b7
type: doc
parents:
  - goal:g7.16.1.11.11.1
next_edges: []
edited_by: director-general-3
season: 2
title: "AA1.M INSTALL PACKAGES for belam's GO, one per act: pieces + carry.env, signers, the signers wiring, the 4 carrier units, the coalescing probe, host act 1 re-run, first real delivery, a 2nd box LAST. DRAFT: nothing here has been run on the host"
tags:
  - aa1m
  - host-act
  - install
  - g7.16.1.11
town: core
---
# doc:dg3-aa1m-install-packages

Author director-general-3, 10-02, on SM's order (21:1xZ): "DRAFT the install packages now, as ONE doc node ... RUN NOTHING ... a nodes-only merge-up AFTER DG1's level round lands (the a() bytes the packages name must be the landed ones). Each act then goes to belam as ONE line via me for its own GO." belam 21:1xZ: "send ONE line (via SM or DG1) with the unit files' path + sha256, the exact command, before-state, one-command rollback; belam reads every unit whole before the GO." The scripts below were dry-run ONLY into scratch dirs (OPT/ETC/SYSD under /tmp, NOSYSTEMCTL=1); no root act, no host file touched.

## Blockers (SM's letters)
| | blocker | state 21:2xZ |
|---|---|---|
| (a) | AA2 per-post stores `/var/lib/agi/<p>/g.git` (goal:g7.16.1.11.12): the carrier moves refs BETWEEN them | OPEN: no store exists on the box; the units and probes wait fine without (host act 2b GHOST), no DELIVERY before |
| (b) | DG1's level round replaces `a()` in the `box` piece | CLEARED: landed 3a33c71b9 (box 2,005 B, the level a()); the sha256 below is the LANDED piece; re-print it at the GO if the trunk moves again |
| (c) | belam's cells | CLEARED: box.alias = "local-town", box.hub = "" (059414660), box.repo = "/data/work/agi" (12e8065cc) |

## The order
```
A0 read-only checks (no GO) ─▶ A1 pieces + carry.env ─▶ A2 signers ─▶ A3 wiring round (build, then regen) ─▶ A6 host act 1 re-run
                                   │                                       
                                   └─▶ A4 units (12 path instances) ─▶ A7 first real delivery (needs (a))  ─▶ A8 2nd box LAST (needs box.hub)
A5 coalescing probe: scratch, any time, independent
```
Every act = ONE belam GO. The line sent via SM: `[host-act] <Ax>: run as root: <command>; before: <state>; rollback: <one command>; read whole: <path + sha256>`.

## Scripts (committed on the trunk with this node; belam reads each whole)
| file | bytes | sha256 |
|---|---|---|
| .agi/context/local-maxxing/aa1m/aa1m-install.sh | 2157 | 7c8a3e82b421dadf8f4dcf548e698f35a3b710504657c2a70ec522972874f5d8 |
| .agi/context/local-maxxing/aa1m/aa1m-probe5.sh | 1453 | bf58294d9c21c695792db21d646b57c327297988d2869d1e41fb6f030d3cbb2e |
It reads ONLY the pinned trunk sha T (a 40-hex sha; a post-writable ref or a replace object changes nothing), runs `git` in the box repo with safe.directory via env, writes `/opt/agi/bin`, `/etc/agi`, `/etc/systemd/system`, never a post's home. Needs `REPO=<the box repo>` and REFUSES unless it equals the cell `box.repo` at T (belam 12e8065cc: "/data/work/agi"); AGI_REPO and safe.directory in carry.env come from that cell, never from box.root (finding F1).

## Piece and unit bytes (sha256 of the extracted piece = what the step prints; trunk 3a33c71b9, the level round LANDED)
| piece | sha256 |
|---|---|
| box (2,005 B) | 71d37bf835a7e0fa768cc06413c174568b4dbfa85e754acc4c3f363b0fc33501 |
| box-carry | 76e189d487e53a39b5d9f7cac7d90afa089b33af407066e12d67bc5fd86592db |
| agi-signers | 5f337eed7b3208f622803f9fbe07afdf04ce278d0f2c05e11f621d44e1953c66 |
| sect | ebb669a1a4f94ceb082814347f2585eba36162fd826140cab19f3d159aae91e9 |
| agi-carry@.path | 9bf0c59e9a77f9c38d77fef3fdef089c31a1f4dbbffd34c0d2ff50a34a9f4a45 |
| agi-carry@.service | 3a648c6334527d9d425b3aca509cb363882df4be497804ebd8d55234d872cc1b |
| agi-carry-fetch.timer | 0e647e34e5af9cdc622afba480bfd644ab45a890644c6b3cda6ecfdf0ac068bb |
| agi-carry-fetch.service | 3aa54edd7cc31fbd1db83236e0b4e3dce1069e3bd36bdee6d89e708427cad383 |
(`box` is the trunk piece `### box` in engine-post.md; the others are in engine-root.md; box-carry calls `sect box <T>` for a(), so root needs `sect` on PATH: it is installed here.)

## The acts
Common prefix, as root (R = the box repo, T = the landing sha belam names): `echo "<sha256 of the script>  $R/.agi/context/local-maxxing/aa1m/aa1m-install.sh" | sha256sum -c - && REPO=$R sh $R/.agi/context/local-maxxing/aa1m/aa1m-install.sh <STEP> <T>`.
| act | what | before-state | rollback (ONE command) | expected reading | blockers |
|---|---|---|---|---|---|
| A0 | read-only: `ls /opt/agi/bin /etc/agi; systemctl list-unit-files 'agi-carry*' \| wc -l; ls -l /proc/1/fd \| grep -c anon_inode:inotify; ls -d /var/lib/agi/*/g.git` | n/a | n/a | /opt/agi/bin = claude pi; /etc/agi absent; 0 carry units; inotify count N (then A4 adds 12 of max_user_instances 128); no g.git | none |
| A1 | STEP=pieces: box (2,005 B), box-carry, agi-signers, sect -> /opt/agi/bin; /etc/agi/carry.env (AGI_BOX AGI_HUB AGI_REPO AGI_TRUNK GIT_CONFIG_VALUE_0) | /opt/agi/bin lacks them; /etc/agi absent | `rm -f /opt/agi/bin/box /opt/agi/bin/box-carry /opt/agi/bin/agi-signers /opt/agi/bin/sect /etc/agi/carry.env; rmdir /etc/agi` | 4 sha256 lines equal the table above; carry.env: AGI_BOX=local-town, AGI_HUB= (empty), AGI_REPO=/data/work/agi (= box.repo), GIT_CONFIG_VALUE_0 the same, AGI_TRUNK=T | none open ((b) and (c) cleared) |
| A2 | STEP=signers: `agi-signers <p>` for the 12 v5 rows of this box -> /var/lib/agi/allowed_signers (root, 0644, append-only) | file absent | `rm -f /var/lib/agi/allowed_signers /var/lib/agi/allowed_signers.lock` | `wc -l` = 12; one line per post `<p>@agi namespaces="git",valid-after="<now>" ssh-ed25519 AAAA...`; a re-run prints no new line (idempotent). NB valid-after = the install time: OLD history does not verify against this file, by design | after A1 |
| A3 | the WIRING = a BUILD ROUND (not a host act), then the existing genome regenerates the post unit: (i) gitconfig `allowedSignersFile=~/.signers` -> `/var/lib/agi/allowed_signers` (ii) agi-post@.service gains `ExecStartPre=+/opt/agi/bin/agi-signers %i` BEFORE the user ExecStartPre (iii) retire `mkdir -p t/.agi/keys;cp .ssh/id_ed25519.pub t/.agi/keys/%i` and `cd t;signers>../.signers`, and the `signers` piece (finding F4). Each post then restarts under belam's move procedure | trunk without the commit | revert the trunk commit (agi-project regenerates the old unit); delete nothing | a restarted post: `git verify-commit` of its own next commit prints Good for `<p>@agi`; no new file under .agi/keys after its Stop hook | A2 first (every key in the file BEFORE the flip); a hypothesis to place: DG1 |
| A4 | STEP=units: the 4 unit files -> /etc/systemd/system, daemon-reload, `enable --now agi-carry@<p>.path` for each of the 12 rows; the fetch timer ONLY if box.hub is non-empty | no agi-carry* unit | `sh -c 'for u in $(systemctl list-units --all --plain --no-legend "agi-carry@*.path" \| cut -d" " -f1);do systemctl disable --now $u;done;systemctl disable --now agi-carry-fetch.timer 2>/dev/null;rm -f /etc/systemd/system/agi-carry*;systemctl daemon-reload;systemctl reset-failed;:'` PROOF: `systemctl list-units --all --no-legend "agi-carry*" \| wc -l` = 0 | 4 sha256 lines equal the table; 12 x `agi-carry@<p>.path active waiting`; inotify = before + 12; `hub empty: fetch timer not enabled`; NO service run until a store ref changes (journal empty) | after A1; delivery needs (a) |
| A5 | the coalescing probe: `sh aa1m-probe5.sh` (scratch /tmp/m5, throwaway units in /run) | no /tmp/m5, no agi-act5 unit | the script prints its own one-line ROLLBACK | `COALESCE ... starts=2` = systemd runs the oneshot again for events during a run; `starts=1` = those events are LOST (then the carrier's re-scan + exit 75 + Restart=on-failure is the only cover) | none; any time |
| A6 | host act 1 RE-RUN: alive's act1.sh (sha256 90cdb304cfd265d41980eadf6b7e8552b1153e8dbe43cadfb107520b9d84a1ca, alive to commit it under aa1m/) | /tmp/m1 absent | `rm -rf /tmp/m1` | `CARRIED hello-m1 G` (was U) and `BARRIER HOLDS` | A2 + A3 (the receiver verifies with its own gitconfig file) |
| A7 | first real delivery: one `box send` by a post, its path unit fires, `box read` by the recipient | no ref in the recipient store | delete the one ref in the recipient store | `journalctl -u agi-carry@<p>` = 1 run; `box read` prints the message in the RECIPIENT's own store; no file under .agi/sessions/inbox | A4 + (a) |
| A8 | a 2nd box LAST: box.hub set by belam, a remote head, the fetch timer on both boxes | one box | remove the remote + disable the timer | a send by a post on box 1 is read on box 2 and the reply returns (alive B4) | (a) + box.hub + belam on box 2 |

## Findings and bank
- F1 RESOLVED by belam 12e8065cc: the NEW cell `box.repo` = "/data/work/agi" is the install's repo (AGI_REPO + safe.directory); `box.root` ("/home/ubuntu/work/agi", not a path on this box) STAYS because it is a [box].md field the paths check scans as a leak literal. What the leak scanner should look for on this box is a finding for DG1 to place, not for this install. The script refuses a REPO that is not box.repo at T.
- F2 carry.env pins AGI_TRUNK at install: a landing does not move it. Re-running STEP=pieces with the new T refreshes it; the tick that does it automatically is a later round.
- F3 the 12 rows include director-general-4 and director-general-5 (down by the owner's word): their path units wait harmlessly (+2 inotify). No row marker says down; none invented here.
- F4 root cause of public-key blobs in history: the post unit copies ~/.ssh/id_ed25519.pub into t/.agi/keys/<p> and the Stop hook's `git add -A` (row 94) commits it, comment field included. A3 retires the copy; until then cut every merge-up from a trunk worktree.
- F5 a() is installed with the `box` piece: re-run both test files before A1 whenever the trunk moves (on 3a33c71b9: box-mail.t.sh 63 ok 0 FAIL, box-carry.t.sh 44 ok 0 FAIL).
