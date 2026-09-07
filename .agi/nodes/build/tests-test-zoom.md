---
id: build:tests-test-zoom
mint_id: 74d2f98590974c44ad7c6b5488415fc2
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_zoom.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_zoom.py"
---
`extensions/agi/tests/test_zoom.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_zoom.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ZOOM
  how: '`ZOOM.read_text(encoding="utf-8")` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ctx_path(proc)
  how: '`_ctx_path(proc).read_text()` at line 115'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ctx_path(proc)
  how: '`_ctx_path(proc).read_text()` at line 133'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ctx_path(proc)
  how: '`_ctx_path(proc).read_text()` at line 140'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ctx_path(proc)
  how: '`_ctx_path(proc).read_text()` at line 151'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ctx_path(proc)
  how: '`_ctx_path(proc).read_text()` at line 161'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ctx_path(proc)
  how: '`_ctx_path(proc).read_text()` at line 252'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ctx_path(proc)
  how: '`_ctx_path(proc).read_text()` at line 263'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ctx_path(small)
  how: '`_ctx_path(small).read_text()` at line 276'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ctx_path(lvl1)
  how: '`_ctx_path(lvl1).read_text()` at line 277'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "sessions" / "iter-001" / agent / "context.md"
  how: '`(tmp_path / "sessions" / "iter-001" / agent / "context.md").read_text()`
    at line 295'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _node
  how: 'defines private function `_node` at line 35, signature: (root: Path, ntype:
    str, slug: str, parents=(), fm_extra: str='''', body: str=''body text'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run
  how: 'defines public function `run` at line 48, signature: (project: Path, iter_n:
    int, agent_id: str, *extra_args: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 56, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ctx_path
  how: 'defines private function `_ctx_path` at line 81, signature: (proc: subprocess.CompletedProcess)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_not_a_project_root_refuses
  how: 'defines public function `test_not_a_project_root_refuses` at line 89, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_invalid_level_value_rejected
  how: 'defines public function `test_invalid_level_value_rejected` at line 95, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_output_path_matches_sessions_convention
  how: 'defines public function `test_output_path_matches_sessions_convention` at
    line 100, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_level1_shows_goal_tree_and_states_its_meaning
  how: 'defines public function `test_level1_shows_goal_tree_and_states_its_meaning`
    at line 112, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_level1_no_target_shows_whole_goal_census
  how: 'defines public function `test_level1_no_target_shows_whole_goal_census` at
    line 130, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_level2_excludes_noncensus_ideas
  how: 'defines public function `test_level2_excludes_noncensus_ideas` at line 137,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_level3_shows_payload_ref_and_states_its_meaning
  how: 'defines public function `test_level3_shows_payload_ref_and_states_its_meaning`
    at line 148, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_level3_no_target_shows_whole_level3_census
  how: 'defines public function `test_level3_no_target_shows_whole_level3_census`
    at line 158, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_levels_4_and_5_refuse_without_touching_the_graph
  how: 'defines public function `test_levels_4_and_5_refuse_without_touching_the_graph`
    at line 170, signature: (project, level)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_level4_names_what_would_need_to_exist
  how: 'defines public function `test_level4_names_what_would_need_to_exist` at line
    181, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_level5_names_what_would_need_to_exist
  how: 'defines public function `test_level5_names_what_would_need_to_exist` at line
    187, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_target_refuses_instead_of_falling_back
  how: 'defines public function `test_missing_target_refuses_instead_of_falling_back`
    at line 198, signature: (project, level)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_small_without_target_is_still_required
  how: 'defines public function `test_small_without_target_is_still_required` at line
    208, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_broken_sqlite_backend_refuses_rather_than_falls_back
  how: 'defines public function `test_broken_sqlite_backend_refuses_rather_than_falls_back`
    at line 214, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_source_never_returns_compose_big_as_a_fallback
  how: defines public function `test_source_never_returns_compose_big_as_a_fallback`
    at line 227
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_legacy_big_keeps_original_whole_graph_content
  how: 'defines public function `test_legacy_big_keeps_original_whole_graph_content`
    at line 247, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_legacy_small_keeps_original_any_type_content
  how: 'defines public function `test_legacy_small_keeps_original_any_type_content`
    at line 258, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_legacy_and_numeric_targeting_the_same_node_differ_in_scope
  how: 'defines public function `test_legacy_and_numeric_targeting_the_same_node_differ_in_scope`
    at line 271, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ctx
  how: 'defines private function `_ctx` at line 285, signature: (tmp_path, agent,
    runtime=None, cc_dispatch=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cc_project_gets_the_cc_contract_not_pi_s
  how: 'defines public function `test_cc_project_gets_the_cc_contract_not_pi_s` at
    line 298, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pi_contract_is_the_report_plus_cli_done
  how: 'defines public function `test_pi_contract_is_the_report_plus_cli_done` at
    line 309, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_explicit_runtime_flag_overrides_the_config_default
  how: 'defines public function `test_explicit_runtime_flag_overrides_the_config_default`
    at line 325, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_default_runtime_fails_closed_to_pi
  how: 'defines public function `test_default_runtime_fails_closed_to_pi` at line
    330, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_one_contract_definition_serves_every_renderer
  how: defines public function `test_one_contract_definition_serves_every_renderer`
    at line 353
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_contracts_forbid_git
  how: 'defines public function `test_both_contracts_forbid_git` at line 360, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_contracts_ask_for_the_struggles_line
  how: 'defines public function `test_both_contracts_ask_for_the_struggles_line` at
    line 375, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _zoom_module
  how: defines private function `_zoom_module` at line 394
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_contract_names_the_report_language_and_field_spelling
  how: defines public function `test_contract_names_the_report_language_and_field_spelling`
    at line 405
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_small_zoom_emits_the_file_path_beside_the_node_id
  how: 'defines public function `test_small_zoom_emits_the_file_path_beside_the_node_id`
    at line 416, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_path_hint_is_best_effort_not_a_hard_failure
  how: 'defines public function `test_path_hint_is_best_effort_not_a_hard_failure`
    at line 428, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f"{slug}.md"
  how: '`(d / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")` at line
    45'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text(''{"metric_primary": "outcome_coverage"}'')`
    at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "context" / "INJECTION.md"
  how: '`(tmp_path / "context" / "INJECTION.md").write_text( "# injection\nINJECTION-MARKER-TEXT\n",
    encoding="utf-8" )` at line 59'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: blocker
  how: '`blocker.write_text("i am a file, not a directory")` at line 216'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text( ''{"persistence": {"type":
    "sqlite", "path": "blocker/db.sqlite"}}'' )` at line 217'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "context" / "INJECTION.md"
  how: '`(tmp_path / "context" / "INJECTION.md").write_text("x\n")` at line 221'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text(cfg)` at line 288'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{not json")` at line 347'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text(''{"cc_dispatch": {}}'')`
    at line 349'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "goal" / "g4.3-a-long-derived-slug.md"
  how: '`(root / "nodes" / "goal" / "g4.3-a-long-derived-slug.md").write_text( ''---\nid:
    "goal:g4.3"\ntype: goal\nparents: []\n---\n\nbody\n'' )` at line 422'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.