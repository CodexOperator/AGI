---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 2
tags:
  - card
  - prime
  - belam
thought_session: belam-s2-V
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs; progress lives on the town board. Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s2-V 19:0xZ 10-11: woke 17:1xZ (crons re-armed: CHECK f1b8bceb, scan f88711f2); ff'd SM's b6feb687d4 (.39 round 1 + .40.1 memguard with (f),(g)) on the council's 3/3 + the 18:59Z L acks; the merge-up first said green, SM amended to NOT green (111 failed, 0 attributed) and the council did not hold. That landing un-gates plan 4e: memguard-restage.sh is now allowed (race fix + (g) are in), still measured first. No owner message this gen.
<!-- THOUGHT:END -->

## §0 State (19:0xZ 10-11, read from date -u)
| | |
|---|---|
| STANDING | OWNER 20:2xZ 10-11 QUIET: "you shouldn't be mailed except once every few hours at most" -> masters send ONE digest per ~4 h, exceptions [red] + blocking owner asks (told SM + TM 20:2xZ); hourly scan cron DROPPED, CHECK 13 */4 only · OWNER 19:4xZ 10-11 (verbatim, relayed to SM for goal .41): "Make sure that the projection work is done before season rollover. Everything must be able to project cleanly." = .41 gates the season-2 close · owner 07:5xZ 10-10: every 4-h CHECK = TRAJECTORY FIRST (skill agi-merge-pass §1 T1-T3); owner 21:5xZ 10-10: IDLE mostly, the council rules, belam ffs council-approved tips + breaks ties |
| post | belam-s2-V (since 17:1xZ 10-11; IV 09:3xZ-17:1xZ); user agi-belam, works in ~/t (detached) on posts/belam; env now carries AGI_POST=belam + RUNTIME_DIRECTORY=/run/agi-belam |
| E | 4 cores · 7.8 GB · agi.slice MemoryHigh 5120 / Max 6144 MiB · ROOT disk vg0-root 60 GB holds every post home + /tmp (52% at 19:0xZ) · /data 360 GB (313 GB free) |
| posts (12, all claude) | DG1-5 · DT-1 · TM · alive · all-is-one · self-perpetuating · SM · belam; each has agi-post@<p> + agi-boxwake@<p> (template, Wants=) |
| mail | `AGI_POST=belam box read` / `... box send <p>` (stdin); belam mails the masters (SM, TM); the council answers SM; memory alarms arrive by `send.py read belam` |
| crons | session-only, RE-ARM AT WAKE: CHECK (13 */4) ONLY (owner quiet 20:2xZ 10-11). Box: user belam's crontab = crons.md (metrics_cell board commit at :23-:27 lands on MAIN UNSIGNED until .42) |
| carry.env pin | AGI_TRUNK = 5f5dc2c4be (since 14:32Z); backups /etc/agi/carry.env.pre-pin-2026101{1T101540Z,1T114855Z,1T120833Z,1T143246Z}; a pin move re-projects every /run unit through agi-project.path |
| landing | `sudo -n -u belam git -C /data/work/agi merge --ff-only <sha>`; then `git update-ref refs/heads/posts/belam <sha> <old>` + `git checkout -q --detach <sha>` in ~/t (never a bare `git reset`: it leaves old files); card commits through `AGI_POST=belam agi-at <path>`, then ff MAIN to posts/belam + `sudo -n -u belam git -C /data/work/agi push -q origin posts/belam`; a :2x board commit on MAIN in between = a signed 'take MAIN' merge (merge-tree + commit-tree -S) |
| merge pass | B6 MERGED ef9b043e68; BASE for B7 = 4e9dbced38; 0 experiment files since (521 commits) -> no PASS, no notice |

## §1 Plan
```
1. [merge-up] -> re-read the approver's ref (alive answers for the council) + my box for a later [return]/[withdraw]
   -> tree/blob identity vs the approved sha(s) (a re-mint passes only if the extra paths == HEAD) -> .agi/keys per commit
   -> engine-wrap/engine-post pieces named? (self-installing at each post start) -> anonymize diff + every message,
   GPU grep, origin falsifier -> ff MAIN -> [landed] to SM. A [withdraw] after my ff = SM fixes forward, never a revert.
2. CHECK every 4 h + the hourly scan (memory, swap, /dev/shm by owner, ROOT disk %, agi.slice anon+shmem, wake x12, dialogs).
3. OWNER RULINGS OWED (§6): season-2 CLOSE + research pause · host-act GOs (.12 ring, .11.1) · claude pin · host identity · 657 archive refs.
4. HOST ACTS OWED, each MEASURED in scratch first (run agi-project's own section from the trunk into a scratch dir at the live pin
   AND at the new sha; the live pin's render must == /run byte-for-byte; then run any new ExecCondition by hand as every post's uid):
   a. SM's NEXT landing carries memory_alarm --warn-psi-some-avg60 10 -> 30 (crons.md e4d62b39d7) -> `crons.py apply` after the ff.
   b. goal .42 (board commits G, option E, council 15:07Z C1-C6; DG4 re-cut 16b368ad72 running lanes): at its ff run
      `crons.py apply --sudo` IN THE SAME MINUTE (SM: the */5 self-apply drops graph_metrics from uid belam's crontab).
   c. goal .38.1 MAIN hook: DONE 01:43Z 10-12 at 375139b329 (agi-hook via uid belam's sudo; sha256 5abda4fff53c == the piece). Re-run on a later piece change: sudo -n -u belam sudo -n env PATH=/opt/agi/bin:/usr/bin:/bin AGI_TRUNK=local-maxxing/season2/main sh -c 'cd /data/work/agi && sect agi-hook <sha> | sh -s <sha>'.
   d. any engine-root landing (agi-post@ / agi-boxwake@ / agi-project) is live only at my pin move; restart agi-boxwake@ x12
      if its ExecStart changed. Pin move: cp -p carry.env to a dated backup; sed the ONE AGI_TRUNK line; verify live == render.
   e. MEMGUARD re-stage: DONE 00:32Z 10-12 at 3762e56145 via memguard-restage.sh (PROVEN). Next time the same: SHA=<sha> sh ~/memguard-restage.sh, then the a1/a2 proofs. Old by-hand route: save
      ~/memguard-A0/a2.since -> A0 on the LANDED sha -> restore -> sudo systemctl stop agi-memguard -> a1.undo -> a1 -> a1.proof
      -> a2.sh -> SHA=<sha> a2.proof.sh (PROVEN = 0 0 + healthy). Undo: sh ~/memguard-A0/src/extensions/agi/boxkit/memguard-a2.undo.sh
   f. a post asking for scratch on /data: sudo mkdir /data/work/gate-<p>; chown agi-<p>:; chmod 700 (made: gate-sm 17:09Z, gate-director-general-5 19:02Z, gate-director-general-1 20:12Z).
5. BOX RULE (mine, relayed by SM, in skill agi-memory-guard): no lane/test scratch on /dev/shm NOR in a post home (root disk);
   /data/work/gate-<p>; nice -n 10; ONE heavy suite on the box; a full suite starts only at agi.slice anon+shmem < 3500 MiB
   AND MemAvailable >= 2.5 GB AND PSI full avg60 < 2; it stops itself at full avg60 > 10.
6. A restart by hand only when idle: transcript >= 60 s, only baseline procs in the unit, MemAvailable >= 2.5 GB; then the pane log ~<p>/o (grep -a 'Esc to cancel').
NEVER: rule a [decision] the council can rule · assign a design or a build · dispatch · write in another post's tree or files
```

## §2 Landed
belam-s2-V (17:1xZ-): ff b6feb687d4 19:00:08Z (.39 r1 + .40.1 memguard; council alive 16:21/16:42/17:06Z + L acks 18:59Z; pytest NOT green, 0 attributed) · [landed] to SM 19:00Z · /data/work/gate-director-general-5 (19:02Z) · .38.1: GO for the ~/bin self-install (19:07Z; the MAIN .git/hooks install stays my later host act) + DG5's 24 refs/heads/posts/director-general-5-* RETIRED to refs/archive/posts/ (CAS per name, after DG5's dg5-* copies matched and its 12 lanes were switched off the old names) · ff 97865e4139 19:14Z (.38.1 ref guard, self-installs at each post start)
belam-s2-IV (09:3xZ-17:1xZ): 18 ffs 2387a51ce7 .. c52ccd53c9 · memguard A2 PROVEN · .37 re-render + drop-ins 50-52 retired · .32 agi-boxwake@ x12 · pins -> 5f5dc2c4be · rulings .38.1, .42 laned; box rule (detail: git + goal notes + refs/box/belam/sanctuary-master)

## 🔴 Where it stops
belam-s2-V: LANDED SM's stack 3762e56145 00:31Z 10-12 (.42 E code half · SM branch psi 30 · .20.2 every alarm on signed box mail · .41 agi-sync) + all host acts green: alarm_spool.py in /opt/agi/bin, agi-quiet-watch re-installed (backup /var/backups/agi-quiet-watch-20261012T003153Z), memguard re-staged at 3762e56145 (PROVEN), ONE crons.py apply --sudo (send.py gone from every crontab; agi-belam 3 + agi-sanctuary-master 2 lines), alarm-first-start rc 0. Alarms now arrive as [alarm <job>] box mail from sanctuary-master.
- .40.1.1 LANDED b32076b914 00:54Z + sysctl 60-agi-vm.conf vfs_cache_pressure 200 LIVE 00:55Z (PRE: slice 4898, slab 1068, swap 1432 MiB, events high 383172); AFTER reading due 01:57Z (one-shot cron) -> one line to SM. Both DG notes FIXED in stack 6 911a1d95eb (ff 01:26Z: sysctl-check reads /proc/sys, fill line = anon+shmem+slab_unreclaimable, apply --sudo prints installed/unchanged; agi-belam 4 + agi-sanctuary-master 3 lines incl. */5 caps).
- LANDED 375139b329 01:43Z (stack 7: box-mail lane, unit-paths carry check, config:engine-capsule, agi-hook) + 4c installed.
- owed next: 4c agi-hook (DG3 f8e0a26efc) · .43 (DG3 cb81a8fa3e) · .44 capsule pack (DG4) · memguard row 3 onto the spool (next .20.2 cut).
- next command: `AGI_POST=belam box read`.

## §4 Traps (this generation's only)
| # | trap | rule |
|---|---|---|
| 101 | "scratch on disk" read as a post HOME: SM's ~/gate/tmp filled the ROOT disk 71% -> 82% in ~1 h (17:0xZ) | say /data/work/gate-<p> by path; the hourly scan reads `df /` too |
| 102 | a slice gate on agi.slice memory.current never opens: it counts reclaimable cache + kernel memory and sits at MemoryHigh | gate on memory.stat anon + shmem (< 3500 MiB) |
| 104 | memory warns with NO suite: agi.slice AT MemoryHigh with anon 1.6 GB = 2.7 GB kernel SLAB (dentries) charged to the slice; reclaim swaps the posts (23:1xZ) | read agi.slice memory.stat slab; relief = sync + drop_caches=2 (23:19Z: 5104 -> 2571 MiB); durable fix laned to SM 23:2xZ |
| 103 | a stopped transient unit stays loaded while a template's Wants= names it, so a plain stop restarts the transient | stop it AND move /run/systemd/transient/<unit> to a backup, daemon-reload, then start the template |

## §5 Verification
at 19:1xZ: MAIN 97865e4139 == posts/belam == ~/t HEAD; DG5 refs/heads/posts/director-general-5-* 0, refs/archive/posts/* 24 · 24 units active · memguard active · / 52% · anon+shmem 2504 MiB · falsifier 0

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| RECURSIVE PACK (owner 20:2x-20:3xZ 10-11, verbatim with SM): the container = its own pack (file/dir), attached to any node by mint id (re-pointable), rendered there; ONE format for rollover (goals/exps -> builds), box moves (pack a post's slices -> carry -> unpack) and any slice | ROUTED to SM 20:3xZ for a council design + leaves (engine shell verbs pack/unpack/move; REGROW falsifier; candidate: git bundle per pack); after .41, before the season-2 close. Replaces D2's goal-tree nest: and D4's bundle DROP. + owner 20:4xZ: the pack IS a signed capsule payload, encrypted optional = ONE envelope with goal .4 (secrets keep always-encrypted + quorum pop; slices may be plain-signed); relayed 20:4xZ |
| SEASON-2 CLOSE (asked 04:1xZ 10-11, after the loop end closed 24cdb55824) + RESEARCH PAUSED (council no-go 12:47Z on goal:g5.28's own Falsifier; DT-1 idle; nothing queued) | owner: close season 2 now (B7 + the morals review) and accept the pause; a reopen must name the main-track hypothesis it feeds |
| root-guard mail identity: OWNER GO 19:5xZ 10-11 ("we need to fix whoever is using the old mail path"), LANED to SM 19:57Z = goal .20.2 (DG1: rows -> user: agi-belam + ~/bin/agi-notice, send.py out, ETA ~23:30Z, live only after .42 C1; interim: the user@ row loses --notify = 1 msg/alarm; flap = target 4). OWNER 21:1x-21:2xZ "Pressure alarm should use new mail system also" / "All alarms" -> target = BOX MAIL for every alarm (memory_alarm x2, send.py wake */2, memguard, rc-keepalive; quiet-watch already box via runuser+box send = the pattern); relayed 21:2xZ. Only old-path writer today = memory_alarm.py x2 cron jobs (uid belam crontab, send.py --notify belam, 48 unsigned/day, doubled) | cut 1 agi-notice (no key), cut 2 <box>-host identity; crons.py apply (--sudo) = my host act at the ff |
| 657 refs/archive/worktrees/* in MAIN from the pre-move bundle (/mnt/agi-flash/agi-backup-20261008T201541Z/agi-all.bundle); origin holds 0 | keep local + the bundle as the second copy, or publish: owner |
| CLAUDE UPGRADE = every post's hooks off: posts run /usr/local/bin/claude -> ~belam/.local/bin/claude (the owner's own install); an upgrade that rejects settings.json 'tui' skips the whole file | pin the posts to a root-owned copy (/opt/agi/claude-<ver>); move the pin only after .36's scratch-HOME probe AND .36.1's hooks-loaded proof pass on the new binary |
| egress watchdog never runs (literal \" quotes) while E is in FULL tunnel | fix it (drop 6 backslashes) or leave it; idea:egress-watchdog-keeps-e-reachable |
| guard layer 5 not installed + a STRAY /data/work/.sanctuary/guard/guard.env (Sep 25) + an OLD guard-init.sh beside it: guard-init DIES on it by design since c84628156d; nobody runs sudo guard-init until the act | owner GO = ONE act: mv both -> *.retired-<ts> (never rm), then install layer 5 (config:guard E lines first) |
| agi-belam sudo NOPASSWD ALL on E (grok-era) | keep for now; the council narrows it to the host-act verbs |
| refs/grid on E differs from L in 5,845 refs | reconcile into a namespace on E; owner picks; no force-push |
| /data/scrub backups hold the UNREDACTED history (mode 700) · `*.pre-tier-*` backups (~/.claude, ~/.pi) | delete on the owner's word |
| the 2 x 5 USD TypeSafe jev keys | release: no live consumer |
| belam row opus-5-5 / high vs the live Prime opus-5-5[1m] / max | owner sets the row |
| GitHub history: ssh comment user@host | OWNER: leave it in, no rewrite, no purge |
