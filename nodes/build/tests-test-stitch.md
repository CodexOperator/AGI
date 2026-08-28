---
build_kind: code
confidence: 1.0
id: "build:tests-test-stitch"
mint_id: a7fb261841994fcbb57d2c2770d09211
origin: build-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_stitch.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_stitch.py"
type: build
---

`extensions/agi/tests/test_stitch.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
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
  how: '`node_path.read_text(encoding=''utf-8'')` at line 461'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 502'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 515'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 549'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 568'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 605'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / rel
  how: '`(engine / rel).read_bytes()` at line 781'
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
  how: '`(out / rel).read_bytes()` at line 787'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / rel
  how: '`(engine / rel).read_text()` at line 853'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / rel
  how: '`(engine / rel).read_text()` at line 856'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tip / rel
  how: '`(tip / rel).read_text()` at line 882'
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
- name: a / rel
  how: '`(a / rel).read_bytes()` at line 758'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: b / rel
  how: '`(b / rel).read_bytes()` at line 758'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out / rel
  how: '`(out / rel).read_text()` at line 878'
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
- name: test_verify_from_grid_does_not_call_an_unpublished_new_file_missing
  how: 'defines public function `test_verify_from_grid_does_not_call_an_unpublished_new_file_missing`
    at line 241, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_from_grid_still_reports_a_payload_neither_source_has
  how: 'defines public function `test_verify_from_grid_still_reports_a_payload_neither_source_has`
    at line 273, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_has_drift_false_when_all_categories_empty
  how: defines public function `test_has_drift_false_when_all_categories_empty` at
    line 290
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_clean_tree_has_no_drift
  how: 'defines public function `test_verify_clean_tree_has_no_drift` at line 296,
    signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_finds_orphan_file
  how: 'defines public function `test_verify_finds_orphan_file` at line 311, signature:
    (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_orphan_scan_skips_when_engine_not_git_repo
  how: 'defines public function `test_verify_orphan_scan_skips_when_engine_not_git_repo`
    at line 320, signature: (tmp_path, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_finds_duplicate_payload_ref
  how: 'defines public function `test_verify_finds_duplicate_payload_ref` at line
    337, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_well_formed_chain_is_not_drift
  how: 'defines public function `test_verify_well_formed_chain_is_not_drift` at line
    356, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_same_version_collision_is_still_drift
  how: 'defines public function `test_verify_same_version_collision_is_still_drift`
    at line 373, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_supersedes_missing_id_is_still_drift
  how: 'defines public function `test_verify_supersedes_missing_id_is_still_drift`
    at line 386, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_version_gap_is_still_drift
  how: 'defines public function `test_verify_version_gap_is_still_drift` at line 399,
    signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_chain_writes_head_version
  how: 'defines public function `test_materialize_chain_writes_head_version` at line
    412, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_version_flag_selects_requested_version
  how: 'defines public function `test_materialize_version_flag_selects_requested_version`
    at line 425, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_materialize_version_flag_reports_missing_version
  how: 'defines public function `test_materialize_version_flag_reports_missing_version`
    at line 437, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_materialize_version_flag
  how: 'defines public function `test_cli_materialize_version_flag` at line 446, signature:
    (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_load_level3_nodes_coerces_non_integer_version
  how: 'defines public function `test_load_level3_nodes_coerces_non_integer_version`
    at line 457, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_finds_stale_contract_after_source_edit
  how: 'defines public function `test_verify_finds_stale_contract_after_source_edit`
    at line 475, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_ignores_model_authored_prose_drift
  how: 'defines public function `test_verify_ignores_model_authored_prose_drift` at
    line 495, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_unreadable_contract_reported_not_crashed
  how: 'defines public function `test_verify_unreadable_contract_reported_not_crashed`
    at line 510, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_build_version_node_missing_contract_is_not_drift
  how: 'defines public function `test_verify_build_version_node_missing_contract_is_not_drift`
    at line 541, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_build_version_node_malformed_contract_is_still_drift
  how: 'defines public function `test_verify_build_version_node_malformed_contract_is_still_drift`
    at line 564, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_reads_contract_with_embedded_backtick_fence
  how: 'defines public function `test_verify_reads_contract_with_embedded_backtick_fence`
    at line 584, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_diff_contract_ignores_prose_fields_directly
  how: defines public function `test_diff_contract_ignores_prose_fields_directly`
    at line 618
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_diff_contract_reports_added_and_removed
  how: defines public function `test_diff_contract_reports_added_and_removed` at line
    628
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_engine_root_missing_degrades
  how: 'defines public function `test_verify_engine_root_missing_degrades` at line
    642, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verify_project_with_no_level3_dir_degrades
  how: 'defines public function `test_verify_project_with_no_level3_dir_degrades`
    at line 654, signature: (tmp_path, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_load_level3_nodes_skips_wrong_type_and_malformed
  how: 'defines public function `test_load_level3_nodes_skips_wrong_type_and_malformed`
    at line 666, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_verify_exit_0_by_default_even_with_drift
  how: 'defines public function `test_cli_verify_exit_0_by_default_even_with_drift`
    at line 681, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_verify_strict_exit_1_with_drift
  how: 'defines public function `test_cli_verify_strict_exit_1_with_drift` at line
    690, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_verify_strict_exit_0_when_clean
  how: 'defines public function `test_cli_verify_strict_exit_0_when_clean` at line
    698, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_materialize_requires_out
  how: 'defines public function `test_cli_materialize_requires_out` at line 705, signature:
    (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_materialize_end_to_end
  how: 'defines public function `test_cli_materialize_end_to_end` at line 711, signature:
    (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_materialize_refuses_engine_root_as_out
  how: 'defines public function `test_cli_materialize_refuses_engine_root_as_out`
    at line 721, signature: (tmp_path, engine, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _grid_project
  how: 'defines private function `_grid_project` at line 735, signature: (project:
    Path, engine: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_from_grid_matches_the_engine_tree_byte_for_byte
  how: 'defines public function `test_from_grid_matches_the_engine_tree_byte_for_byte`
    at line 744, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_from_grid_preserves_the_exec_bit
  how: 'defines public function `test_from_grid_preserves_the_exec_bit` at line 761,
    signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_from_grid_reads_the_graph_not_the_engine
  how: 'defines public function `test_from_grid_reads_the_graph_not_the_engine` at
    line 775, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_from_grid_reports_a_node_with_no_grid_history
  how: 'defines public function `test_from_grid_reports_a_node_with_no_grid_history`
    at line 790, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_publish_refuses_without_from_grid
  how: 'defines public function `test_publish_refuses_without_from_grid` at line 803,
    signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_plain_out_still_refuses_the_engine_repo
  how: 'defines public function `test_plain_out_still_refuses_the_engine_repo` at
    line 808, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_out_never_writes_into_the_graph_repo_even_with_publish
  how: 'defines public function `test_out_never_writes_into_the_graph_repo_even_with_publish`
    at line 813, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_publish_refuses_a_dirty_engine_tree
  how: 'defines public function `test_publish_refuses_a_dirty_engine_tree` at line
    818, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_publish_refuses_a_non_git_target
  how: 'defines public function `test_publish_refuses_a_non_git_target` at line 829,
    signature: (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_publish_writes_the_graphs_bytes_into_the_engine
  how: 'defines public function `test_publish_writes_the_graphs_bytes_into_the_engine`
    at line 836, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_grid_version_materializes_a_chosen_version_not_the_tip
  how: 'defines public function `test_grid_version_materializes_a_chosen_version_not_the_tip`
    at line 859, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_grid_version_beyond_history_is_reported_not_silently_the_tip
  how: 'defines public function `test_grid_version_beyond_history_is_reported_not_silently_the_tip`
    at line 885, signature: (project, engine, tmp_path)'
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
- name: engine / rel
  how: '`(engine / rel).write_text(''import os\n\n\ndef brand_new():\n    pass\n'')`
    at line 253'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / ghost
  how: '`(engine / ghost).write_text(''# transient\n'')` at line 281'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text(text, encoding=''utf-8'')` at line 464'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: bar
  how: '`bar.write_text(''import sys\nimport json\n\n\ndef bar():\n    pass\n'', encoding=''utf-8'')`
    at line 484'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text(text, encoding=''utf-8'')` at line 504'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text(text, encoding=''utf-8'')` at line 517'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text(text, encoding=''utf-8'')` at line 551'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text(text, encoding=''utf-8'')` at line 574'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.write_text(''def f(rec):\n    ctx.write_text(f"""## Header\\n\\n```json\\n{rec}\\n```\\n\\nmore
    text '' + ''x'' * 200 + ''""")\n'', encoding=''utf-8'')` at line 594'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'nodes' / 'build' / 'not-level3.md'
  how: '`(project / ''nodes'' / ''build'' / ''not-level3.md'').write_text(''---\nid:
    idea:stray\ntype: idea\n---\nbody\n'', encoding=''utf-8'')` at line 668'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'nodes' / 'build' / 'garbage.md'
  how: '`(project / ''nodes'' / ''build'' / ''garbage.md'').write_text(''not frontmatter
    at all\n'', encoding=''utf-8'')` at line 670'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'agi-tree.config.json'
  how: '`(project / ''agi-tree.config.json'').write_text(''{}'')` at line 739'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / rel
  how: '`(engine / rel).write_text(''#!/bin/sh\necho hi\n'')` at line 765'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'agi-tree.config.json'
  how: '`(project / ''agi-tree.config.json'').write_text(''{}'')` at line 796'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine / 'extensions/agi/bin/foo.py'
  how: '`(engine / ''extensions/agi/bin/foo.py'').write_text(''import os\n# edited\n'')`
    at line 824'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: staged
  how: '`staged.write_text(edited)` at line 849'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(content, encoding=''utf-8'')` at line 49'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(content, encoding=''utf-8'')` at line 325'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: staged
  how: '`staged.write_text(text)` at line 872'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
