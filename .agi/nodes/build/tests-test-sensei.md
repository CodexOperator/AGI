---
build_kind: code
confidence: 1.0
id: "build:tests-test-sensei"
mint_id: 87f797e069b24069b1d0784ea0bcdcd3
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_sensei.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_sensei.py"
type: build
---

`extensions/agi/tests/test_sensei.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_sensei.py
parse_ok: true
inputs:
- name: json
  how: '`import json` at line 7'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sensei
  how: '`import sensei` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _row
  how: 'defines private function `_row` at line 18, signature: (**kw)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_conv
  how: 'defines private function `_write_conv` at line 25, signature: (path: Path,
    blocks)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_direct_supervisor_room_for_quorum_advisor_prime_dm_for_named_seat
  how: defines public function `test_direct_supervisor_room_for_quorum_advisor_prime_dm_for_named_seat`
    at line 34
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pick_worst_returns_highest_rate_row_ties_broken_by_count
  how: defines public function `test_pick_worst_returns_highest_rate_row_ties_broken_by_count`
    at line 43
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_apply_refuses_without_a_reply_after_since_on_every_thread
  how: 'defines public function `test_apply_refuses_without_a_reply_after_since_on_every_thread`
    at line 57, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: seat_fixture
  how: 'defines public function `seat_fixture` at line 75, signature: (root: Path,
    row: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pick_worst_ledger_reads_json_array_and_jsonl
  how: 'defines public function `test_pick_worst_ledger_reads_json_array_and_jsonl`
    at line 86, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_apply_protected_target_never_calls_write_py_without_owner_approved
  how: 'defines public function `test_apply_protected_target_never_calls_write_py_without_owner_approved`
    at line 114, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _Args
  how: defines private class `_Args` at line 146
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_apply_ephemeral_target_checks_only_the_supervisor_thread
  how: 'defines public function `test_apply_ephemeral_target_checks_only_the_supervisor_thread`
    at line 154, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_apply_unprotected_target_writes_note_exactly_once
  how: 'defines public function `test_apply_unprotected_target_writes_note_exactly_once`
    at line 178, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text("\n---\n".join(parts), encoding="utf-8")` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nodes / "seats.md"
  how: '`(nodes / "seats.md").write_text( "---\nid: config:seats\nmint_id: x\ntype:
    config\n" f"seats:\n  - {json.dumps(row, sort_keys=True)}\n---\n", encoding="utf-8")`
    at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: arr
  how: '`arr.write_text(json.dumps([ {"seat_or_role": "kid", "model": "deepseek-v4",
    "fail_rate": 0.4, "failed": 4}, {"seat_or_role": "director", "model": "deepseek-v4",
    "fail_rate": 0.6, "failed": 6}, ], indent=2), encoding="utf-8")` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: jl
  how: '`jl.write_text(json.dumps({"seat_or_role": "kid", "model": "m", "fail_rate":
    0.2, "failed": 1}) + "\n" + json.dumps({"seat_or_role": "liaison", "model": "m",
    "fail_rate": 0.5, "failed": 2}) + "\n", encoding="utf-8")` at line 103'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps([ {"seat_or_role": "kid", "model": "deepseek-v4", "fail_rate":
    0.4, "failed": 4}, {"seat_or_role": "director", "model": "deepseek-v4", "fail_rate":
    0.6, "failed": 6}, ], indent=2)` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(row, sort_keys=True)` at line 81'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"seat_or_role": "liaison", "model": "m", "fail_rate": 0.5, "failed":
    2})` at line 105'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"seat_or_role": "kid", "model": "m", "fail_rate": 0.2, "failed":
    1})` at line 103'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
