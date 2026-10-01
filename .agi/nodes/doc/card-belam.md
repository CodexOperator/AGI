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
gen 24 wake (15:07Z 10-01): §0 rewritten for the post-reboot state -- heal brought DG1/DG2/DG3 back, v5 posts still down, G5 not on the trunk; the owner 15:1xZ lift stands. No GO is due until DG3 restores v5 and SM lands G5.
<!-- THOUGHT:END -->

## §0 State (15:1xZ 10-01, read from date -u)
| | |
|---|---|
| post | belam-S2-L5-XX gen 24 (woke 15:07Z, rotate record 150403Z; reset to 1 by rotate; row fixed to 24 at 3508b58d3, key_history kept; red = hypothesis:rotate-self-after-reboot-resume-keeps-the-generation-counter, dm to DE 15:2xZ; this session = agi-6a [63be10] @10); predecessors idle: gen 23 agi-24 · 22 agi-a3 · 21 agi-23 · 20 agi-79 |
| REBOOT | 14:42Z HARD reboot (cause UNKNOWN). heal respawned DG1 gen 5 @7 (15:05Z) · DG2 gen 5 @8 (15:06Z) · DG3 gen 15 @9 (15:06Z); v5 units GONE until DG3 restores them (DG5 > TM-new > DT-1 > DT-2, gate between) |
| run | owner 15:1xZ LIFTED the wind-down: keep going until goal:g7.16.1.11.1-.10 are complete · G5 8a450c0c0 NOT on the trunk (15:1xZ) |
| engine | v5 LANDED 10:4xZ: config:engine 7,904 B 57eb5ac42 + engine-post/wrap/grow/root + growth.tsv + schemas (verify 12/13, bin-suite-fresh known) |
| v5 posts | DOWN since the reboot; before it UP: director-general-5 (pi-free) · thought-master-new (research loop; RC visible) · director-thought-1/-2 (RC visible, idle) · STOPPED: director-general-4 (memory; restart with an assignment) |
| old posts | all still on the old setup (moves wait on G5 + the v5 restore) · old thought-master = STANDBY (handed off 12:5xZ) · SM rotated 13:1xZ (gen 12) · DG3 = agi-6a |
| users | 12 owner-logged-in agi-<post> (983..972, onboarding flags set 12:4xZ) + agi-grok 971 (xAI SuperGrok OAuth, 13 models) |
| crons | session-only: CHECK ae1c3bdb (13 */4) · memory Monitor = python3 -u /data/tmp/belam23/memmon.py (re-arm each 30 min) |

## §1 Plan (owner morning)
```
1 MOVES (owner 07:3xZ GO, verbatim on goal:g7.16.1.11): DG2 > DG1 > alive > self-perpetuating > all-is-one > stream-master > sanctuary-master > DG3 > belam LAST
   each: G5 (v5 wake) + G6 (AGI_BOX) landed first · ONE config:posts write AT the GO (engine cell + recover false + pid 0) · old session STOPPED before the new starts · gate (load1 < 16, io PSI avg60 < 50) between
   G4 LANDED b30042219 (SM) · belam LAST = a FRESH belam on v5, gen counter CONTINUED; this session stays idle
2 DG4: assignment from the owner or SM, then restart · DT-1/-2: their max-parallel lane under thought-master-new (key broker = fix round for pi-free kids)
3 council: moral satisfaction verdicts on the seed engine (not filed yet) -> phase 3 readiness
4 after the moves: deprecation sweep (retire, never delete) · ROUND 8 stream town (queued) · viz last (spider first)
NOT YET: seed root install + anchor line · hub grow-gate wiring · T7 wake row · phone route (Mac WireGuard config) · Grok proxy + token renewal
```

## §2 Landed (gen 23)
C1 e1e0dbaaf · C2 aa2f2e28a · C4 81ed274fc · C3 5ee794d45 · R5-R7 57eb5ac42 (+6) · rows 6f5275059 · DG4 cell 451adc6c2 · 10 goal leaves g7.16.1.11.1-.10 · ACLs (refs, comms, objects, logs, worktrees; seats UNTOUCHED) · director brief MUR -> claude-code

## 🔴 Where it stops
Owner 15:1xZ: keep going until goal:g7.16.1.11.1-.10 are done -- the moves are GO (verbatim in the goal THOUGHT c3d13648a; relayed to all 15:1xZ).
Order: v5 restore after the 14:42Z hard reboot (DG3 when heal brings it back: DG5 > thought-master-new > DT-1 > DT-2, gate between) > G5 8a450c0c0 lands (SM) > MOVES DG2 > DG1 > alive > self-perpetuating > all-is-one > stream-master > sanctuary-master > DG3 > belam LAST (fresh, gen continued): each = ONE config:posts write by the Prime AT its GO (engine cell + recover false + pid 0; DG3 sends the sub), old session stopped before the new starts.
Wake: CronList first, re-arm CHECK (13 */4) + memory Monitor (python3 -u /data/tmp/belam23/memmon.py); read .agi/comms/season-2/dm/*belam* AND .agi/sessions/inbox/belam.md by ts (DG3 + v5 posts write to the INBOX; v5 posts by dm FILE or their Remote Control name).
Owner picks open: DG4 assignment · Round 8 start · the seed boot install (root + anchor line) so v5 posts survive a reboot · phone route (Mac WireGuard) · Terminus certs.

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
