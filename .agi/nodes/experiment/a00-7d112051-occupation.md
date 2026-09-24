---
id: experiment:a00-7d112051-occupation
type: experiment
parents:
  - hypothesis:a00-7d112051-46748a
edited_by: a00-7d112051
line_ceiling: 40
production_lines: 10
---
# Persistent supervisor exhaustion does not leave a false live occupation

Implemented the terminalization fix in `dispatch._supervise_persistent`: when the bounded restart loop ends with a dead child, the current `agent.json` is rewritten as `status: failed`, `pid: null`, `persistent: false`, with the exhaustion reason. Added a negative test covering four immediately-dead children and asserting the three-terminal-cell contract.

Ran `python3 -m pytest extensions/agi/tests/test_dispatch_persistent.py -q`: 4 passed (the run reports unrelated tier-gate phantom records). The existing live-restart test still proves the current pid and restart count while a child remains alive.
