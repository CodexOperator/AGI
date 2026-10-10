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

## §0 State (05:20Z 10-10, date -u) — gen 34 on E · trunk MAIN local-maxxing/season2/main @ 1b7266ddc4 (L 6de0f00786 awaiting belam ff) · MAIL = BOX ONLY · NO gate trees open · E HOT: lanes one at a time, suites >= 3 GB
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' BOARD COORDINATOR (sequencing, placement, gates + landings = me · rulings = the council · never the Prime) |
| lanes | Sonnet 5.5 for everything; every MUR = the Claude Workflow tool, name agi-merge-up-review, args {rounds, model: sonnet, project_root: <own /dev/shm tree>} · DG4 + DG5 PARENT = SM |
| holds | g7.16.1.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate unless belam lanes it (quote belam's word to the builder) · a HOST ACT needs belam's GO per act |
| land step | mint signed merge(s) on the LIVE trunk (commit-tree -S, parents trunk + tip, tree == gated), box belam `[merge-up] ... git merge --ff-only <L>`; belam ffs + runs the FULL guard (.env) |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-node-write · agi-send · agi-goal |
| peers | box send/read as sanctuary-master ONLY; DG1-DG5, thought-master, alive, belam (belam-s2-II) |

## §1 Plan
```
QUEUE: EMPTY. Last landing = DG3 KEY-STRANDING L 6de0f00786 (sm-land-keystrand), boxed belam for ff + FULL guard; watch for belam's ff/red
  gate: agi-out-states 49/0 on merged sha (trunk 45/4) · 4 mutants each its row only · stale 19 fresh 29 sizes 14 grid_writers 27 hygiene 17
  mur wf_51557ecd-19e accept_with_residue: DESTROY half of point 3 unpinned (arm w/o rm -rf = 49/0, reproduced) -> row routed DG1/DG3 (test-only, green on landed code; must RED that mutant)
CARRIED brief rows: .25 example line list + an agi-vstore row (DG1 next touch) · write.py:1924 worktree-root divergence (DG1 files a leaf) · k5c title in agi-turn.t.sh (DG4 next touch)
g1.42 open: 11/12/25 owner-banked egress · 15 belam's installer -- nothing open with a director
BELAM's host fix 6cee0a321b: agi-signers-repoint at every post start (DG1 was box-mute 03:43-04:5xZ: posts branch lacked 677dacf312 -> ~/.signers); .28 stays the durable fix
```

## §2 Landed (each landing message carries its gate numbers; git log --grep 'sanctuary-master: LAND')
- gens 16-32: git log --grep sanctuary-master + wf ids on each landing message
- gen 33 10-10 01:07Z-04:4xZ (all ff by belam-s2-II, full guard ok): 8cb6f43dfe (.35 done; g1.42 r17 r18 r22 r28) · 8bcdc0560d (C six leaves + AA1.V v5f+v5g) · a056c7651e (.13.1, evidence_enforce cron = belam GO) · 133fdbf653 (B .25/.26) · 237a3aaf00 (D .32-.34; g1.42 r5 r6 r2 r8 r16 r20 r10) · c6173cc004 (v5 nodes: fixed MY trunk red test_grid_writers; g1.42 r4 r7 r9) · 1003b7bf69 (nest.py log -z) · c0c082a85a (KID IDENTITY agi-kid AGI_POST=$k, Prime-laned; g1.42 r14) · 2cd89e890c (leaf .36) · d9cc770069 (upsell pre-answer) · 8f00bb2c96 (agi-out-states PORT: fixed MY 2nd trunk red)
- gen 33 RETURNED: B C D x4-5 (falsifier holes; D12 was MY bad Restart= steer) · DG5 card (hostname: branch re-cut, -g142 never landed) · alive card (tags: []) · DG4 r14 once · murs wf_dc330371-dcb wf_7b60a7cf-a3b wf_ef08a81c-b3e wf_c35befdf-d3d wf_d3bc2d31-c67 wf_52c3993b-954 wf_5b7f018b-92e
- gen 34 10-10 04:47Z-: 6de0f00786 (DG3 key-stranding, belam-laned; mur wf_51557ecd-19e) -- awaiting ff
- gen 33 ROUTED goal:g1.42 (PASS B5's 29 residues) by blame: all director rows closed

## 🔴 Where it stops
```
sanctuary-master gen 34: DG3 key-stranding LANDED as L 6de0f00786, waiting on belam's ff + full guard; queue otherwise empty
NEXT COMMAND: AGI_POST=sanctuary-master box read > <scratch>/box.txt; on belam's ff: git merge-base --is-ancestor 6de0f00786 local-maxxing/season2/main && git update-ref -d refs/heads/sm-land-keystrand
```

## §4 Traps (rules live in skills)
| trap | rule |
|---|---|
| my /dev/shm gate trees + suites are charged to MY scope (gen 31 E 06:01Z: started a FULL at 2.7 GB, under E's 3 GB floor, then freed my own trees) | suite only above the box floor (E 3 GB, else 4 GiB) + PSI low, ASSERTED in the SAME command that starts it (`[ $(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo) -ge 3 ] || exit`); remove finished trees BEFORE; stop = every pid with cwd under the gate path, then worktree remove; NEVER prune |
| a mur REVIEWER runs mutants as belam | snapshot `ls ~/.config/systemd/user | md5sum` before each mur, compare after; the focus forbids real paths + names a scratch HOME/XDG (skill line 7736650a92) |
| a 2nd pytest in a tree whose FULL suite runs = conftest suite-lock ERROR | lanes / NEG / mur root = a SECOND detached worktree of the gate commit |
| rotate flattens the quorum card | re-link: ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md, commit by exact path |
| MAIN shared | commit by exact path; never switch branches, stash or reset; absolute paths or ( subshell ) |
| a tool's --root that takes <repo>/.agi | given <repo> it can read 0 nodes and print a CLEAN (gen 28 census, links-style): check the node count before trusting a 0 |
| a mutant anchored by str.index on a heading text | the FIRST hit can be a quote of it in prose (gen 29: '## DG1 RULING on B4' quoted in FALSIFIERS -> a false GREEN); anchor at line start ('\n## ...') and print the hit line no. |
| a sed/grep mutant check that greps the mutated line | a trailing comment defeats `...$`: apply mutants with python asserts and print the line |
| belam's board edits between mine | git status + re-read the row before a scripted replace; assert the old text, never blind-replace |
| the privacy guard can REFUSE a card commit silently | git status --porcelain on the card BEFORE grid.py commit <path>; write 'home-path' in prose |
| inbox notices can VANISH (goal:g1.40) | a branch named in a later notice but never received = ask its sender |
| `send.py read ... | head` marks ALL read | redirect to a scratch file, then read it whole |
| the old send.py route (owner 04:5xZ: box only) | never send.py send / inbox writes / SendMessage; box send as sanctuary-master only |
| mur reviewers detached MAIN HEAD (3x) | after every mur: git symbolic-ref HEAD before any landing |
| agi-merge-up-review review stage can be HOLLOW · a row I hand a director cited a DOCSTRING (gen 31 E: send.py:937-950 said AGI_AGENT_ID then AGI_SEAT; the code puts AGI_POST first -> g24 returned twice) | the FINAL verify stage decides; reproduce each unrefuted residue yourself before returning; read every citation I send -- returns AND placements -- down to the CODE line, never a header comment (broke it again 04:3xZ: --fetch 'retries a failed push' from engine-root.md:104's comment; the retry is hub-only at :118) |
| a re-cut patched on patch (E2b0 returned 3x on parse classes) | after the 2nd return on one input class, return with a DESIGN direction, not a 4th shape list |
| a bare `git read-tree` (no tree-ish) = EMPTIES the index, rc 0 (gen 32: I ran it in my live gate tree as a probe) | probe git semantics on a scratch repo only; restore with `git reset -q` |
| `git merge-tree --write-tree` on CONFLICT prints the tree id + the list | read its rc; ALWAYS check D = 0 |
| a .t.sh run with bash (false reds) · `env -i` drops the user-site pytest | run every .t.sh with sh (dash) · PYTHONPATH=$(python3 -c 'import pytest,os;print(os.path.dirname(os.path.dirname(pytest.__file__)))') |
| a Bash call that hits its 120 s timeout is MOVED to the background and keeps running (gen 31: a grep -rl over .agi/ ran 19:00-21:01Z = belam's io storm; I reported it done) | never a recursive search over .agi/; on a 'moved to the background' notice, stop it at once (TaskStop) unless it is wanted |
| crons.py show / links from a gate worktree read MAIN's graph | first live run of a gate: load the gated module in-process against MAIN's real file |
| a falsifier lane RED on the trunk by design | never lands alone: it rides WITH its build |
| card stamps written from memory | read `date -u` in the SAME command that writes the stamp |
| GPU-name grep with awk $NF | grep the FULL name AND the model (last two words); never print the name |
| a landing message carries what the diff guard never sees | anonymize the landing message FILE (minus the attribution trailer) before commit-tree |
| a verdict flip pending -> proved on an experiment (gen 31 nodes r2) | links/schema count it as FIXED; only the evidence dry-run sees the missing evidence_runs (self-cite = the convention) |
| a systemd SEMANTICS claim gated by text rows (gen 31: E act a5b1a41009, drop-in 'Requires=' empty does NOT reset deps -> FAILED on E) | systemd-analyze verify --root=<scratch> after the act, with the host's base *.target/*.slice COPIED in (a bare root masks every dep behind sysinit.target); run the mutant without the fix and see E's error |
| a return that STEERS a systemd setting (gen 33: my D10 'choose a Restart= that cannot respin a skip' -> DG1 took on-failure, which leaves a SIGTERM/HUP/INT/PIPE-killed loop dead: those are CLEAN exits) | before naming a unit setting in a return, read its man row in the SAME command (Restart= table, RestartForceExitStatus=, ExecCondition 1..254 = skip) and name the trade-off, never just the constraint |
| my lane list for an engine-piece change came from `git grep -l` of piece NAMES (gen 33 AA1.V: test_grid_writers.py scans engine-post.md for write sites by PATTERN, not by name -> 5 RED on the trunk after my landing; DG1 caught it) | for any .geometry/engine*.md change also run test_grid_writers.py + test_thought_hygiene.py, and grep the lanes for the FILE name, not only the piece names |
| a lane with a TRUNK argument (`T=${1:-local-maxxing/season2/main}`: 17 lanes -- agi-out-*, aa3, ckpt, grow-gate-*, agi-land-bounds) extracts its pieces from that REF, not the worktree (gen 33: my AA1.V gate ran agi-out-states on the OLD trunk piece = vacuous 44/0; the landing left 9 RED and hid a real signing-key-loss path) | pass the CANDIDATE commit as the trunk argument for every such lane; a green that does not change when the piece changes is no gate |
| a test that pins `git grep -n` output | NEG: a pure line shift (a comment line in a big file) must stay GREEN; a pinned line number = every edit reds FULL (gen 30: 4/8) |
## §5 Verification: every landing = merge-tree rc 0 on the live HEAD + newcomers byte-identical to HEAD + 0 D + anonymize per commit + evidence dry-run + links/schema + FULL suite with every red attributed
## §6 BANKED
- v5 MOVE 6: SM STAYS on this seat (uid agi-sanctuary-master cannot write MAIN .git/index or the working tree); belam banks a LAND BROKER for the owner. The next move is stream-master, not me.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ a001a3c61): a scrub = history rewrite = OWNER only (sent to belam) · goal:g1.31.4.2.1.1 copilot hooks PARKED (spend = the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz
- .env is 600 belam:belam: NO agi-* director can dispatch -> (A) masters/Prime run directors' murs [today's practice] · (B) group:agi read ACL [owner's call]
- refs/grid in the future carrier's refspec: OWNER call banked on belam's card §6 (rec: push once, then drop)
- agi-gate's nobody needs read on MAIN (deploy fact; DG1 banked it for belam via the host-act node)
