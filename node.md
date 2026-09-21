---
build_kind: code
confidence: 1.0
id: "build:tests-test-telemetry-rollup"
mint_id: 0ba12e45387649f3a68098a3fe9e31f4
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_telemetry_rollup.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_telemetry_rollup.py"
type: build
---

`extensions/agi/tests/test_telemetry_rollup.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_telemetry_rollup.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 6'
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
- name: telemetry_rollup
  how: '`import telemetry_rollup` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _write_node
  how: 'defines private function `_write_node` at line 25, signature: (graph: Path,
    nid: str, ntype: str, parents: list[str], extra_fm: dict | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph
  how: 'defines public function `graph` at line 75, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_walk_experiments_from_outcome
  how: 'defines public function `test_walk_experiments_from_outcome` at line 141,
    signature: (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_walk_experiments_from_separate_outcome
  how: 'defines public function `test_walk_experiments_from_separate_outcome` at line
    152, signature: (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_walk_experiments_with_mvp_parent
  how: 'defines public function `test_walk_experiments_with_mvp_parent` at line 160,
    signature: (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_walk_experiments_empty_chain
  how: 'defines public function `test_walk_experiments_empty_chain` at line 168, signature:
    (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_collect_telemetry_basic_sum
  how: 'defines public function `test_collect_telemetry_basic_sum` at line 180, signature:
    (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_collect_telemetry_with_accepted_bytes
  how: 'defines public function `test_collect_telemetry_with_accepted_bytes` at line
    195, signature: (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_collect_empty_list
  how: defines public function `test_collect_empty_list` at line 210
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_format_ratios_with_data
  how: defines public function `test_format_ratios_with_data` at line 226
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_format_ratios_no_bytes
  how: defines public function `test_format_ratios_no_bytes` at line 234
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_format_ratios_no_data
  how: defines public function `test_format_ratios_no_data` at line 241
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_do_rollup_writes_sums
  how: 'defines public function `test_do_rollup_writes_sums` at line 253, signature:
    (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_do_rollup_dry_run_writes_nothing
  how: 'defines public function `test_do_rollup_dry_run_writes_nothing` at line 274,
    signature: (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_do_rollup_rejects_non_report_type
  how: 'defines public function `test_do_rollup_rejects_non_report_type` at line 286,
    signature: (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_do_rollup_nonexistent_node
  how: 'defines public function `test_do_rollup_nonexistent_node` at line 292, signature:
    (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rollup_from_bigger_outcome
  how: 'defines public function `test_rollup_from_bigger_outcome` at line 303, signature:
    (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rollup_from_overview
  how: 'defines public function `test_rollup_from_overview` at line 315, signature:
    (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_count_aligned_outcomes_zero
  how: 'defines public function `test_count_aligned_outcomes_zero` at line 333, signature:
    (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_count_aligned_outcomes_counted
  how: 'defines public function `test_count_aligned_outcomes_counted` at line 339,
    signature: (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_do_rollup_includes_aligned_count_and_cost
  how: 'defines public function `test_do_rollup_includes_aligned_count_and_cost` at
    line 347, signature: (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_do_rollup_cost_per_aligned_computed
  how: 'defines public function `test_do_rollup_cost_per_aligned_computed` at line
    360, signature: (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_do_rollup_aligned_no_cost_per_aligned
  how: 'defines public function `test_do_rollup_aligned_no_cost_per_aligned` at line
    372, signature: (graph: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_smoke_help
  how: defines public function `test_cli_smoke_help` at line 387
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: type_dir / f"{slug}.md"
  how: '`(type_dir / f"{slug}.md").write_text("\n".join(lines) + "\n")` at line 67'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: g / "config.json"
  how: '`(g / "config.json").write_text("{}")` at line 98'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
