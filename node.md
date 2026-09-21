---
id: verdict:the-verb-layer-holds
mint_id: 7d28693a2a424e7cb0cd9ac65b0c0284
type: verdict
parents:
  - experiment:both-callers-one-edit
next_edges: []
confidence: 0.9
edited_by: season.py
evidence_runs:
  - experiment:both-callers-one-edit
scaffold_hash: 98cccffcf59205b6
season: 1
thought_session: season
title: The verb layer holds, and no verb turned up that needs a cursor
verdict: proved
---
# verdict:the-verb-layer-holds

## Verdict

proved

## Evidence

`experiment:both-callers-one-edit`:

- The `&&`-serialised form and the direct verb calls produce an **identical
  accumulated edit**, asserted on the object rather than on the file.
- **No file write in `edit.py`** — AST-checked for `open`, `write_text`,
  `write_bytes`, `writelines`, `os.replace`. Zero. Every verb ends in
  `node_writer.update_node`.
- `id`, `mint_id`, `type`, `scaffold_hash` refused by every verb.
- `edited_by` and `thought_session` written on submit — the **first writer**
  of a field reserved since `goal:g2.7`.
- 11 tests; suite 1316 → 1327.

## What is proved

**Building the verbs before the shell was the right order, and the hypothesis
made that falsifiable rather than assumed.** Its disproof condition was a verb
that only makes sense with a cursor, a selection or a mode. Five verbs later,
none appeared: every operation edit mode needs is expressible as a name and
arguments, so the modal shell can bind keys to verbs that already exist rather
than the verbs being shaped by keybindings.

**Splitting on `&&` is not a parser**, which was the goal's own scope test.
No quoting, nesting or precedence was needed, so the seam has not moved.

## What is NOT proved — read this before citing it

- **There is no modal shell.** No cursor, no keys, no live re-render, no
  submit-on-keystroke. `goal:g13.1` is a modal editor and this is its verb
  layer. Half.
- **No human has used it.** Tests, plus one `--dry-run` against a real node.
  Nothing has been submitted to the live corpus through this path.
- **`thought_session` is written but not linked.** It stores whatever string a
  caller passes; nothing connects it to a session transcript, which is
  `goal:g2.7`'s actual ask. The field is no longer dead — it is not yet
  provenance.
- **The `note` verb is the only body operation.** Dropping to `$EDITOR` is
  named in the goal as legitimate and is not implemented.

## The finding that outlived the feature

The full suite went red on a test that **passed in isolation and in file
order**. The first cause was a leaked monkeypatch in code written one iteration
earlier; fixing it was not enough. `test_completion.py` and
`test_evidence_gate.py` load engine modules by path and reassign
`sys.modules[name]`, so **`node_writer` is not one object once the whole suite
runs in one process** — the test patched its imported name while `write.py`
called through a different module.

The durable rule: **patch the object the caller actually calls through, not a
name that happens to resolve to it.** And a failure visible only in full-suite
order is the worst kind, because both narrower runs are green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The proof here is a NEGATIVE result and that is what makes it worth anything:
the hypothesis predicted no cursor-shaped verb would appear, and none did.
Had one appeared, the honest verdict would have been that the shell should
lead. Stating the disproof condition in advance is the only reason this
verdict is more than a description of what got built.

Confidence 0.9 rather than higher because five verbs is a small sample of the
operations a real editing session wants. The prediction survives what was
built; a sixth verb could still be the one that needs a mode.

The sys.modules finding is in the verdict rather than only the experiment
because it is not about edit mode at all — it is about this test suite, it
will recur, and a verdict is what gets read.
<!-- THOUGHT:END -->