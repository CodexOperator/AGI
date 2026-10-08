---
build_kind: code
confidence: 1.0
id: "build:tests-test-nest"
mint_id: b9eb8dd13d72440793cf2fe8467d5c34
origin: build-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_nest.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_nest.py"
type: build
---

`extensions/agi/tests/test_nest.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
goal:g7.16.1.11.21: alive's 10 cases N1-N10 lifted from doc:rse-d1-nest into a committed pytest file (33 rows with DG2's falsifier lane); imported by test_nest_r.py as tests.test_nest. Falsifier of build:bin-nest.
<!-- THOUGHT:END -->

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_nest.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shutil
  how: '`import shutil` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: NEST
  how: '`NEST.read_text(encoding="utf-8")` at line 458'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text(encoding="utf-8")` at line 278'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(m.group(1))` at line 284'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "goal" / "a.md"
  how: '`(root / "nodes" / "goal" / "a.md").read_text(encoding="utf-8")` at line 449'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo.d / ".git" / "index"
  how: '`(repo.d / ".git" / "index").read_bytes()` at line 224'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: node
  how: 'defines public function `node` at line 45, signature: (i, parents=(), nest=None,
    extra='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Repo
  how: defines public class `Repo` at line 54
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo
  how: 'defines public function `repo` at line 87, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nest
  how: 'defines public function `nest` at line 91, signature: (repo, verb, n, rev=''HEAD'',
    env=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: slice_of
  how: 'defines public function `slice_of` at line 99, signature: (repo, n)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_n1_a_node_with_no_nest_is_its_own_slice
  how: 'defines public function `test_n1_a_node_with_no_nest_is_its_own_slice` at
    line 104, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_n2_subtree_descends_through_a_member_with_no_nest
  how: 'defines public function `test_n2_subtree_descends_through_a_member_with_no_nest`
    at line 109, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_n3_a_member_with_its_own_subtree_expands_itself
  how: 'defines public function `test_n3_a_member_with_its_own_subtree_expands_itself`
    at line 115, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_n4_an_arbitrary_list_of_any_types_and_a_cycle_stops
  how: 'defines public function `test_n4_an_arbitrary_list_of_any_types_and_a_cycle_stops`
    at line 122, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_n5_a_collapse_is_one_one_node_commit_and_the_member_files_stay
  how: 'defines public function `test_n5_a_collapse_is_one_one_node_commit_and_the_member_files_stay`
    at line 129, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_n6_log_reaches_every_members_history
  how: 'defines public function `test_n6_log_reaches_every_members_history` at line
    138, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_n7_a_retired_member_keeps_its_history
  how: 'defines public function `test_n7_a_retired_member_keeps_its_history` at line
    144, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_n8_a_member_with_a_list_stops_the_descent_and_expands_its_list
  how: 'defines public function `test_n8_a_member_with_a_list_stops_the_descent_and_expands_its_list`
    at line 153, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_n9_history_older_than_the_one_repo_move_is_read
  how: 'defines public function `test_n9_history_older_than_the_one_repo_move_is_read`
    at line 160, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_n10_inline_lists_parse_as_lists
  how: 'defines public function `test_n10_inline_lists_parse_as_lists` at line 169,
    signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_x_the_walk_is_first_parent_a_side_branch_commit_shows_only_as_its_merge
  how: 'defines public function `test_x_the_walk_is_first_parent_a_side_branch_commit_shows_only_as_its_merge`
    at line 178, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_x_following_a_retire_move_does_not_depend_on_the_users_diff_renames_config
  how: 'defines public function `test_x_following_a_retire_move_does_not_depend_on_the_users_diff_renames_config`
    at line 192, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_x_slice_includes_a_retired_member
  how: 'defines public function `test_x_slice_includes_a_retired_member` at line 202,
    signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_x_subtree_descends_through_two_nest_less_levels
  how: 'defines public function `test_x_subtree_descends_through_two_nest_less_levels`
    at line 211, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_x_a_read_only_run_leaves_refs_objects_and_the_index_as_they_were
  how: 'defines public function `test_x_a_read_only_run_leaves_refs_objects_and_the_index_as_they_were`
    at line 218, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _follow
  how: 'defines private function `_follow` at line 232, signature: (repo, path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d13_a_retired_members_log_equals_git_follow
  how: 'defines public function `test_d13_a_retired_members_log_equals_git_follow`
    at line 247, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d13_commits_follow_reaches_through_a_copy_line_are_not_the_nodes_history
  how: 'defines public function `test_d13_commits_follow_reaches_through_a_copy_line_are_not_the_nodes_history`
    at line 261, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _schema_texts
  how: defines private function `_schema_texts` at line 277
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _frontmatter
  how: 'defines private function `_frontmatter` at line 281, signature: (text)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_s_no_schema_lists_nest_as_required
  how: defines public function `test_s_no_schema_lists_nest_as_required` at line 287
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _nest_type
  how: 'defines private function `_nest_type` at line 293, signature: (fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_s_the_goal_schema_allows_nest_as_a_str_or_list
  how: 'defines public function `test_s_the_goal_schema_allows_nest_as_a_str_or_list`
    at line 298, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_s_every_schema_that_declares_nest_declares_it_str_or_list
  how: defines public function `test_s_every_schema_that_declares_nest_declares_it_str_or_list`
    at line 305
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scratch_root
  how: 'defines private function `_scratch_root` at line 317, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _goal
  how: 'defines private function `_goal` at line 326, signature: (nid, nest_lines='''',
    parents=''  []\n'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_s_a_node_with_and_without_nest_keeps_the_schema_count
  how: 'defines public function `test_s_a_node_with_and_without_nest_keeps_the_schema_count`
    at line 334, signature: (tmp_path, nest_lines)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _corpus
  how: 'defines private function `_corpus` at line 346, signature: (tmp_path, nodes)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _links_main
  how: 'defines private function `_links_main` at line 355, signature: (root)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l_nest_unresolved_names_each_dangling_nest_id_with_its_container
  how: 'defines public function `test_l_nest_unresolved_names_each_dangling_nest_id_with_its_container`
    at line 367, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l_main_reports_each_on_its_own_line_and_a_count_line
  how: 'defines public function `test_l_main_reports_each_on_its_own_line_and_a_count_line`
    at line 377, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l_a_clean_corpus_prints_the_line_with_zero
  how: 'defines public function `test_l_a_clean_corpus_prints_the_line_with_zero`
    at line 388, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l_a_nest_id_naming_a_retired_node_resolves
  how: 'defines public function `test_l_a_nest_id_naming_a_retired_node_resolves`
    at line 397, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l_a_nest_id_never_enters_count_broken_links
  how: 'defines public function `test_l_a_nest_id_never_enters_count_broken_links`
    at line 404, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _metrics
  how: 'defines private function `_metrics` at line 413, signature: (root)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l_the_metrics_cell_counts_them_beside_an_unchanged_broken_links
  how: 'defines public function `test_l_the_metrics_cell_counts_them_beside_an_unchanged_broken_links`
    at line 419, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_l_the_metrics_cell_is_zero_when_nothing_dangles
  how: 'defines public function `test_l_the_metrics_cell_is_zero_when_nothing_dangles`
    at line 425, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_d11_d12_the_writer_collapses_with_exactly_one_tracked_file_changed_and_the_count_holds
  how: 'defines public function `test_d11_d12_the_writer_collapses_with_exactly_one_tracked_file_changed_and_the_count_holds`
    at line 431, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_neg_nest_py_holds_no_update_ref_commit_tree_or_mktree
  how: defines public function `test_neg_nest_py_holds_no_update_ref_commit_tree_or_mktree`
    at line 456
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo.d / ".agi/nodes/doc/src.md"
  how: '`(repo.d / ".agi/nodes/doc/src.md").write_text(node("doc:src", extra=big +
    "edit\n"))` at line 265'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo.d / ".agi/nodes/doc/cp2.md"
  how: '`(repo.d / ".agi/nodes/doc/cp2.md").write_text(node("doc:cp2", extra=big))`
    at line 266'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "config.json"
  how: '`(root / "config.json").write_text("{}", encoding="utf-8")` at line 322'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(_goal("a", nest_lines), encoding="utf-8")` at line 340'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(text)` at line 71'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(text, encoding="utf-8")` at line 351'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(_goal(nid), encoding="utf-8")` at line 436'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
