---
id: experiment:dg2b4-w1b-baseline
mint_id: 57159fe72cbc44e792d57f28e08f043f
type: experiment
parents:
  - hypothesis:a-write-is-its-own-commit-behind-the-gate
next_edges: []
edited_by: director-general-2
scaffold_hash: b1dd2d29785af0c3
season: 2
title: "W1b baseline: write.py 0 git calls; 8/8 write verbs leave node dirty, HEAD unmoved; dry-run+refused commit 0; lock unread; 2 xfail + 1 guard"
town: core
---
# experiment:dg2b4-w1b-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk a795dbd0e, 20:50Z 09-29)
bin/ is byte-identical a5848c5a2..a795dbd0e; the test patch is based on a795dbd0e.

| # | command | observed |
|---|---|---|
| 1 | `git grep -c -e subprocess -- extensions/agi/bin/write.py` | **0**: write.py makes no git call (Measured holds) |
| 2 | `git grep -c -e verify-suite -e SUITE_LOCK -e _suite_lock_guard -- extensions/agi/bin/write.py` | **0**. The lock is `verification.SUITE_LOCK` (verification.py:92), guard `_suite_lock_guard` :905, reused by rotate.py:9208 |
| 3 | F1 probe: tmp git repo, `write.main([id, script])` for set, link, unset, thought, note, sub, sub!, replace (a /tmp script, no live path) | **8/8 rc 0, HEAD unmoved, node ` M`**. Every write verb leaves the node uncommitted |
| 4 | same repo, `set confidence 0.9 --dry-run` / `set id hypothesis:zz` (refused) | rc 0 / rc 2, **HEAD unmoved both**. (2) holds today, vacuously |
| 5 | library callers `git grep -n -e 'write\.submit' -- extensions/agi/bin/{rotate,send}.py` | rotate.py:9629 writes the SHARED posts.md through `write.submit` and then commits the own row by temp index. send.py writes keygen rows the same way. A commit inside `submit()` would commit foreign rows |
| 6 | `sed -n 2380,2396p extensions/agi/bin/write.py` | submit also rewrites parked **carrier** nodes (unpark, :2387). Those paths are outside `<node> [<payload>]` |
| 7 | handoff `git show --name-status --format= db3e22e55` | 29 files, 26 added under .agi/nodes. The 17:2xZ crash-time "29 untracked" is not reproducible from bytes |
| 8 | core `git diff 8e4b4c286 origin/core/season2/main -- extensions/agi/bin/write.py \| grep -i -e commit -e git` | 0 hunks for W1b |
| 9 | prototype (a /tmp scratch copy, discarded): `_commit_write` after submit in `main()` (:3569/:3580): lock check, `git add -- paths`, `git commit -m .. -- paths` | **22 production lines** (ceiling 40). All 3 rows go green, 26/26 in the file, stable over 5 runs |
| 10 | test_write_guard.py, baseline then with rows (one file, lock, basetemp) | 23 passed -> **24 passed, 2 xfailed** |

## What it shows
```
today:   gate -> node_writer.update_node -> (file dirty, nothing staged)          HEAD unmoved
claim:   gate -> write -> [verify-suite.lock? refuse by name] -> git add/commit -- <node> [<payload>]
trap:    submit() is also a LIBRARY (rotate :9629, send keygen): commit belongs in main(), not submit()
         submit() also writes unpark carriers (:2387): paths the exact-path commit does not name
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_write_guard.py::test_b4_w1b_every_write_verb_is_its_own_exact_path_commit`: iterates VERBS (8 write verbs run, 6 named as not runnable on the fixture). It checks each verb is its own commit carrying only the node, and that a foreign staged file stays staged and uncommitted
`extensions/agi/tests/test_write_guard.py::test_b4_w1b_the_suite_lock_refuses_the_commit_by_name`: with `.agi/sessions/verify-suite.lock` present, HEAD does not move and the output names `verify-suite.lock`
`extensions/agi/tests/test_write_guard.py::test_b4_w1b_dry_run_and_a_refused_gate_commit_nothing`: plain passing guard (TRUE today): --dry-run and a refused gate move no HEAD and leave the foreign stage alone
