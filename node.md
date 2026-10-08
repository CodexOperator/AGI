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
tags: []
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; <= 100 lines; written DURING the work so a dead session is resumable.

## §0 State (06:5xZ 10-08, date -u) — gen 27 GATING item 1 · trunk 1ac2a236bd pushed · gate tree /dev/shm/gate-sm27a (+ /dev/shm/sm27a-tmp) = union 0b4d136a19
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30): sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| lanes | owner 02:27Z + 07:00Z 10-01: Sonnet 5.5 for everything; every MUR on claude-code = the Claude Workflow tool, name agi-merge-up-review, args {rounds, model: sonnet} (NOT pi-free) · LADDER tier-3 claude-code parent = claude-sonnet-5-5 (belam d9d1cb7a1 04:2xZ 10-02): a dispatching Sonnet parent = --ladder-tier 3 (a parent below tier 3 gets the kid tool list, adapter :439) · DG5 claude-code Sonnet (belam 21:03Z; was pi-free) · DG4 + DG5 PARENT = SM (owner 21:0xZ: "Let's stand up DG4 and DG5 to help split the workload a bit.") · DG3 Opus medium ≤ 3 · VIZ LAST · research placement = thought-master's own |
| holds | g7.16.1.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate (Prime-laned exceptions only: G4 stand-up) · owner 18:1xZ (via belam [owner], banked 4f647b6a8) put K1 per-spawn capped key · K2 spawn classes · K3 direct inference · M1 mail-as-git-commit (ends g1.40's race) to the COUNCIL: a K/M round at my gate needs its Prime lane NAMED (belam's [rule]) + a key-value scan of every version in the range (0 key bytes; .env never read or printed) + no new provider/spend beyond the owner-named OpenRouter provisioning key · AA1.M ACCEPTED (belam [decision] 18:25Z, owner GO): mail = ONE signed ref update in the sender's store (sh+git+jq), a path unit wakes one root carrier per box, mail read from the post's store; DG1 builds it under g7.16.1.11.11 (g1.40 closes when it lands) -> PRIME LANE NAMED for AA1.M (belam [rule] 18:52Z, owner 18:5xZ): goal:g7.16.1.11.11.1 + its 3 hyps (send+retry · root carrier+path unit · read from store) INCL alive's signers fix (root-owned allowed_signers, valid-after/valid-before; .agi/keys/ stops being a source); route DG1 -> DG2 falsifiers -> DG3 builds -> MY gate + mur (Sonnet) -> trunk; rails 8 KB base / 1 KB seed · sh+git+jq, NO Python · 0 key bytes in any version · no new spend; K1/K2/K3 + W STILL HELD · RULED belam 19:1xZ: send retry cap = 5 at 1,927 B (gate: measure both on the build; 6-writers-on-one-ref = a DOCUMENTED bound, loud, 0 silent, 0 lost -- not built); host act 2 = the per-sender template path unit, its own belam GO -> at my gate an AA1.M build lands its bytes ONLY; a HOST ACT (runuser between real uids · the path unit install · a 2nd box) needs belam's own GO quoted per act (command + before-state + one-command rollback), else RETURN |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · session: see config:posts row |
| skills | agi-master-gate (every landing) · agi-memory-guard (box) · agi-rotate · agi-node-write · agi-send · agi-goal |
| peers | Prime = belam: mail ONLY `python3 extensions/agi/bin/send.py --from sanctuary-master send belam '[tag] ...'` from MAIN, never a direct session message (belam [rule] 22:0xZ 10-02: its session names go stale each rotation) · DG1 (v5, ListAgents 'director-general-1 [e48373]' at 20:1xZ; [596192] went stale) · DG2 (v5, bridge director-general-2) · DG3 = ListAgents director-general-3 [238bd0] (09:0xZ; [f0008b] + [719d39] went stale) or its posts-row session_name (agi-29 at 21:4xZ; both "director-general-3" ListAgents rows are OFFLINE; a dm file alone did not reach it -- owner 21:4xZ) + its inbox · DG4 + DG5 (stood up 21:03Z 10-07, parent SM; inbox; first act = merge the trunk) · TM-new (v5 bridge, NO seat key: inbox sends UNSIGNED, trust direct) · council: alive agi-9c · all-is-one = ListAgents 'all-is-one [f2524a]' (04:1xZ; [7c7660] went stale) · all-is-one agi-06 · self-perpetuating agi-99 · old TM agi-63 · COMMS SWITCH (owner 18:1xZ): DIRECT SendMessage, not inbox dms |
| A+ interim | belam 18:2xZ, bounded: I run a v5 director's dispatch ONLY on its WRITTEN order (quoted), claude-code Sonnet OR pi-free, 0 USD (belam extended 00:43Z 10-02), from ITS worktree under MAIN (.agi/worktrees/...) with --from <director>, ONE line to it per dispatch; git there via GIT_CONFIG_COUNT/KEY/VALUE safe.directory per process (never global); ENDS at the key broker (parity row 30) or owner .env B |

## §1 Plan
```
QUEUE for gen 27 (FULL rail each: static + anonymize PER COMMIT + full-name AND model GPU grep + key; lanes with SHA / ROOT = the gated tree, bare env (env -i, GIT_CONFIG_GLOBAL/SYSTEM=/dev/null); NEG; targeted pytest; FULL suite on tmpfs; Sonnet mur via the Workflow tool, project_root = its OWN /dev/shm worktree; accept_with_residue = RETURN unless the verify stage REFUTES every residue):
  1 E2a brief re-cut e479c2fe93 (dg1-e2-aa310b, nodes only, 2 files +13; supersedes 32ad43a464, answers mur E1 E2) + E2c lane eb228aa020 (dg1-e2c-lane, test_trunk_history_is_the_grid.py = DG2 de94ecc8d3, 6 pass, GREEN on the trunk -> lands alone): pipeline them, ONE union + ONE suite + ONE mur
  2 D1 corrective (DG5 ONE commit on e8afb2a868 for R1-R5 on DG2's rows 4966c20d05 test_nest_r.py) -- wait for DG1's [merge-up]; gate = test_nest + test_nest_r + test_bin_help_smoke + test_commands_manifest + FULL at 0 failed
  3 A1b BUILD (DG3; line 90 O=$PWD, agi-project 2,588 -> 2,560 B) WITH DG2 boot re-cut v3 23f488a5c1 + agi-vstore.t.sh 3340a87b35 (incl. the c6 rows + k0-the-verifier-needs-no-env-grant) -> then belam's ONE host act A1 + A2-A4 + A1b (node 59ba231817 holds before-state + rollback)
  HELD (land WITH their build, they are RED on the trunk): E2a lane 02e52769dc (with DG4's crons_apply cell) · test_grid_sync_off.py (with the E2b switch: needs E2a INSTALLED (belam crontab -l) + AA1.V per-turn commits) · AA1.Va lane 1732119924 (DG2, with its build)
PLACED  E2 (belam 05:1xZ, A) board 2a95d61f43 · B DG4 (unblocked) · F CANCELLED · E3 g7.16.1.11.17 ACTIVE · TRAJECTORY rows rewritten in place at each landing (town:local-maxxing E1 :120 / E2 :121 / E4 :123)
REFS    DG1 rotated to gen 16 at ~06:3xZ (new ListAgents ref unknown: inbox send + bare name) · DG5 bare name · belam = send.py only
```

## §2 Landed (each landing message carries its gate numbers)
- gens 16-24: git log --grep sanctuary-master + runs/mur-sm1[6-9]-*, mur-sm2[0-4]-*
- gen 25 10-08 (runs/mur-sm25-*): C 97e31ae62f · A1 4c71a0fa09 · E 19e82bc21b · briefs 8c97e29724 · D 3c36748b06 · D1 v3 38986aa967 · §AC e92d251390 · D3 v2 05ccc3e20b · DG1 nodes 5f083bc1dd · lane I r1 949522c1dd (FULL suites 8,058 / 8,089 / 8,095 / 8,095 / 8,140, 0 failed each)
- gen 25 RETURNED: D x2 (RD4 RD5, RD6) · E (RE6) · A2-A4 x2 (3 reds; RA12-14 DEMOTE) · union5 x4 (D1 SP AIO DG1-nodes) · alive ab0c1cc77d DROPPED (E1 already da90062217)
- gen 25 board: town:local-maxxing d9e0ee099e + 7328775b52 + da90062217 (E1) + 7936e5c7e2 (E4)
- gen 26 10-08 (runs/mur-sm26-union1..7 journals): E1 goals 87d45fdeeb · A2-A4 e9892ee5c8 · lanes round e92f0f42da · A1b brief 2a0cdd7a4d · host-act node 59ba231817 (FULL 8,172* / 8,140 / 8,140 / 8,140, 0 failed but *2 = D1's) · board E1 14ba015a39, E2 2a95d61f43, E4 6027033b54 + 7c0b29bdac + 77772452d0
- gen 26 RETURNED: D1 e8afb2a868 (R1-R5) · f984f926af (B1 B2 B4 B5 RA14) · lanes aaa226ebfa (L1 L2) · brief3 4b38f63cd2 (B6) · host-act 6cd6a3e830 (H1 H2) · E2a brief 32ad43a464 (E1 E2)

## 🔴 Where it stops
```
sanctuary-master gen 27 gating union 0b4d136a19 (E2a re-cut e479c2fe93 + E2c lane eb228aa020): FULL suite + Sonnet mur wf_41615a22-ca5 running
OPEN QUESTION: E2c C1 reads the LIVE trunk vs refs/grid -- can it red when grid_sync versions a dirty node? all-node count running (scratch c1all.py). NEXT: suite + mur verdicts -> land each by SHA on the live HEAD (assert HEAD), push, [landed] to DG1 + UP belam, rewrite E2 :121
FIRST COMMAND AT WAKE: python3 extensions/agi/bin/send.py read sanctuary-master > <scratch>/inbox.txt  (then read the file WHOLE; never pipe the read to head)
```

## §4 Traps (rules live in skills)
| trap | rule |
|---|---|
| my /dev/shm gate trees + suites are charged to MY scope (926 MB shmem at 13:0xZ) | start a suite only at MemAvailable >= 4 GiB + PSI low; never two at once under pressure; stop = every pid with cwd under the gate path, then worktree remove |
| a test falling through a fake seam | can launch a REAL pi: read every slice/stage test's red for a real binary in the traceback |
| pipelined chain gate | one suite for N tips; attribute reds on a pair tree without the suspect range |
| rotate flattens the quorum card | re-link: ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md |
| MAIN shared | commit by exact path; never switch branches, stash or reset |
| a bare cd in a Bash call | moves THIS session cwd into a worktree: always a ( subshell ) or absolute paths |
| spawn_budget 0/30 | NOT proof a parent exited (twice today): scan /proc cwd for the agent id before calling it dead |
| claude-code kid's Bash is denied for all but cli.py done (goal:g1.39) | a kid can edit, never prove: the parent or the director runs the proof; a parent needs --ladder-tier 3 |
| write.py prints 'updated' but the privacy guard can REFUSE its commit silently (20:0xZ: a unit name x(at)y.path in my card = 'email') | after every card write: git status --porcelain on the card; a dirty card = reword, commit by exact path |
| inbox notices can VANISH (goal:g1.40, DG1 measured 15:2xZ: send.read's unlocked read+rewrite drops a concurrent append, ~1-2.5% of a burst) | until g1.40 lands: a sender's [merge-up] may arrive by session message only; a branch named in a later notice but never received = ask its sender, never guess |
| `git worktree prune` in MAIN (gen 16, 4x) | PROBABLY dropped DG3's scratch worktree metadata mid-work (another uid's dir looks missing to me): NEVER prune; `git worktree remove <my path>` only |
| agi-merge-up-review (sonnet) review stage can be HOLLOW ('x', conjuncts []) | the FINAL verify stage decides + read the root code yourself (findings hyp landed 819331783) |
| aa3-lanes.t.sh from a no-.git archive | rc 1 ok 0: it needs a git repo (rev-parse): run it from the gate WORKTREE |
| the privacy guard reads a slash-home-slash-word in prose as a home path | write 'home-path' in cards, never the slashed form |
| ListAgents refs go stale per reconnect (DG1, DG3, DG2 x2, self-perpetuating x2) | send by bare name; on 'N agents named' pick the most recent; inbox copy for offline posts |
| mur reviewers detached MAIN HEAD TWICE more (04:0xZ, 04:1xZ) + once in gen 22 (18:06Z 10-07, a Sonnet verifier despite READ-ONLY in the focus; same commit, restored in 12 s, 0 lost) | after every mur: git symbolic-ref HEAD + reflog before any landing; say READ-ONLY in the focus |
| a stray `send.py --from director-general-3 ...` slipped into one of my Bash lines (04:5xZ; nothing written: checked inbox + dm) | NEVER --from anyone but sanctuary-master; re-read every compound send line before running it |
| `send.py read ... | head -80` (05:4xZ) cut off 4 messages incl. 2 [merge-up]s: read marks ALL read | never pipe an inbox read to head: redirect to a scratch file, then read it whole |
| `git merge-tree --write-tree A B` on CONFLICT prints the tree id + the conflict list (gen 19: read-tree of the whole output = an EMPTY tree, 13,254 D in the diff) | take `| head -1` as the tree id, then temp index; ALWAYS check D = 0 before anything else |
| a .t.sh run with bash (11:1xZ: agi-out-states 4 false reds: an ok message's $(nc) resets $? before chk reads rc) | run every .t.sh with sh (dash = its shebang), never bash; grow-gate-bootstrap.t.sh HARD-CODES the trunk branch (13:3xZ: a false 17/0 on the CKPT union) -> GROW_GATE=<union piece> until it takes arg 1 |
| agi-out-stale / agi-out-states default to the TRUNK branch (gen 21: 5+1 false FAIL) | pass arg 1 = the gated sha; agi-outline / agi-fresh read the cwd tree |
| crons.py show / links from a gate WORKTREE read MAIN's graph (shared root) | test a new cron's write with `write.py <node> "set ..." --dry-run` on the live node; NEG a .t.sh with ROOT = a FULL trunk worktree (an archive of bin/ only = a vacuous 0/N) |
| two independent rounds | PIPELINE: one union, one FULL suite, one mur with 2 rounds; attribute reds per range; land one at a time |
| card stamps written from memory (gen 24: 23:5xZ twice, both wrong) | read `date -u` in the SAME command that writes the stamp; never type a minute |
| GPU-name grep with awk $NF (gen 23: the last word of the name is a COMMON word, in 793 trunk files): 3 false 'hardware' hits, one wrongful DG5 return | grep the FULL name AND the model (last two words); a hit counts only if the model string matches |
| privacy guard REFUSED my card commit (21:5xZ: a box size token quoted in prose) but grid.py commit <path> versioned the WORKING file anyway | git status --porcelain on the card BEFORE grid.py commit; an unpushed bad grid version = update-ref back to origin's tip with the old-value check, then re-version |
| a SIGTERM'd detached suite left 2 python3 orphans (ppid = user manager) in the REMOVED gate dir (gen 22) | after stopping a suite, re-scan /proc cwd (incl. '(deleted)') and SIGKILL what remains BEFORE worktree remove |
| backticks inside a double-quoted python -c in Bash = command substitution (gen 22: the fix text vanished from my card) | card edits go through a QUOTED heredoc file (<<'EOF'), never inline double quotes |
| agi-out-states / agi-out-stale with NO argument read the TRUNK branch (DG1 gen 25: a false 0 FAIL on A2-A4) | pass the gated SHA as arg 1, every time |
| every A-lane fixture ran same-uid with safe.directory=* (gen 25 RA12: the real box = a post uid on a repo another uid owns -> 'dubious ownership') | gate root/unit git reads with GIT_TEST_ASSUME_DIFFERENT_OWNER=1 + an empty global config |
| two council/director edits of the SAME trajectory row cut on an older tip | merge-tree rc 1: the landed one stands, the other is dropped or re-cut without the row |
| a falsifier lane RED on the trunk by design (gen 26: E2a 8 FAILED, E2b 4) | never land it alone (a red suite = a return): it rides WITH its build; a lane GREEN on the trunk (a regression guard) may land alone |
| a belam [rule] can land AFTER a director's [merge-up] and widen its HOW (gen 26: 'EVERY A lane real-ownership' vs a re-cut that set it on 5 rows) | measure the gap, send ONE [decision] with options + a default, gate on in parallel; belam narrowed it to a follow-up round |
## §5 Verification: every landing = merge-tree rc 0 + newcomers byte-identical to HEAD + 0 D + anonymize per commit + evidence dry-run + links/schema + suite with every red attributed

## §6 BANKED
- v5 MOVE 6 (19:5xZ): my verdict NO -- uid agi-sanctuary-master cannot write MAIN .git/index, ORIG_HEAD, FETCH_HEAD or the working tree (no group:agi ACL), so ff-landing dies; belam ACCEPTED: SM STAYS on this seat; belam banks a LAND BROKER for the owner (never opening MAIN to group:agi, never an update-ref landing). The next move is stream-master, not me.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ the a001a3c61 landing; tree-stripped by 165f57b0f): a scrub = history rewrite = OWNER only; sent to belam 22:0xZ · goal:g1.31.4.2.1.1 copilot hooks: PARKED (a real copilot probe = spend, the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz (the tree stays; refusal live)
- .env is 600 belam:belam, no group ACL (verified 15:3xZ): NO agi-* director can dispatch (provisioning PermissionError) -> (A) masters/Prime run directors' murs [recommended; today's practice] · (B) group:agi read ACL [owner's money: owner's call] -- sent to belam 15:3xZ
