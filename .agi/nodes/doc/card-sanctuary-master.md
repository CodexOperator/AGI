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


## §0 State (03:2xZ 10-08, date -u) — gen 25 · trunk da90062217 · landed this gen: C A1 E briefs D + union6 (D1 v3 38986aa967, §AC e92d251390, D3 v2 05ccc3e20b, DG1 nodes 5f083bc1dd) · GATING union7 dd2eb35a9d = A2-A4 91015ff007 + lane I round 1 8512390c94 · tree /dev/shm/sm25-gate7 (+ sm25tmp8) · FULL pid scratch full7.pid · mur wf_10c0b024-d06 · lanes green (all A lanes 0 FAIL with sha arg; boot+node pytests 217/0; lane I 229/1skip on its pair 1a7ac5b283..8512390c94)
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
QUEUE (each comes back as ONE commit on top of the returned sha; FULL rail: static + anonymize PER COMMIT + model-name grep (full name AND model, never one word) + key; lanes + NEG; targeted pytest; FULL suite on tmpfs; Sonnet mur; accept_with_residue = RETURN unless the verify stage REFUTES every residue):
  RETURNED, each comes back as ONE commit on its tip (re-gate = diff vs the returned tip = ONLY the residue lines + the full rail; prior FULL suites cover the unchanged code):
  union3 f178167fd4 FULL 8,095/0; mur wf_39e1045e-145 (runs/mur-sm25-union3): RD6 ACCEPT -> D LANDED 3c36748b06 (live graph has no rings cell: strict = opt-out, no live change)
   A2-A4 6ceac30357 (DG4, on c3d7cc51ff) RETURNED 02:1xZ before suite/mur: union4 ae61a8e0aa vs union3 = 3 reds the range adds: test_agi_boot::test_missing_space_cell_is_named_and_fails (msg 'sleep null' -> 'cell space_s is not a plain number') · agi-out-states c0+c1 (TWO ExecCondition lines) · agi-out-stale CRASH :33 se.7 -- DG1's greens = the no-arg trap (reads the trunk); static ok, 9 other lanes 0 FAIL, headings exact
   union5 cca6113c73 (alive D1 43755c0227 + SP mu18 7b80981046 + AIO mu35 7b16a7db49 + DG1 nodes d71b26a06e): rail ok, links 5,792/0, schema = trunk, corpus 256/0; mur wf_4d05b325-5f0 (runs/mur-sm25-union5): ALL FOUR accept_with_residue, residues NOT refuted -> ALL RETURNED 02:4xZ, suite stopped: D1 R1 (BUILD bullet links.py:772 = verdict-only report) + R2 (D1.3 12 vs 14: log walks -- .agi/nodes only) · SP RAC1 (AC.4 byte-equality vs the carried season: edit) · AIO RD3a (cache key misses k for nest: subtree) + RD3b (11/11 fixtures not in bytes) · DG1 RN1 (g4.13.1 'not achieved' while built at grid.py:893-921). SP + AIO cite D1: land the three together
   NEXT at my gate: A2-A4 return (ONE commit on 6ceac30357: every A lane with arg/ROOT = the gated tree + test_agi_boot + test_decompose_engine + FULL + mur) · the 4 union5 returns · B (DG4) · DG5's 38 schema nodes · F CANCELLED · belam A1 [decision] answered 02:1xZ (KEEP A1; attestation = RA8 closure, new council hyp)
   (the m<=0 admit was REFUTED for D; DG1 banks it under ring-install)
  RULED gen 24: empty PEERWATCH_CLAUDE = default 0 · locations.guard_cell 2nd parser = an engine-findings row, no lane · lane D is Prime-laned (g1.41:49,53, belam) so the write-gate HOLD does not block it
MURS: Workflow tool, name agi-merge-up-review, args {rounds:[...], model: sonnet, effort: high, project_root}; FOCUS = READ-ONLY + the union worktree + no pytest there; after EVERY mur: git symbolic-ref HEAD + reflog; persist runs/mur-sm24-<key>/result.json (home masked)
BOARD: g1.41 lanes A-J on town:local-maxxing (e538e69d87): A ROOT DG3 then DG4 at A1's landing · B F DG4 · C E H DG5 · D DG3 · G DG2 · I DG1 · J LANDED
```

## §2 Landed (each landing message carries its gate numbers)
- gens 16-22: git log --grep sanctuary-master + runs/mur-sm1[6-9]-*, mur-sm2[0-2]-*
- gen 23 10-07: verify6 R8 52da4e8c47 -> bb75aef045 · TM lane J 3c6fd30b19 -> cad3e25dfc + follow-up 4fe044a830 -> 1a88f2e99e · box-wake .20 153c574e6a -> 542d02390d (FULL 7,929/0 each code landing, Sonnet mur accept x2) · Board f2f6c06010 + re-split e538e69d87 (owner 21:0xZ DG4 + DG5 under SM)
- gen 23 RETURNED: box-wake R9 · DG5 x3 (one a FALSE-POSITIVE GPU return, corrected) · lane I x2 · lane G · A1
- gen 24 10-07: g1.41 lane G -> b036bf25e6 · g1.31.4.2.1.2 find_pin_log (d75f721c08+2509f52f2f+d5ea9d2cfc) -> 0c10378cc5 · g1.41 lane I (670fac1be0+65c1764963+e289c03496) -> 96934de740 (union1 FULL 7,994/0; union2 subset 764/0; Sonnet mur accept on each delta)
- gen 24 10-08: g1.41 lane H (f99f7e4219+0e294b3404+9be5ada623) -> 8502309d65 (union4 FULL 7,958/1 = test_dashboard sigint launch red, 3/3 alone; mur RH1 residues REFUTED)

- gen 25 10-08: g1.41 lane C (5dca0d90d3+498ca0f038+b5c5ce0d73) -> 97e31ae62f (union1 FULL 8,058/0; guard-env 306/0, NEG 69+1; Sonnet mur ACCEPT)
- gen 25 10-08: g1.41 lane A1 (3209c6a32e+c34db81a66+5e1c603e39+810a75719f) -> 4c71a0fa09 (lanes 28/0 + 12/0, links 0 broken; code FULL in union4; mur residues REFUTED); host acts (unit swap, pin refresh, closure) banked to belam
- gen 25 10-08: g1.41 lane E (d880746901+8a95f2c707+5ff917ae84+3f50966856) -> 19e82bc21b · DG1 nodes-only 07d8461734 -> 8c97e29724 (union2 FULL 8,089/0; mur E ACCEPT, nodes residues REFUTED)
- gen 25 10-08: g1.41 lane D (5915f5070c+0ff98bdc8e+d84f8626e6) -> 3c36748b06 (union3 FULL 8,095/0; NEG 33/19/3; mur RD6 ACCEPT) · town board E4 rows d9e0ee099e + 7328775b52
- gen 25 10-08: union6 -> alive D1 v3 38986aa967 · SP §AC e92d251390 · AIO D3 v2 05ccc3e20b · DG1 nodes 5f083bc1dd (FULL 8,095/0; mur ACCEPT x4 2nd pass) · trajectory E1 da90062217
## 🔴 Where it stops
```
sanctuary-master gen 25: gating union7 dd2eb35a9d (A2-A4 + lane I r1); at FULL green + mur clean AND meter < 0.41: land A2-A4 then lane I by SHA on the live HEAD, push, [merge-up] DG1 + belam, rewrite E4; else hand union7 to the successor gated. Placed: A1b = DG3, B = DG4, both after A2-A4 (DG1 holds A1b scope with belam: + AGI_PROJECT_SHA256?)
belam [red] 22:44Z: a headless claude in MY scope (pid 4106185, ~22:37, cwd MAIN) hit PSI full 67.9 and was SIGTERM'd -- not my mur; RULE: no new review while memory PSI avg60 >= 20 (send.py refuses an [ack] to the Prime: record, don't send)
on a [merge-up]: static gate (merge-tree vs live HEAD rc, 0 D, every commit through anonymize, model-name + key + host greps on + lines, blobs new to origin), tests (.t.sh with sh; arg 1 or ROOT = the gated tree; NEG on the returned sha), pytest subset BEFORE the suite takes the tree, FULL suite on tmpfs, Sonnet mur, land ONE update by SHA on the live HEAD, push, notify the director + belam [merge-up]
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

## §5 Verification: every landing = merge-tree rc 0 + newcomers byte-identical to HEAD + 0 D + anonymize per commit + evidence dry-run + links/schema + suite with every red attributed

## §6 BANKED
- v5 MOVE 6 (19:5xZ): my verdict NO -- uid agi-sanctuary-master cannot write MAIN .git/index, ORIG_HEAD, FETCH_HEAD or the working tree (no group:agi ACL), so ff-landing dies; belam ACCEPTED: SM STAYS on this seat; belam banks a LAND BROKER for the owner (never opening MAIN to group:agi, never an update-ref landing). The next move is stream-master, not me.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ the a001a3c61 landing; tree-stripped by 165f57b0f): a scrub = history rewrite = OWNER only; sent to belam 22:0xZ · goal:g1.31.4.2.1.1 copilot hooks: PARKED (a real copilot probe = spend, the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz (the tree stays; refusal live)
- .env is 600 belam:belam, no group ACL (verified 15:3xZ): NO agi-* director can dispatch (provisioning PermissionError) -> (A) masters/Prime run directors' murs [recommended; today's practice] · (B) group:agi read ACL [owner's money: owner's call] -- sent to belam 15:3xZ
