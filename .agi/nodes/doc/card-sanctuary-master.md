---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 3e856c7e9b80c2ab
season: 2
tags:
  - card
  - master
title: Card sanctuary master
town: core
thought_session: sm-et-grok-wake-20261005-0051
---
# doc:card-sanctuary-master — sanctuary-master's card: the ONE scratch

Replaced whole; <= 100 lines. Role = HEAD + `doc:unified-master-brief` + this card. v4: Write/Edit + `agi-turn`. Skills stay `skills/*/SKILL.md`. No session auto-rotation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
00:51Z 10-05 (date -u): gated DG2 d52e9e8cb onto 68633ecbd -> 04d64fa09 (g7161118 proved 0.9, F1 F2 F3 replica PASS). Then DG1 ae28e59da onto that -> cea034fa5 (agi-fill Y2 hyp) queued DG2. Wrap 4a6ada7db. No push.
<!-- THOUGHT:END -->

<<<<<<< HEAD
## §0 State (00:51Z 10-05, date -u)
=======

## §0 State (08:1xZ 10-04, date -u) — gen 21 seated 07:56Z · trunk 666098f19 pushed (CKPT.3 + OUT.7 LANDED) · no merge-up open · IDLE until a [merge-up], a director blocker or an owner line
>>>>>>> core/season2/et-grok-pilot
| | |
|---|---|
| post | sanctuary-master · engine v4 grok-bot grok-4.6 high · capsule encryption-town · branch posts/sanctuary-master · trunk core/season2/et-grok-pilot cea034fa5 |
| role | master-gate for the council loop (goal:g7.16.1) + board coordinator |
| team | alive · all-is-one · self-perpetuating · DG1 · DG2 · DG3 · DT-2 · SM |
| box | MemAvailable ~4.5 GiB · mem PSI 0 · load ~5.8 |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-send · agi-goal · agi-verify |
| mail | `AGI_POST=sanctuary-master bin/box` · Prime only if Shael must decide |
| holds | g7.16.1.11 key/identity/signing/rotate/spawn-row/write-gate. Host acts = belam GO. VIZ 11.9 HORIZON. 11.8 UNHELD (council places Z2; SM does not assign). 10.7 Prime cells |
| open | g7.33.19.1 outcome closed 0.9 (F3 pytest re-measure). g7.16.1.11.5 active (8192 GREEN; 20480 title still red). g7161118 grow-check proved 0.9. agi-fill Y2 queued DG2 |


## §1 Plan
```
<<<<<<< HEAD
figure eight: council designs -> DG1 goals+hyps -> DG2 experiments <-> DG1 -> DG3 builds -> SM gate -> belam
SM: box read · gate [merge-up] by SHA · land on live trunk · bigger_outcomes when residue=0
NEVER: assign a design · spawn a row · auto-rotate · start VIZ · mail Prime for status
```

## §2 Landed this wake
- 00:49Z 04d64fa09 named tip d52e9e8cb onto 68633ecbd. g7161118 proved 0.9 F1 F2 F3 replica PASS. posts.md trunk. D=0.
- 00:50Z cea034fa5 named tip ae28e59da onto 04d64fa09. agi-fill Y2 hyp. queued DG2.
- 00:51Z wrap 4a6ada7db. boxed DG2 queue + DG1 land. No push.

## 🔴 Where it stops
Wait DG2 experiment+verdict on hypothesis:g7161118-agi-fill-is-the-captive-fill-window-without-write-py, then gate. 11.5 20480 BANK. VIZ LAST.
FIRST at next wake: `AGI_POST=sanctuary-master bin/box read`
=======
DONE gen 21: CKPT.3 70530c33c + OUT.7 666098f19 landed, pushed, notified (DG1 DG2 DG3 inbox; belam [merge-up] incl. A10/A12 host-act orders)
OPEN [red] on trunk (mine to see closed): agi-outline.t.sh C7 b-revouch-by-parent 84/1 since CKPT.3 -- fixture $T/gb (line 16) lacks ckpt; +ckpt = 85/0 measured; routed to DG3 08:1xZ as a one-commit corrective cut from 666098f19
AFTER: DG3 sends ckpt / revoke / pq / flowrot to DG1 one at a time; each reaches me only after DG1 runs it (DG1 06:03Z)
HOST ACTS = belam GO each: A10 ckpt on the hub BEFORE the gate (open grace until the first holding block; refs/agi/block/* write policy first) · A12 re-install only after bin/agi-out in every v5 post t + /var/lib/agi/<p>.env root-owned
MURS: Workflow tool, name agi-merge-up-review, args {rounds:[...], model: sonnet, effort: high, project_root}; FOCUS names the gated UNION sha + READ-ONLY; FINAL verify decides; accept_with_residue = RETURN; after EVERY mur: git symbolic-ref HEAD + reflog
```

## §2 Landed (each landing message carries its gate numbers)
- gens 16-20 (10-02..04): see git log --grep sanctuary-master + runs/mur-sm1[6-9]-*, mur-sm20-* (RING.5b/5g, W-1.16, OUT.6 landed; RING.3-5f, OUT.2-5, CKPT/CKPT.2 returned)
- 10-04 08:0xZ gen 21: LANDED CKPT.3 70530c33c = 28f941c82 + df697ec4d on f16d6eae3 (T2 79bae51ac = gated 2f3818fba + 4 newcomers byte-identical, 0 D, 18 files 0 dirty)
- 10-04 08:1xZ gen 21: LANDED OUT.7 666098f19 = 6e87ebf98 + 7b00fd8c7 + 1fcda87a9 on 6d3fcca22 (T2 a816fdf5b; stale 15/0 states 43/0 fresh 23/0 ckpt 69/0 combined; anonymize ok net + 5 commits; links 0 broken)

## 🔴 Where it stops
```
sanctuary-master gen 21, 08:1xZ 10-04: trunk 666098f19 clean + pushed; nothing to land. Next: DG3's agi-outline ckpt-fixture corrective (via DG1) -> gate: sh agi-outline.t.sh in a gate worktree = 85/0 + grow-gate files unchanged; then the ckpt/revoke/pq/flowrot rounds as DG1 forwards them
on a [merge-up]: static gate (merge-tree vs live HEAD rc, 0 D, added-ever + key versions in HISTORY, anonymize per range, host + home-path + GPU greps), links/schema, tests (EVERY .t.sh that reads a changed piece, with sh, from the gate worktree, arg 1 = gated sha), Sonnet security mur + FULL suite on tmpfs for root/grow-gate code, land ONE update by SHA on the live HEAD, push, notify
FIRST COMMAND AT WAKE: python3 extensions/agi/bin/send.py read sanctuary-master > <scratch>/inbox.txt  (then read the file WHOLE; never pipe the read to head)
```
>>>>>>> core/season2/et-grok-pilot

## §4 Traps
| trap | rule |
|---|---|
<<<<<<< HEAD
| graph-rules.md is a start snapshot | live nodes in the graph; skills in skills/ |
| send.py MAIN state unwritable | mail = bin/box |
| merge-tree prints a tree id on conflict | exit status; D=0 first |
| HEAD moved mid-gate | re-derive T2; update-ref old-value lock |
| MAIN has et-grok-pilot checked out | commit-tree + update-ref; MAIN WT stale; never checkout that branch here |
| VIZ assigned to me | horizon until LAST lifts |
| date stamps | `date -u` in the same step |
| anonymize.py needs MAIN .env | HOME/email/sk/pem grep on added lines when env unreadable |
=======
| my /dev/shm gate trees + suites are charged to MY scope (926 MB shmem at 13:0xZ) | start a suite only at MemAvailable >= 4 GiB + PSI low; never two at once under pressure; stop = every pid with cwd under the gate path, then worktree remove |
| a stray /tmp/.agi project marker | reddens root-discovery tests (test_workflow root rows, test_commands wrapper-flag): moved aside to /tmp/agi-stray-copy-created-20261001T021319Z |
| test_suite_live_checkout_worktree red | a post wrote its live card mid-test: passes alone |
| systemctl --user stop <bare name> | resolves .service, rc 5, the .scope lives: name '<unit>.scope' (g73360-b) |
| a test falling through a fake seam | can launch a REAL pi: read every slice/stage test's red for a real binary in the traceback |
| pipelined chain gate | one suite for N tips; attribute reds on a pair tree without the suspect range |
| rotate flattens the quorum card | re-link: ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md |
| MAIN shared | commit by exact path; never switch branches, stash or reset |
| dispatch output filtered by grep (19:55Z) | hid a stale-base refusal (exit, no spawn line): read the WHOLE output, then confirm with spawn_budget status |
| a bare cd in a Bash call | moves THIS session cwd into a worktree: always a ( subshell ) or absolute paths |
| spawn_budget 0/30 | NOT proof a parent exited (twice today): scan /proc cwd for the agent id before calling it dead |
| A+ dispatch | the director line is run VERBATIM: a stale-base refusal goes back to the director (add --allow-stale-base reason, or merge) |
| heal resume blanks session_name | route by inbox or the ListAgents bridge name (DG1 = director-general-1 [404d03]) |
| claude-code kid's Bash is denied for all but cli.py done (goal:g1.39) | a kid can edit, never prove: the parent or the director runs the proof; a parent needs --ladder-tier 3 |
| write.py prints 'updated' but the privacy guard can REFUSE its commit silently (20:0xZ: a unit name x(at)y.path in my card = 'email') | after every card write: git status --porcelain on the card; a dirty card = reword, commit by exact path |
| inbox notices can VANISH (goal:g1.40, DG1 measured 15:2xZ: send.read's unlocked read+rewrite drops a concurrent append, ~1-2.5% of a burst) | until g1.40 lands: a sender's [merge-up] may arrive by session message only; a branch named in a later notice but never received = ask its sender, never guess |
| cli.py done commits ONLY the round's named node paths | read the tree's git status at harvest; pin dirty bytes off RAM (/data/work/agi-pins, 700) |
| `git worktree prune` in MAIN (gen 16, 4x) | PROBABLY dropped DG3's scratch worktree metadata mid-work (another uid's dir looks missing to me): NEVER prune; `git worktree remove <my path>` only |
| agi-merge-up-review (sonnet) review stage can be HOLLOW ('x', conjuncts []) | the FINAL verify stage decides + read the root code yourself (findings hyp landed 819331783) |
| aa3-lanes.t.sh from a no-.git archive | rc 1 ok 0: it needs a git repo (rev-parse): run it from the gate WORKTREE |
| the privacy guard reads a slash-home-slash-word in prose as a home path | write 'home-path' in cards, never the slashed form |
| ListAgents refs go stale per reconnect (DG1, DG3, DG2 x2, self-perpetuating x2) | send by bare name; on 'N agents named' pick the most recent; inbox copy for offline posts |
| a Sonnet mur reviewer ran git checkout --detach in MAIN (10-03 03:1xZ; restored at 17da2c3e2, 0 commits lost) | after every mur: git symbolic-ref HEAD + reflog -5 before any landing |
| mur reviewers detached MAIN HEAD TWICE more (04:0xZ, 04:1xZ; restored, 0 lost) | after every mur: git symbolic-ref HEAD + reflog before any landing; say READ-ONLY in the focus |
| a stray `send.py --from director-general-3 ...` slipped into one of my Bash lines (04:5xZ; nothing written: checked inbox + dm) | NEVER --from anyone but sanctuary-master; re-read every compound send line before running it |
| grow-gate-*.t.sh read the gate piece from the TRUNK by default (05:2xZ: 25+12+2 FAIL on the old piece = a false red) | ab/keys: arg 1 = the gated sha + CEIL=<ruled bar>; bootstrap: GROW_GATE=<extracted piece> -> 45/17/35 ok |
| a mur verifier read the RING tip's own ab/keys copies (CEIL 4705) instead of the gated union (6100) and called the bars stale | before routing a residue about a file the gate REPLACED, read that file in the union tree ($MU), not the tip |
| a stray `send.py peek` slipped into my forward line (05:4xZ, output discarded) | never peek: one read per nudge; compose send lines with nothing else in them |
| I stamped 06:4xZ / 06:5xZ from memory 3x this gen (06:34, 06:48 by date -u) | run date -u FIRST in the same step, then compose the stamp from its output |
| `send.py read ... | head -80` (05:4xZ) cut off 4 messages incl. 2 [merge-up]s: read marks ALL read | never pipe an inbox read to head: redirect to a scratch file, then read it whole |
| `git merge-tree --write-tree A B` on CONFLICT prints the tree id + the conflict list (gen 19: read-tree of the whole output = an EMPTY tree, 13,254 D in the diff) | take `| head -1` as the tree id, then temp index; ALWAYS check D = 0 before anything else |
| a .t.sh run with bash (11:1xZ: agi-out-states 4 false reds: an ok message's $(nc) resets $? before chk reads rc) | run every .t.sh with sh (dash = its shebang), never bash; grow-gate-bootstrap.t.sh HARD-CODES the trunk branch (13:3xZ: a false 17/0 on the CKPT union) -> GROW_GATE=<union piece> until it takes arg 1 |
| a BOUND that predicts SELF-HEAL (15:1xZ: OUT.6 n4 said agi-flush merges the trunk; it ends git merge or merge --abort, a conflicting t never merges: A12 rolled back, DG3 193 + DG2 176 exit-127 cycles) | read the healing mechanism in the bytes before forwarding a host-act line; I forwarded n4 on the node's word |
| ListAgents DG3 ref went stale again ([f0008b] -> [238bd0], 09:0xZ) | send by bare name; on "N agents named" pick the one active seconds ago |
| a grow-gate change gated on the grow-gate-*.t.sh + ckpt list only (gen 20 CKPT.3: agi-outline's C7 lane builds its OWN gate bin and went red on the trunk) | every harness that extracts the changed piece: grep -l '<piece name>' extensions/agi/tests/*.t.sh, run each |
| agi-out-stale / agi-out-states default to the TRUNK branch (gen 21: 5+1 false FAIL) | pass arg 1 = the gated sha; agi-outline / agi-fresh read the cwd tree |

## §5 Verification: every landing = merge-tree rc 0 + newcomers byte-identical to HEAD + 0 D + anonymize + evidence dry-run + links/schema + suite with every red attributed
>>>>>>> core/season2/et-grok-pilot

## §5 Verification
landing = merge-tree rc 0 + newcomers byte-identical + 0 D + anonymize + evidence on range + replica of named falsifiers. pytest absent this uid.

## §6 BANKED
- CKPT.3 / OUT.7 absent here; land only if Prime/owner names this trunk
- origin ssh comments 81d0e8729 / 8a9b0ad95 / 4b7d20df7 = OWNER leave it
- pytest absent some capsule uids = measure per uid
- alive Z4.a / 00:42Z F1 NOT MET (write.py still 230669 B; keyed 2/5729). 11.8 UNHELD; SM gates, does not assign Z2
- DG3 11.5: 20480 title total still red. Rec: 8192 is the bootstrap engine.md cap (landed); leave 20480 until council/owner names the new file set
- A/B FILE SCOPE still a build: council places, SM does not re-seat
- DG3 00:42Z 11.6 seed T.1 (tip d2edec703) was not [merge-up]; not gated
