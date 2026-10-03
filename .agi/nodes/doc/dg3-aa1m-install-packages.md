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
| .agi/context/local-maxxing/aa1m/aa1m-install.sh | 2649 | bf6e0bc1deb3cd469c169f830cb289f1b9e04e8e93b005a17797995f340c19a2 |
| .agi/context/local-maxxing/aa1m/aa1m-probe5.sh | 1547 | a5d7d1842a7188f0e3800c813a1d9c7c9e19c47aecbe4e4988b7e2aecb3d3e91 |
It reads ONLY the pinned trunk sha T (a 40-hex sha: a short sha exits 1; a post-writable ref or a replace object changes nothing) and is run FROM T (`git show T:<path> >f && sha256sum f && sh f`: a failed show cannot run an empty script), so the script bytes are the bytes at T, never the working tree. It runs `git` in the box repo with safe.directory via env, writes `/opt/agi/bin`, `/etc/agi`, `/etc/systemd/system`, never a post's home. It REFUSES unless REPO equals the cell `box.repo` at T, and REFUSES any box cell holding a character outside [A-Za-z0-9._/:@-] or starting with `-` (a cell is written UNQUOTED into carry.env, safe only because of that charset gate, and carry.env is never sourced). The scratch overrides are AGI_DRY_* plus AGI_STORES and are refused when uid is 0.

## Piece and unit bytes (sha256 of the extracted piece = what the step prints; trunk 21629a697 + the closer: the level round, A3.2 and A3.4 LANDED; the `box` piece is unchanged since 3a33c71b9, the `box-carry` row is the CLOSER's piece (dg3-lost-wake) and equals the trunk's bytes only once the closer lands: re-print it at the GO)
| piece | sha256 |
|---|---|
| box (2,005 B) | 71d37bf835a7e0fa768cc06413c174568b4dbfa85e754acc4c3f363b0fc33501 |
| box-carry (3,246 B: the --fetch sweep) | 56cd92155310622cfaaf3153ea44a42882500e92a78734a90879d89b6498bec4 |
| agi-signers (1,727 B: PATH line + bounds, A3.2) | 6b9df8d919d70b6c4ecb4968b708950795ff846cb4be09f5bf51ceee2d9d9915 |
| sect | ebb669a1a4f94ceb082814347f2585eba36162fd826140cab19f3d159aae91e9 |
| agi-carry@.path | 9bf0c59e9a77f9c38d77fef3fdef089c31a1f4dbbffd34c0d2ff50a34a9f4a45 |
| agi-carry@.service | 3a648c6334527d9d425b3aca509cb363882df4be497804ebd8d55234d872cc1b |
| agi-carry-fetch.timer | 0e647e34e5af9cdc622afba480bfd644ab45a890644c6b3cda6ecfdf0ac068bb |
| agi-carry-fetch.service | 3aa54edd7cc31fbd1db83236e0b4e3dce1069e3bd36bdee6d89e708427cad383 |
(`box` is the trunk piece `### box` in engine-post.md; `sect` is in engine.md; the others are in engine-root.md; box-carry calls `sect box <T>` for a(), so root needs `sect` on PATH: it is installed here.)

## The acts
Common GO line, as root (R = the box repo; T = the FULL 40-hex sha of the landing that carries this node and the script, named by belam: the sha is the pin AND the script's bytes). Compare the bytes first: `git -C $R show T:.agi/context/local-maxxing/aa1m/aa1m-install.sh | sha256sum` = the table. Then: `f=$(mktemp) && git -C $R merge-base --is-ancestor T local-maxxing/season2/main && git -C $R show T:.agi/context/local-maxxing/aa1m/aa1m-install.sh >$f && sha256sum $f && REPO=$R sh $f <STEP> T`. Every act line below shows `<T40>` = that full sha; a GO line carries it spelled out.
| act | what | before-state | rollback (ONE command) | expected reading | blockers |
|---|---|---|---|---|---|
| A0 | read-only: `ls /opt/agi/bin /etc/agi; systemctl list-unit-files 'agi-carry*' \| wc -l; ls -l /proc/1/fd \| grep -c anon_inode:inotify; ls -d /var/lib/agi/*/g.git` | n/a | n/a | /opt/agi/bin = claude pi; /etc/agi absent; 0 carry units; inotify count N (then A4 adds 12 of max_user_instances 128); no g.git | none |
| A1 | STEP=pieces `<T40>`: box (2,005 B), box-carry, agi-signers, sect -> /opt/agi/bin; /etc/agi/carry.env (AGI_BOX AGI_HUB AGI_REPO AGI_TRUNK GIT_CONFIG_VALUE_0) | /opt/agi/bin lacks them; /etc/agi absent | `rm -f /opt/agi/bin/box /opt/agi/bin/box-carry /opt/agi/bin/agi-signers /opt/agi/bin/sect /etc/agi/carry.env; rmdir /etc/agi` | 4 sha256 lines equal the table above; carry.env: AGI_BOX=local-town, AGI_HUB= (empty), AGI_REPO=/data/work/agi (= box.repo), GIT_CONFIG_VALUE_0 the same, AGI_TRUNK=T | none open ((b) and (c) cleared) |
| A2 | STEP=signers `<T40>`: `agi-signers <p>` for the 12 v5 rows of this box -> /var/lib/agi/allowed_signers (root, 0644, append-only) | file absent | `rm -f /var/lib/agi/allowed_signers /var/lib/agi/allowed_signers.lock` | `wc -l` = 12; one line per post `<p>@agi namespaces="git",valid-after="<now>" ssh-ed25519 AAAA...`; a re-run prints no new line (idempotent). NB valid-after = the install time: OLD history does not verify against this file, by design | after A1 |
| A3 | the WIRING = a BUILD ROUND (not a host act), then the existing genome regenerates the post unit: (i) gitconfig `allowedSignersFile=~/.signers` -> `/var/lib/agi/allowed_signers` (ii) agi-post@.service runs, in order, the awk gate, the user KEY STEP (`mkdir -p .ssh;...ssh-keygen`, so a first start has a key), then `ExecStartPre=+/usr/bin/env -i PATH=/usr/sbin:/usr/bin:/bin /opt/agi/bin/agi-signers %i` (root, clean env: a post-planted bin/ is never on its PATH), then the rest of the user line (iii) retired `mkdir -p t/.agi/keys;cp .ssh/id_ed25519.pub t/.agi/keys/%i` and `cd t;signers>../.signers`, and the `signers` piece (finding F4); LANDED as A3.2 (63e5d65ae, DEMOTE D1 closed both ways by mur dg3-a3-signers-c). Each post then restarts under belam's move procedure | trunk without the commit | SM (the trunk writer) runs `git -C $R revert --no-edit <the full sha of the wiring commit>` and lands it; agi-project regenerates the old unit; PROOF `git -C $R show local-maxxing/season2/main:.agi/nodes/.geometry/engine-root.md \| grep -c 'agi-signers %i'` = 0 | a restarted post: `git verify-commit` of its own next commit prints Good for `<p>@agi`; no new file under .agi/keys after its Stop hook | A2 first (every key in the file BEFORE the flip); a hypothesis to place: DG1 |
| A4 | STEP=units `<T40>`: the 4 unit files -> /etc/systemd/system, daemon-reload, `enable --now agi-carry@<p>.path` for each of the 12 rows; the fetch timer ALWAYS (the --fetch pass sweeps every local post first, so on a hub-less box it is the lost-wake closer; its hub step exits at once when box.hub is empty) | FIRST install: no agi-carry* unit. RE-RUN after the earlier hub-gated A4: the 4 unit files and the path units are present, agi-carry-fetch.timer is absent | `sh -c 'for u in $(systemctl list-units --all --plain --no-legend "agi-carry@*.path" \| cut -d" " -f1);do systemctl disable --now $u;done;systemctl disable --now agi-carry-fetch.timer 2>/dev/null;rm -f /etc/systemd/system/agi-carry*;systemctl daemon-reload;systemctl reset-failed;:'` PROOF: `systemctl list-units --all --no-legend "agi-carry*" \| wc -l` = 0 | 4 sha256 lines equal the table; 12 x `agi-carry@<p>.path active waiting`; inotify = before + 12; `agi-carry-fetch.timer active waiting` (enabled even with box.hub empty); NO `agi-carry@<p>.service` run until a store ref changes; `agi-carry-fetch.service` (oneshot) runs once at enable and then every 60 s, each run exit 0 with nothing on stderr (journal: one short entry a minute, not empty) | after A1; delivery needs (a) |
| A5 | the coalescing probe: `sh aa1m-probe5.sh` (a fresh mktemp -d under /tmp, throwaway units agi-act5.path/.service in /run) | no /tmp/m5.* dir, no agi-act5 unit | the script prints its own one-line ROLLBACK | `COALESCE ... starts=2` = systemd runs the oneshot again for events during a run; `starts=0` = the unit never fired, INCONCLUSIVE; `starts=1` = those events are LOST (then the carrier's re-scan + exit 75 + Restart=on-failure is the only cover) | none; any time |
| A6 | host act 1 RE-RUN: act1.sh (sha256 90cdb304cfd265d41980eadf6b7e8552b1153e8dbe43cadfb107520b9d84a1ca, 915 B) is ON THE TRUNK at 9778def43 under .agi/context/local-maxxing/aa1m/ and runs from T like the others; waits on A2 + A3 (build 677dacf31, at SM) + belam GO | /tmp/m1 absent | `rm -rf /tmp/m1` | `CARRIED hello-m1 G` (was U) and `BARRIER HOLDS` | A2 + A3 (the receiver verifies with its own gitconfig file) |
| A7 | first real delivery: one `box send` by a post, its path unit fires, `box read` by the recipient | no ref in the recipient store | as root, P = the sender and Q = the recipient belam names, each ref deleted AS ITS OWNER (a store's hooks and config never run as root): `sh -c 'runuser -u agi-P -- git -C /var/lib/agi/P/g.git update-ref -d refs/box/P/Q;runuser -u agi-Q -- git -C /var/lib/agi/Q/g.git update-ref -d refs/box/P/Q;runuser -u agi-Q -- git -C /var/lib/agi/Q/g.git update-ref -d refs/held/Q/P'` (BOTH copies, or the next wake re-delivers) plus A4's rollback if the units go too | `journalctl -u agi-carry@<p>` = 1 run; `box read` prints the message in the RECIPIENT's own store; no file under .agi/sessions/inbox | A4 + (a) |
| A8 | a 2nd box LAST: box.hub set by belam, a remote head, the fetch timer on both boxes | one box | belam sets `box.hub` back to the empty string in config.json, then, as root, with R = the box repo and T2 = the full sha of that config commit on the trunk, SELF-CONTAINED (R, T2 and f are passed into the quoted script as environment, they are not shell variables of the GO line): `R=<the box repo> T2=<the full 40-hex sha> f=$(mktemp) sh -c 'git -C $R show $T2:.agi/context/local-maxxing/aa1m/aa1m-install.sh >$f&&REPO=$R sh $f pieces $T2'` (rewrites carry.env with AGI_HUB empty, so the path-unit carriers stop pushing; box-carry has no remote, it pushes by the URL in AGI_HUB); the fetch timer is KEPT (on a hub-less box its --fetch pass is the lost-wake closer; its hub step exits at once on an empty AGI_HUB); PROOF `systemctl is-enabled agi-carry-fetch.timer` = enabled and `grep AGI_HUB= /etc/agi/carry.env` = `AGI_HUB=` | a send by a post on box 1 is read on box 2 and the reply returns (alive B4) | (a) + box.hub + belam on box 2 |

## Findings and bank
- F1 RESOLVED by belam 12e8065cc: the NEW cell `box.repo` = "/data/work/agi" is the install's repo (AGI_REPO + safe.directory); `box.root` (another box's path; a [box].md field the leak scanner reads) STAYS. What the leak scanner should look for on this box is a finding for DG1 to place, not for this install. The script refuses a REPO that is not box.repo at T.
- F2 carry.env pins AGI_TRUNK at install: a landing does not move it. Re-running STEP=pieces with the new T refreshes it; the tick that does it automatically is a later round.
- F3 the 12 rows include director-general-4 and director-general-5 (down by the owner's word): their path units wait harmlessly (+2 inotify). No row marker says down; none invented here.
- F4 root cause of public-key blobs in history: the post unit copies ~/.ssh/id_ed25519.pub into t/.agi/keys/<p> and the Stop hook's `git add -A` (row 94) commits it, comment field included. A3 retires the copy; until then cut every merge-up from a trunk worktree.
- S-residues of the security mur (dg3-aa1m-install) closed: the script no longer sources carry.env (cells validated, charset-gated and written unquoted: a hostile box.hub is refused, dry-run proven), a failing timer enable now exits non-zero (if/else), the GO line runs the script FROM T with an ancestor check, T is the full sha, A3/A7/A8 rollbacks are exact, A6 is marked BLOCKED, probe5 uses mktemp -d, prints one count and a 0 = inconclusive reading, the dry-run overrides are AGI_DRY_* and refused as root.
- F5 a() is installed with the `box` piece: re-run both test files before A1 whenever the trunk moves (on the merged closer tip with DG2's k9/k11/k12 cases: box-mail.t.sh 63 ok 0 FAIL, box-carry.t.sh 63 ok 0 FAIL: k8 = the lost-wake sweep, k9 = a hung child is bounded, s11 = a planted bin/date is not run, u1 = the root unit line holds env -i).
