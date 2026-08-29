---
build_kind: code
confidence: 1.0
id: "build:tests-test-publish-alarm"
mint_id: 2c10c7ff301945bb8fac2961341c3476
origin: build-scan
payload_ref: extensions/agi/tests/test_publish_alarm.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_publish_alarm.py"
type: build
---

`extensions/agi/tests/test_publish_alarm.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_publish_alarm.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 55'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: io
  how: '`import io` at line 56'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 58'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 59'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 60'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 62'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 64'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads((root / STATE_REL).read_text(encoding="utf-8"))` at line 112'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / STATE_REL
  how: '`(root / STATE_REL).read_text()` at line 342'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: HOOK_SH
  how: '`HOOK_SH.read_text(encoding="utf-8")` at line 1406'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / STATE_REL
  how: '`(root / STATE_REL).read_text(encoding="utf-8")` at line 112'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / STATE_REL
  how: '`(root / STATE_REL).read_text()` at line 346'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/bin/foo.py"
  how: '`(engine / "extensions/agi/bin/foo.py").read_text()` at line 924'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/bin/fresh.py"
  how: '`(engine / "extensions/agi/bin/fresh.py").read_text()` at line 964'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 831'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: project
  how: 'defines public function `project` at line 96, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_state
  how: 'defines private function `_write_state` at line 104, signature: (root: Path,
    **fields)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_state
  how: 'defines private function `_read_state` at line 111, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git
  how: 'defines private function `_git` at line 115, signature: (root: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_project
  how: 'defines private function `_git_project` at line 120, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _dirty
  how: 'defines private function `_dirty` at line 134, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _run_publish
  how: 'defines private function `_run_publish` at line 140, signature: (root: Path,
    *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _run_hook
  how: 'defines private function `_run_hook` at line 145, signature: (cwd: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_never_published_is_the_loudest_value_not_the_quietest
  how: 'defines public function `test_never_published_is_the_loudest_value_not_the_quietest`
    at line 157, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_marker_at_all_does_not_report_as_healthy
  how: 'defines public function `test_no_marker_at_all_does_not_report_as_healthy`
    at line 167, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_successful_publish_clears_both_numbers
  how: 'defines public function `test_a_successful_publish_clears_both_numbers` at
    line 173, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_names_itself_and_keeps_the_clock_running
  how: 'defines public function `test_a_refusal_names_itself_and_keeps_the_clock_running`
    at line 182, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_cron_that_simply_stops_still_moves_the_number
  how: 'defines public function `test_a_cron_that_simply_stops_still_moves_the_number`
    at line 192, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_with_no_reason_is_still_not_silent
  how: 'defines public function `test_a_refusal_with_no_reason_is_still_not_silent`
    at line 200, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_corrupt_marker_alarms_rather_than_reassures
  how: 'defines public function `test_a_corrupt_marker_alarms_rather_than_reassures`
    at line 206, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_clock_that_moved_backwards_does_not_read_as_a_future_publish
  how: 'defines public function `test_a_clock_that_moved_backwards_does_not_read_as_a_future_publish`
    at line 217, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_reason_survives_as_one_metric_token
  how: 'defines public function `test_the_reason_survives_as_one_metric_token` at
    line 228, signature: (project, raw)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_reason_that_is_not_a_string_does_not_crash_the_metrics_stage
  how: 'defines public function `test_a_reason_that_is_not_a_string_does_not_crash_the_metrics_stage`
    at line 243, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_metrics_reach_the_metric_lines
  how: 'defines public function `test_both_metrics_reach_the_metric_lines` at line
    249, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_compute_carries_the_publish_alarm
  how: 'defines public function `test_compute_carries_the_publish_alarm` at line 258,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_stall_raises_a_warning_a_healthy_publish_does_not
  how: 'defines public function `test_a_stall_raises_a_warning_a_healthy_publish_does_not`
    at line 264, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_exits_non_zero
  how: 'defines public function `test_a_refusal_exits_non_zero` at line 282, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_writes_a_machine_readable_marker
  how: 'defines public function `test_a_refusal_writes_a_machine_readable_marker`
    at line 289, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_marker_is_not_written_under_nodes
  how: 'defines public function `test_the_marker_is_not_written_under_nodes` at line
    299, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_refusal_says_the_bytes_are_safe
  how: 'defines public function `test_the_refusal_says_the_bytes_are_safe` at line
    311, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_does_not_erase_the_last_real_publish
  how: 'defines public function `test_a_refusal_does_not_erase_the_last_real_publish`
    at line 323, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_never_touches_the_marker
  how: 'defines public function `test_dry_run_never_touches_the_marker` at line 337,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_gate_zero_is_still_a_refusal
  how: 'defines public function `test_gate_zero_is_still_a_refusal` at line 349, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_a_silent_no_op_outside_a_project
  how: 'defines public function `test_the_hook_is_a_silent_no_op_outside_a_project`
    at line 364, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_stays_silent_outside_a_project_even_with_a_stray_marker
  how: 'defines public function `test_the_hook_stays_silent_outside_a_project_even_with_a_stray_marker`
    at line 376, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_when_the_publish_is_stalled
  how: 'defines public function `test_the_hook_shouts_when_the_publish_is_stalled`
    at line 388, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_even_when_there_is_no_map_to_inject
  how: 'defines public function `test_the_hook_shouts_even_when_there_is_no_map_to_inject`
    at line 404, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_quiet_when_the_publish_is_healthy
  how: 'defines public function `test_the_hook_is_quiet_when_the_publish_is_healthy`
    at line 416, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_when_the_cron_itself_has_stopped
  how: 'defines public function `test_the_hook_shouts_when_the_cron_itself_has_stopped`
    at line 428, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_corrupt_marker_does_not_break_the_hook
  how: 'defines public function `test_a_corrupt_marker_does_not_break_the_hook` at
    line 440, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_marker_means_no_banner
  how: 'defines public function `test_no_marker_means_no_banner` at line 450, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_out
  how: 'defines private function `_git_out` at line 477, signature: (root: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _init_repo
  how: 'defines private function `_init_repo` at line 482, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pair
  how: 'defines private function `_pair` at line 488, signature: (tmp_path, engine_lags:
    bool=True, extra_nodes: dict | None=None, staged: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pending
  how: 'defines private function `_pending` at line 541, signature: (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _dirty_a_node
  how: 'defines private function `_dirty_a_node` at line 545, signature: (project:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _publish
  how: 'defines private function `_publish` at line 552, signature: (project: Path,
    engine: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_blocked_publish_parks_the_bytes_instead_of_stranding_them
  how: 'defines public function `test_a_blocked_publish_parks_the_bytes_instead_of_stranding_them`
    at line 556, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_never_writes_the_default_branch
  how: 'defines public function `test_the_fallback_never_writes_the_default_branch`
    at line 573, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_leaves_the_engine_checkout_exactly_where_it_was
  how: 'defines public function `test_the_fallback_leaves_the_engine_checkout_exactly_where_it_was`
    at line 585, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_leaves_no_worktree_behind
  how: 'defines public function `test_the_fallback_leaves_no_worktree_behind` at line
    601, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parking_the_bytes_does_not_make_the_alarm_read_healthy
  how: 'defines public function `test_parking_the_bytes_does_not_make_the_alarm_read_healthy`
    at line 617, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_marker_says_where_the_parked_bytes_went
  how: 'defines public function `test_the_marker_says_where_the_parked_bytes_went`
    at line 637, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_second_run_at_the_same_dirty_state_does_not_commit_again
  how: 'defines public function `test_a_second_run_at_the_same_dirty_state_does_not_commit_again`
    at line 652, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_moving_grid_does_add_a_second_commit
  how: 'defines public function `test_a_moving_grid_does_add_a_second_commit` at line
    670, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_pending_branch_can_still_be_fast_forwarded
  how: 'defines public function `test_the_pending_branch_can_still_be_fast_forwarded`
    at line 688, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_parked_commit_does_not_claim_the_graph_sha_describes_it
  how: 'defines public function `test_the_parked_commit_does_not_claim_the_graph_sha_describes_it`
    at line 701, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_parks_nothing_the_real_publish_would_refuse
  how: 'defines public function `test_the_fallback_parks_nothing_the_real_publish_would_refuse`
    at line 718, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_declined_fallback_shows_what_the_verify_actually_said
  how: 'defines public function `test_a_declined_fallback_shows_what_the_verify_actually_said`
    at line 736, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_creates_no_branch
  how: 'defines public function `test_dry_run_creates_no_branch` at line 752, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_never_cuts_a_branch_in_the_graph_repo
  how: 'defines public function `test_the_fallback_never_cuts_a_branch_in_the_graph_repo`
    at line 765, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_stale_pending_branch_is_rebuilt_rather_than_extended
  how: 'defines public function `test_a_stale_pending_branch_is_rebuilt_rather_than_extended`
    at line 782, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _nodes_digest
  how: 'defines private function `_nodes_digest` at line 821, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _grid_tips
  how: 'defines private function `_grid_tips` at line 836, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scratch_dirs
  how: defines private function `_scratch_dirs` at line 841
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_contracts_disagree_refusal_leaves_nodes_byte_identical
  how: 'defines public function `test_a_contracts_disagree_refusal_leaves_nodes_byte_identical`
    at line 845, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_contracts_disagree_refusal_burns_no_grid_versions
  how: 'defines public function `test_a_contracts_disagree_refusal_burns_no_grid_versions`
    at line 860, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_says_that_it_wrote_nothing
  how: 'defines public function `test_a_refusal_says_that_it_wrote_nothing` at line
    872, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_scratch_worktree_never_survives_the_run
  how: 'defines public function `test_the_scratch_worktree_never_survives_the_run`
    at line 884, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_derivation_never_touches_the_real_nodes_dir
  how: 'defines public function `test_the_derivation_never_touches_the_real_nodes_dir`
    at line 898, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_happy_path_still_applies_publishes_and_commits
  how: 'defines public function `test_the_happy_path_still_applies_publishes_and_commits`
    at line 911, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_successful_run_applies_the_derivations_prunes_too
  how: 'defines public function `test_a_successful_run_applies_the_derivations_prunes_too`
    at line 932, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_file_authored_under_payloads_still_publishes
  how: 'defines public function `test_a_file_authored_under_payloads_still_publishes`
    at line 948, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_newly_minted_node_is_all_a_refusal_may_leave
  how: 'defines public function `test_a_newly_minted_node_is_all_a_refusal_may_leave`
    at line 968, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_writes_neither_nodes_nor_grid_versions
  how: 'defines public function `test_dry_run_writes_neither_nodes_nor_grid_versions`
    at line 989, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_does_not_adopt_a_newly_minted_node
  how: 'defines public function `test_dry_run_does_not_adopt_a_newly_minted_node`
    at line 1007, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _repo_with_upstream
  how: 'defines private function `_repo_with_upstream` at line 1028, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _commits
  how: 'defines private function `_commits` at line 1048, signature: (root: Path,
    n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unpushed_commits_counts_what_the_remote_does_not_have
  how: 'defines public function `test_unpushed_commits_counts_what_the_remote_does_not_have`
    at line 1061, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pushing_takes_the_number_back_to_zero
  how: 'defines public function `test_pushing_takes_the_number_back_to_zero` at line
    1071, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_upstream_is_not_zero
  how: 'defines public function `test_no_upstream_is_not_zero` at line 1087, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_detached_head_is_not_zero
  how: 'defines public function `test_detached_head_is_not_zero` at line 1101, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_path_that_is_not_a_git_repo_is_not_zero
  how: 'defines public function `test_a_path_that_is_not_a_git_repo_is_not_zero` at
    line 1112, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_missing_engine_clone_is_not_zero_and_does_not_crash
  how: 'defines public function `test_a_missing_engine_clone_is_not_zero_and_does_not_crash`
    at line 1118, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_engine_dir_inside_the_graph_repo_never_answers_for_the_graph
  how: 'defines public function `test_an_engine_dir_inside_the_graph_repo_never_answers_for_the_graph`
    at line 1125, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_symlinked_engine_clone_still_measures
  how: 'defines public function `test_a_symlinked_engine_clone_still_measures` at
    line 1140, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_unknown_sentinel_cannot_be_mistaken_for_a_measurement
  how: 'defines public function `test_the_unknown_sentinel_cannot_be_mistaken_for_a_measurement`
    at line 1154, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_measuring_the_gap_makes_no_network_call
  how: 'defines public function `test_measuring_the_gap_makes_no_network_call` at
    line 1164, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_gap_is_still_measurable_with_an_unreachable_remote
  how: 'defines public function `test_the_gap_is_still_measurable_with_an_unreachable_remote`
    at line 1187, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_repos_are_covered
  how: 'defines public function `test_both_repos_are_covered` at line 1207, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_project_with_no_engine_clone_reports_unknown_on_that_half_only
  how: 'defines public function `test_a_project_with_no_engine_clone_reports_unknown_on_that_half_only`
    at line 1229, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_compute_and_emit_carry_the_push_gap
  how: 'defines public function `test_compute_and_emit_carry_the_push_gap` at line
    1243, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_non_project_does_not_crash_the_metrics_stage
  how: 'defines public function `test_a_non_project_does_not_crash_the_metrics_stage`
    at line 1257, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_reason_survives_as_one_metric_token
  how: 'defines public function `test_the_reason_survives_as_one_metric_token` at
    line 1266, signature: (project, key)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _emit_with_gap
  how: 'defines private function `_emit_with_gap` at line 1282, signature: (project,
    capsys, **stats)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_large_gap_shouts
  how: 'defines public function `test_a_large_gap_shouts` at line 1295, signature:
    (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_healthy_repo_is_silent
  how: 'defines public function `test_a_healthy_repo_is_silent` at line 1302, signature:
    (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_one_cycle_of_ordinary_work_does_not_shout
  how: 'defines public function `test_one_cycle_of_ordinary_work_does_not_shout` at
    line 1308, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_threshold_would_have_caught_the_real_outage
  how: 'defines public function `test_the_threshold_would_have_caught_the_real_outage`
    at line 1319, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_unmeasurable_gap_does_not_shout
  how: 'defines public function `test_an_unmeasurable_gap_does_not_shout` at line
    1326, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _hook_project
  how: 'defines private function `_hook_project` at line 1344, signature: (tmp_path,
    graph_gap: int, engine_gap: int | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_when_commits_are_stranded
  how: 'defines public function `test_the_hook_shouts_when_commits_are_stranded` at
    line 1365, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_quiet_when_nothing_is_stranded
  how: 'defines public function `test_the_hook_is_quiet_when_nothing_is_stranded`
    at line 1381, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_quiet_on_a_project_it_cannot_measure
  how: 'defines public function `test_the_hook_is_quiet_on_a_project_it_cannot_measure`
    at line 1391, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_and_the_metric_cannot_disagree_about_the_threshold
  how: 'defines public function `test_the_hook_and_the_metric_cannot_disagree_about_the_threshold`
    at line 1402, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_still_a_silent_no_op_outside_a_project
  how: 'defines public function `test_the_hook_is_still_a_silent_no_op_outside_a_project`
    at line 1412, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 98'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(json.dumps(fields), encoding="utf-8")` at line 107'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "agi-tree.config.json"
  how: '`(root / "agi-tree.config.json").write_text("{}")` at line 124'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "n.md"
  how: '`(root / "nodes" / "n.md").write_text(''---\nid: "goal:n"\ntype: goal\n---\n\nbody\n'')`
    at line 125'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("{not json at all")` at line 211'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: outside / "context" / "publish-state.json"
  how: '`(outside / "context" / "publish-state.json").write_text( json.dumps({"last_run_status":
    "refused", "last_run_reason": "graph-dirty"}))` at line 381'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 389'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 417'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 431'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 443'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / STATE_REL
  how: '`(project / STATE_REL).write_text("{ truncated")` at line 444'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 455'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "agi-tree.config.json"
  how: '`(project / "agi-tree.config.json").write_text("{}")` at line 517'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/bin/foo.py"
  how: '`(engine / "extensions/agi/bin/foo.py").write_text("import os\n\n\ndef foo():\n    return
    2\n")` at line 680'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/src/pkg/bar.py"
  how: '`(engine / "extensions/agi/src/pkg/bar.py").write_text("# master moved on\n")`
    at line 795'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fresh
  how: '`fresh.write_text(NEW_PAYLOAD, encoding="utf-8")` at line 958'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fresh
  how: '`fresh.write_text(NEW_PAYLOAD, encoding="utf-8")` at line 975'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fresh
  how: '`fresh.write_text(NEW_PAYLOAD, encoding="utf-8")` at line 1012'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "f.txt"
  how: '`(root / "f.txt").write_text("0\n")` at line 1040'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / "f.txt"
  how: '`(repo / "f.txt").write_text("0\n")` at line 1094'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "agi-tree.config.json"
  how: '`(graph / "agi-tree.config.json").write_text("{}")` at line 1214'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "agi-tree.config.json"
  how: '`(graph / "agi-tree.config.json").write_text("{}")` at line 1350'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "context" / "INJECTION.md"
  how: '`(graph / "context" / "INJECTION.md").write_text("map\n")` at line 1369'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "context" / "INJECTION.md"
  how: '`(graph / "context" / "INJECTION.md").write_text("map\n")` at line 1383'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "context" / "INJECTION.md"
  how: '`(graph / "context" / "INJECTION.md").write_text("map\n")` at line 1394'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(fields)` at line 107'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"last_run_status": "refused", "last_run_reason": "graph-dirty"})`
    at line 382'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(text, encoding="utf-8")` at line 510'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / "build" / f"{slug}.md"
  how: '`(project / "nodes" / "build" / f"{slug}.md").write_text(text, encoding="utf-8")`
    at line 529'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/bin/foo.py"
  how: '`(engine / "extensions/agi/bin/foo.py").write_text("# stale\n", encoding="utf-8")`
    at line 536'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "f.txt"
  how: '`(root / "f.txt").write_text(f"work {i}\n")` at line 1054'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(text, encoding="utf-8")` at line 522'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
