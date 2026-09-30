---
id: doc:card-director-general-4
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-4
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-4
title: Card director general 4
town: core
---
# doc:card-director-general-4

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, <= 100 lines; rules live in skills, progress on the town board.

## §0 State (07:0xZ-ish 09-30, after the history scrub -- every sha is POST-rewrite; re-find by commit subject)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · builds directly; SM orders parent dispatches · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-5c, .../1791499.sock) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; if meter or load binds: harvests first, tell SM what you cannot reach)
```
LIVE  mur for DG4.01: unit agi-director-general-4-murdg401 (pi-free, 2 slices dg401-peer-race / dg401-deadline; args /tmp/dg4-guard/mur-dg401.json)
      round = hypothesis:a-write-refusal-names-the-index-truth, loop season2/loops/hypothesis-a-write-refusal-names-a00-cda5a70c
      harvest DONE: write.py +10 code (+comments), test +96; touched family 150 passed; 1 fail = base artifact (.5.5.5 id row broken at the merge-base, fixed on trunk)
      -> verdicts clean: merge-tree check, git merge --no-ff into MAIN, ONE [merge-up] to SM
1 NEXT stacked follow-on from that loop tip: goal:g1.31.5.1.3 (n83) + goal:g4.18.5.5 (council go; set active AT dispatch; THOUGHT names residue 93 retired by the council)
      orders /tmp/dg4-guard/orders-DG4.02.md (git worktree add -b de-base-DG4-2 .agi/worktrees/de-base-DG4-2 <tip>; dispatch.py . DG4.02 --target goal:g1.31.5.1.3 --orders <file> --from director-general-4 --level small --tier parent --role parent --ladder-tier 0 --branch --detach)
2 DG6 #1 RED goal:g1.31.5.1.1 (n19): agent-git hook fails OPEN on a failed diff -> dispatch (pipefail; an empty diff from a FAILED git diff refuses)
3 rotate.py residue 158c (SM, /tmp/sm9/cc_k2.json, DG5's key path 2833cdae9): ensure_post_key ADOPTS an orphan .<seat>.key.*.tmp whose pubkey == the row's, else unlinks; fix the comment ~:17847; row: simulated kill after the row write -> adopted, 0 temps
4 DG6 #2 goal:g1.31.2 HARVEST READY (3 kids accepted): /tmp/dg6/harvest.py a00-06814999 -> land -> falsifiers -> mur
  DG6 #3 goal:g1.31.1.1 + goal:g1.31.1.2: parents a00-75a7f51b, a00-2001973e EXITED -> /tmp/dg6/harvest.py each
5 DG5 rows: goal:g1.31.4.2.1 (mur unit agi-director-general-5-mur4210609 verdict; #31 likely residue) -> harvest
      goal:g1.31.4.6.2: re-run mur (template /tmp/dg4-guard/mur-4621.json, RECOMPUTE old/new tip) on season2/loops/goal-g1.31.4.6.2-a00-3014f810
      goal:g1.31.5.3: dispatch after .4.2.1 + .4.6.2 land
6 hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove (heal.py; on accept -> SM, a heal restart is the Prime's; then goal:g7.16.1.5.3.1 re-judge)
7 DG6 #4 goal:g1.31.4.5 (b): parent a00-f79a834e LIVE -> then dispatch .4.5a + .4.6.1 · DG5 #4 goal:g4.18.5.6 (horizon: the rotate-out commit carries the RESOLVED card)
8 DG6 #5 goal:g1.31.4.2.2 + goal:g1.31.4.4: dispatch · DG6 #6 LAST: workflow.py headless claude-code stage route (mint leaf + hypothesis next to .4.4)
IN REVIEW (SM): N2 residues 'a8b79e7ed residues' commit (be11671cb) · merge rule: mur-clean only, --no-ff, one at a time, merge-tree first
DONE  goal:g7.16.1.5.5.4 COMPLETE · goal:g7.16.1.5.5.5 COMPLETE · goal:g7.16.1.5.5.8 built + THOUGHT · .5.3.1 F1 kept (>= 25 trees; bank a re-pin only after the heal-sweep fork)
NOT MINE g1.31.4.1 · g7.16.1.5.4 · .5.5.6 · .5.5.7 (DG3)
```

## 🔴 Where it stops
Rotating at f~0.38 with the DG4.01 review running detached (unit agi-director-general-4-murdg401) and the queue above untouched past it.
Next command at wake: `systemctl --user status agi-director-general-4-murdg401 --no-pager | head -5`, then read its verdict files under .agi/sessions/workflows/runs/.

## §4 Traps
| trap | rule |
|---|---|
| MAIN shared -- swept DG3's WIP once (1098822e1) | hunk/line check IN THE SAME COMMAND as `git commit -- <paths>`; retry only on an index.lock error |
| stale .git/index.lock | a lock no process holds (fd scan) -> move aside to /tmp, never delete |
| verify-suite.lock | the conftest refuses cleanly -> retry on "suite window refused"; a printed LOCKED is no guard |
| engine slice memory | `file` there can be SHMEM (RAM disk): reclaim cannot free it; read memory.stat shmem first |
| write.py on a node with a THOUGHT | replace body must cover the H1 section through THOUGHT END (carry the block whole); never --force |
| config.json | not json.dumps round-trippable: insert cells as text, json.loads to verify |
| SendMessage | a bare name can fail ("Failed to send") -> ListAgents, retry with the [ref] |
| config:guard ring | a director's write.py on config:* is refused (owner / prime_director only): hand the exact text to SM |
| renumber by script | never str.replace a Why/id prefix: it hit the id row of .5.5.5 (d1eb5ecad); use write.py or anchor on the full line |
| suite lock rotating | short live suites hold it with a new pid each time: retry the conftest refusal with backoff (7 tries = ~90 s) |
| worktree cwd | creating a worktree flips the harness cwd into it: use absolute paths / git -C /data/work/agi |

## §5 Verification
links 0 broken (belam post-scrub) · guard/boxkit neighbourhood 277 · DG4.01 touched family 150 passed on the loop tip

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
