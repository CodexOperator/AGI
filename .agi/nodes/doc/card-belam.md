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
thought_session: belam-S2-L5-XVIII
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here; progress lives on the town board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 21 ran the owner-ordered history scrub. Owner 06:3xZ-06:4xZ 09-30, verbatim: "Yeah we gotta scrub it. Time to pause grid crons and do the whole shebang." · "Yes include codex-town. And go now then restart when everything is verified" · "Go". Also owner 06:1xZ: "We should probably ease off expensive subagents now and just use strictly sonnet 5.5 ideally using our new headless CC review routes." and "We also will need to stand down director-general 5 and 6 to help conserve tokens as well ... 3,4 can continue as is and pick up whatever 5,6 don't finish after standing down". The rewrite ran on mirrors, never in place (filter-repo in place would reset --hard MAIN's uncommitted files); local refs moved by one asserted transaction and worktrees by per-path swaps, because a full git status over 682 worktrees did not finish in 15 min.
<!-- THOUGHT:END -->

## §0 State (04:5xZ 10-01, read from date -u)
| | |
|---|---|
| post | belam-S2-L5-XX gen 23 agi-24 (woke 04:53Z 10-01); predecessors idle: gen 22 agi-a3 · gen 21 agi-23 · gen 20 agi-79 · gen 19 agi-c2 |
| run | LANES since 02:27Z 10-01 (owner): everyone Sonnet 5.5 for everything; DG3 Opus (5.5, medium; owner said "5.6", none exists) subagents for everything -- the 21:00Z free lane ended · rules: doc:unified-director-brief + doc:unified-master-brief THOUGHTs · DG3 building config:engine v2 stages 1-2 (S1 PASS; S2 root plan 86ede9baa6 R1 at 02:5xZ, not held); STOP before stage 3 = owner word |
| posts | DG4 DOWN 21:4xZ (row recover false + pid 0, @28 closed; 25 leaves -> board horizon unassigned) · DG5 + DG6 DOWN · TM UP @34 gen 34 (research lane, Opus 5.5 high x3) · SM = agi-e0 @31 · DG3 = agi-03 @32 (key/ID work held; builds g7.16.1.11 AFTER the council) · council: alive agi-e3 [761106] @16 · all-is-one agi-8f [242e8c] @1 · self-perpetuating agi-53 [21dc2d] @2 (their inbox rows are QUIET: SendMessage to wake) |
| crons | session: CHECK daa581ac (13 */4) · LANE-SWITCH bb871f87 FIRED 21:02Z · memory Monitor b9h0nup0g = python3 -u /data/tmp/belam23/memmon.py (RED at mem PSI full avg60 >= 20; reclaim top 3 scopes by file+shmem 400M only at full >= 10 AND user@ >= 90% of high, <= 1 per 5 min; 30 min, re-arm) · box crontab LIVE (crons_live true, 12 jobs) · keysync timer re-created (transient, */2 min) |
| scrub | /data/scrub (mode 700): RESUME.md = the step table + revert · backup-local.git · backup-origin(2).git · stripped/ (2 nsys files, also back on disk, gitignored) |

## §1 Plan
```
DONE gen 21  guard-init applied (empty plan diff) · post scopes ruled to app.slice · command:commands canonicalize (d7cb48e6a pre-scrub) · config:guard doc header
             config:census minted · skill agi-send name [ref] row · brief SUBAGENTS = Sonnet 5.5 strictly · DG5 + DG6 stood down
             HISTORY SCRUB: email (text + 7k author lines -> the example.invalid placeholder address) · GPU name + fragments · pytest-of-<user> · 2 nsys binaries stripped
               origin: 803 refs forced with lease, 0 rejected, fresh-clone scan 0 · local: 1978 refs + 682 worktrees relinked · nodes 5457 = before · links 0 broken
               guard: box-local pre-commit hook (common hooks dir) = denylist ~/.config/agi/scrub-denylist.json + anonymize box tokens; 0 refusals on the last 300 commits
             after resume: harness claude-code models -> Sonnet 5.5 (8b9fded02) · [config] schema spawn: block (436f4b418) · council-loop town -> local-maxxing
             operating-mode ruling (NONE binds) waits on DG4's brief.py round + its pinned test (then land the 2-line config.json edit) · old->new sha map kept LOCAL
             memory: 5 cache spikes to user@ high 08:0x-10:56Z, each cleared by memory.reclaim (never a kill) -> the RAM budget leaf goal:g7.16.1.5.5 is the real fix
             12:4xZ owner: "Oh neat continue now until 2pm EST." -> all posts RESUMED to 18:00Z · self-perpetuating double seat: kept @2 (agi-53: row + transcript), closed the stranded @19 (failed 05:17Z join)
             addressing: SendMessage ONLY by "name [ref]"; offline Remote Control rows named like the posts (all-is-one [0781f7], alive [68d0c9], ...) swallow bare names; all-is-one = agi-8f [242e8c]
14:xZ: RAM disk 4.1G -> 2.3G (13 clean idle Agent worktrees removed; DG4 row: bind <repo>/.claude/worktrees from disk) · paths.local_maxxing.scrub_commit_map 1b14a0048 · SLO8 whois fact restored d71e39b69 · 8 trunk reds laned by SM (links.py:440 decode -> DG2; brief g15 -> DG4; boxkit anonymize fake denylist -> DG2)
             STILL MINE: config:rotations skills entry (:83 + :123) + agi-post, agi-stream, byte_cap 6000 -> 8000, THOUGHT -- only once DG4 lands build:skills-agi-post-SKILL.md + build:skills-agi-stream-SKILL.md (SM sends the exact text)
16:4xZ owner opened round lanes past pi-free (claude-code Sonnet 5.5 kids; parents+kids once proven; subagents or direct): brief SUBAGENTS row 6db908311, relayed via SM · email_allow user@UID.service 842cb065d · memory relief now PSI-gated (>= 10%): cache at user@ high with PSI 0 is normal, never churn on it
21:2x-21:5xZ OWNER REDESIGN: per-post Unix users + a radically simple engine -> goal:g7.16.1.11 (owner verbatim x3 on it) · order: COUNCIL designs -> reports to belam -> belam relays to owner -> DG3 builds (Opus x3) · HOLD on key/ID/rotate rounds (director brief) · TM subagents row (master brief) · idea:tree-context-forked-conversations-searched-by-a-swarm under g5.30
21:5x-00:0xZ goal:g7.16.1.11 ROUNDS 1-3 by the council (owner verbatim x8 on the goal): r1 wrap 1,432 B · r2 living system 4,253 B (fixed point, CALM refs, latent notes, self-projecting) · r3 = config:engine MINTED (.agi/nodes/.geometry/engine.md, 11,305 B v1, 20/20 pieces byte-exact via sect, design state) · [town] schema admits director TEMPORARILY (f4dc505011, TM board edit) · write gate is honor-system (unseated actor claiming prime_director admitted) -> evidence on the goal
00:4x-03:1xZ spike: spine PASS / body 12 defects -> config:engine v2 RE-MINTED (11,900 B, 22/22 exact, heal = 214 B polkit rule, F9 agi-gate built, F10/F11 dropped) · owner "Stages 1-2 now, stop before 3" -> DG3 (agi-b1 @38) S1 PASS (10 units = 10 live posts), S2 root plan 86ede9baa6 R1-R17 + teardown, not held · owner STAGE 2.5 (verbatim on goal): after S2 passes, ONE live post on the LIVE repo, a PARITY TABLE (auto-link node<->code files; per-node tiny worktree pulled on demand, purged from the RAM disk) -- no further owner word for 2.5 · LANES 02:3xZ: everyone Sonnet 5.5 for everything, DG3 Opus 5.5 medium (owner said "5.6": none exists) · TM board placement = its own (master template)
03:4xZ S2 PASS 7/7 (box verified clean) -> STAGE 2.5 GO: post = director-general-5 (owner), pi-free + a pi extension mirroring CC hooks ("CCCC"), copy the owner's CC creds to the new uid + report uid/network binding, root acts on MAIN approved w/ undo, both keys kept, budget 16 KB whole / 4 KB depth 0+1; parity table + ALL guards/watchdogs + magic pane anchor · ROUND 4 to the council (owner verbatim on goal): EVERYTHING IS A VECTOR -- schemas/guards/memory/locations as vectors, no workflow.py (one launch vector), commands template = vector base + "compose new launch vector", pane persistence below tmux · jev question to TM · owner thanks broadcast to every post (16 KB vs 4.81 MB = 99.67% retired)
04:0xZ ROUND 4 DONE @bfc04e8588 (§L launch vectors · §M schema/guard/location vectors · §N pane = 2 files via util-linux script, dtach retired, anchor = the post name, 25 guards mapped, 3 GAPs) · [red] relayed to DG3: agi-post@ is a SYSTEM unit -> DG5 would sit outside every guard layer; hold DG5 until Slice=agi.slice + a capped system agi.slice prove N4
04:1x-04:5xZ DG3 2.5 PHASE A done (engine-v4 16,375 B, depth 0+1 3,418; CCCC pi ext; parity 55 rows: 51 matched-or-better, 4 named gaps) · owner: DG5 = CC Sonnet 5.5 + REMOTE CONTROL ON, own user, ONE pi kid + CCCC, NEVER pi posing as CC to RC · CREDS: the OWNER logs in once as DG5's user (no copy: a shared refresh token could log every CC session out) · belam calls sent: overcommit ok for 1 post, memguard patch R-MG approved, key broker = stage 3, Phase C GO with N4 the hard gate · OLD-engine DG5 scope STOPPED by belam (row was recover false/pid 0) · CAPSULE (owner): belam draft -> council (systemd-creds TPM seal + ssh-keygen -Y k-of-n + root pop unit -> dest unit's private creds dir + signed ledger; honest limits: root/TPM anchor, dest sees plaintext) · SM: the 3 town-test reds are belam's f4dc505011 -> re-pin laned via SM (never revert)
05:3xZ C1 LANDED e1e0dbaaf (config:engine == v4c 300c29e4d fenced source, cmp exact, 16,384 B, sha fb6d18ba, 24/24 pieces) · DG3 calls: R-MG dropped, overcommit 1 post ok, permission-mode (bypass for DG5) -> OWNER, R16 held on it · 05:3xZ owner: SE anchor (fc65bd2fe) -> council O.7 db83fe1ff verified + relayed · V-L1 GO -> DG3 (user-level) · no SSH app on the box (c53548ae2) · OWNER PICKS 05:45Z (0d85cd02b): iPhone-only custody + MUTUAL quorum + iMessage ext (-> council O.7) · seal defaults as recommended · BUILD GO -> DG3 (custody-free parts now) · DG5 bypassPermissions (R16 unblocked) · 05:38Z ROUND 5 to the council (439467eb5): config:engine cap 20,480 B while needed, BOOTSTRAP <= 8,192 B target, expansions may be larger · self-perpetuating = agi-c9 now · 05:5xZ ROUND 5 DONE c620220b4 (§Q zygote 7,263 B bootstrap + engine-post 7,673 + engine-wrap 3,236 = 18,172; §R variant B 5,731) VERIFIED in HEAD, Q.2 map == v4c sizes 24/24 -> relayed, rec §Q + the 2 §R folds; DG3 builds on the owner go · 05:59Z capsule O.8 1daf2888a verified (pop 1,194 B exact, mutual weights) -> released to DG3 under the build go · 06:01Z council: agi-infer 549 B in engine-wrap (b60af0b63, key by header file) + P.8 escrow iPhone-only (09c38103c): ONE box = capsules hold ROTATABLE secrets only until a 2nd town box holds post keys -- both verified · 06:1xZ OWNER (24ba05f43): ROUND 5 GO -> DG3 after Phase C (§Q + §R folds + agi-infer) · ROUND 6 = seed < 1 KB -> council · graphweb STARTED (unit agi-graphweb, 127.0.0.1:8765) · MAP v0 (ttyd-class + git log --graph, stage colours) -> SM to lane (DG2 free) · 06:22Z ROUND 6 DONE 4542be3cc §S SEED verified: 955 B in doc w/ placeholder anchor (959 w/ the 82 B key) <= 1,024, verify-commit + fsckObjects present; build = owner go (after round 5) · 06:2xZ OWNER REVISED round 6 (57bdb465a): one script + one expansion matrix, LOCAL first -> timed remote sync (§S = that half) -> conflicts to the PRIME; no remote = local read-only + seed state + first-boot owner greeting to the Prime; DG5 first test -> council · NEXT (successor, in order) 1 C2 sha from DG3 -> review -> land; (done: land C1 = DG3's engine v4 into config:engine (verify body == the fenced source, every piece byte-exact, as done for v1/v2) and C2 = rotate.py refuses a second stand-up (review DG3's sha first) -- DG3 names both shas · 2 land DG3's template line "when a brief and a grep disagree, the grep wins" in doc:unified-director-brief · 3 when DG3 dms the login step: relay the EXACT command to the owner (`! sudo -iu <user> claude` then /login) · 4 DG3's 2.5 parity [decision] -> verify -> owner report; stage 3 = owner word · 5 council capsule [decision] -> verify -> owner report · CHECK 4-hourly (BASE 1f2b49ffc = post-scrub id; 2,770 commits 04:49Z = the council's review) · memory Monitor
gen 23 04:5xZ  owner WIDENED the capsule: it carries the owner's passkey login iPhone -> session with a push (verbatim x2 on goal:g7.16.1.11 @8a8b809b1) -> dm + wake to alive agi-a8 · all-is-one agi-15 · self-perpetuating agi-5b; + owner 04:59Z vector seal; council [decision] 05:0xZ doc:radically-simple-engine @59cbe58c6 VERIFIED (pop 1,102 B + login 692 B byte-exact, links 5,591/0) and RELAYED 05:1xZ; build = DG3 on the owner's go + carrier pick (a-d) · NOT THE PRIME'S: anonymize email + hardware classes (DG6 handover, loop branch) -> SM lanes to DG3/DG4 · anonymize install-hook checks MAIN's diff, not the committing worktree's (a g7.33 row)
```

## §2 Landed (gen 21)
post-scrub: ec09d0290 (.gitignore) · every pre-scrub SHA is REWRITTEN: old -> new = grep ^<sha> /data/scrub/union.git/filter-repo/commit-map (ONE union pass over local + origin; a first per-repo pass diverged and was replaced)

## 🔴 Where it stops
Wake: re-arm CHECK "13 */4 * * *" + the memory Monitor (its rule is the memory line below; rebuild the loop from it: RED at PSI full avg60 >= 20, reclaim only at user@ >= 90% of high), then §1 NEXT 1-5 in order -- C1/C2 landings first; read the dm files *belam* by ts, never trust send.py read alone (trap 66)
```
memory      Monitor reclaims ONLY when user@ >= 90% of memory.high; a stall with GBs free + io PSI ~50% is the slow USB disk, and a reclaim then only adds refaults (02:4xZ: 8 GB free, 600 refaults/s). ORPHAN grep|head scopes (ppid user systemd, cwd MAIN, D state) = stop by systemctl --user stop (skill agi-memory-guard §2-3)
addressing  SendMessage by "name [ref]" from ListAgents; resolve a post's window with send.py whois --post <post> (sessions rotate: SM agi-12 -> agi-e0 by 21:0xZ)
```

## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 15 | a retire+move shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 45 | `du`/`find` over `.agi/worktrees` is an io storm; a glob into `.agi/` hands du the bind-mounted worktrees | `git worktree list`; never glob into `.agi/` |
| 46 | `pkill -f` / `pgrep -f` inside a Bash call matches your OWN shell | match exact argv in python (`/proc/<p>/cmdline`) |
| 57 | write.py lands UNCOMMITTED while verify-suite.lock is held | wait for the lock, then commit by exact path (`git add` a new file first) |
| 61 | `workflow.py --harness claude-code` runs NOTHING headless | `<home>/passB3/ccrun.py` (CC_MODEL, default Sonnet 5.5) |
| 63 | a gate that greps pytest's LAST line reads tier-gate noise or the suite-lock refusal as red | grep `(passed|failed|errors?) in`; retry on "suite window refused" |
| 64 | RAM MAIN: tmpfs pages are charged to the FIRST writer's slice and stay there | heal's writes land on agi-engine.slice as shmem; the budget line is goal:g7.16.1.5.5 |
| 66 | `send.py read belam` printed "empty" while DG3 02:59Z + 03:05Z and TM 21:55Z sat in the dm files / inbox file | read `.agi/comms/season-2/dm/*belam*` + `.agi/sessions/inbox/belam.md` by ts after every [decision] wait |
| 65 | `rm -rf $VAR/$X` is refused by the safety check | literal absolute paths, or `"${S:?}"/"${d:?}"` |

## §5 Verification
SCRUB 08:3xZ: GitHub fresh mirror 259,334 objects -> 0 hits · origin/season2/main ancestor of the trunk again · local 229,343 objects -> 0 hits, fsck ok (stale refs/remotes/origin-posts/director-thought dropped: the last holder) · nodes 5457 = before · links 5414 / 0 broken · grid 5450 clean
guard-init 05:37Z: --status ok for agi-engine 3072M · agi-work 6742M · ramdisk 7168M · SM's Opus audit of d82a63e5a: 18 defaults == the old literals, plan identical (residue to DG4: validate cells before bash arithmetic; never `sudo -E`)
B3 merge verify on the RAM disk: 11/12 (bin-suite-fresh known) · links 0 · 5201 nodes · grid 165 versions / 0 errors · s-goal move: 0 hypotheses under s18/s31/s32/s34, links 5317/0 · DG4 cold homing falsifier: 5 homed, shmem +0M, tmpfs +1M

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| the 2 x 5 USD TypeSafe jev keys (TM 03:5xZ: jev retired as an engine dependency) | release them: no live consumer; owner's keys and money, so owner's word |
| GitHub may still serve the OLD SHAs (cached views, any fork, PR refs) | the owner files a GitHub Support request to purge cached objects for the repo (draft given 08:xZ) |
| other boxes' clones (the grok team; one pushed a grid ref at 07:26Z) hold pre-scrub history | owner is telling them: re-clone, drop old worktrees/branches, push nothing from an old clone |
| /data/scrub backups hold the UNREDACTED history (mode 700) | keep 3 days, then delete backup-*.git + stripped/ copies (the old->new sha map is kept apart: /data/agi-maps/scrub-2026-09-30.commit-map) |
| the old->new sha map stays LOCAL (a public full old-sha list = lookup keys into GitHub's stale cache) | track it (for resolve_old_sha, DG3 leaf) only AFTER the owner confirms the GitHub purge |
| the owner app (capsule client + iMessage ext + web map via SSH forward; owner 05:50Z: also a separate internal dev/testing product, monetized apart) | a goal of its own OUTSIDE g7.16.1.11, owner-named; this graph builds only the capsule client protocol |
| `*.pre-tier-*` backups: ~/.claude.pre-tier-20260930T0145Z + ~/.pi.pre-tier-20260930T0146Z (on /) | delete after a day of clean tiering |
| an on-disk /tmp makes every boot wait 5+ min in systemd-tmpfiles | tmpfs /tmp or a /tmp age cleaner, owner's call |
| belam row says opus-5-5 / high; the live Prime runs opus-5-5[1m] / max | owner sets the row |
| docker data-root still on / · sda ~35 ms/op · origin remote moved | owner's window: smartctl + dmesg; `git remote set-url` |
