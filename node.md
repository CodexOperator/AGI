---
id: build:tests-test-locations
mint_id: fbfb81ea4bdd46c49c540bcddac0ef32
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_locations.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_locations.py"
---
`extensions/agi/tests/test_locations.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_locations.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(capsys.readouterr().out)` at line 463'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 550'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: make_legacy
  how: 'defines public function `make_legacy` at line 30, signature: (root: Path,
    name: str=''agi-tree.config.json'', **cfg)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: make_graph_dir
  how: 'defines public function `make_graph_dir` at line 38, signature: (repo: Path,
    name: str=''config.json'', **cfg)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_legacy_root_from_subdir
  how: 'defines public function `test_legacy_root_from_subdir` at line 50, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_legacy_name_still_accepted
  how: 'defines public function `test_legacy_name_still_accepted` at line 57, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_canonical_wins_when_both_names_present
  how: 'defines public function `test_canonical_wins_when_both_names_present` at line
    62, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_project_returns_none
  how: 'defines public function `test_no_project_returns_none` at line 68, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_graph_dir_resolves_to_the_dot_agi_itself
  how: 'defines public function `test_graph_dir_resolves_to_the_dot_agi_itself` at
    line 76, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_graph_dir_found_walking_up_from_source
  how: 'defines public function `test_graph_dir_found_walking_up_from_source` at line
    84, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bare_config_json_is_a_marker_only_inside_dot_agi
  how: 'defines public function `test_bare_config_json_is_a_marker_only_inside_dot_agi`
    at line 92, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dot_agi_without_a_config_is_not_a_project
  how: 'defines public function `test_dot_agi_without_a_config_is_not_a_project` at
    line 101, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_nearest_enclosing_wins_between_two_graphs
  how: 'defines public function `test_nearest_enclosing_wins_between_two_graphs` at
    line 110, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_graph_dir_beats_legacy_marker_in_the_same_directory
  how: 'defines public function `test_graph_dir_beats_legacy_marker_in_the_same_directory`
    at line 126, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_near_legacy_beats_distant_graph_dir
  how: 'defines public function `test_near_legacy_beats_distant_graph_dir` at line
    134, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_descend_prefers_basename_match
  how: 'defines public function `test_descend_prefers_basename_match` at line 150,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_descend_ambiguous_returns_none
  how: 'defines public function `test_descend_ambiguous_returns_none` at line 158,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_descend_skips_a_tree_dir_with_no_config
  how: 'defines public function `test_descend_skips_a_tree_dir_with_no_config` at
    line 166, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_source_root_defaults_to_repo_under_graph_dir_layout
  how: 'defines public function `test_source_root_defaults_to_repo_under_graph_dir_layout`
    at line 177, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_source_root_defaults_to_engine_beside_a_legacy_tree
  how: 'defines public function `test_source_root_defaults_to_engine_beside_a_legacy_tree`
    at line 183, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_source_root_falls_back_to_the_graph_root
  how: 'defines public function `test_source_root_falls_back_to_the_graph_root` at
    line 191, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_source_root_relative_is_resolved_against_the_graph_root
  how: 'defines public function `test_source_root_relative_is_resolved_against_the_graph_root`
    at line 196, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_source_root_can_climb_out_of_the_repo
  how: 'defines public function `test_source_root_can_climb_out_of_the_repo` at line
    212, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_source_root_explicit_absolute_override
  how: 'defines public function `test_source_root_explicit_absolute_override` at line
    220, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_source_root_override_beats_the_layout_default
  how: 'defines public function `test_source_root_override_beats_the_layout_default`
    at line 227, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goals_render_to_the_repo_root_not_inside_dot_agi
  how: 'defines public function `test_goals_render_to_the_repo_root_not_inside_dot_agi`
    at line 237, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goals_stay_at_the_graph_root_under_the_legacy_layout
  how: 'defines public function `test_goals_stay_at_the_graph_root_under_the_legacy_layout`
    at line 244, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goals_file_override_resolves_the_dropin_collision
  how: 'defines public function `test_goals_file_override_resolves_the_dropin_collision`
    at line 249, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goals_file_with_a_separator_is_relative_to_the_graph_root
  how: 'defines public function `test_goals_file_with_a_separator_is_relative_to_the_graph_root`
    at line 257, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goals_file_absolute_is_used_as_is
  how: 'defines public function `test_goals_file_absolute_is_used_as_is` at line 263,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_blank_goals_file_falls_back_to_the_default
  how: 'defines public function `test_blank_goals_file_falls_back_to_the_default`
    at line 269, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_malformed_config_does_not_raise
  how: 'defines public function `test_malformed_config_does_not_raise` at line 277,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_dict_config_is_treated_as_empty
  how: 'defines public function `test_non_dict_config_is_treated_as_empty` at line
    286, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_config_loads_as_empty
  how: 'defines public function `test_missing_config_loads_as_empty` at line 293,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_env_override_wins
  how: 'defines public function `test_env_override_wins` at line 300, signature: (tmp_path,
    monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_legacy_env_spelling_still_read
  how: 'defines public function `test_legacy_env_spelling_still_read` at line 307,
    signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _bash_find_root
  how: 'defines private function `_bash_find_root` at line 317, signature: (start:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bash_and_python_agree
  how: 'defines public function `test_bash_and_python_agree` at line 327, signature:
    (tmp_path, shape)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _bash_find_root_in
  how: 'defines private function `_bash_find_root_in` at line 385, signature: (cwd:
    Path, arg: str, timeout: int=10)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_relative_start_with_no_project_terminates
  how: 'defines public function `test_relative_start_with_no_project_terminates` at
    line 395, signature: (tmp_path, arg)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_relative_start_resolves_to_an_absolute_root
  how: 'defines public function `test_relative_start_resolves_to_an_absolute_root`
    at line 407, signature: (tmp_path, arg)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_relative_start_agrees_with_python
  how: 'defines public function `test_relative_start_agrees_with_python` at line 419,
    signature: (tmp_path, arg)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_symlinked_start_resolves_like_python
  how: 'defines public function `test_symlinked_start_resolves_like_python` at line
    438, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_what_prints_one_path
  how: 'defines public function `test_cli_what_prints_one_path` at line 452, signature:
    (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_json_reports_the_layout
  how: 'defines public function `test_cli_json_reports_the_layout` at line 459, signature:
    (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_missing_project_exits_nonzero
  how: 'defines public function `test_cli_missing_project_exits_nonzero` at line 469,
    signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _resolve_in
  how: 'defines private function `_resolve_in` at line 525, signature: (entry: str,
    cwd: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_only_locations_declares_the_marker_names
  how: defines public function `test_only_locations_declares_the_marker_names` at
    line 540
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_entry_point_resolves_the_same_root_from_repo_and_graph_dir
  how: 'defines public function `test_entry_point_resolves_the_same_root_from_repo_and_graph_dir`
    at line 559, signature: (entry, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_root_taking_entry_points_share_the_config_lookup
  how: 'defines public function `test_root_taking_entry_points_share_the_config_lookup`
    at line 586, signature: (entry)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_zoom_accepts_the_repo_root_and_the_graph_dir
  how: 'defines public function `test_zoom_accepts_the_repo_root_and_the_graph_dir`
    at line 602, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / name
  how: '`(root / name).write_text(json.dumps(cfg or {"metric_primary": "outcome_coverage"}))`
    at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / name
  how: '`(graph / name).write_text(json.dumps(cfg or {"metric_primary": "outcome_coverage"}))`
    at line 42'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "autoresearch-tree.config.json"
  how: '`(root / "autoresearch-tree.config.json").write_text("{}")` at line 64'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: plain / "config.json"
  how: '`(plain / "config.json").write_text("{}")` at line 96'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "agi-tree.config.json"
  how: '`(root / "agi-tree.config.json").write_text("{ this is not json")` at line
    281'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "agi-tree.config.json"
  how: '`(root / "agi-tree.config.json").write_text("[1, 2, 3]")` at line 289'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "nodes" / "goal" / "g1.md"
  how: '`(graph / "nodes" / "goal" / "g1.md").write_text( ''---\nid: "goal:g1"\ntype:
    goal\nstatus: active\n'' ''title: "G1: a goal"\nparents: []\n---\n\nbody\n'' )`
    at line 612'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(cfg or {"metric_primary": "outcome_coverage"})` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(cfg or {"metric_primary": "outcome_coverage"})` at line 42'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.