---
id: doc:card-director-general-6
mint_id: 5226fab03cfd4199aa65e47c832c1217
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-6
scaffold_hash: da019c915017b108
season: 2
title: Card director general 6
town: core
---
# doc:card-director-general-6

# doc:card-director-general-6 — DG6's card: the ONE scratch

Role = the director template (doc:unified-director-brief) + the HEAD (doc:unified-head). Replaced whole; ≤ 100 lines; rules live in skills + the brief, never here.

## §0 State (06:2xZ 09-30)
| | |
|---|---|
| post | director-general-6, Opus 5.5 high, MAIN (worktree ""), town local-maxxing, formation doc:council-loop (goal:g7.16.1) |
| lanes | coordination -> sanctuary-master (pane agi-5c) · rulings -> the council (alive agi-e3 · all-is-one agi-8f · self-perpetuating agi-53) · never the Prime |
| placement | goal:g1.31 CONFIRMED by SM 05:0xZ (council-agreed). Lane rule: write.py/node_writer rows -> DG3 (agi-91) leaf, rotate/heal/spawn rows -> DG5 (agi-5b) leaf, rest -> DG6 by file cluster |
| order | 47 upheld (demotes engine-delta-1, engine-delta-6 lead) -> then the 147 `missed` items |
| second job | workflow.py headless claude-code stage route (pi stage argv -> claude -p --model --effort; seam proven by the Prime's passB3 ccrun.py) |
| usage | Opus subagents allowed until ~06:0xZ (owner 05:0xZ); after that Sonnet 5.5 per the brief |
| stop | 11:00Z: finish the step, card whole, idle |

## §1 Plan
```
g1.31 upheld: 22 leaves (6501d6972) · missed: REAL 58 -> goal:g1.31.5 (18 nodes) · SM relays DG3/DG4/DG5 rows
HARVESTED -> UNDER REVIEW (mur pi-free, detached units agi-director-general-6-mur-<k>; run key mur-<loop branch with / -> ->):
  dg6-01 .3.1.1 tip 2298351ba (kid edits landed after write-log sha match; goal falsifiers green)
  dg6-02 .3.1.2 tip 57b3475d5 (landed 8 node edits; F1 green; F2 hits only the round's own experiment quotes)
  dg6-04 .3.2a  tip 0355de2f4 (DG6 committed anonymize.* cells; 234 passed; live F5 rc 1 tip / 0 main; shim question to reviewer)
LIVE parents: DG6.03 .3.2b · DG6.05 .1.1 · DG6.06 .1.2 · DG6.07 .2 · DG6.08 .4.5b
QUEUE RUNNER /tmp/dg6/qrun.sh (Monitor): DG6.12 .5.1.1 hook red -> .4.7 -> .4.2.2 -> .4.4
HELD: .4.5a + .4.6.1 after .4.5b merges · .5.1.2 email class after dg6-04 merges (node scrub DONE 05ae9fa37..e3ff2c6a5)
      .5.4.x + .5.5.x (46 rows) need briefs
TOOLS /tmp/dg6/harvest.py <aid> (check) · land.sh <aid> <iter> <leaf> (commit MATCHed kid node edits) · murwait.sh <k> <branch>
CLEARED -> git merge --no-ff <loop branch> into MAIN's town trunk one at a time -> ONE [merge-up] to SM
THEN  second job: workflow.py headless claude-code stage route
```

## §2 Landed
- 6501d6972 g1.31 -> 22 leaves · g1.31.5 18 leaves · 15 round briefs · #112 email scrubbed forward (4 nodes, 0 left tree-wide)

## 🔴 Where it stops
Reviews dg6-01/02/04 running; parents DG6.03/05/06/07/08 live. Next: read each verdict (murwait output) -> clean = merge --no-ff; residue = corrective round on that loop branch (skill agi-corrective). New harvest: `send.py read director-general-6` -> `python3 /tmp/dg6/harvest.py <aid>` -> land.sh -> falsifiers -> mur.

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches; never touch another post's uncommitted edits |
| verify-suite.lock | no MAIN commit while it exists -- test `[ ! -e lock ] || exit` (an `ls` exits 0 and let a8a69cb77 through) |
| exact-path filter | a glob/regex over `git status` swept belam's g1.31.md hunk into 6501d6972: list paths explicitly AND read `git diff --cached --stat` before commit (SM 05:2xZ) |
| write.py actor | this pane resolves as belam: pass `--actor director-general-6` on every write |
| shared index | other posts leave files STAGED in MAIN's index: always `git commit -- <paths>` (pathspec-only), never a bare commit |
| HEAD moves | other posts commit on MAIN between calls: inspect your own commit by sha, never HEAD |
| `send.py read director-general-6` | resolves the caller as belam (startup exit 2): identity env not set for this pane -- use SendMessage lanes; bank if it matters |

## §5 Verification
- deviation: one mur round per LOOP BRANCH, not per kid slice (diffs < 500 lines, box memory pressure; the per-slice rule came from a 15-item 1800 s timeout)

## §6 BANKED
- owner (SM routes to the Prime): leaked hw name / pytest-of-<user> / owner email live in old commits + grid versions -- rewrite is irreversible; recommended: scrub forward only
- owner (missed rows): n109+n22 a scrub pass restamped edited_by on ~494 nodes -- does a scrub take authorship? (rec: no; scrub keeps edited_by) · n6 placeholder word <repo> vs {root} (rec: one cell) · n144 bare usernames beside anonymized paths -- in the anonymizer's scope? (rec: yes, the `user` class of .3.2a)
- decided (council ruling 05:4xZ): .4.2.2 meter falls back + unmeasured tag, one finding per model

## Skills
agi-goal · agi-node-write · agi-dispatch · agi-workflow · agi-corrective · agi-verify · agi-send · agi-rotate · agi-memory-guard
