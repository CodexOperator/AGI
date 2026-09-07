---
id: build:tests-graph-core-test-frontmatter-errors
mint_id: b09f0a63d98b47dba2fa9d7fe15903b2
type: build
parents:
  - idea:engine-tests-graph-core
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/graph_core/test_frontmatter_errors.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/graph_core/test_frontmatter_errors.py"
---
`extensions/agi/tests/graph_core/test_frontmatter_errors.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests-graph-core`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/graph_core/test_frontmatter_errors.py
parse_ok: true
inputs:
- name: pathlib.Path
  how: '`from pathlib import Path` at line 3'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.persistence.load_node_dir
  how: '`from graph_core.persistence import load_node_dir` at line 5'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.persistence.FrontmatterError
  how: '`from graph_core.persistence import FrontmatterError` at line 5'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _json
  how: '`import json as _json` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pytest
  how: '`import pytest as _pytest` at line 76'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _yaml
  how: '`import yaml as _yaml` at line 77'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.persistence.frontmatter.FrontmatterError
  how: '`from graph_core.persistence.frontmatter import FrontmatterError` at line
    79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.persistence.frontmatter.load_node_file
  how: '`from graph_core.persistence.frontmatter import load_node_file` at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: test_dir_load_isolates_bad_file
  how: 'defines public function `test_dir_load_isolates_bad_file` at line 8, signature:
    (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dir_load_skips_non_node_files
  how: 'defines public function `test_dir_load_skips_non_node_files` at line 22, signature:
    (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dir_load_mixed_md_and_json
  how: 'defines public function `test_dir_load_mixed_md_and_json` at line 32, signature:
    (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dir_load_not_a_directory
  how: 'defines public function `test_dir_load_not_a_directory` at line 41, signature:
    (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dir_load_continues_after_multiple_errors
  how: 'defines public function `test_dir_load_continues_after_multiple_errors` at
    line 51, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_malformed_yaml_raises_frontmatter_error_not_a_yaml_error
  how: 'defines public function `test_malformed_yaml_raises_frontmatter_error_not_a_yaml_error`
    at line 90, signature: (tmp_path, bad_yaml)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_malformed_json_raises_frontmatter_error_not_a_decode_error
  how: 'defines public function `test_malformed_json_raises_frontmatter_error_not_a_decode_error`
    at line 97, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_underlying_cause_is_preserved_for_debugging
  how: 'defines public function `test_the_underlying_cause_is_preserved_for_debugging`
    at line 104, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_every_malformed_shape_fails_in_exactly_one_class
  how: 'defines public function `test_every_malformed_shape_fails_in_exactly_one_class`
    at line 120, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: good
  how: '`good.write_text("---\nid: hyp:ok\ntype: hypothesis\n---\n\nbody\n")` at line
    11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: bad
  how: '`bad.write_text("---\nid: hyp:bad\n")` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "node.md"
  how: '`(tmp_path / "node.md").write_text("---\nid: a\n---\nb\n")` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "README.txt"
  how: '`(tmp_path / "README.txt").write_text("not a node")` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "data.csv"
  how: '`(tmp_path / "data.csv").write_text("a,b\n1,2\n")` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "a.md"
  how: '`(tmp_path / "a.md").write_text("---\nid: a\n---\nbody-a\n")` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "b.json"
  how: '`(tmp_path / "b.json").write_text(''{"frontmatter": {"id": "b"}, "body": "body-b"}\n'')`
    at line 35'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.write_text("---\nid: x\n---\n")` at line 44'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "good1.md"
  how: '`(tmp_path / "good1.md").write_text("---\nid: a\n---\n")` at line 53'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "good2.md"
  how: '`(tmp_path / "good2.md").write_text("---\nid: b\n---\n")` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "bad1.md"
  how: '`(tmp_path / "bad1.md").write_text("no frontmatter at all")` at line 55'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "bad2.json"
  how: '`(tmp_path / "bad2.json").write_text("{not json")` at line 56'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(bad_yaml)` at line 92'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("{not json")` at line 99'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("---\nid: [unclosed\n---\nbody\n")` at line 108'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: j
  how: '`j.write_text("{not json")` at line 114'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(text)` at line 134'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.