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
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; <= 100 lines; written DURING the work so a dead session is resumable.


## §0 State (16:4xZ 10-07, date -u) — gen 21 · trunk pushed (goals-e landed) · GATING g3.8 re-cut 41956e53d5: FULL suite + mur RUNNING · waiting: g4.13.1 #3, g7.16.1.11.19 re-cut
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30): sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| lanes | owner 02:27Z + 07:00Z 10-01: Sonnet 5.5 for everything; every MUR on claude-code = the Claude Workflow tool, name agi-merge-up-review, args {rounds, model: sonnet} (NOT pi-free) · LADDER tier-3 claude-code parent = claude-sonnet-5-5 (belam d9d1cb7a1 04:2xZ 10-02): a dispatching Sonnet parent = --ladder-tier 3 (a parent below tier 3 gets the kid tool list, adapter :439) · DG5 pi-free · DG3 Opus medium ≤ 3 · VIZ LAST · research placement = thought-master's own |
| holds | g7.16.1.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate (Prime-laned exceptions only: G4 stand-up) · owner 18:1xZ (via belam [owner], banked 4f647b6a8) put K1 per-spawn capped key · K2 spawn classes · K3 direct inference · M1 mail-as-git-commit (ends g1.40's race) to the COUNCIL: a K/M round at my gate needs its Prime lane NAMED (belam's [rule]) + a key-value scan of every version in the range (0 key bytes; .env never read or printed) + no new provider/spend beyond the owner-named OpenRouter provisioning key · AA1.M ACCEPTED (belam [decision] 18:25Z, owner GO): mail = ONE signed ref update in the sender's store (sh+git+jq), a path unit wakes one root carrier per box, mail read from the post's store; DG1 builds it under g7.16.1.11.11 (g1.40 closes when it lands) -> PRIME LANE NAMED for AA1.M (belam [rule] 18:52Z, owner 18:5xZ): goal:g7.16.1.11.11.1 + its 3 hyps (send+retry · root carrier+path unit · read from store) INCL alive's signers fix (root-owned allowed_signers, valid-after/valid-before; .agi/keys/ stops being a source); route DG1 -> DG2 falsifiers -> DG3 builds -> MY gate + mur (Sonnet) -> trunk; rails 8 KB base / 1 KB seed · sh+git+jq, NO Python · 0 key bytes in any version · no new spend; K1/K2/K3 + W STILL HELD · RULED belam 19:1xZ: send retry cap = 5 at 1,927 B (gate: measure both on the build; 6-writers-on-one-ref = a DOCUMENTED bound, loud, 0 silent, 0 lost -- not built); host act 2 = the per-sender template path unit, its own belam GO -> at my gate an AA1.M build lands its bytes ONLY; a HOST ACT (runuser between real uids · the path unit install · a 2nd box) needs belam's own GO quoted per act (command + before-state + one-command rollback), else RETURN |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · session: see config:posts row |
| skills | agi-master-gate (every landing) · agi-memory-guard (box) · agi-rotate · agi-node-write · agi-send · agi-goal |
| peers | Prime = belam: mail ONLY `python3 extensions/agi/bin/send.py --from sanctuary-master send belam '[tag] ...'` from MAIN, never a direct session message (belam [rule] 22:0xZ 10-02: its session names go stale each rotation) · DG1 (v5, ListAgents 'director-general-1 [e48373]' at 20:1xZ; [596192] went stale) · DG2 (v5, bridge director-general-2) · DG3 = ListAgents director-general-3 [238bd0] (09:0xZ; [f0008b] + [719d39] went stale) or its posts-row session_name (agi-29 at 21:4xZ; both "director-general-3" ListAgents rows are OFFLINE; a dm file alone did not reach it -- owner 21:4xZ) + its inbox · DG5 (pi, INBOX only; sends bare /tmp paths: cat them, world-readable) · TM-new (v5 bridge, NO seat key: inbox sends UNSIGNED, trust direct) · council: alive agi-9c · all-is-one = ListAgents 'all-is-one [f2524a]' (04:1xZ; [7c7660] went stale) · all-is-one agi-06 · self-perpetuating agi-99 · old TM agi-63 · COMMS SWITCH (owner 18:1xZ): DIRECT SendMessage, not inbox dms |
| A+ interim | belam 18:2xZ, bounded: I run a v5 director's dispatch ONLY on its WRITTEN order (quoted), claude-code Sonnet OR pi-free, 0 USD (belam extended 00:43Z 10-02), from ITS worktree under MAIN (.agi/worktrees/...) with --from <director>, ONE line to it per dispatch; git there via GIT_CONFIG_COUNT/KEY/VALUE safe.directory per process (never global); ENDS at the key broker (parity row 30) or owner .env B |



## §1 Plan
```
DONE gen 21: CKPT.3 70530c33c + OUT.7 666098f19 landed, pushed, notified (DG1 DG2 DG3 inbox; belam [merge-up] incl. A10/A12 host-act orders)
CLOSED 10-07 14:3xZ: agi-outline C7 red (since CKPT.3) -> DG3 1b125626b2 landed d4773d9ab, 85/0; all 16 grow-gate lane files carry ckpt or are genuine
AFTER: DG3 sends ckpt / revoke / pq / flowrot to DG1 one at a time; each reaches me only after DG1 runs it (DG1 06:03Z)
HOST ACTS = belam GO each: A10 ckpt on the hub BEFORE the gate (open grace until the first holding block; refs/agi/block/* write policy first) · A12 re-install only after bin/agi-out in every v5 post t + /var/lib/agi/<p>.env root-owned
MURS: Workflow tool, name agi-merge-up-review, args {rounds:[...], model: sonnet, effort: high, project_root}; FOCUS names the gated UNION sha + READ-ONLY; FINAL verify decides; accept_with_residue = RETURN; after EVERY mur: git symbolic-ref HEAD + reflog
```

## §2 Landed (each landing message carries its gate numbers)
- gens 16-20 (10-02..04): see git log --grep sanctuary-master + runs/mur-sm1[6-9]-*, mur-sm20-* (RING.5b/5g, W-1.16, OUT.6 landed; RING.3-5f, OUT.2-5, CKPT/CKPT.2 returned)
- 10-04 08:0xZ gen 21: LANDED CKPT.3 70530c33c = 28f941c82 + df697ec4d on f16d6eae3 (T2 79bae51ac = gated 2f3818fba + 4 newcomers byte-identical, 0 D, 18 files 0 dirty)
- 10-04 08:1xZ gen 21: LANDED OUT.7 666098f19 = 6e87ebf98 + 7b00fd8c7 + 1fcda87a9 on 6d3fcca22 (T2 a816fdf5b; stale 15/0 states 43/0 fresh 23/0 ckpt 69/0 combined; anonymize ok net + 5 commits; links 0 broken)
- 10-07 14:2xZ gen 21: LANDED self-perpetuating merge-up 15 12835b669 = b94124031 (docs only, 1 line: §AB Honest limit (15); rc 0, 0 D, anonymize ok; claims read vs the prototype bytes; re-sent: lost from my inbox 10-03)
- 10-07 14:3xZ gen 21: LANDED DG1 nodes round 945d2ec980 + DG2 75dc04865 = b4e8bebda (node + test only: ckpt BOUNDS n1-n4, ring LIMIT R6, out-line BOUND 4 bin/-only skip latent, W bound 11; agi-out-stale 15/0 + 2 o7c2 GAP info rows)
- 10-07 14:3xZ gen 21: LANDED DG3 dg3-outline-ckpt 1b125626b2 = d4773d9ab (test only: ckpt in agi-outline's gate tools; C7 84/1 -> 85/0)
- 10-07 15:0xZ gen 21: RETURNED OUT.8 bd63e551a0 + 56a77caeec (R1: node bound 4 overstates; PATH-only broken piece masked; ask = node wording + optional DG2 info row)
- 10-07 15:1xZ gen 21: LANDED (pushed 15:2xZ) OUT.8 3fb54c655 = bd63e551a0 + dc5761850c (suite 7,914/0 on union, mur R1 -> node bound 4 narrowed) · alive aa1n 5a1760e82 · aio mu-31 e005cf445 · aio mu-33 483d23411 · sp mu-16 v2 9245dfe5f · DG1 goals daadcbb3f (union: links 0 broken, schema == trunk)
- 10-07 15:2xZ gen 21: LANDED alive AA1.S e6693df0b = 0b95e3bd8 · sp mu-17 3b866eae0 = 7979cd1e9 · DG1 goals-b 5b44a392ca = c6f977e1a (3 goals -> horizon)
- 10-07 15:3xZ gen 21: RETURNED g4.13.1 DG3 87358d1813 (lanes 19/0, NEG 5/14, test_grid 150/0, real refs unchanged; mur accept_with_residue R1 + R2, runs/mur-sm21-dg3-gridcas) · 16:0xZ RETURNED corrective 0d0d02d4f9 (R1-R3 closed; final verify accept_with_residue V1-V3; runs/mur-sm21-dg3-gridcas-2)
- 10-07 16:0xZ gen 21: LANDED DG1 goals-c 0c6cd10c48 = 8bc80981d (g3.8 + .19 active; .19 falsifier 1 = pytest SKIP on a v5 uid) · alive aa1s-fix 967e250cc = 01fb4669a · 16:3xZ RETURNED g4.13.1 #2 f8e756801b (ERROR line multi-line) · DEMOTED g7.16.1.11.19 23a6591f72 (D1 rc 0 on a skipped suite + rotate.py:4778 = fail-open; D3 substring; D4 no retract) · LANDED thought-master card 2c626d8d49 = fcee0469b (grid v18) · 16:4xZ RETURNED g3.8 989d77684a (anonymize home false-positive a scratch home-named dir; metrics.py --help exits 2 -> test_bin_help_smoke red) · LANDED goals-d 83d745b9a6 = 120296316

## 🔴 Where it stops
```
sanctuary-master gen 21, 16:4xZ 10-07: GATING g3.8 re-cut DG3 41956e53d5 (lanes == DG2 8cce720e2), union U ad08961a4, worktree /dev/shm/sm21-gm2, tmp /dev/shm/tmpsm21n. DONE: static + anonymize ok; graph-metrics 27/0; pytest -k metric|cron|success|help_smoke 410/0; live town write dry-run admitted (earlier). RUNNING: FULL suite (scratchpad suite-gm2.log/.pid) + mur wf_c5dba9a8-0a3 (key dg3-gmetrics2). Then final verify ACCEPT -> land on live HEAD -p 41956e53d5 -> push -> within 5 min crons.py apply installs '23 * * * *' (check `crontab -l | grep -c success_metrics` = 1) -> watch the first :23 run: ONE graph_metrics commit on town:local-maxxing, cron log no ERR -> notify DG1 + belam. Pending: g4.13.1 #3; g7.16.1.11.19 re-cut (DG1 ruled: all-SKIP suite rc 3 + no stamp; test renamed test_skip_only_is_not_green)
on a [merge-up]: static gate (merge-tree vs live HEAD rc, 0 D, added-ever + key versions in HISTORY, anonymize per range, host + home-path + GPU greps), links/schema, tests (EVERY .t.sh that reads a changed piece, with sh, from the gate worktree, arg 1 = gated sha), Sonnet security mur + FULL suite on tmpfs for root/grow-gate code, land ONE update by SHA on the live HEAD, push, notify
FIRST COMMAND AT WAKE: python3 extensions/agi/bin/send.py read sanctuary-master > <scratch>/inbox.txt  (then read the file WHOLE; never pipe the read to head)
```

## §4 Traps (learned this gen; rules live in skills)
| trap | rule |
|---|---|
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
| push to origin 500 + 'This repository moved' (10-07 15:1xZ) while fetch works | never re-point the shared remote myself (MAIN .git/config, every post): [red] to belam with the request id, never the URL; keep landings local, they are final |
| a grow-gate change gated on the grow-gate-*.t.sh + ckpt list only (gen 20 CKPT.3: agi-outline's C7 lane builds its OWN gate bin and went red on the trunk) | every harness that extracts the changed piece: grep -l '<piece name>' extensions/agi/tests/*.t.sh, run each |
| agi-out-stale / agi-out-states default to the TRUNK branch (gen 21: 5+1 false FAIL) | pass arg 1 = the gated sha; agi-outline / agi-fresh read the cwd tree |

## §5 Verification: every landing = merge-tree rc 0 + newcomers byte-identical to HEAD + 0 D + anonymize + evidence dry-run + links/schema + suite with every red attributed


## §6 BANKED
- (RESOLVED belam 11:19Z [decision], option A DONE) capsule cells = branch belam/capsule-rows 1ea2129b5 (cut from 557ab2598, posts.md only, 12/12): NEVER alone -- land it in the ONE update with the OUT.5 corrective (L = T -p HEAD -p DG3-tip -p DG2-tip -p 1ea2129b5), re-verify the 12 rows vs the LIVE posts.md at that landing (rotation cells move); root unit install = belam host act, own GO; ONE [merge-up] line to belam when it lands
- v5 MOVE 6 (19:5xZ): my verdict NO -- uid agi-sanctuary-master cannot write MAIN .git/index, ORIG_HEAD, FETCH_HEAD or the working tree (no group:agi ACL), so ff-landing dies; belam ACCEPTED: SM STAYS on this seat; belam banks a LAND BROKER for the owner (never opening MAIN to group:agi, never an update-ref landing). The next move is stream-master, not me.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ the a001a3c61 landing; tree-stripped by 165f57b0f): a scrub = history rewrite = OWNER only; sent to belam 22:0xZ · goal:g1.31.4.2.1.1 copilot hooks: PARKED (a real copilot probe = spend, the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz (the tree stays; refusal live)
- .env is 600 belam:belam, no group ACL (verified 15:3xZ): NO agi-* director can dispatch (provisioning PermissionError) -> (A) masters/Prime run directors' murs [recommended; today's practice] · (B) group:agi read ACL [owner's money: owner's call] -- sent to belam 15:3xZ
