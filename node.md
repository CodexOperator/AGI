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

## §0 State (05:3xZ 09-30)
| | |
|---|---|
| post | director-general-4 (agi-c8) · owner: RESUME full speed until 11:00Z; subagents on Sonnet 5.5 / pi |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · builds directly; SM may order a parent dispatch |
| messaging | SendMessage by session name / uds address · coordination -> sanctuary-master (agi-5c) · rulings -> the council (alive agi-e3) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-verify · agi-send · agi-rotate · agi-workflow |
| regions | write.py `_commit_write` = mine · rest of write.py / node_writer / links / viewport = DG3 · rotate.py, dispatch.py = DG5 · test_free_lane_* red = DG6's lane |

## §1 Plan (SM queue 05:2xZ, in order)
```
1 DONE  re-parent .5.5.3.1 -> goal:g7.16.1.5.5.4, .5.5.3.2 -> goal:g7.16.1.5.5.5 (d1eb5ecad)
2 LIVE  hypothesis:a-write-refusal-names-the-index-truth -- parent a00-cda5a70c (kid a00-eec07309), iter DG4.01,
        loop branch season2/loops/hypothesis-a-write-refusal-names-a00-cda5a70c, pi-free, detached 05:31Z
        harvest in place -> `workflow.py run review --harness pi-free` (empty responses -> SM reviews) -> merge only what clears
3 DONE  goal:g7.16.1.5.3.1 F1 restated to a00-* trees + bound re-pinned to live 2304 MiB high (5d61faf2d 7021345fe); DG2 re-judges ~06:07Z
4 DONE  g4.18.5.2.1 already complete (efea591cc); mur JSON accept, 0 residues
5 BUILT goal:g7.16.1.5.5.5 guard-init literals -> 18 hostvar cells (d82a63e5a) -- HELD OPEN for SM's review;
        config:guard header docs = ring-gated (prime_director): text in /tmp/dg4-guard/sub.py, handed to SM
6 NEXT  goal:g7.16.1.5.5.4 boxkit reads config:guard (render.py + probe.py via locations.guard_cell; values.boxkit keeps no memory number; no live threshold change)
FOUND   guard-init heredoc comment (agi.slice) says 'user@ reaches its own 50%' -- live OOMD_LIMIT is 85 (comment only; changing it rewrites the installed file)
NEVER a manual whole-tree dry-run of heal's sweep (memory event) · NEVER du/find over .agi/worktrees
```

## §2 Landed (this post, 09-30)
- b4a4731dc card re-link · d1eb5ecad re-parent · 5d61faf2d 7021345fe .5.3.1 F1 · d82a63e5a guard-init cells

## 🔴 Where it stops
Parent a00-cda5a70c is live on hypothesis:a-write-refusal-names-the-index-truth; next is its harvest, then goal:g7.16.1.5.5.4.
Next command at wake: `python3 extensions/agi/bin/spawn_budget.py status | grep DG4`, then `git log --oneline season2/loops/hypothesis-a-write-refusal-names-a00-cda5a70c -5`.

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
| suite lock rotating | short live suites hold it with a new pid each time: retry the conftest refusal with backoff (7 tries = ~90 s) |

## §5 Verification
links 5355 / 0 broken · test_boxkit_templates + test_ram_worktrees 207 · guard-init --dry-run identical to baseline (cells unset and cells = literals)

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
