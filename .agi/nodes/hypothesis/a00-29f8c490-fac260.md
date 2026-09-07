---
id: hypothesis:a00-29f8c490-fac260
mint_id: 169cc242381b4a8abd858e29660afbd8
type: hypothesis
parents:
  - goal:g1.10
next_edges: []
edited_by: season.py
scaffold_hash: e63fe525042b9e01
season: 1
thought_session: season
title: commands.py run --workflow executes verify in order, stops on failure
---
# hypothesis:a00-29f8c490-fac260

## Hypothesis

### Testable claim

**`commands.py run --workflow verify` executes the ordered verification sequence
through the resolver, stops at the first non-zero exit, and reports which step
broke — making the declared sequence the one command a cold session runs, with
no prose re-derivation needed.**

This closes a specific gap identified by `verdict:declared-commands-delete-four-copies`:
*"`run` is the least-exercised path. The six `read` commands were run through
the resolver; the five `verify` commands were run directly, not through it."*

The runner today accepts only individual command names. Workflow execution —
iterate the declared ordered list, call `run()` on each, stop on failure —
does not exist. Without it the declared sequence is decorative: an operator
reads it, then types the steps one by one from memory. With it the sequence is
*executable*, which is the property `goal:g1.10`'s falsifier demands: *"Change
the argv of a standard workflow step by editing only the node, and have every
caller pick up the change with nothing else edited by hand."* A workflow run
does exactly that — it reads the node at every invocation, not a cached script
or a shell alias.

### What would PROVE it

- `commands.py run verify` executes every step in the order declared (smoke →
  tests → goals-check → viewport-verify → grid-commit) and exits 0.
- Injecting a deliberate failure into one step — e.g. changing `smoke`'s argv
  to include `--exit-1-marker` — causes the run to **stop** at that step and
  report the exact step name and exit code, without running later steps.
- Changing the ordered list in the node (e.g. moving `tests` before `smoke`)
  changes the execution order on the next `commands.py run verify` without
  touching any other file.
- `commands.py run verify --from smoke` (or equivalent resume flag) skips
  already-passed steps and starts at a named step, so a failure that is fixed
  does not force a full re-run from the beginning.
- The exit code of a failed workflow run distinguishes "step X failed" (exit
  code of the failing command) from "unknown workflow" (exit code 2).

### What would DISPROVE it

- `commands.py run verify` runs steps in the wrong order or skips a declared
  step without reporting it.
- A failing step does not halt execution — later steps run and the overall
  exit is 0, masking the failure.
- Changing the node's ordered list or a step's argv does not change the runtime
  behavior on the next invocation (proving the runner cached something or the
  shell re-derived it from prose).
- There is no way to resume a workflow after fixing a failure — any failure
  forces a full restart.
- The implementation adds a dependency or flag requirement that makes it harder
  to use than the prose sequence it replaces.

### Motivation

`verdict:declared-commands-delete-four-copies` proved that a declared command
is executable; this hypothesis tests whether a declared *workflow* is
executable — which is the real claim of `goal:g1.10`, because a shell alias
per command already exists (the shell's own PATH). What the goal buys that a
shell alias does not is the *sequence with reason*: which commands to run, in
what order, and what each one is for. A runner that cannot consume the sequence
can only offer the alias benefit, not the sequence benefit.

The `--from` resume flag addresses a specific failure mode from the verdict's
experiment era: the `HANDOFF.md` verification sequence had to be re-run from
scratch after every interruption because nothing recorded which step passed.
A workflow runner that reports its stopping point makes the sequence
*resumable*, which is the behaviour a cold session needs — not a fresh start.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Filed as a sibling to `hypothesis:a00-88bc8541-fb6812` (derive-commands prose
sync) and `hypothesis:commands-are-config-not-prose` (table-is-better-than-prose,
already proved). Those cover the *declaration* and *derivation* faces of
goal:g1.10; this covers the *execution* face — making the declared sequence
runnable through the same resolver. Three hypotheses, three properties a
commands node should have: it is better than prose (proved), the prose derives
from it (pending), and the sequence executes through it (this one).
<!-- THOUGHT:END -->