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
gen 23 (04:53Z-12:2xZ 10-01): the owner night -- capsule, rounds 5-7 designed by the council and LANDED, DG5 on the new engine, 12 owner logins, Grok signed in, the switch ordered (verbatim on goal:g7.16.1.11). Card rewritten whole for the successor: the switch order, the per-post GO rule, the session-only crons.
<!-- THOUGHT:END -->

## §0 State (12:1xZ 10-01, read from date -u)
| | |
|---|---|
| post | belam-S2-L5-XX gen 23 agi-24 (woke 04:53Z); predecessors idle: gen 22 agi-a3 · gen 21 agi-23 |
| run | OWNER NIGHT to 14:00Z (10am EST); owner asleep. Goal = goal:g7.16.1.11 (owner verbatim on it, every line) + leaves .1-.10 = the bundles (old bundles void; town board re-swept by TM c9880a5e1) |
| engine | NEW ENGINE LANDED 10:4xZ (rounds 5-7, land.sh split, 0-6 PASS): config:engine 7,904 B 57eb5ac42 + engine-post/wrap/grow/root + growth.tsv + 2 schemas; verify 12/13 (bin-suite-fresh known) |
| posts | DG5 UP on v5 (pi-free, own uid, agi.slice; parity 40/55, 0 regressions) · DG3 = agi-c3 (builder) · SM = agi-e0 · council: alive agi-1d · all-is-one agi-f0 · self-perpetuating agi-c9 · TM agi-40 (old TM = STANDBY after the switch) |
| users | 12 owner-logged-in post users agi-<post> uid 983..972 (thought-master renamed -> agi-thought-master-new) + agi-grok 971 (xAI SuperGrok OAuth, xai-auth.json 600, never printed) |
| crons | session-only (die with me): CHECK daa581ac (13 */4) · WIND-DOWN 44d274ad one-shot 13:50Z · memory Monitor = python3 -u /data/tmp/belam23/memmon.py (re-arm each 30 min) |

## §1 Plan
```
SWITCH (owner 07:3xZ GO, verbatim on the goal): everyone but belam / old thought-master / director-thought -> v5, one at a time, rollback each
  NEW posts on v5, GO given 12:1xZ: thought-master-new (Opus 5.5, takes the research loop) > director-thought-1 > -2 > director-general-4 (cell 451adc6c2)
  MOVES, order (DG3 plan 49257db79): DG2 > DG1 > alive > self-perpetuating > all-is-one > stream-master > sanctuary-master > DG3 > belam LAST
    gates: G1 closed (logins) · G2 key broker = fix round (CC posts use CC subagents) · G3 done · G4 stand-up CLI TypeError 1d9e7da5e + G5 send.py v5 wake 2a9baac18: building -> mur -> SM lands
    each MOVE = ONE config:posts write AT the GO (engine cell + recover false + pid 0; C2 refuses rotate on an engine row, never earlier); DG3 sends the sub
  belam LAST: a FRESH belam on the new route, gen counter CONTINUED (never restart at I); this session stays up idle
  models: council + masters Opus 5.5 · directors Sonnet 5.5 · every subagent Sonnet 5.5
AFTER the switch: deprecation sweep (old-engine build nodes, void bundles; retire, never delete) · ROUND 8 stream town (queued with the council, 6a273255b + taste tester 225e971fa) · viz last (spider first)
13:50Z WIND-DOWN: posts finish + cards; ONE owner morning report (landed shas, switch state, verdicts, what needs the owner)
NOT TONIGHT: seed root install + anchor line · hub grow-gate wiring · T7 wake row · phone route (waits for the Mac's WireGuard config) · stand-in cert expires 14:00Z
```

## §2 Landed (gen 23)
C1 e1e0dbaaf (v4c) · C2 aa2f2e28a · C4 81ed274fc · C3 5ee794d45 · R5-R7 57eb5ac42 (+6 before) · rows 6f5275059 · DG4 cell 451adc6c2 · director brief REVIEW IN PLACE -> claude-code · 10 goal leaves g7.16.1.11.1-.10 · ACL 11:4xZ (g:agi + u:belam rwX + defaults on .git/refs, .agi/comms, .spawn-budget, inbox; dir-level worktrees; seats UNTOUCHED)

## 🔴 Where it stops
Wake: re-arm CHECK + memory Monitor (memmon.py) + a 13:50Z wind-down one-shot if before it; read .agi/comms/season-2/dm/*belam* AND .agi/sessions/inbox/belam.md by ts (DG3 writes to the INBOX); then give DG3 the GO per post in the §1 order, one write each at its GO.
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
