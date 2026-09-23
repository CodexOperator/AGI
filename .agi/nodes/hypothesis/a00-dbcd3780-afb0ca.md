---
id: hypothesis:a00-dbcd3780-afb0ca
mint_id: 21d83710f0174cea9ab4d257a9b246da
type: hypothesis
parents:
  - goal:g7.31.2.1
next_edges: []
confidence: 0.8
edited_by: a00-dbcd3780
evidence_runs:
  - experiment:a00-dbcd3780-session-pin
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 76fa08096c7aeba7
season: 2
testable_claim: seat_status.seat_occupation must consult the seat registry for the live window @id and return a three-valued session_ok (True match / False stale-or-empty / None unknown), naming a False in the rendered cell and leaving no-registry renders byte-identical
title: A seat occupation read must name the session pin, not only the pane pin
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# The occupation read is session-blind: name the session pin too

## Lineage

`goal:g7.31.2.1`'s falsifier has two clauses — *pane* pin and *session*
pin. The pane half is landed and probed (`seat_status.seat_occupation`,
`pane_coherent`; `experiment:seat-occupation-view`,
`experiment:a00-aa592d9a-seat-pane-pin`). The session half is open, and the
parent verdict said so: the row's `session_ref` is harness-only and stays
empty until `rotate.py ack` back-fills it, so a seat-start row that reads
`occupied` has not had its SESSION identity checked.

```
seat start ──▶ pane @id  ──▶ seat_occupation ──▶ occupied?
                   │                              │
                   └─ session_id (registry JOIN)   └─ NOT consulted  ◀── residue
```

## Hypothesis

A row's occupation read is SESSION-BLIND: `seat_occupation` certifies
`occupied` from the pane @id and pid liveness alone. So a row whose committed
`session_id` is stale, foreign, or empty (a seating JOIN miss) still reads
`occupied`, even when the live tmux window belongs to a DIFFERENT session.
The falsifier's session clause is unmet until the ONE read also carries the
session identity.

Testable claim: consulting the seat registry for the live window @id yields a
three-valued session fact — `session_ok`

- `True` when the row's `session_id` is non-empty and equals the registry's
  `session_id` for the live window @id;
- `False` when the live window's session is known but the row's is empty or
  differs;
- `None` (unknown, fail-open) when no registry record answers the live window
  @id, or no registry dir was given;

and a `False` is NAMED in the rendered occupation cell, while every render
given no registry dir stays byte-identical.

## What would prove it

A `cmd_spawn` seating whose registry JOIN hits writes `session_id` into the
row; reading that row back with the same registry dir returns
`session_ok is True`. A row edited to a foreign `session_id` returns `False`
and renders a `session-drift(...)` cell. A JOIN-miss seating (empty registry)
returns `None`, never a false match. `collect` without the seam is unchanged.

## What would disprove it

Any `session_ok is True` where the row's `session_id` is empty or differs from
the registry's record for the live window @id; any crash instead of a
fail-open `None` on a missing/unreadable registry; or a changed render when no
registry dir was supplied.

Evidence: `experiment:a00-dbcd3780-session-pin`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.178. The parent chain had two OPEN clauses on goal:g7.31.2.1's falsifier:
pane (landed, probed) and session (open -- the parent's own caveat said the
row's `session_ref` is harness-only and stays empty until `rotate.py ack`).
This hypothesis forks the SESSION clause rather than re-testing the pane one.
Chose the registry-joined `session_id` as the session pin, not `session_ref`,
because `_ack_path`'s own comment says a ref is harness-only and "NOT
derivable" -- so no read could ever match it at seat start, and demanding it
would make the falsifier unfalsifiable. The registry record for the live
window @id IS live at seat start (cmd_spawn joins it), so it is the one
session fact a seat-start reader can honestly compare. Evidence:
experiment:a00-dbcd3780-session-pin.
<!-- THOUGHT:END -->

## Agent Notes
Built the session half of goal:g7.31.2.1: seat_status.seat_occupation now consults the seat registry for the live window @id (its own docstring said registry_dir was not consulted) and returns three-valued session_ok (True match / False stale-or-empty / None unknown), naming a False as session-drift in the rendered cell; no-registry renders stay byte-identical. A JOIN-hit seat start reads occupied with session_ok true; a foreign or empty row session reads false; a join miss reads null. 4 probe conjuncts on built bytes, 26 tests in the touched files; production 69 lines (ceiling 40, under the 80 stop line).
