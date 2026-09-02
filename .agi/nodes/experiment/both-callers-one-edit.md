---
id: experiment:both-callers-one-edit
mint_id: 8afa31b5dcbd4699b6b1fd576952b5f5
type: experiment
title: Both callers, one edit
parents:
  - hypothesis:verbs-before-keystrokes
next_edges:
  - verdict:the-verb-layer-holds
scaffold_hash: 5069dd60e8238082
verdict: proved
confidence: 0.9
evidence_runs:
  - experiment:both-callers-one-edit
---

# experiment:both-callers-one-edit

## Experiment

`bin/edit.py`: five verbs (`set`, `unset`, `link`, `thought`, `note`), an
`Edit` accumulator, and `submit`. 11 tests.

### The identity that matters

```python
by_hand  = set(status, active); link(self); thought("why")
scripted = parse_script("set status active && link self && thought why")
assert scripted == by_hand
```

Asserted on the **accumulated object**, not on the resulting file — two paths
that produce the same file could still have taken different operations to get
there, and it is the operations `goal:g13.1` says must be identical.

### No file write in the module

Asserted by walking the AST for `open`, `write_text`, `write_bytes`,
`writelines` and `os.replace` — **not** by `grep`, because this session
already recorded a `grep` for a concept returning a hit from a docstring. Zero
offenders. Every verb ends in `node_writer.update_node`.

### The refusals

`id`, `mint_id`, `type`, `scaffold_hash` are rejected by both `set` and
`unset`. A mint id is assigned once (`goal:g2.5`) and `scaffold_hash` is how
completion is detected — edit mode is not a loophole in the rule the kid brief
already follows.

### Provenance, which had never been written before

`edited_by` and `thought_session` land on submit. **`thought_session` has been
reserved in frontmatter since `goal:g2.7`/`goal:g10.1` with nothing writing
it.** This is the first writer.

### Three behaviours that are easy to get wrong and are tested

- A frontmatter-only edit **leaves an existing thought alone**. Absent means
  empty; clearing one would read as evidence just as a fabricated one would.
- A `thought` verb **replaces** the region rather than accumulating.
- A `note` is idempotent — twice through leaves one `## Agent Notes` and one
  copy of the text.

### 🔴 A test defect this found, in code written one iteration earlier

The full suite went red at `test_set_link_goes_through_the_gated_writer`,
which **passed in isolation and in file order**. Two causes, both mine:

1. A test written in iteration 113 assigned `pw.node_writer.update_node = ...`
   directly on the module object instead of via `monkeypatch`, leaking a stub
   into every later test.
2. Fixing that was not enough. `test_completion.py` and `test_evidence_gate.py`
   load engine modules by file path and then do `sys.modules[name] = mod`, so
   **`node_writer` is not guaranteed to be one object once the whole suite runs
   in one process.** The test patched its own imported name; `write.py` called
   through its own reference; after those files ran, the two were different
   modules. Fixed by patching `write.node_writer` — the caller's own reference.

Worth recording as a general rule: **patch the object the caller actually
calls through, not a name that happens to resolve to it.** And a failure that
appears only in full-suite order is the worst kind, because both narrower runs
are green.

### Counts

11 new tests; suite 1316 → **1327**.

### What this experiment does NOT show

- **There is no modal shell.** No cursor, no keys, no live re-render, no
  submit-on-keystroke. The hypothesis was about build order and this is the
  first half of it.
- **No human has used it.** Verified by tests and one live `--dry-run`.
- **`thought_session` is written but not linked.** It holds whatever string a
  caller passes; nothing yet connects it to an actual session transcript,
  which is `goal:g2.7`'s real ask.
- **`--dry-run` was run against a real node; nothing was submitted to one.**

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The test-defect section is the most useful thing here and it is about my own
code from the previous iteration. The second cause is the interesting one: I
fixed the obvious leak, re-ran, and it was still red — which is the moment the
real cause becomes findable, and would not have been if the first fix had
happened to work.

Recording that `sys.modules` reassignment in two unrelated test files can make
"the same import" two objects is worth more than the fix. It is a property of
this suite, it will bite again, and the rule that survives it is to patch the
caller's own reference.

The last limit is deliberately small and precise. `--dry-run` against a real
node proves the CLI resolves and accumulates; it proves nothing about writing
to the live corpus, and the difference is exactly the one an over-read would
collapse.
<!-- THOUGHT:END -->
