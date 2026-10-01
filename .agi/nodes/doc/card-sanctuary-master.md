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

## §0 State (21:3xZ 10-01, date -u) — gen 14 seated 21:20Z · gate = DG1 e38bdc6f9 (suite on /dev/shm/sm-gate-dg1, M c4c0e3ad4) · 0 murs · DG1 e0a261b7b RETURNED (key blob in history)
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30): sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| lanes | owner 02:27Z + 07:00Z 10-01: Sonnet 5.5 for everything; every MUR on claude-code = the Claude Workflow tool, name agi-merge-up-review, args {rounds, model: sonnet} (NOT pi-free) · DG5 pi-free · DG3 Opus medium ≤ 3 · VIZ LAST · research placement = thought-master's own |
| holds | g7.16.1.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate (Prime-laned exceptions only: G4 stand-up) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · session: see config:posts row |
| skills | agi-master-gate (every landing) · agi-memory-guard (box) · agi-rotate · agi-node-write · agi-send · agi-goal |
| peers | Prime = belam (agi-6a) · DG1 (v5, bridge director-general-1) · DG2 (v5, bridge director-general-2) · DG3 (rotated 19:56Z: new session, use its INBOX) · DG5 (pi, INBOX only; sends bare /tmp paths: cat them, world-readable) · TM-new (v5 bridge, NO seat key: inbox sends UNSIGNED, trust direct) · council: alive agi-9c · all-is-one agi-06 · self-perpetuating agi-99 · old TM agi-63 · COMMS SWITCH (owner 18:1xZ): DIRECT SendMessage, not inbox dms |
| A+ interim | belam 18:2xZ, bounded: I run a v5 director's dispatch ONLY on its WRITTEN order (quoted), pi-free only, 0 USD, from ITS worktree under MAIN (.agi/worktrees/...) with --from <director>, ONE line to it per dispatch; git there via GIT_CONFIG_COUNT/KEY/VALUE safe.directory per process (never global); ENDS at the key broker (parity row 30) or owner .env B |

## §1 Plan
```
NOW    DG1 e38bdc6f9 (dg1-merge-up-2, ONE commit cut from trunk bfcbf7d03; replaces RETURNED e0a261b7b whose 7b37db90f added a host-named pubkey): static gate GREEN, full suite running -> land by SHA (assert HEAD^{tree} == 5ac25bf7b tree, else re-derive T2), push, grid commit --all
NEXT   DG3 heal-pid fix d7a541b94 -> its [merge-up] (offered the Sonnet mur route) · then DG3 heal ack-line round (queued with DG3) · g1.37 heal tri-state (DG3 lane)
HORIZON goal:g1.34 / g1.35 / g1.36 (DG1) · goal:g1.31.4.2.1.2 / .3 (DG5, rotate.py meter seams): place on lanes when a director frees
MURS   route = the Claude Workflow tool, name agi-merge-up-review, args {rounds:[{key, hypothesis, experiments, files, focus (starts with the LEAN no-walk line), merge_up, old_tip, new_tip}], model: sonnet, effort: high, project_root}. workflow.py --harness claude-code only PRINTS that call. Persist verdicts to runs/<run-key>/{review,verify}_<key>.json from the journal (labels via the started rows)
LATER  map v0 last · DG3 tip-guard fork -> merge_gate cells · DG3 row-80 clash on goal:g7.33.19 (told)
```
Scripts kept: /dev/shm/sm-murs/land3.sh (pipelined N-tip landing on the LIVE HEAD with proof; template for the next multi-tip gate).

## §2 Landed this gen (each landing message carries its gate numbers)
- 14e06f47b G10 (DG3) · 0b8f086a5 G9 boot install (DG3; config:posts UNION; nothing installed)
- 67680d223 TM-new a6ac4d92e · d32ef0038 DG1 1554cb042 (+3 home paths anonymized in-gate) · 285f17805 DG5 c700bd684 · 03c5f643b DG2 726b9d4d6 -- ONE pipelined suite 7876/1
- fb4f640e5 DG2 test-only 273931cda (DG5 visibility tests; read by me, no mur) 7884/1
- every suite red = test_skills_first_turn_entry (the trunk red) · grid commit --all 20:5xZ · links 5670/0 · gen 14: 5ac25bf7b agi-master-gate skill: anonymize reads range HISTORY (added-then-removed files ride the merge)

## 🔴 Where it stops
```
SM gen 14 at 21:3xZ: gating DG1 e38bdc6f9 (suite pid 752280, log /dev/shm/smtmp-dg1/suite.log); then DG3 heal-pid d7a541b94 when its merge-up arrives
on a [merge-up]: verdicts or a Sonnet Workflow mur, static gate (merge-tree vs live HEAD, 0 D, anonymize, home grep, evidence dry-run on the gate tree, config:posts cells, first live run of any cron/unit change, NO key files), tmpfs suite, land by SHA, push, grid.py commit --all
FIRST COMMAND AT WAKE: python3 extensions/agi/bin/send.py read sanctuary-master (expect DIRECT session messages too: the comms switch); an empty read is not proof: check the dm files
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


## §5 Verification: every landing = merge-tree rc 0 + T2 newcomers byte-identical to HEAD + 0 D + anonymize + evidence dry-run + full suite with every red attributed (alone / pure-HEAD tree)


## §6 BANKED
- v5 MOVE 6 (19:5xZ): my verdict NO -- uid agi-sanctuary-master cannot write MAIN .git/index, ORIG_HEAD, FETCH_HEAD or the working tree (no group:agi ACL), so ff-landing dies; belam ACCEPTED: SM STAYS on this seat; belam banks a LAND BROKER for the owner (never opening MAIN to group:agi, never an update-ref landing). The next move is stream-master, not me.
- goal:g1.31.4.2.1.1 copilot hooks: PARKED (a real copilot probe = spend, the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz (the tree stays; refusal live)
- .env is 600 belam:belam, no group ACL (verified 15:3xZ): NO agi-* director can dispatch (provisioning PermissionError) -> (A) masters/Prime run directors' murs [recommended; today's practice] · (B) group:agi read ACL [owner's money: owner's call] -- sent to belam 15:3xZ
