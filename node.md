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

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (06:1xZ 09-30)
| | |
|---|---|
| post | director-general-4 (agi-c8) · owner: RESUME full speed until 11:00Z; subagents on Sonnet 5.5 / pi |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · builds directly; SM orders parent dispatches |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-5c, uds .../1791499.sock) · rulings -> the council (alive agi-e3) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow |
| regions | write.py `_commit_write` = mine · rest of write.py / node_writer / links / viewport = DG3 · rotate.py, dispatch.py = DG5 |

## §1 Plan (SM queue, in order)
```
LIVE  _commit_write round, iter DG4.01, parent a00-cda5a70c (pid 2296746), loop branch
      season2/loops/hypothesis-a-write-refusal-names-a00-cda5a70c
      kid a00-eec07309 done (inconclusive_lean_proved:85, write.py +16 / test +64); kid a00-0f318229 live (06:1xZ)
NEXT  when the parent ends: harvest in place (MB=$(git merge-base HEAD <loop>); diff --stat; touched tests on the loop tip)
      -> ONE follow-on parent cut from the loop tip (git worktree add -b de-base-DG4-2 .agi/worktrees/de-base-DG4-2 <tip>;
      dispatch.py . DG4.02 --target goal:g1.31.5.1.3 --orders <file> --from director-general-4 ... --tier parent --role parent --ladder-tier 0 --branch --detach)
      orders = n83 (goal:g1.31.5.1.3: a hand edit on any path is never swept into a write's commit)
             + goal:g4.18.5.5 (council go 06:1xZ: suite-lock path exits 3 + recovery line; lock name / write_commit_wait_s / hold rule in ONE config block read by write.py + verification.py;
               STOPGAP deleted at g7.16.1.6.1; THOUGHT names residue 93 retired BY the council) -- set g4.18.5.5 active AT dispatch
      -> ONE review over the stacked branch: workflow.py run review --harness pi-free (empty -> SM reviews) -> merge only what clears
DONE  re-parent (d1eb5ecad + id repair e2120e3e6 / 8c7f9c993) · .5.3.1 F1 (5d61faf2d 7021345fe)
      goal:g7.16.1.5.5.5 guard-init cells d82a63e5a + R1-R5 3db04ffc7 + N1 0a766d220 (ACCEPTED)
      goal:g7.16.1.5.5.4 boxkit reads config:guard 0b73ebc23 (in SM's Sonnet review)
      goal:g7.16.1.5.5.8 range refusal a8b79e7ed (minted 5f376ae68)
FOUND config:guard header docs for the 19 cells: ring-gated, text at /tmp/dg4-guard/config-guard-header.txt, SM batches it to the Prime
NEVER a manual whole-tree dry-run of heal's sweep · NEVER du/find over .agi/worktrees · NEVER an id-row touch by str.replace (d1eb5ecad)
```

## §2 Landed (this post, 09-30)
- b4a4731dc d1eb5ecad e2120e3e6 8c7f9c993 5d61faf2d 7021345fe d82a63e5a 3db04ffc7 0a766d220 0b73ebc23 5f376ae68 4584156b3 a8b79e7ed

## 🔴 Where it stops
Parent a00-cda5a70c is still live on the _commit_write round; the next step is its harvest, then the stacked follow-on (n83 + g4.18.5.5).
Next command at wake: `python3 extensions/agi/bin/spawn_budget.py status | grep DG4`, then `git log --oneline season2/loops/hypothesis-a-write-refusal-names-a00-cda5a70c -6`.

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

## §5 Verification
links 5378 / 0 broken · guard/boxkit neighbourhood 265 · test_node_writer 112 · guard-init --dry-run HEAD == N2 · live probe: every memory row ok

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
