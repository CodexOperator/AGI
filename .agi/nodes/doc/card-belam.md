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
thought_session: belam-s3-II
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town = this box, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs. Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate · design-taste-frontend (vendored, ~/.claude/skills).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s3-II woke 08:07Z 10-16: the watcher had died with the rotation (it lived in agi-post@belam's cgroup), so it now runs as its own transient system unit; P2 disabled, the two walk keys minted on SM's 08:05:56Z word.
<!-- THOUGHT:END -->

## §0 State (08:1xZ 10-16)
| | |
|---|---|
| trunk | core/season3/main = MAIN's checkout = every post's AGI_TRUNK; season3/main = my PASS line (2a8056bcb5); core/main ff-fed from season3/main after a PASS (ahead = RED). Last PASS base 2a8056bcb5; N ~45, experiments landed 0 (only L27's two R100 moves) |
| pin | /etc/agi/carry.env AGI_TRUNK = fa3174300d (boot:true DG2-5); backup carry.env.pre-fa31-*; /run wants 12, /etc wants 0 (agi-boot projects them) |
| me | uid agi-belam SIGNS and PUSHES: ~/.gitconfig credential.https://github.com.helper = '' then '!sudo -n -u belam /usr/bin/gh auth git-credential' (owner 10-15 "both the power to sign and the power to push"); R1' prefix retired; sudo NOPASSWD ALL kept (owner, council withdrew F5) |
| landing my commits | `AGI_POST=belam agi-at <paths>` -> `sudo -n -u belam git -C /data/work/agi merge --ff-only -q refs/heads/posts/belam` -> `git -C /data/work/agi push -q origin <sha>:refs/heads/core/season3/main refs/heads/posts/belam:refs/heads/posts/belam`. The :28 board land refuses non-job commits until goal .42.2 lands |
| landing SM's L<n> | ~/tools/verify-land.sh takes the ref name `L<n>` (not `<n>`): held, tree, parents, G, D, anonymize, home, gpu; then ff MAIN, CAS posts/belam to it, push both, `git checkout -q --detach` in ~/t |
| crons | CHECK 13 */4 (session-only: re-arm at wake, CronList first) |
| T3 quiet by design | TM + DT-1 PARKED (TM 08:4xZ 10-16: no dispatchable research until a box has >= 8 GB + docker/GPU, or the owner moves g5.28; "you can stop asking"). .44.7 waits on .44.8 S3 by design (SM 08:47Z) |
| Drive | rclone remote `gdrive:` (scope drive.file, agi-belam ~/.config/rclone, mode 600) = the OWNER's Drive folder `agi` (https://drive.google.com/drive/folders/1ZKskZRNkGqok7TuZMj-VfGjwmSAjExJc): explainer 17:32 + MV + rollover report already there |
| WATCHER | ~/drive-deliver.sh as transient unit `drive-deliver.service` (User=agi-belam; survives rotations, NOT a reboot: `sudo -n systemd-run --unit=drive-deliver -p User=agi-belam -p Group=agi-belam --setenv=HOME=<the post home> /bin/sh ~/drive-deliver.sh`). Uploads finished files in /data/work/director-general-3-media/season3/deliver/ to gdrive:agi/season3-media/{explainer,voice-samples,music,html}/, md5-checked; joins explainer-chNN-*.mp4 into explainer/00-explainer-full-so-far.mp4 each time one lands; state + log in ~/.drive-deliver/; stops 10-23 |

## §1 Plan
```
1. MAIL: AGI_POST=belam box read; belam mails SM only (TM stood down 10-21) (DG3 is off-matrix: relay through SM)
2. g5.4.2 media (DG3, council designs first): mint each DG3 stage key on SM's [word]:
   limit = planned + $0.50 (audio needs >= $0.50 remaining or HTTP 402); expires_at in the POST (+60 min, walk keys = walk x2 + 30 min),
   read back non-null; list ENABLED keys on BOTH accounts (OPENROUTER_ADMIN: Default key; AGI_WORKSPACE_PROV_KEY: agi-et-runtime, agi) first;
   write into DG3 ~/keys/<name>.key (dir 700, file 600, `sudo -n -u agi-director-general-3 sh -c "umask 077; cat > ..."`); never print a value
   at DG3's [done]: PATCH disabled=true, read back, shred the file. Settle (~/tools/settle-read.sh, re-run its loop): GET /keys?include_disabled=true&include_expired=true (plain /keys HIDES disabled AND expired ones);
   two agreeing NON-ZERO reads >= 30 min apart, never < mint + 3 h; a 0 then = UNSETTLED at full cap, never delete (council's word to delete)
   WALK DONE 09:07:48Z (18/18 COMPLETE, 36 files; the C15 flag was a FALSE RED: the transcriber wrote '47%', council 09:13Z); walk keys DISABLED 09:09Z + shredded, no dg3-* key live.
   SETTLED: 10 dg3-* keys = $1.397 (walk-tts 0.7807, round3 0.2319, music 0.12, walk-stt 0.1051 ...), goal:g5.4.2 Agent Notes; music settled 09:53Z 10-21, round3 re-read +0.0006 late usage
   M4 animated / M5 HTML / M6 music wait on the council's word: mint each stage key on SM's [word] as above
3. CHECK every 4 h (skill agi-merge-pass §1): T1-T3, then A-C; ONE line when nothing changed
4. PASS when experiments landed > 0: merge core/season3/main into season3/main, ff core/main, read back
```

## §2 Landed (10-15 .. 10-16)
B-3 overwrite 08:10Z 10-15 · L26 a93fe7cf36 · season 3 opened 19:2xZ 10-15 (.44.8 agi.sh + g5.4.1 report template, council design first) · boot pin fa3174300d · L27 fe2b6d3991 (DG3 retire = status + move) · L28 1cb54e68f0 09:1xZ 10-16 (.44.8 S1: agi.sh status/stop, box town up|down, crons.py remove --user) · L29 7965c4fe8c 11:2xZ (.20.3 captive releases an unusable fill window) · L30 3a91789da4 06:1xZ 10-21 (g12.3 season_history rows) · L31 1ce5eb7bb0 08:2xZ (.44.8 S2a: host act folds into agi.sh host; NO live host act until S2b owner/SM GO) · L32 c61f350cf1 09:2xZ (g12.3 season row idempotent on a resumed rollover) · L33 50d5ce0673 09:4xZ (g5.4.1 S1 season report template + facts reader, not wired yet) · L34 390eaa55be 11:4xZ (.42.2 own node commits on posts/belam land at the :28 job) · L35 5e5fe7cdda 12:3xZ (.44.8 S2b agi.sh start + skill agi-town; NO live host/start until one more DG2 commit + owner/SM GO) · L36 3a9483a13f 14:1xZ (.44.8 S2b follow-up; still NO live start: one more DG2 commit B-7/H1) · L37 363ab2c0b0 14:1xZ (.31.1 warm-load test, spy loader) · L38 2063a88cc5 14:4xZ (.31.1 CLOSE) · L39 f5541e638f 15:0xZ (.44.8 S2b bind: B-7 trigger skip, reaper guard removed; NO live start/stop yet) · L40 7f9f2e2a61 15:2xZ (.45 R1: TM + DT-1 boot false) · L41 4230313395 15:4xZ (.45 T: role templates v1.1) · L42 9e01ddc8d2 15:5xZ (.44.8 (iii) oneshot rule + pidchk; no live stop yet) · L43 08e9aea156 16:2xZ (.45 S1: director-review row boot false + card + seeds test; post-move-checks.sh) · L44 4363277b5c 16:3xZ (.45 K-a/b/c: CHECKS script ready for G3 + runbook in skill agi-post §8) · goals cut: .42.2 (:28 lands Prime commits), .31.1 (warm-load test), .20.3 (captive lock), g5.4.2 (media set) · taste skill vendored /data/work/skills-vendor/taste-skill@f624f37a8c · Node 22 /opt/node22 + Chrome for Testing /opt/chrome-cft (/usr/bin/chromium, AppArmor /etc/apparmor.d/chrome-cft for its sandbox)

## 🔴 Where it stops
RESUMED 06:1xZ 10-21 (owner: "Resume everything", after all 12 posts restarted together ~06:08Z; the 10-16 PAUSE is lifted); 06:14Z the owner chose "Keep whole town" over the "Wake SM only" he gave in alive's session: crons_live true c5e968e525 + apply incl --sudo; keepalive + quiet-watch timers enabled; CHECK cron 64875a4a; [owner] RESUME boxed to SM + TM. The restart dropped the github credential again (trap 114: re-added). Watcher still up (stops 10-23).
POST SHUFFLE (owner GO 14:4xZ 10-21, goal:g7.16.1.11.45, owner away a few hours): director-review under SM (presentation work); DG1->director-goals-1, DG2->director-science-1, DG3/4/5->DG1/2/3; TM + DT-1 down. A name = user, home, branch, unit and principal, projected from posts.md at the pin: rename = new identity + carried card, old row retired off-box, home moved aside (never rm). SM asked 14:5xZ for council design + stack S1 (director-review) / S2 (renames) / S3 (my runbook); TM + DT-1 DOWN 14:4xZ (cards 0120b6b42b + fd9a987d85, G; agi-post@ + agi-boxwake@ stopped; no crontabs); boot-false = R1, LANDED as L40 7f9f2e2a61; BUT the live boot pin (carry.env AGI_TRUNK) is still fa3174300d where both read boot true: a REBOOT starts them until the pin bump (an owner/SM GO host step) -> re-stop them on any restart. Council 14:44Z: renames = design B (usermod -l/groupmod keep the uid, fresh key, old key retired + stamped valid-before); S1 + CHECKS on DG5; each move only on SM's GO. belam mails SM only now.
COUNCIL OWNS THE .45 SCHEDULE (15:25Z + addendum 15:26Z): G0 gates land -> G1 TM+DT-1 down -> G1b pin bump -> G2 director-review start (owner login) -> G3 DG1->goals-1 -> G4 DG2->science-1 -> G5 DG3->DG1 -> G6 DG4->DG2 -> G7 DG5->DG3; each GO = a council [decision] via SM. carry.env has ONE writer: `sudo PIN=<landed sha> sh agi.sh host` (never a hand edit); GO for each bump needs (a) my agi-project DRY projection at the PIN (adds/changes/drops, users sysusers would create) + (b) the ROOT rehearsal (ROOT=<scratch>, AGI_HOST_UNITS=<stub>). PER MOVE: 0 card -> 1a stop post + boxwake -> 4a rows+cards commit LANDS via SM's gate while down -> ONE sitting, root only: 1b usermod -l + groupmod -n, 2 old key to retired/keys + valid-before stamp, 3 refs/branch/crontab/linger/worktree repair, 4b agi.sh host at the landed sha -> CHECKS (+ getent passwd/group agi-<old> empty, no agi-post@<old> active). Any RED = stop, council rules. G1b: PIN a18c484bc4 (council 16:53Z); (a)+(b) sent 17:0xZ (one new user agi-director-review; /etc changes = carry.env, host.done, /opt/agi/bin/box; no unit restarted; scratch in my scratchpad g1b/). GO after GATE121 (~18:05Z) on the council's [decision]: `sudo PIN=a18c484bc423b6d75a5c2cb4b8c5551b1b9a4cf3 sh extensions/agi/bin/agi.sh host` from ~/t at the PIN, then re-run = host: met. Templates v1.1 LANDED L41 4230313395.
NEXT COMMAND: AGI_POST=belam box read

## §4 Traps (this generation's only)
| # | trap | rule |
|---|---|---|
| 108 | an unquoted heredoc ate every $ figure in goal:g5.4.2 ("$15" -> "5") | every node body through a QUOTED heredoc (<<'EOF'), values patched in after |
| 109 | `pgrep -f <name>` / `pkill -f '...rclone authorize'` match the calling shell's own command line (a false "already running", exit 144) | match the exact argv: `ps -u agi-belam -o pid,args | grep '[d]rive-deliver.sh$'` |
| 110 | a temp token file shredded before rclone confirmed it: the one-use OAuth code was lost, the owner signed in twice | keep a credential copy until the consumer proves it works, then shred |
| 111 | the agi-at reset leaves a STALE town:local-maxxing metrics line in ~/t (twice) | `git restore --source=HEAD --staged --worktree -- .agi/nodes/town/local-maxxing.md` (it is older data, in git) |
| 113 | a setsid'd watcher still dies with the post: agi-post@<post> stops its whole cgroup at rotation | anything that must outlive the post runs as its own unit (`sudo -n systemd-run --unit=...`) |
| 114 | ~/.gitconfig was rewritten 08:05Z 10-16 (the rotation) without the github credential lines: push -> 'could not read Username' | at wake: `git config --global --get-all credential.https://github.com.helper` must print '' + the gh line; else re-add both |
| 115 | verify-land anon-diff=1 on L28 = systemd unit names (`agi-post@dg2.service`, `agi-carry@a.path`) read as emails | list the hits (`/usr/bin/grep -oE` on the diff, ugrep chokes on the pattern); land only if every hit is a unit name |
| 116 | settle-read at 11:17Z returned NO dg3-* key: an expired key leaves /keys?include_disabled=true (the lag also hid ~$0.6 of the walk at 09:09Z) | always `&include_expired=true` (fixed in ~/tools/settle-read.sh); GET /keys/<full hash> still answers |
| 117 | the 14:12Z 10-21 memory warn was MY `sudo find /data/work /var/lib/agi` (it outlived its 2-min tool timeout and filled the dentry slab to 1.7 GB) | never walk those trees with find: ask the post for the path, or `git -C <its tree> log --all -- '*name'`; kill a timed-out walk |
| 112 | a box mail carried this box's host name (public repo) | write "this box" in mail and nodes; the owner does not mind it much (10-16), history left as is |

## §5 Verification
08:1xZ 10-16: enabled keys = ADMIN {walk-tts, walk-stt, Default}, WORKSPACE {agi-et-runtime, agi}; drive-deliver.service active, uploaded r2-bill-p2 08:08:50Z md5 ok · 08:0xZ 10-16: MAIN == posts/belam == origin core/season3/main (latest belam commit 7d21bd5c80 + this card) · 12 agi-post@ active · watcher alive, 2+ files uploaded md5 ok · enabled stage keys: P2 only

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| g5.4.2 voice: the council picks under the owner's "do your best" by a pre-registered rule (native pin if two takes <= 100 Hz within 5%, else c2a normalised to 100 Hz; 91 Hz + raw banked); the owner overrules on waking | show him the pilot + the README in deliver/ first |
| g5.4.2 walk: 18/18 chapters on Drive (gdrive:agi/season3-media/explainer/, joined as 00-explainer-full-so-far.mp4); C15 complete (its flag = the transcriber writing 47%); open: "sed" -> "said"; M4 animated / M5 HTML / M6 music wait for the council | tell him on waking; nothing for his ears in C15 |
| council §Y2: should posts mint through captive fill windows at all; agi-fill is on no post's PATH | no for now: write the node file + agi-at |
| g5.4.2 M6: three ~30 s INSTRUMENTAL style samples on Drive music/ (a swing-flamenco, b balkan-brass-swing, c trombone-flamenco-jazz; README-music.txt has the prompts); key settled $0.12; sent to the owner 14:3xZ 10-21 with the owner's own two SUNG Lyria songs from 10-14 (/data/work/belam-media: three-of-three 2:59, nothing-gets-deleted-here 2:23, = Drive agi/season3-rollover-report/song-b.mp3; lyrics in suno-songs.md) | the owner picks a sample, one of the existing songs, or none; no new track until then. Owner 10-21: keep needrestart as is (it restarted the town 06:08Z on a liblzma update) |
| .45 director-review first start (council 14:44Z): ONE owner login for the new post (agi.sh start S6 [owner-do], or /login in its pane) | when the owner is back and S1 has landed: show the one command; nothing else needs a login (renamed posts keep theirs) |
| .45 role templates (owner 15:1xZ: "create new templates as needed for these directors as they'll be used elsewhere"): doc:role-director-review / -goals / -science landed d12c41d80f, council reviewing | owner confirms the scopes: goals = goal stewardship (shape, leaves, honest status); science = hypotheses, experiments, verdicts; review = presentation creation + checking deliverables |
| ElevenLabs direct account: none (owner 10-16); Voice Design route OFF | revisit if he gets a key |
| the owner's complex-analysis project spends on the OPENROUTER_ADMIN account | the account delta is contaminated; per-key settled usage is the figure |
| history rewrite for the host name | none (owner: "I don't care about host name as much") |
| 657 refs/archive/worktrees/* in MAIN; refs/grid on E vs L differ by 5,845 | keep local + bundle; reconcile into a namespace; owner picks |
| claude upgrade turns every post's hooks off (settings.json 'tui') | pin posts to a root-owned copy; move the pin only after the hooks-loaded proof |
