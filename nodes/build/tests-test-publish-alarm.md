---
build_kind: code
confidence: 1.0
id: "build:tests-test-publish-alarm"
mint_id: 8053b4cdd5b8421996fc4f66656c5d9d
origin: build-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_publish_alarm.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_publish_alarm.py"
type: build
---

`extensions/agi/tests/test_publish_alarm.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_publish_alarm.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: io
  how: '`import io` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 35'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads((root / STATE_REL).read_text(encoding="utf-8"))` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / STATE_REL
  how: '`(root / STATE_REL).read_text()` at line 305'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / STATE_REL
  how: '`(root / STATE_REL).read_text(encoding="utf-8")` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / STATE_REL
  how: '`(root / STATE_REL).read_text()` at line 309'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: project
  how: 'defines public function `project` at line 59, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_state
  how: 'defines private function `_write_state` at line 67, signature: (root: Path,
    **fields)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_state
  how: 'defines private function `_read_state` at line 74, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git
  how: 'defines private function `_git` at line 78, signature: (root: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_project
  how: 'defines private function `_git_project` at line 83, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _dirty
  how: 'defines private function `_dirty` at line 97, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _run_publish
  how: 'defines private function `_run_publish` at line 103, signature: (root: Path,
    *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _run_hook
  how: 'defines private function `_run_hook` at line 108, signature: (cwd: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_never_published_is_the_loudest_value_not_the_quietest
  how: 'defines public function `test_never_published_is_the_loudest_value_not_the_quietest`
    at line 120, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_marker_at_all_does_not_report_as_healthy
  how: 'defines public function `test_no_marker_at_all_does_not_report_as_healthy`
    at line 130, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_successful_publish_clears_both_numbers
  how: 'defines public function `test_a_successful_publish_clears_both_numbers` at
    line 136, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_names_itself_and_keeps_the_clock_running
  how: 'defines public function `test_a_refusal_names_itself_and_keeps_the_clock_running`
    at line 145, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_cron_that_simply_stops_still_moves_the_number
  how: 'defines public function `test_a_cron_that_simply_stops_still_moves_the_number`
    at line 155, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_with_no_reason_is_still_not_silent
  how: 'defines public function `test_a_refusal_with_no_reason_is_still_not_silent`
    at line 163, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_corrupt_marker_alarms_rather_than_reassures
  how: 'defines public function `test_a_corrupt_marker_alarms_rather_than_reassures`
    at line 169, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_clock_that_moved_backwards_does_not_read_as_a_future_publish
  how: 'defines public function `test_a_clock_that_moved_backwards_does_not_read_as_a_future_publish`
    at line 180, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_reason_survives_as_one_metric_token
  how: 'defines public function `test_the_reason_survives_as_one_metric_token` at
    line 191, signature: (project, raw)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_reason_that_is_not_a_string_does_not_crash_the_metrics_stage
  how: 'defines public function `test_a_reason_that_is_not_a_string_does_not_crash_the_metrics_stage`
    at line 206, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_metrics_reach_the_metric_lines
  how: 'defines public function `test_both_metrics_reach_the_metric_lines` at line
    212, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_compute_carries_the_publish_alarm
  how: 'defines public function `test_compute_carries_the_publish_alarm` at line 221,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_stall_raises_a_warning_a_healthy_publish_does_not
  how: 'defines public function `test_a_stall_raises_a_warning_a_healthy_publish_does_not`
    at line 227, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_exits_non_zero
  how: 'defines public function `test_a_refusal_exits_non_zero` at line 245, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_writes_a_machine_readable_marker
  how: 'defines public function `test_a_refusal_writes_a_machine_readable_marker`
    at line 252, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_marker_is_not_written_under_nodes
  how: 'defines public function `test_the_marker_is_not_written_under_nodes` at line
    262, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_refusal_says_the_bytes_are_safe
  how: 'defines public function `test_the_refusal_says_the_bytes_are_safe` at line
    274, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_does_not_erase_the_last_real_publish
  how: 'defines public function `test_a_refusal_does_not_erase_the_last_real_publish`
    at line 286, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_never_touches_the_marker
  how: 'defines public function `test_dry_run_never_touches_the_marker` at line 300,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_gate_zero_is_still_a_refusal
  how: 'defines public function `test_gate_zero_is_still_a_refusal` at line 312, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_a_silent_no_op_outside_a_project
  how: 'defines public function `test_the_hook_is_a_silent_no_op_outside_a_project`
    at line 327, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_stays_silent_outside_a_project_even_with_a_stray_marker
  how: 'defines public function `test_the_hook_stays_silent_outside_a_project_even_with_a_stray_marker`
    at line 339, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_when_the_publish_is_stalled
  how: 'defines public function `test_the_hook_shouts_when_the_publish_is_stalled`
    at line 351, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_even_when_there_is_no_map_to_inject
  how: 'defines public function `test_the_hook_shouts_even_when_there_is_no_map_to_inject`
    at line 367, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_quiet_when_the_publish_is_healthy
  how: 'defines public function `test_the_hook_is_quiet_when_the_publish_is_healthy`
    at line 379, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_when_the_cron_itself_has_stopped
  how: 'defines public function `test_the_hook_shouts_when_the_cron_itself_has_stopped`
    at line 391, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_corrupt_marker_does_not_break_the_hook
  how: 'defines public function `test_a_corrupt_marker_does_not_break_the_hook` at
    line 403, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_marker_means_no_banner
  how: 'defines public function `test_no_marker_means_no_banner` at line 413, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(json.dumps(fields), encoding="utf-8")` at line 70'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "agi-tree.config.json"
  how: '`(root / "agi-tree.config.json").write_text("{}")` at line 87'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "n.md"
  how: '`(root / "nodes" / "n.md").write_text(''---\nid: "goal:n"\ntype: goal\n---\n\nbody\n'')`
    at line 88'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("{not json at all")` at line 174'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: outside / "context" / "publish-state.json"
  how: '`(outside / "context" / "publish-state.json").write_text( json.dumps({"last_run_status":
    "refused", "last_run_reason": "graph-dirty"}))` at line 344'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 352'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 380'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 394'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 406'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / STATE_REL
  how: '`(project / STATE_REL).write_text("{ truncated")` at line 407'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 418'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(fields)` at line 70'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"last_run_status": "refused", "last_run_reason": "graph-dirty"})`
    at line 345'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
