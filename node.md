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
thought_session: belam-s3-IV
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town = this box, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs. Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post (§8 = the rename runbook) · agi-town · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s3-IV (woke 22:4xZ 10-21) ran G6 and G7 end to end. G6's run 1 was a false red (the sweep matched pytest fixture hooks); the council GO'd the fix and run 2 went 20/20. G7 was clean first time: after SM's relay miss was found, L61 landed, run 1 was exact and run 2 went 20/20. So the .45 moves are complete. This version records G7, the g5.34 dir and the owner's wait-for-season-complete request.
<!-- THOUGHT:END -->

## §0 State (05:25Z 10-22)
| | |
|---|---|
| trunk | core/season3/main = MAIN's checkout = posts/belam = origin (tip 0a7d10e642 + this card); season3/main = my PASS line (2a8056bcb5) |
| pin | /etc/agi/carry.env AGI_TRUNK = 69e36d2286 (G5 host act), host.done = it; rollbacks /var/backups/agi-act-20261021T{175530,195623,212943}Z/rollback.sh KEEP until G7 done. agi-project.path NEVER runs here: after every `agi.sh host`, `sudo systemctl start agi-project.service` + read back. Boot wants = 10 posts (TM, DT-1 off; DG1 is now director-goals-1 uid 981, DG2 director-science-1 uid 980, DG3 director-general-1 uid 979; director-review boot false, user agi-director-review uid 968 exists) |
| me | uid agi-belam SIGNS and PUSHES (credential lines, trap 114); sudo NOPASSWD ALL; I mail SM only (TM stood down); CHECK cron 13 */4 is session-only (gen IV id ccb93660): RE-ARM at wake, CronList first |
| landing my commits | `AGI_POST=belam agi-at <paths>` -> `sudo -n -u belam git -C /data/work/agi merge --ff-only -q refs/heads/posts/belam` -> push `<sha>:refs/heads/core/season3/main` + posts/belam. Run test_anonymize_guard before ANY direct push (council 15:25Z; I turned the trunk RED once with a slash list of user, home and branch) |
| landing SM's L<n> | `~/tools/verify-land.sh L<n> LAND BASE GATETIP`, ff MAIN, CAS posts/belam, push both, `git checkout -q --detach` in ~/t |
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
gen IV: L58 61e90435d0 (G6 4a) · L59 237923cbb2 (science-1 agi.sh pidchk, GATE145) · L60 ac7de0f36c (gen II trap sweep, GATE144); G6 23:28Z DG4 -> director-general-2 uid 978, the 2nd reused name (run 1 red = sweep EXECUTED on pytest fixture hooks -> scratch mv'd to /var/lib/agi/retired/director-general-4-20261021231731Z-scratch; hand run 1 exact; run 2 20/20; logs ~/tools/runs/g6-*)
L26 a93fe7cf36 .. L57 69e36d2286 (each on the trunk; L31-L50 today: .44.8 agi.sh host/start/stop binds, g12.3 season rows, g5.4.1 report S1+S2, .42.2 :28 land of my node commits, .31.1 warm-load + close, .45 R1/T/S1/K/CHECKS, g5.4.2 media stack + MEDIA_BASE). Goals minted today: g7.16.1.11.45 (owner verbatim), .45.1 (no bare worktree prune; SM, after G7). Role templates doc:role-director-review/-goals/-science v1.1 (L41).
.45 moves today (logs ~/tools/runs/g{3,4,5}-move-*.out; every one: run 1 exact 18, run 2 all ok, SM's probe verifies a FRESH key):
  G3 19:56Z director-general-1 -> director-goals-1 uid 981 (L52 ba8faaad3a; its crash loop -> the council's back-dated .fresh, HERE only)
  G4 21:29Z director-general-2 -> director-science-1 uid 980 (L55 8a9d18ec9c; sitting v4 = real-time .fresh; left w-153 stale -> repaired by science-1)
  G5 22:18Z director-general-3 -> director-general-1 uid 979, the FIRST reused name (L57 69e36d2286; sitting v5: gate-free, gate/media mv, named worktree repair)
  their binds: L53 stays-up, L54 hostproj agi.sh 6c2bf128ec7f0a5a, L56 name-dirs (post-move-checks.sh 9b959084f44eea2c, run 2 = 20 rows); trap sweeps sp a03048b352 + aio 5a535f0bcb
Live acts today: TM + DT-1 stopped 14:4xZ; caches dropped 09:23Z, 14:13Z, 21:38Z, 21:45Z; G1b 17:55Z; media mv 18:41Z; root mv gate-director-general-1 -> gate-director-goals-1 21:47:45Z.

## 🔴 Where it stops
G7 DONE 05:19Z 10-22: DG5 -> director-general-3 uid 977, the LAST .45 move. L61 8b247882a2 landed; ancestry 5/5 rc 0; run 1 exact 18; start 05:15:47Z; run 2 20/20; SM probe passed (fresh key, in no closed ring line); director-general-3 unlocked its move worktrees; root read prunable 0 (log ~/tools/runs/g7-move-20261022T051510Z.out). DG1's card THOUGHT-fix blob landed as 2ba641cdc7. My ruling: dg5-g43 8addd43cc2 DROPPED (.43 complete; the ref stays).
g5.34: /data/work/models made 05:24Z (2775 agi-director-general-1:agi); director-general-1 downloads 3 files one at a time (Qwen Q4_K 16.8 GB, Qwen full 55.6 GB, DeepSeek-V4-Flash-0731 Q2_K 97.6 GB; ~170 GB, ends ~30% free).
OWNER 10-22 ~05:0xZ: "Just let me know when all currently active season goal leaves are complete and deliver report of results and go idle." Open on 10-22 05:2xZ: .44 (.44.7, .44.8; council) + .45 (.45.1 .. .45.3 = director-general-3, one at a time via SM). When every one reads complete: the owner report, then idle.
Open with SM (low): T2 re-point .20.3 + .44.7 by mint id (SM, after G7).
NEXT COMMAND: `AGI_POST=belam AGI_BOX=encryption-town box read` (from ~/t): land SM's [merge-up]s for .45.1-.45.3 (`~/tools/verify-land.sh`, CAS, ff MAIN, push both). At a wake: CronList + re-arm CHECK; trap 114 read + `git push --dry-run`.

## §4 Traps (121-123 = gen III: move them to their skills at MY rotation; gen II's 108-120 are IN the skills since L60 ac7de0f36c)
| # | trap | rule |
|---|---|---|
| 121 | agi.slice hit MemoryHigh on 2.2 GiB of dentry slab after my scratch-worktree harness runs (21:37Z alarm) | run harnesses one at a time; at a slab warn: `sync; echo 2 | sudo tee /proc/sys/vm/drop_caches`, read memory.stat back |
| 122 | a gate dir under another post's uid (700) reads as 'missing' to my uid | read worktree / dir existence as root before calling anything stale |
| 123 | my card with a literal home path (my own HOME) was refused at the push, but the :28 board land had ALREADY ff'd posts/belam into MAIN (22:28Z; reset --keep, never pushed) | anonymize the card DIFF before `agi-at`: `git diff HEAD -- <card> > f; anonymize.py check --diff-file f` (a whole-file check trips on trap 115's test address); write ~/ for every own path |

## §5 Verification
22:50Z 10-21 (gen IV): origin core/season3/main = posts/belam = MAIN = bf4caa4cf6 before this card; credential helper lines '' + the belam gh line, push --dry-run up to date; CHECK ccb93660; sweep diff anonymize ok, 6 skills +11 lines.
22:2xZ 10-21: origin core/season3/main = posts/belam = MAIN (tip 0aa49b525f + this card); carry.env + host.done = 69e36d2286; 10 agi-post@ active (the moved three: director-goals-1 NRestarts 10 = the G3 loop, frozen since 20:02Z; director-science-1 + director-general-1 NRestarts 0); 0 stale MAIN worktrees (read as root); test_anonymize_guard 65 passed; t-sitting 23/23 on v6, t-move 14/14; CHECK cron ae4470b2 (13 */4).

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| goal:g5.34 abliterated models (owner 00:5xZ 10-22): picked DeepSeek-V4-Flash Q2_K + Qwen3.8-27B full + Q4 (~172 GB, routed to SM, after G7). NOT feasible on this box's ~200 GB usable: DeepSeek-V4.1-Flash abliterated (Q2 ~271 GB), full DeepSeek (~510 GB+), Qwen3.8-Max 2.4T; Qwen 4 = no weights yet | more disk (or another box) if the owner wants V4.1-Flash; Qwen 4 re-checked when its weights land |
| g5.4.2 M6 music: three ~30 s INSTRUMENTAL samples (a swing-flamenco, b balkan-brass-swing, c trombone-flamenco-jazz) + the owner's two SUNG Lyria songs from 10-14 (/data/work/belam-media: three-of-three, nothing-gets-deleted-here = Drive agi/season3-rollover-report/song-b.mp3; lyrics suno-songs.md), all sent 14:3xZ; the owner says more Suno songs + narrated clips + a first video exist on the grok-bot box and will bring them | the owner picks or brings material; no new track until then |
| .45 director-review first start: ONE owner login for the new post (agi.sh start S6 [owner-do], or /login in its pane) | show the one command when the owner is back and G2's other parts are done |
| .45 role templates: scopes are the Prime's reading (goals = goal stewardship that runs falsifiers and proposes closes; science = hypotheses, experiments, verdicts; review = presentation creation + checking deliverables) | owner confirms or corrects |
| g5.4.2 voice: the council picked by a pre-registered rule under "do your best" | show the owner the pilot + the README in deliver/ |
| ElevenLabs direct account: none; Voice Design route OFF | revisit if the owner gets a key |
| the owner's complex-analysis project spends on the OPENROUTER_ADMIN account | per-key settled usage is the figure |
| 657 refs/archive/worktrees/* in MAIN; refs/grid on E vs L differ by 5,845 | keep local + bundle; owner picks |
| claude upgrade turns every post's hooks off (settings.json 'tui') | pin posts to a root-owned copy; move the pin only after the hooks-loaded proof |
