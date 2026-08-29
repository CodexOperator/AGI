---
build_kind: code
confidence: 1.0
id: "build:tests-test-unify"
mint_id: a2c72e35f9de48f1a04be896c0643dc7
origin: build-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_unify.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_unify.py"
type: build
---

`extensions/agi/tests/test_unify.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_unify.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hashlib
  how: '`import hashlib` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: unify
  how: '`import unify` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / ".gitignore"
  how: '`(engine / ".gitignore").read_text()` at line 318'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(capsys.readouterr().out)` at line 466'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "GOALS.md"
  how: '`(engine / "GOALS.md").read_text()` at line 227'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / ".agi" / "config.json"
  how: '`(engine / ".agi" / "config.json").read_text()` at line 234'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 163'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _git
  how: 'defines private function `_git` at line 31, signature: (repo: Path, *args:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rev_parse
  how: 'defines private function `_rev_parse` at line 41, signature: (repo: Path,
    ref: str=''HEAD'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: make_tree_repo
  how: 'defines public function `make_tree_repo` at line 92, signature: (tmp_path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _root_commit
  how: 'defines private function `_root_commit` at line 129, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: make_engine_repo
  how: 'defines public function `make_engine_repo` at line 136, signature: (tmp_path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _hash_tree
  how: 'defines private function `_hash_tree` at line 157, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repos
  how: 'defines public function `repos` at line 168, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: migrated
  how: 'defines public function `migrated` at line 175, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_histories_are_ancestors_of_head
  how: 'defines public function `test_both_histories_are_ancestors_of_head` at line
    195, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_grid_refs_transfer_with_count_and_target_preserved
  how: 'defines public function `test_grid_refs_transfer_with_count_and_target_preserved`
    at line 211, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goals_md_ends_at_repo_root_not_inside_dot_agi
  how: 'defines public function `test_goals_md_ends_at_repo_root_not_inside_dot_agi`
    at line 223, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_config_ends_at_dot_agi_config_json
  how: 'defines public function `test_config_ends_at_dot_agi_config_json` at line
    230, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_find_project_root_resolves_to_dot_agi
  how: 'defines public function `test_find_project_root_resolves_to_dot_agi` at line
    237, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_node_file_bytes_change
  how: 'defines public function `test_no_node_file_bytes_change` at line 246, signature:
    (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_report_node_count_matches
  how: 'defines public function `test_report_node_count_matches` at line 253, signature:
    (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_drops_symlink_entries
  how: defines public function `test_merge_gitignore_drops_symlink_entries` at line
    260
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_reroots_generated_paths
  how: defines public function `test_merge_gitignore_reroots_generated_paths` at line
    267
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_reroot_beats_dedup_for_names_shared_with_the_engine
  how: defines public function `test_merge_gitignore_reroot_beats_dedup_for_names_shared_with_the_engine`
    at line 281
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_dedupes_generic_patterns
  how: defines public function `test_merge_gitignore_dedupes_generic_patterns` at
    line 295
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_keeps_uniques_from_both_sides
  how: defines public function `test_merge_gitignore_keeps_uniques_from_both_sides`
    at line 301
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_merge_gitignore_preserves_explanatory_comments
  how: defines public function `test_merge_gitignore_preserves_explanatory_comments`
    at line 308
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_end_to_end_gitignore_is_one_file_at_root
  how: 'defines public function `test_end_to_end_gitignore_is_one_file_at_root` at
    line 314, signature: (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_mutates_nothing
  how: 'defines public function `test_dry_run_mutates_nothing` at line 326, signature:
    (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_explicit_dry_run_flag_overrides_yes
  how: 'defines public function `test_explicit_dry_run_flag_overrides_yes` at line
    341, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_dirty_target
  how: 'defines public function `test_preflight_refuses_dirty_target` at line 354,
    signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_target_that_already_has_dot_agi
  how: 'defines public function `test_preflight_refuses_target_that_already_has_dot_agi`
    at line 362, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_missing_source
  how: 'defines public function `test_preflight_refuses_missing_source` at line 370,
    signature: (tmp_path, repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_dirty_source
  how: 'defines public function `test_preflight_refuses_dirty_source` at line 378,
    signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_force_allows_dirty_and_existing_agi
  how: 'defines public function `test_preflight_force_allows_dirty_and_existing_agi`
    at line 386, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_refuses_the_real_repos
  how: 'defines public function `test_preflight_refuses_the_real_repos` at line 394,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_preflight_force_does_not_bypass_real_repo_guard
  how: 'defines public function `test_preflight_force_does_not_bypass_real_repo_guard`
    at line 406, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_second_run_refuses_cleanly
  how: 'defines public function `test_second_run_refuses_cleanly` at line 416, signature:
    (migrated)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_graft_graph_alone
  how: 'defines public function `test_graft_graph_alone` at line 434, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_relocate_files_requires_a_prior_graft
  how: 'defines public function `test_relocate_files_requires_a_prior_graft` at line
    442, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_fetch_grid_refs_raises_on_a_bad_remote
  how: 'defines public function `test_fetch_grid_refs_raises_on_a_bad_remote` at line
    449, signature: (repos)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_report_json_on_dry_run
  how: 'defines public function `test_cli_report_json_on_dry_run` at line 461, signature:
    (repos, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_yes_runs_the_real_migration
  how: 'defines public function `test_cli_yes_runs_the_real_migration` at line 470,
    signature: (repos, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "agi-tree.config.json"
  how: '`(d / "agi-tree.config.json").write_text(''{"metric_primary": "outcome_coverage"}\n'')`
    at line 99'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "GOALS.md"
  how: '`(d / "GOALS.md").write_text("# GOALS\n\n## G1: something\n")` at line 100'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / ".gitignore"
  how: '`(d / ".gitignore").write_text(TREE_GITIGNORE)` at line 101'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goal_dir / "g1.md"
  how: '`(goal_dir / "g1.md").write_text( ''---\nid: "goal:g1"\nmint_id: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\ntype:
    goal\n'' ''---\n\nfirst version of g1\n'' )` at line 104'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: kits_dir / "example.md"
  how: '`(kits_dir / "example.md").write_text("a kit\n")` at line 110'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goal_dir / "g1.md"
  how: '`(goal_dir / "g1.md").write_text( ''---\nid: "goal:g1"\nmint_id: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\ntype:
    goal\n'' ''---\n\nsecond version of g1, edited\n'' )` at line 116'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / ".gitignore"
  how: '`(d / ".gitignore").write_text(ENGINE_GITIGNORE)` at line 143'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ext / "hello.py"
  how: '`(ext / "hello.py").write_text("print(''hello'')\n")` at line 146'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ext / "hello.py"
  how: '`(ext / "hello.py").write_text("print(''hello world'')\n")` at line 151'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions" / "agi" / "bin" / "hello.py"
  how: '`(engine / "extensions" / "agi" / "bin" / "hello.py").write_text("dirty\n")`
    at line 356'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tree / "nodes" / "goal" / "g1.md"
  how: '`(tree / "nodes" / "goal" / "g1.md").write_text("uncommitted edit\n")` at
    line 380'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / "extensions" / "agi" / "bin" / "hello.py"
  how: '`(engine / "extensions" / "agi" / "bin" / "hello.py").write_text("dirty\n")`
    at line 389'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
