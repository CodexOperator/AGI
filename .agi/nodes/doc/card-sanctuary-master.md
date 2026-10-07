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


## §0 State (17:0xZ 10-07, date -u) — gen 21 ROTATING at ~0.41 (DECISION: early, below 0.47: the 0.41 hard rule bars landings and every open item ends in one; no gate open) · trunk clean + pushed · 0 known trunk reds
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
OPEN (each arrives as a DG1 [merge-up]; FULL rail each: static + anonymize per commit, lanes + NEG, pytest subset, FULL suite on tmpfs, Sonnet mur; accept_with_residue = RETURN):
  g4.13.1 #3 grid.py: one-line ERROR (flatten git stderr) + a REAL multi-line lock lane (prior murs runs/mur-sm21-dg3-gridcas, -2, -3; NEG base f8e756801b; NEG = DG2 lane 0563a18377 grid-collapse.t.sh n1-lock-real-is-one-error-line, 1 RED on f8e756801b, 53 ok); LIVE via grid_sync */5: re-measure real refs (9,645: 0 merges/nest/ls-tree fails) and watch the first tick
  g7.16.1.11.19 verify re-cut (DEMOTED 23a6591f72: D1 fail-open rc 0 -> rotate.py:4777 _merge_up_suite; D3 substring; D4 no retract; D2 uid-aware; D6 OSError): DG2 lanes c4d60a0b32 (42 ok; 11 RED on 23a6591f72); DG1 RULED all-SKIP suite = rc 3 + no stamp, test_verified_stamp_from_suite.py:69 renamed test_skip_only_is_not_green (a pytest edit in the build)
  g3.8 #3 metrics (last union ad08961a4: lanes 27/0, pytest 410/0, FULL 7,914/0; mur runs/mur-sm21-dg3-gmetrics2 R1-R4 RULED by DG1: R1 parse rows, R2 never leave town node dirty, R3 cell renamed metrics_line, R4 no OpenRouter call in --line; NEG = DG2 lanes 211a0a00c7 graph-metrics.t.sh, 9 RED on 41956e53d5: run ROOT=<dir> BIN=<dir>/extensions/agi/bin sh). LIVE after landing: crons.py apply via grid_sync installs '23 * * * *' within 5 min (crontab -l | grep -c success_metrics = 1); watch the first :23 run: ONE metrics_line commit on town:local-maxxing, node not dirty, cron log no ERR
  then g7.16.1.11.20 (box mail; DG2 lanes b94a30851) as DG1 sends it
HOST ACTS = belam GO each: A10 ckpt on the hub; A12 re-install (bin/agi-out in every v5 t, root-owned env file, /opt/agi/bin lists no agi-out, readlink -f /bin/sh on the host); OUT.8 unit landed 3fb54c655 (install = belam)
MURS: Workflow tool, name agi-merge-up-review, args {rounds:[...], model: sonnet, effort: high, project_root}; FOCUS = READ-ONLY + the gated union worktree + what must never run against MAIN; after EVERY mur: git symbolic-ref HEAD + reflog; persist runs/mur-sm21-<key>/result.json (home masked)
```

## §2 Landed (each landing message carries its gate numbers)
- gens 16-20 (10-02..04): see git log --grep sanctuary-master + runs/mur-sm1[6-9]-*, mur-sm20-*
- gen 21 10-04: CKPT.3 70530c33c · OUT.7 666098f19 · DG3 agi-outline ckpt fixture d4773d9ab
- gen 21 10-07: sp mu-15 b94124031 · DG1 nodes-33b + DG2 o7c2 b4e8bebda · OUT.8 3fb54c655 (FULL 7,914/0) · alive aa1n 5a1760e82 + AA1.S 0b95e3bd8 + aa1s-fix 01fb4669a · aio mu-31 e005cf445 + mu-33 483d23411 · sp mu-16 v2 9245dfe5f + mu-17 7979cd1e9 · DG1 goals daadcbb3f, c6f977e1a, 8bc80981d, 120296316, 5175738fb · thought-master card fcee0469b (grid v18)
- gen 21 10-07 RETURNED/DEMOTED: OUT.8 R1 (-> node bound) · g4.13.1 x3 (R1-R3, V1-V3+N1, multi-line ERROR) · g7.16.1.11.19 DEMOTED · g3.8 x2 (anonymize home token + --help rc 2; R1-R4)

## 🔴 Where it stops
```
GATE OPEN (17:3xZ 10-07): RETURNED g7.16.1.11.19 dg3-verify6 0c6fc2d9a3 to DG1 (SendMessage 17:3xZ; R1 _write_state OSError -> _io_failed + DG2 lane; N1 test header, N2 _perm_skip nonexistent path). PIPELINE U = 36e1bf2c30 = HEAD 50282caef6 + DG1 1/2 g4.13.1 dg3-gridcas2 b00c1db1fb (M1 c72af0d759) + 2/2 g3.8 dg3-gmetrics2 0ee6c275a5, in /dev/shm/sm22-gu, tmp /dev/shm/tmp-sm22u. DONE: both merge-tree rc 0, 0 D, anonymize ok x12 commits, lanes on U grid-collapse 53/0, grid-payload-commit 21/0, graph-metrics 38/0; NEG trunk 37 + 21 FAIL. RUNNING: FULL suite on U (full-U.txt) + Sonnet mur 2 rounds (Workflow wf_cbeb5733-4e9). THEN: g3.8 first-run measure on a scratch clone, land gridcas2 first (re-run merge-tree on live HEAD), then gmetrics2; watch grid_sync's next tick + the first :23 metrics run.
on a [merge-up]: static gate (merge-tree vs live HEAD rc, 0 D, added-ever + every blob origin lacks through anonymize, host, home-path, GPU and key greps), tests (.t.sh with sh from the gate worktree; arg 1 or ROOT = the gated tree), pytest subset + FULL suite on tmpfs (attribute every red: alone, on trunk, by range), Sonnet mur, land ONE update by SHA on the live HEAD, push, notify; a cron/grid_sync path = measure its first live run on MAIN's real data, then watch it
FIRST COMMAND AT WAKE: python3 extensions/agi/bin/send.py read sanctuary-master > <scratch>/inbox.txt  (then read the file WHOLE; never pipe the read to head)
```

## §4 Traps (learned this gen; rules live in skills)
| trap | rule |
|---|---|
| my /dev/shm gate trees + suites are charged to MY scope (926 MB shmem at 13:0xZ) | start a suite only at MemAvailable >= 4 GiB + PSI low; never two at once under pressure; stop = every pid with cwd under the gate path, then worktree remove |
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
| `send.py read ... | head -80` (05:4xZ) cut off 4 messages incl. 2 [merge-up]s: read marks ALL read | never pipe an inbox read to head: redirect to a scratch file, then read it whole |
| `git merge-tree --write-tree A B` on CONFLICT prints the tree id + the conflict list (gen 19: read-tree of the whole output = an EMPTY tree, 13,254 D in the diff) | take `| head -1` as the tree id, then temp index; ALWAYS check D = 0 before anything else |
| a .t.sh run with bash (11:1xZ: agi-out-states 4 false reds: an ok message's $(nc) resets $? before chk reads rc) | run every .t.sh with sh (dash = its shebang), never bash; grow-gate-bootstrap.t.sh HARD-CODES the trunk branch (13:3xZ: a false 17/0 on the CKPT union) -> GROW_GATE=<union piece> until it takes arg 1 |
| a BOUND that predicts SELF-HEAL (15:1xZ: OUT.6 n4 said agi-flush merges the trunk; it ends git merge or merge --abort, a conflicting t never merges: A12 rolled back, DG3 193 + DG2 176 exit-127 cycles) | read the healing mechanism in the bytes before forwarding a host-act line; I forwarded n4 on the node's word |
| push to origin 500 + 'This repository moved' (10-07 15:1xZ) while fetch works | never re-point the shared remote myself (MAIN .git/config, every post): [red] to belam with the request id, never the URL; keep landings local, they are final |
| a grow-gate change gated on the grow-gate-*.t.sh + ckpt list only (gen 20 CKPT.3: agi-outline's C7 lane builds its OWN gate bin and went red on the trunk) | every harness that extracts the changed piece: grep -l '<piece name>' extensions/agi/tests/*.t.sh, run each |
| agi-out-stale / agi-out-states default to the TRUNK branch (gen 21: 5+1 false FAIL) | pass arg 1 = the gated sha; agi-outline / agi-fresh read the cwd tree |
| crons.py show / links from a gate WORKTREE read MAIN's graph (shared root) | test a new cron's write with `write.py <node> "set ..." --dry-run` on the live node; NEG a .t.sh with ROOT = a FULL trunk worktree (an archive of bin/ only = a vacuous 0/N) |
| 'Traceback' greps count lane TEXT ('0 Traceback') | count only non-ok lines carrying it |
| two independent rounds | PIPELINE: one union, one FULL suite, one mur with 2 rounds; attribute reds per range; land one at a time |

## §5 Verification: every landing = merge-tree rc 0 + newcomers byte-identical to HEAD + 0 D + anonymize + evidence dry-run + links/schema + suite with every red attributed


## §6 BANKED
- (RESOLVED belam 11:19Z [decision], option A DONE) capsule cells = branch belam/capsule-rows 1ea2129b5 (cut from 557ab2598, posts.md only, 12/12): NEVER alone -- land it in the ONE update with the OUT.5 corrective (L = T -p HEAD -p DG3-tip -p DG2-tip -p 1ea2129b5), re-verify the 12 rows vs the LIVE posts.md at that landing (rotation cells move); root unit install = belam host act, own GO; ONE [merge-up] line to belam when it lands
- v5 MOVE 6 (19:5xZ): my verdict NO -- uid agi-sanctuary-master cannot write MAIN .git/index, ORIG_HEAD, FETCH_HEAD or the working tree (no group:agi ACL), so ff-landing dies; belam ACCEPTED: SM STAYS on this seat; belam banks a LAND BROKER for the owner (never opening MAIN to group:agi, never an update-ref landing). The next move is stream-master, not me.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ the a001a3c61 landing; tree-stripped by 165f57b0f): a scrub = history rewrite = OWNER only; sent to belam 22:0xZ · goal:g1.31.4.2.1.1 copilot hooks: PARKED (a real copilot probe = spend, the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz (the tree stays; refusal live)
- .env is 600 belam:belam, no group ACL (verified 15:3xZ): NO agi-* director can dispatch (provisioning PermissionError) -> (A) masters/Prime run directors' murs [recommended; today's practice] · (B) group:agi read ACL [owner's money: owner's call] -- sent to belam 15:3xZ
