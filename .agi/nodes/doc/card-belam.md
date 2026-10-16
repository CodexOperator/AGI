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
thought_session: belam-s3-I
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town = this box, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs. Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate · design-taste-frontend (vendored, ~/.claude/skills).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s3-I rotating out 08:0xZ 10-16 at the context line. Season 3 is open and running on the owner's words; the owner went to bed 07:5xZ ("just do your best") and said usage is nearly out ("if not see you next week"), so the delivery of the g5.4.2 media was moved onto a Claude-free watcher before this rotation.
<!-- THOUGHT:END -->

## §0 State (08:0xZ 10-16)
| | |
|---|---|
| trunk | core/season3/main = MAIN's checkout = every post's AGI_TRUNK; season3/main = my PASS line (2a8056bcb5); core/main ff-fed from season3/main after a PASS (ahead = RED). Last PASS base 2a8056bcb5; N ~45, experiments landed 0 (only L27's two R100 moves) |
| pin | /etc/agi/carry.env AGI_TRUNK = fa3174300d (boot:true DG2-5); backup carry.env.pre-fa31-*; /run wants 12, /etc wants 0 (agi-boot projects them) |
| me | uid agi-belam SIGNS and PUSHES: ~/.gitconfig credential.https://github.com.helper = '' then '!sudo -n -u belam /usr/bin/gh auth git-credential' (owner 10-15 "both the power to sign and the power to push"); R1' prefix retired; sudo NOPASSWD ALL kept (owner, council withdrew F5) |
| landing my commits | `AGI_POST=belam agi-at <paths>` -> `sudo -n -u belam git -C /data/work/agi merge --ff-only -q refs/heads/posts/belam` -> `git -C /data/work/agi push -q origin <sha>:refs/heads/core/season3/main refs/heads/posts/belam:refs/heads/posts/belam`. The :28 board land refuses non-job commits until goal .42.2 lands |
| landing SM's L<n> | scratchpad verify-land.sh takes the ref name `L<n>` (not `<n>`): held/tree/parents/G/D/anonymize/home/gpu; then ff MAIN, CAS posts/belam to it, push both, `git checkout -q --detach` in ~/t |
| crons | CHECK 13 */4 (session-only: re-arm at wake, CronList first) |
| Drive | rclone remote `gdrive:` (scope drive.file, agi-belam ~/.config/rclone, mode 600) = the OWNER's Drive folder `agi` (https://drive.google.com/drive/folders/1ZKskZRNkGqok7TuZMj-VfGjwmSAjExJc): explainer 17:32 + MV + rollover report already there |
| WATCHER | /var/lib/agi/belam/drive-deliver.sh, setsid, no Claude (pid 1648835 at 08:0xZ; a reboot kills it: restart `setsid nohup /bin/sh /var/lib/agi/belam/drive-deliver.sh >/dev/null 2>&1 </dev/null &`). Uploads finished files in /data/work/director-general-3-media/season3/deliver/ to gdrive:agi/season3-media/{explainer,voice-samples,music,html}/, md5-checked; joins explainer-chNN-*.mp4 into explainer/00-explainer-full-so-far.mp4 each time one lands; state + log in ~/.drive-deliver/; stops 10-23 |

## §1 Plan
```
1. MAIL: AGI_POST=belam box read; belam mails SM + TM only (DG3 is off-matrix: relay through SM)
2. g5.4.2 media (DG3, council designs first): mint each DG3 stage key on SM's [word]:
   limit = planned + $0.50 (audio needs >= $0.50 remaining or HTTP 402); expires_at in the POST (+60 min, walk keys = walk x2 + 30 min),
   read back non-null; list ENABLED keys on BOTH accounts (OPENROUTER_ADMIN: Default key; AGI_WORKSPACE_PROV_KEY: agi-et-runtime, agi) first;
   write into DG3 ~/keys/<name>.key (dir 700, file 600, `sudo -n -u agi-director-general-3 sh -c "umask 077; cat > ..."`); never print a value
   at DG3's [done]: PATCH disabled=true, read back, shred the file. Settle: GET /keys?include_disabled=true (plain /keys HIDES disabled ones);
   two agreeing NON-ZERO reads >= 30 min apart, never < mint + 3 h; a 0 then = UNSETTLED at full cap, never delete (council's word to delete)
   NEXT now: P2 56120eb9f6 (temperature 0) is LIVE until 09:03:16Z -> DISABLE at DG3's [done]; then the 2 WALK keys (TTS + STT) on SM's word
3. CHECK every 4 h (skill agi-merge-pass §1): T1-T3, then A-C; ONE line when nothing changed
4. PASS when experiments landed > 0: merge core/season3/main into season3/main, ff core/main, read back
```

## §2 Landed (10-15 .. 10-16)
B-3 overwrite 08:10Z 10-15 · L26 a93fe7cf36 · season 3 opened 19:2xZ 10-15 (.44.8 agi.sh + g5.4.1 report template, council design first) · boot pin fa3174300d · L27 fe2b6d3991 (DG3 retire = status + move) · goals cut: .42.2 (:28 lands Prime commits), .31.1 (warm-load test), .20.3 (captive lock), g5.4.2 (media set) · taste skill vendored /data/work/skills-vendor/taste-skill@f624f37a8c · Node 22 /opt/node22 + Chrome for Testing /opt/chrome-cft (/usr/bin/chromium, AppArmor /etc/apparmor.d/chrome-cft for its sandbox)

## 🔴 Where it stops
belam rotates 08:0xZ 10-16 at the line; P2 key 56120eb9f6 is live for DG3 (disable at its [done]), the walk keys come next on SM's word; delivery to Drive runs Claude-free.
NEXT COMMAND: AGI_POST=belam box read

## §4 Traps (this generation's only)
| # | trap | rule |
|---|---|---|
| 108 | an unquoted heredoc ate every $ figure in goal:g5.4.2 ("$15" -> "5") | every node body through a QUOTED heredoc (<<'EOF'), values patched in after |
| 109 | `pgrep -f <name>` / `pkill -f '...rclone authorize'` match the calling shell's own command line (a false "already running", exit 144) | match the exact argv: `ps -u agi-belam -o pid,args | grep '[d]rive-deliver.sh$'` |
| 110 | a temp token file shredded before rclone confirmed it: the one-use OAuth code was lost, the owner signed in twice | keep a credential copy until the consumer proves it works, then shred |
| 111 | the agi-at reset leaves a STALE town:local-maxxing metrics line in ~/t (twice) | `git restore --source=HEAD --staged --worktree -- .agi/nodes/town/local-maxxing.md` (it is older data, in git) |
| 112 | a box mail carried this box's host name (public repo) | write "this box" in mail and nodes; the owner does not mind it much (10-16), history left as is |

## §5 Verification
08:0xZ 10-16: MAIN == posts/belam == origin core/season3/main (latest belam commit 7d21bd5c80 + this card) · 12 agi-post@ active · watcher alive, 2+ files uploaded md5 ok · enabled stage keys: P2 only

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| g5.4.2 voice: the council picks under the owner's "do your best" by a pre-registered rule (native pin if two takes <= 100 Hz within 5%, else c2a normalised to 100 Hz; 91 Hz + raw banked); the owner overrules on waking | show him the pilot + the README in deliver/ first |
| council §Y2: should posts mint through captive fill windows at all; agi-fill is on no post's PATH | no for now: write the node file + agi-at |
| ElevenLabs direct account: none (owner 10-16); Voice Design route OFF | revisit if he gets a key |
| the owner's complex-analysis project spends on the OPENROUTER_ADMIN account | the account delta is contaminated; per-key settled usage is the figure |
| history rewrite for the host name | none (owner: "I don't care about host name as much") |
| 657 refs/archive/worktrees/* in MAIN; refs/grid on E vs L differ by 5,845 | keep local + bundle; reconcile into a namespace; owner picks |
| claude upgrade turns every post's hooks off (settings.json 'tui') | pin posts to a root-owned copy; move the pin only after the hooks-loaded proof |
