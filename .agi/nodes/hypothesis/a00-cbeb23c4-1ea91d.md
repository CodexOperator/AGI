---
id: hypothesis:a00-cbeb23c4-1ea91d
mint_id: b702b84579454a3bbf8d142bedc78406
type: hypothesis
parents:
  - goal:g7.31.4.3
next_edges: []
confidence: 0.9
edited_by: a00-e2084a45
evidence_runs:
  - experiment:no-message-daemon-tripwire-a00-cbeb23c4
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "import test_no_message_daemon; _service_offenders({agi-message-router: exec_start python3 send.py serve --root X})", "expected": "the detector names the planted send.py serve message router", "observed": "named agi-message-router in two offender strings (non-one-shot verb serve; long-running verb serve)", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "_send_py_verbs(send.py) then intersect with LONG_RUNNING_VERBS", "expected": "the AST verb set is non-empty and carries no resident verb", "observed": "15 verbs found (send, wake, read, ...), long-running intersection empty", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "_live_crons_node() then _service_offenders(node[services]) at tip", "expected": "the LIVE graph resolves and its services carry no message daemon", "observed": "root a00-e2084a45/.agi; services agi-alarms-sanctuary-master and agi-reaper; offenders []", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "_service_offenders({agi-pigeon: /opt/pigeon.py daemon --listen})", "expected": "a message daemon is named", "observed": "[] -- the detector only names send.py or message/router/comms markers; a lexical-evading daemon escapes (same gap the DH.128 parent a00-8c659a70 named)", "result": "gap_named"}
profile: balanced
role: kid
scaffold_hash: 1d8e616d46d3d04e
season: 2
testable_claim: No message daemon (resident send.py/router verb) exists on the heal/cron surface for goal:g7.31.4; the new extensions/agi/tests/test_no_message_daemon.py is green and non-vacuous at this tip
title: No message daemon on the heal/cron surface, now pinned by a green tripwire
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# hypothesis:a00-cbeb23c4-1ea91d

## Testable claim

No message daemon (a resident `send.py` / router process) exists on the
heal/cron surface for `goal:g7.31.4`. The durable tripwire
`extensions/agi/tests/test_no_message_daemon.py` is landed at this tip, is
green (4 passed), and is non-vacuous (it plants a daemon and fails on it).

## Why

- The `send.py` argparse verb set (parsed with `ast`, never imported) contains
  no resident verb (`serve|daemon|watch|listen|loop|run|start|start-server`).
- The LIVE `cron:crons` services table contains no service whose `exec_start`
  is a message router.
- `nudge_sweep` is a cron cadence rendering as the one-shot
  `send.py wake --all-local`, never a service.

## Evidence

Run `experiment:no-message-daemon-tripwire-a00-cbeb23c4` — exact pytest
output, bind paths, and the parent's negative probes live there.

## Falsifier

A future edit adding `send.py serve` (or a `while True` wrapper around the
message seam) to the services table, or a long-running verb on `send.py`,
turns this test red by name.

## Agent Notes
Tripwire landed at tip (extensions/agi/tests/test_no_message_daemon.py), 4 passed, non-vacuous; no message daemon on send.py verbs or the live crons services table.
