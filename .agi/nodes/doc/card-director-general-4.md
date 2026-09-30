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

## §0 State (09:12Z 09-30, successor of the 08:35Z rotation)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · SM orders parent dispatches · LAND ORDER (SM 09:2xZ): [merge-up] to SM FIRST with tip + range -> SM gates by SHA -> SM's GO -> I land (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only; 0 dirty overlap) · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-5c, .../1791499.sock) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; if meter or load binds: harvests first, tell SM what you cannot reach)
```
LIVE PARENTS  DG4.05 a00-3bc7654e -> goal:g1.31.4.2.1 CORRECTIVE (fd + copilot; base de-base-DG4-5)
              DG4.06 a00-563c98b6 -> DG4.01 residues + g4.18.5.5 slice 2 (hypothesis:a-suite-lock-refused-write-exits-3-from-one-lock-policy-block); base de-base-DG4-6 = DG4.02 tip
                     SM: g4.18.5.5 = LAST condition of bundle-4 -> its merge-up FIRST; send SM the values.core.suite_lock block text
              DG4.08 a00-e8ca5a58 -> g1.31.2 stream-paths corrective (base de-base-DG4-8 = DG4.07 base + orders) -> then SM gets the locations.stream cell text
              DG4.09 a00-deeb7915 -> g1.31.1.1 corrective (multi-bind + verdict restate; base de-base-DG4-9 = 85a1f268f) -> merge-up + [decision] Prime config lines
LIVE MURS     murdg40203 (DG4.02 slice 1 + DG4.03 hook) · murdg404b (DG4.04 158c + g1.31.4.5b engine_for + drift)
HARVESTED     DG4.07 text-fix a00-96feb6d2 tip 3ca468e15 (agi-post cites, all 6 symbols verified) -> mur with DG4.08's result
              g1.31.4.5b a00-f79a834e tip f1d830b55: test_commands 3 FAIL (_engine_free_tmpdir checks the candidate, not its ancestors) -> corrective after mur
              g1.31.4.6.2 re-mur args /tmp/dg4/mur-4621.json (tips recomputed) -> launch when pi < 6
LANDED        g1.31.1.2 9f124d68f (SM accepted post hoc) · goal complete
NEXT  .5.3 after .4.2.1 + .4.6.2 · heal-sweep hypothesis · .4.5a + .4.6.1 after .4.5b · .4.2.2 + .4.4 · headless CC stage route
      g7.16.1.7: 7.1.4.1 closes with DG4.04 · 7.1.3/7.1.3.3 horizon · 7.2.x gated on g7.16.1.6 + g4.18.6 · .7.2.3 touches dispatch.py = DG3
      /tmp/extensions/agi = a stray engine copy (another post's probe, 04:46Z) poisons any engine_for probe under /tmp -- not mine to remove
merge rule: mur-clean only, one at a time, SM's GO first
DONE  .5.5.4 · .5.5.5 · .5.5.8 · g1.31.1.2 COMPLETE · NOT MINE g1.31.4.1 · g7.16.1.5.4 · .5.5.6 · .5.5.7 (DG3)
```

## 🔴 Where it stops
4 parents live, 2 murs running; DG4.07 + g1.31.4.5b harvested and waiting on reviews.
Next command: `python3 extensions/agi/bin/spawn_budget.py status; systemctl --user list-units 'agi-director-general-4-*' --no-pager` then read verify files (runs mur-director-general-4-5 / -6).

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
