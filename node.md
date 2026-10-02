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
gen 26 (07:1xZ 10-02): Z4 phase A LANDED as ONE trunk update c2decf431 (SM, 07:03Z): my 4 anchor commits as authored (held on belam/z4a-anchor so the trunk was never red) + DG1's C4 + prose + DG1.11 tests on top. Verified on the trunk by belam. "Anchor-signed" = Prime-authored (no schema commit here has ever carried a git signature; grow-gate's AGI_ANCHOR is design only, doc:radically-simple-engine §Y1).
<!-- THOUGHT:END -->

## §0 State (07:1xZ 10-02, read from date -u)
| | |
|---|---|
| post | belam gen 26 (gen_after 1, row window @5), session 285ac5d4, OLD engine (owner 00:1xZ: the belam v5 move = the successor-after-next, only after AA3 land + keys are BUILT) |
| box | REBOOTED 22:17:34Z 10-01 (owner GO). agi-boot in /etc, enabled: exit 0 22:32:58Z · F1 6/6 120 s apart · F2 ACL pair · F3 5/5 down · heal 4/4 old posts |
| v5 up | alive · all-is-one · self-perpetuating · DG1 · TM-new · DT-1 (boot set) + DG2 (00:0xZ) + DG3 (moved 00:0xZ, row dbce857b4, h.conf only) |
| down | DG4 · DG5 · DT-2 · stream-master: owner "keep the 5 down" (disabled, recover false, 0 procs) |
| old setup | belam @1 · SM @2 · old TM @3 (heal guards ONLY these; v5 = systemd Restart) |
| tree | config:posts parent cells: owner > belam > council{members alive, all-is-one, self-perpetuating · lands [SM]} > SM > DG1 · TM-new > DT-1 (f3a7eb1da ec5daa28a 1efd017e6 faabf9b7a b6b2c33d3) |
| mail | = append to the post's inbox file in MAIN; the v5 wrapper turns growth into a turn. `send.py --from belam send <p> "<text>"`. Inbox dir g:agi rwx + default rw (01:1xZ). SendMessage = fallback only |
| crons | session-only: CHECK e8519b0a (13 */4) + memory Monitor (inline /proc/meminfo + PSI, 30 min, re-arm; memmon.py not found without an io sweep): both die with me, re-arm at wake |
| merge pass | paused_by_owner (05:1xZ 09-30: council / automated). BASE 1f2b49ffc9 |
| A+ | ladder tier-3 claude-code parent = Sonnet 5.5 (d9d1cb7a1; owner 02:27Z 10-01 "Everyone else on sonnet 5.5 for everything they need") · SM runs a v5 director's WRITTEN dispatch order on claude-code Sonnet 5.5, 0 USD (01:1xZ); ends when the council's keys land |

## §1 Plan
```
figure eight (doc:council-loop) — the Prime REVIEWS, never assigns a design or a build (template 76f1129d1)
council bundle DONE (RULING 2 = per-post ~/g.git + trunk-only commons, ACCEPTED 03:3xZ; DG1 swaps the one-box half; AA3.12 land-from-own-store): AA1 boxes (doc:rse-aa1-boxes) · AA2 rotations + 8 KB + load matrix + versioning + per-user stores (doc:radically-simple-engine) · AA3 land (doc:rse-aa3-land)
 -> DG1 goals g7.16.1.11.11-.14 + 14 hypotheses LANDED (SM 818f6652f) -> DG2 experiments <-> DG1 inner loops -> DG3 builds -> SM mur
 -> DG1 outcomes -> SM bigger outcomes -> council overview nodes -> belam = the SEASON WRAP (owner's end condition)
belam: answer [decision]s · give each host act (sudo, /etc, unit installs) its own GO · hold every result to the 8 KB base (8,168 B) / 1 KB seed + the owner lines
NOT by hand: grid cron off · refs/grid retire · hourly snapshot = AA3.10-.11 · ladder:ladder retires for the post tree (owner 03:1xZ, sent to the council; Z3) -- built by the directors
```

## §2 Landed (gen 26)
wake: trunk synced w/ origin/season2/main 895c1ad3c (trap 70) cd6d99162 · card re-linked 00b79c1e7 · Z4 phase A anchor set 52d7fc4ca (4 blobs == DG1's) -> LANDED c2decf431 (SM, one atomic update, 07:03Z) · scratch worktrees removed

## 🔴 Where it stops
Nothing open for belam: Z4 phase A landed c2decf431 and verified; phase B (freeze + move readers, workflow.py first) = DG1/DG2/DG3 work, reviewed via SM's [merge-up]s
- standing residue: test_town_mint_final.py:175 needs the a00-80511a41 fence's ladder parent -> ONE later DG1 round (fence fix + substitution delete); not belam's
Council bundle is with DG1; DG2 + DG3 on v5 work DG1's leaves; belam reviews only; next belam stays on the old engine
- wake: CronList -> re-arm CHECK (13 */4) + memory Monitor · sync the trunk with origin/season2/main FIRST (trap 70) · read .agi/sessions/inbox/belam.md by ts (trap 66)
- watch: SM's [merge-up]s of DG1/DG2/DG3 work; review against the 8 KB base / 1 KB seed and the owner lines on town:local-maxxing (Agent Notes)
- each host act a v5 post asks for (sudo, install, unit start) = its own belam GO, before-state recorded, rollback named
- nothing is owed to the owner; every open item is in §6

## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 15 | a retire+move shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 45 | `du`/`find` over `.agi/worktrees` is an io storm | `git worktree list`; never glob into `.agi/` |
| 46 | `pkill -f` / `pgrep -f` matches your OWN shell | match by comm + /proc environ |
| 57 | write.py lands UNCOMMITTED while verify-suite.lock is held | wait, then commit by exact path |
| 61 | `workflow.py --harness claude-code` runs nothing headless | `<home>/passB3/ccrun.py` (SM's mur route) |
| 63 | grepping pytest's LAST line reads noise as red | grep `(passed|failed|errors?) in` |
| 66 | `send.py read belam` prints "empty" while mail sits in the inbox FILE | read `.agi/sessions/inbox/belam.md` by ts |
| 67 | `open(p,"w").write(f(open(p).read()))` truncates first | read, write a tmp, os.replace |
| 69 | an order without an ack can sit unread | one-line ack back; none in 15 min = re-send |
| 70 | a belam / DG3 rotation pushes its key row to season2/main; town rotate-self then refuses | merge-tree; identical rows -> commit-tree with the trunk tree, CAS update-ref |
| 73 | loose objects > gc.auto: every commit ran a failing gc | gc.auto=0 in MAIN (rollback: unset) |
| 75 | write.py `sub` strips leading whitespace: a new frontmatter row lost its indent | anchor AFTER `  - ` (insert as `<row>\n  - <anchor>`) |
| 76 | `lxc version` on this Ubuntu auto-installs the LXD snap | never call bare lxc / lxd |
| 77 | heal's resume rewrites your row; `rotate.py ack` refuses on a dirty own row | check pid + pane, commit heal's write, then ack |
| 78 | SendMessage "Failed" can still deliver; a v5 uid cannot append to another's inbox until AA1 | wait for a reply; v5 -> v5 mail = AA1 boxes |

## §5 Verification
Z4A on the trunk c2decf431: 4 anchor commits as authored · 3 anchor blobs == 52d7fc4ca · 0/5 towns parent ladder:ladder · 10 test files 76 passed 0 failed · links 5719/0 · schema 246/18/0 (unchanged) · growth.tsv == grow-project · verify 12/13 (bin-suite-fresh known) · nodes 5,760

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| the 2 x 5 USD TypeSafe jev keys (jev retired as an engine dependency) | release them: no live consumer; owner's keys and money |
| GitHub history: ssh comment user@host (81d0e8729 8a9b0ad95 4b7d20df7) | OWNER 22:5xZ: leave it in -> no rewrite, no purge; SM's added-ever gate stays |
| other boxes' clones hold pre-scrub history | owner tells them: re-clone, push nothing from an old clone |
| /data/scrub backups hold the UNREDACTED history (mode 700) | delete backup-*.git + stripped/ after 10-03 (3 days); the sha map stays local, never tracked (no purge coming) |
| the owner app (capsule client + iMessage ext + web map) | a goal of its own OUTSIDE g7.16.1.11, owner-named |
| `*.pre-tier-*` backups (~/.claude, ~/.pi, on /) | past the day of clean tiering: delete on the owner's word |
| /tmp on disk: tmpfiles 3m30s this boot (14m28s before) | owner 22:2xZ "Leave it for now" |
| belam row opus-5-5 / high vs the live Prime opus-5-5[1m] / max | owner sets the row |
| docker data-root on / · sda ~35 ms/op · origin remote moved | owner's window: smartctl + dmesg; `git remote set-url` |
