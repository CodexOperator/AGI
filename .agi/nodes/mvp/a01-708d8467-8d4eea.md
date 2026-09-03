---
id: mvp:a01-708d8467-8d4eea
mint_id: 04df06242e7b450697d1322af753af34
type: mvp
parents:
  - verdict:declared-commands-delete-four-copies
next_edges: []
confidence: 0.8
scaffold_hash: ef0fc72bd1430e98
title: Every declared command runs through the resolver, under test
verdict: pending
---
# mvp:a01-708d8467-8d4eea

## MVP

A test that runs **every declared command** through `commands.run()` and asserts
exit code 0, covering all three workflows (`verify`, `read`, `see`).

`verdict:declared-commands-delete-four-copies` says plainly: *"`run` is the
least-exercised path. The six `read` commands went through the resolver; the
five `verify` commands were run directly, not through it."* The existing
existence test (`every_declared_command_points_at_something_that_exists`) and
the subcommand-vocabulary test cover *static* properties — a script being at
its path, a subcommand being one argparse declares. Neither actually invokes
the resolver and runs the command.

This MVP is the one missing dynamic check: **the resolver path, for every
command, tested.**

---

### What the test must assert

```python
@real_only
def test_every_declared_command_runs_through_the_resolver():
    """Not just "this file exists" — the resolver substitutes paths,
    builds argv, finds the cwd, and calls subprocess. That full chain
    must exit 0 for every declared command, including all three workflows."""
    failed = []
    for name, cmd in commands.load(REAL_ROOT).items():
        # run() is the resolver path — not subprocess.call(argv) directly
        ret = commands.run(REAL_ROOT, name)
        if ret != 0:
            failed.append((name, ret, cmd.argv))
    assert failed == [], (
        "declared commands that failed through the resolver:\n"
        + "\n".join(f"  {n}: exit {r} — `{' '.join(a)}`"
                      for n, r, _ in failed))
```

### Why this is not already covered

- `test_every_declared_command_points_at_something_that_exists` checks file
  existence, which stays green when a different file sits at the right path
  (the `write.py` → `links.py` rename proved that).
- `test_every_declared_command_accepts_its_own_subcommand` checks argparse
  vocabulary statically, which catches a renamed script but not a path
  substitution failure, a cwd that does not exist, or a runtime dependency
  the command does not actually have.
- `test_a_bare_first_word_runs_a_declared_command` checks ONE command
  (`links`) through the `agi` router, not the full set.

These three guards cover three different failure modes and miss a fourth:
**the command is declared, its file exists, its subcommand is valid, its
argv parses — and it still fails at runtime, and nothing told us.**

### What it would have caught

- **Any command whose `<root>` or `<engine>` substitution produces a path
  that does not resolve**, since `commands.run()` calls `subprocess.call()`
  and gets a non-zero exit.
- **A command whose `cwd` does not exist**, which `subprocess.call()`
  catches with a non-zero exit (unlike `run()` itself, which does not fail
  on a bad cwd — subprocess raises `FileNotFoundError`).
- **A command that depends on a runtime that happens to be absent on this
  machine** (`python3 -m pytest` with no pytest installed is a non-zero exit
  the static checks miss entirely).

### What it does NOT assert

- **That the correct output was produced.** This is an existence-plus-exit
  check, not a semantic one. `view` exits 0 whether or not the viewport
  connects; `credentials` exits 0 whether or not keys are being issued. The
  correct-response tests belong at the workflow level.
- **That the `run` path is faster or cleaner.** Performance is not the
  claim; the claim is that it *works*, tested.
- **That every script is imported cleanly.** Import errors produce exit code
  1, which this catches — but the error message is whatever Python prints,
  not a structured diagnosis.

## Inputs

- `REAL_ROOT` — the project's `.agi` directory, already resolved by
  `locations.find_project_root()`.
- Every declared command's `argv` and `cwd`, already substituted by
  `commands.load()`.

## Outputs

- A passing test that closes the `"run" is the least-exercised path` caveat
  from `verdict:declared-commands-delete-four-copies`.
- A failing test when a declared command cannot exit 0 through the resolver,
  named along with its exit code and argv, so the fix is targeted.

## Acceptance

1. The test discovers every command `commands.load()` returns, including
   `verify`, `read`, and `see` workflows.
2. `commands.run()` is the invocation path — not `subprocess.call(argv)`
   directly, not `bash driver.sh <name>`.
3. All 14-15 declared commands exit 0 through the resolver.
4. The test suite (`python3 -m pytest extensions/agi/tests/test_commands.py -q`)
   gains exactly one new test, and the total count increments by 1.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The verdict's title overstates and its body corrects it: "declared commands
are executable" is the proved half; "the four copies are deleted" is not.
The sibling `mvp:prose-derives-from-the-command-node` covers the derivation.
This MVP covers a different gap — the one where a command passes three static
guards and still fails at runtime, and nothing notices until a cold session
types it and gets an error.

The test deliberately uses `commands.run()` rather than calling subprocess
directly or routing through `agi <verb>`, because the claim is about the
*resolver path* — that `commands.run()` (which substitutes, builds argv,
resolves cwd, and calls subprocess) works for every command. The router test
(`test_a_bare_first_word_runs_a_declared_command`) tests a different path.

Three things should not change after this MVP: the resolver should stay thin
(the verdict explicitly warns against it becoming "the program the node
exists to avoid being"), the test should stay in the `real_only` group (it
must run against the real project, not the fixture, because fixtures cannot
reproduce the full runtime), and the scope guard (`<= 20`) must stay as the
binding constraint on growth.
<!-- THOUGHT:END -->


## Agent Notes
MVP: Automated test that runs every declared command through commands.run() and asserts exit 0 — covering verify, read, and see workflows. Closes the 'run is the least-exercised path' caveat from the verdict.
