---
id: hypothesis:a00-46926322-66e092
mint_id: eb79e493dfb7499b8ba1455527f4f6cf
type: hypothesis
parents:
  - goal:g1.10
next_edges: []
confidence: 0.0
scaffold_hash: 8b7932f7b853df83
testable_claim: "**`commands.py run <name>` executes every `verify`-workflow command through the resolver, not directly — so the argv stored in the node is what actually runs, and changing it changes behaviour without editing any other file.**"
title: Commands.py run reaches every verify command through the resolver
verdict: pending
---
# hypothesis:a00-46926322-66e092

## Hypothesis

### Testable claim

**`commands.py run <name>` executes every `verify`-workflow command through the
resolver, not directly — so the argv stored in the node is what actually runs,
and changing it changes behaviour without editing any other file.**

`verdict:declared-commands-delete-four-copies` states explicitly: *"`run` is the
least-exercised path. The six `read` commands were run through the resolver;
the five `verify` commands were run directly, not through it."* The `verify`
commands (`smoke`, `tests`, `goals-check`, `viewport-verify`, `grid-commit`)
have been exercised only as standalone scripts invoked outside the resolver.

The humble claim: `commands.py run` passes every declared argv through
`_substitute`, `get`, and `subprocess.call` — the same code path the `agi`
router uses. If a verify command's argv is wrong in the node, `commands.py run`
catches it; invoking the script directly would not. That is the whole gap: the
property that proved the hypothesis (`grid-commit` as `grid.py --all` vs
`grid.py commit --all`) was checked for `read` commands but not for `verify`
commands.

### What would PROVE it

- `commands.py run smoke` exits 0 and produces real snapshot/render output
  (not just a no-op or a dry parse).
- `commands.py run tests` exits 0 and runs the real pytest suite.
- `commands.py run goals-check` exits 0.
- `commands.py run viewport-verify` exits 0.
- `commands.py run grid-commit` exits 0 (or reports nothing to commit, which
  is exit-0 behaviour from `grid.py commit --all`).
- Editing the node — e.g. changing `smoke`'s argv to include `--exit-1` —
  causes `commands.py run smoke` to fail with exit code 1, proving the
  resolver is the path actually taken.
- The `commands.py run` path uses the SAME `get()` → `run()` →
  `subprocess.call()` chain that `driver.sh`'s `agi` router calls, so
  verifying one verifies the other.

### What would DISPROVE it

- `commands.py run smoke` fails with a resolver error (wrong path, wrong argv)
  rather than a script error, proving the declaration was never exercised and
  has drifted from what actually runs.
- One of the verify commands exits non-zero when run through the resolver but
  exits 0 when invoked directly, proving the resolver injects a wrong argv.
- Editing the node's argv and re-running `commands.py run` produces the same
  behaviour as before the edit, proving the resolver cached or ignored the
  change.
- The `commands.py run` path has a different argv resolution or working
  directory than the `agi` router, making the two disagree.

### Coverage gap addressed

`test_commands.py` tests:
- `commands.load()` — parsing, substitution (`test_commands_resolve_from_the_node`)
- Subcommand acceptance (`test_every_declared_command_accepts_its_own_subcommand`)
- Target existence (`test_every_declared_command_points_at_something_that_exists`)
- The `agi` router for `links` (`test_a_bare_first_word_runs_a_declared_command`)

**NOT tested:**
- `commands.py run <name>` for ANY command — the resolver's own run method
- The five verify commands through the resolver at all
- End-to-end: edit node → `commands.py run` picks up the change

This hypothesis closes that gap with the same claim that proved the parent
hypothesis: *a wrong command in the table fails instead of being believed.*
Applying it to the verify workflow confirms the claim holds for every workflow,
not just the one whose gap was already tested.

### Motivation

`goal:g1.10`'s falsifier demands: *"Change the argv of a standard workflow
step by editing only the node, and have every caller — driver.sh, the skill's
table, a fresh operator following QUICKSTART.md — pick up the change."* The
`commands.py run` path is the most direct test of this: edit the node, run
via the resolver, observe the change. If the resolver is the canonical runner
for every workflow, the falsifier holds for every workflow.


## Agent Notes
Filled hypothesis body: commands.py run path is untested for verify commands (the gap verdict:declared-commands-delete-four-copies explicitly named). Claims resolver must execute all five verify commands through the same get()->run()->subprocess.call chain as read commands, proving the falsifier holds for every workflow.