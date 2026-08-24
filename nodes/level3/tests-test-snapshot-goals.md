---
confidence: 1.0
id: "level3:tests-test-snapshot-goals"
origin: level3-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_snapshot_goals.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/tests/test_snapshot_goals.py"
type: level3
---

`extensions/agi/tests/test_snapshot_goals.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
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
  how: '`node.read_text(encoding=''utf-8'')` at line 341'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: next((nested / 'nodes' / 'goal').glob('g1-*.md'))
  how: '`next((nested / ''nodes'' / ''goal'').glob(''g1-*.md'')).read_text()` at line
    430'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 62'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 97'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 99'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 100'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 312'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 315'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 61'
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
  how: 'defines public function `project` at line 54, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fm_of
  how: 'defines public function `fm_of` at line 60, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goal_nodes
  how: 'defines public function `goal_nodes` at line 65, signature: (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_node
  how: 'defines public function `write_node` at line 72, signature: (project: Path,
    rel: str, fm: dict, body: str=''body'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parses_ids_titles_statuses
  how: 'defines public function `test_parses_ids_titles_statuses` at line 82, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_next_edges_emitted
  how: 'defines public function `test_no_next_edges_emitted` at line 107, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_status_preserved_and_warns
  how: 'defines public function `test_unknown_status_preserved_and_warns` at line
    117, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_horizon_is_a_known_status
  how: 'defines public function `test_horizon_is_a_known_status` at line 124, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_seeds_populated_from_parent_pointer
  how: 'defines public function `test_seeds_populated_from_parent_pointer` at line
    134, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_goal_ref_warns_but_exits_zero
  how: 'defines public function `test_unknown_goal_ref_warns_but_exits_zero` at line
    149, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_goal_ref_fails_under_strict
  how: 'defines public function `test_unknown_goal_ref_fails_under_strict` at line
    159, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_strict_exits_zero_when_all_refs_resolve
  how: 'defines public function `test_strict_exits_zero_when_all_refs_resolve` at
    line 169, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_non_goal_ref_warns_but_exits_zero
  how: 'defines public function `test_unknown_non_goal_ref_warns_but_exits_zero` at
    line 187, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_non_goal_ref_fails_under_strict
  how: 'defines public function `test_unknown_non_goal_ref_fails_under_strict` at
    line 198, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_known_non_goal_ref_is_not_flagged
  how: 'defines public function `test_known_non_goal_ref_is_not_flagged` at line 207,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prefix_mismatch_reported_distinctly_with_suggestion
  how: 'defines public function `test_prefix_mismatch_reported_distinctly_with_suggestion`
    at line 217, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_genuinely_missing_ref_has_no_suggestion
  how: 'defines public function `test_genuinely_missing_ref_has_no_suggestion` at
    line 231, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goal_ref_message_unchanged_by_the_extension
  how: 'defines public function `test_goal_ref_message_unchanged_by_the_extension`
    at line 242, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_summary_line_splits_prefix_mismatch_from_missing
  how: 'defines public function `test_summary_line_splits_prefix_mismatch_from_missing`
    at line 253, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prune_removes_stale_goals_doc_but_spares_agent_nodes
  how: 'defines public function `test_prune_removes_stale_goals_doc_but_spares_agent_nodes`
    at line 269, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prune_removes_renamed_slug_duplicate
  how: 'defines public function `test_prune_removes_renamed_slug_duplicate` at line
    283, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_goals_md_is_noop_and_prunes_nothing
  how: 'defines public function `test_missing_goals_md_is_noop_and_prunes_nothing`
    at line 295, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_idempotent_byte_identical
  how: 'defines public function `test_idempotent_byte_identical` at line 308, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parse_goals_body_cap
  how: defines public function `test_parse_goals_body_cap` at line 324
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_resnapshot_preserves_fields_the_snapshot_does_not_own
  how: 'defines public function `test_resnapshot_preserves_fields_the_snapshot_does_not_own`
    at line 332, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nested
  how: 'defines public function `nested` at line 385, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _by_id
  how: 'defines private function `_by_id` at line 391, signature: (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_subgoals_and_short_term_goals_become_nodes
  how: 'defines public function `test_subgoals_and_short_term_goals_become_nodes`
    at line 396, signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_subgoal_parent_points_at_its_long_term_goal
  how: 'defines public function `test_subgoal_parent_points_at_its_long_term_goal`
    at line 403, signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_short_term_goal_is_a_root_with_no_parent
  how: 'defines public function `test_short_term_goal_is_a_root_with_no_parent` at
    line 413, signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_subgoal_carries_its_own_status
  how: 'defines public function `test_subgoal_carries_its_own_status` at line 421,
    signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_subgoal_body_is_not_absorbed_into_its_parent
  how: 'defines public function `test_subgoal_body_is_not_absorbed_into_its_parent`
    at line 428, signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_long_term_goals_are_unchanged_by_the_new_kinds
  how: 'defines public function `test_long_term_goals_are_unchanged_by_the_new_kinds`
    at line 435, signature: (nested)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sg_run
  how: 'defines private function `_sg_run` at line 446, signature: (project, *extra)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sg_project
  how: 'defines private function `_sg_project` at line 455, signature: (tmp_path,
    goals_md, seed_parent)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_strict_goals_fails_on_a_dangling_goal_reference
  how: 'defines public function `test_strict_goals_fails_on_a_dangling_goal_reference`
    at line 468, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_strict_goals_ignores_non_goal_dangling_parents
  how: 'defines public function `test_strict_goals_ignores_non_goal_dangling_parents`
    at line 477, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_strict_goals_passes_when_every_goal_ref_resolves
  how: 'defines public function `test_strict_goals_passes_when_every_goal_ref_resolves`
    at line 486, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_default_still_only_warns
  how: 'defines public function `test_default_still_only_warns` at line 491, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'GOALS.md'
  how: '`(tmp_path / ''GOALS.md'').write_text(GOALS_DOC, encoding=''utf-8'')` at line
    55'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node
  how: '`node.write_text(f''---{head}next_edges:\n  - idea:seeded\nembedding_coords:
    [0.1, 0.2]\n---{body}'', encoding=''utf-8'')` at line 343'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'GOALS.md'
  how: '`(tmp_path / ''GOALS.md'').write_text(NESTED_DOC, encoding=''utf-8'')` at
    line 386'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'agi-tree.config.json'
  how: '`(tmp_path / ''agi-tree.config.json'').write_text(''{}'')` at line 456'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'GOALS.md'
  how: '`(tmp_path / ''GOALS.md'').write_text(goals_md)` at line 457'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / 'seed.md'
  how: '`(d / ''seed.md'').write_text(f''---\nid: "idea:seed"\ntype: idea\nparents:\n  -
    {seed_parent}\n---\n\nbody\n'')` at line 460'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
