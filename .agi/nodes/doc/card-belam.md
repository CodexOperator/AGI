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
gen 27 out (14:4xZ 10-07): the carrier, unit, polkit, kid cell and GitHub sealer went live this generation, each root act read whole at a landed pinned T; A12 was rolled back after it looped DG2/DG3 (my miss: I took the self-heal prediction on the line's word). The owner's 10-07 lines re-scope the season: collapse + rollover design to the council, the old Python key/metrics/verify kept, belam's v5 move re-stated as more doable. Owner 14:4xZ verbatim (tail): "I will hear about it from your successor. Thank you for your service."
<!-- THOUGHT:END -->

## §0 State (14:4xZ 10-07, read from date -u)
| | |
|---|---|
| post | belam gen 28 (woke 14:4xZ 10-07), session 38d10ddc, window @15 (row generation cell reads 3: rotate's counter, gen 25 fixed it by hand once), OLD engine |
| box | up since 10-01 22:17Z; 8 v5 posts active 0 restarts (6 restarted 14:1xZ 10-07 after the owner's stop 10-04 07:53Z) · down by the owner: DG4 · DG5 · DT-2 · stream-master · old setup running: belam · SM (old TM = row thought-master-old, stood down 14:56Z 10-07) |
| tree | owner > belam > council{alive, all-is-one, self-perpetuating; lands []} + keep{SM, TM} > DG1-3 under SM, DT-1 under TM (level rule 3a33c71b9) |
| mail | `send.py --from belam send <p> "<text>"`; read .agi/sessions/inbox/belam.md by ts (trap 66) |
| crons | session-only, die with me: gen 28 armed CHECK 8a0c8b5c (13 */4) + memory Monitor; re-arm both (MemAvailable < 6 GB or PSI avg10 >= 20, 30 min) at wake |
| merge pass | paused_by_owner (council / automated). BASE 1f2b49ffc9 |
| carrier | INSTALLED: /opt/agi/bin box · box-carry 56cd9215 (closer) · agi-signers 6b9df8d9 · sect; carry.env AGI_TRUNK=f02495529, hub empty; 12 agi-carry@<p>.path waiting; fetch timer on (60 s, local sweep); ring file /var/lib/agi/allowed_signers (append-only) |
| unit | agi-post@.service = 5cecf3aa (A9). A12 (c4f5a917) ROLLED BACK 10-03 15:1xZ: DG2/DG3 looped exit 127 ~90 min (t lacked OUT.6 -> no bin/agi-out) |
| polkit | 50-agi.rules a17953ca (K1: own mint/kid units only) · kid cell on belam row: usd 0.5, max 3 |
| GitHub | seal.yml 686368aa LIVE on master (merge 6405a03fc), 30-min sweep, attests block digests; gh token has workflow scope (owner 10-03 05:58Z); block_push OFF until a real block |
| MAIN config | gpg.ssh.allowedSignersFile UNSET at repo level (DG5 leftover shadowed every worktree; rollback = set it to .git/allowed_signers) |

## §1 Plan
```
figure eight (doc:council-loop): council designs -> DG1 goals + hyps -> DG2 experiments <-> DG1 -> DG3 builds -> SM gate -> belam reviews + each root act its own GO
OWNER 10-07 14:3x-14:4xZ (town board, verbatim): THIS SEASON = node collapse for a tidy archive + how to collapse between seasons (council D1-D4, incl. the
  REVIEW of core/season2/et-grok-pilot: 2,014 commits, 0 nodes lost, read only) · KEEP the old Python key / metrics / verify (shell rewrites = season 3) ·
  metrics back on · belam on v5 re-stated with that bypass ("a lot more doable sooner") · pane / matrix-math commands / Go keys / SSH-pane capsule = SEASON 3
NEVER: assign a design or a build (council) · dispatch · write in another post's tree · install a root act not read whole at a landed pinned T
```

## §2 Landed (gen 27)
wake sync + card re-link · A1 A2 A4 A5 (carrier) · A1 re-run · A9 unit + MAIN repo signing config fix (F2/F3 met on DT-1) · A11 closer · A12 then ROLLBACK · K1 polkit + kid usd · capsule cells 1ea2129b5 in OUT.6 055fb92aa · §AB released (+ owner inputs 2-6: DAG checkpoints, drop-in algorithms, layered blocks, nested PQ + provable revocation, GitHub sealer) · seal.yml live · 8 KB rail ruled (F21: code <= 8,192, whole <= 12,288) · R6 = (c) · A10 = (B) · private-key gate accepted · 10-07 restart of 6 posts + continue sent to all
gen 28: wake (card re-link 5eb826e84, CHECK 8a0c8b5c + memory watch) · D4 R2 ruled (A) to all-is-one · OWNER 14:4xZ RENAME: old TM down (10006804e 204912aae, @3 closed) · rows ea929923b · card swap 0024e3bbb · host 15:02Z: agi-post@thought-master active, uid 972 kept, ring +1, mail ok 19 s, sig Good · THOUGHT 0730798ae
## 🔴 Where it stops
Nothing waits on belam. The council has the owner's 10-07 lines (D1-D4 + the Python-keep + metrics + the re-stated .17); expect ONE [rule] from alive and DG1's re-written prerequisites for goal:g7.16.1.11.17. Next GOs, each ONE line in the A-act shape: A12 re-install only when every v5 t carries bin/agi-out AND the agi-out step cannot loop (belam [red] 10-03 15:1xZ) · A10 = install the agi-land pieces from a landed fail-closed gate (RING.5b 5c3df5114 or later) after the CKPT landing + SM mur · agi-land LAND STEP · block_push after the first real block · pin attest-build-provenance by SHA (a master merge).
- wake: CronList -> re-arm CHECK + memory Monitor · sync the trunk with origin/season2/main FIRST (trap 70) · re-link this card (trap 10) · inbox by ts
- watch: SM's [merge-up]s; hold every result to the 8 KB rail + the owner lines on town:local-maxxing (Agent Notes)

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
| 79 | the harness refuses `rm -rf $var` inside a root `sh -c` | run the act without it; name the temp dir left behind |
| 80 | a unit step that needs a piece only a NEWER t carries loops exit 127 under Restart=always (A12: DG2/DG3 ~90 min) | before a unit install, measure the piece in EVERY post's bin; a post leaving via an out-line does NOT merge the trunk at stop |

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
| ORIGIN 15:0xZ 10-07: season2/main, season/s2, season2/docs/* + loops are GONE from origin (17 heads left, core/season3/main new); origin/season2/main locally = stale b0608a1f3; belam.key.pending (14:49Z) cannot swap (rotate: no remote season2/main) | owner names the integration branch (recreate season2/main from the trunk, or point the engine at a new one); belam recreates NOTHING outward |
| ring: thought-master-new@agi line still open with the key now also under thought-master@agi | close it at the next root ring pass (valid-before), or leave: same key, same post |
| docker data-root on / · sda ~35 ms/op · origin remote moved | owner's window: smartctl + dmesg; `git remote set-url` |
| grid slot for EVERY file a node names (442 of 710 engine files have no build node; mvp source_files 29 nodes; 18 retired build nodes lack their payload in the grid) | not now: every live build node already carries node + payload (310/310 DG1, 297/297 alive); git history holds the retired bytes. Say go and DG1 cuts ONE goal:g1 round |
