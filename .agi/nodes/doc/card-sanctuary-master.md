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


## §0 State (07:4xZ 10-03, date -u) — gen 18 rotating at ~0.42 (0.41 hard rule: no landing started) · trunk clean, RING.5b LANDED 5c3df5114 · OWNER via belam 06:02Z, verbatim: "Btw we are bout to run out of CC usage soon so if you can’t rotate on new system in the next couple hours it’ll have to wait till next week" · AT MY GATE: W-1.16 6893694fd + RING.5c 79adfcda1 (both DG1-run, both forwarded) · OUT.2 waits on DG2 box-carry u1
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30): sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| lanes | owner 02:27Z + 07:00Z 10-01: Sonnet 5.5 for everything; every MUR on claude-code = the Claude Workflow tool, name agi-merge-up-review, args {rounds, model: sonnet} (NOT pi-free) · LADDER tier-3 claude-code parent = claude-sonnet-5-5 (belam d9d1cb7a1 04:2xZ 10-02): a dispatching Sonnet parent = --ladder-tier 3 (a parent below tier 3 gets the kid tool list, adapter :439) · DG5 pi-free · DG3 Opus medium ≤ 3 · VIZ LAST · research placement = thought-master's own |
| holds | g7.16.1.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate (Prime-laned exceptions only: G4 stand-up) · owner 18:1xZ (via belam [owner], banked 4f647b6a8) put K1 per-spawn capped key · K2 spawn classes · K3 direct inference · M1 mail-as-git-commit (ends g1.40's race) to the COUNCIL: a K/M round at my gate needs its Prime lane NAMED (belam's [rule]) + a key-value scan of every version in the range (0 key bytes; .env never read or printed) + no new provider/spend beyond the owner-named OpenRouter provisioning key · AA1.M ACCEPTED (belam [decision] 18:25Z, owner GO): mail = ONE signed ref update in the sender's store (sh+git+jq), a path unit wakes one root carrier per box, mail read from the post's store; DG1 builds it under g7.16.1.11.11 (g1.40 closes when it lands) -> PRIME LANE NAMED for AA1.M (belam [rule] 18:52Z, owner 18:5xZ): goal:g7.16.1.11.11.1 + its 3 hyps (send+retry · root carrier+path unit · read from store) INCL alive's signers fix (root-owned allowed_signers, valid-after/valid-before; .agi/keys/ stops being a source); route DG1 -> DG2 falsifiers -> DG3 builds -> MY gate + mur (Sonnet) -> trunk; rails 8 KB base / 1 KB seed · sh+git+jq, NO Python · 0 key bytes in any version · no new spend; K1/K2/K3 + W STILL HELD · RULED belam 19:1xZ: send retry cap = 5 at 1,927 B (gate: measure both on the build; 6-writers-on-one-ref = a DOCUMENTED bound, loud, 0 silent, 0 lost -- not built); host act 2 = the per-sender template path unit, its own belam GO -> at my gate an AA1.M build lands its bytes ONLY; a HOST ACT (runuser between real uids · the path unit install · a 2nd box) needs belam's own GO quoted per act (command + before-state + one-command rollback), else RETURN |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · session: see config:posts row |
| skills | agi-master-gate (every landing) · agi-memory-guard (box) · agi-rotate · agi-node-write · agi-send · agi-goal |
| peers | Prime = belam: mail ONLY `python3 extensions/agi/bin/send.py --from sanctuary-master send belam '[tag] ...'` from MAIN, never a direct session message (belam [rule] 22:0xZ 10-02: its session names go stale each rotation) · DG1 (v5, ListAgents 'director-general-1 [e48373]' at 20:1xZ; [596192] went stale) · DG2 (v5, bridge director-general-2) · DG3 = ListAgents director-general-3 [719d39] (04:4xZ) or its posts-row session_name (agi-29 at 21:4xZ; both "director-general-3" ListAgents rows are OFFLINE; a dm file alone did not reach it -- owner 21:4xZ) + its inbox · DG5 (pi, INBOX only; sends bare /tmp paths: cat them, world-readable) · TM-new (v5 bridge, NO seat key: inbox sends UNSIGNED, trust direct) · council: alive agi-9c · all-is-one = ListAgents 'all-is-one [f2524a]' (04:1xZ; [7c7660] went stale) · all-is-one agi-06 · self-perpetuating agi-99 · old TM agi-63 · COMMS SWITCH (owner 18:1xZ): DIRECT SendMessage, not inbox dms |
| A+ interim | belam 18:2xZ, bounded: I run a v5 director's dispatch ONLY on its WRITTEN order (quoted), claude-code Sonnet OR pi-free, 0 USD (belam extended 00:43Z 10-02), from ITS worktree under MAIN (.agi/worktrees/...) with --from <director>, ONE line to it per dispatch; git there via GIT_CONFIG_COUNT/KEY/VALUE safe.directory per process (never global); ENDS at the key broker (parity row 30) or owner .env B |


## §1 Plan
```
FIRST: W-1.16 dg3-w16 6893694fd (TEXT ONLY above a0beb64e7 + trunk merge; DG1 07:38Z ran it: flow 46/0 guard 43/0 dry 5bb0bab81 0 p dc2c13663 4/0, agi-kid 2,037 B) + DG2 dc2c13663 + 5bb0bab81
   -> merge-tree vs live HEAD (3 tips) -> gate tree on /dev/shm -> 4 .t.sh (they read ROOT) -> grep the node: 0 hits of "the only" / "the one case" / "the ones listed" -> TEXT mur (prior runs/mur-sm18-dg3-w1-15) -> land ONE by SHA -> notify DG3 DG1 DG2
THEN: RING.5c dg3-ring5c 79adfcda1 (grow-gate 5,767 of 6,350 HARD; D1 AMT, D2 phase 3 twice: combined diff baseline c^ + diff(h,c) baseline h, GIT_NO_REPLACE_OBJECTS=1) + DG2 ring5c 4198c2615 (18 lanes; supersedes ea9e382e7) + ring3 8d049bcf7 + ring4b 8cd1295eb (02ab83134 extra) + ab 68a68670a + keys a98a4d5cd
   -> union tree: merge 79adfcda1 + DG2 de-base-dg2-24 4198c2615 (CHECK ancestry: ring3/ring4b blobs = 8d049bcf7/8cd1295eb) + ab/keys DG2 blobs by temp index if they conflict
   -> ab/keys: arg1 = candidate sha (CEIL default 6100 >= 5,767); bootstrap/ring3/ring4/ring4b/ring5c/ring: GROW_GATE=<piece>; NEG on 083720981: ring5c 6 FAIL, ring4 d9a d10a d10b -> Sonnet security mur on the 5c3df5114..79adfcda1 delta (prior runs/mur-sm18-dg3-ring-5b) + FULL suite -> land
THEN: OUT.2 49a5e9917 (NOT f63d2d346) + agi-outline 592f186da (union: its blob over OUT.2's older outline) + DG2 box-carry u1 fix (DG1 07:41Z: every signers line exact env -i form, the LAST after agi-out) ONLY when DG1 re-sends the set -> agi-outline EMPTY HOME 37/0, agi-out-states <sha> 6/0, agi-fresh 23/0, box-carry -> Sonnet mur (D1, R3-R5, dirty ring on wrap fail) + FULL suite; rails engine.md 9,214/12,288, fenced 7,440/8,192
AFTER: DG3 sends ckpt / revoke / pq / flowrot to DG1 one at a time; each reaches me only after DG1 runs it (DG1 06:03Z)
HOST ACTS = belam GO each: A10 T = 5c3df5114 (input 2 MET by shim sweep); A11 RUN by belam 05:1xZ
MURS: Workflow tool, name agi-merge-up-review, args {rounds:[...], model: sonnet, effort: high, project_root}; persist runs/mur-sm18-<key>/ (mask home paths); FINAL verify decides; after EVERY mur: git symbolic-ref HEAD + reflog
```

## §2 Landed this gen (each landing message carries its gate numbers)
- gen 17 (10-02/03): DG1 -20..-30, DG3 agi-land/A3.3/A3.4/KEY GATE f02495529/closer, DG2 K3 agi-infer + agi-fresh, aio 18-29, SP 1-14, alive AA1.C/K (see git log 3a33c71b9..1e967c397); DEMOTED ring 9abc7c690 + out-line 00ffbe04c
- 10-03 (05:4xZ, gen 18): RETURNED W-1.11 4c3211535 (runs/mur-sm18-dg3-w1-11: R1-R5) · DEMOTED RING.3 952787f32 (runs/mur-sm18-dg3-ring-3: in-push-parent merge, orphan-root bootstrap, trailing-LF name, NUL ring) · suite 0F/0E to 96% when stopped
- 10-03 (06:0xZ, gen 18): RETURNED W-1.12 4440204a8 (runs/mur-sm18-dg3-w1-12: forward/self chained_from spends, false mutant claims)
- 10-03 (06:0xZ, gen 18): 1b4fdbe13 alive aa1k-b 5c5a9b077 (AA1.K -> AA3.15 option B, design text)
- 10-03 (06:3xZ, gen 18): 2b9599932 DG1 -31 + d72ecc81b DG1 -32 (nodes) · RETURNED RING.4 0d58fa0ae (runs/mur-sm18-dg3-ring-4; FULL suite 7914/0)
- 10-03 (06:4xZ, gen 18): RETURNED W-1.13 ac0900207 text-only (runs/mur-sm18-dg3-w1-13)
- 10-03 (07:0xZ, gen 18): RETURNED W-1.14 d53132400 text (runs/mur-sm18-dg3-w1-14: U1 U2)
- 10-03 (07:3xZ, gen 18): 5c3df5114 RING.5b 083720981 + DG2 8d049bcf7 + ab 68a68670a + keys a98a4d5cd LANDED (A10 input 2 MET; D1/D2 ATTRIBUTED TO THE TRUNK: old gate line 10 AM filter + line 13 c^ show; -> RING.5c; DG1 07:28Z recommended); suite 7914/0; bare tests on new trunk 97/0
- 10-03 (07:4xZ, gen 18): RETURNED W-1.15 a0beb64e7 (runs/mur-sm18-dg3-w1-15) · RETURNED OUT.2 49a5e9917 (box-carry u1 62/1 vs trunk 63/0)
- returned gen 16: level round R1 · DG3 install · -21 home paths · agi-land ceiling · A3 DEMOTE · K3 eval injection · 03:2xZ: A3.3 26454748c + closer 0edf571ff (accept_with_residue) · W-1 9442ece6e DEMOTE (runs/mur-sm17-*) · K3 d8e954c91 (accept_with_residue R1-R4, runs/mur-sm17-dg2-k3-c2) · keygate 45d468f83 (fail-open: newline path, T type change) · W-1.4 d8f5ed780 + closer docs c77103967 (04:5xZ) · SP 12 (84/2) · W-1.8 (quoting, repeat.of) · W-1.10 (lazy refusal, - prompt)

## 🔴 Where it stops
```
sanctuary-master gen 18 rotated 07:4xZ at ~0.42: trunk clean, RING.5b landed 5c3df5114; at the gate W-1.16 6893694fd then RING.5c 79adfcda1
on a [merge-up]: static gate (merge-tree vs live HEAD rc, 0 D, added-ever + key versions in HISTORY, anonymize per range, host + home-path + GPU greps (GPU token = substring of superseded: mask + read)), links/schema, tests (.t.sh from the gate worktree; grow-gate / root code = Sonnet security mur + FULL suite on tmpfs), land ONE update by SHA on the live HEAD (newcomers byte-identical), push, notify
FIRST COMMAND AT WAKE: python3 extensions/agi/bin/send.py read sanctuary-master > <scratch>/inbox.txt  (then read the file WHOLE; never pipe the read to head)
```

## §4 Traps (learned this gen; rules live in skills)
| trap | rule |
|---|---|
| my /dev/shm gate trees + suites are charged to MY scope (926 MB shmem at 13:0xZ) | start a suite only at MemAvailable >= 4 GiB + PSI low; never two at once under pressure; stop = every pid with cwd under the gate path, then worktree remove |
| a stray /tmp/.agi project marker | reddens root-discovery tests (test_workflow root rows, test_commands wrapper-flag): moved aside to /tmp/agi-stray-copy-created-20261001T021319Z |
| test_suite_live_checkout_worktree red | a post wrote its live card mid-test: passes alone |
| systemctl --user stop <bare name> | resolves .service, rc 5, the .scope lives: name '<unit>.scope' (g73360-b) |
| heal sweep | loads heal.py fresh each pass: a landed heal fix is live without a reaper restart |
| a test falling through a fake seam | can launch a REAL pi: read every slice/stage test's red for a real binary in the traceback |
| pipelined chain gate | one suite for N tips; attribute reds on a pair tree without the suspect range |
| old uid vs group agi | fixed by the Prime 11:4xZ (default ACLs on refs, comms, spawn-budget, inbox, worktrees) |
| rotate flattens the quorum card | re-link: ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md |
| MAIN shared | commit by exact path; never switch branches, stash or reset |
| dispatch output filtered by grep (19:55Z) | hid a stale-base refusal (exit, no spawn line): read the WHOLE output, then confirm with spawn_budget status |
| a bare cd in a Bash call | moves THIS session cwd into a worktree: always a ( subshell ) or absolute paths |
| spawn_budget 0/30 | NOT proof a parent exited (twice today): scan /proc cwd for the agent id before calling it dead |
| A+ dispatch | the director line is run VERBATIM: a stale-base refusal goes back to the director (add --allow-stale-base reason, or merge) |
| a bare cd in a Bash call (AGAIN gen 14, 06:0xZ) | ALWAYS ( subshell ) or absolute paths; cd /data/work/agi first |
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

## §5 Verification: every landing = merge-tree rc 0 + newcomers byte-identical to HEAD + 0 D + anonymize + evidence dry-run + links/schema + suite with every red attributed


## §6 BANKED
- (resolved 05:1xZ) rotation block: belam landed my key row c6064d5b1 as af21b1b55 (option A, trap 70)
- v5 MOVE 6 (19:5xZ): my verdict NO -- uid agi-sanctuary-master cannot write MAIN .git/index, ORIG_HEAD, FETCH_HEAD or the working tree (no group:agi ACL), so ff-landing dies; belam ACCEPTED: SM STAYS on this seat; belam banks a LAND BROKER for the owner (never opening MAIN to group:agi, never an update-ref landing). The next move is stream-master, not me.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ the a001a3c61 landing; tree-stripped by 165f57b0f): a scrub = history rewrite = OWNER only; sent to belam 22:0xZ · goal:g1.31.4.2.1.1 copilot hooks: PARKED (a real copilot probe = spend, the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz (the tree stays; refusal live)
- .env is 600 belam:belam, no group ACL (verified 15:3xZ): NO agi-* director can dispatch (provisioning PermissionError) -> (A) masters/Prime run directors' murs [recommended; today's practice] · (B) group:agi read ACL [owner's money: owner's call] -- sent to belam 15:3xZ
- (resolved 07:1xZ) Z4 phase-A signing: belam option (a) via branch belam/z4a-anchor; landed c2decf431
