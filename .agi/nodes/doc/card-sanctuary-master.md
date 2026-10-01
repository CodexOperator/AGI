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

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (19:06Z 10-01, date -u) — ROTATING at 0.44 (line 0.47) · G10 URGENT suite re-armed in bg · 5 rounds live under directors · no move held on me except G10
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30): sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| lanes | owner 02:27Z + 07:00Z 10-01: Sonnet 5.5 for everything; every MUR = workflow.py run agi-merge-up-review --harness claude-code (NOT pi-free) · DG5 pi-free · DG3 Opus medium ≤ 3 · VIZ LAST · research placement = thought-master's own |
| holds | g7.16.1.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate (Prime-laned exceptions only: G4 stand-up) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · session: see config:posts row |
| skills | agi-master-gate (every landing) · agi-memory-guard (box) · agi-rotate · agi-node-write · agi-send · agi-goal |
| peers | Prime = belam (agi-6a) · DG1 (v5, bridge director-general-1) · DG2 (v5, bridge director-general-2) · DG3 (agi-e1, the ONLY director that can still dispatch) · DG5 (pi, INBOX only; sends bare /tmp paths: cat them, world-readable) · TM-new (v5 bridge, NO seat key: inbox sends UNSIGNED, trust direct) · council: alive agi-9c · all-is-one agi-06 · self-perpetuating agi-99 · old TM agi-63 · COMMS SWITCH (owner 18:1xZ): DIRECT SendMessage, not inbox dms |
| A+ interim | belam 18:2xZ, bounded: I run a v5 director's dispatch ONLY on its WRITTEN order (quoted), pi-free only, 0 USD, from ITS worktree under MAIN (.agi/worktrees/...) with --from <director>, ONE line to it per dispatch; git there via GIT_CONFIG_COUNT/KEY/VALUE safe.directory per process (never global); ENDS at the key broker (parity row 30) or owner .env B |

## §1 Plan
```
NEXT   G10 5987d7656 (DG3 URGENT, belam red: v5 meter read 0, MOVE 3 waits on it): gate tree /dev/shm/smgate10 (ids /dev/shm/sm-gate-g10.txt H M T); run 1 MEMSTOPPED 19:02:43Z (cause = git auto-gc, belam set gc.auto 0); run 2 auto-starts at mem PSI some60 < 10, log /dev/shm/smtmp10/suite.log -> LAND FIRST on green
NEXT   PLACE 2 heal rounds (belam 19:0xZ, A+ ok): (a) heal crash-respawn writes the NEW pid into the row (falsifier: one respawn, two passes, one live session); (b) heal.py:3660/3665 tells non-prime seats `ack --gen` -> the ack line moves to config:rotations keyed by role (template-max). Mint under goal:g1, offer to a director, dispatch on its written line.
MURS   DG1.02 mur-dg1-3 (verdict -> DG1) · DG5 pin leaf mur-posts-director-general-5-2 on 63a629410 (on accept: gate vs MERGE-BASE, the range carries trunk merges) · DG2.01 mur-de-base-dg2-1 on d8c25b18e..aa20f195f (verdict -> DG2, then gate)
QUEUED TM-new 165f57b0f (seeds x3 replication DISPROVED by its pre-registered rule; 22 files +4254, datasets 3x0.9 MB, 1 config cell osc_neuron_period_seeds_dir, osc_neuron_period_seeds_test.py; TM-new applied the key-comment + home-path fixes itself -- VERIFY them; context gate = that test file alone under timeout + leftover count). G10 suite pid 2852179 RUNNING since 19:04:16Z. LIVE   DG1.03 parent a00-b465ec27 (de-base-dg101-2; I killed its runaway find 19:0xZ, DG1 told) -> DG1 harvests, asks the re-mur
LATER  map v0 last · DG3 tip-guard fork -> merge_gate cells · DG3 row-80 clash on goal:g7.33.19 (told)
```
Run args live in my session scratchpad (gone at rotation): rebuild a mur from the director's [merge-up] dm (shape: workflow.py run merge-up-review --harness pi-free --args '{"rounds":[{key,hypothesis,experiments,files,focus,merge_up,old_tip,new_tip}]}', focus starts with the LEAN line).

## §2 Landed this gen (each landing message carries its gate numbers)
- 900728906 G4 (DG3) · b30042219 g73360-b (DG2) · 6c87be791 G6 (DG3: v4 drop-in AGI_BOX) · fec9f352f G5 (DG3: send treats a v5 post as a peer) · 2e94bd1f3 G7 (DG3: strace -b execve) · a001a3c61 TM-new research (key comments + DT-1 home path fixed in-gate) · cfda80960 C2 (DG5: guard fails by name, 0 prod lines) · c34954f72 G8 (DG3: moved v5 tree archived) · 0376b07da TM-new context leak fix (row 80)
- suites: chain 7773 / 1 · G6 7776 / 1 · G5 7787 / 1 · G7 7790 / 1 · TM-new 7790 / 1 -- the 1 = test_skills_first_turn_entry, red on pure HEAD fafb9eefb (the trunk's)
- after 18:0xZ: 0376b07da TM-new context leak fix · cfda80960 C2 · c34954f72 G8 · 5ee791456 G7d -- every suite 1 red = skills_first_turn (trunk's)

## 🔴 Where it stops
```
sanctuary-master rotated 19:0xZ at 0.44: G10 URGENT gate suite re-armed in bg, land it first; 3 murs + 1 dispatch live under directors
G10 land: T = merge-tree(live HEAD, 5987d7656); newcomers vs the gated base byte-identical to HEAD; commit-tree -p HEAD -p tip; git -c gc.auto=0 merge --ff-only; push; dm DG3 + belam (MOVE 3 waits)
if the bg waiter died with me: check /dev/shm/smtmp10/suite.log + suite.pid; no suite running -> relaunch (cd /dev/shm/smgate10; env -u TMUX -u TMUX_PANE TMPDIR=/dev/shm/smtmp10 setsid nohup python3 -m pytest -q -p no:cacheprovider -rf --basetemp=/dev/shm/smtmp10/bt extensions/agi/tests/)
read the VERIFY's refuted flags before relaying any residue (19:0xZ: I relayed 2 refuted ones to DG1)
HELD: MAP v0 60817b0ac (DG2; gotty 127.0.0.1:8787 read-only) -- VIZ LAST; gate reads anonymize.py filter verb, config.json map cell, gotty sha256 pin, --permit-write=false
HELD: g75213 7cd127824e code gate COMPLETE -> GO on the Prime's DISK bind (re-derive T2)
UNOWNED (DG4 down; never land a returned tip): lineage 4620846a3f · DG4.13 9baba2bc99 + r49 7eb1c65aed · DG4.18 c576956960
FIRST COMMAND AT WAKE: python3 extensions/agi/bin/send.py read sanctuary-master (and expect DIRECT session messages: the comms switch)
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

## §5 Verification: every landing = merge-tree rc 0 + T2 newcomers byte-identical to HEAD + 0 D + anonymize + evidence dry-run + full suite with every red attributed (alone / pure-HEAD tree)

## §6 BANKED
- goal:g1.31.4.2.1.1 copilot hooks: PARKED (a real copilot probe = spend, the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz (the tree stays; refusal live)
- .env is 600 belam:belam, no group ACL (verified 15:3xZ): NO agi-* director can dispatch (provisioning PermissionError) -> (A) masters/Prime run directors' murs [recommended; today's practice] · (B) group:agi read ACL [owner's money: owner's call] -- sent to belam 15:3xZ
