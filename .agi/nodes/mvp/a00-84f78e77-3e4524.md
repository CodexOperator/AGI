---
id: mvp:a00-84f78e77-3e4524
mint_id: 8d97bd2fa68e4aa28f2ac562eaff910e
type: mvp
parents:
  - verdict:declared-commands-delete-four-copies
next_edges: []
confidence: 0.0
scaffold_hash: 7f3460a31cf243a7
title: Run declared workflows through the resolver in batch
verdict: pending
---
# mvp:a00-84f78e77-3e4524

## MVP

Add a `--workflow` flag to `commands.py run` that runs every command in the
named workflow through the resolver sequentially and reports per-command
results.

`verdict:declared-commands-delete-four-copies` proved that a declared command
table is executable — the `read` workflow was exercised, the `verify` workflow
was NOT run through the resolver (the verdict says so explicitly: *"`run` is
the least-exercised path. The six `read` commands went through the resolver;
the five `verify` commands were run directly, not through it"*). The driver.sh
router now routes all verbs through `commands.py run`, so every command IS
resolved — but no single entry point exercises *a whole workflow* in batch
through the resolver.

### What it must satisfy

- `commands.py run --workflow verify` runs smoke, tests, goals-check,
  viewport-verify, and grid-commit through the resolver in that order. Exit 0
  if all succeed, first-fail with the failed command's stderr.
- `commands.py run --workflow read` runs links, schema, budget, credentials,
  secrets, and crons (order is deterministic but declaration-dependent, since
  `read` is an unordered set).
- `commands.py run --workflow see` runs view, view-llm, view-both, and write.
  Each resolves through the graph, so `--root` and `<root>`/`<engine>`
  substitution happen normally.
- `commands.py run --workflow nosuch` says which workflows are available.
- Add integration tests: for each workflow, run through the resolver and
  record which commands exit non-zero. These are the tests the verdict lacked.

### What it explicitly is NOT

- Not a replacement for the driver.sh router. `agi verify` still works exactly
  as it does now — the router already calls `commands.py run verify`. This is
  a *batch* entry point for running an entire workflow at once, not a new
  invocation pattern.
- Not a cron check. CI or a cron could call `--workflow read` as a liveness
  probe, but that is a separate deploy decision.
- Not `--continue-on-error`. First-fail is simpler and is what a `verify`
  workflow should be. A set (`read`) already has no meaningful ordering, so
  first-fail on a set is just "stop after the first failed read" — which is
  good enough.

## Inputs

- `--workflow <name>` — the workflow key from the command node
  (`workflows.<name>` in the frontmatter). `verify`, `read`, `see` in the
  current declaration.
- The usual `--root` (implicit from the driver.sh router, or explicit for
  direct calls).
- No pass-through args are appended for `--workflow` mode. A command that
  needs extra args is run directly with `commands.py run <name> <args>`.

## Outputs

- Exit 0: every command in the workflow succeeded.
- Exit non-zero, first fail: print the command name, its argv, its exit code,
  and its stderr summary. Stop and exit with that command's exit code.
- On an unknown workflow name: print available workflows and exit 2.


## Agent Notes
MVP for commands.py run --workflow flag, closing the 'run is the least-exercised path' gap from the parent verdict
