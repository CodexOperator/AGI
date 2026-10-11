---
id: doc:dg2-aa1m-host-act-2
mint_id: fa7fa981a4594c3b9d6d2d068fe17ff4
type: doc
parents:
  - goal:g7.16.1.11.11.1
next_edges: []
edited_by: director-general-2
season: 2
title: "AA1.M HOST ACT 2 package for belam's GO: does a per-sender PathChanged unit wake the carrier on EVERY send (scratch, throwaway units, stub service, one command + one rollback)"
tags:
  - aa1m
  - host-act
  - path-unit
  - g7.16.1.11
town: core
---
# doc:dg2-aa1m-host-act-2

Author director-general-2, 10-02, on DG1's sharpen ask (19:16Z). Written 19:16Z BEFORE the runs (it has since RUN as host act 2 and 2b: see the RAN sections below; the hypothesis it motivates is the corrective fork, parent edge: the goal, per the [doc] schema's ONE goal parent, DG1 corrective on mur dg1aa1m-il1). It is the package for belam's own GO (belam 19:1xZ: "Host act 2 comes to belam as ONE line for its own GO"). The experiment that motivates it: experiment:dg2-aa1m-m2-path-unit-watch.

## RAN (belam, root, 19:32:46Z; rolled back 19:33:10Z): result and the one flaw
Every line MET except GHOST-after (NOT TESTED: my script's flaw, below). The PACK hazard below is WITHDRAWN for systemd: the unit re-arms (5 fired), only raw inotify dies. Full table: experiment:dg2-aa1m-m2-host-act-2. Flaw: the ghost step ran `mkdir` as the row user under the root-owned `/tmp/m2` = Permission denied. The run's record sha256 stays 9e4180a560f642fbc0e3e0fa88dbb08593518407fa880049bb2efd277417539d (the script below is that version, unchanged).

## The ghost-AFTER line: RAN as host act 2b (belam 19:39:48Z): MET. Below: the one-shot as it was offered
`.agi/context/local-maxxing/aa1m/host-act-2-ghost.sh` (1,674 B, sha256 a53de7d5fdf0437196cbab1d25197ff1af2f2136e3217b835ed3fd7aa8a946c2; root, scratch under /tmp/m3, throwaway unit `agi-act2g@`, rolls itself back): `echo "a53de7d5fdf0437196cbab1d25197ff1af2f2136e3217b835ed3fd7aa8a946c2  <path>" | sha256sum -c - && sh <path>` · before-state: no /tmp/m3, no `agi-act2g*` unit · EXPECT: `GHOST before...: active waiting` · `fired>=1` after root creates the dirs and the row user touches a file · more after a 2nd write · `ROLLED BACK: units=0 /tmp/m3=0`. It is the old ghost line with the one fix (root creates the dirs). Dry-checked: `sh -n` and `systemd-analyze verify` only.
**RESULT: fired=1, then fired=2 on a 2nd write: a waiting unit attaches when the dir appears; no ordering after the post unit is required (host act 2 = 8 of 8; experiment:dg2-aa1m-m2-host-act-2b).** The question as asked: **Is it moot?** Only if the path unit is started AFTER the dir exists: e.g. the post unit's `ExecStartPre=+` creates `refs/box/<P>` and the path unit is started by that unit (`WantedBy=agi-post@%i.service` + `After=`), never at boot. The DEFAULT shape of a path unit (enabled to `paths.target`, up at boot) starts BEFORE any post unit has run, so the dir does not exist yet and the unit waits (host act 2 measured that it waits, `active/waiting`); whether it then attaches when the dir appears is the one line left unmeasured. It is cheap (about 6 s), so the recommendation is: run it, unless DG3 builds the second shape.

## The ONE line for belam (the original act, already run)
Run as root, once: `echo "9e4180a560f642fbc0e3e0fa88dbb08593518407fa880049bb2efd277417539d  /data/work/agi/.agi/worktrees/de-base-dg2-4/.agi/context/local-maxxing/aa1m/host-act-2.sh" | sha256sum -c - && sh /data/work/agi/.agi/worktrees/de-base-dg2-4/.agi/context/local-maxxing/aa1m/host-act-2.sh` (the path moves to the trunk copy `.agi/context/local-maxxing/aa1m/host-act-2.sh` when DG1's merge-up lands; the script is 2,520 B and is read whole below). Print is 8 lines; compare with EXPECT.
- **Before-state:** no `/tmp/m2`; `systemctl list-units --all --no-legend 'agi-act2*' | wc -l` = 0; no live store, no real carrier, no post unit touched. The units go to `/run/systemd/system` (tmpfs: they vanish at a reboot even if the rollback is never run).
- **Rollback, ONE command:** `sh -c 'systemctl stop "agi-act2@*.path" "agi-act2c@*.path"; rm -f /run/systemd/system/agi-act2*; systemctl daemon-reload; systemctl reset-failed "agi-act2*" 2>/dev/null; rm -rf /tmp/m2; :'` · PROOF: `systemctl list-units --all --no-legend 'agi-act2*' | wc -l` = 0 and `ls -d /tmp/m2 2>/dev/null | wc -l` = 0.
- **Dry-checked without root (what I could):** `sh -n` clean; the four unit texts pass `systemd-analyze verify`; the same six sends run against the two watch placements with raw inotify (the TWIN below). NOT checked: anything systemd itself does (the real PathChanged mask, the re-arm, the ghost row): that is what the act is for.

## What it tests (each line prints once; EXPECT in brackets)
| line | question | expect |
|---|---|---|
| `GHOST before its dir exists` | what does a row with NO store dir yet do (the live state today: `/var/lib/agi/*/g.git` does not exist)? | `ActiveState=active SubState=waiting` is the hope; if it is `failed`/`inactive`, the live rows MUST get their dir before the unit starts |
| `ROW alive` | a unit on the sender's OWN `refs/box/<P>` (dir pre-created, owned by the row's uid) fires on every send? | sends=3 fired=**3** |
| `CTRL all-is-one` | the unit AS SPECIFIED (`refs/box`, the sender dir not pre-created) fires once per sender, not per send? | sends=3 fired=**1** |
| `NEG` | no send, and a write elsewhere in the store (`refs/heads/z`) wake nothing? | fired equal before/after |
| `PACK` | after `git pack-refs --all` (a gc does it) deletes the empty pre-created dir, do the next 2 sends still wake? | fired=5; **3 = the watch died with the dir** (raw inotify does) |
| `GHOST after` | the dir + a file appear later: does the waiting unit attach and fire? | fired>=1 |
| `INOTIFY` | instances pid 1 holds before / after / the limit | after = before + 3 (one per path unit) |

## The unit text (scratch names; the live ones differ only by the path and the service)
`agi-act2@.path` (48 B): `[Path]\nPathChanged=/tmp/m2/%i/g.git/refs/box/%i` · `agi-act2c@.path` (45 B): `[Path]\nPathChanged=/tmp/m2/%i/g.git/refs/box` · `agi-act2@.service` = `agi-act2c@.service` (76 B): `[Service]\nType=oneshot\nExecStart=/bin/sh -c 'echo fired >>/tmp/m2/fired.%i'`.

## The live design this would unlock (NOT part of the act; DG3's build, belam's GO per install)
- `agi-carry@.path`: `[Path]\nPathChanged=/var/lib/agi/%i/g.git/refs/box/%i\n[Install]\nWantedBy=paths.target` · `agi-carry@.service`: `[Service]\nType=oneshot\nExecStart=/opt/agi/bin/box-carry %i` (the carrier DG3 builds). One template pair, one instance per row.
- the per-row directory: created by ROOT at the post unit's start (`ExecStartPre=+`, the house idiom), owned by the row's uid, 0755: `install -d -o agi-%i -g agi-%i -m 755 /var/lib/agi/%i/g.git/refs/box/%i`. The path unit cannot create a dir its sender must own (`MakeDirectory=` makes it root-owned and the sender could not write a ref in it).
- **Counts:** 32 rows on the trunk today (`config:posts`, all 32 with a harness) = 32 instances; each path unit holds ONE inotify instance in pid 1 (root) against `fs.inotify.max_user_instances` = 128 (read from /proc/sys on this box) and `max_user_watches` = 128,113: 32 + the root's other users must stay under 128, the act prints the `before=` figure so the margin is measured, not assumed. Watches are not the limit (1-2 per unit).

## TWIN (no root, raw inotify with systemd PathChanged's event mask, the same six sends 1 s apart) — scratch script `.agi/context/local-maxxing/aa1m/host-act-2-twin.py`
- TWIN ROW alive (inotify on refs/box/alive, dir pre-created): sends=3 event-bursts=**3**
- TWIN CTRL all-is-one (inotify on refs/box, sender dir not pre-created): sends=3 event-bursts=**1**
- PACK (raw inotify): send 1 = 4 events; `git pack-refs --all` = 6 events + `IN_IGNORED` (the kernel dropped the watch), the dir is GONE (git prunes the empty `refs/box/<P>` dir; `git gc` does the same); sends 2 and 3 after it = **0 events**.
**The twin is inotify, not systemd PathChanged.** It says what the kernel gives any watcher; whether systemd re-arms a path unit whose directory was deleted and recreated is exactly the PACK line of the act.

## If the PACK line reads 3 (the unit does not re-arm): the mitigations, none chosen (NOT NEEDED: it read 5)
(a) store config `gc.packRefs=false` (set where the store is created, agi-store) so gc never prunes `refs/box/<P>`; nothing else in the engine calls `pack-refs`; (b) the carrier's own wake re-creates the dir (`install -d`) after every run, so the NEXT send is watched; (c) the timer alone, with its latency. (a) costs one config line; (b) loses the first send after a prune.

## Honest limits
One uid's view of three instances, a stub service, 1 s send gaps (a burst of sends inside one service run coalesces into one activation: the carrier must read every ref per wake, not one message per wake). Nothing here measures the runuser carry (host act 1) or a second box (host act 3). The ghost row's result decides whether the live units need ordering after the post unit's `ExecStartPre=+`.

## The script, whole (the version belam RAN: 2,520 B, sha256 9e4180a560f642fbc0e3e0fa88dbb08593518407fa880049bb2efd277417539d)
~~~sh
#!/bin/sh
# act2.sh (ROOT, scratch only): does a PathChanged unit on a sender's own refs/box/<P> fire on EVERY send, and one on refs/box only on the first?
# Throwaway units in /run/systemd/system (gone at reboot), stub service, stores under /tmp/m2; no live store, no real carrier.
D=/tmp/m2;U=/run/systemd/system;A=alive;B=all-is-one
r(){ u=$1;shift;runuser -u agi-$u -- env HOME=/var/lib/agi/$u "$@";}
n(){ ls -l /proc/1/fd|grep -c anon_inode:inotify;}
f(){ [ -f $D/fired.$1 ]&&wc -l<$D/fired.$1||echo 0;}
snd(){ r $1 sh -c "cd $D/$1/g.git&&git update-ref refs/box/$1/$2 \$(echo \$\$|GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=$1@agi GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=$1@agi git commit-tree \$(git hash-object -w -t tree /dev/null))";sleep 1;}
install -d -m 755 $D;for u in $A $B;do install -d -o agi-$u -g agi-$u -m 755 $D/$u;r $u git init -q --bare $D/$u/g.git;done
r $A mkdir -p $D/$A/g.git/refs/box/$A;r $B mkdir -p $D/$B/g.git/refs/box
printf '[Path]\nPathChanged=/tmp/m2/%%i/g.git/refs/box/%%i\n'>$U/agi-act2@.path;printf '[Path]\nPathChanged=/tmp/m2/%%i/g.git/refs/box\n'>$U/agi-act2c@.path
for t in agi-act2 agi-act2c;do printf "[Service]\nType=oneshot\nExecStart=/bin/sh -c 'echo fired >>/tmp/m2/fired.%%i'\n">$U/$t@.service;done
systemctl daemon-reload;i0=$(n);systemctl start agi-act2@$A.path agi-act2c@$B.path agi-act2@ghost.path;i1=$(n)
echo "GHOST before its dir exists: $(systemctl show -p ActiveState,SubState,Result agi-act2@ghost.path|tr '\n' ' ')"
snd $A $B;snd $A $B;snd $A dg5;snd $B $A;snd $B $A;snd $B dg5;sleep 2
echo "ROW   $A (watch refs/box/$A, dir pre-created): sends=3 fired=$(f $A) [expect 3]"
echo "CTRL  $B (watch refs/box, sender dir NOT pre-created): sends=3 fired=$(f $B) [expect 1]"
x=$(f $A);r $A touch $D/$A/g.git/refs/heads/z;sleep 3;echo "NEG   no send + a write elsewhere, 3 s: fired $x -> $(f $A) [expect equal]"
r $A git -C $D/$A/g.git pack-refs --all;echo "PACK  pack-refs --all pruned the pre-created dir: $([ -d $D/$A/g.git/refs/box/$A ]&&echo no||echo YES)";snd $A $B;snd $A dg5;sleep 2
echo "PACK  2 more sends after the prune: fired=$(f $A) [expect 5; 3 = the watch died with the dir]"
r $A sh -c "mkdir -p $D/ghost/g.git/refs/box/ghost&&touch $D/ghost/g.git/refs/box/ghost/x";sleep 2
echo "GHOST after the dir + a file appear: fired=$(f ghost) $(systemctl show -p ActiveState,SubState agi-act2@ghost.path|tr '\n' ' ')"
echo "INOTIFY instances held by pid 1: before=$i0 after_start=$i1 now=$(n) limit(max_user_instances)=$(cat /proc/sys/fs/inotify/max_user_instances)"
~~~
