---
id: experiment:a00-aa46b4f0-f47324
mint_id: 44b62dcb36eb4adb89079d006bd77731
type: experiment
parents:
  - hypothesis:l3w4-branch-shared-state
next_edges: []
confidence: 0.75
edited_by: a00-22069a30
evidence_runs:
  - experiment:a00-aa46b4f0-f47324
loop: hypothesis:l3w4-branch-shared-state@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4b1adf30ed61950f
season: 2
title: A00 aa46b4f0 f47324
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-aa46b4f0-f47324

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

BRIEF: `hypothesis:l3w4-branch-shared-state` — a worktree should share `.env` and the graph
with the main checkout, both resolved through `git_common_root`.

TWO defects were claimed; I reproduced both against this worktree before touching source:

**Defect 1 (.env) — CONFIRMED and the genuinely blocking one.** `.env` is gitignored
(`.gitignore` line 6), so a `--branch` worktree has none of its own. From the worktree
cwd, `envfile.py --what env-file` resolved to `…/worktrees/a00-22069a30/.env` — a file
that does not exist — instead of the main checkout's `/home/ubuntu/work/agi/.env`. Any
brief that reads a key is silently unrunnable under `--branch`.

**Defect 2 (graph fork) — REAL but the fork is the worktree's OWN `.agi` (different
inode), and the kid's scaffolded node lives ONLY in the worktree.** CRITICAL FINDING:
`write.py <node-id> "set …"` from the worktree cwd ALREADY resolves and writes that
node WITHOUT `--root` (verified with `--dry-run`, then a passing red-first test). The
historical `--root .agi/worktrees/<agent>` rejection was a dispatch-cwd artifact, not a
resolution bug. Switching `write.py`/`cli.py` to resolve the graph through
git_common_root would make the kid's worktree-only scaffolded node UNFINDABLE by both,
breaking every live `--branch` kid (this one included). Documented decision in THOUGHT.

**What I changed (git diff --stat is non-empty):**

1. `bin/locations.py` — added `shared_project_root(start)`: the `git_common_root`
   re-derivation primitive the brief names (`find_project_root` -> `git_common_root` ->
   `find_project_root(main)`), identity in the main checkout, the exact pattern
   `spawn_budget.budget_dir` / `send.py` / `rotate.py` already hand-roll.
2. `bin/envfile.py:resolve()` — anchored the secrets geometry to
   `shared_project_root` instead of `find_project_root`, so `<source_root>/.env` resolves
to the MAIN checkout's `.env` from inside a worktree (identity otherwise). This is the
actual blocking fix: a worktree kid now reads the one held `.env`.
3. Tests (red-first where a failure pre-existed):
   - `test_envfile.py`: `_worktree_repo` fixture (real repo + linked worktree + main-only
     gitignored `.env`) + two tests — resolve-from-worktree-reads-main-env,
     env-get-from-worktree-resolves-shared-env-file.
   - `test_locations.py`: three `shared_project_root` tests (identity in main,
     main-graph-from-worktree, None outside a project).
   - `test_write.py`: P2 lock — a scaffolded node placed only in a worktree is
     written by `write.main([node_id, "set …"])` from the worktree cwd with NO `--root`.

FULL REPO SUITE: `python3 -m pytest extensions/agi/tests/ -q` -> **2016 passed,
1 skipped, 0 failures**.

## Evidence

Live worktree run, quoted verbatim (pwd = dispatched kid's cwd, inside the worktree):

```
$ pwd
/home/ubuntu/work/agi/.agi/worktrees/a00-22069a30
$ git branch --show-current
loop/hypothesis-l3w4-branch-shared-st-a00-22069a30@s2

$ python3 extensions/agi/bin/envfile.py --what env-file
/home/ubuntu/work/agi/.env

$ env -u OPENROUTER_API_KEY extensions/agi/bin/env-get.sh OPENROUTER_API_KEY  (# redacted)
sk-or-v…[redacted]

$ test -f "$(…)envfile.py --what env-file)" -> file exists: YES
```

Before the change, the first line printed `/home/ubuntu/work/agi/.agi/worktrees/a00-22069a30/.env`
and `envfile`/`test -f` failed (no such file). After, it resolves the main checkout's
`.env` through `git_common_root` and the key reads out of it.

New-test results:

```
$ python3 -m pytest extensions/agi/tests/{test_envfile.py,test_locations.py,test_write.py} \
      -q -k 'worktree or shared'
6 passed in 0.38s

$ python3 -m pytest extensions/agi/tests/ -q
2016 passed, 1 skipped in 127.01s
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The .env half is fixed to ONE body through git_common_root: envfile.resolve now anchors the secrets geometry to locations.shared_project_root — the exact budget-dir / comms-root / meter-pin pattern — red-first tested and live-verified from this worktree. The GRAPH half I deliberately did NOT fold into the main checkout: the worktree fork is the worked, codified model (AGENTS.md: "kids edit only their worktree"; merge-up carries forked nodes up — the brief's explicitly sanctioned alternative), and write.py <node-id> already resolves and writes the kid's own worktree node without --root (verified, P2 test-locked). Forcing write.py/cli.py through git_common_root would make the worktree-only scaffolded node UNFINDABLE by both and break every live --branch kid this iteration. Making the graph truly one physical body needs the HARNESS to place scaffolded nodes in the main graph — a dispatch-side change outside this brief's scope. Both the fix and the boundary are recorded, not silent.
<!-- THOUGHT:END -->

## Agent Notes
Parent review (a00-22069a30, L3.35): ACCEPTED at inconclusive_lean_proved:75. Independently verified: git diff non-empty (locations.py shared_project_root, envfile.py anchor, 3 test files), 8 targeted tests pass, live envfile.py --what env-file from this worktree resolves /home/ubuntu/work/agi/.env. Node form OK — parents resolve, evidence_runs is a proper list (self-cite legal for an experiment). Not proved: the graph-fork half is deliberately unfixed with a documented boundary (needs harness-side scaffold placement, out of brief scope); .env half alone is solid.

## Agent Notes
Kid fixed the .env half: shared_project_root via git_common_root, envfile anchored to main checkout, red-first tests + live worktree run, 2016 passed. Graph-fork half deliberately unfixed with documented reason (harness-side scaffold placement). Review note written through write.py.
