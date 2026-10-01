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

## §0 State (19:12Z 10-01, date -u) — gen 13 seated 19:06Z, meter 0.11 · G10 suite run 2 at 38% · heal x2 queued with DG3 · DG5 pin2 returned with residues
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
GATE   G9 boot install 2561b390e (DG3 [merge-up] 19:5xZ, residues 0): static gate GREEN (merge-tree rc 0 vs 231658e9a, 5 files, 0 D, posts.md delta = boot:true on the owner's 8 rows ONLY, anonymize ok, evidence 0, nothing auto-projects engine-root.md); suite on /dev/shm/smgate9 (ids /dev/shm/sm-gate-g9.txt H M TG T; log /dev/shm/smtmp9/suite.log) -> on green: T2 = merge-tree(live HEAD, tip), newcomers byte-identical, commit-tree, ff, push; dm DG3 + belam. NOTHING installs: install = belam GO + the owner's Proxmox location
NEXT   TM-new 165f57b0f (seeds x3 replication DISPROVED by its pre-registered rule; 22 files +4254, datasets 3x0.9 MB, 1 config cell osc_neuron_period_seeds_dir, osc_neuron_period_seeds_test.py; TM-new applied the key-comment + home-path fixes itself -- VERIFY them; context gate = that test file alone under timeout + leftover count) -- after G9
MURS   route = the Claude Workflow tool, name agi-merge-up-review, args {rounds, model: sonnet, effort: high, project_root} (workflow.py --harness claude-code only PRINTS that call). wf_0ad5ed4b-641 DONE 19:4xZ: pin3 / dg101-c2 / dg102-c1 = all accept_with_residue -> verdicts in runs/mur-posts-director-general-5-3, mur-dg1-4, mur-dg1-5 (gitignored), sent to DG5 (5 items incl. the key file) + DG1
LIVE   DG1.04 a00-31bde705 + DG1.05 a00-e9f36dcf dispatched 19:5xZ (A+, pi-free, DG1's written rows) -> DG1 harvests -> one Sonnet re-mur of both · DG2.01 mur-de-base-dg2-1 pi-free review still running (I killed its 7.2 GB grep child; re-run via the Workflow route if it dies) · DG3 heal x2 dispatched by DG3 (its Sonnet subagents); heal-pid fix d7a541b94 waits on its mur
LATER  map v0 last · DG3 tip-guard fork -> merge_gate cells · DG3 row-80 clash on goal:g7.33.19 (told)
```
Run args: /dev/shm/sm-murs/ (mur-all.json = the last Workflow args; orders-dg10{4,5}.md). A mur round = {key, hypothesis, experiments, files, focus (starts with the LEAN line), merge_up, old_tip, new_tip}.

## §2 Landed this gen (each landing message carries its gate numbers)
- 900728906 G4 (DG3) · b30042219 g73360-b (DG2) · 6c87be791 G6 (DG3: v4 drop-in AGI_BOX) · fec9f352f G5 (DG3: send treats a v5 post as a peer) · 2e94bd1f3 G7 (DG3: strace -b execve) · a001a3c61 TM-new research (key comments + DT-1 home path fixed in-gate) · cfda80960 C2 (DG5: guard fails by name, 0 prod lines) · c34954f72 G8 (DG3: moved v5 tree archived) · 0376b07da TM-new context leak fix (row 80)
- suites: chain 7773 / 1 · G6 7776 / 1 · G5 7787 / 1 · G7 7790 / 1 · TM-new 7790 / 1 -- the 1 = test_skills_first_turn_entry, red on pure HEAD fafb9eefb (the trunk's)
- gen 13: 14e06f47b G10 (DG3, v5 meter reads the newest usage line; 7823/1 trunk red)
- after 18:0xZ: 0376b07da TM-new context leak fix · cfda80960 C2 · c34954f72 G8 · 5ee791456 G7d -- every suite 1 red = skills_first_turn (trunk's)

## 🔴 Where it stops
```
sanctuary-master 19:3xZ: G10 landed 14e06f47b; 2 murs running on claude-code (DG5 pin3, DG1 dg101-c2), verdicts in .agi/sessions/workflows/runs/<run-key>/
on each mur verdict: read verify_<key>.json refuted flags -> accept = gate vs MERGE-BASE + tmpfs suite (/dev/shm/<gate>, TMPDIR /dev/shm/<other>) -> land by SHA; residue = back to its director
if a mur runner died with me: ls /dev/shm/sm-murs/*.log + workflow.py status; relaunch from /dev/shm/sm-murs/<run>.json (claude-code harness)
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
- v5 MOVE 6 (19:5xZ): my verdict NO -- uid agi-sanctuary-master cannot write MAIN .git/index, ORIG_HEAD, FETCH_HEAD or the working tree (no group:agi ACL), so ff-landing dies; belam ACCEPTED: SM STAYS on this seat; belam banks a LAND BROKER for the owner (never opening MAIN to group:agi, never an update-ref landing). The next move is stream-master, not me.
- goal:g1.31.4.2.1.1 copilot hooks: PARKED (a real copilot probe = spend, the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz (the tree stays; refusal live)
- .env is 600 belam:belam, no group ACL (verified 15:3xZ): NO agi-* director can dispatch (provisioning PermissionError) -> (A) masters/Prime run directors' murs [recommended; today's practice] · (B) group:agi read ACL [owner's money: owner's call] -- sent to belam 15:3xZ
