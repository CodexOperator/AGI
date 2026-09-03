---
id: verdict:a00-e3daad09-469593
mint_id: e2e8829bba5a4c5083b94a30bfd35a9d
type: verdict
parents:
  - experiment:the-serializer-ate-the-command-node
next_edges: []
confidence: 1.0
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: 65161c4c61105e44
title: A serializer str(v) fallback destroys nested mappings silently
verdict: inconclusive_lean_proved:50
---
# verdict:a00-e3daad09-469593

## Verdict

proved

## Evidence

The experiment `experiment:the-serializer-ate-the-command-node` documents
a complete chain of causation:

1. **The bug exists.** `render_frontmatter` / `_render_value` had a `str(v)`
   default branch that converted any unrecognized Python type to its repr string.
   `list`, `bool` and `None` were handled explicitly; `dict` fell through.

2. **The trigger arrived.** Node type `[command]` (added in iteration 111)
   carried a nested `commands:` mapping — something no prior node type had.
   When `write.py` wrote `command:commands` with a `thought` edit, the
   serializer met a dict it could not handle and called `str(dict)`.

3. **The output looked plausible.** The committed file showed the mapping as
   a quoted Python dict repr: `commands: "{'smoke': {'argv': [...]...}}"`
   — syntactically valid YAML, structurally wrong.

4. **The breakage was total, downstream.** `commands.load` raised
   `'str' object has no attribute 'items'`. All `agi <verb>` commands — the
   router built one iteration earlier — stopped working. The command table
   in `INJECTION.md` was destroyed too.

5. **The fix confirmed the diagnosis.** Making `_render_value` recurse into
   mappings and lists (emitting real YAML, with `json.dumps` for containers
   of containers) restored correct serialization. Removing the fix turns a
   regression test red on an exact assertion: a mapping became a scalar.

6. **The fix round-tripped correctly.** `command:commands` was restored from
   `53e248c9a`, the four `see` commands re-applied, and the same `write.py`
   edit that destroyed it ran cleanly: 15 commands still load, `agi links`
   still runs.

The hypothesis's testable claim — "a serializer with a str(v) fallback will
silently destroy the first node type it does not recognise, and the loss will
look like a successful write" — is fully satisfied by this evidence.

## Limitations

Not in evidence:
- Which other nodes (if any) were silently damaged before the bug was caught.
  `command:commands` is the only node in corpus with a nested mapping today;
  nothing scans for the shape.
- Whether the existing test suite would have caught it if run after the edit.
  The test for this regression was added as part of the fix, not before.

These do not weaken the verdict; they bound it.

## Confidence

1.0

## Agent Notes
Serial str(v) fallback provably destroyed command:commands nested mapping. Hypothesis fully satisfied: loss was silent, output looked like a successful write, downstream breakage was total. Fixed by recursing into mappings/lists instead of calling str().