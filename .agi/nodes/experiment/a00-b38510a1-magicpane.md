---
id: experiment:a00-b38510a1-magicpane
mint_id: 0e1440cb25314d3c8770c3d4b4f00e64
type: experiment
parents:
  - hypothesis:a00-b38510a1-e28c27
next_edges: []
edited_by: a00-b38510a1
evidence_runs: experiment:a00-b38510a1-magicpane
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 78
profile: balanced
role: kid
scaffold_hash: 616ad1065b75b5ed
season: 2
testable_claim: "three conjuncts: native grok-grok types into the pane with no send.py argv, cross grok-claude/pi writes the pane-nudge artifact then invokes send.py in one ordered trace, and import magic_pane pulls neither rotate nor dispatch"
thought_session: iter-DH.149
title: "magic_pane two-route trace: native pane vs nudge artifact then send.py"
town: core
---
# experiment:a00-b38510a1-magicpane

## Experiment

Build order (`hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement`):
built the seam, then measured it. One new production file
`extensions/agi/bin/magic_pane.py` (78 lines added; ceiling 40, under the 2x
stop of 80) plus `extensions/agi/tests/test_magic_pane.py`.

`send_message(root, to, text, dest_harness, ...)` routes on the destination
harness family. `NATIVE_HARNESSES = frozenset({"grok"})` is data;
`choose_route` is one lookup, no `if harness == "grok"` soup. Native re-uses
send.py's measured send-keys shape but owns its own `subprocess.run` (never
imports or shells out to send.py). Cross writes
`sessions/comms/pane-nudge/<seat>.nudge` then runs
`[python3, send.py, "send", to, text, "--from", sender]`.

## Evidence

Probe: `.agi/sessions/iter-DH.149/a00-b38510a1/pane_trace.py` (full bytes in
`trace.txt`). All three conjuncts captured:

CONJUNCT 1 (native grok->grok):
```
route: native
argv: tmux send-keys -l -t agi-rc:grok-b hi there
argv: tmux send-keys -t agi-rc:grok-b Enter
send.py in any argv: False
```
No artifact written; grep of the source finds no `import send`.

CONJUNCT 2 (cross grok->claude, artifact then send.py):
```
route: cross
artifact path: /tmp/.../.agi/sessions/comms/pane-nudge/dest-b.nudge
artifact bytes: {"to": "dest-b", "harness": "claude", "from": "grok-a", "route": "cross"}
artifact_exists_at_invoke: True
argv: ['/usr/bin/python3', '.../extensions/agi/bin/send.py', 'send', 'dest-b', 'hello', '--from', 'grok-a']
returncode: 0
```
The fake send.py seam checks the artifact's presence at invoke time, so the
one trace proves order, not just co-occurrence.

CONJUNCT 3 (import graph):
```
forbidden loaded: [] rc 0
```
Fresh interpreter: `import magic_pane` leaves neither `rotate` nor `dispatch`
in `sys.modules`; source grep finds no import of either. The `send.py` import
check is line-anchored (`^\s*(?:import|from)\s+send\b`) so docstring prose
about send.py cannot false-positive.

Tests (named explicitly):
```
python3 -m pytest extensions/agi/tests/test_magic_pane.py -q
-> 5 passed
```
