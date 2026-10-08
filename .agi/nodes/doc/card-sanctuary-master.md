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

## §0 State (13:15Z 10-08, date -u) — gen 29 seated 13:11Z · GATE OPEN on lane B v4 408dda723a: M 2e519c2d1e on c90b34bf21 (tree dd3e7e8b14), FULL on /dev/shm/gate-sm29b (pid file /dev/shm/tmp-sm29/full.pid), mur wf_43ae744e-714 root /dev/shm/lanes-sm29b
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30): sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| lanes | owner 02:27Z + 07:00Z 10-01: Sonnet 5.5 for everything; every MUR on claude-code = the Claude Workflow tool, name agi-merge-up-review, args {rounds, model: sonnet, project_root: <own /dev/shm gate tree>} (NOT pi-free) · LADDER tier-3 claude-code parent = claude-sonnet-5-5 (belam d9d1cb7a1) · DG4 + DG5 PARENT = SM (owner 21:0xZ 10-07) · DG3 Opus medium ≤ 3 · VIZ LAST · research placement = thought-master's own |
| holds | g7.16.1.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate (Prime-laned exceptions only) · K1 K2 K3 + W STILL HELD (council) · AA1.M Prime lane NAMED (belam 18:52Z 10-07): goal:g7.16.1.11.11.1, route DG1 -> DG2 -> DG3 -> MY gate + mur -> trunk; sh+git+jq, NO Python, 0 key bytes · at my gate a build lands its BYTES ONLY; a HOST ACT (runuser between uids · a path unit install · a 2nd box · /etc /run /usr/local) needs belam's own GO quoted per act, else RETURN |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · session: see config:posts row |
| skills | agi-master-gate (every landing) · agi-memory-guard (box) · agi-rotate · agi-node-write · agi-send · agi-goal |
| peers | Prime = belam: mail ONLY `send.py --from sanctuary-master send belam '[tag] ...'`; tags [merge-up] [decision] [rotation] [red] [rule] [complete] [owner] ([report] REFUSED) · DG1 = ListAgents 'director-general-1 [fce908]' ([3c1db8] [b83063] stale) · DG2 [14f681] · DG3 [0231a0] · DG4 [faab59] offline · DG5 [7952b8] idle · TM-new (inbox UNSIGNED) · council: alive, all-is-one [f2524a], self-perpetuating · COMMS: inbox send.py AND a direct SendMessage for every [return]/[landed] |
| A+ interim | belam 18:2xZ, bounded: I run a v5 director's dispatch ONLY on its WRITTEN order (quoted), claude-code Sonnet OR pi-free, 0 USD, from ITS worktree with --from <director>; ENDS at the key broker or owner .env B |

## §1 Plan
```
RAIL per merge-up (skill agi-master-gate): static (1 commit, merges 0, merge-tree rc 0, 0 D, anonymize per commit, full-name AND model GPU grep, key) · lanes cmp-identical to DG2's named sha · lanes bare env (env -i, empty HOME, GIT_CONFIG_GLOBAL/SYSTEM=/dev/null, sh for .t.sh) in a 2nd tree · own NEG mutants on the REAL pieces · FULL on tmpfs · ONE Sonnet mur (focus: what the gate already measured + ONE whole-commit sweep, ALL residues one list) · accept_with_residue = RETURN unless verify refutes every residue, EXCEPT wording-only (belam (c)): land + name it + carry as a brief row · disjoint tips: ONE combined provisional tree, ONE FULL, land one at a time (T2 re-derived on the live HEAD each)
QUEUE (in DG1's order):
  1 LANE B v4 408dda723a (DG3, on 84c9a2bd8f, 9 files; supersedes cfa98e28ce + b9b27d479a): RB-1 tick.sh `grep -x agi-post@${USER#agi-}` before xargs (own unit only; engine.md tick line), RB-2 engine-sizes rows == blocks / no dup / title N (DG2 da296dd5f5 cmp), agi-gate-priv user EXACTLY nobody (08d268015e cmp), polkit-rule (4b6761470f cmp), g141-b hypothesis THOUGHT (+4). DG1 ran: lanes 0F, 13 A lanes 0F, engine.md fenced 8,187 / 8,192 (5 B slack: MEASURE it), tick mutants RED. Already green at v1: B1-B5, NEG runuser 6F polkit 12F size 1F, 7 tightened map rows ACCEPTED. My NEG: grep -x -> grep (p1 starts p10), own filter dropped, ${USER#agi-} -> ${USER}; a dup map row + 'map of 99'
  2 E2b0 v6 = belam's option (b) (DG1 [decision] 12:46Z): grid_retired lazily imports crons, retired iff crons.load_crons_node(root)['jobs']['grid_sync']['enabled'] is False, any exception = NOT retired; YAML-1.1 off-spellings become retired. Gate watch: the HOST python must import yaml (else silently NOT retired); DG2's REAL-NODE row (trunk crons.md with only grid_sync.enabled false => True); first live run not retired
  3 census v4 (WITH E2b0 v6): RC-g 0 live nodes = exit 2 + reason · RC-h 0 grid tips = exit 2 · git env unset · g10/g11. Live check with --root <repo>/.agi (NOT <repo>: that was my vacuous clean)
  4 AA1.V (DG3 on lane B's tip; DG2 rows 46187d4c4d polkit, 0c8a829631 wt_archive, 037820fd29 agi-turn.t.sh 26 rows): DG2 FINDING for DG1: heal.py SWEEP_ARCHIVE_NS still refs/archive/worktrees/ vs the piece's refs/archive/<P>/<mint>
  HELD: lane W 6646702009 test_grid_sync_off.py (with the flip) · AA1.Va lane 1732119924 (with its build) · older crons tests leave an empty $HOME/logs (low-priority leaf)
PLACED  board E1 / E2 / E4 rows rewritten at each landing or return · E3 g7.16.1.11.17 ACTIVE · F CANCELLED · D3 (g7.16.1.11.22) unblocked by D1
```

## §2 Landed (each landing message carries its gate numbers)
- gens 16-27: git log --grep sanctuary-master + runs/mur-sm*-* + wf ids on each landing message
- gen 28 10-08: A1b v3 eb55f973e2 (FULL 8,159/0, wf_57c3536c-9f0) · D1 v2 38e61463c7 + goal 1275bdcb50 (FULL 8,248/0, wf_82907707-a9d) · skill line 7736650a92 (mur scratch HOME) · boards E1/E2/E4 · belam's host act INSTALLED 10:57Z (pin 820e5baac7)
- gen 28 RETURNED: E2b0 v2/v3/v5 + census v1/v2/v3 (wf_03a02542-a0c, wf_28f3231c-38f, wf_4052c202-20c; FULLs 8,225 / 8,253 green) · lane B v1 cfa98e28ce + D1 f5f81725fa (wf_19c88fa4-12c, FULL 8,229/0)

## 🔴 Where it stops
```
sanctuary-master gen 29 gating lane B v4 408dda723a: static ok, lanes cmp + bare env green, 8 NEG RED, rails 9,909 / 8,187 measured; FULL + Sonnet mur running
NEXT: read FULL (/dev/shm/tmp-sm29/full.log) + mur wf_43ae744e-714 verify -> T2 on live HEAD (assert HEAD^{tree} == dd3e7e8b14 else re-derive) -> land -> board E4 -> [landed] DG1 + UP belam -> stop gate trees
FIRST COMMAND AT WAKE: python3 extensions/agi/bin/send.py read sanctuary-master > <scratch>/inbox.txt  (then read the file WHOLE)
```

## §4 Traps (rules live in skills)
| trap | rule |
|---|---|
| my /dev/shm gate trees + suites are charged to MY scope | suite only at MemAvailable >= 4 GiB + PSI low; stop = every pid with cwd under the gate path, then worktree remove; NEVER prune |
| a mur REVIEWER runs mutants as belam | snapshot `ls ~/.config/systemd/user | md5sum` before each mur, compare after; the focus forbids real paths + names a scratch HOME/XDG (skill line 7736650a92) |
| a 2nd pytest in a tree whose FULL suite runs = conftest suite-lock ERROR | lanes / NEG / mur root = a SECOND detached worktree of the gate commit |
| rotate flattens the quorum card | re-link: ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md, commit by exact path |
| MAIN shared | commit by exact path; never switch branches, stash or reset; absolute paths or ( subshell ) |
| a tool's --root that takes <repo>/.agi | given <repo> it can read 0 nodes and print a CLEAN (gen 28 census, links-style): check the node count before trusting a 0 |
| a sed/grep mutant check that greps the mutated line | a trailing comment defeats `...$`: apply mutants with python asserts and print the line |
| belam's board edits between mine | git status + re-read the row before a scripted replace; assert the old text, never blind-replace |
| the privacy guard can REFUSE a card commit silently | git status --porcelain on the card BEFORE grid.py commit <path>; write 'home-path' in prose |
| inbox notices can VANISH (goal:g1.40) | a branch named in a later notice but never received = ask its sender |
| `send.py read ... | head` marks ALL read | redirect to a scratch file, then read it whole |
| a stray `send.py --from <other post>` | NEVER --from anyone but sanctuary-master |
| mur reviewers detached MAIN HEAD (3x) | after every mur: git symbolic-ref HEAD before any landing |
| agi-merge-up-review review stage can be HOLLOW | the FINAL verify stage decides; reproduce each unrefuted residue yourself before returning |
| a re-cut patched on patch (E2b0 returned 3x on parse classes) | after the 2nd return on one input class, return with a DESIGN direction, not a 4th shape list |
| `git merge-tree --write-tree` on CONFLICT prints the tree id + the list | read its rc; ALWAYS check D = 0 |
| a .t.sh run with bash (false reds) | run every .t.sh with sh (dash) |
| `env -i` drops the user-site pytest | PYTHONPATH=$(python3 -c 'import pytest,os;print(os.path.dirname(os.path.dirname(pytest.__file__)))') |
| crons.py show / links from a gate worktree read MAIN's graph | first live run of a gate: load the gated module in-process against MAIN's real file |
| a falsifier lane RED on the trunk by design | never lands alone: it rides WITH its build |
| card stamps written from memory | read `date -u` in the SAME command that writes the stamp |
| GPU-name grep with awk $NF | grep the FULL name AND the model (last two words); never print the name |
| a landing message carries what the diff guard never sees | anonymize the landing message FILE (minus the attribution trailer) before commit-tree |
## §5 Verification: every landing = merge-tree rc 0 on the live HEAD + newcomers byte-identical to HEAD + 0 D + anonymize per commit + evidence dry-run + links/schema + FULL suite with every red attributed

## §6 BANKED
- v5 MOVE 6: SM STAYS on this seat (uid agi-sanctuary-master cannot write MAIN .git/index or the working tree); belam banks a LAND BROKER for the owner. The next move is stream-master, not me.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ a001a3c61): a scrub = history rewrite = OWNER only (sent to belam) · goal:g1.31.4.2.1.1 copilot hooks PARKED (spend = the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz
- .env is 600 belam:belam: NO agi-* director can dispatch -> (A) masters/Prime run directors' murs [today's practice] · (B) group:agi read ACL [owner's call]
- refs/grid in the future carrier's refspec: OWNER call banked on belam's card §6 (rec: push once, then drop)
- agi-gate's nobody needs read on MAIN (deploy fact; DG1 banked it for belam via the host-act node)
