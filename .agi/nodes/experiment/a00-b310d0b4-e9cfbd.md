---
id: experiment:a00-b310d0b4-e9cfbd
mint_id: b1826ef423194a42bd7eabd79ca23db7
type: experiment
parents:
  - hypothesis:l4-rotation-alerts-follow-a-routing-matrix-in-config-rotations-audit-plus-edges-intersect-live-minus-self-minus-silent
next_edges: []
confidence: 0.55
edited_by: a00-a21fe617
evidence_runs:
  - experiment:a00-b310d0b4-e9cfbd
loop: hypothesis:l4-rotation-alerts-follow-a-routing-matrix-in-config-rotations-audit-plus-edges-intersect-live-minus-self-minus-silent@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe P4/P5: _derive_receivers with an empty alerts map and with alerts absent", "expected": "absent -> today-broadcast byte-identical; empty map == absent", "observed": "a -> [b, c]; held", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P2: audit and edges deliberately contain the rotating seat itself and the silent name", "expected": "neither self nor silent appears", "observed": "belam -> [master-sensei, sanctuary-director]; held", "result": "held"}
  - {"conjunct": 3, "class": "auth", "cmd": "parent probe: read send.send_dm gate plus the new prime branch", "expected": "prime reaches its receivers; send_dm refuses prime origin", "observed": "send.py:3262 refuses prime origin; prime branch delivers via send.send per receiver; held", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe P3: rotation record written at rotate.py:16436 BEFORE _announce_rotation at :16590; announced_to set only on the seating record (:4072)", "expected": "the rotation record carries announced_to", "observed": "no announced_to on any rotation record; FALSIFIED", "result": "falsified"}
  - {"conjunct": 5, "class": "gate", "cmd": "parent probe P1: run_after_join(seat=stream-master, type_input=recorder, send_dm=recorder)", "expected": "silent post gets ZERO machine lines: neither seam fires", "observed": "type_input FIRED with the after_join dm while send_dm was correctly refused; FALSIFIED", "result": "falsified"}
profile: balanced
role: kid
scaffold_hash: 8414152ff1fa0511
season: 2
title: A00 b310d0b4 e9cfbd
town: core
verdict: inconclusive_lean_disproved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-b310d0b4-e9cfbd

## Experiment

A g15 CLAIM (build-to-prove, not measure-only). The owner order (07:3xZ via Prime XIX,
relayed in the parent hypothesis) is that rotation alerts follow an `alerts:` routing
matrix on config:rotations — receivers = (audit + edges[seat]) ∩ live − self − silent —
the Sensei gets exactly ONE machine line per rotation, stream-master is never a machine
alert, and the Prime delivers per-receiver instead of only posting to the room.

**Pre-fix measured state** (rotate.py @3af8dd489): `_derive_receivers` (:3960) = every
config:seats row ∩ live tmux windows − self → a BROADCAST; `_announce_rotation` posts the
prime to ROTATION_ALERT_ROOM + own inbox and returns `[ROTATION_ALERT_ROOM]`, never
reaching the matrix; no `alerts:` key on config:rotations; the after_join dm is a second
machine-sender class with no silent gate.

**Built:**
1. `rotate.py::_load_alerts(root)` — reads config:rotations frontmatter `alerts:` as a
   dict; parses a quoted-JSON str cell too (the single bare-flow `set alerts {…}` line
   write.py produces loads as a native dict; a quoted scalar parses via json.loads).
2. `rotate.py::_alert_silent(root)` + `rotate.py::_alert_allowed(root, receiver)` — the ONE
   shared silent gate (stream-master wins over audit AND edges).
3. `rotate.py::_derive_receivers(root, seat, live_names)` — `alerts:` PRESENT →
   `sorted((audit ∪ edges[seat]) ∩ live − {seat} − silent)`; ABSENT → the today-broadcast,
   byte-identical. A post absent from edges alerts audit only; dead edges drop.
4. `_announce_rotation` prime branch — the prime now DELIVERS to its derived receivers via
   `send.send` (send_dm REFUSES prime origin: "a dm may not originate from the prime"; this
   is the one deviation from the claim's literal "by send.send_dm" — recorded, not silent),
   keeps the room post as the record with NO nudge (measured: `send_room` never nudges — no
   `_nudge_window` call in it), and keeps the own-inbox copy.
5. silent applied to the after_join machine sender: `run_after_join` guards the default
   send_dm closure AND a caller-injected seam with `_alert_allowed(root, to)`.
6. The ONE rotation/seating record `_announce_rotation` itself writes (the seating record)
   now carries `announced_to` = the derived receivers (computed BEFORE the write).

The `alerts:` matrix (audit/edges/silent) is NOT written to the live config node by the
round — the Prime applies the ONE `set alerts {…}` line at merge-up. The exact line, dry-run-
proven below, ships so the Prime can drop it.

**Tests** (`extensions/agi/tests/test_rotation_alerts.py`, 8, all green): the parent's full
matrix as fixture data (bare-flow ONE-line `alerts:`), seats.md + live_names:
1. belam live w/ both edges → exactly [master-sensei, sanctuary-director, sanctuary-helper]
2. sensei-director → [master-sensei, sanctuary-master]
3. stream-master rotating → [master-sensei] (silent silences its INBOX, not its outgoing)
4. a post absent from edges → [master-sensei]
5. a dead edge (not live) dropped
6. stream-master never a receiver for ANY seat
7. alerts: ABSENT → today broadcast (byte-identical)
8. after_join dm to a silent post refused (seam never fired)

Existing prime tests (`test_announce_rotation_prime_*` in test_rotate.py) REWRITTEN for the
new prime contract (deliver to derived receivers, keep room record + own-inbox copy).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotation_alerts.py -q
8 passed in 20.10s

$ python3 -m pytest test_rotate.py test_rotate_alert_two_tree.py test_rotate_startup.py \
    test_rotate_autopsy.py test_sensei_rotate_out_audit.py test_rotation_alerts.py
423 passed, 1 xfailed

ruff: my files clean (rotate.py 23 pre-existing errors, none in edited regions;
      test_rotation_alerts.py all checks pass)
```

The exact Prime merge-up write (dry-run proven: parses to the matrix, `belam` live with both
edges + sensei live → [sanctuary-director, sanctuary-helper, master-sensei]):

```
write.py config:rotations 'set alerts {audit:[master-sensei],edges:{belam:[sanctuary-director,sanctuary-helper],sanctuary-director:[belam],sanctuary-helper:[belam],sanctuary-master:[sensei-director],sensei-director:[sanctuary-master]},silent:[stream-master]}'
```

Acceptance measure for the NEXT live rotation of each post (the round never writes config):
announce line lists matrix ∩ live; Sensei appears once; stream-master zero machine lines; the
behaviour is the broadcast (byte-identical) on any post whose `alerts:` is yanked.

## Agent Notes
Built the alerts: routing matrix: _derive_receivers=(audit U edges[seat])∩live-{seat}-silent, _alert_allowed silent gate shared by the 3 machine senders (including after_join), prime branch now delivers per-receiver via send.send (send_dm refuses prime origin). 8 new tests in test_rotation_alerts.py + 2 prime tests rewritten; 423 passed. The sensei-wake template-line edit + live config alerts: write are the Prime's merge-up act, not the round.

## Agent Notes
Built the alerts: routing matrix: _derive_receivers=(audit U edges[seat]) cap live - {seat} - silent; _alert_allowed silent gate shared by the 3 machine senders incl after_join; prime branch now delivers per-receiver via send.send (send_dm refuses prime origin). 8 new tests in test_rotation_alerts.py + 2 prime tests rewritten; 423 green. sensei-wake template edit + live config alerts: write are the Prime's merge-up act.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SM.16. Instruction: receivers = (audit + edges[seat]) cap live - self - silent; silent applies to EVERY machine sender; the announce records announced_to on the rotation record. Machine, measured: _derive_receivers is correct and alerts-absent stays byte-identical (probes P2/P4/P5 held), and the prime branch reaches receivers via send.send because send.py:3262 refuses prime origin (probe on the source). But two conjuncts fail my probes. (4) the rotation record is written at rotate.py:16436 BEFORE _announce_rotation at :16590, and announced_to rides only on the seating record (:4072) -- probe P3. (5) run_after_join types the dm into the silent successor through the type_input seam at :12111, before the _alert_allowed gate at :12157 -- probe P1 fired the typing seam for stream-master. Near miss: gating only send_dm satisfies the words after_join dm but loses the mechanism, because in production the second input is TYPED into the successor pane and send_dm is never reached. Verdict demoted inconclusive_lean_proved:85 -> inconclusive_lean_disproved:55.
<!-- THOUGHT:END -->
