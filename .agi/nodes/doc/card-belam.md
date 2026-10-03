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
gen 26 (18:5xZ 10-02): the owner worked live with belam all afternoon; every line is verbatim on town:local-maxxing Agent Notes (64bf778d4 .. 62e8ea465). Ruled: no ladder reader moves · workflow.py retires, manifests KEPT, skill = agi-spawn-chain, the FLOW ROTATION = council (growth.tsv + parent cells only) · shell tests for v5 pieces · per-spawn key from the .env provisioning key + 2 spawn classes + direct inference = council (K1-K3) · mail without send.py = AA1.M ACCEPTED (owner GO; path unit; no worktree hop) and LANED to DG2/DG3 (SM's g7.16.1.11 HOLD lifts only by a named belam [rule]). Paid: posts lost acks because send.py has no [ack] to the Prime and their cards named a stale belam session -> route rule sent, 6/6 re-acked by send.py.
<!-- THOUGHT:END -->

## §0 State (02:2xZ 10-03, read from date -u)
| | |
|---|---|
| post | belam gen 27, session 332d4bf1, window @8; the row's generation cell reads 2 (rotate counted 1 -> 2 again; gen 25 fixed it by hand at ff323856c), OLD engine (owner 00:1xZ: v5 move = goal:g7.16.1.11.17, after AA3 land + keys) |
| box | rebooted 22:17:34Z 10-01 (owner GO); agi-boot enabled; heal guards the old posts only |
| v5 up | alive · all-is-one · self-perpetuating · DG1 · DG2 · DG3 · TM-new · DT-1 |
| down | DG4 · DG5 · DT-2 · stream-master: owner "keep the 5 down" |
| old setup | belam · SM · old TM |
| tree | owner > belam > council{alive, all-is-one, self-perpetuating; lands []} + keep{SM, TM-new} > DG1-3 under SM, DT-1 under TM-new (level rule 3a33c71b9: mail within a level or one up/down) |
| mail | `send.py --from belam send <p> "<text>"` = append to the post's inbox file in MAIN; read .agi/sessions/inbox/belam.md by ts (trap 66) |
| crons | session-only: CHECK 6bbe9d5d (13 */4) + memory Monitor b8kr1990e (MemAvailable < 6 GB or PSI avg10 >= 20, 30 min, re-arm): both die with me |
| merge pass | paused_by_owner (05:1xZ 09-30: council / automated). BASE 1f2b49ffc9 |
| carrier | AA1.M INSTALLED at T=d57b52bd46a7189c4ed77e3596abf90af112851b (gen 27, 02:1xZ-02:2xZ): /opt/agi/bin/{box,box-carry,agi-signers,sect} · /etc/agi/carry.env (hub empty) · /var/lib/agi/allowed_signers 12 lines · 4 units + 12 agi-carry@<p>.path active/waiting · no fetch timer. Rollbacks = doc:dg3-aa1m-install-packages A1 / A2 / A4 |

## §1 Plan
```
figure eight (doc:council-loop): council designs -> DG1 goals + hyps -> DG2 experiments <-> DG1 -> DG3 builds -> SM gate -> belam reviews
belam: answer [decision]s · each host act its own GO (read whole, before-state, rollback) · hold results to the 8 KB base / 1 KB seed + the owner lines
NEVER: assign a design or a build (council) · dispatch · write in a director's tree
```

## §2 Landed (gen 27)
trunk synced with origin/season2/main 1054e030f (key row identical, trunk tree kept) · card re-linked 3048194b8 · host acts A1 A2 A4 A5 RUN (A5 starts=1: systemd drops PathChanged events during a run; carrier re-scan = the cover; residual gap after the final scan = finding to SM) · W hold RELEASED to DG1 (Z4.8 af4b1ca90 + 8e3bd232f on the trunk) · grid: payload-path fix = goal:g1 GO to DG1; slot-every-file = owner option (§6)
## 🔴 Where it stops
Wait for ONE [rule] line each from SM, DG1, alive (sent 02:2xZ); none in 15 min = re-send (trap 69). Next GOs, each as ONE line with command + before + rollback: A6 (after alive bd3960e23 lands + DG1's A3 signers BUILD round) · A7 (after the AA2 per-post stores, 5e448309c at SM) · K1 kid cell on my row + agi-mint@ / agi-kid@ / the 345 B polkit rule · the agi-land LAND STEP · A8 LAST (needs box.hub + a 2nd box). Re-running A1 `pieces` with a new T = its own GO (F2: AGI_TRUNK stays pinned until then).
- HELD: nothing of mine. At W's merge-up belam renames the skills clause in both config:rotations entries (-> build:skills-agi-spawn-chain-SKILL.md) on a branch
- goal:g7.16.1.11.17 (belam on v5) HORIZON; this belam stays on the old engine
- wake: CronList -> re-arm CHECK + memory Monitor · sync the trunk with origin/season2/main FIRST (trap 70) · re-link this card (trap 10) · inbox by ts
- watch: SM's [merge-up]s; review against the 8 KB base / 1 KB seed and the owner lines on town:local-maxxing (Agent Notes)

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
| 69 | an order without an ack can sit unread; send.py refuses [ack] to belam, so posts fell back to SendMessage to stale belam sessions (acks lost 17:4xZ) | ask for ONE [rule] line by send.py, never "[ack]"; none in 15 min = re-send (goal:g1.40 race) |
| 70 | a belam / DG3 rotation pushes its key row to season2/main; town rotate-self then refuses | merge-tree; identical rows -> commit-tree with the trunk tree, CAS update-ref |
| 73 | loose objects > gc.auto: every commit ran a failing gc | gc.auto=0 in MAIN (rollback: unset) |
| 75 | write.py `sub` strips leading whitespace: a new frontmatter row lost its indent | anchor AFTER `  - ` (insert as `<row>\n  - <anchor>`) |
| 76 | `lxc version` on this Ubuntu auto-installs the LXD snap | never call bare lxc / lxd |
| 77 | heal's resume rewrites your row; `rotate.py ack` refuses on a dirty own row | check pid + pane, commit heal's write, then ack |
| 78 | SendMessage "Failed" can still deliver; a v5 uid cannot append to another's inbox until AA1 | wait for a reply; v5 -> v5 mail = AA1 boxes |

## §5 Verification
pb3 on the trunk 96140880b: rotations.md == ab864f427 · test_skills_first_turn_entry 4 passed · wake reads agi-post + agi-stream rc 0 · links 5724/0
Z4A on the trunk c2decf431: 76 passed · links 5719/0 · schema 246/18/0 · growth.tsv == grow-project · verify 12/13 (bin-suite-fresh known) · nodes 5,760

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
| grid slot for EVERY file a node names (442 of 710 engine files have no build node; mvp source_files 29 nodes; 18 retired build nodes lack their payload in the grid) | not now: every live build node already carries node + payload (310/310 DG1, 297/297 alive); git history holds the retired bytes. Say go and DG1 cuts ONE goal:g1 round |
