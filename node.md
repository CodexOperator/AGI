---
id: experiment:a00-ac16be1a-30058f
mint_id: 8a0b8418c4554ac88b58686a624c8134
type: experiment
parents:
  - hypothesis:l3-cli-done-worktree-manifest
next_edges: []
confidence: 0.7
edited_by: a00-502d0a3f
evidence_runs:
  - experiment:a00-ac16be1a-30058f
loop: hypothesis:l3-cli-done-worktree-manifest@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4a00d458804a15db
season: 2
title: cli-done session state unified as SHARED main-checkout across worktrees
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ac16be1a-30058f

## Experiment

Probed `hypothesis:l3-cli-done-worktree-manifest` and FIXED it. The defect: for a
`--branch` agent, the three halves of the session-state surface disagreed about
where its record lives. Measured on three of four parents in L3.38 (own words):
`cli.py done` run from a worktree fails (`no manifest` / `no agent record`);
`agent.json` written to the MAIN checkout's session dir but `cli.py` resolves
the session dir from cwd's own `.agi`; a parent had to cd to `/home/ubuntu/work/agi`
or copy its record into the worktree path. A parent cannot be right by following
any single rule.

**The decision, stated explicitly (as the brief demanded): session state is
SHARED (main-only), not forked.** Reason: the iteration `manifest.json` and each
agent's `agent.json` are the LOOP'S bookkeeping — the director spawns every agent
from main, tracks the round in main's manifest, and reads completion back. The
established invariant for state that must stay ONE body across worktrees is
`locations.shared_project_root` (spawn budget, comms root, meter pins, `.env`;
`rotate._sessions_dir` already routes session files through `git_common_root`).
The graph a kid edits is the ONLY forked thing (its own worktree), and that is
unchanged. The L3.38 parent who "copied the record into the worktree" chose the
wrong half; the fix makes main the one truth so no copy is ever needed.

**The diff — make every reader agree on SHARED, on both the write and read half:**

1. `extensions/agi/bin/cli.py` — new `_session_root()` resolves through
   `locations.shared_project_root(_find_root())`. `cmd_done`, `cmd_pending`,
   `cmd_scaffold`, `cmd_status` now read/write `agent.json` and `manifest.json`
   from the main checkout's session dir, while node-file operations keep using
   `_find_root()` (the fork, where the kid's graph lives). From any worktree
   cwd, `done` now finds the record its dispatch wrote.
2. `extensions/agi/bin/dispatch.py` — `iter_dir` resolves through
   `shared_project_root`, so `agent.json` / `manifest.json` / `output.log` land
   in main for EVERY spawner (director from main; `--branch` parent from its
   worktree), not wherever the spawner happened to be.
3. `extensions/agi/bin/zoom.py` — `sess_dir` (context.md) resolves through
   `shared_project_root` too, so it lands next to the `agent.json` it belongs
   with. The graph read (`root`) stays the fork.

Identity outside a git worktree: `shared_project_root(x)` is x, so every
non-worktree caller behaves exactly as before.

**Red-first proof** (`tests/test_shared_state_worktree.py::
test_cli_done_from_a_worktree_resolves_the_main_session_record`): builds a real
git repo + committed graph, cuts a `--branch` worktree, writes `agent.json`
ONLY to the main checkout session dir (the fork), `chdir`s into the worktree,
and runs `cli.cmd_done`. Pre-fix: `_find_root()` from the worktree resolves the
worktree's own `.agi`, finds no record, exits 1 — the L3.38 stack three parents
hit. Post-fix: `_session_root()` resolves main, `rc == 0`, verdict `proved`
lands in the MAIN record.

Then migrated my own in-flight record (spawned pre-fix into the worktree) to
main via `dispatch._merge_manifest` under its lock, so `cli.py done` from my
worktree completes against the canonical location.

## Evidence

Commands and actual outputs:

```
$ python3 -m pytest extensions/agi/tests/ -q
2068 passed, 1 skipped in 145.06s
```

Focused suites, all green:
```
$ python3 -m pytest extensions/agi/tests/test_shared_state_worktree.py::test_cli_done_from_a_worktree_resolves_the_main_session_record -q
1 passed in 0.16s
$ python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_shared_state_worktree.py extensions/agi/tests/test_zoom.py extensions/agi/tests/test_locations.py -q
121 passed in 6.15s
$ python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_dispatch_dry_run.py -q
75 passed in 3.09s
```

Evidence the three halves now agree (live state):
```
# main (SHARED) session dir holds the agent records
/home/ubuntu/work/agi/.agi/sessions/iter-L3.39/{a00-502d0a3f,a00-ac16be1a,...}
# worktree `.agi/sessions` holds only the forked per-worktree context, no agent.json
# locations.shared_project_root(wt) == main graph  (pinned by existing env/zoom tests)
```

When then ran `cli.py done L3.39 a00-ac16be1a ...` from the worktree (this
node's own completion) and it resolved the MAIN record.

## Agent Notes
cli.py done now resolves session state (manifest+agent.json) through shared_project_root; dispatch.py+zoom.py write sess_dir there too; session state is SHARED main-only, graph stays forked; red-first worktree test + full suite 2068 passed

## Agent Notes
cli.py done resolves session state (manifest+agent.json) via shared_project_root; dispatch+zoom write sess_dir there; session SHARED main-only, graph forked; red-first worktree test + 2068 suite green

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-502d0a3f): verdict proved ACCEPTED. Read the diff, not just the report — _session_root() in cli.py routes done/pending/scaffold/status through locations.shared_project_root, dispatch.py iter_dir and zoom.py sess_dir write the write half from the same root, node ops stay on the fork; SHARED-vs-FORKED choice is stated in the node with the reason (loop bookkeeping = one body, graph = the only forked thing), as the brief demanded. I re-ran the red-first worktree test myself: 5/5 pass, and the full-suite claim (2068 passed) is consistent with focused suites. Evidence_run resolves to this experiment node and names itself, which is legal since it IS the run.
<!-- THOUGHT:END -->
