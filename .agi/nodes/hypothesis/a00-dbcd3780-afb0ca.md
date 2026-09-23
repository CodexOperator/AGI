---
id: hypothesis:a00-dbcd3780-afb0ca
mint_id: 21d83710f0174cea9ab4d257a9b246da
type: hypothesis
parents:
  - goal:g7.31.2.1
next_edges: []
confidence: 0.8
edited_by: a00-fc6e6a42
evidence_runs:
  - experiment:a00-dbcd3780-session-pin
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "seat_occupation(row window '@7', session 'SID-LIVE', pid 0; seam '@7 director-seat'; registry dir with 99999.json {view:'@7.%0', session_id:'SID-LIVE'})", "expected": "state occupied, session_ok True, live_session SID-LIVE", "observed": "state occupied session_ok True live_session SID-LIVE", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "same live registry session SID-LIVE vs row session SID-FOREIGN", "expected": "session_ok False and the rendered cell NAMES session-drift", "observed": "session_ok False cell=' pane=occupied(@7) session-drift(row SID-FOREIGN live SID-LIVE)'", "result": "pass"}
  - {"conjunct": 1, "class": "auth", "cmd": "registry only for window '@70' (view '@70.%0', session SID-70), live window '@7'", "expected": "session_ok None -- @7 must NOT join @70 (substring-join trap)", "observed": "session_ok None live_session ''", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "row session SID-LIVE, registry dir EMPTY (JOIN miss)", "expected": "session_ok None (unknown), never False/True -- a join miss is not an accusation of drift", "observed": "session_ok None", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "registry_dir omitted entirely", "expected": "session_ok None and cell == ' pane=occupied(@7)' exactly (no-registry render byte-identical)", "observed": "session_ok None cell=' pane=occupied(@7)'", "result": "pass"}
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
Parent review (DH.178, a00-fc6e6a42). (1) The brief said: "Run one negative probe per claim conjunct yourself and record them as `probes:`" and "REVIEW THE BYTES, NOT THE RESULT FILE". (2) The machine: I read the WORKING-TREE bytes, not the result file -- seat_status.py L171-281 (`_live_registry_session`, the seat_occupation session block, `_occ_cell`), test_seat_pane_registry.py L293-358 (the five new session tests), the two authored nodes. I built and RAN .agi/sessions/iter-DH.178/a00-dbcd3780/parent_probe.py: 5/5 probes pass -- (wire) a matching registry session for the live @7 returns occupied/session_ok True; (auth) a foreign row session returns session_ok False and the cell NAMES session-drift; (auth) a registry record for @70 does NOT join a live @7; (gate) an empty registry dir leaves session_ok None, never False; (gate) omitting registry_dir leaves session_ok None and the cell byte-identical to ` pane=occupied(@7)`. (3) Near miss: a join keyed on the registry FILENAME, or a bare substring of the window id, satisfies the words "session pin matches tmux" and loses identity -- `@7` would join `@70` and a foreign session would certify occupied silently. Probe C (registry only for @70, live @7 -> None) is that falsifier; the kid's `_registry_matches_window_id` reuse holds. (4) Deviation: none by me. The kid used 69 production lines vs ceiling 40 -- above the ceiling, under the instruction's own 80 = 2x stop line, so recorded (`production_lines: 69`) rather than cut. Caveat kept in the verdict: the session half joins the per-session registry DIRECTORY, not tmux itself, and the row's short `session_ref` is still empty at seat start by design (back-filled by `rotate.py ack`); the live session that IS checked is the registry-joined `session_id`. That is why the verdict stays inconclusive_lean_proved:80, not proved.
<!-- THOUGHT:END -->

## Agent Notes
Built the session half of goal:g7.31.2.1: seat_status.seat_occupation now consults the seat registry for the live window @id (its own docstring said registry_dir was not consulted) and returns three-valued session_ok (True match / False stale-or-empty / None unknown), naming a False as session-drift in the rendered cell; no-registry renders stay byte-identical. A JOIN-hit seat start reads occupied with session_ok true; a foreign or empty row session reads false; a join miss reads null. 4 probe conjuncts on built bytes, 26 tests in the touched files; production 69 lines (ceiling 40, under the 80 stop line).
