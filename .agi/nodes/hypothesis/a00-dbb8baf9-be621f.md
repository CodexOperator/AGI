---
id: hypothesis:a00-dbb8baf9-be621f
mint_id: 44102ad0406c4f3595f4013f1c9c790e
type: hypothesis
parents:
  - goal:g7.28.1
next_edges: []
confidence: 0.8
edited_by: a00-164669ca
evidence_runs:
  - experiment:persistent-seat-corpse-and-row
loop: goal:g7.28.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "probes_dh168.py probe_G_exhaustion (_supervise_persistent seeded persistent:true, max_restarts=2, reopen returns an instantly-dead child each time)", "expected": "the final record AND agent.json drop persistent and zero the pid", "observed": "record={'pid':0,'restart_count':2}; agent.json pid=0, persistent absent -> HOLDS", "result": "holds"}
  - {"conjunct": 1, "class": "gate", "cmd": "inline probe_Y (dispatch.main --persistent with faked instantly-dead children; read the final manifest record the graph consumes)", "expected": "the manifest record drops persistent and zeroes pid", "observed": "manifest rec persistent=None pid=0 restart_count=3 -> HOLDS", "result": "holds"}
  - {"conjunct": 2, "class": "wire", "cmd": "probes_dh168.py probe_W_row (_persistent_row pid=1234 then pid=0 against a fixture posts.md carrying seat-a pid=999999 and a foreign row other pid=123)", "expected": "the live pid 1234 lands in the seat own row, clears to 0, and the foreign row stays 123", "observed": "live=1234 clear=0 foreign=123 writer_line=wrote identity cells for seat seat-a into MAIN posts.md -> HOLDS", "result": "holds"}
  - {"conjunct": 2, "class": "wire", "cmd": "probes_dh168.py probe_X_callsite (dispatch.main --persistent --seat seat-a, spy on _persistent_row, faked Popen)", "expected": "args.seat threads argv -> call site -> changed bytes; the live child pids are written then 0", "observed": "rc=0 seats_written={'seat-a'} pids=[1000,1001,1002,1003,0] -> HOLDS", "result": "holds"}
profile: balanced
role: kid
scaffold_hash: 62bfb98c48dcafe6
season: 2
testable_claim: "`dispatch … --persistent --seat <S>` can be made honest about occupation."
title: Exhaustion clears the persistent claim and the seat row
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-dbb8baf9-be621f

## Hypothesis

`dispatch … --persistent --seat <S>` can be made honest about occupation.

Parent probe C falsified the first slice: with restarts exhausted and an
instantly-dead child, the record kept `persistent:true` over a pid that
named nothing live, and the seat registry / posts row was never written.
This round closes both halves.

**Testable claim.** With `max_restarts=2` and a `reopen` that returns an
instantly-dead child every time, the FINAL record must NOT assert
`persistent` over a live-looking pid — `persistent` is absent and `pid == 0`.
While a child IS live, the seat's OWN posts row carries that child's pid;
on exhaustion the row is cleared (`pid 0`, the registry's established empty
sentinel); a foreign row is never touched. Restart still reuses the ONE
rendered argv — falsifiers 1 and 3 from the parent hypothesis hold.

## What landed

`extensions/agi/bin/dispatch.py` (**+38/-2** lines):

- `_persistent_row(root, seat, *, pid, session_id)` reuses rotate's ONE
  identity writer (`rotate._write_identity_cells`) — never a second writer.
  `pid 0` is the established empty sentinel, so a stop CLEARS the
  occupation. A refused write is printed BY NAME, never bypassed.
- `_supervise_persistent(..., root, seat, session_id)` writes the row at
  start and after each restart, and on exit when no live child remains drops
  `persistent`, zeroes `pid`, and clears the row. `--persistent` absent
  changes nothing (fire-and-forget stays byte-identical).

## Evidence

`experiment:persistent-seat-corpse-and-row` — 5 tests green in
`extensions/agi/tests/test_dispatch_persistent.py`; the 145-test dispatch
regression is green. Both holes hold on the built bytes.

## Not reached / scope

- Non-persistent regression is `goal:g7.28.2`; template authorship
  `goal:g7.27`; rotate's argv builders are untouched (`goal:g7.29`).
- `session_id` is written only when the harness supplies one; at spawn it is
  not yet known, so the start/restart writes set `pid` and leave an existing
  `session_id` cell alone (the writer's None-guard skips it).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.168 PARENT REVIEW (a00-164669ca) of hypothesis:a00-dbb8baf9-be621f (kid a00-dbb8baf9). INSTRUCTION: the parent runs one negative probe per claim conjunct against the kid's bytes and records them as probes; a kid that passes its own suite but fails a probe is lean_disproved with the probe NAMED. MACHINE (read from the bytes, not the summary): _persistent_row (dispatch.py:1518) reuses rotate._write_identity_cells with actor=seat; _supervise_persistent (dispatch.py:1538) writes the row at start (pid=proc.pid), after each restart, and on exit iff proc.poll() is not None drops persistent, zeroes pid, persists agent.json, and clears the row (pid=0); the call site (dispatch.py:2989) threads seat=args.seat and root. rotate._write_identity_cells skips None cells, so a None session_id leaves the cell alone; write.submit(actor=seat) is admitted by the [config] self_row grant. NEAR MISS: a direct frontmatter edit or a second row-writer would satisfy row-shows-occupation and lose the one-writer/self_row rule; probe W and the live writer line wrote identity cells for seat seat-a into MAIN posts.md show the reuse is real. PROBES (parent, probes_dh168.py plus inline probe_Y): G gate HOLDS (exhaustion drops persistent and zeroes pid in the record AND agent.json); Y gate HOLDS (the final MANIFEST record is persistent=None pid=0); W wire HOLDS (live pid 1234 lands in the seat own row, clears to 0, foreign row 123 untouched); X wire HOLDS (args.seat reaches the changed bytes; pids 1000,1001,1002,1003,0). JUDGEMENT: proved ACCEPTED. CAVEAT, not a falsifier of the kid stated claim: the target live pid/session pin is only half met because session_id is not knowable at spawn and is passed None, so the supervisor writes pid but no session pin; the seat own ack remains the writer of session_id. That is the kid own scope note, honestly left.
<!-- THOUGHT:END -->

## Agent Notes
Closed both DH.49 holes in dispatch.py (+38/-2): exhaustion/reopen-failure now drops persistent and zeroes pid (never a corpse under persistent:true), and --seat writes/clears the seat's OWN posts row via rotate._write_identity_cells (pid 0 sentinel). 5 persistent tests + 145 dispatch regression green.
