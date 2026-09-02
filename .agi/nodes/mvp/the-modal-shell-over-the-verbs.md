---
id: mvp:the-modal-shell-over-the-verbs
mint_id: 3e9177c585e444e39c55e526f527d266
type: mvp
title: The modal shell binds keys to verbs that already exist
parents:
  - verdict:the-verb-layer-holds
next_edges: []
scaffold_hash: f4b9ab2242b6109e
status: open
confidence: 0.8
---

# mvp:the-modal-shell-over-the-verbs

## What this must satisfy

`verdict:the-verb-layer-holds` proved the build order was right and states its
own gap plainly: **there is no modal shell.** No cursor, no keys, no live
re-render, no submit-on-keystroke. `goal:g13.1` is a modal editor and what
exists is its verb layer.

### The interfaces

- A **keymap as data** — key to verb name — so the binding is inspectable and
  a test can assert every key resolves to a verb that exists. A keystroke
  bound to nothing is the split `goal:g13.1` forbids, arriving from the other
  direction.
- A **headless driver**: `drive(keys, node_id)` returning the accumulated
  `Edit`. That is what makes the shell testable without a TTY, and it is the
  same accumulate-then-submit path the `&&` form already uses.
- The **renderer is `viewport.py`'s**, called, never copied. `goal:g13.1`:
  *"relies on the renderer and the writer to do everything in the background"*.

### The invariants

1. **The viewport must never gain a write path.** `goal:g9`'s reader-only
   invariant, currently enforced by a test that inspects `viewport.py`. Edit
   mode may *call* the renderer; the renderer may not learn to write.
2. **Every key maps to a nameable verb, and every verb is reachable by name.**
   Both directions, or the two callers have diverged.
3. **One submit per session.** The shell accumulates exactly as the serial
   form does; nothing writes until submit.
4. **No new parser.** `goal:g13.1`'s own scope test — if edit mode needs its
   own parser or its own file-writing code, the seam is wrong.

### The falsifier

Drive the headless driver with a key sequence and the equivalent `&&` script;
both produce an identical `Edit` and an identical resulting node. A test
asserts the keymap and `VERBS` are in bijection. `viewport.py` still passes
its reader-only check. A human runs the shell against a scratch node and
submits one change with provenance recorded.

### What is still not this

**`thought_session` is written but not linked.** It stores whatever string a
caller passes; nothing connects it to a session transcript, which is
`goal:g2.7`/`goal:g10.1`'s actual ask and the finest grain of the LOD axis.
The shell will make it easy to pass a real session id and will not, by itself,
make one exist.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted at the end of the session that built the verb layer, from that
verdict's own first limit, so the graph records where this stopped rather than
leaving it in a handoff the next director deletes by default.

The headless driver is the design decision worth arguing with. A modal shell
is the least testable thing in this repo, and the way to keep it honest is to
make the interactive loop a thin adapter over something that can be driven
without a terminal. If that turns out to be awkward, it is evidence the keymap
is carrying state the verbs should own.

Invariant 1 is restated here even though `viewport.py` already enforces it,
because this is the first time anything write-shaped will sit next to the
renderer and call into it. The temptation to let the viewport do "just one"
write arrives exactly here.
<!-- THOUGHT:END -->
