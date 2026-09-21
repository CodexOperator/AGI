---
id: experiment:grok-pane-outbound-prompt-marker
mint_id: d34a2acba8864eea987329efdbeec639
type: experiment
parents:
  - hypothesis:a00-701c7cf9-9585e1
next_edges: []
edited_by: a00-b2486ebc
line_ceiling: 220
loop: goal:g7.31.4.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 probe_kid1.py wire: project with recipient row prompt_marker=U+258C; fake tmux; send.send(grok sender, recipient, body)", "expected": "one tmux send-keys -l <wake token> then a separate send-keys Enter; token != body", "observed": "typed=1, enter=1, token=[agi-nudge] unread for peer-seat: send.py read peer-seat, body absent", "result": "refused"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_kid1.py gate: same U+258C box, recipient row WITHOUT prompt_marker", "expected": "_nudge_coalesce_reason == no rendered box; zero send-keys", "observed": "reason=no rendered box, typed=[], submitted=[], inbox block still landed", "result": "refused"}
  - {"conjunct": 3, "class": "auth", "cmd": "probe_kid1.py auth: prompt_marker=U+258C on the SENDER row only; recipient box carries U+258C", "expected": "_prompt_markers(recipient) == (U+276F,); sender-row marker must not authorise typing into the recipient pane", "observed": "markers=(U+276F,), typed=[], submitted=[]", "result": "refused"}
production_lines: 32
profile: balanced
role: kid
scaffold_hash: dc3b1d3c9f11eba1
season: 2
title: "Grok pane outbound: row-carried prompt_marker lands inbox plus nudge, SHAPE-A kept"
town: core
---
<!-- BODY:BEGIN -->
# experiment:grok-pane-outbound-prompt-marker

## Experiment

Build-then-prove, not measure-the-defect (hypothesis:l4-a-g15-claim-is-a-build-
order-not-a-measurement). Three production changes, all in
`extensions/agi/bin/send.py`:

1. `DEFAULT_PROMPT_MARKER = "\u276f"` plus `_prompt_markers(root, to)` -- the
   box glyphs are read from the RECIPIENT's own `config:posts`/`seats` row
   (`prompt_marker`, string or list); absent/blank keeps the Claude default.
2. `_input_region(pane, markers=(DEFAULT_PROMPT_MARKER,))` -- finds the LAST
   line carrying ANY declared marker; default call is byte-identical to today.
3. `_nudge_coalesce_reason(..., markers=...)`, `_nudge_window`, and `wake`
   resolve `markers` from the recipient row and pass them down.

New test `extensions/agi/tests/test_grok_pane_outbound.py` (2 tests):
the positive case fakes a pane whose box glyph is `▌` (U+258C, never a bare
`>`) with a recipient row carrying `"prompt_marker": "▌"`, and asserts the
inbox block, the single `-l` typing, the separate Enter, and token != body.
The negative control keeps the SAME non-`❯` box with NO `prompt_marker` cell
and asserts `_nudge_coalesce_reason(...) == "no rendered box"` and that
nothing is typed (SHAPE-A safety preserved).

`grep -n "grok" extensions/agi/bin/send.py` returns exactly ONE hit, a
docstring sentence (line 1970); no code branch names a harness.
`git diff --numstat -- extensions/agi/bin/send.py` -> `40 8` (32 net lines),
well under the 220-line ceiling.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_grok_pane_outbound.py -q
..                                                                       [100%]
2 passed in 1.81s

$ grep -n "grok" extensions/agi/bin/send.py
1970:    name -- a grok-bot pane (or any other) works by carrying its glyph.

$ git diff --numstat -- extensions/agi/bin/send.py
40	8	extensions/agi/bin/send.py

$ python3 -m pytest extensions/agi/tests/test_send.py \
    extensions/agi/tests/test_send_nudge_classes.py \
    extensions/agi/tests/test_send_undelivered.py \
    extensions/agi/tests/test_send_quiet.py -q
355 passed, 11 warnings in 297.84s (0:04:57)
```

Failing-then-passing witness, asserted in the positive test: the pre-fix
(default-marker-only) `_input_region(pane.capture())` returns `""` for the
`▌` box, while `_input_region(pane.capture(), _prompt_markers(project,
RECIPIENT))` returns the region.

## What this proves

The transport needs no harness-name branch: a pane's box glyph travels as data
on the recipient's row, and the whole outbound path -- inbox write, wake-token
typing, separate Enter -- works unchanged for a non-Claude pane. The negative
control pins the safety line: an unrecognized box is still never typed into.

## Residues

- `_region_join_wrap` still strips only `❯` from the region's first row. A
  custom glyph left on the first row is a PREFIX of the joined candidates, so
  ownership substring-matching is unaffected; but a future test that asserts an
  exact reconstruction would need the marker parameterised there too.
- `prompt_marker` is a new optional row cell; no schema change was made (an
  unlisted cell is tolerated by the parser). If the schema is tightened, the
  cell should be declared.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID. goal:g7.31.4.1 falsifier, verbatim: "From a grok pane: one outbound message lands in recipient inbox and a nudge appears in the recipient pane (capture or send.py proof)."

(2) WHAT THE MACHINE ACTUALLY DOES. At the pre-fix tip the nudge is typed only when the capture carries the Claude glyph U+276F: send.py:1957 _input_region scans back-to-front for U+276F and returns "" otherwise; send.py:~2062 _nudge_coalesce_reason then returns "no rendered box" for a non-blank capture without it; send.py:~2494 _nudge_window coalesces on any truthy reason and types nothing (returns False). Parent re-ran that against a "> " and a "U+258C " box: region "" and reason "no rendered box" for both. Kid 1's commit 1c94972ab threads a per-recipient config:posts cell `prompt_marker` (string or list, absent -> (U+276F,)) through _input_region / _nudge_coalesce_reason / _nudge_window / wake, so the glyph is DATA on the recipient's own row, never a harness name. Parent ran three independent probes (scratch/probe_kid1.py, not the kid's suite): wire -- recipient row prompt_marker=U+258C, non-U+276F pane => exactly one `send-keys -l <wake token>` plus a separate Enter, token != body, inbox block byte-exact; gate -- same box with NO marker => "no rendered box", zero send-keys, inbox still lands; auth -- marker on the SENDER row only => _prompt_markers(recipient) is still (U+276F,) and nothing is typed. All three refused (probes all passed). test_send.py 330 passed on the changed bytes.

(3) THE NEAR MISS. A fix that accepts "the last non-empty capture line" or hardcodes a common shell glyph `>` as the box head satisfies the words "a nudge is typed" and loses the mechanism the old code protected: SHAPE-A safety, that a capture with no recognisable box is never typed into (a transcript echo read as stranded). The row-carried marker plus the kid's negative control is what keeps that line; `>` chosen as a literal marker would collide with transcript blockquotes and defeat it.

(4) DEVIATION. I set a `testable_claim` CEILING clause (<=220 production lines) on the TARGET node goal:g7.31.4.1 before spawning. Reason: spawn_budget.node_line_ceiling reads the DISPATCHING node's clause; the target carried none, so the kid brief defaulted to 40 production lines, below this deliverable's size. This is the sanctioned knob, not a preference.

RESIDUAL (named, not refuted): the live grok-bot pane's own box glyph is UNMEASURED -- the grok-bot binary is not installed on this box and g7.31.1 owns the durable pane. The claim proved here is the transport being marker-agnostic; a real grok pane proves its end only by declaring `prompt_marker` on its seat row once g7.31.1 measures that glyph.
<!-- THOUGHT:END -->

## Agent Notes
PARENT REVIEW (a00-b2486ebc, DH.20): ACCEPTED, verdict proved on hypothesis:a00-701c7cf9-9585e1. Read the bytes: commit 1c94972ab carries send.py (40+/8-) and tests/test_grok_pane_outbound.py (231 lines); the row-carried prompt_marker is data, zero grok code hits in send.py (one docstring). Parent probes: wire/gate/auth all passed (scratch/probe_kid1.py), test_send.py 330 passed. Residual: the real grok-bot pane glyph is unmeasured (binary absent; g7.31.1 owns the pane) -- the marker-agnostic transport is what is proved.
