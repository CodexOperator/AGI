---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 3
tags:
  - card
  - prime
  - belam
thought_session: belam-s3-III
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town = this box, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs. Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post (§8 = the rename runbook) · agi-town · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s3-III (woke 19:2xZ 10-21) ran G3, G4, G5 of goal:g7.16.1.11.45 end to end (each: step 0 card land, 1a, the 4a L, sitting --dry, move.sh as its own unit, run 2, SM's probe). This version compacts the G3-G5 record into §2 and leaves §🔴 on G6's prep: sitting v6 is written and boxed for SM's gate.
<!-- THOUGHT:END -->

## §0 State (22:2xZ 10-21)
| | |
|---|---|
| trunk | core/season3/main = MAIN's checkout = posts/belam = origin (tip 69e36d2286 = L57 + this card); season3/main = my PASS line (2a8056bcb5) |
| pin | /etc/agi/carry.env AGI_TRUNK = 69e36d2286 (G5 host act), host.done = it; rollbacks /var/backups/agi-act-20261021T{175530,195623,212943}Z/rollback.sh KEEP until G7 done. agi-project.path NEVER runs here: after every `agi.sh host`, `sudo systemctl start agi-project.service` + read back. Boot wants = 10 posts (TM, DT-1 off; DG1 is now director-goals-1 uid 981, DG2 director-science-1 uid 980, DG3 director-general-1 uid 979; director-review boot false, user agi-director-review uid 968 exists) |
| me | uid agi-belam SIGNS and PUSHES (credential lines, trap 114); sudo NOPASSWD ALL; I mail SM only (TM stood down) |
| landing my commits | `AGI_POST=belam agi-at <paths>` -> `sudo -n -u belam git -C /data/work/agi merge --ff-only -q refs/heads/posts/belam` -> push `<sha>:refs/heads/core/season3/main` + posts/belam. Run test_anonymize_guard before ANY direct push (council 15:25Z; I turned the trunk RED once with a slash list of user, home and branch) |
| landing SM's L<n> | `~/tools/verify-land.sh L<n> LAND BASE GATETIP`, ff MAIN, CAS posts/belam, push both, `git checkout -q --detach` in ~/t |
| crons | CHECK 13 */4 (session-only: RE-ARM at wake, CronList first) |
| WATCHER | ~/drive-deliver.sh as unit drive-deliver.service (D=/data/work/media/season3/deliver since 18:41Z; state ~/.drive-deliver, *.before-media-mv backups); restart = `sudo -n systemd-run --unit=drive-deliver -p User=agi-belam -p Group=agi-belam --setenv=HOME=<post home> /bin/sh ~/drive-deliver.sh`; stops 10-23. A replaced chapter = one partial full-video upload per batch |
| media | /data/work/media/season3 (agi-director-review:agi), MEDIA_BASE default; old parent keeps only 'warm'. Full explainer on Drive = 18 animated chapters, 3226.30 s, joinprobe 18/18 exit 0 (17:5xZ) |

## §1 Plan
```
1. MAIL: AGI_POST=belam box read (unread mail waits at this rotation)
2. goal:g7.16.1.11.45 THE POST SHUFFLE, the council owns the schedule (each GO = a council [decision] via SM):
   G0 done · G1 TM+DT-1 down (L40) · G1b pin a18c484bc4 · G2 director-review start = owner login + DG3 hand-over · G3 DG1->director-goals-1
   G4 DG2->director-science-1 · G5 DG3->DG1 · G6 DG4->DG2 · G7 DG5->DG3, ONE move at a time
   per move: 0 card -> 1a stop agi-post@<old> + agi-boxwake@<old> -> 4a rows+cards L (SM cuts, I land) -> move.sh (sitting + run 1 + coded start + run 2) -> SM's probe line
3. g5.4.2 media keys (only on SM's [word]): limit = planned + $0.50, expires_at in the POST, DG3/director-review ~/keys 600, never print; [done] -> PATCH disabled, shred;
   settle = two agreeing non-zero reads >= 30 min apart, never < mint + 3 h (~/tools/settle-read.sh, include_expired). 10 keys settled = $1.397 of $25
4. CHECK every 4 h (skill agi-merge-pass §1); PASS when experiments landed > 0
```

## §2 Landed (10-15 .. 10-21)
L26 a93fe7cf36 .. L57 69e36d2286 (each on the trunk; L31-L50 today: .44.8 agi.sh host/start/stop binds, g12.3 season rows, g5.4.1 report S1+S2, .42.2 :28 land of my node commits, .31.1 warm-load + close, .45 R1/T/S1/K/CHECKS, g5.4.2 media stack + MEDIA_BASE). Goals minted today: g7.16.1.11.45 (owner verbatim), .45.1 (no bare worktree prune; SM, after G7). Role templates doc:role-director-review/-goals/-science v1.1 (L41).
.45 moves today (logs ~/tools/runs/g{3,4,5}-move-*.out; every one: run 1 exact 18, run 2 all ok, SM's probe verifies a FRESH key):
  G3 19:56Z director-general-1 -> director-goals-1 uid 981 (L52 ba8faaad3a; its crash loop -> the council's back-dated .fresh, HERE only)
  G4 21:29Z director-general-2 -> director-science-1 uid 980 (L55 8a9d18ec9c; sitting v4 = real-time .fresh; left w-153 stale -> repaired by science-1)
  G5 22:18Z director-general-3 -> director-general-1 uid 979, the FIRST reused name (L57 69e36d2286; sitting v5: gate-free, gate/media mv, named worktree repair)
  their binds: L53 stays-up, L54 hostproj agi.sh 6c2bf128ec7f0a5a, L56 name-dirs (post-move-checks.sh 9b959084f44eea2c, run 2 = 20 rows); trap sweeps sp a03048b352 + aio 5a535f0bcb
Live acts today: TM + DT-1 stopped 14:4xZ; caches dropped 09:23Z, 14:13Z, 21:38Z, 21:45Z; G1b 17:55Z; media mv 18:41Z; root mv gate-director-general-1 -> gate-director-goals-1 21:47:45Z.

## 🔴 Where it stops
G6 PREP (DG4 -> director-general-2): sitting v6 a23e40e614747a92 (v5 485709be602a5075 kept as ~/tools/sitting.sh.v5-485709be) = (a) head guard 'every moving worktree locked' + (b) gate-free = gate-NEW absent OR (owned by UID AND gate-OLD absent); t-sitting.sh 9416f13de4306500 23/23; move.sh 842bac7cf231842a + t-move.sh 356eafe597a137c0 unchanged -> boxed SM [review] 22:23:40Z, WAITING SM's gate + the council.
G6 also needs (others'): DG4 locks its moving worktrees as itself (v6 refuses otherwise) · ROOT mv `sudo mv /data/work/gate-director-general-2 /data/work/gate-director-science-1` ONLY on the council's word (ls -ld both before/after), then science-1's NAMED repairs · DG4's step-0 card (land: ff if it sits on the trunk, else merge-tree + commit-tree -S 2 parents) · DG5's 4a -> SM's gate -> MOVE GO.
AT THE MOVE (the G5 form): 1a stop agi-post@ + agi-boxwake@director-general-4 (0 procs, 20 s) -> [1a-done] -> land SM's L (verify-land) -> rmdir an EMPTY /data/work/director-general-4-media if the council says so -> ancestry lines (2ebb270242, bc0bbc6d0d, the L) -> sitting --dry (BASE = the L's parent 1) -> `sudo -n systemd-run --unit=g6-move-dg4 --collect -p WorkingDirectory=$HOME/t -p StandardOutput=append:<runs/out> -p StandardError=append:<same> --setenv=HOME=/root --setenv=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin /bin/sh ~/tools/move.sh director-general-4 director-general-2 <uid> <L> <L^1> ~/t` (absolute paths) -> run 2 rows + stale-worktree read as root + key not in a closed ring line -> [run-2] to SM.
Then G7 (DG5 -> director-general-3). Open with SM (low): CHECK T2 (.42.2 + .44.8 close; .20.3 + .44.7 place); who pruned MAIN ~21:44Z (my candidate heal.py:1869/:2051 -> goal .45.1).
NEXT COMMAND: AGI_POST=belam box read   (SM's gate on v6; the council's G6 prep word)

## §4 Traps (this generation's only)
| # | trap | rule |
|---|---|---|
| 108 | an unquoted heredoc ate every $ figure in goal:g5.4.2 ("$15" -> "5") | every node body through a QUOTED heredoc (<<'EOF'), values patched in after |
| 109 | `pgrep -f <name>` matches the calling shell's own command line | match the exact argv: `ps -u agi-belam -o pid,args | grep '[d]rive-deliver.sh$'` |
| 110 | a temp token file shredded before rclone confirmed it: the one-use OAuth code was lost | keep a credential copy until the consumer proves it works, then shred |
| 111 | the agi-at reset leaves a STALE town:local-maxxing metrics line in ~/t | `git restore --source=HEAD --staged --worktree -- .agi/nodes/town/local-maxxing.md` |
| 112 | a box mail carried this box's host name (public repo) | write "this box" in mail and nodes |
| 113 | a setsid'd watcher dies with the post's cgroup at rotation | anything that must outlive the post runs as its own unit (`sudo -n systemd-run --unit=...`) |
| 114 | the rotation / restart rewrites ~/.gitconfig without the github credential lines: push -> 'could not read Username' | at wake: `git config --global --get-all credential.https://github.com.helper` must print '' + `!sudo -n -u belam /usr/bin/gh auth git-credential` (the token lives in uid belam; a plain gh line fails: agi-belam has no gh login); else re-add both, then `git push --dry-run` |
| 115 | verify-land anon-diff/anon-msg hits = systemd unit names, the Co-Authored-By trailer, or t@t.invalid test authors | list the hits; land only if every hit is one of those |
| 116 | an expired key leaves /keys?include_disabled=true | always `&include_expired=true` (in ~/tools/settle-read.sh) |
| 117 | my `sudo find /data/work /var/lib/agi` outlived its tool timeout and filled the dentry slab (14:12Z memory warn) | never walk those trees with find; kill a timed-out walk |
| 118 | `agi.sh host` printed `host: met` while /run held the OLD pin's projection (agi-project.path is never active here) | after every host act: `systemctl start agi-project.service`, then read back wants + agi-users.conf + getent |
| 119 | a stub harness inherited my ~/.gitconfig core.hooksPath: the ref-guard hook ran under the stub `id` ("[ref-guard] fail open: no user") | a harness sets HOME=<scratch> + GIT_CONFIG_NOSYSTEM=1 |
| 120 | the link check (links.py links) hung 16 min at 0% CPU | kill it; check the one new link by hand |
| 121 | agi.slice hit MemoryHigh on 2.2 GiB of dentry slab after my scratch-worktree harness runs (21:37Z alarm) | run harnesses one at a time; at a slab warn: `sync; echo 2 | sudo tee /proc/sys/vm/drop_caches`, read memory.stat back |
| 122 | a gate dir under another post's uid (700) reads as 'missing' to my uid | read worktree / dir existence as root before calling anything stale |

## §5 Verification
22:2xZ 10-21: origin core/season3/main = posts/belam = MAIN (tip 0aa49b525f + this card); carry.env + host.done = 69e36d2286; 10 agi-post@ active (the moved three: director-goals-1 NRestarts 10 = the G3 loop, frozen since 20:02Z; director-science-1 + director-general-1 NRestarts 0); 0 stale MAIN worktrees (read as root); test_anonymize_guard 65 passed; t-sitting 23/23 on v6, t-move 14/14; CHECK cron ae4470b2 (13 */4).

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| g5.4.2 M6 music: three ~30 s INSTRUMENTAL samples (a swing-flamenco, b balkan-brass-swing, c trombone-flamenco-jazz) + the owner's two SUNG Lyria songs from 10-14 (/data/work/belam-media: three-of-three, nothing-gets-deleted-here = Drive agi/season3-rollover-report/song-b.mp3; lyrics suno-songs.md), all sent 14:3xZ; the owner says more Suno songs + narrated clips + a first video exist on the grok-bot box and will bring them | the owner picks or brings material; no new track until then |
| .45 director-review first start: ONE owner login for the new post (agi.sh start S6 [owner-do], or /login in its pane) | show the one command when the owner is back and G2's other parts are done |
| .45 role templates: scopes are the Prime's reading (goals = goal stewardship that runs falsifiers and proposes closes; science = hypotheses, experiments, verdicts; review = presentation creation + checking deliverables) | owner confirms or corrects |
| g5.4.2 voice: the council picked by a pre-registered rule under "do your best" | show the owner the pilot + the README in deliver/ |
| needrestart: keep it (owner 10-21; it restarted the town 06:08Z on a liblzma update) | none |
| ElevenLabs direct account: none; Voice Design route OFF | revisit if the owner gets a key |
| the owner's complex-analysis project spends on the OPENROUTER_ADMIN account | per-key settled usage is the figure |
| 657 refs/archive/worktrees/* in MAIN; refs/grid on E vs L differ by 5,845 | keep local + bundle; owner picks |
| claude upgrade turns every post's hooks off (settings.json 'tui') | pin posts to a root-owned copy; move the pin only after the hooks-loaded proof |
