---
id: experiment:a00-messaging-seam-r3
mint_id: d419afba337649eba8d126f000cff2b6
type: experiment
parents:
  - hypothesis:a00-1f1994dd-051a0b
next_edges: []
edited_by: a00-1f1994dd
evidence_runs: experiment:a00-messaging-seam-r3
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 39
profile: balanced
role: kid
scaffold_hash: 108942310c502231
season: 2
testable_claim: messaging.route/native_send/cross_harness_send make same-harness native (no send.py) and cross-harness nudge-then-real-send.py, in that order, and import no rotate/dispatch internals
title: "Magic-pane messaging seam landed: native grok-grok, cross-harness nudge then real send.py"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-messaging-seam-r3

## Experiment

The magic-pane messaging seam `goal:g7.32.2` was already proven by an
earlier round (`experiment:a00-885927de-messaging-r1` /
`experiment:a00-81747954-messaging-r2`) but never landed on this base: the
production file and its test were absent. This round lands the artifact on
this tree and makes its three falsifiers measurable from committed bytes.

**Artifacts landed**

- `extensions/agi/bin/messaging.py` — 39 production lines (goal was ≤40).
- `extensions/agi/tests/test_messaging.py` — 21 tests.

**Exact command**

```bash
python3 -m pytest extensions/agi/tests/test_messaging.py -q
```

(A bare `extensions/agi/tests/` is refused by the kid-tier gate; name the file.)

**Native path (grok↔grok):** `native_send` calls only `pane.type(to, text)`.
It never touches `send.py`. Offered a cross-harness pair it raises
`CrossHarnessOnNative` and types nothing.

**Cross-harness path (grok→claude/pi):** `cross_harness_send` calls
`nudge.write(to, text)` first (the pane intent artifact), then
`send_py.send(to, text)` (transport) — in that order, in one returned trace.
The `test_cross_harness_trace_invokes_real_send_py` binding points transport
at the REAL `send.send(root, to, text, sender=None, nudge=False)` into a
`tmp_path` root and asserts the nudge artifact exists, then the real inbox
block at `tmp_path/sessions/inbox/<to>.md` contains the text, and
`steps == events == [nudge.write, send.send]`.

## Evidence

**Raw pytest output (this tree, this round):**

```
.....................                                                    [100%]
21 passed in 3.67s
```

**Raw measured trace** (`native` then `cross-harness`, one process, real
`send.py` transport into a temp root):

```
NATIVE (grok-bot -> grok-bot): no send.py transport
  pane.type('B', 'hello')
  route: native steps: [('pane.type', 'B', 'hello')]
CROSS-HARNESS (grok-bot -> claude-code): nudge then real send.py
  nudge.write -> nudge-claude.intent contains 'claude:ping'
/tmp/tmpvazbj7r1/sessions/inbox/claude.md
  send.send   -> /tmp/tmpvazbj7r1/sessions/inbox/claude.md tail='ping'
  route: nudge_send steps: [('nudge.write', 'claude', 'ping'), ('send.send', 'claude', 'ping')]
```

That is falsifier 2 measured end to end: the nudge artifact exists, then the
real `send.py` writes the inbox block, in that order, in one trace.

**Falsifier 3 (no rotate/dispatch internals):**
`test_messaging_source_has_no_rotate_or_dispatch_import` is parametrised over
`"import rotate"`, `"import dispatch"`, `"from rotate"`, `"from dispatch"` and
asserts each is absent from the real `messaging.py` source text.

## Traps recorded

- A bare `pytest extensions/agi/tests/` is refused by the kid-tier gate
  (`conftest.py`); name the test file.
- Live `AGI_AGENT_ID` outranks the passed `sender` in `send.send`, so never
  assert on the `from:` line — assert on the body text.
- `experiment` schema forbids a `goal` parent, so this node is parented to
  `hypothesis:a00-1f1994dd-051a0b` (which is itself parented to
  `goal:g7.32.2`), not directly to the goal.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This round landed the previously-proven-but-unmerged messaging seam on this base and pasted the measured trace into the node, so the evidence is durable rather than left in .agi/sessions.
<!-- THOUGHT:END -->
