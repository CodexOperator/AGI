---
id: build:tests-test-lifecycle-guards
mint_id: 3cedcf24cd124b6081f86fb4b37deea2
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_lifecycle_guards.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_lifecycle_guards.py"
---
`extensions/agi/tests/test_lifecycle_guards.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_lifecycle_guards.py
parse_ok: true
inputs:
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
- name: eg
  how: '`import evidence_gate as eg` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "completion.py"
  how: '`(BIN / "completion.py").read_text()` at line 243'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _node
  how: 'defines private function `_node` at line 22, signature: (d: Path, nid: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_build_corpus_reads_a_real_nodes_dir
  how: 'defines public function `test_build_corpus_reads_a_real_nodes_dir` at line
    27, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_build_corpus_refuses_a_project_root
  how: 'defines public function `test_build_corpus_refuses_a_project_root` at line
    32, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_missing_directory_is_still_empty_not_an_error
  how: 'defines public function `test_a_missing_directory_is_still_empty_not_an_error`
    at line 47, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_three_live_callers_still_pass
  how: 'defines public function `test_the_three_live_callers_still_pass` at line 53,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _goal_fm
  how: 'defines private function `_goal_fm` at line 64, signature: (gid, status, kind=''subgoal'',
    parents=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _snapshot_goals
  how: defines private function `_snapshot_goals` at line 71
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_complete_root_with_a_live_subgoal_warns
  how: 'defines public function `test_a_complete_root_with_a_live_subgoal_warns` at
    line 80, signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_active_and_horizon_subgoals_both_count
  how: 'defines public function `test_active_and_horizon_subgoals_both_count` at line
    93, signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_fully_finished_tree_is_silent
  how: 'defines public function `test_a_fully_finished_tree_is_silent` at line 103,
    signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_childless_short_term_goal_never_warns
  how: 'defines public function `test_a_childless_short_term_goal_never_warns` at
    line 116, signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_it_is_a_warning_and_never_a_failure
  how: 'defines public function `test_it_is_a_warning_and_never_a_failure` at line
    125, signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_deprecated_node_ids_is_the_single_definition
  how: 'defines public function `test_deprecated_node_ids_is_the_single_definition`
    at line 140, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_live_only_view_hides_nodes_without_mutating_the_graph
  how: defines public function `test_the_live_only_view_hides_nodes_without_mutating_the_graph`
    at line 160
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _completion
  how: defines private function `_completion` at line 194
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scaffolded
  how: 'defines private function `_scaffolded` at line 204, signature: (root: Path,
    nid: str, filled: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_parent_is_complete_when_all_its_kids_are
  how: 'defines public function `test_a_parent_is_complete_when_all_its_kids_are`
    at line 214, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_parent_is_not_complete_while_one_kid_is_unfilled
  how: 'defines public function `test_a_parent_is_not_complete_while_one_kid_is_unfilled`
    at line 221, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_owning_nothing_is_not_complete
  how: 'defines public function `test_owning_nothing_is_not_complete` at line 228,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_harness_name_reaches_the_parent_completion_path
  how: defines public function `test_no_harness_name_reaches_the_parent_completion_path`
    at line 239
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rules
  how: defines private function `_rules` at line 254
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_build_schema_declares_exactly_two_parent_shapes
  how: defines public function `test_build_schema_declares_exactly_two_parent_shapes`
    at line 260
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_shapes_is_an_or_across_whole_shapes_not_an_and
  how: defines public function `test_parent_shapes_is_an_or_across_whole_shapes_not_an_and`
    at line 270
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_shape_naming_a_disallowed_type_is_refused
  how: defines public function `test_a_shape_naming_a_disallowed_type_is_refused`
    at line 285
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_shape_outside_the_min_max_bounds_is_refused
  how: defines public function `test_a_shape_outside_the_min_max_bounds_is_refused`
    at line 296
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_absent_parent_shapes_leaves_every_other_type_alone
  how: defines public function `test_absent_parent_shapes_leaves_every_other_type_alone`
    at line 306
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f"{nid.split(':')[-1]}.md"
  how: '`(d / f"{nid.split('':'')[-1]}.md").write_text(f"---\nid: {nid}\ntype: mvp\n---\nbody\n")`
    at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "live.md"
  how: '`(d / "live.md").write_text("---\nid: build:live\ntype: build\n---\nx\n")`
    at line 150'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "dead.md"
  how: '`(d / "dead.md").write_text( "---\nid: build:dead\ntype: build\nstatus: deprecated\n---\nx\n")`
    at line 151'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f"{nid.split(':')[-1]}.md"
  how: '`(d / f"{nid.split('':'')[-1]}.md").write_text( f"---\nid: {nid}\ntype: {nid.split('':'',
    1)[0]}\n---\n{body}")` at line 210'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.