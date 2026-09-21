---
id: build:tests-test-crons
mint_id: f8afe4ca2643442b84ec3e4da9d71ba5
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_crons.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_crons.py"
---
`extensions/agi/tests/test_crons.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_crons.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: crons
  how: '`import crons` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.read_text()` at line 400'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.read_text()` at line 403'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.read_text()` at line 413'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.read_text()` at line 563'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.read_text()` at line 416'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.read_text()` at line 568'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 372'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _crons_frontmatter
  how: 'defines private function `_crons_frontmatter` at line 39, signature: (crons_live=True,
    cadences=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_crons_node
  how: 'defines public function `write_crons_node` at line 51, signature: (root: Path,
    crons_live=True, cadences=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git
  how: 'defines private function `_git` at line 57, signature: (path: Path, *args:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_init
  how: 'defines private function `_git_init` at line 64, signature: (path: Path, branch:
    str=''master'', detach: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: make_project
  how: 'defines public function `make_project` at line 77, signature: (tmp_path, name=''proj'',
    crons_live=True, cadences=None, repo_branch=''master'', engine_branch=''master'',
    detach_repo=False, detach_engine=False, engine=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_load_valid_node
  how: 'defines public function `test_load_valid_node` at line 95, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_node_file_names_the_path
  how: 'defines public function `test_missing_node_file_names_the_path` at line 104,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_frontmatter_delimiter
  how: 'defines public function `test_missing_frontmatter_delimiter` at line 112,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_malformed_yaml_raises_naming_the_file
  how: 'defines public function `test_malformed_yaml_raises_naming_the_file` at line
    121, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_crons_live_key
  how: 'defines public function `test_missing_crons_live_key` at line 130, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_bool_crons_live
  how: 'defines public function `test_non_bool_crons_live` at line 139, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_job_name_rejected
  how: 'defines public function `test_unknown_job_name_rejected` at line 146, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_every_mins_and_schedule_rejected
  how: 'defines public function `test_both_every_mins_and_schedule_rejected` at line
    153, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_enabled_job_with_neither_field_rejected
  how: 'defines public function `test_enabled_job_with_neither_field_rejected` at
    line 162, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_disabled_job_may_omit_schedule
  how: 'defines public function `test_disabled_job_may_omit_schedule` at line 169,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bad_every_mins_type_rejected
  how: 'defines public function `test_bad_every_mins_type_rejected` at line 175, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bad_schedule_field_count_rejected
  how: 'defines public function `test_bad_schedule_field_count_rejected` at line 182,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_job_absent_from_cadences_is_never_rendered
  how: 'defines public function `test_job_absent_from_cadences_is_never_rendered`
    at line 189, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_resolve_branch_on_normal_repo
  how: 'defines public function `test_resolve_branch_on_normal_repo` at line 200,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_resolve_branch_non_default_name
  how: 'defines public function `test_resolve_branch_non_default_name` at line 206,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_resolve_branch_detached_head_refuses
  how: 'defines public function `test_resolve_branch_detached_head_refuses` at line
    214, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_refuses_on_detached_repo
  how: 'defines public function `test_render_refuses_on_detached_repo` at line 221,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_refuses_on_detached_engine
  how: 'defines public function `test_render_refuses_on_detached_engine` at line 228,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_uses_the_actual_checked_out_branch
  how: 'defines public function `test_render_uses_the_actual_checked_out_branch` at
    line 235, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_every_line_cds_into_root_first
  how: 'defines public function `test_render_every_line_cds_into_root_first` at line
    250, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_order_matches_known_jobs
  how: 'defines public function `test_render_order_matches_known_jobs` at line 259,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_grid_sync_line_self_reapplies
  how: 'defines public function `test_grid_sync_line_self_reapplies` at line 270,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_self_reapply_names_the_engine_copy_not_the_running_one
  how: 'defines public function `test_self_reapply_names_the_engine_copy_not_the_running_one`
    at line 285, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_disabled_job_omitted
  how: 'defines public function `test_disabled_job_omitted` at line 306, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_crons_live_false_renders_nothing
  how: 'defines public function `test_crons_live_false_renders_nothing` at line 316,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_project_hash_distinct_per_project
  how: 'defines public function `test_project_hash_distinct_per_project` at line 326,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_block_markers_are_deterministic
  how: 'defines public function `test_block_markers_are_deterministic` at line 332,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_split_no_match_returns_everything_as_before
  how: 'defines public function `test_split_no_match_returns_everything_as_before`
    at line 352, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_split_unterminated_block_raises
  how: 'defines public function `test_split_unterminated_block_raises` at line 360,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read
  how: 'defines private function `_read` at line 371, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_apply_writes_managed_block_preserving_unrelated_lines
  how: 'defines public function `test_apply_writes_managed_block_preserving_unrelated_lines`
    at line 375, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_apply_twice_is_byte_identical
  how: 'defines public function `test_apply_twice_is_byte_identical` at line 394,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_apply_dry_run_writes_nothing
  how: 'defines public function `test_apply_dry_run_writes_nothing` at line 409, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_two_projects_coexist_in_one_crontab
  how: 'defines public function `test_two_projects_coexist_in_one_crontab` at line
    420, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_kill_switch_removes_all_managed_lines
  how: 'defines public function `test_kill_switch_removes_all_managed_lines` at line
    445, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_remove_only_this_projects_block
  how: 'defines public function `test_remove_only_this_projects_block` at line 463,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_remove_when_nothing_installed_is_a_clean_noop
  how: 'defines public function `test_remove_when_nothing_installed_is_a_clean_noop`
    at line 475, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_show_reports_up_to_date_after_apply
  how: 'defines public function `test_show_reports_up_to_date_after_apply` at line
    485, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_show_reports_drift_before_apply
  how: 'defines public function `test_show_reports_drift_before_apply` at line 494,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_disabled_engine_push_job_needs_no_engine_git
  how: 'defines public function `test_disabled_engine_push_job_needs_no_engine_git`
    at line 503, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_apply_show_remove_round_trip
  how: 'defines public function `test_cli_apply_show_remove_round_trip` at line 521,
    signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_missing_project_exits_nonzero
  how: 'defines public function `test_cli_missing_project_exits_nonzero` at line 541,
    signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_missing_node_exits_nonzero_naming_the_file
  how: 'defines public function `test_cli_missing_node_exits_nonzero_naming_the_file`
    at line 549, signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_dry_run_reports_without_writing
  how: 'defines public function `test_cli_dry_run_reports_without_writing` at line
    559, signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(_crons_frontmatter(crons_live, cadences))` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path / ".keep"
  how: '`(path / ".keep").write_text("x")` at line 69'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "agi-tree.config.json"
  how: '`(root / "agi-tree.config.json").write_text("{}")` at line 84'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "agi-tree.config.json"
  how: '`(root / "agi-tree.config.json").write_text("{}")` at line 107'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("no frontmatter here\n")` at line 116'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("---\ncrons_live: [oops\n---\nbody\n")` at line 125'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("---\ncadences: {}\n---\nbody\n")` at line 134'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.write_text("\n".join(UNRELATED_LINES) + "\n")` at line 378'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.write_text("\n".join(UNRELATED_LINES) + "\n")` at line 397'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.write_text("\n".join(UNRELATED_LINES) + "\n")` at line 412'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.write_text("\n".join(UNRELATED_LINES) + "\n")` at line 426'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.write_text("\n".join(UNRELATED_LINES) + "\n")` at line 450'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.write_text("\n".join(UNRELATED_LINES) + "\n")` at line 466'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.write_text("\n".join(UNRELATED_LINES) + "\n")` at line 478'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.write_text("")` at line 488'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.write_text("")` at line 497'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.write_text("\n".join(UNRELATED_LINES) + "\n")` at line 524'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "agi-tree.config.json"
  how: '`(root / "agi-tree.config.json").write_text("{}")` at line 552'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fixture
  how: '`fixture.write_text("\n".join(UNRELATED_LINES) + "\n")` at line 562'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_dump
  how: '`yaml.safe_dump(fm, sort_keys=False)` at line 48'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.