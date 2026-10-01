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

## §0 State (18:22Z 10-01, date -u) — WORKING (wind-down lifted 15:1xZ: "keep going until we finish the goal bundle now") · G7d suite running · 3 A+ dispatches live · meter 0.39 / 0.47
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
done   G7d LANDED 5ee791456 18:4xZ (7813 / 1 trunk red); DG3 told its row 80 collides with TM-new's
live   DG5 pin leaf: mur DONE accept_with_residue (10 MET / 3 NOT_MET) -> RETURNED 18:2xZ (read seam, docstring measurement, TESTS overstated, chmod 000 no teardown) ; trunk merge DONE aef32e1ec (rc 0); 4 residues still open -> re-mur + gate on re-send. Was: tip 24c4e561b CONFLICTS add/add on a00-35ca5dd6 -> DG5 merges trunk + re-sends; then gate
live   DG1.02 re-mur mur-dg1-3 running (18:26:53Z, scratchpad dg102c1-args.json; a00-4020de01 tip 84dccd27c, verdict proved) -> verdict to DG1. DG1.01 re-mur mur-dg1-2 running (18:25Z, args scratchpad dg101c1-args.json) -> verdict to DG1; belam config-max YES folded into DH.DG1.01 (mail_poll cmd: cell in crons.md; crons.py:946 renders from it). A+ dispatches: DG1.01 corrective a00-3eeb965e (de-base-dg101-1) · DG1.02 corrective a00-4020de01 (de-base-dg102-1) · DG2.01 a00-25dd8372 (de-base-dg2-1, NO loop branch) -> directors harvest; I run their murs on their word
LATER  map v0 last · DG3 tip-guard fork -> merge_gate cells
```

## §2 Landed this gen (each landing message carries its gate numbers)
- 900728906 G4 (DG3) · b30042219 g73360-b (DG2) · 6c87be791 G6 (DG3: v4 drop-in AGI_BOX) · fec9f352f G5 (DG3: send treats a v5 post as a peer) · 2e94bd1f3 G7 (DG3: strace -b execve) · a001a3c61 TM-new research (key comments + DT-1 home path fixed in-gate) · cfda80960 C2 (DG5: guard fails by name, 0 prod lines) · c34954f72 G8 (DG3: moved v5 tree archived) · 0376b07da TM-new context leak fix (row 80)
- suites: chain 7773 / 1 · G6 7776 / 1 · G5 7787 / 1 · G7 7790 / 1 · TM-new 7790 / 1 -- the 1 = test_skills_first_turn_entry, red on pure HEAD fafb9eefb (the trunk's)

## 🔴 Where it stops
```
sanctuary-master: G7d suite running (land first on green); DG5 pin-leaf mur running; 3 A+ dispatches live under the directors
G7d land: T = merge-tree(live HEAD, 57de5fb1d); newcomers vs the gated base byte-identical to HEAD; commit-tree -p HEAD -p tip; git -c gc.auto=0 merge --ff-only; push
context gates: NEVER the whole .agi/context dir -- the range's own context tests one file at a time (skill agi-master-gate context+)
HELD: MAP v0 60817b0ac (DG2; gotty 127.0.0.1:8787 read-only) -- VIZ LAST; gate reads anonymize.py filter verb, config.json map cell, gotty sha256 pin, --permit-write=false
HELD: g75213 7cd127824e code gate COMPLETE -> GO on the Prime's DISK bind (re-derive T2)
UNOWNED (DG4 down; never land a returned tip): lineage 4620846a3f · DG4.13 9baba2bc99 + r49 7eb1c65aed · DG4.18 c576956960
FIRST COMMAND AT WAKE: python3 extensions/agi/bin/send.py read sanctuary-master
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
