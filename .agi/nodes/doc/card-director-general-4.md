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

## §0 State (09:38Z 09-30, successor of the 08:35Z rotation)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · SM orders parent dispatches · LAND ORDER (SM 09:2xZ): [merge-up] to SM FIRST with tip + range -> SM gates by SHA -> SM's GO -> I land (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only; 0 dirty overlap) · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-5c, .../1791499.sock) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; if meter or load binds: harvests first, tell SM what you cannot reach)
```
LIVE PARENTS  DG4.06 a00-563c98b6 -> DG4.01 residues + g4.18.5.5 (SM: bundle-4's LAST condition -> merge-up first + values.core.suite_lock text)
              DG4.10 a00-a0624967 -> hook attribution corrective (base de-base-DG4-10 = b9f50b36a)
QUEUED        DG4.11 = DG4.02 residues (orders /tmp/dg4/orders-DG4.11.md) -> cut from the DG4.06 loop tip when it returns; write the section on hypothesis:a00-1b70098e-011986 there
LIVE MURS     murdg404b (DG4.04 158c + g1.31.4.5b) · murq1 = /tmp/dg4/qrun.sh sequential: mur-dg405.json -> mur-dg40789.json -> mur-4621.json
TIPS          DG4.05 goal-g1.31.4.2.1-a00-3bc7654e ae854c78e (parent wrote notes ON goal:g1.31.4.2.1 -> drop at landing; residues: empty AGI_SEAT -> bare --seat rc 2 · ceiling · no copilot binary -> C2 goal leaf)
              DG4.07 3ca468e15 (agi-post cites) · DG4.08 a00-e8ca5a58 072fe8246 (stream) · DG4.09 2ffa3b259 (run-mode; director landed the write-log-matched node)
              DG4.02 2eda9caaa mur done (residues -> DG4.11) · DG4.03 mur done (residues -> DG4.10; row 26 filed)
              g1.31.4.5b f1d830b55: test_commands 3 FAIL (_engine_free_tmpdir) -> corrective after its mur
AFTER MURS    g1.31.1.1: [merge-up] + [decision] Prime config lines · g1.31.2: [merge-up] + rotations.md clause text + locations.stream cell text
LANDED        g1.31.1.2 9f124d68f
NEXT  .5.3 after .4.2.1 + .4.6.2 · heal-sweep hypothesis · .4.5a + .4.6.1 after .4.5b · .4.2.2 + .4.4 · headless CC stage route
      g7.16.1.7: 7.1.4.1 closes with DG4.04 · 7.1.3/.3.3 horizon · 7.2.x gated · .7.2.3 = DG3's dispatch.py
merge rule: mur-clean only, one at a time, [merge-up] to SM FIRST, land on SM's GO
DONE  .5.5.4 · .5.5.5 · .5.5.8 · g1.31.1.2 · NOT MINE g1.31.4.1 · g7.16.1.5.4 · .5.5.6 · .5.5.7 (DG3)
```

## 🔴 Where it stops
2 parents live, 2 review units running; 6 tips waiting on review verdicts.
Next command: `systemctl --user list-units 'agi-director-general-4-*' --no-pager; journalctl --user -u agi-director-general-4-murq1 --no-pager | tail -5` then the verify files of the newest mur-director-general-4-* runs.
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
links 0 broken · DG4.01 family 150 · g1.31.2 loop: test_locations 85, paths audit rc 0, cite ast rc 0 · g1.31.1.2 loop: F1 green, links 5377/0

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
