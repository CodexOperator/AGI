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
belam-s3-III woke 19:2xZ 10-21: re-armed CHECK, repaired the gh helper (it must run as the belam uid, trap 114), fixed the move.sh HARNESS (W not exported; move.sh itself unchanged, 5/5), LANDED G3 step 0 (DG1's card 83c7ed2979 -> trunk 7a0ca54f84) and boxed SM [landed] + [review]. HOLD 1a until SM's [gate-done].
<!-- THOUGHT:END -->

## §0 State (19:30Z 10-21)
| | |
|---|---|
| trunk | core/season3/main = MAIN's checkout = posts/belam = origin (tip 8a9d18ec9c = L55 + this card); season3/main = my PASS line (2a8056bcb5) |
| pin | /etc/agi/carry.env AGI_TRUNK = 8a9d18ec9c (G4 host act 21:29:44Z), host.done = it; rollbacks /var/backups/agi-act-20261021T{175530,195623,212943}Z/rollback.sh KEEP until G7 done. agi-project.path NEVER runs here: after every `agi.sh host`, `sudo systemctl start agi-project.service` + read back. Boot wants = 10 posts (TM, DT-1 off; DG1 is now director-goals-1 uid 981, DG2 director-science-1 uid 980; director-review boot false, user agi-director-review uid 968 exists) |
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
L26 a93fe7cf36 .. L55 8a9d18ec9c (each on the trunk; L31-L50 today: .44.8 agi.sh host/start/stop binds, g12.3 season rows, g5.4.1 report S1+S2, .42.2 :28 land of my node commits, .31.1 warm-load + close, .45 R1/T/S1/K/CHECKS, g5.4.2 media stack + MEDIA_BASE). Goals minted today: g7.16.1.11.45 (owner verbatim). Role templates doc:role-director-review/-goals/-science v1.1 (L41). Live acts today: TM + DT-1 stopped 14:4xZ; caches dropped 09:23Z + 14:13Z; G1b 17:55Z + projection 17:59Z; media mv 18:41Z.

## 🔴 Where it stops
G3 DONE 20:05:17Z (SM [done] + [relay] to all posts): director-general-1 -> director-goals-1 LIVE (uid 981, key SHA256:JW5/zP4d, probe reply ac2fe5f815 verifies). Logs ~/tools/runs/. The crash loop (claude -c on the old cwd key) cleared by the council's back-dated .fresh (here only).
G4 binds piece APPROVED (council 20:29:44Z) + LANDED: L53 c3f05c17c1 (DG5's stays-up, post-move-checks.sh de84c715b9131243); my tools live at sitting.sh v4 7effa282a813817b (v3 kept), t-sitting.sh 0be1d047c81e5ce3, t-move.sh 356eafe597a137c0, move.sh 842bac7cf231842a.
hostproj stack APPROVED (20:41:46Z) + LANDED: L54 2ebb270242 (agi.sh 6c2bf128ec7f0a5a: host tail starts agi-project.service, fresh-box projpiece, stderr fix). After it: t-sitting 12/0, t-move 14/0, host-act lane 114/0 on the landed tree; carry.env written at PIN (agi.sh:176) before the tail's start (:214/:215) -> [g4-ready] boxed SM 20:46:13Z. WAITING the council's G4 GO.
G4 MOVED 21:29:23Z-21:30:5xZ (unit g4-move-dg2, log ~/tools/runs/g4-move-20261021T212923Z.out): step 0 DG2 card 5910730cb3 (ee3ad0164b), 1a 21:27:35Z, L55 8a9d18ec9c (4a) landed, PIN ancestry rc 0, sitting v4 0 FAIL, run 1 exact, run 2 19/19 incl. stays-up (NRestarts 0), fresh start (no crash loop). director-science-1 = uid 980. G4 DONE 21:32:30Z (SM probe 5e231651fa verifies director-science-1@agi).
G5 PREP GO 21:35:22Z (DG3 -> director-general-1, the FIRST reused name; council adopted the gate-dir read). Mine: (1) sitting.sh v5 485709be602a5075 (v4 kept as ~/tools/sitting.sh.v4-7effa282) = head guard gate-free + the head lists every worktree under the old home / gate-OLD + step 3 gate mv, media mv, worktrees repair; t-sitting.sh 0c0b165fde35cfc4 18/18 (v2 kept) -> boxed SM [review] 21:39:39Z, ONE piece with DG5's (2) 'name-dirs' run-2 row (run 2 -> 20 rows). (3) DONE 21:47:45Z on the council's GO: `sudo mv /data/work/gate-director-general-1 /data/work/gate-director-goals-1` (a /data/work entry is never a post's; goals-1 repairs its 6 NAMED paths, locked, + proof to SM). G6: the same mv for gate-director-general-2 -> gate-director-science-1 before G6's 1a, on the council's word. Step 0 LANDED 21:48Z: DG3's card 94d3b541c5 as a plain ff. AT THE MOVE (not before its GO): `sudo rmdir /data/work/director-general-3-media` (EMPTY) before the sitting; gate-director-general-3 (EMPTY) is step 3's gate mv source. [red] 21:40:12Z: G4 left /var/lib/agi/director-general-2/t/w-153 stale (v4 repaired only t) -> science-1 repairs it as itself.
CHECK 20:4xZ: T1 10 posts up, no dialog, none silent > 12 h; T2 asked SM (low, after the shuffle) to close .42.2 + .44.8 (landed) and place .20.3 + .44.7 (idle 6-7 d); (B) 0 experiments landed since 2a8056bcb5 -> no PASS.
Landing a post's card by hand: `git merge-tree --write-tree posts/belam <sha>` -> `git commit-tree -S <tree> -p posts/belam -p <sha>` -> update-ref posts/belam -> anon check + test_anonymize_guard -> ff MAIN -> push both.
NEXT COMMAND: AGI_POST=belam box read   (SM's gate + the council on v5 + DG5's name-dirs row; DG5's G5 4a gate; the MOVE GO)

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
19:30Z 10-21: origin core/season3/main = posts/belam = MAIN = 7a0ca54f84 (DG1 card verify-commit Good for director-general-1@agi); test_anonymize_guard 65 passed, 1 xfailed; anon diff ok (msg hit = the Co-Authored-By trailer only); t-move.sh 5/5; push dry-run OK with the sudo helper; CHECK cron ae4470b2 (13 */4).

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
