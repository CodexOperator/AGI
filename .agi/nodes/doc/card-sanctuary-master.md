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


## §0 State (17:5xZ 10-07, date -u) — gen 22 seated 17:01Z · trunk clean + pushed · 0 known trunk reds (grid_sync logs 2 PRE-EXISTING ERROR lines every tick since 09-30: experiment a00-829ed05f + a00-da06914d have no mint_id) · no gate open
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
  FIRST: belam [red] 18:27Z (VERIFIED, PASS B4, HOLDS the season2/main merge; heal.py:1905 status rc + :1882 rev-parse rc): leaf goal:g7.16.1.5.3.2 LANDED 6bdaf7a00a. dg3-healsweep2 29956e9de2 RETURNED 18:5xZ (R3: hd_rc read only on EMPTY stdout; unborn HEAD prints "HEAD" rc 128 -> fix: if hd_rc != 0 or not head + DG2 lanes 1838d2b677 (12 tests: f3b ["HEAD"]/128, f3c REAL unborn worktree, f6 dry-run SKIP empty; 2 RED on 29956e9de2, 9 RED on trunk) = NEG); gate so far: static clean, test_heal*.py 281/0, new file 7F/3P on trunk, mur runs/mur-sm22-dg3-healsweep2, FULL suite on /dev/shm/sm22-gh running. NEXT: the 1-line re-cut -> test_heal*.py + FULL suite -> land -> [merge-up] SHA to belam (send.py, tag [merge-up]) -> watch heal re-exec + the next sweep lines in ~/logs/agi-reaper-agi-*.log (baseline 18:45Z: only a00-eb774813 remove-failed locked)
  g7.16.1.11.20 box-wake 954522af59 WITHDRAWN by DG1 17:54Z (DO NOT LAND: nobody sends box mail; the re-cut = DUAL ROUTE, agi-run + cccc.ts poll the inbox file AND box n, each source types its own line; the pure-box cutover = a later leaf with belam GO). Re-gate the dual-route build when DG1 sends it NEG = DG2 32c2f4704a box-wake.t.sh (26 lanes; 954522af59 4 FAIL, trunk pieces 18 FAIL; ROOT = a tree with .geometry/engine*.md + bin)
  g7.16.1.11.19 verify: RETURNED x2 in gen 22 (0c6fc2d9a3 R1; a159c558c6 18:0xZ R2 = mkdir in _write_state ~:886 + _record_suite_ts ~:1283 outside the try -> traceback; notes N4 stamp on rc 2, N5 l8 comment, N6 first-path skip). a159c558c6 gate: lanes 49/0, NEG trunk 27 FAIL, NEG 0c6fc2d9a3 5 FAIL, mur accept_with_residue (runs/mur-sm22-dg3-verify6-final), FULL suite 7,915/0. DG1 RULED 18:09Z: R2 both mkdirs + :1040 lock mkdir into their try; N4 fail-closed (no stamp when _IO_ERRORS); N5 comment; N6 banked. NEXT: DG3 one commit on a159c558c6 + DG2 lanes 29ad3d5bbe (d6g1 d6g2 d6h d6i + d6j control; 4 RED on a159c558c6) = NEG; build also needs _io_failed to judge the nearest EXISTING ancestor (DG2)
LIVE (measured, closed): grid_sync 17:55Z tick on the new grid.py = 9 refs pushed, 0 update-ref ERROR, 0 skip (the 2 no-mint_id ERROR lines predate it: 150 in the log since 09-30); graph_metrics installed (crontab = 1); FIRST :23 run = commit 171ffe7b35 18:24:06Z, +1 line, 1 metrics_line cell, town node clean, no skip/ERR
FOLLOW-UPS sent to DG1 (not blocking, F1-F5): metrics_cell edited_by/cell window · avg_tokens row-1 only · producer timeout/flock · _rename_ref folds create failures into conflict · CAS-miss English-text match
MURS: Workflow tool, name agi-merge-up-review, args {rounds:[...], model: sonnet, effort: high, project_root}; FOCUS = READ-ONLY + the gated union worktree + what must never run against MAIN; after EVERY mur: git symbolic-ref HEAD + reflog; persist runs/mur-sm22-<key>/result.json (home masked)
```

## §2 Landed (each landing message carries its gate numbers)
- gens 16-21: see git log --grep sanctuary-master + runs/mur-sm1[6-9]-*, mur-sm2[01]-*
- gen 22 10-07: g4.13.1 #3 dg3-gridcas2 5895e8bea5 + g3.8 #3 dg3-gmetrics2 1e930932ea (union 36e1bf2c30 FULL 7,915/0, mur accept x2, links 5778/0)
- gen 22 10-07 RETURNED: g7.16.1.11.19 dg3-verify6 0c6fc2d9a3 (R1 baseline write fail-open)

## 🔴 Where it stops
```
19:1xZ 10-07: BOTH RETURNED (mur runs/mur-sm22-g2-heal-verify, accept_with_residue x2): heal 9ebf332a36 R4 = a listed unborn tree caches the zero oid, skips the rc guard, update-ref <zero-oid> DELETES an existing archive ref (fix: null-oid cached head = no head; lane = f3c without the cache stub + a planted archive ref survives); verify edce42f35b R5 = lanes for the lock-mkdir (None, None) refusal + a retract failing on an owned 555 dir. Union 9b88e0b2f0 FULL suite still running in /dev/shm/sm22-g2 (a red goes to DG1). NEXT: the two re-cuts pipelined (heal lands FIRST, then [merge-up] SHA to belam via send.py), then .20 dual route d926526a71 (lanes 32c2f4704a)
on a [merge-up]: static gate (merge-tree vs live HEAD rc, 0 D, added-ever + every blob origin lacks through anonymize, host, home-path, GPU and key greps), tests (.t.sh with sh from the gate worktree; arg 1 or ROOT = the gated tree), pytest subset + FULL suite on tmpfs (attribute every red: alone, on trunk, by range), Sonnet mur, land ONE update by SHA on the live HEAD, push, notify; a cron/grid_sync path = measure its first live run on MAIN's real data (a --shared scratch clone, the rendered line, env -i), then watch it
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
| mur reviewers detached MAIN HEAD TWICE more (04:0xZ, 04:1xZ) + once in gen 22 (18:06Z 10-07, a Sonnet verifier despite READ-ONLY in the focus; same commit, restored in 12 s, 0 lost) | after every mur: git symbolic-ref HEAD + reflog before any landing; say READ-ONLY in the focus |
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
