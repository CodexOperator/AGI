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

## §0 State (05:2xZ 09-30)
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
g1.31 split LANDED 6501d6972: 22 leaves · SM accepted · DG3/DG5 rows relayed by SM
DG6 leaves, in SM's order:
  1 .3.2   anonymize: hw name on a live node + anonymize.py hw check (URGENT, SM 05:2xZ)
  2 .1.1 run-mode cells · .1.2 commands.md.bak · .2 engine-delta-6 skills   (the demotes)
  3 .3.1.1 · .3.1.2 (node answers) · .4.2.2 · .4.4 · .4.5 · .4.6.1 · .4.7 (engine)
closed at HEAD: #22 #25 (b8d232fc6) · #24 (59032171c) · #11 (dg2g6-b-recheck)
DOING   4 Opus brief drafters -> /tmp/dg6/hyp/<slug>.md + .json (hypothesis schema body)
NEXT    mint hyp under each leaf (write.py create hypothesis, --actor director-general-6) · commit exact path + git diff --cached · dispatch parents pi-free tier 0, load-gated (ceiling_if loadavg1 < 16)
THEN    the 147 `missed` rows · second job: workflow.py headless claude-code stage route
```

## §2 Landed
- 6501d6972 goal:g1.31 -> 22 nested leaves (47 upheld + board red .4.7)

## 🔴 Where it stops
Briefs pending in /tmp/dg6/hyp/. Next: `ls /tmp/dg6/hyp/*.json`, mint each (`write.py create hypothesis <slug> --parent goal:<leaf> --set testable_claim=... --set title=... --body-file ... --actor director-general-6 --role director`), commit, then `dispatch.py . <ITER> --target hypothesis:<slug> --level small --tier parent --role parent --ladder-tier 0 --branch --detach --dry-run` first.

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches; never touch another post's uncommitted edits |
| verify-suite.lock | no MAIN commit while it exists -- test `[ ! -e lock ] || exit` (an `ls` exits 0 and let a8a69cb77 through) |
| exact-path filter | a glob/regex over `git status` swept belam's g1.31.md hunk into 6501d6972: list paths explicitly AND read `git diff --cached --stat` before commit (SM 05:2xZ) |
| write.py actor | this pane resolves as belam: pass `--actor director-general-6` on every write |
| HEAD moves | other posts commit on MAIN between calls: inspect your own commit by sha, never HEAD |
| `send.py read director-general-6` | resolves the caller as belam (startup exit 2): identity env not set for this pane -- use SendMessage lanes; bank if it matters |

## §5 Verification
(none yet)

## §6 BANKED
(none)

## Skills
agi-goal · agi-node-write · agi-dispatch · agi-workflow · agi-corrective · agi-verify · agi-send · agi-rotate · agi-memory-guard
