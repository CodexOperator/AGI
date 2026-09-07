---
id: build:tests-test-grid
mint_id: e13d59c2cdd94a09aed671ce4e8b0d10
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_grid.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_grid.py"
---
`extensions/agi/tests/test_grid.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_grid.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 3'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 4'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 5'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 6'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 7'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / "level3" / "plain.md"
  how: '`(project / "nodes" / "level3" / "plain.md").read_text()` at line 832'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / "level3" / "plain.md"
  how: '`(project / "nodes" / "level3" / "plain.md").read_text()` at line 842'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: staged
  how: '`staged.read_bytes()` at line 873'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: staged
  how: '`staged.read_bytes()` at line 881'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "bin" / "run.sh"
  how: '`(engine / "bin" / "run.sh").read_bytes()` at line 881'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.read_text()` at line 80'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 620'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 622'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 731'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 733'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 745'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out
  how: '`out.read_bytes()` at line 824'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.read_bytes()` at line 824'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.read_bytes()` at line 838'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.read_bytes()` at line 1088'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.read_text()` at line 69'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 477'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 489'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 521'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.read_text()` at line 964'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: project
  how: 'defines public function `project` at line 24, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: versions
  how: 'defines public function `versions` at line 36, signature: (root, node_id)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_init_idempotent_and_refuses_non_repo
  how: 'defines public function `test_init_idempotent_and_refuses_non_repo` at line
    46, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_commit_creates_version_and_skips_unchanged
  how: 'defines public function `test_commit_creates_version_and_skips_unchanged`
    at line 52, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_grid_refs_stay_out_of_branch_listing
  how: 'defines public function `test_grid_refs_stay_out_of_branch_listing` at line
    60, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_edit_makes_v2_and_diff_shows_it
  how: 'defines public function `test_edit_makes_v2_and_diff_shows_it` at line 66,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_session_branch_is_separate_dimension
  how: 'defines public function `test_session_branch_is_separate_dimension` at line
    77, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_without_id_is_skipped
  how: 'defines public function `test_node_without_id_is_skipped` at line 87, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_commit_prefix_marks_auto_snapshots
  how: 'defines public function `test_commit_prefix_marks_auto_snapshots` at line
    93, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_refuses_ref_hostile_chars
  how: defines public function `test_sanitize_refuses_ref_hostile_chars` at line 102
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cron_lines_are_cwd_proof
  how: 'defines public function `test_cron_lines_are_cwd_proof` at line 109, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_publish_engine_cron_also_pushes_the_engine
  how: 'defines public function `test_publish_engine_cron_also_pushes_the_engine`
    at line 120, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sync_pushes_grid_refs_and_sets_fetch_spec
  how: 'defines public function `test_sync_pushes_grid_refs_and_sets_fetch_spec` at
    line 152, signature: (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_find_project_root_accepts_canonical_and_legacy_config
  how: 'defines public function `test_find_project_root_accepts_canonical_and_legacy_config`
    at line 168, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_only_the_first_colon_separates
  how: defines public function `test_only_the_first_colon_separates` at line 185
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_node_ref_is_a_path_prefix_of_another
  how: defines public function `test_no_node_ref_is_a_path_prefix_of_another` at line
    198
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_is_injective_across_colon_and_dash
  how: defines public function `test_sanitize_is_injective_across_colon_and_dash`
    at line 208
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_escape_alphabet_cannot_be_forged
  how: defines public function `test_escape_alphabet_cannot_be_forged` at line 213
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_is_injective_over_adversarial_corpus
  how: defines public function `test_sanitize_is_injective_over_adversarial_corpus`
    at line 243
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_output_is_a_valid_git_refname
  how: defines public function `test_sanitize_output_is_a_valid_git_refname` at line
    252
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_real_agi_tree_corpus_round_trips_distinctly
  how: defines public function `test_sanitize_real_agi_tree_corpus_round_trips_distinctly`
    at line 267
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: migrate_project
  how: 'defines public function `migrate_project` at line 299, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_node
  how: 'defines private function `_write_node` at line 307, signature: (root, rel,
    node_id, body=''body\n'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_refs_dry_run_changes_nothing
  how: 'defines public function `test_migrate_refs_dry_run_changes_nothing` at line
    313, signature: (migrate_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_refs_write_moves_ref_and_preserves_history
  how: 'defines public function `test_migrate_refs_write_moves_ref_and_preserves_history`
    at line 326, signature: (migrate_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_refs_is_idempotent
  how: 'defines public function `test_migrate_refs_is_idempotent` at line 343, signature:
    (migrate_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_refs_refuses_to_overwrite_conflicting_destination
  how: 'defines public function `test_migrate_refs_refuses_to_overwrite_conflicting_destination`
    at line 358, signature: (migrate_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_refs_reports_collision_and_touches_neither_id
  how: 'defines public function `test_migrate_refs_reports_collision_and_touches_neither_id`
    at line 379, signature: (migrate_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_project
  how: 'defines public function `mint_project` at line 413, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_mint_node
  how: 'defines private function `_write_mint_node` at line 421, signature: (root,
    rel, node_id, mint_id=None, parents=None, body=''body\n'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_ref_for_raises_on_missing_mint_id
  how: 'defines public function `test_write_ref_for_raises_on_missing_mint_id` at
    line 434, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_ref_for_returns_mint_ref_when_present
  how: 'defines public function `test_write_ref_for_returns_mint_ref_when_present`
    at line 440, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_commit_all_skips_missing_mint_id_but_keeps_going
  how: 'defines public function `test_commit_all_skips_missing_mint_id_but_keeps_going`
    at line 445, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_commit_never_falls_back_to_node_id_ref_for_missing_mint_id
  how: 'defines public function `test_commit_never_falls_back_to_node_id_ref_for_missing_mint_id`
    at line 459, signature: (mint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_falls_back_to_legacy_ref_when_no_mint_ref_exists
  how: 'defines public function `test_read_falls_back_to_legacy_ref_when_no_mint_ref_exists`
    at line 469, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_versions_falls_back_to_legacy_ref
  how: 'defines public function `test_versions_falls_back_to_legacy_ref` at line 485,
    signature: (mint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_clean_via_legacy_ref_for_node_without_mint_id_yet
  how: 'defines public function `test_status_clean_via_legacy_ref_for_node_without_mint_id_yet`
    at line 498, signature: (mint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_falls_back_to_legacy_ref_instead_of_reporting_new
  how: 'defines public function `test_status_falls_back_to_legacy_ref_instead_of_reporting_new`
    at line 512, signature: (mint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_reports_new_when_neither_ref_exists
  how: 'defines public function `test_status_reports_new_when_neither_ref_exists`
    at line 531, signature: (mint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_mint_trailer_in_commit_body
  how: 'defines public function `test_parent_mint_trailer_in_commit_body` at line
    539, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_mint_trailer_marks_unresolved_parent
  how: 'defines public function `test_parent_mint_trailer_marks_unresolved_parent`
    at line 555, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_parents_means_no_trailer_body
  how: 'defines public function `test_no_parents_means_no_trailer_body` at line 566,
    signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_node_ref_is_a_valid_git_ref
  how: defines public function `test_mint_node_ref_is_a_valid_git_ref` at line 574
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_node_ref_is_identity_under_sanitize
  how: defines public function `test_mint_node_ref_is_identity_under_sanitize` at
    line 580
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: migmint_project
  how: 'defines public function `migmint_project` at line 596, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_dry_run_changes_nothing
  how: 'defines public function `test_migrate_mint_refs_dry_run_changes_nothing` at
    line 604, signature: (migmint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_write_moves_ref_and_preserves_full_history
  how: 'defines public function `test_migrate_mint_refs_write_moves_ref_and_preserves_full_history`
    at line 616, signature: (migmint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_is_idempotent
  how: 'defines public function `test_migrate_mint_refs_is_idempotent` at line 635,
    signature: (migmint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_second_run_reports_zero_moved
  how: 'defines public function `test_migrate_mint_refs_second_run_reports_zero_moved`
    at line 649, signature: (migmint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_refuses_to_overwrite_conflicting_destination
  how: 'defines public function `test_migrate_mint_refs_refuses_to_overwrite_conflicting_destination`
    at line 660, signature: (migmint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_conflict_is_reported
  how: 'defines public function `test_migrate_mint_refs_conflict_is_reported` at line
    679, signature: (migmint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_skips_node_without_mint_id_not_guessed
  how: 'defines public function `test_migrate_mint_refs_skips_node_without_mint_id_not_guessed`
    at line 692, signature: (migmint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_reports_duplicate_mint_id_collision
  how: 'defines public function `test_migrate_mint_refs_reports_duplicate_mint_id_collision`
    at line 707, signature: (migmint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_versions_and_log_report_full_history_after_migration
  how: 'defines public function `test_versions_and_log_report_full_history_after_migration`
    at line 724, signature: (migmint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine
  how: 'defines public function `engine` at line 764, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _payload_node
  how: 'defines private function `_payload_node` at line 777, signature: (project,
    name, node_id, payload_ref, mint_id=MINT_P)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_git_mode_reads_lstat_not_stat
  how: 'defines public function `test_git_mode_reads_lstat_not_stat` at line 787,
    signature: (engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_symlink_blob_is_link_text_not_target_bytes
  how: 'defines public function `test_symlink_blob_is_link_text_not_target_bytes`
    at line 795, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_payload_round_trips_with_mode
  how: 'defines public function `test_payload_round_trips_with_mode` at line 807,
    signature: (project, engine, tmp_path, name, ref, expect_mode)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_three_version_bumps_of_a_payload_are_three_versions
  how: 'defines public function `test_three_version_bumps_of_a_payload_are_three_versions`
    at line 827, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_payload_version_out_of_range_is_a_hard_error
  how: 'defines public function `test_payload_version_out_of_range_is_a_hard_error`
    at line 850, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_staged_payload_beats_the_engine_tree
  how: 'defines public function `test_staged_payload_beats_the_engine_tree` at line
    858, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_checkout_materializes_payloads_for_editing
  how: 'defines public function `test_checkout_materializes_payloads_for_editing`
    at line 876, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unresolvable_payload_ref_warns_and_still_commits_the_node
  how: 'defines public function `test_unresolvable_payload_ref_warns_and_still_commits_the_node`
    at line 885, signature: (project, engine, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_sees_a_payload_only_edit
  how: 'defines public function `test_status_sees_a_payload_only_edit` at line 897,
    signature: (project, engine, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_writes_no_objects
  how: 'defines public function `test_status_writes_no_objects` at line 909, signature:
    (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: g11
  how: 'defines public function `g11` at line 942, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _bump
  how: 'defines private function `_bump` at line 962, signature: (graph, text)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_repo_root_is_the_git_repo_never_the_graph_dir
  how: 'defines public function `test_repo_root_is_the_git_repo_never_the_graph_dir`
    at line 968, signature: (g11)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_git_invocation_ever_targets_the_graph_dir
  how: 'defines public function `test_no_git_invocation_ever_targets_the_graph_dir`
    at line 978, signature: (g11, monkeypatch, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_byte_identical_corpus_reports_zero_changed
  how: 'defines public function `test_byte_identical_corpus_reports_zero_changed`
    at line 1014, signature: (g11, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_reports_the_same_set_from_either_cwd
  how: 'defines public function `test_status_reports_the_same_set_from_either_cwd`
    at line 1027, signature: (g11, capsys, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_diff_reads_node_md_when_the_graph_is_a_subdirectory
  how: 'defines public function `test_diff_reads_node_md_when_the_graph_is_a_subdirectory`
    at line 1048, signature: (g11, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_payload_round_trips_with_no_staging_copy
  how: 'defines public function `test_payload_round_trips_with_no_staging_copy` at
    line 1069, signature: (g11, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cron_marker_distinguishes_two_migrated_projects
  how: 'defines public function `test_cron_marker_distinguishes_two_migrated_projects`
    at line 1095, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cron_lines_name_the_repo_under_the_g11_layout
  how: 'defines public function `test_cron_lines_name_the_repo_under_the_g11_layout`
    at line 1114, signature: (g11)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_find_project_root_honours_the_env_override
  how: 'defines public function `test_find_project_root_honours_the_env_override`
    at line 1125, signature: (g11, monkeypatch, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ensure_repo_names_the_repo_not_the_graph_dir
  how: 'defines public function `test_ensure_repo_names_the_repo_not_the_graph_dir`
    at line 1146, signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "x.md"
  how: '`(d / "x.md").write_text( f''---\nid: "idea:x"\nmint_id: {MINT_X}\ntype: idea\n---\n\nfirst
    thought\n'' )` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 47'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.write_text(f.read_text().replace("first thought", "second thought"))` at
    line 69'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.write_text(f.read_text() + "\ndraft addition\n")` at line 80'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / "idea" / "noid.md"
  how: '`(project / "nodes" / "idea" / "noid.md").write_text("no frontmatter here\n")`
    at line 88'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: canonical / "agi-tree.config.json"
  how: '`(canonical / "agi-tree.config.json").write_text("{}")` at line 176'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: legacy / "autoresearch-tree.config.json"
  how: '`(legacy / "autoresearch-tree.config.json").write_text("{}")` at line 177'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 301'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(f''---\nid: "{node_id}"\ntype: level3\n---\n\n{body}'')` at
    line 309'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 415'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("---\n" + "\n".join(fm) + f"\n---\n\n{body}")` at line 430'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text().replace( ''id: "idea:x"'', f''id: "idea:x"\nmint_id:
    {MINT_A}''))` at line 477'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text().replace( ''id: "idea:x"'', f''id: "idea:x"\nmint_id:
    {MINT_A}''))` at line 489'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text().replace( ''id: "idea:x"'', f''id: "idea:x"\nmint_id:
    {MINT_A}''))` at line 521'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 598'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text() + "\nedit 2\n")` at line 620'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text() + "\nedit 3\n")` at line 622'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text() + "\nedit 2\n")` at line 731'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text() + "\nedit 3\n")` at line 733'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text() + "\nedit 4\n")` at line 745'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "bin" / "plain.py"
  how: '`(root / "bin" / "plain.py").write_text("print(''v1'')\n")` at line 769'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: exe
  how: '`exe.write_text("#!/bin/sh\necho v1\n")` at line 771'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text( f''---\nid: "{node_id}"\nmint_id: {mint_id}\ntype: level3\n''
    f"payload_ref: {payload_ref}\n---\n\nbuild node\n" )` at line 780'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: staged
  how: '`staged.write_text("print(''edited in the graph'')\n")` at line 865'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "bin" / "plain.py"
  how: '`(engine / "bin" / "plain.py").write_text("print(''moved'')\n")` at line 904'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "bin" / "plain.py"
  how: '`(engine / "bin" / "plain.py").write_text("print(''moved'')\n")` at line 914'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / ".agi" / "config.json"
  how: '`(repo / ".agi" / "config.json").write_text("{}")` at line 953'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / ".agi" / "nodes" / "idea" / "x.md"
  how: '`(repo / ".agi" / "nodes" / "idea" / "x.md").write_text( f''---\nid: "idea:x"\nmint_id:
    {MINT_G11}\ntype: idea\n---\n\nfirst thought\n'' )` at line 954'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.write_text(f.read_text().replace("first thought", text))` at line 964'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.write_text("print(''v1'')\n")` at line 1076'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node
  how: '`node.write_text( f''---\nid: "level3:thing"\nmint_id: {MINT_P}\ntype: level3\n''
    f"payload_ref: extensions/agi/bin/thing.py\n---\n\nbuild node\n" )` at line 1079'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "config.json"
  how: '`(graph / "config.json").write_text("{}")` at line 1152'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.write_text(f"print(''v{n}'')\n# éà中文 {n}\n")` at line 837'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.