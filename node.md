---
id: build:tests-test-legacy
mint_id: 0bc74393622c4afebd87a7f8583a8895
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: director-general-1
origin: build-scan
payload_ref: extensions/agi/tests/test_legacy.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_legacy.py"
---
`extensions/agi/tests/test_legacy.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_legacy.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shutil
  how: '`import shutil` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stat
  how: '`import stat` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "viewport.py"
  how: '`(BIN / "viewport.py").read_text()` at line 572'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Path(top) / DOC_REL
  how: '`(Path(top) / DOC_REL).read_text()` at line 958'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(r.stdout)` at line 1040'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "viewport.py"
  how: '`(BIN / "viewport.py").read_text()` at line 1097'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: HERE
  how: '`HERE.read_text()` at line 1165'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_dir(home) / "legacy.tsv"
  how: '`(cache_dir(home) / "legacy.tsv").read_text()` at line 922'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 373'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_dir(home) / "legacy.v1.tsv"
  how: '`(cache_dir(home) / "legacy.v1.tsv").read_text()` at line 944'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: env:D3_TRUNK
  how: reads `os.environ`/`os.getenv` for literal key 'D3_TRUNK'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: env:HOME
  how: reads `os.environ`/`os.getenv` for literal key 'HOME'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: env:XDG_CACHE_HOME
  how: reads `os.environ`/`os.getenv` for literal key 'XDG_CACHE_HOME'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: mint
  how: 'defines public function `mint` at line 38, signature: (i: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_text
  how: 'defines public function `node_text` at line 42, signature: (nid: str, typ:
    str, i: int, parents: list[str], **extra)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _home
  how: 'defines private function `_home` at line 49, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Repo
  how: defines public class `Repo` at line 60
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_legacy
  how: defines public function `load_legacy` at line 103
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_table
  how: 'defines public function `build_table` at line 119, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l2_the_doc_table_each_case_judged_at_its_own_commit
  how: 'defines public function `test_l2_the_doc_table_each_case_judged_at_its_own_commit`
    at line 154, signature: (tmp_path, monkeypatch, cid)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l2_a_member_graphed_later_does_not_clear_its_containers_mark
  how: 'defines public function `test_l2_a_member_graphed_later_does_not_clear_its_containers_mark`
    at line 166, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l2_a_carried_node_with_a_season_2_goal_reads_legacy_until_a_NEW_goal_is_gained
  how: 'defines public function `test_l2_a_carried_node_with_a_season_2_goal_reads_legacy_until_a_NEW_goal_is_gained`
    at line 182, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l2_a_goal_gained_then_dropped_on_a_merged_branch_does_not_graph_the_node
  how: 'defines public function `test_l2_a_goal_gained_then_dropped_on_a_merged_branch_does_not_graph_the_node`
    at line 198, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l2_the_entry_is_the_NEWEST_of_the_nest_commit_and_the_season_carry
  how: 'defines public function `test_l2_the_entry_is_the_NEWEST_of_the_nest_commit_and_the_season_carry`
    at line 226, signature: (tmp_path, monkeypatch, order)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l2_a_retire_move_keeps_the_history_so_the_carry_entry_survives_it
  how: 'defines public function `test_l2_a_retire_move_keeps_the_history_so_the_carry_entry_survives_it`
    at line 247, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l2_the_mark_is_never_read_from_a_front_matter_field
  how: 'defines public function `test_l2_the_mark_is_never_read_from_a_front_matter_field`
    at line 261, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l2_a_path_with_no_history_is_a_question_mark
  how: 'defines public function `test_l2_a_path_with_no_history_is_a_question_mark`
    at line 272, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: grid_version
  how: 'defines public function `grid_version` at line 289, signature: (repo: Repo,
    i: int, text: str, parents: list[str], n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_l1
  how: 'defines public function `build_l1` at line 302, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l1_the_mark_equals_v1s_grid_ref_rule_for_every_node_with_a_grid_ref
  how: 'defines public function `test_l1_the_mark_equals_v1s_grid_ref_rule_for_every_node_with_a_grid_ref`
    at line 324, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l1_on_the_trunk_every_build_node_with_a_grid_ref_reads_the_same_mark
  how: 'defines public function `test_l1_on_the_trunk_every_build_node_with_a_grid_ref_reads_the_same_mark`
    at line 340, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: grep_field
  how: 'defines public function `grep_field` at line 367, signature: (repo_dir: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: grid_lines
  how: 'defines public function `grid_lines` at line 372, signature: (p: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_neg_no_node_file_carries_a_legacy_front_matter_field
  how: 'defines public function `test_neg_no_node_file_carries_a_legacy_front_matter_field`
    at line 376, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_neg_the_rule_reads_no_grid_ref
  how: 'defines public function `test_neg_the_rule_reads_no_grid_ref` at line 386,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_v
  how: 'defines public function `build_v` at line 409, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: vp
  how: 'defines public function `vp` at line 439, signature: (repo: Repo, *args: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: line_of
  how: 'defines public function `line_of` at line 445, signature: (out: str, needle:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l3_verify_exits_0_with_the_mark_on
  how: 'defines public function `test_l3_verify_exits_0_with_the_mark_on` at line
    451, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l3_the_terminal_and_the_llm_view_print_the_same_mark_string
  how: 'defines public function `test_l3_the_terminal_and_the_llm_view_print_the_same_mark_string`
    at line 461, signature: (tmp_path, nid)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: vp2
  how: 'defines public function `vp2` at line 478, signature: (repo: Repo, *args:
    str, home: Path | None=None, bin_dir: Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mark_on
  how: 'defines public function `mark_on` at line 485, signature: (out: str, nid:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l4a_a_new_commit_on_a_node_invalidates_its_cached_mark
  how: 'defines public function `test_l4a_a_new_commit_on_a_node_invalidates_its_cached_mark`
    at line 490, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_season_fx
  how: 'defines public function `build_season_fx` at line 505, signature: (tmp_path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l4b_a_new_season_with_no_node_commit_invalidates_the_cached_mark
  how: 'defines public function `test_l4b_a_new_season_with_no_node_commit_invalidates_the_cached_mark`
    at line 524, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l4c_an_unwritable_home_still_renders_the_mark
  how: 'defines public function `test_l4c_an_unwritable_home_still_renders_the_mark`
    at line 537, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l4c2_a_cache_path_that_is_a_file_still_renders_the_mark
  how: 'defines public function `test_l4c2_a_cache_path_that_is_a_file_still_renders_the_mark`
    at line 552, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: scratch_bin
  how: 'defines public function `scratch_bin` at line 564, signature: (tmp_path: Path,
    name: str, old: str, new: str, nth: int=1)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l4d_verify_exits_0_on_a_clean_scratch_copy
  how: 'defines public function `test_l4d_verify_exits_0_on_a_clean_scratch_copy`
    at line 584, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l4d_verify_fails_when_one_view_drops_or_alters_the_mark
  how: 'defines public function `test_l4d_verify_fails_when_one_view_drops_or_alters_the_mark`
    at line 598, signature: (tmp_path, which, nth, new)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_decoy
  how: 'defines public function `build_decoy` at line 610, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l4e_a_title_that_reads_like_a_mark_does_not_fail_the_clean_verify
  how: 'defines public function `test_l4e_a_title_that_reads_like_a_mark_does_not_fail_the_clean_verify`
    at line 618, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l4e_a_decoy_title_does_not_mask_a_really_dropped_mark
  how: 'defines public function `test_l4e_a_decoy_title_does_not_mask_a_really_dropped_mark`
    at line 629, signature: (tmp_path, which, nth)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d1a_a_path_with_no_history_reads_a_question_mark_and_an_empty_label
  how: 'defines public function `test_d1a_a_path_with_no_history_reads_a_question_mark_and_an_empty_label`
    at line 651, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d1b_labels_omits_a_path_that_has_no_history
  how: 'defines public function `test_d1b_labels_omits_a_path_that_has_no_history`
    at line 663, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d1c_an_uncommitted_node_file_carries_no_mark_in_either_view
  how: 'defines public function `test_d1c_an_uncommitted_node_file_carries_no_mark_in_either_view`
    at line 677, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: vpmod
  how: defines public function `vpmod` at line 693
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GitCount
  how: defines public class `GitCount` at line 706
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fr
  how: 'defines public function `fr` at line 721, signature: (v, nid: str, title:
    str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stamp
  how: 'defines public function `stamp` at line 725, signature: (v, frames, root,
    top, h, hier=0)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: window
  how: 'defines public function `window` at line 729, signature: (top: int, h: int,
    hier: int, n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d2a_a_second_call_with_an_equal_key_runs_no_subprocess_and_returns_equal_frames
  how: 'defines public function `test_d2a_a_second_call_with_an_equal_key_runs_no_subprocess_and_returns_equal_frames`
    at line 733, signature: (tmp_path, monkeypatch, vpmod)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d2b_a_changed_key_part_recomputes
  how: 'defines public function `test_d2b_a_changed_key_part_recomputes` at line 750,
    signature: (tmp_path, monkeypatch, vpmod, part)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d2c_clearing_the_memo_resets_it
  how: 'defines public function `test_d2c_clearing_the_memo_resets_it` at line 775,
    signature: (tmp_path, monkeypatch, vpmod)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d3a_the_stamp_window_is_the_union_of_what_the_human_pane_shows_and_what_llm_shows
  how: 'defines public function `test_d3a_the_stamp_window_is_the_union_of_what_the_human_pane_shows_and_what_llm_shows`
    at line 793, signature: (tmp_path, vpmod)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: add_posts
  how: 'defines public function `add_posts` at line 830, signature: (repo: Repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: frame_marks
  how: 'defines public function `frame_marks` at line 836, signature: (out: str, view:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d3b_the_cli_hierarchy_layer_at_top_5_prints_the_true_label_on_every_frame_either_view_shows
  how: 'defines public function `test_d3b_the_cli_hierarchy_layer_at_top_5_prints_the_true_label_on_every_frame_either_view_shows`
    at line 850, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d3c_the_graph_layer_at_top_5_is_unchanged_control
  how: 'defines public function `test_d3c_the_graph_layer_at_top_5_is_unchanged_control`
    at line 869, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_dir
  how: 'defines public function `cache_dir` at line 894, signature: (home: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: seed
  how: 'defines public function `seed` at line 898, signature: (home: Path, name:
    str, rows: list)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d4a_the_cache_file_is_named_legacy_v1_tsv
  how: 'defines public function `test_d4a_the_cache_file_is_named_legacy_v1_tsv` at
    line 906, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d4b_a_planted_row_in_the_old_legacy_tsv_is_ignored_and_the_file_is_not_rewritten
  how: 'defines public function `test_d4b_a_planted_row_in_the_old_legacy_tsv_is_ignored_and_the_file_is_not_rewritten`
    at line 911, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d4c_a_matching_row_in_legacy_v1_tsv_is_served_control
  how: 'defines public function `test_d4c_a_matching_row_in_legacy_v1_tsv_is_served_control`
    at line 925, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d4d_a_run_writes_legacy_v1_tsv_in_four_columns_and_no_legacy_tsv
  how: 'defines public function `test_d4d_a_run_writes_legacy_v1_tsv_in_four_columns_and_no_legacy_tsv`
    at line 937, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_doc_line
  how: defines public function `cache_doc_line` at line 955
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d4e_the_doc_documents_legacy_v1_tsv_and_the_four_column_row
  how: defines public function `test_d4e_the_doc_documents_legacy_v1_tsv_and_the_four_column_row`
    at line 964
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d4f_the_doc_names_the_file_the_code_uses
  how: 'defines public function `test_d4f_the_doc_names_the_file_the_code_uses` at
    line 979, signature: (monkeypatch, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run_interactive
  how: 'defines public function `run_interactive` at line 1032, signature: (tmp_path:
    Path, repo: Repo, keys: str, bin_dir: Path | None=None, layer: str=''hierarchy'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_hierarchy_marks
  how: 'defines public function `check_hierarchy_marks` at line 1045, signature: (out:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_equal_window_runs_no_git
  how: 'defines public function `check_equal_window_runs_no_git` at line 1054, signature:
    (out: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_i1_the_interactive_hierarchy_layer_at_top_3_draws_the_true_mark_on_every_frame_its_pane_shows
  how: 'defines public function `test_i1_the_interactive_hierarchy_layer_at_top_3_draws_the_true_mark_on_every_frame_its_pane_shows`
    at line 1062, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_i2_a_redraw_of_an_equal_window_runs_no_git
  how: 'defines public function `test_i2_a_redraw_of_an_equal_window_runs_no_git`
    at line 1068, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_i3_the_graph_layer_control_draws_the_true_marks
  how: 'defines public function `test_i3_the_graph_layer_control_draws_the_true_marks`
    at line 1074, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: scratch_bin_multi
  how: 'defines public function `scratch_bin_multi` at line 1090, signature: (tmp_path:
    Path, name: str, patches: list)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_i4_mutants_of_the_real_viewport_make_the_hierarchy_mark_row_red
  how: 'defines public function `test_i4_mutants_of_the_real_viewport_make_the_hierarchy_mark_row_red`
    at line 1115, signature: (tmp_path, name, patches)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_i5_a_mutant_that_forgets_the_memo_each_redraw_makes_the_equal_window_row_red
  how: 'defines public function `test_i5_a_mutant_that_forgets_the_memo_each_redraw_makes_the_equal_window_row_red`
    at line 1125, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nested_pytest
  how: 'defines public function `nested_pytest` at line 1140, signature: (tmp_path:
    Path, test_file: Path, decoy: Path, *extra: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_x1_the_fixture_points_the_cache_at_the_tmp_dir_whatever_the_environment_says
  how: 'defines public function `test_x1_the_fixture_points_the_cache_at_the_tmp_dir_whatever_the_environment_says`
    at line 1148, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_x2_a_whole_file_run_with_a_decoy_xdg_cache_home_leaves_the_decoy_empty
  how: 'defines public function `test_x2_a_whole_file_run_with_a_decoy_xdg_cache_home_leaves_the_decoy_empty`
    at line 1154, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_x3_a_mutant_without_the_fixture_line_writes_the_decoy_cache_red_control
  how: 'defines public function `test_x3_a_mutant_without_the_fixture_line_writes_the_decoy_cache_red_control`
    at line 1163, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: w
  how: '`w.write_text("x = ''refs/grid/node/''\n")` at line 389'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: h / ".cache"
  how: '`(h / ".cache").write_text("not a directory")` at line 557'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "viewport.py"
  how: '`(d / "viewport.py").write_text(src)` at line 577'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo.dir / ghost
  how: '`(repo.dir / ghost).write_text(node_text("goal:uncommitted", "goal", 40, ["goal:root"],
    title=''"T-ghost"'', season=3))` at line 672'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / name
  how: '`(d / name).write_text(text)` at line 902'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: runner
  how: '`runner.write_text(RUNNER)` at line 1036'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "viewport.py"
  how: '`(d / "viewport.py").write_text(src)` at line 1101'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mut
  how: '`mut.write_text(src.replace(FIXTURE_LINE, "    pass"))` at line 1169'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: self.dir / ".agi" / "config.json"
  how: '`(self.dir / ".agi" / "config.json").write_text("{}")` at line 69'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(text)` at line 81'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
goal:g7.16.1.11.22 (E1 D3; rows director-general-2, merge row director-general-5 a65acfc66e): 70 passing rows + 1 skipped over legacy.py and the viewport stamp: the doc 11-case table C1-C11 each judged at its own commit, the no-history class (? -> empty, an uncommitted file has no mark in both views), the cache across a commit and a season and an unwritable HOME, viewport.py --verify comparing the mark of both views (a title that reads like a mark must still pass), the stamp memo (a second equal call runs 0 child processes), the hierarchy-layer window at top>0, the legacy.v1.tsv cache name and the doc line, the INTERACTIVE loop on a stub curses (hierarchy marks at top>0, a pan-only redraw runs no stamp git; three mutants of the real viewport.py), the XDG leak guard (the autouse _home fixture scrubs XDG_CACHE_HOME; a whole-file run with a decoy XDG dir leaves it empty, a control without the line fills it), and ONE real MERGE TOPOLOGY (test_l2_a_goal_gained_then_dropped_on_a_merged_branch_does_not_graph_the_node: a node whose second-parent branch gains then drops a goal parent before a --no-ff merge keeps the mark legacy; SM L10 survivor: dropping --first-parent at legacy.py:17 leaves the other 69 green and turns this row RED, re-run by me on a copy). Opt-in L1 (D3_TRUNK) compares every build node with a grid ref against v1. Previous version: 69 rows + 1 skipped, minted on 42634e22af (02223d2efc). The BUILD-CONTRACT was regenerated by level3.build_node on a65acfc66e (line numbers moved; the THOUGHT block sits after the contract because write_frontmatter preserves it at the end).
<!-- THOUGHT:END -->
