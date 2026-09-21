---
id: experiment:a00-06f2fb5b-dcb884
mint_id: f140f6d70bc74d8cb4ddb0db9cc2cbb4
type: experiment
parents:
  - hypothesis:l4-rotation-alerts-follow-a-routing-matrix-in-config-rotations-audit-plus-edges-intersect-live-minus-self-minus-silent
next_edges: []
confidence: 0.9
edited_by: a00-a21fe617
evidence_runs:
  - experiment:a00-06f2fb5b-dcb884
loop: hypothesis:l4-rotation-alerts-follow-a-routing-matrix-in-config-rotations-audit-plus-edges-intersect-live-minus-self-minus-silent@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P4 rerun: write._coerce on the shipped set-alerts line, node_writer._render_value, yaml.safe_load, write that cell to a scratch rotations node, then _load_alerts + _derive_receivers", "expected": "the emitted string cell parses to the matrix; belam receivers = [master-sensei, sanctuary-director, sanctuary-helper]", "observed": "cell is a str; _load_alerts returned a dict with audit/edges/silent; receivers exactly the matrix set; held", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe P2 rerun: _announce_rotation(record_path=<rotation json>) with monkeypatched send/send_room/wake", "expected": "the rotation record carries announced_to == delivered", "observed": "announced_to == delivered; held", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe P3 rerun: cmd_rotate_self call site threads record_path", "expected": "the kwarg reaches the announce", "observed": "record_path kwarg at rotate.py:16661; held", "result": "held"}
  - {"conjunct": 5, "class": "gate", "cmd": "parent probe P1 rerun: run_after_join(seat=stream-master, type_input=recorder, send_dm=recorder)", "expected": "silent successor receives zero machine lines", "observed": "typed=0 sent=0; held", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent ran tests/test_rotation_alerts.py", "expected": "green including the real write.py pump regression", "observed": "11 passed in 40.14s; held", "result": "held"}
profile: balanced
role: kid
scaffold_hash: 4aba794cd35cdd4d
season: 2
title: A00 06f2fb5b dcb884
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-06f2fb5b-dcb884

## Experiment

Parent probe P4 (from experiment:a00-b310d0b4-e9cfbd / a00-00207b29-5c9b9a)
falsified conjunct 1: the SHIPPED `set alerts {…}` write.py line does NOT
produce a routing map. Measured: `write.py config:rotations 'set alerts
{audit:[...],edges:{...},silent:[...]}'` runs verb_set -> write._coerce, which
keeps the unquoted-key flow map as a STR (only pure JSON parses); node_writer.
_render_value then QUOTES it; yaml.safe_load reads the cell back as a string;
and _load_alerts did only json.loads on that string — which rejects unquoted
keys (JSONDecodeError) — so it returned {} and the whole matrix was treated as
ABSENT -> broadcast. The feature never activated. The two kid fixtures stayed
green only because they hand-wrote valid JSON/flow-YAML maps, a shape write.py
never emits.

This run fixed the parse at the `_load_alerts` seam, file scope:
extensions/agi/bin/rotate.py + extensions/agi/tests/test_rotation_alerts.py.

FIX (rotate.py `_load_alerts`): when a `{`-leading string cell is read, try
json.loads; if that does not yield a dict, fall back to yaml.safe_load (which
parses the exact unquoted-key flow spelling write.py emits) and return {} only
when both fail. Also handles a JSON string-literal cell (json.loads returning
a str, not a dict) by the same fallback. Added `import yaml` to rotate.py.

TEST (test_rotation_alerts.py::test_real_write_py_emitted_str_shape_still_routes):
routes the matrix through the REAL write._coerce -> node_writer._render_value
-> yaml.safe_load round-trip (the P4-measured shape), writes that exact quoted
string cell onto a scratch config:rotations node, then asserts _derive_receivers
returns the matrix set [master-sensei, sanctuary-director, sanctuary-helper]
for seat=belam — NOT the broadcast (which would wrongly include silent
stream-master). The fixture is write.py's emitted shape, never a hand-written
map.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotation_alerts.py -q`: 11 passed
- `pytest test_rotate_alert_two_tree.py test_rotate_verb.py -q`: 20 passed, 1 xfailed
- `pytest test_rotate.py -q -k "receiver or announce or alert"`: 24 passed
- P4 bytes confirmed before the fix: _coerce -> str; rendered `alerts:
  "{audit:[...],edges:{...},silent:[...]}"`; yaml reads str; json.loads FAILS
  JSONDecodeError; yaml.safe_load -> {'audit': ['master-sensei'], 'edges':
  {'belam': ['a','b']}, 'silent': [...]}. After the fix the same bytes route.

Other conjuncts re-checked green: after_join silent gate (send_dm + type_input
seams), announced_to stamp, audit-only for edge-absent/silent-rotating posts.

## Agent Notes

Proved: _load_alerts now parses the write.py-emitted string cell into the
routing matrix; conjunct 1 holds on the real shipped bytes.

## Agent Notes
Fixed _load_alerts to yaml-fallback parse the write.py-emitted quoted flow-string once absent; P4 matrix now routes on real shipped bytes, not broadcast.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SM.16 kid 3. Instruction: make _load_alerts accept the shape write.py ACTUALLY emits, then re-check the conjuncts. Machine, measured by parent probe P4: write._coerce keeps the Prime set-alerts flow map a STR, node_writer._render_value quotes it, and the added yaml.safe_load fallback in _load_alerts parses that exact string into the dict — _load_alerts returned audit/edges/silent and belam receivers were [master-sensei, sanctuary-director, sanctuary-helper]. Re-ran P1 (silent after_join type seam typed=0 sent=0), P2 (rotation record announced_to == delivered), P3 (cmd_rotate_self threads record_path at :16661) and tests/test_rotation_alerts.py (11 passed). Near miss now closed: the previous kid fixture hand-wrote valid JSON into YAML, a shape the tool never emits, so its green suite proved a shape that ships nowhere. Verdict proved accepted. Residual is PRIME-OWNED by the claim itself, not a code gap: the live config:rotations alerts write and the rotations.md:122 sensei-wake template drop are config writes the round is forbidden to make.
<!-- THOUGHT:END -->
