---
confidence: 1.0
id: "level3:tests-test-level3"
origin: level3-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_level3.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/tests/test_level3.py"
type: level3
---

`extensions/agi/tests/test_level3.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_level3.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(yaml_block)` at line 137'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 415'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(path.read_text(encoding=''utf-8'').split(''---'', 2)[1])`
    at line 127'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 399'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 402'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 131'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 127'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: write_engine_tree
  how: 'defines public function `write_engine_tree` at line 89, signature: (root:
    Path, files: dict[str, str] | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine
  how: 'defines public function `engine` at line 103, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 108, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run
  how: 'defines public function `run` at line 118, signature: (project: Path, engine:
    Path | None, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fm_of
  how: 'defines public function `fm_of` at line 126, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: body_of
  how: 'defines public function `body_of` at line 130, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: contract_of
  how: 'defines public function `contract_of` at line 134, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: level3_nodes
  how: 'defines public function `level3_nodes` at line 140, signature: (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_node
  how: 'defines public function `write_node` at line 145, signature: (project: Path,
    rel: str, fm: dict, body: str=''body'', origin: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_default_engine_root_points_at_this_repo
  how: defines public function `test_default_engine_root_points_at_this_repo` at line
    155
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_discovers_every_file_passing_the_g6_8_boundary
  how: 'defines public function `test_discovers_every_file_passing_the_g6_8_boundary`
    at line 164, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_files_scanned_count_matches_the_boundary
  how: 'defines public function `test_files_scanned_count_matches_the_boundary` at
    line 193, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_python_payload_is_honest_about_not_being_parsed
  how: 'defines public function `test_non_python_payload_is_honest_about_not_being_parsed`
    at line 202, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_empty_scope_is_refused_never_treated_as_prune_everything
  how: 'defines public function `test_empty_scope_is_refused_never_treated_as_prune_everything`
    at line 214, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_frontmatter_uses_payload_ref_and_origin_only
  how: 'defines public function `test_frontmatter_uses_payload_ref_and_origin_only`
    at line 234, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_imports_and_top_level_defs_are_derived
  how: 'defines public function `test_imports_and_top_level_defs_are_derived` at line
    250, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_write_calls_argv_env_stdout_are_derived
  how: 'defines public function `test_read_write_calls_argv_env_stdout_are_derived`
    at line 272, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_literal_open_mode_is_uncovered_not_guessed
  how: 'defines public function `test_non_literal_open_mode_is_uncovered_not_guessed`
    at line 291, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_syntax_error_file_gets_parse_ok_false_and_empty_contract
  how: 'defines public function `test_syntax_error_file_gets_parse_ok_false_and_empty_contract`
    at line 309, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_empty_file_gets_empty_but_present_contract_lists
  how: 'defines public function `test_empty_file_gets_empty_but_present_contract_lists`
    at line 319, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bin_script_matches_exact_unit_path
  how: 'defines public function `test_bin_script_matches_exact_unit_path` at line
    331, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_src_package_matches_directory_prefix
  how: 'defines public function `test_src_package_matches_directory_prefix` at line
    337, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_matching_unit_is_parentless_and_flagged
  how: 'defines public function `test_no_matching_unit_is_parentless_and_flagged`
    at line 343, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_engine_root_is_noop
  how: 'defines public function `test_missing_engine_root_is_noop` at line 356, signature:
    (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_git_engine_root_is_noop
  how: 'defines public function `test_non_git_engine_root_is_noop` at line 364, signature:
    (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_engine_root_prunes_nothing
  how: 'defines public function `test_missing_engine_root_prunes_nothing` at line
    373, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_writes_nothing
  how: 'defines public function `test_dry_run_writes_nothing` at line 387, signature:
    (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_idempotent_byte_identical
  how: 'defines public function `test_idempotent_byte_identical` at line 397, signature:
    (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_twice_round_trip_preserves_foreign_field
  how: 'defines public function `test_write_twice_round_trip_preserves_foreign_field`
    at line 411, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prune_removes_stale_level3_scan_but_spares_others
  how: 'defines public function `test_prune_removes_stale_level3_scan_but_spares_others`
    at line 435, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_project_local_script_lookup_argument_exists
  how: defines public function `test_no_project_local_script_lookup_argument_exists`
    at line 463
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text(f''---{head}next_edges:\n  - hyp:graph-core-r1\nembedding_coords:
    [0.1, 0.2]\n---{body}'', encoding=''utf-8'')` at line 417'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(content, encoding=''utf-8'')` at line 96'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
