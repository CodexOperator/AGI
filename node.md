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

## §0 State (05:5xZ 09-30)
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
g1.31 upheld: 22 leaves (6501d6972) · 13 briefs · missed: 147 triaged -> REAL 59 (3 red) -> goal:g1.31.5 (drafting, 2 Opus)
LIVE (pi-free, 0 USD):  DG6.01 a00-f7c21d0b .3.1.1 · DG6.02 a00-ab940124 .3.1.2 · DG6.03 a00-dbbb2896 .3.2b
                        DG6.04 a00-fb71a5f6 .3.2a · DG6.05 a00-75a7f51b .1.1
QUEUE RUNNER /tmp/dg6/qrun.sh (Monitor; log /tmp/dg6/qrun.log): pops /tmp/dg6/queue.txt head when load1<16 AND io avg60<50 AND my parents<10, 90 s apart
  queue: .1.2 · .2 · .4.5b · .4.7 · .4.2.2 (council ruling applied 5988edbda) · .4.4
  AFTER .4.5b lands: .4.5a pb3-box-home-cells-derived-per-box · .4.6.1 pb3-drift-test-s26-caller-injective-json-field
NEXT  mint g1.31.5 (reds 112 -> 19 go to the HEAD of queue.txt, SM 05:4xZ) · send SM the DG3/DG4/DG5 leaf ids
      lanes (SM): 83 -> DG4 (agi-c8 [6d9f0c]) · 84 + 60 -> DG3 · 107 -> DG5 · rest DG6/NODE
HARVEST per round in place: merge-base diff · touched tests + neighbourhood (--basetemp /tmp) · mur --harness pi-free per kid slice -> merge cleared -> ONE [merge-up] to SM
THEN  second job: workflow.py headless claude-code stage route
```

## §2 Landed
- 6501d6972 goal:g1.31 -> 22 leaves · 13 round briefs (324df95ec, 7eb1dacb6, 2619b8972, a2c9f4c7b, 0723de5cd, 5988edbda + write.py auto-commits)

## 🔴 Where it stops
Queue runner live; drafters for g1.31.5 pending (/tmp/dg6/g1.31.5*.md). Next: mint g1.31.5 tree (same loop as g1.31: strip H1, create, set confidence/origin/seeds/tags, --actor director-general-6), commit pathspec-only, brief the reds, `sed -i 1i` them into /tmp/dg6/queue.txt. If the runner died: `bash /tmp/dg6/qrun.sh` via Monitor.

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
(none yet)

## §6 BANKED
- owner (SM routes to the Prime): leaked hw name / pytest-of-<user> / owner email live in old commits + grid versions -- rewrite is irreversible; recommended: scrub forward only
- owner (missed rows): n109+n22 a scrub pass restamped edited_by on ~494 nodes -- does a scrub take authorship? (rec: no; scrub keeps edited_by) · n6 placeholder word <repo> vs {root} (rec: one cell) · n144 bare usernames beside anonymized paths -- in the anonymizer's scope? (rec: yes, the `user` class of .3.2a)
- decided (council ruling 05:4xZ): .4.2.2 meter falls back + unmeasured tag, one finding per model

## Skills
agi-goal · agi-node-write · agi-dispatch · agi-workflow · agi-corrective · agi-verify · agi-send · agi-rotate · agi-memory-guard
