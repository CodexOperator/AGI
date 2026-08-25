---
confidence: 1.0
id: "level3:tests-test-grid"
mint_id: e13d59c2cdd94a09aed671ce4e8b0d10
origin: level3-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_grid.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/tests/test_grid.py"
type: level3
---

`extensions/agi/tests/test_grid.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_grid.py
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
- name: f
  how: '`f.read_text()` at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 587'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 589'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 698'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 700'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 712'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.read_text()` at line 68'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 444'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 456'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 488'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: project
  how: 'defines public function `project` at line 23, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: versions
  how: 'defines public function `versions` at line 35, signature: (root, node_id)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_init_idempotent_and_refuses_non_repo
  how: 'defines public function `test_init_idempotent_and_refuses_non_repo` at line
    45, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_commit_creates_version_and_skips_unchanged
  how: 'defines public function `test_commit_creates_version_and_skips_unchanged`
    at line 51, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_grid_refs_stay_out_of_branch_listing
  how: 'defines public function `test_grid_refs_stay_out_of_branch_listing` at line
    59, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_edit_makes_v2_and_diff_shows_it
  how: 'defines public function `test_edit_makes_v2_and_diff_shows_it` at line 65,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_session_branch_is_separate_dimension
  how: 'defines public function `test_session_branch_is_separate_dimension` at line
    76, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_without_id_is_skipped
  how: 'defines public function `test_node_without_id_is_skipped` at line 86, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_commit_prefix_marks_auto_snapshots
  how: 'defines public function `test_commit_prefix_marks_auto_snapshots` at line
    92, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_refuses_ref_hostile_chars
  how: defines public function `test_sanitize_refuses_ref_hostile_chars` at line 101
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cron_lines_are_cwd_proof
  how: 'defines public function `test_cron_lines_are_cwd_proof` at line 108, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sync_pushes_grid_refs_and_sets_fetch_spec
  how: 'defines public function `test_sync_pushes_grid_refs_and_sets_fetch_spec` at
    line 119, signature: (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_find_project_root_accepts_canonical_and_legacy_config
  how: 'defines public function `test_find_project_root_accepts_canonical_and_legacy_config`
    at line 135, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_only_the_first_colon_separates
  how: defines public function `test_only_the_first_colon_separates` at line 152
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_node_ref_is_a_path_prefix_of_another
  how: defines public function `test_no_node_ref_is_a_path_prefix_of_another` at line
    165
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_is_injective_across_colon_and_dash
  how: defines public function `test_sanitize_is_injective_across_colon_and_dash`
    at line 175
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_escape_alphabet_cannot_be_forged
  how: defines public function `test_escape_alphabet_cannot_be_forged` at line 180
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_is_injective_over_adversarial_corpus
  how: defines public function `test_sanitize_is_injective_over_adversarial_corpus`
    at line 210
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_output_is_a_valid_git_refname
  how: defines public function `test_sanitize_output_is_a_valid_git_refname` at line
    219
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_real_agi_tree_corpus_round_trips_distinctly
  how: defines public function `test_sanitize_real_agi_tree_corpus_round_trips_distinctly`
    at line 234
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: migrate_project
  how: 'defines public function `migrate_project` at line 266, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_node
  how: 'defines private function `_write_node` at line 274, signature: (root, rel,
    node_id, body=''body\n'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_refs_dry_run_changes_nothing
  how: 'defines public function `test_migrate_refs_dry_run_changes_nothing` at line
    280, signature: (migrate_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_refs_write_moves_ref_and_preserves_history
  how: 'defines public function `test_migrate_refs_write_moves_ref_and_preserves_history`
    at line 293, signature: (migrate_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_refs_is_idempotent
  how: 'defines public function `test_migrate_refs_is_idempotent` at line 310, signature:
    (migrate_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_refs_refuses_to_overwrite_conflicting_destination
  how: 'defines public function `test_migrate_refs_refuses_to_overwrite_conflicting_destination`
    at line 325, signature: (migrate_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_refs_reports_collision_and_touches_neither_id
  how: 'defines public function `test_migrate_refs_reports_collision_and_touches_neither_id`
    at line 346, signature: (migrate_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_project
  how: 'defines public function `mint_project` at line 380, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_mint_node
  how: 'defines private function `_write_mint_node` at line 388, signature: (root,
    rel, node_id, mint_id=None, parents=None, body=''body\n'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_ref_for_raises_on_missing_mint_id
  how: 'defines public function `test_write_ref_for_raises_on_missing_mint_id` at
    line 401, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_ref_for_returns_mint_ref_when_present
  how: 'defines public function `test_write_ref_for_returns_mint_ref_when_present`
    at line 407, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_commit_all_skips_missing_mint_id_but_keeps_going
  how: 'defines public function `test_commit_all_skips_missing_mint_id_but_keeps_going`
    at line 412, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_commit_never_falls_back_to_node_id_ref_for_missing_mint_id
  how: 'defines public function `test_commit_never_falls_back_to_node_id_ref_for_missing_mint_id`
    at line 426, signature: (mint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_falls_back_to_legacy_ref_when_no_mint_ref_exists
  how: 'defines public function `test_read_falls_back_to_legacy_ref_when_no_mint_ref_exists`
    at line 436, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_versions_falls_back_to_legacy_ref
  how: 'defines public function `test_versions_falls_back_to_legacy_ref` at line 452,
    signature: (mint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_clean_via_legacy_ref_for_node_without_mint_id_yet
  how: 'defines public function `test_status_clean_via_legacy_ref_for_node_without_mint_id_yet`
    at line 465, signature: (mint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_falls_back_to_legacy_ref_instead_of_reporting_new
  how: 'defines public function `test_status_falls_back_to_legacy_ref_instead_of_reporting_new`
    at line 479, signature: (mint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_reports_new_when_neither_ref_exists
  how: 'defines public function `test_status_reports_new_when_neither_ref_exists`
    at line 498, signature: (mint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_mint_trailer_in_commit_body
  how: 'defines public function `test_parent_mint_trailer_in_commit_body` at line
    506, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_mint_trailer_marks_unresolved_parent
  how: 'defines public function `test_parent_mint_trailer_marks_unresolved_parent`
    at line 522, signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_parents_means_no_trailer_body
  how: 'defines public function `test_no_parents_means_no_trailer_body` at line 533,
    signature: (mint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_node_ref_is_a_valid_git_ref
  how: defines public function `test_mint_node_ref_is_a_valid_git_ref` at line 541
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_node_ref_is_identity_under_sanitize
  how: defines public function `test_mint_node_ref_is_identity_under_sanitize` at
    line 547
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: migmint_project
  how: 'defines public function `migmint_project` at line 563, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_dry_run_changes_nothing
  how: 'defines public function `test_migrate_mint_refs_dry_run_changes_nothing` at
    line 571, signature: (migmint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_write_moves_ref_and_preserves_full_history
  how: 'defines public function `test_migrate_mint_refs_write_moves_ref_and_preserves_full_history`
    at line 583, signature: (migmint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_is_idempotent
  how: 'defines public function `test_migrate_mint_refs_is_idempotent` at line 602,
    signature: (migmint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_second_run_reports_zero_moved
  how: 'defines public function `test_migrate_mint_refs_second_run_reports_zero_moved`
    at line 616, signature: (migmint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_refuses_to_overwrite_conflicting_destination
  how: 'defines public function `test_migrate_mint_refs_refuses_to_overwrite_conflicting_destination`
    at line 627, signature: (migmint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_conflict_is_reported
  how: 'defines public function `test_migrate_mint_refs_conflict_is_reported` at line
    646, signature: (migmint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_skips_node_without_mint_id_not_guessed
  how: 'defines public function `test_migrate_mint_refs_skips_node_without_mint_id_not_guessed`
    at line 659, signature: (migmint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_migrate_mint_refs_reports_duplicate_mint_id_collision
  how: 'defines public function `test_migrate_mint_refs_reports_duplicate_mint_id_collision`
    at line 674, signature: (migmint_project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_versions_and_log_report_full_history_after_migration
  how: 'defines public function `test_versions_and_log_report_full_history_after_migration`
    at line 691, signature: (migmint_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'agi-tree.config.json'
  how: '`(tmp_path / ''agi-tree.config.json'').write_text(''{}'')` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / 'x.md'
  how: '`(d / ''x.md'').write_text(f''---\nid: "idea:x"\nmint_id: {MINT_X}\ntype:
    idea\n---\n\nfirst thought\n'')` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'agi-tree.config.json'
  how: '`(tmp_path / ''agi-tree.config.json'').write_text(''{}'')` at line 46'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.write_text(f.read_text().replace(''first thought'', ''second thought''))`
    at line 68'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.write_text(f.read_text() + ''\ndraft addition\n'')` at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'nodes' / 'idea' / 'noid.md'
  how: '`(project / ''nodes'' / ''idea'' / ''noid.md'').write_text(''no frontmatter
    here\n'')` at line 87'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: canonical / 'agi-tree.config.json'
  how: '`(canonical / ''agi-tree.config.json'').write_text(''{}'')` at line 143'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: legacy / 'autoresearch-tree.config.json'
  how: '`(legacy / ''autoresearch-tree.config.json'').write_text(''{}'')` at line
    144'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'agi-tree.config.json'
  how: '`(tmp_path / ''agi-tree.config.json'').write_text(''{}'')` at line 268'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(f''---\nid: "{node_id}"\ntype: level3\n---\n\n{body}'')` at
    line 276'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'agi-tree.config.json'
  how: '`(tmp_path / ''agi-tree.config.json'').write_text(''{}'')` at line 382'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(''---\n'' + ''\n''.join(fm) + f''\n---\n\n{body}'')` at line
    397'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text().replace(''id: "idea:x"'', f''id: "idea:x"\nmint_id:
    {MINT_A}''))` at line 444'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text().replace(''id: "idea:x"'', f''id: "idea:x"\nmint_id:
    {MINT_A}''))` at line 456'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text().replace(''id: "idea:x"'', f''id: "idea:x"\nmint_id:
    {MINT_A}''))` at line 488'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'agi-tree.config.json'
  how: '`(tmp_path / ''agi-tree.config.json'').write_text(''{}'')` at line 565'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text() + ''\nedit 2\n'')` at line 587'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text() + ''\nedit 3\n'')` at line 589'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text() + ''\nedit 2\n'')` at line 698'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text() + ''\nedit 3\n'')` at line 700'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(p.read_text() + ''\nedit 4\n'')` at line 712'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
