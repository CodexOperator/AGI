---
id: build:tests-test-publish-alarm
mint_id: 8053b4cdd5b8421996fc4f66656c5d9d
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_publish_alarm.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_publish_alarm.py"
---
`extensions/agi/tests/test_publish_alarm.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

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
  how: '`(root / STATE_REL).read_text()` at line 259'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: HOOK_SH
  how: '`HOOK_SH.read_text(encoding="utf-8")` at line 1290'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / STATE_REL
  how: '`(root / STATE_REL).read_text(encoding="utf-8")` at line 112'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / STATE_REL
  how: '`(root / STATE_REL).read_text()` at line 263'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/bin/foo.py"
  how: '`(engine / "extensions/agi/bin/foo.py").read_text()` at line 837'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/bin/fresh.py"
  how: '`(engine / "extensions/agi/bin/fresh.py").read_text()` at line 877'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 744'
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
- name: test_publish_stats_no_longer_exists_on_metrics
  how: defines public function `test_publish_stats_no_longer_exists_on_metrics` at
    line 168
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_retired_publish_metrics_are_not_emitted
  how: 'defines public function `test_the_retired_publish_metrics_are_not_emitted`
    at line 177, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_compute_no_longer_carries_the_publish_alarm
  how: 'defines public function `test_compute_no_longer_carries_the_publish_alarm`
    at line 190, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_exits_non_zero
  how: 'defines public function `test_a_refusal_exits_non_zero` at line 199, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_writes_a_machine_readable_marker
  how: 'defines public function `test_a_refusal_writes_a_machine_readable_marker`
    at line 206, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_marker_is_not_written_under_nodes
  how: 'defines public function `test_the_marker_is_not_written_under_nodes` at line
    216, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_refusal_says_the_bytes_are_safe
  how: 'defines public function `test_the_refusal_says_the_bytes_are_safe` at line
    228, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_does_not_erase_the_last_real_publish
  how: 'defines public function `test_a_refusal_does_not_erase_the_last_real_publish`
    at line 240, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_never_touches_the_marker
  how: 'defines public function `test_dry_run_never_touches_the_marker` at line 254,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_gate_zero_is_still_a_refusal
  how: 'defines public function `test_gate_zero_is_still_a_refusal` at line 266, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_a_silent_no_op_outside_a_project
  how: 'defines public function `test_the_hook_is_a_silent_no_op_outside_a_project`
    at line 281, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_stays_silent_outside_a_project_even_with_a_stray_marker
  how: 'defines public function `test_the_hook_stays_silent_outside_a_project_even_with_a_stray_marker`
    at line 293, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_when_the_publish_is_stalled
  how: 'defines public function `test_the_hook_shouts_when_the_publish_is_stalled`
    at line 305, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_even_when_there_is_no_map_to_inject
  how: 'defines public function `test_the_hook_shouts_even_when_there_is_no_map_to_inject`
    at line 321, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_quiet_when_the_publish_is_healthy
  how: 'defines public function `test_the_hook_is_quiet_when_the_publish_is_healthy`
    at line 333, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_when_the_cron_itself_has_stopped
  how: 'defines public function `test_the_hook_shouts_when_the_cron_itself_has_stopped`
    at line 345, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_corrupt_marker_does_not_break_the_hook
  how: 'defines public function `test_a_corrupt_marker_does_not_break_the_hook` at
    line 357, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_marker_means_no_banner
  how: 'defines public function `test_no_marker_means_no_banner` at line 367, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_out
  how: 'defines private function `_git_out` at line 391, signature: (root: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _init_repo
  how: 'defines private function `_init_repo` at line 396, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pair
  how: 'defines private function `_pair` at line 402, signature: (tmp_path, engine_lags:
    bool=True, extra_nodes: dict | None=None, staged: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pending
  how: 'defines private function `_pending` at line 455, signature: (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _dirty_a_node
  how: 'defines private function `_dirty_a_node` at line 459, signature: (project:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _publish
  how: 'defines private function `_publish` at line 466, signature: (project: Path,
    engine: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_blocked_publish_parks_the_bytes_instead_of_stranding_them
  how: 'defines public function `test_a_blocked_publish_parks_the_bytes_instead_of_stranding_them`
    at line 470, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_never_writes_the_default_branch
  how: 'defines public function `test_the_fallback_never_writes_the_default_branch`
    at line 487, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_leaves_the_engine_checkout_exactly_where_it_was
  how: 'defines public function `test_the_fallback_leaves_the_engine_checkout_exactly_where_it_was`
    at line 499, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_leaves_no_worktree_behind
  how: 'defines public function `test_the_fallback_leaves_no_worktree_behind` at line
    515, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parking_the_bytes_does_not_make_the_alarm_read_healthy
  how: 'defines public function `test_parking_the_bytes_does_not_make_the_alarm_read_healthy`
    at line 531, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_marker_says_where_the_parked_bytes_went
  how: 'defines public function `test_the_marker_says_where_the_parked_bytes_went`
    at line 550, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_second_run_at_the_same_dirty_state_does_not_commit_again
  how: 'defines public function `test_a_second_run_at_the_same_dirty_state_does_not_commit_again`
    at line 565, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_moving_grid_does_add_a_second_commit
  how: 'defines public function `test_a_moving_grid_does_add_a_second_commit` at line
    583, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_pending_branch_can_still_be_fast_forwarded
  how: 'defines public function `test_the_pending_branch_can_still_be_fast_forwarded`
    at line 601, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_parked_commit_does_not_claim_the_graph_sha_describes_it
  how: 'defines public function `test_the_parked_commit_does_not_claim_the_graph_sha_describes_it`
    at line 614, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_parks_nothing_the_real_publish_would_refuse
  how: 'defines public function `test_the_fallback_parks_nothing_the_real_publish_would_refuse`
    at line 631, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_declined_fallback_shows_what_the_verify_actually_said
  how: 'defines public function `test_a_declined_fallback_shows_what_the_verify_actually_said`
    at line 649, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_creates_no_branch
  how: 'defines public function `test_dry_run_creates_no_branch` at line 665, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_fallback_never_cuts_a_branch_in_the_graph_repo
  how: 'defines public function `test_the_fallback_never_cuts_a_branch_in_the_graph_repo`
    at line 678, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_stale_pending_branch_is_rebuilt_rather_than_extended
  how: 'defines public function `test_a_stale_pending_branch_is_rebuilt_rather_than_extended`
    at line 695, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _nodes_digest
  how: 'defines private function `_nodes_digest` at line 734, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _grid_tips
  how: 'defines private function `_grid_tips` at line 749, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scratch_dirs
  how: defines private function `_scratch_dirs` at line 754
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_contracts_disagree_refusal_leaves_nodes_byte_identical
  how: 'defines public function `test_a_contracts_disagree_refusal_leaves_nodes_byte_identical`
    at line 758, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_contracts_disagree_refusal_burns_no_grid_versions
  how: 'defines public function `test_a_contracts_disagree_refusal_burns_no_grid_versions`
    at line 773, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refusal_says_that_it_wrote_nothing
  how: 'defines public function `test_a_refusal_says_that_it_wrote_nothing` at line
    785, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_scratch_worktree_never_survives_the_run
  how: 'defines public function `test_the_scratch_worktree_never_survives_the_run`
    at line 797, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_derivation_never_touches_the_real_nodes_dir
  how: 'defines public function `test_the_derivation_never_touches_the_real_nodes_dir`
    at line 811, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_happy_path_still_applies_publishes_and_commits
  how: 'defines public function `test_the_happy_path_still_applies_publishes_and_commits`
    at line 824, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_successful_run_applies_the_derivations_prunes_too
  how: 'defines public function `test_a_successful_run_applies_the_derivations_prunes_too`
    at line 845, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_file_authored_under_payloads_still_publishes
  how: 'defines public function `test_a_file_authored_under_payloads_still_publishes`
    at line 861, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_newly_minted_node_is_all_a_refusal_may_leave
  how: 'defines public function `test_a_newly_minted_node_is_all_a_refusal_may_leave`
    at line 881, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_writes_neither_nodes_nor_grid_versions
  how: 'defines public function `test_dry_run_writes_neither_nodes_nor_grid_versions`
    at line 902, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_does_not_adopt_a_newly_minted_node
  how: 'defines public function `test_dry_run_does_not_adopt_a_newly_minted_node`
    at line 920, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _repo_with_upstream
  how: 'defines private function `_repo_with_upstream` at line 941, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _commits
  how: 'defines private function `_commits` at line 961, signature: (root: Path, n:
    int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unpushed_commits_counts_what_the_remote_does_not_have
  how: 'defines public function `test_unpushed_commits_counts_what_the_remote_does_not_have`
    at line 974, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pushing_takes_the_number_back_to_zero
  how: 'defines public function `test_pushing_takes_the_number_back_to_zero` at line
    984, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_upstream_is_not_zero
  how: 'defines public function `test_no_upstream_is_not_zero` at line 1000, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_detached_head_is_not_zero
  how: 'defines public function `test_detached_head_is_not_zero` at line 1014, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_path_that_is_not_a_git_repo_is_not_zero
  how: 'defines public function `test_a_path_that_is_not_a_git_repo_is_not_zero` at
    line 1025, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_missing_engine_clone_is_not_zero_and_does_not_crash
  how: 'defines public function `test_a_missing_engine_clone_is_not_zero_and_does_not_crash`
    at line 1031, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_engine_dir_inside_the_graph_repo_never_answers_for_the_graph
  how: 'defines public function `test_an_engine_dir_inside_the_graph_repo_never_answers_for_the_graph`
    at line 1038, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_symlinked_engine_clone_still_measures
  how: 'defines public function `test_a_symlinked_engine_clone_still_measures` at
    line 1053, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_unknown_sentinel_cannot_be_mistaken_for_a_measurement
  how: 'defines public function `test_the_unknown_sentinel_cannot_be_mistaken_for_a_measurement`
    at line 1067, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_measuring_the_gap_makes_no_network_call
  how: 'defines public function `test_measuring_the_gap_makes_no_network_call` at
    line 1077, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_gap_is_still_measurable_with_an_unreachable_remote
  how: 'defines public function `test_the_gap_is_still_measurable_with_an_unreachable_remote`
    at line 1100, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_push_gap_stats_measures_the_projects_own_repo
  how: 'defines public function `test_push_gap_stats_measures_the_projects_own_repo`
    at line 1128, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_push_gap_stats_resolves_a_graph_dir_to_its_enclosing_repo
  how: 'defines public function `test_push_gap_stats_resolves_a_graph_dir_to_its_enclosing_repo`
    at line 1136, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_compute_and_emit_carry_the_push_gap
  how: 'defines public function `test_compute_and_emit_carry_the_push_gap` at line
    1155, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_non_project_does_not_crash_the_metrics_stage
  how: 'defines public function `test_a_non_project_does_not_crash_the_metrics_stage`
    at line 1166, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_reason_survives_as_one_metric_token
  how: 'defines public function `test_the_reason_survives_as_one_metric_token` at
    line 1172, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _emit_with_gap
  how: 'defines private function `_emit_with_gap` at line 1187, signature: (project,
    capsys, **stats)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_large_gap_shouts
  how: 'defines public function `test_a_large_gap_shouts` at line 1199, signature:
    (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_healthy_repo_is_silent
  how: 'defines public function `test_a_healthy_repo_is_silent` at line 1205, signature:
    (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_one_cycle_of_ordinary_work_does_not_shout
  how: 'defines public function `test_one_cycle_of_ordinary_work_does_not_shout` at
    line 1211, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_threshold_would_have_caught_the_real_outage
  how: 'defines public function `test_the_threshold_would_have_caught_the_real_outage`
    at line 1221, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_unmeasurable_gap_does_not_shout
  how: 'defines public function `test_an_unmeasurable_gap_does_not_shout` at line
    1228, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _hook_project
  how: 'defines private function `_hook_project` at line 1244, signature: (tmp_path,
    gap: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_shouts_when_commits_are_stranded
  how: 'defines public function `test_the_hook_shouts_when_commits_are_stranded` at
    line 1260, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_quiet_when_nothing_is_stranded
  how: 'defines public function `test_the_hook_is_quiet_when_nothing_is_stranded`
    at line 1276, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_and_the_metric_cannot_disagree_about_the_threshold
  how: 'defines public function `test_the_hook_and_the_metric_cannot_disagree_about_the_threshold`
    at line 1286, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_hook_is_still_a_silent_no_op_outside_a_project
  how: 'defines public function `test_the_hook_is_still_a_silent_no_op_outside_a_project`
    at line 1296, signature: (tmp_path)'
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
- name: outside / "context" / "publish-state.json"
  how: '`(outside / "context" / "publish-state.json").write_text( json.dumps({"last_run_status":
    "refused", "last_run_reason": "graph-dirty"}))` at line 298'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 306'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 334'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 348'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 360'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / STATE_REL
  how: '`(project / STATE_REL).write_text("{ truncated")` at line 361'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "INJECTION.md"
  how: '`(project / "context" / "INJECTION.md").write_text("map\n")` at line 371'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "agi-tree.config.json"
  how: '`(project / "agi-tree.config.json").write_text("{}")` at line 431'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/bin/foo.py"
  how: '`(engine / "extensions/agi/bin/foo.py").write_text("import os\n\n\ndef foo():\n    return
    2\n")` at line 593'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/src/pkg/bar.py"
  how: '`(engine / "extensions/agi/src/pkg/bar.py").write_text("# master moved on\n")`
    at line 708'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fresh
  how: '`fresh.write_text(NEW_PAYLOAD, encoding="utf-8")` at line 871'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fresh
  how: '`fresh.write_text(NEW_PAYLOAD, encoding="utf-8")` at line 888'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fresh
  how: '`fresh.write_text(NEW_PAYLOAD, encoding="utf-8")` at line 925'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "f.txt"
  how: '`(root / "f.txt").write_text("0\n")` at line 953'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / "f.txt"
  how: '`(repo / "f.txt").write_text("0\n")` at line 1007'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_dir / "config.json"
  how: '`(graph_dir / "config.json").write_text("{}")` at line 1148'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "agi-tree.config.json"
  how: '`(graph / "agi-tree.config.json").write_text("{}")` at line 1250'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "context" / "INJECTION.md"
  how: '`(graph / "context" / "INJECTION.md").write_text("map\n")` at line 1264'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "context" / "INJECTION.md"
  how: '`(graph / "context" / "INJECTION.md").write_text("map\n")` at line 1278'
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
    at line 299'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(text, encoding="utf-8")` at line 424'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / "build" / f"{slug}.md"
  how: '`(project / "nodes" / "build" / f"{slug}.md").write_text(text, encoding="utf-8")`
    at line 443'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions/agi/bin/foo.py"
  how: '`(engine / "extensions/agi/bin/foo.py").write_text("# stale\n", encoding="utf-8")`
    at line 450'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "f.txt"
  how: '`(root / "f.txt").write_text(f"work {i}\n")` at line 967'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(text, encoding="utf-8")` at line 436'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.