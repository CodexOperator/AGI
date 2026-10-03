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


## §0 State (12:2xZ 10-03, date -u) — gen 20 · trunk 055fb92aa: RING.5g LANDED 7d79f605a + OUT.6 LANDED 055fb92aa (with belam 12 capsule cells) · IDLE until the next [merge-up] (DG3 ckpt / revoke / pq / flowrot via DG1, one at a time)
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
DONE (gen 20, 7d79f605a): LANDED RING.5g = DG3 dg3-ring5d 7d7603b69 + DG2 de-base-dg2-24 ee70ff541 + ab/keys = 6a5617e30 BLOBS (temp index: ab/keys add/add conflict; take `git merge-tree --write-tree` LINE 1 only as the tree id)
   GATED by gen 19 on trunk 15976de4b: union 8d756721e, merge-tree rc 0, 0 D, anonymize ok (net + every version), 0 home/host/GPU/key; piece 6,335 B (bar 6,350); 12 grow-gate files 0 FAIL BARE (ab 45 keys 35 bootstrap 17 ring 2 ring3 47 ring4 32 ring4b 17 ring5c 18 ring5d 7 ring5e 15 ring5e-dg3 13 ring5f 17); FULL suite 7914/0; mur runs/mur-sm19-dg3-ring-5g review ACCEPT + final verify ACCEPT (notes only)
   -> re-derive T2 on the LIVE head (same 3 steps), diff(8d756721e^{tree}, T2) = newcomer files only, byte-identical to HEAD; range files not dirty in MAIN; L = commit-tree T2 -p HEAD -p 7d7603b69 -p ee70ff541; ff-only; push; notify DG1 DG2 DG3
RETURNED 11:3xZ (D1 early x() leaves ~/.ssh/n + o4f fl() hides it; D2 rail admits reserved HOME names e.g. .ssh/n; runs/mur-sm20-dg3-out-5): the corrective re-gates as OUT.5 did -- was: DG3 dg3-out2 21c423f0b + DG2 agi-outline de-base-dg2-16 e11581904 (blob over the tip copy, temp index) -- DG1 10:34Z measured: out-states 28/0 (7 FAIL on 7064ed72b), outline 72/0 empty+host HOME, fresh 23/0, box-carry 64/0; agi-out 3,096 B, fenced 7,887/8,192
   -> union; static + RAIL (2) (share-shaped lines in every version; rotated_by_sig hex = public posts.md); capsule-rows.txt 12/12 vs LIVE posts.md v4 rows; tests (+ NEG on 7064ed72b); Sonnet security mur (prior runs/mur-sm19-dg3-out-4: capsule rail R1-R3) + FULL suite
   -> LAND in ONE update with belam writing the 12 engine.capsule cells (belam 08:43Z + 09:18Z [rule]: "capsule" rel. to HOME; agree mechanics with belam BEFORE the ff); landing message names: the Prime's live `systemctl show agi-post@<p> -p ActiveState,Result,NRestarts` check, the root unit install preceding/accompanying the first ring
AFTER: DG3 sends ckpt / revoke / pq / flowrot to DG1 one at a time; each reaches me only after DG1 runs it (DG1 06:03Z)
HOST ACTS = belam GO each: A10 T = 5c3df5114 (input 2 MET by shim sweep); A11 RUN by belam 05:1xZ
MURS: Workflow tool, name agi-merge-up-review, args {rounds:[...], model: sonnet, effort: high, project_root}; FOCUS names the gated UNION sha + "read/run only the union copies" (verifiers read stale tip copies twice gen 19); persist runs/mur-sm19-<key>/ (gitignored; mask home paths); FINAL verify decides, then CHECK its residue against the bytes; accept_with_residue = RETURN; after EVERY mur: git symbolic-ref HEAD + reflog
```

## §2 Landed this gen (each landing message carries its gate numbers)
- gens 16-18 (10-02/03): landed DG1 -20..-32, RING.5b 5c3df5114 + ab/keys; returned W-1.11..15, RING.3/4, OUT.2 (detail: git log + runs/mur-sm17-*, mur-sm18-*)
- 10-03 (08:0xZ, gen 19): feb29e0a1 W-1.16 6893694fd + DG2 p dc2c13663 + dry 5bb0bab81 LANDED (46/43/4/13 0 FAIL; FULL suite 7914/0 stacked w/ RING.5c; mur verify residue refuted by bytes) · RETURNED RING.5c 79adfcda1 + DG2 4198c2615 (runs/mur-sm19-dg3-ring-5c: R1 engine-grow.md:59-61 diff(h,c) reads trunk-added nodes as ADDs -> merge-up refused for a non-owner signer; R2 LIMITS posts.md jq; R3 ring4.t.sh:87; R4 ring5c 14->18 cite)
- 10-03 (08:5xZ, gen 19): RETURNED OUT.2 3345e38a9 + DG2 592f186da (union e1f5a1c79: outline 37/0 x2, states 6/0, fresh 23/0, box-carry 64/0, suite 7914/0; runs/mur-sm19-dg3-out-2: R1 engine-post.md:109-110 wrap fail/kill -> agi-flush/agi-turn commits a half ring); [decision] AGI_CAPSULE row cell banked with belam
- 10-03 (09:0xZ, gen 19): DEMOTED RING.5d d1832b29f + DG2 5b1eea56b (union ce2739768: 9 grow-gate 0 FAIL @6350, ring5d@5c 4 FAIL, suite 7914/0, bare ab bytes FAIL @6100; runs/mur-sm19-dg3-ring-5d: D1 lg ancestry -> ours-merge(R,X) then merge(M1,X) lands an owner-ringed node as dg1, rc 0 one- and two-push, 5c refuses)
- 10-03 (09:5xZ, gen 19): RETURNED RING.5e 68c170a81 + DG2 8c969fbad + 6a5617e30 accept_with_residue (union 735f797b0: 11 grow-gate files 0 FAIL bare, NEG 4+6 on 5d, suite 7914/0; runs/mur-sm19-dg3-ring-5e) · OUT.3 7e880d166 HELD for belam rule (tests green, no mur)
- 10-03 (10:4xZ, gen 19): RETURNED OUT.4 7064ed72b + DG2 25655ceb4 accept_with_residue (union 150170081: outline 60/0 x2, states 20/0, fresh 23/0, box-carry 64/0, suite 7914/0, 0 share bytes; runs/mur-sm19-dg3-out-4: capsule rail R1-R3)
- 10-03 (10:5xZ, gen 19): RETURNED RING.5f a518f5384 + DG2 02d035fa4 accept_with_residue (union d3cc0c41a: 12 grow-gate files 0 FAIL bare, NEG 5+3 on 5e, suite 7914/0; runs/mur-sm19-dg3-ring-5f: sentinel/[moral].md coupling)
- 10-03 (10:5xZ, gen 19): RING.5g 7d7603b69 + DG2 ee70ff541 ACCEPTED (union 8d756721e, suite 7914/0, mur accept/accept) -- LANDED gen 20 as 7d79f605a on 2aa85532b (T2 63cbe0230 re-derived 2 ways, identical; post-land grow-gate 0 not-ok, links 0 broken); OUT.5 21c423f0b received · 10-03 (11:3xZ, gen 20): RETURNED OUT.5 21c423f0b + DG2 e11581904 accept_with_residue (union 2cce5418f on 557ab2598: out-states 28/0 sh, outline 72/0, fresh 23/0, box-carry 64/0, NEG 7+9 on 7064ed72b, capsule rows 12/12 byte-exact, suite 7,224/0 at 91% stopped on return; runs/mur-sm20-dg3-out-5: D1 + D2) · [decision] capsule cells option A: belam 1ea2129b5 (11:19Z) · 10-03 (12:2xZ, gen 20): LANDED OUT.6 055fb92aa = DG3 2566b6f94 (node-only OUT.6b re-gated) + DG2 a506002b5 + belam 1ea2129b5 (out-states 43/0 on the landed trunk) · (12:1xZ) RETURNED OUT.6 741ab1c99 + DG2 a506002b5 NODE-ONLY (code green: suite 7,914/0, out-states 43/0, outline 85/0, NEG 13+11; runs/mur-sm20-dg3-out-6: node figures + BOUNDS n4/python3)

## 🔴 Where it stops
```
sanctuary-master gen 20 at 12:2xZ: trunk clean at 055fb92aa (OUT.6 + belam cells LANDED, pushed, notified); belam holds the host acts (unit install after posts merge trunk = n4, python3-cryptography = n5, systemctl show check = n1); IDLE until the next [merge-up]
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
| `git merge-tree --write-tree A B` on CONFLICT prints the tree id + the conflict list (gen 19: read-tree of the whole output = an EMPTY tree, 13,254 D in the diff) | take `| head -1` as the tree id, then temp index; ALWAYS check D = 0 before anything else |
| a .t.sh run with bash (11:1xZ: agi-out-states 4 false reds: an ok message's $(nc) resets $? before chk reads rc) | run every .t.sh with sh (dash = its shebang), never bash |
| ListAgents DG3 ref went stale again ([f0008b] -> [238bd0], 09:0xZ) | send by bare name; on "N agents named" pick the one active seconds ago |

## §5 Verification: every landing = merge-tree rc 0 + newcomers byte-identical to HEAD + 0 D + anonymize + evidence dry-run + links/schema + suite with every red attributed


## §6 BANKED
- (RESOLVED belam 11:19Z [decision], option A DONE) capsule cells = branch belam/capsule-rows 1ea2129b5 (cut from 557ab2598, posts.md only, 12/12): NEVER alone -- land it in the ONE update with the OUT.5 corrective (L = T -p HEAD -p DG3-tip -p DG2-tip -p 1ea2129b5), re-verify the 12 rows vs the LIVE posts.md at that landing (rotation cells move); root unit install = belam host act, own GO; ONE [merge-up] line to belam when it lands
- (resolved 05:1xZ) rotation block: belam landed my key row c6064d5b1 as af21b1b55 (option A, trap 70)
- v5 MOVE 6 (19:5xZ): my verdict NO -- uid agi-sanctuary-master cannot write MAIN .git/index, ORIG_HEAD, FETCH_HEAD or the working tree (no group:agi ACL), so ff-landing dies; belam ACCEPTED: SM STAYS on this seat; belam banks a LAND BROKER for the owner (never opening MAIN to group:agi, never an update-ref landing). The next move is stream-master, not me.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ the a001a3c61 landing; tree-stripped by 165f57b0f): a scrub = history rewrite = OWNER only; sent to belam 22:0xZ · goal:g1.31.4.2.1.1 copilot hooks: PARKED (a real copilot probe = spend, the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz (the tree stays; refusal live)
- .env is 600 belam:belam, no group ACL (verified 15:3xZ): NO agi-* director can dispatch (provisioning PermissionError) -> (A) masters/Prime run directors' murs [recommended; today's practice] · (B) group:agi read ACL [owner's money: owner's call] -- sent to belam 15:3xZ
- (resolved 07:1xZ) Z4 phase-A signing: belam option (a) via branch belam/z4a-anchor; landed c2decf431
