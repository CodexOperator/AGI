---
id: build:tests-test-snapshot-goals
mint_id: 6822341f98a441c5af4da675e6d7dd90
type: build
parents:
  - idea:engine-tests
  - goal:g1.13
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_snapshot_goals.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_snapshot_goals.py"
---
`extensions/agi/tests/test_snapshot_goals.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_snapshot_goals.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 3'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 4'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 5'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 6'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node
  how: '`node.read_text(encoding="utf-8")` at line 372'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: next((nested / "nodes" / "goal").glob("g1-*.md"))
  how: '`next((nested / "nodes" / "goal").glob("g1-*.md")).read_text()` at line 461'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "GOALS.md"
  how: '`(tmp_path / "GOALS.md").read_text()` at line 689'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: doc
  how: '`doc.read_text()` at line 753'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 916'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 922'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pw
  how: '`pw.read_text()` at line 1001'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 72'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 107'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 109'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 110'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 322'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 325'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node
  how: '`node.read_text()` at line 736'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: doc
  how: '`doc.read_text()` at line 756'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: doc
  how: '`doc.read_text()` at line 760'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "GOALS.md"
  how: '`(tmp_path / "GOALS.md").read_text()` at line 770'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "GOALS.md"
  how: '`(tmp_path / "GOALS.md").read_text()` at line 796'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: bsb
  how: '`bsb.read_text()` at line 949'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 71'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "GOALS.md"
  how: '`(project / "GOALS.md").read_text()` at line 745'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: doc
  how: '`doc.read_text()` at line 851'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 936'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: run
  how: 'defines public function `run` at line 45, signature: (project: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 64, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fm_of
  how: 'defines public function `fm_of` at line 70, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goal_nodes
  how: 'defines public function `goal_nodes` at line 75, signature: (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_node
  how: 'defines public function `write_node` at line 82, signature: (project: Path,
    rel: str, fm: dict, body: str=''body'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parses_ids_titles_statuses
  how: 'defines public function `test_parses_ids_titles_statuses` at line 92, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_next_edges_emitted
  how: 'defines public function `test_no_next_edges_emitted` at line 117, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_status_preserved_and_warns
  how: 'defines public function `test_unknown_status_preserved_and_warns` at line
    127, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_horizon_is_a_known_status
  how: 'defines public function `test_horizon_is_a_known_status` at line 134, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_seeds_populated_from_parent_pointer
  how: 'defines public function `test_seeds_populated_from_parent_pointer` at line
    144, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_goal_ref_warns_but_exits_zero
  how: 'defines public function `test_unknown_goal_ref_warns_but_exits_zero` at line
    159, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_goal_ref_fails_under_strict
  how: 'defines public function `test_unknown_goal_ref_fails_under_strict` at line
    169, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_strict_exits_zero_when_all_refs_resolve
  how: 'defines public function `test_strict_exits_zero_when_all_refs_resolve` at
    line 179, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_non_goal_ref_warns_but_exits_zero
  how: 'defines public function `test_unknown_non_goal_ref_warns_but_exits_zero` at
    line 197, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_non_goal_ref_fails_under_strict
  how: 'defines public function `test_unknown_non_goal_ref_fails_under_strict` at
    line 208, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_known_non_goal_ref_is_not_flagged
  how: 'defines public function `test_known_non_goal_ref_is_not_flagged` at line 217,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prefix_mismatch_reported_distinctly_with_suggestion
  how: 'defines public function `test_prefix_mismatch_reported_distinctly_with_suggestion`
    at line 227, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_genuinely_missing_ref_has_no_suggestion
  how: 'defines public function `test_genuinely_missing_ref_has_no_suggestion` at
    line 241, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goal_ref_message_unchanged_by_the_extension
  how: 'defines public function `test_goal_ref_message_unchanged_by_the_extension`
    at line 252, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_summary_line_splits_prefix_mismatch_from_missing
  how: 'defines public function `test_summary_line_splits_prefix_mismatch_from_missing`
    at line 263, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prune_removes_stale_goals_doc_but_spares_agent_nodes
  how: 'defines public function `test_prune_removes_stale_goals_doc_but_spares_agent_nodes`
    at line 279, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prune_removes_renamed_slug_duplicate
  how: 'defines public function `test_prune_removes_renamed_slug_duplicate` at line
    293, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_goals_md_is_noop_and_prunes_nothing
  how: 'defines public function `test_missing_goals_md_is_noop_and_prunes_nothing`
    at line 305, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_idempotent_byte_identical
  how: 'defines public function `test_idempotent_byte_identical` at line 318, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parse_goals_body_cap
  how: defines public function `test_parse_goals_body_cap` at line 334
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parse_goals_truncates_visibly_at_a_block_boundary
  how: 'defines public function `test_parse_goals_truncates_visibly_at_a_block_boundary`
    at line 344, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_resnapshot_preserves_fields_the_snapshot_does_not_own
  how: 'defines public function `test_resnapshot_preserves_fields_the_snapshot_does_not_own`
    at line 363, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nested
  how: 'defines public function `nested` at line 416, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _by_id
  how: 'defines private function `_by_id` at line 422, signature: (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_subgoals_and_short_term_goals_become_nodes
  how: 'defines public function `test_subgoals_and_short_term_goals_become_nodes`
    at line 427, signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_subgoal_parent_points_at_its_long_term_goal
  how: 'defines public function `test_subgoal_parent_points_at_its_long_term_goal`
    at line 434, signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_short_term_goal_is_a_root_with_no_parent
  how: 'defines public function `test_short_term_goal_is_a_root_with_no_parent` at
    line 444, signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_subgoal_carries_its_own_status
  how: 'defines public function `test_subgoal_carries_its_own_status` at line 452,
    signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_subgoal_body_is_not_absorbed_into_its_parent
  how: 'defines public function `test_subgoal_body_is_not_absorbed_into_its_parent`
    at line 459, signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_long_term_goals_are_unchanged_by_the_new_kinds
  how: 'defines public function `test_long_term_goals_are_unchanged_by_the_new_kinds`
    at line 466, signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sg_run
  how: 'defines private function `_sg_run` at line 477, signature: (project, *extra)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sg_project
  how: 'defines private function `_sg_project` at line 490, signature: (tmp_path,
    goals_md, seed_parent)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_strict_goals_fails_on_a_dangling_goal_reference
  how: 'defines public function `test_strict_goals_fails_on_a_dangling_goal_reference`
    at line 503, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_strict_goals_ignores_non_goal_dangling_parents
  how: 'defines public function `test_strict_goals_ignores_non_goal_dangling_parents`
    at line 512, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_strict_goals_passes_when_every_goal_ref_resolves
  how: 'defines public function `test_strict_goals_passes_when_every_goal_ref_resolves`
    at line 521, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_default_still_only_warns
  how: 'defines public function `test_default_still_only_warns` at line 526, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_frontmatter_preserves_none_scalar
  how: 'defines public function `test_write_frontmatter_preserves_none_scalar` at
    line 549, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_frontmatter_preserves_none_list_entry
  how: 'defines public function `test_write_frontmatter_preserves_none_list_entry`
    at line 554, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_frontmatter_none_survives_a_second_round_trip
  how: 'defines public function `test_write_frontmatter_none_survives_a_second_round_trip`
    at line 559, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: capped_project
  how: 'defines public function `capped_project` at line 575, signature: (tmp_path,
    monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_body_cap_reads_the_project_config
  how: 'defines public function `test_body_cap_reads_the_project_config` at line 583,
    signature: (capped_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_body_cap_falls_back_on_a_broken_config
  how: 'defines public function `test_body_cap_falls_back_on_a_broken_config` at line
    587, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_body_under_the_cap_is_untouched
  how: 'defines public function `test_body_under_the_cap_is_untouched` at line 593,
    signature: (capped_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_truncation_cuts_at_a_block_boundary_and_says_so
  how: 'defines public function `test_truncation_cuts_at_a_block_boundary_and_says_so`
    at line 598, signature: (capped_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_unsplittable_first_block_is_kept_whole_not_severed
  how: 'defines public function `test_an_unsplittable_first_block_is_kept_whole_not_severed`
    at line 614, signature: (capped_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_zero_cap_disables_capping
  how: 'defines public function `test_zero_cap_disables_capping` at line 623, signature:
    (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_truncation_is_never_silent
  how: 'defines public function `test_truncation_is_never_silent` at line 630, signature:
    (capped_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bare_invocation_refuses_to_guess_a_direction
  how: 'defines public function `test_bare_invocation_refuses_to_guess_a_direction`
    at line 644, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_round_trip_is_byte_identical
  how: 'defines public function `test_round_trip_is_byte_identical` at line 654, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_heading_level_is_stored_not_inferred
  how: 'defines public function `test_heading_level_is_stored_not_inferred` at line
    663, signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_document_order_is_naturally_sorted_by_goal_id_on_render
  how: 'defines public function `test_document_order_is_naturally_sorted_by_goal_id_on_render`
    at line 677, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_natural_sort_orders_dotted_subgoals_numerically
  how: defines public function `test_natural_sort_orders_dotted_subgoals_numerically`
    at line 696
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_natural_sort_orders_short_term_goals_numerically
  how: defines public function `test_natural_sort_orders_short_term_goals_numerically`
    at line 704
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_natural_sort_puts_g_goals_before_s_goals
  how: defines public function `test_natural_sort_puts_g_goals_before_s_goals` at
    line 710
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_natural_sort_full_worked_example
  how: defines public function `test_natural_sort_full_worked_example` at line 716
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preamble_becomes_a_doc_node_not_a_goal
  how: 'defines public function `test_preamble_becomes_a_doc_node_not_a_goal` at line
    727, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_banner_does_not_accrete_across_round_trips
  how: 'defines public function `test_the_banner_does_not_accrete_across_round_trips`
    at line 740, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_deleting_a_heading_does_not_delete_the_node
  how: 'defines public function `test_deleting_a_heading_does_not_delete_the_node`
    at line 748, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_refuses_to_write_an_empty_document
  how: 'defines public function `test_render_refuses_to_write_an_empty_document` at
    line 763, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_goal_node_missing_heading_level_is_a_hard_error
  how: 'defines public function `test_a_goal_node_missing_heading_level_is_a_hard_error`
    at line 773, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_goal_node_missing_order_renders_without_error
  how: 'defines public function `test_a_goal_node_missing_order_renders_without_error`
    at line 783, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_integrity_check_runs_in_the_render_direction_too
  how: 'defines public function `test_integrity_check_runs_in_the_render_direction_too`
    at line 799, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_frontmatter_preserves_embedded_double_quotes
  how: 'defines public function `test_write_frontmatter_preserves_embedded_double_quotes`
    at line 810, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_frontmatter_preserves_backslashes
  how: 'defines public function `test_write_frontmatter_preserves_backslashes` at
    line 821, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prune_only_touches_nodes_this_script_can_produce
  how: 'defines public function `test_prune_only_touches_nodes_this_script_can_produce`
    at line 827, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prune_still_removes_a_goal_the_document_dropped
  how: 'defines public function `test_prune_still_removes_a_goal_the_document_dropped`
    at line 845, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_extract_thought_absent_is_none
  how: defines public function `test_extract_thought_absent_is_none` at line 860
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_extract_thought_returns_block_with_markers
  how: defines public function `test_extract_thought_returns_block_with_markers` at
    line 868
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_extract_thought_is_multiline_and_non_greedy
  how: defines public function `test_extract_thought_is_multiline_and_non_greedy`
    at line 876
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_splice_carries_thought_across_a_regenerating_write
  how: defines public function `test_splice_carries_thought_across_a_regenerating_write`
    at line 884
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_splice_prefers_a_thought_authored_this_pass
  how: defines public function `test_splice_prefers_a_thought_authored_this_pass`
    at line 894
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_splice_is_a_noop_without_a_stored_thought
  how: defines public function `test_splice_is_a_noop_without_a_stored_thought` at
    line 903
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_frontmatter_preserves_thought_block
  how: 'defines public function `test_write_frontmatter_preserves_thought_block` at
    line 908, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_frontmatter_without_preserve_body_still_wipes
  how: 'defines public function `test_write_frontmatter_without_preserve_body_still_wipes`
    at line 928, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_one_serializer_not_two
  how: defines public function `test_one_serializer_not_two` at line 939
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_strip_thought_removes_the_block
  how: defines public function `test_strip_thought_removes_the_block` at line 959
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_strip_thought_is_a_noop_without_one
  how: defines public function `test_strip_thought_is_a_noop_without_one` at line
    966
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_strips_thought_but_the_node_keeps_it
  how: defines public function `test_render_strips_thought_but_the_node_keeps_it`
    at line 971
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_check_round_trip_survives_a_thought
  how: defines public function `test_render_check_round_trip_survives_a_thought` at
    line 982
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_does_not_define_its_own_serializer
  how: defines public function `test_post_wire_does_not_define_its_own_serializer`
    at line 993
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "GOALS.md"
  how: '`(tmp_path / "GOALS.md").write_text(GOALS_DOC, encoding="utf-8")` at line
    65'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node
  how: '`node.write_text( f"---{head}next_edges:\n  - idea:seeded\nembedding_coords:
    [0.1, 0.2]\n" f"---{body}", encoding="utf-8", )` at line 374'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "GOALS.md"
  how: '`(tmp_path / "GOALS.md").write_text(NESTED_DOC, encoding="utf-8")` at line
    417'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 491'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "GOALS.md"
  how: '`(tmp_path / "GOALS.md").write_text(goals_md)` at line 492'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "seed.md"
  how: '`(d / "seed.md").write_text( f''---\nid: "idea:seed"\ntype: idea\nparents:\n  -
    {seed_parent}\n---\n\nbody\n'')` at line 495'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text(''{"goal_body_cap": 120}'')`
    at line 578'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{not json")` at line 588'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text(''{"goal_body_cap": 0}'')`
    at line 624'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "GOALS.md"
  how: '`(tmp_path / "GOALS.md").write_text(doc)` at line 685'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: doc
  how: '`doc.write_text(before.replace( "## G2 — Persistent ideation system — status:
    active\n\nAdapt the research loop.\n", ""))` at line 754'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "GOALS.md"
  how: '`(tmp_path / "GOALS.md").write_text("# real content\n")` at line 767'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: doc
  how: '`doc.write_text(doc.read_text().replace( "## G2 — Persistent ideation system
    — status: active\n\nAdapt the research loop.\n", ""))` at line 851'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
One test added for the widened [goal].md spawn rule: a goal may carry a build parent, and the GOALS.md->nodes import must keep it while still replacing the goal parent from the heading hierarchy. The fixture writes the prior node at the slug the import rewrites, so the case is one node coming back rather than two files sharing an id, and it plants a deliberately wrong goal parent to prove the derived half still wins.
<!-- THOUGHT:END -->