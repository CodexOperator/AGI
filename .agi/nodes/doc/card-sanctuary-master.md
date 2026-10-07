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


## §0 State (20:35Z 10-07, date -u) — gen 23 seated 20:00Z, verify6 LANDED bb75aef045, box-wake RETURNED R9 (see 🔴) · trunk bb75aef045 · 0 known trunk reds (grid_sync logs 2 PRE-EXISTING ERROR lines every tick since 09-30: experiments a00-829ed05f + a00-da06914d have no mint_id) · no gate open, no gate tree on /dev/shm
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
OPEN (each arrives as a DG1 [merge-up]; FULL rail each: static + anonymize per commit, lanes + NEG, pytest subset, FULL suite on tmpfs, Sonnet mur; accept_with_residue = RETURN):
  g7.16.1.11.19 verify: RETURNED x4 in gen 22 (R1 baseline fail-open · R2 mkdir outside try · R5 untested fail-closed branches · R8 acquire_suite_lock bare raises: ~:1000 path.exists() + ~:1004/~:1008 unlink outside any try). Last tip 0b390c7236 (7 commits on 5f672d11e5): union FULL suite 7,929/0, lanes 65/0, mur runs/mur-sm22-g4-verify-r5. NEXT: DG3 one commit on 0b390c7236 (guard the 3 calls -> (None, None)); NEG = DG2 3d8d6f32d2 verify-v5-uid.t.sh (71 lanes; 0b390c7236 = 5 FAIL d7a5 d7a6 d7a7 d7g5 d7g7; d7a8 control)
  g7.16.1.11.20 box-wake DUAL ROUTE: RETURNED d926526a71 (R6 AGI_POST unset in a v5 pane -> box n dies; R7 box n stderr floods the pane/~/o; N10 setInterval not unref'd -> pi -p kids may hang; N11 count [off-matrix] lines). DG1 RULED: AGI_POST=${AGI_POST:-$AGI_SEAT} in both pieces (no host act), 2>/dev/null + stdio ignore, .unref(), grep -vc '^\[' WITH ||true in cccc.ts (DG2's trap: grep -vc exits 1 on 0 -> execSync throws -> s never resets). NEG = DG2 1d03ba36cc box-wake.t.sh (33 lanes; d926526a71 = 25 FAIL). Also run agi-kid-flow/agi-outline/agi-fresh (cwd tree) + agi-out-stale (arg 1 = gated sha). Pure-box cutover = a later leaf, belam GO
LIVE (measured, closed): grid.py 5895e8bea5 first tick clean · metrics cron first :23 run clean (171ffe7b35) · HEAL 28b5d9cd95: watcher re-exec 19:38:36Z, every sweep since = removed 0 / refused 1 (a00-eb774813 LOCKED tree, as before), 0 'git status failed' / 'rev-parse' refusals
FOLLOW-UPS banked by DG1 (not blocking): F1-F5 (metrics/grid) · N7 heal refusal line per 30 s pass · rotate.py:4960 'held by pid None' wording · inflight_mark 5th unwrapped mkdir
MURS: Workflow tool, name agi-merge-up-review, args {rounds:[...], model: sonnet, effort: high, project_root}; FOCUS = READ-ONLY + the gated union worktree + what must never run against MAIN; after EVERY mur: git symbolic-ref HEAD + reflog; persist runs/mur-sm22-<key>/result.json (home masked)
```

## §2 Landed (each landing message carries its gate numbers)
- gens 16-21: see git log --grep sanctuary-master + runs/mur-sm1[6-9]-*, mur-sm2[01]-*
- gen 22 10-07: g4.13.1 #3 grid.py 5895e8bea5 + g3.8 #3 metrics 1e930932ea (union FULL 7,915/0) · goal leaf g7.16.1.5.3.2 6bdaf7a00a · HEAL FIX for belam's [red] 00c0321840 -> 28b5d9cd95 (union FULL 7,929/0, mur accept x2; SHA to belam 19:38Z)
- gen 23 10-07: TM lane J follow-up 4fe044a830 -> 1a88f2e99e · g1.41 RE-SPLIT e538e69d87 (B F -> DG4, A passes DG3 -> DG4 at A1's landing, C E H DG5); orders to DG4 DG5 DG1 21:0xZ
- gen 23 10-07: goal:g1.41 lane J (thought-master) 3c6fd30b19 -> cad3e25dfc (corpus 566/0; mur residues refuted, routed: rows -> belam, scrub -> owner); box-wake union FULL 7,929/0 before its R9 return
- gen 23 10-07: goal:g1.41 PASS B4 residue lanes PLACED on town:local-maxxing Board f2f6c06010 (A ROOT DG3 boot hole first · B/D/F DG3 · C/E/H DG5 · G DG2 · I DG1 · J thought-master); DG1 + TM told 20:5xZ
- gen 23 10-07: g7.16.1.11.19 verify6 R8 52da4e8c47 -> bb75aef045 (union FULL 7,929/0, mur accept x2; DG1 + belam 20:3xZ)
- gen 22 10-07 RETURNED: verify6 x4 (R1 R2 R5 R8) · heal x2 (R3 R4) · box-wake x2 (box-only cutover; R6 R7)

## 🔴 Where it stops
```
sanctuary-master gen 23: LANDED verify6 bb75aef045 · TM lane J cad3e25dfc + 1a88f2e99e · box-wake .20 542d02390d (FULL 7,929/0, mur accept x2)
  GATING PIPELINE on HEAD 542d02390d: union /dev/shm/gsm23p (ids in /dev/shm/sm23-pipe.txt: M1 222e81e6e0 = + DG5 d75f721c08 find_pin_log corrective; M2 fc601a87d1 = + lane G 433b38e9f5 tests). Measured: rc 0 x2, 0 D, anonymize ok per commit; DG5 7 new tests pass, NEG 562902df0a R1 R3 R4 FAIL; lane G 4 files 447/4xf. RUNNING: FULL suite pid /dev/shm/sm23-suite-p.pid, mur wf_e7bbfc1b-dab (2 rounds). LAND one at a time: DG5 first (T2 = mt(HEAD, d75f721c08)), then lane G
  RETURNED: lane I d494ee2970 (anonymize REFUSES a box-derived size token (a KiB figure) in the lm-kv THOUGHT; refused blob in history -> ONE commit on the live trunk; '262,144 B' / '2^18 B' / '0.25 MiB' pass). NEXT after these: A1 boot-pin (DG2 lanes fe42f38c12)
  CORRECTION 21:3xZ: my earlier GPU 'history' return to DG5 was a FALSE POSITIVE (see trap)
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
| GPU-name grep with awk $NF (gen 23: the last word of the name is a COMMON word, in 793 trunk files): 3 false 'hardware' hits, one wrongful DG5 return | grep the FULL name AND the model (last two words); a hit counts only if the model string matches |
| a SIGTERM'd detached suite left 2 python3 orphans (ppid = user manager) in the REMOVED gate dir (gen 22) | after stopping a suite, re-scan /proc cwd (incl. '(deleted)') and SIGKILL what remains BEFORE worktree remove |
| backticks inside a double-quoted python -c in Bash = command substitution (gen 22: the fix text vanished from my card) | card edits go through a QUOTED heredoc file (<<'EOF'), never inline double quotes |
| write.py 'replace body N:M' refuses a range that cuts a paragraph or a fenced block; --force is NOT a CLI flag | replace the WHOLE section (heading to the next heading) |

## §5 Verification: every landing = merge-tree rc 0 + newcomers byte-identical to HEAD + 0 D + anonymize + evidence dry-run + links/schema + suite with every red attributed


## §6 BANKED
- (RESOLVED belam 11:19Z [decision], option A DONE) capsule cells = branch belam/capsule-rows 1ea2129b5 (cut from 557ab2598, posts.md only, 12/12): NEVER alone -- land it in the ONE update with the OUT.5 corrective (L = T -p HEAD -p DG3-tip -p DG2-tip -p 1ea2129b5), re-verify the 12 rows vs the LIVE posts.md at that landing (rotation cells move); root unit install = belam host act, own GO; ONE [merge-up] line to belam when it lands
- v5 MOVE 6 (19:5xZ): my verdict NO -- uid agi-sanctuary-master cannot write MAIN .git/index, ORIG_HEAD, FETCH_HEAD or the working tree (no group:agi ACL), so ff-landing dies; belam ACCEPTED: SM STAYS on this seat; belam banks a LAND BROKER for the owner (never opening MAIN to group:agi, never an update-ref landing). The next move is stream-master, not me.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ the a001a3c61 landing; tree-stripped by 165f57b0f): a scrub = history rewrite = OWNER only; sent to belam 22:0xZ · goal:g1.31.4.2.1.1 copilot hooks: PARKED (a real copilot probe = spend, the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz (the tree stays; refusal live)
- .env is 600 belam:belam, no group ACL (verified 15:3xZ): NO agi-* director can dispatch (provisioning PermissionError) -> (A) masters/Prime run directors' murs [recommended; today's practice] · (B) group:agi read ACL [owner's money: owner's call] -- sent to belam 15:3xZ
