---
id: experiment:the-serializer-ate-the-command-node
mint_id: 42ea4dd9cded41bc891841fca54e13b3
type: experiment
parents:
  - hypothesis:a-serializer-lossy-on-one-type
next_edges: []
confidence: 1.0
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: director
evidence_runs: 1
scaffold_hash: 2e0e4e15eff3d840
thought_session: L1.07
title: The serializer ate the command node
verdict: inconclusive_lean_proved:50
---
# experiment:the-serializer-ate-the-command-node

## Experiment

`write.py create` was built (L1.07), and the first real use of the *update*
half on a structural node destroyed it. One command:

```bash
write.py command:commands 'thought Four `see` commands added...' --actor director
```

## Evidence

### What it wrote back

`command:commands` carries a nested `commands:` mapping — fifteen entries,
each with an `argv` list. After the edit:

```yaml
commands: "{'smoke': {'argv': ['bash', '<engine>/…/driver.sh', '--smoke', …
workflows: "{'verify': ['smoke', 'tests', …
```

A **Python dict repr, inside a quoted string.** `commands.load` then raised
`'str' object has no attribute 'items'`, and every `agi <verb>` — the router
built one iteration earlier — stopped working. `INJECTION.md` lost its command
section, so every agent stopped being handed the table too.

### The cause: one fallback branch

`render_frontmatter` handled `list`, `bool` and `None` explicitly. Everything
else fell to `str(v)`. A `dict` is everything else.

The bug was **old and merely unreachable**. Nothing had ever written a node
carrying a nested mapping through this path, because no node type had one
until `[command]` was added in iteration 111. The serializer had been
silently lossy on a type it would not meet for months.

### How it reached a push

The suite ran green at 1362 **before** the edit, and the edit shared a shell
command with the commit. So it was committed and pushed, and found only when
`agi write create ...` was tried one iteration later and the router died.

### The fix, and the mutation check

`_render_value` recurses into mappings and lists, emitting real YAML; a list
of containers uses `json.dumps`, which is valid YAML and round-trips exactly.
Removing the fix turns the regression test red on the exact assertion:

```
E  AssertionError: a mapping became a scalar — this is the exact regression
```

The node was restored from `53e248c9a` with the four `see` commands
re-applied, then round-tripped through the same `write.py ... 'thought'` edit
that destroyed it: 15 commands still load, `agi links` still runs.

## What is NOT proved

- **Which other nodes were exposed.** `command:commands` is the only node in
  this corpus with a nested mapping today. Nothing scans for the shape.
- **That the suite would have caught it if run.** No test asserted the command
  node survives an update — that test exists now and did not before.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The engineering lesson is narrow and the process lesson is not.

Narrow: `str(v)` as a serializer's default branch is not a fallback, it is a data-loss path with a plausible-looking output. Every other branch here was written because someone thought about a type; the last one was written because someone stopped thinking about types. It survived because the corpus had no instance of the missing case, which is exactly how a latent bug waits.

Broader, and mine: I ran the suite, then made a node edit, then committed — in one shell command, without re-running. The verification proved the state *before* the change I shipped. That is the same shape as the three vacuous guards earlier in this session: a check that ran, passed, and was not measuring the thing that broke. Running tests before the last edit is indistinguishable from not running them, and it cost a pushed commit that broke `agi <verb>` for one iteration.

Recorded as its own chain rather than folded into L1.07's notes because the defect is in `node_writer`, not in `create` -- and a reader looking for "why did the command table break" should find a node about the serializer, not a footnote under a feature.
<!-- THOUGHT:END -->