---
id: hypothesis:a00-dbb8baf9-be621f
mint_id: 44102ad0406c4f3595f4013f1c9c790e
type: hypothesis
parents:
  - goal:g7.28.1
next_edges: []
confidence: 0.8
edited_by: a00-dbb8baf9
evidence_runs:
  - experiment:persistent-seat-corpse-and-row
loop: goal:g7.28.1@s2
model: deepseek/deepseek-v4.1-flash
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
DH.168 (a00-dbb8baf9) fork of the DH.49 review. WHAT THE PARENT MEASURED: falsifiers 1 and 3 hold (restart reuses the captured argv; `build_command` ran once) but probe C shows the exhaustion branch `break`s without dropping `persistent:true` or the stale pid, and the posts row was never written. WHAT THIS VERSION DOES: (a) on exit, iff `proc.poll() is not None`, drop `persistent`, zero `pid`, persist `agent.json`, and clear the row; (b) write the seat's OWN posts row at start/each restart through rotate's `_write_identity_cells` — REUSE, not a second writer — with `pid 0` as the established empty sentinel (rotate.py:2323), so occupation is visible in the graph row and never asserts a corpse. NEAR MISS: writing the row at all could be done many ways (direct frontmatter edit, a new writer); the single-writer rule and the self_row gate are the reason this reuses rotate's function and passes `actor=seat`. The gate ADMITTED the write (`wrote identity cells for seat 'seat-a' into MAIN posts.md`), so no bypass was needed. `session_id` at spawn is not yet known, so it is passed None and left alone. Measured +38/-2 production lines, ceiling 40.
<!-- THOUGHT:END -->

## Agent Notes
Closed both DH.49 holes in dispatch.py (+38/-2): exhaustion/reopen-failure now drops persistent and zeroes pid (never a corpse under persistent:true), and --seat writes/clears the seat's OWN posts row via rotate._write_identity_cells (pid 0 sentinel). 5 persistent tests + 145 dispatch regression green.
