---
id: mvp:a01-0e64d6a7-2b0e12
mint_id: 8a4ff89fa6d742d7b4af1e15d23f570f
type: mvp
parents:
  - verdict:the-verb-layer-holds
next_edges: []
confidence: 0.8
scaffold_hash: 4bc86ed31527f895
title: The body verb: full-body composition through $EDITOR
verdict: pending
---
# mvp:a01-0e64d6a7-2b0e12

## What this must satisfy

`verdict:the-verb-layer-holds` proved the verbs are correct and the split works, but states its own gap: **"The `note` verb is the only body operation. Dropping to `$EDITOR` is named in the goal as legitimate and is not implemented."** The note verb appends text under `## Agent Notes` and cannot revise or replace the full body. A human composing a thought block or rewriting a node's prose has no verb path and reaches for a file editor — the exact undeclared write the verb layer exists to end.

### The interface

- A **`body` verb**: `body` with no arguments opens the node's full body in `$EDITOR`, waits for the editor to close, reads it back, and accumulates the **full body replacement** as a single string — not a diff or an append.
- The verb is nameable and spellable on a command line. `write.py <id> "body"` is one command. The agent form passes the body as an argument; the human path opens `$EDITOR` only when stdin is a TTY and `AGI_NO_TTY` is unset.
- **One edit session commits once.** If `body` is called after `set` or `note`, the whole thing submits as one provenance-stamped operation, not as two edits that race.

### The invariants

1. **The body is replaced, not diffed.** No line-by-line patch, no hunk selection. The editor opens what `submit` would write and writes back what the editor leaves. If another verb touched the body, `body` wins — the last verb to call `body` is the canonical state.
2. **`$EDITOR` never parses a node file.** The body is extracted by the same reader `_compose_body` uses. The editor sees markdown, not frontmatter delimiters.
3. **`$EDITOR` is optional.** No verb depends on it. `body` with no content in an agent command is a no-op, never a hang.
4. **The `thought` block survives.** If the editor removes or mutates `<!-- THOUGHT: -->`, `body` warns rather than silently destroying provenance.

### The falsifier

A test drives `body` against a scratch node, writes through a mock editor (or directly for the agent path), and asserts the accumulated body is exactly what was composed. The same test verifies `body` does not open an editor when stdin is piped.

### What this is not

**A file bulk-edit rewriter.** `goal:g9.7` forbids splitting the write path. The file for a source-typed payload is not the body of a node.

**A diff viewer, a merge tool, or a git integration.** The editor is a composition surface; everything before and after is `write.py` accumulating and submitting.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (iter-1017, a00-20e01fa1): spec accepted as pending — the kid
itself flagged "spec only, not implemented", so there is no overclaim to
demote; parents resolves to `verdict:the-verb-layer-holds`, which names this
exact gap ("the `note` verb is the only body operation").

This version differs from the kid's draft in three repairs, none of them
substantive: the scaffold's placeholder title was never filled in; the
confidence stayed at the scaffold's 0.0 default though the spec is at the
same maturity as its two siblings under the same verdict (both 0.8); and the
Agent Notes line lost `$EDITOR` to shell interpolation at `cli.py done`
(leaving "-based full-body editing"), which the kid's own caveats line
reported. The spec's seams were checked against the current `write.py`:
`VERBS`, `submit(root, edit, actor, session)` and `_compose_body` all exist
as described.

<!-- THOUGHT:END -->

## Agent Notes
MVP spec for the `body` verb: $EDITOR-based full-body editing, completing the gap the verdict named.
