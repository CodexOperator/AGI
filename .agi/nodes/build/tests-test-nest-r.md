---
build_kind: code
confidence: 1.0
id: "build:tests-test-nest-r"
mint_id: 72ef3dda124641f194076fcab9e3263c
origin: build-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_nest_r.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_nest_r.py"
type: build
---

`extensions/agi/tests/test_nest_r.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
goal:g7.16.1.11.21: DG2's falsifier rows for the corrective rounds (R1-R4: once-only expansion, D+A retire-edit by path, mint ids, the command line (R5 is the _OUTSIDE_CLIS line in test_commands_manifest.py); RD-1 cross-type same basename; RD-3 malformed nest values in nest.py, links.nest_malformed and the metrics cell), 55 rows, each RED on a mutant of the real piece. Falsifier of build:bin-nest.
<!-- THOUGHT:END -->

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_nest_r.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: itertools
  how: '`import itertools` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tests.test_nest
  how: '`from tests import test_nest as base` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tests.test_nest.Repo
  how: '`from tests.test_nest import Repo` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tests.test_nest.node
  how: '`from tests.test_nest import node` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tests.test_nest.nest
  how: '`from tests.test_nest import nest` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tests.test_nest.slice_of
  how: '`from tests.test_nest import slice_of` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: repo
  how: 'defines public function `repo` at line 41, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _hang_guard
  how: 'defines private function `_hang_guard` at line 45, signature: (repo, verb,
    n)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _r1_fixture
  how: 'defines private function `_r1_fixture` at line 59, signature: (repo, order,
    tail=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r1_a_list_nest_is_the_same_slice_in_either_order
  how: 'defines public function `test_r1_a_list_nest_is_the_same_slice_in_either_order`
    at line 69, signature: (repo, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r1_the_slice_is_closed_every_members_slice_is_inside_the_containers
  how: 'defines public function `test_r1_the_slice_is_closed_every_members_slice_is_inside_the_containers`
    at line 80, signature: (repo, order)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r1_two_nest_less_list_members_chained_with_a_subtree_member_in_any_order
  how: 'defines public function `test_r1_two_nest_less_list_members_chained_with_a_subtree_member_in_any_order`
    at line 89, signature: (repo, order)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r1_a_subtree_cycle_and_a_list_cycle_terminate_with_the_same_slice
  how: 'defines public function `test_r1_a_subtree_cycle_and_a_list_cycle_terminate_with_the_same_slice`
    at line 98, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _status_of
  how: 'defines private function `_status_of` at line 112, signature: (repo, rev)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _small_member
  how: 'defines private function `_small_member` at line 116, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r2_a_retire_that_also_edits_the_node_keeps_the_add_and_the_retire_in_log
  how: 'defines public function `test_r2_a_retire_that_also_edits_the_node_keeps_the_add_and_the_retire_in_log`
    at line 121, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r2_a_clean_small_move_still_maps
  how: 'defines public function `test_r2_a_clean_small_move_still_maps` at line 133,
    signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r2_a_delete_and_an_add_of_different_basenames_is_not_one_nodes_move
  how: 'defines public function `test_r2_a_delete_and_an_add_of_different_basenames_is_not_one_nodes_move`
    at line 142, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _mint_fixture
  how: 'defines private function `_mint_fixture` at line 159, signature: (repo, nest_cell)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r3_a_mint_id_in_a_nest_list_puts_its_node_in_the_slice
  how: 'defines public function `test_r3_a_mint_id_in_a_nest_list_puts_its_node_in_the_slice`
    at line 172, signature: (repo, cell)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r3_a_mint_id_entry_brings_the_nodes_history_into_log
  how: 'defines public function `test_r3_a_mint_id_entry_brings_the_nodes_history_into_log`
    at line 177, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r3_a_mint_id_entry_expands_the_nodes_own_nest
  how: 'defines public function `test_r3_a_mint_id_entry_expands_the_nodes_own_nest`
    at line 182, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r3_an_entry_that_is_neither_an_id_nor_a_mint_is_absent_from_the_slice
  how: 'defines public function `test_r3_an_entry_that_is_neither_an_id_nor_a_mint_is_absent_from_the_slice`
    at line 189, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r3_a_mint_string_equal_to_another_nodes_id_the_exact_id_wins
  how: 'defines public function `test_r3_a_mint_string_equal_to_another_nodes_id_the_exact_id_wins`
    at line 195, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _links_corpus
  how: 'defines private function `_links_corpus` at line 204, signature: (tmp_path,
    cell)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r3_nest_unresolved_resolves_a_mint_id_in_either_list_spelling
  how: 'defines public function `test_r3_nest_unresolved_resolves_a_mint_id_in_either_list_spelling`
    at line 212, signature: (tmp_path, cell)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r3_nest_unresolved_names_an_entry_that_is_neither_id_nor_mint
  how: 'defines public function `test_r3_nest_unresolved_names_an_entry_that_is_neither_id_nor_mint`
    at line 219, signature: (tmp_path, cell)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _run
  how: 'defines private function `_run` at line 229, signature: (args, cwd, env=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r4_help_prints_the_usage_line_on_stdout_and_exits_0
  how: 'defines public function `test_r4_help_prints_the_usage_line_on_stdout_and_exits_0`
    at line 237, signature: (tmp_path, flag)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r4_no_arguments_is_the_usage_line_on_stderr_rc_2_and_nothing_on_stdout
  how: 'defines public function `test_r4_no_arguments_is_the_usage_line_on_stderr_rc_2_and_nothing_on_stdout`
    at line 243, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r4_an_unknown_verb_or_the_wrong_argument_count_is_usage_on_stderr_rc_2
  how: 'defines public function `test_r4_an_unknown_verb_or_the_wrong_argument_count_is_usage_on_stderr_rc_2`
    at line 251, signature: (repo, args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r4_an_id_in_neither_id_nor_mint_id_is_named_on_stderr_rc_1_and_stdout_is_empty
  how: 'defines public function `test_r4_an_id_in_neither_id_nor_mint_id_is_named_on_stderr_rc_1_and_stdout_is_empty`
    at line 259, signature: (repo, verb)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r4_a_known_id_still_exits_0_with_output
  how: 'defines public function `test_r4_a_known_id_still_exits_0_with_output` at
    line 267, signature: (repo, verb)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_r4_a_mint_id_is_a_known_id_for_the_container_too
  how: 'defines public function `test_r4_a_mint_id_is_a_known_id_for_the_container_too`
    at line 273, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _swap_fixture
  how: 'defines private function `_swap_fixture` at line 280, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rd1_an_add_and_a_delete_of_the_same_basename_in_different_type_dirs_is_not_one_nodes_move
  how: 'defines public function `test_rd1_an_add_and_a_delete_of_the_same_basename_in_different_type_dirs_is_not_one_nodes_move`
    at line 293, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _history_then_swap
  how: 'defines private function `_history_then_swap` at line 301, signature: (repo,
    old, new, member)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rd1_a_retire_edit_d_plus_a_maps_in_both_directions
  how: 'defines public function `test_rd1_a_retire_edit_d_plus_a_maps_in_both_directions`
    at line 319, signature: (repo, old, new)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _nest_cell_repo
  how: 'defines private function `_nest_cell_repo` at line 330, signature: (repo,
    value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rd3_a_malformed_nest_value_exits_1_and_says_so
  how: 'defines public function `test_rd3_a_malformed_nest_value_exits_1_and_says_so`
    at line 337, signature: (repo, verb, value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rd3_subtree_a_list_and_an_empty_cell_still_pass
  how: 'defines public function `test_rd3_subtree_a_list_and_an_empty_cell_still_pass`
    at line 346, signature: (repo, verb, value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rd3_links_reports_each_malformed_value_on_its_own_line_and_a_count
  how: 'defines public function `test_rd3_links_reports_each_malformed_value_on_its_own_line_and_a_count`
    at line 362, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rd3_a_malformed_nest_never_enters_count_broken_links
  how: 'defines public function `test_rd3_a_malformed_nest_never_enters_count_broken_links`
    at line 374, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rd2_slice_prints_sorted_unique_ids_one_per_line
  how: 'defines public function `test_rd2_slice_prints_sorted_unique_ids_one_per_line`
    at line 382, signature: (repo)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rd3_the_metrics_cell_counts_the_malformed_values_beside_an_unchanged_broken_links
  how: 'defines public function `test_rd3_the_metrics_cell_counts_the_malformed_values_beside_an_unchanged_broken_links`
    at line 391, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo.d / ".agi/nodes/deprecated/goal/s1.md"
  how: '`(repo.d / ".agi/nodes/deprecated/goal/s1.md").write_text(RETIRED)` at line
    125'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo.d / ".agi/nodes/deprecated/goal/s1.md"
  how: '`(repo.d / ".agi/nodes/deprecated/goal/s1.md").write_text(member)` at line
    149'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo.d / ".agi/nodes/hypothesis/foo.md"
  how: '`(repo.d / ".agi/nodes/hypothesis/foo.md").write_text("---\nid: hypothesis:foo\nparents:
    []\n---\n" + "".join(f"hypothesis text {i}\n" for i in range(7)))` at line 288'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo.d / new
  how: '`(repo.d / new).write_text(c)` at line 311'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
