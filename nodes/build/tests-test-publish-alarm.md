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
  how: '`import importlib.util` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: io
  how: '`import io` at line 35'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 36'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 37'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 38'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 39'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 40'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 41'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 43'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads((root / STATE_REL).read_text(encoding="utf-8"))` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / STATE_REL
  how: '`(root / STATE_REL).read_text()` at line 321'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / STATE_REL
  how: '`(root / STATE_REL).read_text(encoding="utf-8")` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / STATE_REL
  how: '`(root / STATE_REL).read_text()` at line 325'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: project
  how: 'defines public function `project` at line 75, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_state
  how: 'defines private function `_write_state` at line 83, signature: (root: Path,
    **fields)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_state
  how: 'defines private function `_read_state` at line 90, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git
  how: 'defines private function `_git` at line 94, signature: (root: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_project
  how: 'defines private function `_git_project` at line 99, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _dirty
  how: 'defines private function `_dirty` at line 113, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _run_publish
  how: 'defines private function `_run_publish` at line 119, signature: (root: Path,
    *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _run_hook
  how: 'defines private function `_run_hook` at line 124, signature: (cwd: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_never_published_is_the_loudest_value_not_the_quietest
  how: 'defines public function `test_never_published_is_the_loudest_value_not_the_quietest`
    at line 136, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_marker_at_all_does_not_report_as_healthy
  how: 'defines public function `test_no_marker_at_all_does_not_report_as_healthy`
    at line 146, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_successful_publish_clears_both_numbers
  how: 'defines public function `test_a_successful_publish_clears_both_numbers` at
    line 152, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_names_itself_and_keeps_the_clock_running
  how: 'defines public function `test_a_refusal_names_itself_and_keeps_the_clock_running`
    at line 161, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_cron_that_simply_stops_still_moves_the_number
  how: 'defines public function `test_a_cron_that_simply_stops_still_moves_the_number`
    at line 171, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_with_no_reason_is_still_not_silent
  how: 'defines public function `test_a_refusal_with_no_reason_is_still_not_silent`
    at line 179, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_corrupt_marker_alarms_rather_than_reassures
  how: 'defines public function `test_a_corrupt_marker_alarms_rather_than_reassures`
    at line 185, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_clock_that_moved_backwards_does_not_read_as_a_future_publish
  how: 'defines public function `test_a_clock_that_moved_backwards_does_not_read_as_a_future_publish`
    at line 196, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_reason_survives_as_one_metric_token
  how: 'defines public function `test_the_reason_survives_as_one_metric_token` at
    line 207, signature: (project, raw)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_reason_that_is_not_a_string_does_not_crash_the_metrics_stage
  how: 'defines public function `test_a_reason_that_is_not_a_string_does_not_crash_the_metrics_stage`
    at line 222, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_metrics_reach_the_metric_lines
  how: 'defines public function `test_both_metrics_reach_the_metric_lines` at line
    228, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_compute_carries_the_publish_alarm
  how: 'defines public function `test_compute_carries_the_publish_alarm` at line 237,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_stall_raises_a_warning_a_healthy_publish_does_not
  how: 'defines public function `test_a_stall_raises_a_warning_a_healthy_publish_does_not`
    at line 243, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_exits_non_zero
  how: 'defines public function `test_a_refusal_exits_non_zero` at line 261, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_writes_a_machine_readable_marker
  how: 'defines public function `test_a_refusal_writes_a_machine_readable_marker`
    at line 268, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_marker_is_not_written_under_nodes
  how: 'defines public function `test_the_marker_is_not_written_under_nodes` at line
    278, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_refusal_says_the_bytes_are_safe
  how: 'defines public function `test_the_refusal_says_the_bytes_are_safe` at line
    290, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_does_not_erase_the_last_real_publish
  how: 'defines public function `test_a_refusal_does_not_erase_the_last_real_publish`
    at line 302, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_never_touches_the_marker
  how: 'defines public function `test_dry_run_never_touches_the_marker` at line 316,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_gate_zero_is_still_a_refusal
  how: 'defines public function `test_gate_zero_is_still_a_refusal` at line 328, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_a_silent_no_op_outside_a_project
  how: 'defines public function `test_the_hook_is_a_silent_no_op_outside_a_project`
    at line 343, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_stays_silent_outside_a_project_even_with_a_stray_marker
  how: 'defines public function `test_the_hook_stays_silent_outside_a_project_even_with_a_stray_marker`
    at line 355, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_when_the_publish_is_stalled
  how: 'defines public function `test_the_hook_shouts_when_the_publish_is_stalled`
    at line 367, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_even_when_there_is_no_map_to_inject
  how: 'defines public function `test_the_hook_shouts_even_when_there_is_no_map_to_inject`
    at line 383, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_quiet_when_the_publish_is_healthy
  how: 'defines public function `test_the_hook_is_quiet_when_the_publish_is_healthy`
    at line 395, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_when_the_cron_itself_has_stopped
  how: 'defines public function `test_the_hook_shouts_when_the_cron_itself_has_stopped`
    at line 407, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_corrupt_marker_does_not_break_the_hook
  how: 'defines public function `test_a_corrupt_marker_does_not_break_the_hook` at
    line 419, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_marker_means_no_banner
  how: 'defines public function `test_no_marker_means_no_banner` at line 429, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_out
  how: 'defines private function `_git_out` at line 456, signature: (root: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _init_repo
  how: 'defines private function `_init_repo` at line 461, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pair
  how: 'defines private function `_pair` at line 467, signature: (tmp_path, engine_lags:
    bool=True, extra_nodes: dict | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pending
  how: 'defines private function `_pending` at line 505, signature: (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _dirty_a_node
  how: 'defines private function `_dirty_a_node` at line 509, signature: (project:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _publish
  how: 'defines private function `_publish` at line 516, signature: (project: Path,
    engine: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_blocked_publish_parks_the_bytes_instead_of_stranding_them
  how: 'defines public function `test_a_blocked_publish_parks_the_bytes_instead_of_stranding_them`
    at line 520, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_never_writes_the_default_branch
  how: 'defines public function `test_the_fallback_never_writes_the_default_branch`
    at line 537, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_leaves_the_engine_checkout_exactly_where_it_was
  how: 'defines public function `test_the_fallback_leaves_the_engine_checkout_exactly_where_it_was`
    at line 549, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_leaves_no_worktree_behind
  how: 'defines public function `test_the_fallback_leaves_no_worktree_behind` at line
    565, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parking_the_bytes_does_not_make_the_alarm_read_healthy
  how: 'defines public function `test_parking_the_bytes_does_not_make_the_alarm_read_healthy`
    at line 581, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_marker_says_where_the_parked_bytes_went
  how: 'defines public function `test_the_marker_says_where_the_parked_bytes_went`
    at line 601, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_second_run_at_the_same_dirty_state_does_not_commit_again
  how: 'defines public function `test_a_second_run_at_the_same_dirty_state_does_not_commit_again`
    at line 616, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_moving_grid_does_add_a_second_commit
  how: 'defines public function `test_a_moving_grid_does_add_a_second_commit` at line
    634, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_pending_branch_can_still_be_fast_forwarded
  how: 'defines public function `test_the_pending_branch_can_still_be_fast_forwarded`
    at line 652, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_parked_commit_does_not_claim_the_graph_sha_describes_it
  how: 'defines public function `test_the_parked_commit_does_not_claim_the_graph_sha_describes_it`
    at line 665, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_parks_nothing_the_real_publish_would_refuse
  how: 'defines public function `test_the_fallback_parks_nothing_the_real_publish_would_refuse`
    at line 682, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_declined_fallback_shows_what_the_verify_actually_said
  how: 'defines public function `test_a_declined_fallback_shows_what_the_verify_actually_said`
    at line 700, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_creates_no_branch
  how: 'defines public function `test_dry_run_creates_no_branch` at line 716, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_never_cuts_a_branch_in_the_graph_repo
  how: 'defines public function `test_the_fallback_never_cuts_a_branch_in_the_graph_repo`
    at line 729, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_stale_pending_branch_is_rebuilt_rather_than_extended
  how: 'defines public function `test_a_stale_pending_branch_is_rebuilt_rather_than_extended`
    at line 746, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 77'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(json.dumps(fields), encoding="utf-8")` at line 86'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "agi-tree.config.json"
  how: '`(root / "agi-tree.config.json").write_text("{}")` at line 103'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "n.md"
  how: '`(root / "nodes" / "n.md").write_text(''---\nid: "goal:n"\ntype: goal\n---\n\nbody\n'')`
    at line 104'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("{not json at all")` at line 190'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: outside / "context" / "publish-state.json"
  how: '`(outside / "context" / "publish-state.json").write_text( json.dumps({"last_run_status":
    "refused", "last_run_reason": "graph-dirty"}))` at line 360'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 368'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 396'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 410'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 422'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / STATE_REL
  how: '`(project / STATE_REL).write_text("{ truncated")` at line 423'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 434'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "agi-tree.config.json"
  how: '`(project / "agi-tree.config.json").write_text("{}")` at line 486'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/bin/foo.py"
  how: '`(engine / "extensions/agi/bin/foo.py").write_text("import os\n\n\ndef foo():\n    return
    2\n")` at line 644'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/src/pkg/bar.py"
  how: '`(engine / "extensions/agi/src/pkg/bar.py").write_text("# master moved on\n")`
    at line 759'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(fields)` at line 86'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"last_run_status": "refused", "last_run_reason": "graph-dirty"})`
    at line 361'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(text, encoding="utf-8")` at line 479'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / "build" / f"{slug}.md"
  how: '`(project / "nodes" / "build" / f"{slug}.md").write_text(text, encoding="utf-8")`
    at line 493'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/bin/foo.py"
  how: '`(engine / "extensions/agi/bin/foo.py").write_text("# stale\n", encoding="utf-8")`
    at line 500'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
