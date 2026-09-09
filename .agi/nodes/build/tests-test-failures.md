---
build_kind: code
confidence: 1.0
id: "build:tests-test-failures"
mint_id: eec7ee9ef2c3461da7be3f855489f493
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_failures.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_failures.py"
type: build
---

`extensions/agi/tests/test_failures.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_failures.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: failures
  how: '`import failures` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(rates_out.read_text(encoding="utf-8"))` at line 273'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: rates_out
  how: '`rates_out.read_text(encoding="utf-8")` at line 273'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(out.read_text())` at line 224'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out
  how: '`out.read_text()` at line 224'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(out.read_text())` at line 244'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out
  how: '`out.read_text()` at line 244'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _agent_json
  how: 'defines private function `_agent_json` at line 26, signature: (agent_id, iter_id,
    **over)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_agent
  how: 'defines private function `_write_agent` at line 52, signature: (sessions,
    iter_id, agent_id, agent_json=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fx
  how: 'defines public function `fx` at line 63, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _derive
  how: 'defines private function `_derive` at line 141, signature: (root)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ledger_reads_died_from_swept_zombie_lease
  how: 'defines public function `test_ledger_reads_died_from_swept_zombie_lease` at
    line 145, signature: (fx)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ledger_reads_demoted_and_rejected_from_evidence_gate_fixtures
  how: 'defines public function `test_ledger_reads_demoted_and_rejected_from_evidence_gate_fixtures`
    at line 154, signature: (fx)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ledger_reads_broken_frontmatter_from_write_log
  how: 'defines public function `test_ledger_reads_broken_frontmatter_from_write_log`
    at line 163, signature: (fx)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ledger_reads_session_limit_from_output_log
  how: 'defines public function `test_ledger_reads_session_limit_from_output_log`
    at line 172, signature: (fx)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ledger_reads_wrong_file_from_write_guard_warn
  how: 'defines public function `test_ledger_reads_wrong_file_from_write_guard_warn`
    at line 179, signature: (fx)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ledger_reads_overclaim_and_no_build_probe_only
  how: 'defines public function `test_ledger_reads_overclaim_and_no_build_probe_only`
    at line 188, signature: (fx)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ledger_skips_unadmitted_slots
  how: 'defines public function `test_ledger_skips_unadmitted_slots` at line 197,
    signature: (fx)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_all_eight_categories_derivable
  how: 'defines public function `test_all_eight_categories_derivable` at line 206,
    signature: (fx)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ledger_is_idempotent_on_rerun
  how: 'defines public function `test_ledger_is_idempotent_on_rerun` at line 215,
    signature: (fx, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _seed_ledger
  how: 'defines private function `_seed_ledger` at line 230, signature: (fx, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rates_by_model_and_by_harness_sum_to_total
  how: 'defines public function `test_rates_by_model_and_by_harness_sum_to_total`
    at line 238, signature: (fx, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_aggregate_produces_pick_worst_shape_from_raw_rows
  how: 'defines public function `test_aggregate_produces_pick_worst_shape_from_raw_rows`
    at line 247, signature: (fx)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sensei_command_writes_rates_table
  how: 'defines public function `test_sensei_command_writes_rates_table` at line 263,
    signature: (fx, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ns
  how: defines private class `_ns` at line 281
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ledger_never_writes_node_frontmatter_directly
  how: 'defines public function `test_ledger_never_writes_node_frontmatter_directly`
    at line 286, signature: (fx, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: adir / "agent.json"
  how: '`(adir / "agent.json").write_text(json.dumps(aj, indent=2), encoding="utf-8")`
    at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: adir / "output.log"
  how: '`(adir / "output.log").write_text("", encoding="utf-8")` at line 58'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sessions / f"iter-{i1}" / "a1-died" / "agent.json"
  how: '`(sessions / f"iter-{i1}" / "a1-died" / "agent.json").write_text(json.dumps(
    _agent_json("a1-died", i1, status="failed"), indent=2), encoding="utf-8")` at
    line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sessions / f"iter-{i1}" / "a2-demoted" / "agent.json"
  how: '`(sessions / f"iter-{i1}" / "a2-demoted" / "agent.json").write_text( json.dumps(a2,
    indent=2), encoding="utf-8")` at line 81'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sessions / f"iter-{i1}" / "a3-reject" / "output.log"
  how: '`(sessions / f"iter-{i1}" / "a3-reject" / "output.log").write_text( "spawning...\nEVIDENCE-GATE
    REJECTED: nothing written\n", encoding="utf-8")` at line 86'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sessions / f"iter-{i1}" / "a4-pending" / "agent.json"
  how: '`(sessions / f"iter-{i1}" / "a4-pending" / "agent.json").write_text(json.dumps(
    _agent_json("a4-pending", i1, verdict="pending"), indent=2), encoding="utf-8")`
    at line 92'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sessions / f"iter-{i1}" / "a5-hung" / "agent.json"
  how: '`(sessions / f"iter-{i1}" / "a5-hung" / "agent.json").write_text(json.dumps(
    _agent_json("a5-hung", i1, status="hung-unhealed"), indent=2), encoding="utf-8")`
    at line 98'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sessions / f"iter-{i1}" / "a6-wrongfile" / "output.log"
  how: '`(sessions / f"iter-{i1}" / "a6-wrongfile" / "output.log").write_text( "WARN
    unsanctioned write: nodes/experiment/someone.md\n" "  to redo: python3 extensions/agi/bin/write.py
    ...\n", encoding="utf-8")` at line 104'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sessions / f"iter-{i1}" / "a7-sessionlimit" / "output.log"
  how: '`(sessions / f"iter-{i1}" / "a7-sessionlimit" / "output.log").write_text(
    ''{"type":"result","subtype":"session_limit",'' ''"reset_time":"2026-09-08T00:00:00Z"}\n'',
    encoding="utf-8")` at line 110'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: review / "results.json"
  how: '`(review / "results.json").write_text(json.dumps({ "reviews": [{"target":
    "hypothesis:fixture", "verdict": "proved", "overclaims": 2, "open_gaps": 1, "files_changed":
    3}] }), encoding="utf-8")` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sessions / "write-log.jsonl"
  how: '`(sessions / "write-log.jsonl").write_text(json.dumps({ "node_id": "experiment:a2-demoted",
    "operation": "repair-frontmatter", "path": "nodes/experiment/a2-demoted.md", "sha256":
    "deadbeef", "ts": "2026-09-07T00:00:00.000000Z", }) + "\n", en...[truncated, 255
    chars total]` at line 128'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(aj, indent=2)` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( _agent_json("a1-died", i1, status="failed"), indent=2)` at line
    74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(a2, indent=2)` at line 82'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( _agent_json("a4-pending", i1, verdict="pending"), indent=2)`
    at line 92'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( _agent_json("a5-hung", i1, status="hung-unhealed"), indent=2)`
    at line 98'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({ "reviews": [{"target": "hypothesis:fixture", "verdict": "proved",
    "overclaims": 2, "open_gaps": 1, "files_changed": 3}] })` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({ "node_id": "experiment:a2-demoted", "operation": "repair-frontmatter",
    "path": "nodes/experiment/a2-demoted.md", "sha256": "deadbeef", "ts": "2026-09-07T00:00:00.000000Z",
    })` at line 128'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
