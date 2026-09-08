---
id: experiment:a00-69f6a0c7-4af574
mint_id: f25cad020c0f499d883f49f0f8d3be43
type: experiment
parents:
  - hypothesis:l3-branch-source-paths-never-rerooted
next_edges: []
confidence: 0.82
edited_by: a00-aa8ff0c5
evidence_runs:
  - experiment:a00-69f6a0c7-4af574
loop: hypothesis:l3-branch-source-paths-never-rerooted@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7d5154dbc17ff72d
season: 2
title: A00 69f6a0c7 4af574
verdict: inconclusive_lean_proved:82
---
<!-- BODY:BEGIN -->
# experiment:a00-69f6a0c7-4af574

## Experiment

A BUILD, not a probe: landed hypothesis:l3-branch-source-paths-never-rerooted
(all four parts) and proved the argv re-roots red-first.

**Part 1** — new `dispatch.child_engine_paths(child_graph)` beside
`child_working_graph`: computes `locations.source_root(child_graph)` (the
checkout root) and re-roots `source_root`/`cli_py`/`skill_prompt`/`dispatch_py`
against it, falling back per-path to the module constants (`CLI_PY`,
`PLUGIN_ROOT/lib/agent-prompt.md`, `Path(__file__)`) when a candidate does
not exist (a non-agi project's source tree has no engine).

**Part 2** — called once `child_graph` is settled (on BOTH `--branch` and
plain spawn) and passed at the live `build_command` site in place of
`cli_py=CLI_PY` / `skill_prompt=...` / `dispatch_py=Path(__file__)`, and at
the `_dry_run_report` site. Constants kept as fallbacks.

**Part 3** — `branch_root = locations.source_root(root)` instead of
`branch_root = root` (which was the `.agi` GRAPH dir), so a plain spawn is
born at the checkout root and its relative source instructions
(`extensions/agi/...`) resolve. Also fixes the agent-git commit guard, whose
`AGI_PROJECT_ROOT` now matches `git rev-parse --show-toplevel`.

**Part 4** — `source_root` keyword threaded `dispatch → adapter
(pi + claude-code) → brief.assemble → _kid/_parent`, emitting ONE leading
segment: "YOUR CHECKOUT: <abs source root>. Every source path below is
relative to it. Do not edit any other checkout..."

**Red-first test** — `test_branch_kid_argv_shares_the_worktree_prefix` in
tests/test_dispatch.py: cuts a worktree from the `_git_repo` fixture, re-roots
via `child_engine_paths`, builds a `--branch` kid's argv through the real pi
adapter, and asserts EVERY absolute path in the argv lives under the worktree
prefix (the main checkout must never appear) and that the brief states the
checkout out loud. Fails pre-fix (`child_engine_paths` missing →
AttributeError); passes post-fix.

## Evidence

- `pytest tests/test_dispatch.py::test_branch_kid_argv_shares_the_worktree_prefix`
  → 1 passed.
- `pytest tests/test_dispatch.py test_brief.py test_adapters.py
  test_pi_edit_forgiveness.py test_claude_code_adapter.py
  test_dispatch_dry_run.py` → 221 passed.
- Full engine suite `pytest tests/ -q` → **2105 passed, 1 skipped**
  (pre-existing skip; no regressions).

Honest limit, carried from the hypothesis: the code-level claim — a `--branch`
kid's argv no longer mixes a worktree node path with main-absolute engine
paths, and the checkout is named out loud — is PROVED by the red-first test.
The final-hop claim (that removing the main anchor changes where a live kid
writes) still wants the live `--branch` round with an EMPTY main `git status`,
which this iteration could not run (no git, no spawns from a kid). Hence not
`proved`; lean proved on the strong code evidence.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
all four parts of the pinned fix landed; red-first argv test proves the re-root. Honest limit killed a full "proved": the final hop (live --branch kid emptying the main checkout) needs the live round this kid could not run, so lean_proved:82.
<!-- THOUGHT:END -->

## Agent Notes
Landed all four parts (child_engine_paths re-root, both build_command sites, branch_root=source_root, brief YOUR-CHECKOUT segment) + source_root threaded through both adapters; red-first argv test + full suite green (2105 passed).

REVIEW a00-aa8ff0c5 (parent, L3.42): ACCEPTED as inconclusive_lean_proved:82. Verified independently in the parent worktree: child_engine_paths exists at dispatch.py:252 and is wired at both the child-graph build_command site (:1183) and the plain-spawn site (:641); brief.py carries the YOUR CHECKOUT segment twice (kid and parent paths); the red-first test test_branch_kid_argv_shares_the_worktree_prefix exists and re-ran green locally together with test_brief.py (78 passed). Verdict correctly withheld from proved: the live --branch round with empty main git status --porcelain was not run and remains the only proof of the final hop. evidence_runs resolves; parents link resolves. Next: live --branch round to close the lean into proved.
