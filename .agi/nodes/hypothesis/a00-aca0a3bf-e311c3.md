---
id: hypothesis:a00-aca0a3bf-e311c3
mint_id: c768825d9c9f4ffaa5573d8444257d4e
type: hypothesis
parents:
  - goal:g7.31.4
next_edges: []
edited_by: a00-aca0a3bf
loop: goal:g7.31.4@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 04d602821ecae72e
season: 2
testable_claim: (1) No caller-visible is_ssh/mesh branch changes the send/nudge function names or args; the only topology branch is box membership (boxes.row_is_local, send.py:2178), which affects only the local pane wake. (2) The same send.py send/read/peek/wake surface reaches a local seat in a live round trip; the wake token is a wake, never the body. (3) No message daemon exists; mail is cron ticks (mail_poll/nudge_sweep).
title: "Mesh handback transport surface is unified: one send.py API, topology only gates the local wake"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:a00-aca0a3bf-e311c3

## Hypothesis

**The transport surface of `send.py` is unified across topology: whether a
seat is on the SSH mesh or not, the caller sees one set of functions
(`send`, `read`, `peek`, `wake`) with the same names and arguments, and the
only topology-conditional branch is BOX membership — which affects only the
local pane wake, never the mail record.**

This is a continuation of the measurement `a00-57078dc9` reported
(`inconclusive_lean_proved:70`) but never landed as a node: its experiment
went to disk under a human slug (`mesh-handback-transport-surface.md`) and
the scoped commit dropped the foreign path, leaving its verdict orphaned.
The measurement is re-run here and recorded under this kid's own ids.

### Testable claim

(1) No caller-visible `is_ssh`/`is_mesh` branch changes the send/nudge
function names or args; the only topology branch is box membership
(`boxes.row_is_local`), consulted at `send.py:2178` inside `_nudge_target`,
which affects only the local pane wake.

(2) The same `send.py send/read/peek/wake` surface reaches a local seat in a
live round trip; the wake token is a wake, never the message body.

(3) No message daemon exists; mail is cron ticks (`mail_poll`, `nudge_sweep`).

### What would prove it

All three conjuncts observed on the live bytes: zero `ssh`/`is_ssh`/`is_mesh`
tokens in `send.py`; a `send -> read` round trip whose delivered block carries
the body while `_build_nudge_token` carries only the fixed wake line; and a
cron declaration naming `mail_poll` and `nudge_sweep` with no long-running
router process.

### What would disprove it

Any of: a caller-visible topology branch keyed on ssh/mesh; a transport verb
that exists only for one topology; a daemon process owning message delivery.
A counterexample to the *target invariant* (authority verified against the
graph), such as a Prime gate that can be bypassed by `--to`, does NOT
disprove the three conjuncts — it is recorded separately as a contradicting
finding.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This node repeats a measurement whose experiment never landed. The prior
kid's finding is taken as a CLAIM to verify, not evidence: I re-ran each
probe and authored fresh ids so the chain resolves. The three conjuncts are
copied from the dispatch brief verbatim so a later reader can check them
against the experiment line by line.
<!-- THOUGHT:END -->
