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

# doc:card-director-general-6 — DG6's card: STOOD DOWN, handover

Role = the director template (doc:unified-director-brief) + the HEAD (doc:unified-head). Replaced whole; ≤ 100 lines.

## §0 State (06:2xZ 09-30) — STOOD DOWN
| | |
|---|---|
| post | director-general-6, Opus 5.5, MAIN, town local-maxxing, formation doc:council-loop |
| order | owner 06:1xZ via belam: "stand down director-general 5 and 6 to help conserve tokens ... 3,4 can continue as is and pick up whatever 5,6 don't finish" |
| stopped | queue runner killed; its queue saved in /tmp/dg6/queue.handover.txt; nothing new dispatched after 06:2xZ |
| still running (detached, pi-free, 0 USD) | parents DG6.07 a00-06814999 · DG6.08 a00-f79a834e (+kid a00-cdd04a9c) · reviews: units agi-director-general-6-mur-dg6-01/02/03/04 |

## §1 HANDOVER — goal:g1.31 (DG3/DG4 via SM's board)
Tools on this box: /tmp/dg6/harvest.py <aid> (check kid edits vs write-log) · /tmp/dg6/land.sh <aid> <iter> <leaf> · /tmp/dg6/murwait.sh <k> <branch> (verdict summary)
| leaf | hypothesis | state | next command |
|---|---|---|---|
| g1.31.3.1.1 | pb3-node-verdicts-match-bytes-1-6-13-46 | landed on loop tip 2298351ba; falsifiers green; mur dg6-01 running | murwait.sh dg6-01 season2/loops/hypothesis-pb3-node-verdicts-mat-a00-f7c21d0b -> clean: merge --no-ff |
| g1.31.3.1.2 | pb3-evidence-pointers-name-committed-bytes | tip 57b3475d5; F1 green (F2 hits only the round's own experiment quotes); mur dg6-02 running | murwait.sh dg6-02 season2/loops/hypothesis-pb3-evidence-pointers-a00-ab940124 |
| g1.31.3.2 (a) | pb3-anonymize-refuses-a-hardware-model-fragment | tip 0355de2f4 (DG6 committed anonymize.* cells); 234 passed; live F5 rc 1; mur dg6-04 running; OPEN Q: cell sources call raw nvidia-smi/lscpu vs the shim rule | murwait.sh dg6-04 season2/loops/hypothesis-pb3-anonymize-refuses-a00-fb71a5f6 |
| g1.31.3.2 (b) | pb3-hw-name-scrubbed-and-four-lost-corrections-restored | tip 807245f4d; leak counts 0; falsifier rc 0; mur dg6-03 running | murwait.sh dg6-03 season2/loops/hypothesis-pb3-hw-name-scrubbed--a00-dbbb2896 |
| g1.31.1.1 | pb3-run-mode-reads-one-formation-cell | parent a00-75a7f51b EXITED, no harvest dm; branch tip d46bf8773 | reconcile: harvest.py a00-75a7f51b -> land/re-dispatch |
| g1.31.1.2 | pb3-commands-bak-retired-by-move | parent a00-2001973e EXITED, no harvest dm; tip 97ffe1738 | harvest.py a00-2001973e |
| g1.31.2 | pb3-agi-post-stream-registered-and-current | parent a00-06814999 LIVE; tip 343f6687c | wait for its harvest dm |
| g1.31.4.5 (b) | pb3-engine-root-one-resolver-pin-retired | parent a00-f79a834e LIVE; tip 8d397f91d | wait; then dispatch .4.5a pb3-box-home-cells-derived-per-box + .4.6.1 pb3-drift-test-s26-caller-injective-json-field |
| g1.31.5.1.1 RED n19 | pb3-agent-git-hook-fails-closed-on-a-failed-diff | minted+committed 3cc5f1b1c, NOT dispatched | dispatch.py . <ITER> --target hypothesis:pb3-agent-git-hook-fails-closed-on-a-failed-diff --level small --tier parent --role parent --ladder-tier 0 --branch --detach |
| g1.31.5.1.2 RED n112 | pb3-anonymize-email-class-and-forward-scrub | PRIVACY row #1: node scrub DONE (05ae9fa37 5585ea79f 6646cf424 e3ff2c6a5; 0 email-shaped left in tracked nodes/skills/QUICKSTART/CLAUDE.md); anonymize.py email class NOT landed | dispatch AFTER g1.31.3.2 (a) merges (same anonymize.py + cell reader) |
| g1.31.4.7 | pb3-free-lane-test-fake-run-honours-text-mode | minted, NOT dispatched (suspected site: links.frontmatter_rows bytes-mode git grep vs the test's str fake) | dispatch |
| g1.31.4.2.2 | pb3-window-tip-fake-proc-per-model-denominator | minted, council ruling applied (5988edbda), NOT dispatched | dispatch |
| g1.31.4.4 | pb3-workflow-knobs-reach-js-one-global-form | minted, NOT dispatched | dispatch |
| g1.31.5.4.1-.4.3 · g1.31.5.5.1-.5.6 | (none yet) | 46 missed rows, leaves minted, NO briefs | brief (hypothesis schema) -> dispatch |
| DG3/DG4/DG5 leaves | g1.31.4.3 · .5.2 (DG3) · .5.1.3 (DG4) · .4.1 .4.2.1 .4.6.2 .5.3 (DG5, also standing down) | relayed by SM | SM reassigns DG5's |
Merge rule: only a mur-clean round merges (--no-ff, one at a time, merge-tree check vs trunk first: a00-6b761b8c is edited by BOTH dg6-01 and dg6-03, different regions) -> ONE [merge-up] to SM.

## §2 Second job (not started) — workflow.py headless claude-code stage route
pi stage argv -> `claude -p --model <m> --effort <e>`; the seam is proven by the Prime's passB3 ccrun.py. Needs its own goal leaf + hypothesis (SM places).

## 🔴 Where it stops
Down-ready. Nothing of DG6's is uncommitted in MAIN. The successor starts at §1 row by row; the four review units finish on their own.

## §4 Traps
| trap | rule |
|---|---|
| kid tier cannot commit | its write.py edits sit uncommitted in the PARENT's worktree (/mnt/agi-ram/worktrees/<aid>): land only after a write-log sha MATCH (harvest.py / land.sh) |
| verify-suite.lock | test with `[ ! -e lock ] || exit`; an `ls` exits 0 and let a8a69cb77 through |
| shared index | other posts leave files STAGED in MAIN: always `git commit -- <paths>`; read `git diff --cached --stat` first (6501d6972 swept belam's g1.31.md hunk) |
| write.py actor | this pane resolved as belam: pass `--actor director-general-6` |
| self-matching falsifier | a goal/brief that quotes the string its grep forbids matches itself: scope greps to target files |

## §6 BANKED
- owner (SM routes to the Prime): leaked hw name / pytest-of-<user> / owner email survive in old commits + grid versions -- rewrite is irreversible; rec: scrub forward only
- owner (missed rows): n109+n22 does a scrub take edited_by? (rec: no) · n6 <repo> vs {root} (rec: one cell) · n144 bare usernames beside anonymized paths in scope? (rec: yes)
- finding for DG3: 140 hypothesis + 56 experiment nodes carry two H1 lines (create adds one while --body-file brings one)

## Skills
agi-goal · agi-node-write · agi-dispatch · agi-workflow · agi-corrective · agi-verify · agi-send · agi-rotate · agi-memory-guard
