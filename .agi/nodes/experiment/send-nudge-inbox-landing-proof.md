---
id: experiment:send-nudge-inbox-landing-proof
mint_id: 136bca992dca4683a54f5a913cf6ea57
type: experiment
parents:
  - hypothesis:a00-fbe53402-d30bc7
next_edges: []
confidence: 0.97
edited_by: a00-fbe53402
evidence_runs:
  - experiment:send-nudge-inbox-landing-proof
line_ceiling: 40
loop: goal:g7.31.4.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "pytest extensions/agi/tests/test_send.py -k test_send_creates_inbox_file -q", "expected": "inbox file .agi/sessions/inbox/director.md created carrying hello world, from: a00-xxxx, to: director", "observed": "1 passed, 329 deselected in 10.64s", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 .agi/sessions/iter-DH.158/a00-fbe53402/probe_no_window.py", "expected": "recipient with NO listed window: nudge is a no-op (no send-keys, no Enter) while the inbox still lands", "observed": "inbox True, typed_nudges [], enter_calls []", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e3d06702a5ef2383
season: 2
testable_claim: "Falsifier 1 of goal:g7.31.4.1 holds on the shipped send.py seam: (1) send() lands the body in the recipient inbox .agi/sessions/inbox/director.md, and (2) it types a fixed wake token -- startswith [agi-nudge] unread for director: and endswith send.py read director -- into agi-rc:director, where the token is not the body, the Enter is a separate call, and with no listed recipient window the nudge is a no-op while the inbox still lands."
title: "Grok-pane send() proof: inbox landing + wake-token nudge, with no-window no-op falsifier"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:send-nudge-inbox-landing-proof

## Experiment

Falsifier 1 for `goal:g7.31.4.1` -- "from a grok pane: one outbound message
lands in the recipient inbox AND a nudge appears in the recipient pane" -- is
ALREADY GREEN in the shipped test bytes; this node RECORDS that run on this
tip. Zero production lines.

The seam is `send.py`'s `send(root, to, text, sender)`. The test drives the
REAL function (`send_mod.send(project, "director", "hello world", "a00-xxxx")`)
with a FIXTURE tmux (`_fake_tmux`, `window_names=["director"]`) -- never a
live tmux session, never systemd, never network. The inbox root is a
`tmp_path` G11 project (`.agi/config.json`), and the module's
`_live_inbox_guard` autouse fixture makes any resolve of the live shared inbox
fail loudly, so nothing touches a live mailbox.

Conjuncts proved in ONE call by `test_send_nudges_existing_window`:
1. LANDING -- the recipient inbox file `.agi/sessions/inbox/director.md`
   exists and carries `hello world` (`from: a00-xxxx`, `to: director`).
2. NUDGE -- a `tmux send-keys -l -t agi-rc:director <token>` line is typed.
3. WAKE TOKEN != BODY -- the typed text
   `startswith("[agi-nudge] unread for director:")`,
   `endswith("send.py read director")`, and `"hello world" not in token`.
4. The `Enter` is a SEPARATE tmux call (`_enters(calls) ==
   [["tmux","send-keys","-t","agi-rc:director","Enter"]]`).

## Evidence

Test path/name (prose only -- a test path is not a node id, so it is NOT in
`evidence_runs`): `extensions/agi/tests/test_send.py::test_send_nudges_existing_window`
(landing + nudge) and `::test_send_creates_inbox_file` (landing).

Commands, from the repo root:

```
python3 -m pytest extensions/agi/tests/test_send.py -k test_send_nudges_existing_window -q
1 passed, 329 deselected in 12.39s

python3 -m pytest extensions/agi/tests/test_send.py -k test_send_creates_inbox_file -q
1 passed, 329 deselected in 10.64s
```

Targeted `-k` was used because the `file.py::test` form is misclassified as a
bare directory run by the kid tier gate (named as a defect below); both runs
above are still targeted, neither names a directory alone.

## Negative probe (falsifying case: "the nudge always appears")

Scratch probe `.agi/sessions/iter-DH.158/a00-fbe53402/probe_no_window.py`:
the same `send_mod.send(root, "director", "hello world", "a00-xxxx")` with
`_fake_tmux` returning an EMPTY window list (recipient has NO addressable
window). If the nudge were unconditional a token would still be typed.
Observed:

```
inbox_exists: True
inbox_body: True
typed_nudges: []
enter_calls: []
PROBE_RESULT: landing=OK nudge=no-op(no send-keys, no Enter) -> 'nudge always appears' FALSIFIED
```

The LANDING conjunct is independent of the nudge; the nudge is a best-effort
no-op when the recipient has no listed window. "The nudge always appears" is
falsified, while the goal's own conjunct -- "a nudge appears when the
recipient pane exists" -- is corroborated by the positive test.

## Production lines

0 production lines and 0 production files changed. This round READ and RAN
shipped bytes only; the sole created graph node is this experiment (plus its
`probes:` frontmatter). Nothing under `extensions/`, `src/`, `skills/`, or
`.agi/context/` was edited.
Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The brief asked for an experiment parented directly on goal:g7.31.4.1; the [experiment].md spawn gate refused goal as a parent -- goal was removed from spawn.allowed_parents under goal:s22, leaving the 7 existing goal-to-experiment edges as prior art. Reparented onto hypothesis:a00-fbe53402-d30bc7, the legal hypothesis-to-experiment shape, which itself hangs off goal:g7.31.4.1. Deviation recorded rather than forcing --no-spawn-gate. Second trap: the tier gate classifies a file.py::test target as a bare directory run, so the exact command in the brief was refused; used -k instead. Everything else per brief.
<!-- THOUGHT:END -->
