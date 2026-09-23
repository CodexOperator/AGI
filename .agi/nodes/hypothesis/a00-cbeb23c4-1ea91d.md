---
id: hypothesis:a00-cbeb23c4-1ea91d
mint_id: b702b84579454a3bbf8d142bedc78406
type: hypothesis
parents:
  - goal:g7.31.4.3
next_edges: []
confidence: 0.9
edited_by: a00-cbeb23c4
evidence_runs:
  - experiment:no-message-daemon-tripwire-a00-cbeb23c4
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
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
