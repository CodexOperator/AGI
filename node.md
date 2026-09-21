---
id: build:tests-test-envfile
mint_id: a5ad06ab8cfe44b0a1eb5bc812de89cc
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_envfile.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_envfile.py"
---
`extensions/agi/tests/test_envfile.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_envfile.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: textwrap
  how: '`import textwrap` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: agi_secrets
  how: '`import envfile as agi_secrets` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: make_project
  how: 'defines public function `make_project` at line 28, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_node
  how: 'defines public function `write_node` at line 36, signature: (graph: Path,
    body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_env
  how: 'defines public function `write_env` at line 66, signature: (repo: Path, text:
    str, mode: int=384)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_resolves_paths_from_the_node
  how: 'defines public function `test_resolves_paths_from_the_node` at line 76, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_source_root_placeholder_is_the_repo_not_the_graph_dir
  how: 'defines public function `test_source_root_placeholder_is_the_repo_not_the_graph_dir`
    at line 85, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_falls_back_when_no_node_and_says_so
  how: 'defines public function `test_falls_back_when_no_node_and_says_so` at line
    98, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unresolvable_placeholder_raises
  how: 'defines public function `test_unresolvable_placeholder_raises` at line 108,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_project_raises
  how: 'defines public function `test_no_project_raises` at line 115, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_can_extend_the_forbidden_floor
  how: 'defines public function `test_node_can_extend_the_forbidden_floor` at line
    123, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_cannot_lower_the_forbidden_floor
  how: 'defines public function `test_node_cannot_lower_the_forbidden_floor` at line
    130, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_forbidden_key_present_is_a_problem
  how: 'defines public function `test_forbidden_key_present_is_a_problem` at line
    146, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_env_file_names_the_required_keys
  how: 'defines public function `test_missing_env_file_names_the_required_keys` at
    line 161, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_empty_required_key_is_a_problem
  how: 'defines public function `test_empty_required_key_is_a_problem` at line 170,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_satisfied_env_file_has_no_problems
  how: 'defines public function `test_satisfied_env_file_has_no_problems` at line
    179, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_loose_mode_is_a_note_not_a_problem
  how: 'defines public function `test_loose_mode_is_a_note_not_a_problem` at line
    189, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_env_line_shapes
  how: 'defines public function `test_read_env_line_shapes` at line 212, signature:
    (tmp_path, line, key, value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_env_skips_comments_and_blanks
  how: 'defines public function `test_read_env_skips_comments_and_blanks` at line
    217, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_env_missing_file_is_empty_not_an_error
  how: 'defines public function `test_read_env_missing_file_is_empty_not_an_error`
    at line 227, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_what_env_file
  how: 'defines public function `test_cli_what_env_file` at line 234, signature: (tmp_path,
    capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_check_exits_nonzero_on_a_problem
  how: 'defines public function `test_cli_check_exits_nonzero_on_a_problem` at line
    242, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_without_check_reports_but_exits_zero
  how: 'defines public function `test_cli_without_check_reports_but_exits_zero` at
    line 248, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_never_prints_a_value
  how: 'defines public function `test_cli_never_prints_a_value` at line 257, signature:
    (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "config.json"
  how: '`(graph / "config.json").write_text(json.dumps({"metric_primary": "outcome_coverage"}))`
    at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text(textwrap.dedent(body).lstrip())` at line 38'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text(textwrap.dedent(text).lstrip())` at line 68'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"metric_primary": "outcome_coverage"})` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.