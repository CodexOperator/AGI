---
confidence: 1.0
id: "level3:tests-test-stitch"
origin: level3-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_stitch.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/tests/test_stitch.py"
type: level3
---

`extensions/agi/tests/test_stitch.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_stitch.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 412'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 453'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 466'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 500'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 519'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 556'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out / 'stray.txt'
  how: '`(out / ''stray.txt'').read_text()` at line 175'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out / 'extensions/agi/bin/foo.py'
  how: '`(out / ''extensions/agi/bin/foo.py'').read_bytes()` at line 224'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / 'extensions/agi/bin/foo.py'
  how: '`(engine / ''extensions/agi/bin/foo.py'').read_bytes()` at line 225'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out / rel
  how: '`(out / rel).read_bytes()` at line 135'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / rel
  how: '`(engine / rel).read_bytes()` at line 135'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: write_engine_tree
  how: 'defines public function `write_engine_tree` at line 42, signature: (root:
    Path, files: dict[str, str] | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine
  how: 'defines public function `engine` at line 56, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 61, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_node
  how: 'defines public function `mint_node` at line 67, signature: (engine_root: Path,
    project_root: Path, rel_path: str, parent_id: str | None=None, id_suffix: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_version_node
  how: 'defines public function `mint_version_node` at line 85, signature: (engine_root:
    Path, project_root: Path, rel_path: str, version: int, supersedes: str | None=None,
    base_node_id: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run
  how: 'defines public function `run` at line 111, signature: (project: Path, engine:
    Path | None, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_copies_every_payload_byte_identical
  how: 'defines public function `test_materialize_copies_every_payload_byte_identical`
    at line 122, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_preserves_relative_structure
  how: 'defines public function `test_materialize_preserves_relative_structure` at
    line 138, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_zero_nodes_writes_nothing
  how: 'defines public function `test_materialize_zero_nodes_writes_nothing` at line
    145, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_refuses_nonempty_out_without_force
  how: 'defines public function `test_materialize_refuses_nonempty_out_without_force`
    at line 155, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_force_writes_into_nonempty_out
  how: 'defines public function `test_materialize_force_writes_into_nonempty_out`
    at line 167, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_refuses_to_write_into_project_root
  how: 'defines public function `test_materialize_refuses_to_write_into_project_root`
    at line 179, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_refuses_to_write_into_engine_root
  how: 'defines public function `test_materialize_refuses_to_write_into_engine_root`
    at line 185, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_refuses_to_write_into_subdir_of_engine_root
  how: 'defines public function `test_materialize_refuses_to_write_into_subdir_of_engine_root`
    at line 191, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_skips_missing_payload_and_reports_it
  how: 'defines public function `test_materialize_skips_missing_payload_and_reports_it`
    at line 200, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_first_writer_wins_on_duplicate_ref
  how: 'defines public function `test_materialize_first_writer_wins_on_duplicate_ref`
    at line 210, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_finds_missing_payload
  how: 'defines public function `test_verify_finds_missing_payload` at line 231, signature:
    (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_has_drift_false_when_all_categories_empty
  how: defines public function `test_has_drift_false_when_all_categories_empty` at
    line 241
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_clean_tree_has_no_drift
  how: 'defines public function `test_verify_clean_tree_has_no_drift` at line 247,
    signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_finds_orphan_file
  how: 'defines public function `test_verify_finds_orphan_file` at line 262, signature:
    (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_orphan_scan_skips_when_engine_not_git_repo
  how: 'defines public function `test_verify_orphan_scan_skips_when_engine_not_git_repo`
    at line 271, signature: (tmp_path, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_finds_duplicate_payload_ref
  how: 'defines public function `test_verify_finds_duplicate_payload_ref` at line
    288, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_well_formed_chain_is_not_drift
  how: 'defines public function `test_verify_well_formed_chain_is_not_drift` at line
    307, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_same_version_collision_is_still_drift
  how: 'defines public function `test_verify_same_version_collision_is_still_drift`
    at line 324, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_supersedes_missing_id_is_still_drift
  how: 'defines public function `test_verify_supersedes_missing_id_is_still_drift`
    at line 337, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_version_gap_is_still_drift
  how: 'defines public function `test_verify_version_gap_is_still_drift` at line 350,
    signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_chain_writes_head_version
  how: 'defines public function `test_materialize_chain_writes_head_version` at line
    363, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_version_flag_selects_requested_version
  how: 'defines public function `test_materialize_version_flag_selects_requested_version`
    at line 376, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_version_flag_reports_missing_version
  how: 'defines public function `test_materialize_version_flag_reports_missing_version`
    at line 388, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_materialize_version_flag
  how: 'defines public function `test_cli_materialize_version_flag` at line 397, signature:
    (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_load_level3_nodes_coerces_non_integer_version
  how: 'defines public function `test_load_level3_nodes_coerces_non_integer_version`
    at line 408, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_finds_stale_contract_after_source_edit
  how: 'defines public function `test_verify_finds_stale_contract_after_source_edit`
    at line 426, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_ignores_model_authored_prose_drift
  how: 'defines public function `test_verify_ignores_model_authored_prose_drift` at
    line 446, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_unreadable_contract_reported_not_crashed
  how: 'defines public function `test_verify_unreadable_contract_reported_not_crashed`
    at line 461, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_build_version_node_missing_contract_is_not_drift
  how: 'defines public function `test_verify_build_version_node_missing_contract_is_not_drift`
    at line 492, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_build_version_node_malformed_contract_is_still_drift
  how: 'defines public function `test_verify_build_version_node_malformed_contract_is_still_drift`
    at line 515, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_reads_contract_with_embedded_backtick_fence
  how: 'defines public function `test_verify_reads_contract_with_embedded_backtick_fence`
    at line 535, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_diff_contract_ignores_prose_fields_directly
  how: defines public function `test_diff_contract_ignores_prose_fields_directly`
    at line 569
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_diff_contract_reports_added_and_removed
  how: defines public function `test_diff_contract_reports_added_and_removed` at line
    579
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_engine_root_missing_degrades
  how: 'defines public function `test_verify_engine_root_missing_degrades` at line
    593, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_project_with_no_level3_dir_degrades
  how: 'defines public function `test_verify_project_with_no_level3_dir_degrades`
    at line 605, signature: (tmp_path, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_load_level3_nodes_skips_wrong_type_and_malformed
  how: 'defines public function `test_load_level3_nodes_skips_wrong_type_and_malformed`
    at line 617, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_verify_exit_0_by_default_even_with_drift
  how: 'defines public function `test_cli_verify_exit_0_by_default_even_with_drift`
    at line 632, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_verify_strict_exit_1_with_drift
  how: 'defines public function `test_cli_verify_strict_exit_1_with_drift` at line
    641, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_verify_strict_exit_0_when_clean
  how: 'defines public function `test_cli_verify_strict_exit_0_when_clean` at line
    649, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_materialize_requires_out
  how: 'defines public function `test_cli_materialize_requires_out` at line 656, signature:
    (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_materialize_end_to_end
  how: 'defines public function `test_cli_materialize_end_to_end` at line 662, signature:
    (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_materialize_refuses_engine_root_as_out
  how: 'defines public function `test_cli_materialize_refuses_engine_root_as_out`
    at line 672, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out / 'stray.txt'
  how: '`(out / ''stray.txt'').write_text(''pre-existing'')` at line 159'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out / 'stray.txt'
  how: '`(out / ''stray.txt'').write_text(''pre-existing'')` at line 171'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text(text, encoding=''utf-8'')` at line 415'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: bar
  how: '`bar.write_text(''import sys\nimport json\n\n\ndef bar():\n    pass\n'', encoding=''utf-8'')`
    at line 435'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text(text, encoding=''utf-8'')` at line 455'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text(text, encoding=''utf-8'')` at line 468'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text(text, encoding=''utf-8'')` at line 502'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text(text, encoding=''utf-8'')` at line 525'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.write_text(''def f(rec):\n    ctx.write_text(f"""## Header\\n\\n```json\\n{rec}\\n```\\n\\nmore
    text '' + ''x'' * 200 + ''""")\n'', encoding=''utf-8'')` at line 545'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'nodes' / 'level3' / 'not-level3.md'
  how: '`(project / ''nodes'' / ''level3'' / ''not-level3.md'').write_text(''---\nid:
    idea:stray\ntype: idea\n---\nbody\n'', encoding=''utf-8'')` at line 619'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'nodes' / 'level3' / 'garbage.md'
  how: '`(project / ''nodes'' / ''level3'' / ''garbage.md'').write_text(''not frontmatter
    at all\n'', encoding=''utf-8'')` at line 621'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(content, encoding=''utf-8'')` at line 49'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(content, encoding=''utf-8'')` at line 276'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
