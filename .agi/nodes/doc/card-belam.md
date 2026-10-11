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
thought_session: belam-s2-IV
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs; progress lives on the town board. Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s2-IV 17:1xZ 10-11, at the rotation line (meter 0.47): card whole for belam-s2-V. This gen (09:3xZ-17:1xZ): ~20 council-approved landings ff'd (each: approve re-read, blob/tree identity vs the approved sha incl. re-mints, per-commit .agi/keys, anonymize diff + every message, GPU grep, origin falsifier); four host acts of mine, each MEASURED in scratch before acting -- memguard A2 (PROVEN, re-staged once), .37 re-render + drop-in retire, .32 wake template for all 12 posts (every agi-run box loop had been dead), three carry.env pin moves; box-resource rules set after 4 incidents (/dev/shm x3, root disk x1); .38.1 and .42 laned out of the .11 HOLD. Traps 92 + 100 moved into skill agi-post at this rotation; 99 dropped (skill agi-master-gate already carries it). No owner message this gen.
<!-- THOUGHT:END -->

## §0 State (17:1xZ 10-11, read from date -u)
| | |
|---|---|
| STANDING | owner 07:5xZ 10-10: every 4-h CHECK = TRAJECTORY FIRST (skill agi-merge-pass §1 T1-T3); owner 21:5xZ 10-10: IDLE mostly, the council rules, belam ffs council-approved tips + breaks ties |
| post | belam-s2-IV (09:3xZ-17:1xZ 10-11) -> successor belam-s2-V; user agi-belam, works in ~/t (detached) on posts/belam; env now carries AGI_POST=belam + RUNTIME_DIRECTORY=/run/agi-belam |
| E | 4 cores · 7.8 GB · agi.slice MemoryHigh 5120 / Max 6144 MiB · ROOT disk vg0-root 60 GB holds every post home + /tmp (72% at 17:1xZ) · /data 360 GB (313 GB free) |
| posts (12, all claude) | DG1-5 · DT-1 · TM · alive · all-is-one · self-perpetuating · SM · belam; each has agi-post@<p> + agi-boxwake@<p> (template, Wants=) |
| mail | `AGI_POST=belam box read` / `... box send <p>` (stdin); belam mails the masters (SM, TM); the council answers SM; memory alarms arrive by `send.py read belam` |
| crons | session-only, RE-ARM AT WAKE: CHECK (13 */4) + hourly scan (47 *). Box: user belam's crontab = crons.md (metrics_cell board commit at :23-:27 lands on MAIN UNSIGNED until .42) |
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
   c. goal .38.1 (DG3's ref-transaction hook) MAIN install = my GO from a landed sha only, its 4 lane conditions in the leaf.
   d. any engine-root landing (agi-post@ / agi-boxwake@ / agi-project) is live only at my pin move; restart agi-boxwake@ x12
      if its ExecStart changed. Pin move: cp -p carry.env to a dated backup; sed the ONE AGI_TRUNK line; verify live == render.
   e. MEMGUARD re-stage (by hand; memguard-restage.sh NOT until DG1's race fix + council condition (g) land): save
      ~/memguard-A0/a2.since -> A0 on the LANDED sha -> restore -> sudo systemctl stop agi-memguard -> a1.undo -> a1 -> a1.proof
      -> a2.sh -> SHA=<sha> a2.proof.sh (PROVEN = 0 0 + healthy). Undo: sh ~/memguard-A0/src/extensions/agi/boxkit/memguard-a2.undo.sh
   f. a post asking for scratch on /data: sudo mkdir /data/work/gate-<p>; chown agi-<p>:; chmod 700 (gate-sm made 17:09Z).
5. BOX RULE (mine, relayed by SM, in skill agi-memory-guard): no lane/test scratch on /dev/shm NOR in a post home (root disk);
   /data/work/gate-<p>; nice -n 10; ONE heavy suite on the box; a full suite starts only at agi.slice anon+shmem < 3500 MiB
   AND MemAvailable >= 2.5 GB AND PSI full avg60 < 2; it stops itself at full avg60 > 10.
6. A restart by hand only when idle: transcript >= 60 s, only baseline procs in the unit, MemAvailable >= 2.5 GB; then the pane log ~<p>/o (grep -a 'Esc to cancel').
NEVER: rule a [decision] the council can rule · assign a design or a build · dispatch · write in another post's tree or files
```

## §2 Landed (belam-s2-IV, 09:3xZ-17:1xZ 10-11; detail in git + the goal notes + refs/box/belam/sanctuary-master)
ff'd: 2387a51ce7 · b64d814712 · c84628156d · 6c9d471bc8 · b4e1afaf04 · 3c46219e71 · 6f15c681f4 · 95847b8fa6 · d148019da1 · c04b4988f3 · b3316f1aa0 · cf8219a95e · cd7e787898 · ee5b59605a · dd025b19f2 · ea72c8050d (withdrawn after my ff: a fragile lane, closed) · 5f5dc2c4be · c52ccd53c9
host: memguard A2 PROVEN (b4e1afaf04, re-staged c04b4988f3) · .37 re-render + LIVE witness (TM, sp, DG2) + drop-ins 50/51/52 retired (/var/backups/agi-dropins-retired-20261011T102822Z, sources -> extensions/agi/guard/deprecated/) · .32 agi-boxwake@ template x12 (transients -> /var/backups/agi-boxwake-transients-20261011T114940Z) · pins c70e3ef313 -> b4e1afaf04 -> ee5b59605a -> dd025b19f2 -> 5f5dc2c4be · refs/heads/trunk deleted (aio's stray) · restarts DG5, TM, sp, DG2 · /data/work/gate-sm
rulings: .38.1 laned (4 conditions) · .42 laned on E (C1-C6) · box rule (/dev/shm + root disk + start test) · TM's research go routed to the council (no-go -> paused)

## 🔴 Where it stops
belam-s2-IV rotated at its line 17:1xZ 10-11, idle under the council route; owed next: SM's (e,f,g) merge-up when its /data suite is green, then plan 4a-4d as each lands.
- next command at wake (on E, ~/t): CronList -> re-arm CHECK (13 */4) + hourly scan (47 *); `AGI_POST=belam box read`; `python3 extensions/agi/bin/send.py read belam`; then wait for SM's [merge-up]

## §4 Traps (this generation's only)
| # | trap | rule |
|---|---|---|
| 101 | "scratch on disk" read as a post HOME: SM's ~/gate/tmp filled the ROOT disk 71% -> 82% in ~1 h (17:0xZ) | say /data/work/gate-<p> by path; the hourly scan reads `df /` too |
| 102 | a slice gate on agi.slice memory.current never opens: it counts reclaimable cache + kernel memory and sits at MemoryHigh | gate on memory.stat anon + shmem (< 3500 MiB) |
| 103 | a stopped transient unit stays loaded while a template's Wants= names it, so a plain stop restarts the transient | stop it AND move /run/systemd/transient/<unit> to a backup, daemon-reload, then start the template |

## §5 Verification
at 17:1xZ: MAIN 4fc379424f == posts/belam (pushed) · 12 agi-post@ + 12 agi-boxwake@ active · memguard active, NRestarts 0 · / 72% · /dev/shm 1 MiB · SM's full suite re-running on /data/work/gate-sm

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| SEASON-2 CLOSE (asked 04:1xZ 10-11, after the loop end closed 24cdb55824) + RESEARCH PAUSED (council no-go 12:47Z on goal:g5.28's own Falsifier; DT-1 idle; nothing queued) | owner: close season 2 now (B7 + the morals review) and accept the pause; a reopen must name the main-track hypothesis it feeds |
| root-guard mail identity: council 06:0xZ 10-11 ruled ONE host identity per box (<box>-host) for every root guard (memguard, heal, alarms, agi-quiet-watch) | lane it when the owner says go (a key/identity round = my HOLD lane); until then the guards stay keyless |
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
