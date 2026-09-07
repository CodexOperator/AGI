---
id: build:tests-test-decompose-engine
mint_id: ff155db7153446ddb9ce3c9e8d0941bc
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_decompose_engine.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_decompose_engine.py"
---
`extensions/agi/tests/test_decompose_engine.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_decompose_engine.py
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
- name: nodes["idea:engine-graph-core"][0]
  how: '`nodes["idea:engine-graph-core"][0].read_text()` at line 189'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nodes["idea:engine-driver-sh"][0]
  how: '`nodes["idea:engine-driver-sh"][0].read_text()` at line 191'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nodes["idea:engine-agi-bridge-index"][0]
  how: '`nodes["idea:engine-agi-bridge-index"][0].read_text()` at line 193'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: idea_nodes(project)["idea:engine-nodoc"][0]
  how: '`idea_nodes(project)["idea:engine-nodoc"][0].read_text()` at line 199'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding="utf-8")` at line 310'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])` at line
    94'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 287'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 290'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 94'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: write_engine_tree
  how: 'defines public function `write_engine_tree` at line 58, signature: (root:
    Path, files: dict[str, str] | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine
  how: 'defines public function `engine` at line 72, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 77, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run
  how: 'defines public function `run` at line 83, signature: (project: Path, engine:
    Path | None, *args, goal_map: Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fm_of
  how: 'defines public function `fm_of` at line 93, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: idea_nodes
  how: 'defines public function `idea_nodes` at line 97, signature: (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_node
  how: 'defines public function `write_node` at line 102, signature: (project: Path,
    rel: str, fm: dict, body: str=''body'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_default_engine_root_points_at_this_repo
  how: defines public function `test_default_engine_root_points_at_this_repo` at line
    112
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_discovers_expected_units_with_kinds_and_scale
  how: 'defines public function `test_discovers_expected_units_with_kinds_and_scale`
    at line 121, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_co_location_alone_still_never_mints_a_unit
  how: 'defines public function `test_co_location_alone_still_never_mints_a_unit`
    at line 151, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_stray_src_init_is_not_its_own_package
  how: 'defines public function `test_stray_src_init_is_not_its_own_package` at line
    176, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_docstring_extracted_for_py_sh_ts
  how: 'defines public function `test_docstring_extracted_for_py_sh_ts` at line 186,
    signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_docstring_says_so_plainly_not_invented
  how: 'defines public function `test_missing_docstring_says_so_plainly_not_invented`
    at line 197, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_engine_root_is_noop
  how: 'defines public function `test_missing_engine_root_is_noop` at line 206, signature:
    (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_git_engine_root_is_noop
  how: 'defines public function `test_non_git_engine_root_is_noop` at line 214, signature:
    (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_engine_root_prunes_nothing
  how: 'defines public function `test_missing_engine_root_prunes_nothing` at line
    223, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_writes_nothing
  how: 'defines public function `test_dry_run_writes_nothing` at line 237, signature:
    (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unit_with_no_goal_map_entry_is_parentless_and_flagged
  how: 'defines public function `test_unit_with_no_goal_map_entry_is_parentless_and_flagged`
    at line 247, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_declared_goal_map_sets_parents
  how: 'defines public function `test_declared_goal_map_sets_parents` at line 266,
    signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_idempotent_byte_identical
  how: 'defines public function `test_idempotent_byte_identical` at line 285, signature:
    (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_twice_round_trip_preserves_foreign_field
  how: 'defines public function `test_write_twice_round_trip_preserves_foreign_field`
    at line 299, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prune_removes_stale_engine_decomp_but_spares_others
  how: 'defines public function `test_prune_removes_stale_engine_decomp_but_spares_others`
    at line 330, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_stale_flag_for_domain_node_with_no_matching_unit
  how: 'defines public function `test_stale_flag_for_domain_node_with_no_matching_unit`
    at line 358, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_stale_flag_when_domain_node_matches_a_live_unit
  how: 'defines public function `test_no_stale_flag_when_domain_node_matches_a_live_unit`
    at line 371, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_project_local_script_lookup_argument_exists
  how: defines public function `test_no_project_local_script_lookup_argument_exists`
    at line 384
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stray
  how: '`stray.write_text("# a data file nobody declared\n", encoding="utf-8")` at
    line 165'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: gm
  how: '`gm.write_text(''{"mappings": {}}'', encoding="utf-8")` at line 258'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: gm
  how: '`gm.write_text( ''{"mappings": {"extensions/agi/src/graph_core": "goal:g6.1"}}'',
    encoding="utf-8", )` at line 268'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text( f"---{head}next_edges:\n  - hyp:graph-core-r1\n" f"embedding_coords:
    [0.1, 0.2]\n---{body}", encoding="utf-8", )` at line 312'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(content, encoding="utf-8")` at line 65'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.