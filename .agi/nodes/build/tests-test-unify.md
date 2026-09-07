---
id: build:tests-test-unify
mint_id: a2c72e35f9de48f1a04be896c0643dc7
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_unify.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_unify.py"
---
`extensions/agi/tests/test_unify.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_unify.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hashlib
  how: '`import hashlib` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: unify
  how: '`import unify` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / ".gitignore"
  how: '`(engine / ".gitignore").read_text()` at line 374'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(capsys.readouterr().out)` at line 522'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(prestate_file.read_text())` at line 672'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(capsys.readouterr().out)` at line 813'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(capsys.readouterr().out)` at line 818'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "GOALS.md"
  how: '`(engine / "GOALS.md").read_text()` at line 268'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / ".agi" / "config.json"
  how: '`(engine / ".agi" / "config.json").read_text()` at line 275'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "CLAUDE.md"
  how: '`(engine / "CLAUDE.md").read_text()` at line 547'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prestate_file
  how: '`prestate_file.read_text()` at line 672'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "CLAUDE.md"
  how: '`(engine / "CLAUDE.md").read_text()` at line 1018'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parked / "CLAUDE.md"
  how: '`(parked / "CLAUDE.md").read_text()` at line 1022'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / ".gitignore"
  how: '`(engine / ".gitignore").read_text()` at line 1007'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 171'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _git
  how: 'defines private function `_git` at line 33, signature: (repo: Path, *args:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rev_parse
  how: 'defines private function `_rev_parse` at line 43, signature: (repo: Path,
    ref: str=''HEAD'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: make_tree_repo
  how: 'defines public function `make_tree_repo` at line 94, signature: (tmp_path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _root_commit
  how: 'defines private function `_root_commit` at line 137, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: make_engine_repo
  how: 'defines public function `make_engine_repo` at line 144, signature: (tmp_path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _hash_tree
  how: 'defines private function `_hash_tree` at line 165, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _add_payload_node
  how: 'defines private function `_add_payload_node` at line 175, signature: (tree:
    Path, node_name: str, payload_ref: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _fingerprint
  how: 'defines private function `_fingerprint` at line 193, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repos
  how: 'defines public function `repos` at line 209, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: migrated
  how: 'defines public function `migrated` at line 216, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_histories_are_ancestors_of_head
  how: 'defines public function `test_both_histories_are_ancestors_of_head` at line
    236, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_grid_refs_transfer_with_count_and_target_preserved
  how: 'defines public function `test_grid_refs_transfer_with_count_and_target_preserved`
    at line 252, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goals_md_ends_at_repo_root_not_inside_dot_agi
  how: 'defines public function `test_goals_md_ends_at_repo_root_not_inside_dot_agi`
    at line 264, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_config_ends_at_dot_agi_config_json
  how: 'defines public function `test_config_ends_at_dot_agi_config_json` at line
    271, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_find_project_root_resolves_to_dot_agi
  how: 'defines public function `test_find_project_root_resolves_to_dot_agi` at line
    278, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_node_file_bytes_change
  how: 'defines public function `test_no_node_file_bytes_change` at line 287, signature:
    (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_report_node_count_matches
  how: 'defines public function `test_report_node_count_matches` at line 294, signature:
    (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_drops_symlink_entries
  how: defines public function `test_merge_gitignore_drops_symlink_entries` at line
    301
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_reroots_generated_paths
  how: defines public function `test_merge_gitignore_reroots_generated_paths` at line
    308
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_reroot_beats_dedup_for_names_shared_with_the_engine
  how: defines public function `test_merge_gitignore_reroot_beats_dedup_for_names_shared_with_the_engine`
    at line 322
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_dedupes_generic_patterns
  how: defines public function `test_merge_gitignore_dedupes_generic_patterns` at
    line 336
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_keeps_uniques_from_both_sides
  how: defines public function `test_merge_gitignore_keeps_uniques_from_both_sides`
    at line 342
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_drops_the_engines_claude_md_block
  how: defines public function `test_merge_gitignore_drops_the_engines_claude_md_block`
    at line 348
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_preserves_explanatory_comments
  how: defines public function `test_merge_gitignore_preserves_explanatory_comments`
    at line 365
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_end_to_end_gitignore_is_one_file_at_root
  how: 'defines public function `test_end_to_end_gitignore_is_one_file_at_root` at
    line 370, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_mutates_nothing
  how: 'defines public function `test_dry_run_mutates_nothing` at line 382, signature:
    (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_explicit_dry_run_flag_overrides_yes
  how: 'defines public function `test_explicit_dry_run_flag_overrides_yes` at line
    397, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_dirty_target
  how: 'defines public function `test_preflight_refuses_dirty_target` at line 410,
    signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_target_that_already_has_dot_agi
  how: 'defines public function `test_preflight_refuses_target_that_already_has_dot_agi`
    at line 418, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_missing_source
  how: 'defines public function `test_preflight_refuses_missing_source` at line 426,
    signature: (tmp_path, repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_dirty_source
  how: 'defines public function `test_preflight_refuses_dirty_source` at line 434,
    signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_force_allows_dirty_and_existing_agi
  how: 'defines public function `test_preflight_force_allows_dirty_and_existing_agi`
    at line 442, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_the_real_repos
  how: 'defines public function `test_preflight_refuses_the_real_repos` at line 450,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_force_does_not_bypass_real_repo_guard
  how: 'defines public function `test_preflight_force_does_not_bypass_real_repo_guard`
    at line 462, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_second_run_refuses_cleanly
  how: 'defines public function `test_second_run_refuses_cleanly` at line 472, signature:
    (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_graft_graph_alone
  how: 'defines public function `test_graft_graph_alone` at line 490, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_relocate_files_requires_a_prior_graft
  how: 'defines public function `test_relocate_files_requires_a_prior_graft` at line
    498, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_fetch_grid_refs_raises_on_a_bad_remote
  how: 'defines public function `test_fetch_grid_refs_raises_on_a_bad_remote` at line
    505, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_report_json_on_dry_run
  how: 'defines public function `test_cli_report_json_on_dry_run` at line 517, signature:
    (repos, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_yes_runs_the_real_migration
  how: 'defines public function `test_cli_yes_runs_the_real_migration` at line 526,
    signature: (repos, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_claude_md_ends_at_repo_root_not_inside_dot_agi
  how: 'defines public function `test_claude_md_ends_at_repo_root_not_inside_dot_agi`
    at line 543, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_agents_md_ends_at_repo_root_not_inside_dot_agi
  how: 'defines public function `test_agents_md_ends_at_repo_root_not_inside_dot_agi`
    at line 550, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_agents_md_is_still_a_symlink_after_the_move
  how: 'defines public function `test_agents_md_is_still_a_symlink_after_the_move`
    at line 556, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_relocate_files_raises_when_claude_md_missing
  how: 'defines public function `test_relocate_files_raises_when_claude_md_missing`
    at line 564, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_relocate_files_raises_when_agents_md_is_not_a_symlink
  how: 'defines public function `test_relocate_files_raises_when_agents_md_is_not_a_symlink`
    at line 574, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_when_a_payload_ref_is_missing_from_the_engine
  how: 'defines public function `test_preflight_refuses_when_a_payload_ref_is_missing_from_the_engine`
    at line 597, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_names_up_to_ten_and_the_true_count
  how: 'defines public function `test_preflight_refuses_names_up_to_ten_and_the_true_count`
    at line 612, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_passes_when_every_payload_ref_resolves
  how: 'defines public function `test_preflight_passes_when_every_payload_ref_resolves`
    at line 625, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_force_overrides_the_publish_lag_gate
  how: 'defines public function `test_force_overrides_the_publish_lag_gate` at line
    635, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_publish_lag_gate_blocks_the_real_migration_without_force
  how: 'defines public function `test_publish_lag_gate_blocks_the_real_migration_without_force`
    at line 644, signature: (repos, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_find_missing_payloads_is_empty_when_tree_has_no_payload_refs
  how: 'defines public function `test_find_missing_payloads_is_empty_when_tree_has_no_payload_refs`
    at line 655, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prestate_file_written_by_a_real_migration
  how: 'defines public function `test_prestate_file_written_by_a_real_migration` at
    line 663, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rollback_restores_head_and_deletes_grid_refs_and_is_clean
  how: 'defines public function `test_rollback_restores_head_and_deletes_grid_refs_and_is_clean`
    at line 689, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rollback_fingerprint_is_byte_identical_to_pre_migration
  how: 'defines public function `test_rollback_fingerprint_is_byte_identical_to_pre_migration`
    at line 709, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rollback_dry_run_mutates_nothing
  how: 'defines public function `test_rollback_dry_run_mutates_nothing` at line 725,
    signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rollback_refuses_with_no_prestate_file
  how: 'defines public function `test_rollback_refuses_with_no_prestate_file` at line
    741, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rollback_refuses_when_already_rolled_back
  how: 'defines public function `test_rollback_refuses_when_already_rolled_back` at
    line 749, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rollback_refuses_when_head_is_reachable_from_a_remote
  how: 'defines public function `test_rollback_refuses_when_head_is_reachable_from_a_remote`
    at line 762, signature: (repos, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_force_overrides_the_pushed_check_with_a_loud_warning
  how: 'defines public function `test_force_overrides_the_pushed_check_with_a_loud_warning`
    at line 787, signature: (repos, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rollback_cli_flag_end_to_end
  how: 'defines public function `test_rollback_cli_flag_end_to_end` at line 807, signature:
    (repos, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_rollback_requires_engine_only_not_tree
  how: 'defines public function `test_cli_rollback_requires_engine_only_not_tree`
    at line 824, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_main_errors_without_tree_and_without_rollback
  how: 'defines public function `test_main_errors_without_tree_and_without_rollback`
    at line 836, signature: (repos, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _make_build_node_with_payload
  how: 'defines private function `_make_build_node_with_payload` at line 851, signature:
    (tree: Path, engine: Path, *, mint: str, ref: str, grid_bytes: bytes, engine_bytes:
    bytes)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_stale_payload_is_detected
  how: 'defines public function `test_stale_payload_is_detected` at line 889, signature:
    (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_published_payload_is_not_stale
  how: 'defines public function `test_published_payload_is_not_stale` at line 900,
    signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_on_stale_payload
  how: 'defines public function `test_preflight_refuses_on_stale_payload` at line
    909, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_force_overrides_the_stale_gate
  how: 'defines public function `test_force_overrides_the_stale_gate` at line 922,
    signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_without_a_grid_ref_is_skipped_not_flagged
  how: 'defines public function `test_node_without_a_grid_ref_is_skipped_not_flagged`
    at line 931, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_force_does_not_unlock_the_real_repo_guard
  how: 'defines public function `test_force_does_not_unlock_the_real_repo_guard` at
    line 953, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_real_migration_flag_does_unlock_it
  how: 'defines public function `test_the_real_migration_flag_does_unlock_it` at line
    972, signature: (tmp_path, monkeypatch, repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rollback_guard_has_the_same_door
  how: 'defines public function `test_rollback_guard_has_the_same_door` at line 982,
    signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ignored_file_at_the_destination_is_displaced_not_fatal
  how: 'defines public function `test_ignored_file_at_the_destination_is_displaced_not_fatal`
    at line 995, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_tracked_file_at_the_destination_is_never_displaced
  how: 'defines public function `test_tracked_file_at_the_destination_is_never_displaced`
    at line 1025, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merged_gitignore_stops_ignoring_claude_md
  how: 'defines public function `test_merged_gitignore_stops_ignoring_claude_md` at
    line 1038, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "agi-tree.config.json"
  how: '`(d / "agi-tree.config.json").write_text(''{"metric_primary": "outcome_coverage"}\n'')`
    at line 101'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "GOALS.md"
  how: '`(d / "GOALS.md").write_text("# GOALS\n\n## G1: something\n")` at line 102'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / ".gitignore"
  how: '`(d / ".gitignore").write_text(TREE_GITIGNORE)` at line 103'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "CLAUDE.md"
  how: '`(d / "CLAUDE.md").write_text("# CLAUDE.md\n\nProject instructions.\n")` at
    line 108'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goal_dir / "g1.md"
  how: '`(goal_dir / "g1.md").write_text( ''---\nid: "goal:g1"\nmint_id: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\ntype:
    goal\n'' ''---\n\nfirst version of g1\n'' )` at line 112'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: kits_dir / "example.md"
  how: '`(kits_dir / "example.md").write_text("a kit\n")` at line 118'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goal_dir / "g1.md"
  how: '`(goal_dir / "g1.md").write_text( ''---\nid: "goal:g1"\nmint_id: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\ntype:
    goal\n'' ''---\n\nsecond version of g1, edited\n'' )` at line 124'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / ".gitignore"
  how: '`(d / ".gitignore").write_text(ENGINE_GITIGNORE)` at line 151'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ext / "hello.py"
  how: '`(ext / "hello.py").write_text("print(''hello'')\n")` at line 154'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ext / "hello.py"
  how: '`(ext / "hello.py").write_text("print(''hello world'')\n")` at line 159'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text( f''---\nid: "build:{node_name}"\n'' f''mint_id: cccccccccccccccccccccccccccccccc\ntype:
    build\n'' f''payload_ref: {payload_ref}\n---\n\nBuild node.\n'' )` at line 183'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions" / "agi" / "bin" / "hello.py"
  how: '`(engine / "extensions" / "agi" / "bin" / "hello.py").write_text("dirty\n")`
    at line 412'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tree / "nodes" / "goal" / "g1.md"
  how: '`(tree / "nodes" / "goal" / "g1.md").write_text("uncommitted edit\n")` at
    line 436'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions" / "agi" / "bin" / "hello.py"
  how: '`(engine / "extensions" / "agi" / "bin" / "hello.py").write_text("dirty\n")`
    at line 445'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: agents
  how: '`agents.write_text("not a symlink\n")` at line 582'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_dir / f"{mint}.md"
  how: '`(build_dir / f"{mint}.md").write_text( f''---\nid: "build:{mint}"\nmint_id:
    {mint}\ntype: build\n'' f''payload_ref: {ref}\n---\n\nbuild node\n'' )` at line
    859'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.write_bytes(engine_bytes)` at line 884'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_dir / "ungridded.md"
  how: '`(build_dir / "ungridded.md").write_text( ''---\nid: "build:ungridded"\nmint_id:
    '' + "9" * 32 + ''\ntype: build\n'' ''payload_ref: src/ungridded.py\n---\n\nno
    grid ref for this one\n'' )` at line 939'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "src" / "ungridded.py"
  how: '`(engine / "src" / "ungridded.py").write_text("whatever\n")` at line 946'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / ".gitignore"
  how: '`(engine / ".gitignore").write_text( (engine / ".gitignore").read_text() +
    "\nCLAUDE.md\nAGENTS.md\n")` at line 1006'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "CLAUDE.md"
  how: '`(engine / "CLAUDE.md").write_text("engine''s own generated copy\n")` at line
    1009'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "AGENTS.md"
  how: '`(engine / "AGENTS.md").write_text("engine''s own generated copy\n")` at line
    1010'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "GOALS.md"
  how: '`(engine / "GOALS.md").write_text("the engine''s own tracked GOALS\n")` at
    line 1029'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.