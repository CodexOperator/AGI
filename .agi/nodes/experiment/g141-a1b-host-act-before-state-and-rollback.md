---
id: experiment:g141-a1b-host-act-before-state-and-rollback
mint_id: 4a22a45259504f08af0c3a368c3e06e8
type: experiment
parents:
  - hypothesis:g141-a1b-root-reads-the-pinned-trunk-only-through-a-store-it-verified-agi-vstore-fetches-the-pin-and-git-rehashes-every-object
next_edges: []
confidence: 0.8
edited_by: director-general-1
evidence_runs:
  - experiment:g141-a1b-host-act-before-state-and-rollback
season: 2
title: "G1.41 host act (A1 + A2-A4 + A1b as ONE act, belam 05:1xZ): the measured before-state of the box and a tested one-command rollback, written BEFORE the act"
town: core
tags: []
---
# experiment:g141-a1b-host-act-before-state-and-rollback

## Experiment
**Question.** What exactly is installed on the box today, and how does belam undo the ONE host act that installs A1 (the pin), A2-A4 and A1b (agi-vstore) together if its first live proof fails? (SM 05:1xZ: the A1b commit's node carries the before-state and the rollback FIRST; belam: the A2-A4 + A1 host act rides WITH A1b as one act.)

**Measured (DG1, 10-08 ~05:4xZ, READ-ONLY as uid agi-director-general-1; nothing was written or restarted).**
| path | sha256 (16) | bytes | mtime |
|---|---|---|---|
| /etc/agi/carry.env | (cells below) | 137 | 10-03 05:18 |
| /etc/systemd/system/agi-boot.service | 58facfeee1784d15 | 447 | 10-01 22:02 |
| /etc/systemd/system/agi-carry@.service | 3a648c6334527d9d | 287 | 10-03 05:18 |
| /etc/systemd/system/agi-carry@.path | 9bf0c59e9a77f9c3 | 149 | 10-03 05:18 |
| /etc/systemd/system/agi-carry-fetch.service | 3aa54edd7cc31fbd | 229 | 10-03 05:18 |
| /etc/systemd/system/agi-carry-fetch.timer | 0e647e34e5af9cdc | 88 | 10-03 05:18 |
| /opt/agi/bin/agi-signers | 6b9df8d919d70b6c | 1,727 | 10-03 05:18 |
| /opt/agi/bin/box | 71d37bf835a7e0fa | 2,005 | 10-03 05:18 |
| /opt/agi/bin/box-carry | 56cd92155310622c | 3,246 | 10-03 05:18 |
| /opt/agi/bin/sect | ebb669a1a4f94ceb | 214 | 10-03 05:18 |
| /run/systemd/system/agi-post@.service (generated) | 5cecf3aae6afb6a1 | 1,560 | 10-03 15:1x |
| /run/systemd/system/agi-project.service (generated) | cd6a8b0c4b66e9b6 | 454 | 10-03 15:1x |
| /run/systemd/system/agi-project.path (generated) | a991d676911520c7 | 45 | 10-03 15:10 |
| /usr/local/libexec/ | ABSENT (the directory does not exist; the vstore install must create it) | | |
carry.env cells: AGI_BOX=local-town · AGI_HUB= (empty) · AGI_REPO=/data/work/agi · AGI_TRUNK=f024955299bc1763db6ce76cb316539b838f0d13 (the 10-03 pin, long behind the trunk) · GIT_CONFIG_VALUE_0=/data/work/agi (a PATH, not '*': the carry units' GIT_CONFIG_COUNT/KEY_0 pair takes its value from this file).
agi-boot.service TODAY is the pre-A1 form: no EnvironmentFile, no pin, no ExecStartPre; its ExecStart reads `HEAD:.agi/nodes/.geometry/engine-root.md` (the moving checkout, not a pin) and pipes the `### agi-boot` section to `sh -s`; Environment carries GIT_CONFIG_VALUE_0=* inline. Active since 10-01 22:32 (Type=oneshot, RemainAfterExit). The baked /run/systemd/system/agi-project.service bakes the old sha 4225c981f5b6b37593c6cfdb92ade24bab337843. `agi-carry-fetch.timer`, `agi-ram-main.service` and `agi-boot.service` are active; the per-post `agi-carry@<post>.path` units are enabled; 12 `agi-post@<post>.service.d` drop-in dirs sit under /run.

**What the ONE act changes (so the rollback list is complete).** carry.env gets the new vetted pin (and keeps its other cells); agi-boot.service becomes the A1 + A2 + A1b form (EnvironmentFile, pin, ExecStartPre=/usr/local/libexec/agi-vstore without a `-`, GIT_DIR); /usr/local/libexec/agi-vstore (856 B, root, 0755, sha256 f60191fd12942280569156cc2308e3ab4ec0c82cbb366676d50e77717b2d1fcc) is created BEFORE the new agi-boot.service; the carry units and box-carry/box/agi-signers/sect are replaced from the vetted tree; the baked agi-project.service/.path and agi-post@.service are regenerated under /run by the new projection. Order (unchanged): vstore file first, then carry.env, then units, then daemon-reload.

**STEP 0 (root, BEFORE anything else): back the before-state up and write ONE rollback command.** REHEARSED by DG1 (v2, after SM's H1 H2 returns) in a scratch root (ROOT=<dir>; fake files with NON-default modes 640 / 600 / 750; a /run tree holding agi-post@.service, a drop-in dir, agi-users.conf, a wants symlink and an unrelated other.service). The simulated act edited three files, deleted one, created /usr/local/libexec/agi-vstore, wrote a NEW post (agi-post@newpost.service.d + its wants link), rewrote agi-users.conf, deleted agi-post@.service and added the agi-project.path wants link. After `sh <backup>/rollback.sh`: every mode back (640 / 600 / 750, asserted, not only bytes), every byte back, the vstore file AND its created directory gone, the new post's drop-in dir and wants link gone, the added wants link gone, other.service untouched, the existing wants link present; a second rollback run was idempotent; a second step 0 in the same second REFUSES (`mkdir` of the backup dir fails: it never overwrites a before-state). NOT run on the real box (that is root's act).
**SM's returns folded (06:2xZ).** H1: the files are copied with `cp -a --parents` (modes, owners, times kept; `install -D -p` writes 0755: reproduced, a 640 file came back 755) and `before.stat` records mode, owner and path of each. H2: the /run set is NOT a file list: step 0 snapshots EVERY `agi-*` entry under /run/systemd/system (the generated units, agi-users.conf, the drop-in dirs) plus `multi-user.target.wants/agi-*` as one `run.tar` and a `run.before` manifest; rollback removes any path of that set that was not there before (dirs included: a NEW post's .d dir and wants link) and then extracts the tar. Notes: the backup directory has a seconds stamp and is made with `mkdir` (never `-p`), so a second run cannot overwrite the pre-act backup; `absentdirs` records /usr/local/libexec when it did not exist and rollback removes it (rmdir, only if empty).
~~~sh
#!/bin/sh
# step 0 of the host act (root): copy the before-state aside (modes and owners kept) and write ONE rollback command; ROOT= is for a rehearsal only
R=${ROOT:-};B=$R/var/backups/agi-act-$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p $R/var/backups&&mkdir $B||{ echo "step0: $B exists or cannot be made: refusing to overwrite a before-state";exit 1;};mkdir $B/files
L="/etc/agi/carry.env /etc/systemd/system/agi-boot.service /etc/systemd/system/agi-carry@.service /etc/systemd/system/agi-carry@.path /etc/systemd/system/agi-carry-fetch.service /etc/systemd/system/agi-carry-fetch.timer /opt/agi/bin/agi-signers /opt/agi/bin/box /opt/agi/bin/box-carry /opt/agi/bin/sect /usr/local/libexec/agi-vstore"
for f in $L;do if [ -e $R$f ];then (cd $R/&&cp -a --parents ${f#/} $B/files/)||exit 1;else echo $f>>$B/absent;fi;done
[ -d $R/usr/local/libexec ]||echo /usr/local/libexec>>$B/absentdirs
for f in $L;do [ -e $R$f ]&&stat -c '%a %U:%G %n' $R$f;done>$B/before.stat
# the generated units: EVERYTHING agi-* under /run/systemd/system, wants links and drop-in dirs included, as one tar + a manifest
U=$R/run/systemd/system;( cd $U 2>/dev/null&&ls -d agi-* multi-user.target.wants/agi-* 2>/dev/null )>$B/run.list
if [ -s $B/run.list ];then tar -C $U -cpf $B/run.tar -T $B/run.list||exit 1;(cd $U&&find $(cat $B/run.list) |sort)>$B/run.before;else : >$B/run.before;fi
(cd $B/files&&find . -type f|sort|xargs -r sha256sum)>$B/before.sha256
printf '%s\n' '#!/bin/sh' "B=$B;R=$R" 'U=$R/run/systemd/system' '[ ! -d $B/files ]||cp -a $B/files/. ${R:-/}||exit 1' 'if [ -d $U ];then ( cd $U;find agi-* multi-user.target.wants/agi-* 2>/dev/null|while read p;do grep -qxF "$p" $B/run.before||rm -rf "$p";done );fi' '[ ! -s $B/run.tar ]||tar -C $U -xpf $B/run.tar' '[ ! -s $B/absent ]||while read f;do rm -f $R$f;done<$B/absent' '[ ! -s $B/absentdirs ]||while read d;do rmdir $R$d 2>/dev/null;done<$B/absentdirs' '[ -n "$R" ]||systemctl daemon-reload' 'echo rolled back from $B'>$B/rollback.sh
echo "backup $B: $(wc -l <$B/before.sha256) files, $(wc -l <$B/run.before) /run paths, $(wc -l <$B/absent 2>/dev/null||echo 0) absent files; rollback: sh $B/rollback.sh"
~~~

**The /run set is covered whole (SM H2).** See step 0: every agi-* entry under /run/systemd/system and multi-user.target.wants/agi-*, not a hand list. If the act or any later fix adds a path OUTSIDE those two places (anywhere under /etc or /opt), add it to `L=` before running.

**ROLLBACK (one command).** `sh /var/backups/agi-act-<stamp>/rollback.sh` (the exact path is printed by step 0): restores every backed-up file with `cp -a` (modes kept), removes every /run agi-* path that was not there before and restores the rest from run.tar, deletes the files that were absent before (today: /usr/local/libexec/agi-vstore) and the directories that were absent (rmdir), then `systemctl daemon-reload`. It does NOT touch the trunk, any post's tree, the pin in git or running processes; the restored carry.env goes back to the 10-03 pin and the restored units to the 10-03 forms. The /run units are volatile: a reboot regenerates them from whatever carry.env and agi-boot.service say, which is the old pair after a rollback.
**Not covered / UNRUN by anyone:** systemd itself (daemon-reload ordering, ExecStartPre skipping ExecStart, PathChanged firing on carry.env); root's real safe.directory on /data/work/agi (alive's W8 ran it as agi-alive over a belam-owned MAIN with an empty HOME: rc 0); whether the pin in carry.env is a commit of the checked-out trunk at the moment of the act (belam's vetted T). The act is belam's own GO; this node only holds the before-state and the rollback.
