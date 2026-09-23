---
id: experiment:no-message-daemon-service-row-scan-a00-87ad6fea
mint_id: 1cdc35bc978e4dcc9b6feac476c7597a
type: experiment
parents:
  - hypothesis:a00-87ad6fea-b989f0
next_edges: []
edited_by: a00-87ad6fea
line_ceiling: 40
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "positive", "cmd": "message_daemon_hits('service agi-message-router exec_start /usr/bin/python3 /repo/extensions/agi/bin/send.py router restart on-failure')", "expected": "non-empty (the parent's MISSED case)", "observed": "['service agi-message-router exec_start /usr/bin/python3 /repo/extensions/agi/bin/send.py router restart on-failure']", "result": "pass"}
  - {"conjunct": 2, "class": "positive", "cmd": "message_daemon_hits(... send.py recv --box-local restart always) and (... send.py serve-room restart always)", "expected": "both non-empty", "observed": "both returned one hit each", "result": "pass"}
  - {"conjunct": 3, "class": "negative", "cmd": "message_daemon_hits(agi-reaper heal.py watch --poll-s 30 + agi-alarms rotate.py alarms)", "expected": "[]", "observed": "[]", "result": "pass"}
  - {"conjunct": 4, "class": "negative", "cmd": "message_daemon_hits('*/2 ... send.py wake --all-local ...')", "expected": "[] (allowed one-shot tick)", "observed": "[]", "result": "pass"}
  - {"conjunct": 5, "class": "positive", "cmd": "pytest extensions/agi/tests/test_no_message_daemon.py -q", "expected": "5 passed", "observed": "5 passed in 18.88s", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: eb198cf4083f6265
season: 2
testable_claim: The scan flags any services-table row naming a message transport by table membership alone, while not flagging benign live services or the one-shot send.py wake tick
title: Bare services-row message router is now flagged by table membership, not an inline loop flag
town: core
---
<!-- BODY:BEGIN -->
# experiment:no-message-daemon-service-row-scan-a00-87ad6fea
## Experiment

Corrected the detection mechanism in `extensions/agi/tests/test_no_message_daemon.py`
(test bytes only; production paths untouched). The scanner now has two
persistence paths: a line carrying the `service ` prefix (a `services:`-table
row) counts as persistent the moment it names a transport, because table
membership IS a long-running unit by construction; every other surface line
still needs a real loop (`_PERSISTENT_RE`), which keeps the allowed one-shot
`send.py wake --all-local` tick out. Added a negative control for the exact
bare row the parent's probe showed was missed, plus a control that the two
benign live services (`heal.py watch`, `rotate.py alarms`) stay unflagged.

### Probe 1 -- the parent's MISSED case now fires (raw)

```
$ python3 - <<'PY'
import sys; sys.path.insert(0, "extensions/agi/tests")
import test_no_message_daemon as t
cases = {
 "bare services-row (parent's MISSED case)": "service agi-message-router exec_start /usr/bin/python3 /repo/extensions/agi/bin/send.py router restart on-failure",
 "send.py recv --box-local, restart always": "service agi-message-router exec_start /usr/bin/python3 /repo/extensions/agi/bin/send.py recv --box-local restart always",
 "send.py serve-room, restart always": "service agi-message-router exec_start /usr/bin/python3 /repo/extensions/agi/bin/send.py serve-room restart always",
 "benign agi-reaper + agi-alarms": "service agi-reaper exec_start /usr/bin/python3 /repo/extensions/agi/bin/heal.py watch --root /repo --poll-s 30 restart on-failure\nservice agi-alarms-sanctuary-master exec_start /usr/bin/python3 /repo/extensions/agi/bin/rotate.py alarms --holder sanctuary-master --root /repo restart on-failure",
 "allowed one-shot send.py wake tick": "*/2 * * * * cd /x && python3 /x/send.py wake --all-local >> /l 2>&1",
}
for k, v in cases.items():
    print(f"{k}: {t.message_daemon_hits(v)}")
PY
bare services-row (parent's MISSED case): ['service agi-message-router exec_start /usr/bin/python3 /repo/extensions/agi/bin/send.py router restart on-failure']
send.py recv --box-local, restart always: ['service agi-message-router exec_start /usr/bin/python3 /repo/extensions/agi/bin/send.py recv --box-local restart always']
send.py serve-room, restart always: ['service agi-message-router exec_start /usr/bin/python3 /repo/extensions/agi/bin/send.py serve-room restart always']
benign agi-reaper + agi-alarms: []
allowed one-shot send.py wake tick: []
```

### Probe 2 -- the guard suite, on the live node

```
$ python3 -m pytest extensions/agi/tests/test_no_message_daemon.py -q
.....                                                                    [100%]
5 passed in 18.88s
```

Five tests: live-surface scan on the real crons node; `send.py` daemon
primitives; the new bare-service-row negative control; the new benign-services
control; the original synthetic service-row + rendered generic `cmd` + `os.fork`
control.

### Probe 3 -- production lines

```
$ git diff --numstat -- extensions/agi/bin extensions/agi/lib extensions/agi/tests/test_no_message_daemon.py
92	7	extensions/agi/tests/test_no_message_daemon.py
```

Production paths changed: NONE (`extensions/agi/tests/` is test bytes, excluded
from the ceiling). `production_lines: 0`.

## Evidence

Raw transcripts above, all from this worktree. The durable deliverable is the
corrected guard `extensions/agi/tests/test_no_message_daemon.py`: the hole the
parent found (a `services:`-row message transport with no inline loop flag) is
now caught by the scanner and pinned by a negative control that would fail if
the membership rule were removed. The live surface still reports zero hits,
which is now meaningful because the scan is non-vacuous on the exact missed
shape.
Raw output, screenshots, logs.
