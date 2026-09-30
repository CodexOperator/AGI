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

## §0 State (05:3xZ 09-30)
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
g1.31 split LANDED 6501d6972 (22 leaves; SM accepted; DG3/DG5 rows relayed by SM)
LIVE (pi-free, 0 USD, iter DG6.0N, dispatched from MAIN):
  DG6.01 a00-f7c21d0b  .3.1.1 hypothesis:pb3-node-verdicts-match-bytes-1-6-13-46
  DG6.02 a00-ab940124  .3.1.2 hypothesis:pb3-evidence-pointers-name-committed-bytes
  DG6.03 a00-dbbb2896  .3.2b  hypothesis:pb3-hw-name-scrubbed-and-four-lost-corrections-restored (URGENT #4)
QUEUE (all minted + committed; held only by load >= 16 -- `until load<16` waiter armed):
  1 DG6.04 .3.2a pb3-anonymize-refuses-a-hardware-model-fragment (kid returns the anonymize.* cell diff; DG6 commits it)
  2 DG6.05 .1.1 pb3-run-mode-reads-one-formation-cell · DG6.06 .1.2 pb3-commands-bak-retired-by-move · DG6.07 .2 pb3-agi-post-stream-registered-and-current
  3 .4.2.2 pb3-window-tip-fake-proc-per-model-denominator · .4.4 pb3-workflow-knobs-reach-js-one-global-form · .4.7 pb3-free-lane-test-fake-run-honours-text-mode
    .4.5b pb3-engine-root-one-resolver-pin-retired -> THEN .4.5a pb3-box-home-cells-derived-per-box (same config.json) + .4.6.1 pb3-drift-test-s26-caller-injective-json-field (tests .4.5b's mechanism)
closed at HEAD: #22 #25 (b8d232fc6) · #24 (59032171c) · #11 (dg2g6-b-recheck)
NEXT  harvest in place per round (merge-base diff, touched tests + neighbourhood, mur --harness pi-free per kid slice) -> merge cleared rounds -> one [merge-up] to SM
THEN  the 147 `missed` rows · second job: workflow.py headless claude-code stage route
```

## §2 Landed
- 6501d6972 goal:g1.31 -> 22 nested leaves · 324df95ec + 7eb1dacb6 + 2619b8972 + a2c9f4c7b + auto-commits: 13 round briefs

## 🔴 Where it stops
Rounds DG6.01-03 live; queue above waits on load. Next: `python3 extensions/agi/bin/spawn_budget.py status`; when load < 16: `dispatch.py . DG6.04 --target hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment --level small --tier parent --role parent --ladder-tier 0 --branch --detach` (then down the queue).

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
- owner: PASS B3 anonymize leak (#4) and pytest-of-<user> paths still live in old commits + grid versions -- rewriting history is irreversible (HEAD D): options (a) leave, scrub forward only [recommended] · (b) owner-run history rewrite
- decision taken (council may overrule): .4.2.2 meter falls back + tags `unmeasured:<model>` instead of refusing (rotation safety)

## Skills
agi-goal · agi-node-write · agi-dispatch · agi-workflow · agi-corrective · agi-verify · agi-send · agi-rotate · agi-memory-guard
