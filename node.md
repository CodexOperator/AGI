---
id: build:tests-test-viewport
mint_id: 24064ed790c7405c986f4b8d5a92ba39
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_viewport.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_viewport.py"
---
`extensions/agi/tests/test_viewport.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_viewport.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 7'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "viewport.py"
  how: '`(BIN / "viewport.py").read_text()` at line 280'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _load_viewport
  how: defines private function `_load_viewport` at line 19
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _Node
  how: defines private class `_Node` at line 38
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _Graph
  how: defines private class `_Graph` at line 46
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph
  how: defines public function `graph` at line 60
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fm
  how: defines public function `fm` at line 72
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_formatters_read_one_stream
  how: 'defines public function `test_both_formatters_read_one_stream` at line 88,
    signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_changing_the_stream_changes_both_views
  how: 'defines public function `test_changing_the_stream_changes_both_views` at line
    99, signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_children_appear_directly_beneath_their_parent
  how: 'defines public function `test_children_appear_directly_beneath_their_parent`
    at line 118, signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_depth_bounds_the_walk
  how: 'defines public function `test_depth_bounds_the_walk` at line 130, signature:
    (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_traversal_is_deterministic
  how: 'defines public function `test_traversal_is_deterministic` at line 135, signature:
    (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_cycle_does_not_hang_the_walk
  how: 'defines public function `test_a_cycle_does_not_hang_the_walk` at line 141,
    signature: (fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_unknown_anchor_fails_loudly
  how: 'defines public function `test_an_unknown_anchor_fails_loudly` at line 150,
    signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_dangling_parent_is_rendered_as_damage
  how: 'defines public function `test_a_dangling_parent_is_rendered_as_damage` at
    line 159, signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_decisive_verdict_without_evidence_is_damage
  how: 'defines public function `test_a_decisive_verdict_without_evidence_is_damage`
    at line 166, signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_decisive_verdict_with_evidence_is_not_damage
  how: 'defines public function `test_a_decisive_verdict_with_evidence_is_not_damage`
    at line 172, signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_damage_reaches_both_views
  how: 'defines public function `test_damage_reaches_both_views` at line 178, signature:
    (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_default_roots_are_the_active_goals
  how: 'defines public function `test_default_roots_are_the_active_goals` at line
    190, signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_default_roots_fall_back_when_nothing_is_active
  how: 'defines public function `test_default_roots_fall_back_when_nothing_is_active`
    at line 194, signature: (graph)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_ids_as_a_set_attribute_does_not_crash
  how: 'defines public function `test_node_ids_as_a_set_attribute_does_not_crash`
    at line 200, signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_window_pans_without_changing_the_stream
  how: 'defines public function `test_the_window_pans_without_changing_the_stream`
    at line 211, signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_horizontal_pan_slices_columns
  how: 'defines public function `test_horizontal_pan_slices_columns` at line 219,
    signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_every_line_is_padded_to_the_window_width
  how: 'defines public function `test_every_line_is_padded_to_the_window_width` at
    line 225, signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_agents_render_as_spiders_where_they_work
  how: 'defines public function `test_agents_render_as_spiders_where_they_work` at
    line 235, signature: (graph, fm)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_agents_of_iteration_reads_manifest_and_agent_json
  how: 'defines public function `test_agents_of_iteration_reads_manifest_and_agent_json`
    at line 243, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_missing_or_corrupt_manifest_returns_nothing_rather_than_raising
  how: 'defines public function `test_a_missing_or_corrupt_manifest_returns_nothing_rather_than_raising`
    at line 253, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_iteration_points_are_sorted_oldest_first
  how: 'defines public function `test_iteration_points_are_sorted_oldest_first` at
    line 265, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_iteration_points_on_a_project_with_no_sessions
  how: 'defines public function `test_iteration_points_on_a_project_with_no_sessions`
    at line 271, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_module_contains_no_write_surface
  how: defines public function `test_the_module_contains_no_write_surface` at line
    279
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "sessions" / "iter-001" / "manifest.json"
  how: '`(tmp_path / "sessions" / "iter-001" / "manifest.json").write_text( ''{"agents":[{"id":"a1","tier":"parent","target":"goal:t"}]}'')`
    at line 246'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "agent.json"
  how: '`(d / "agent.json").write_text(''{"owns":["verdict:v1"]}'')` at line 248'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "manifest.json"
  how: '`(d / "manifest.json").write_text("{not json")` at line 257'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.