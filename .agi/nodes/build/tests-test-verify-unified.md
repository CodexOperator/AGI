---
id: build:tests-test-verify-unified
mint_id: 02285dcb8ab04398a97b329f4b9502c6
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_verify_unified.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_verify_unified.py"
---
`extensions/agi/tests/test_verify_unified.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_verify_unified.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(capsys.readouterr().out)` at line 156'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.read_bytes()` at line 110'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.read_text()` at line 189'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _git
  how: 'defines private function `_git` at line 36, signature: (repo: Path, *args:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _init_repo
  how: 'defines private function `_init_repo` at line 43, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _commit_all
  how: 'defines private function `_commit_all` at line 50, signature: (repo: Path,
    message: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: make_before
  how: 'defines public function `make_before` at line 68, signature: (tmp_path: Path,
    name: str=''graph'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: make_after
  how: 'defines public function `make_after` at line 90, signature: (tmp_path: Path,
    before: Path, name: str=''unified'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: good_pair
  how: 'defines public function `good_pair` at line 126, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_good_pair_passes_every_check
  how: 'defines public function `test_good_pair_passes_every_check` at line 135, signature:
    (good_pair)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_good_pair_cli_exits_zero
  how: 'defines public function `test_good_pair_cli_exits_zero` at line 143, signature:
    (good_pair, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_good_pair_json_reports_ok_true
  how: 'defines public function `test_good_pair_json_reports_ok_true` at line 152,
    signature: (good_pair, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _result
  how: 'defines private function `_result` at line 165, signature: (results, name)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_deleted_node_fails_count_check
  how: 'defines public function `test_deleted_node_fails_count_check` at line 172,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_flipped_byte_fails_bytes_check_without_changing_count
  how: 'defines public function `test_flipped_byte_fails_bytes_check_without_changing_count`
    at line 185, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dropped_grid_ref_fails_as_missing
  how: 'defines public function `test_dropped_grid_ref_fails_as_missing` at line 199,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_diverged_grid_ref_fails_differently_than_missing
  how: 'defines public function `test_diverged_grid_ref_fails_differently_than_missing`
    at line 211, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unrelated_histories_fails_ancestry_check
  how: 'defines public function `test_unrelated_histories_fails_ancestry_check` at
    line 227, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goals_left_inside_dot_agi_fails
  how: 'defines public function `test_goals_left_inside_dot_agi_fails` at line 245,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unresolvable_payload_ref_fails
  how: 'defines public function `test_unresolvable_payload_ref_fails` at line 258,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_config_json_fails
  how: 'defines public function `test_missing_config_json_fails` at line 270, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_malformed_config_json_fails
  how: 'defines public function `test_malformed_config_json_fails` at line 279, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_resolver_disagrees_when_dot_agi_has_no_config
  how: 'defines public function `test_resolver_disagrees_when_dot_agi_has_no_config`
    at line 291, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_exits_nonzero_and_names_failing_checks
  how: 'defines public function `test_cli_exits_nonzero_and_names_failing_checks`
    at line 301, signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _snapshot
  how: 'defines private function `_snapshot` at line 316, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_checker_never_writes_to_either_repo
  how: 'defines public function `test_checker_never_writes_to_either_repo` at line
    324, signature: (good_pair)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_checker_never_writes_even_on_a_failing_run
  how: 'defines public function `test_checker_never_writes_even_on_a_failing_run`
    at line 336, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_after_with_no_dot_agi_reports_named_failures_not_a_crash
  how: 'defines public function `test_after_with_no_dot_agi_reports_named_failures_not_a_crash`
    at line 354, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_payload_ref_count_loss_is_not_a_vacuous_pass
  how: 'defines public function `test_payload_ref_count_loss_is_not_a_vacuous_pass`
    at line 375, signature: (good_pair)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_payload_ref_count_match_still_passes
  how: 'defines public function `test_payload_ref_count_match_still_passes` at line
    396, signature: (good_pair)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / "agi-tree.config.json"
  how: '`(repo / "agi-tree.config.json").write_text("{}")` at line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / "nodes" / "idea" / "a.md"
  how: '`(repo / "nodes" / "idea" / "a.md").write_text(NODE_A)` at line 78'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / "nodes" / "build" / "thing.md"
  how: '`(repo / "nodes" / "build" / "thing.md").write_text(NODE_BUILD)` at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / "nodes" / ".geometry" / "g.md"
  how: '`(repo / "nodes" / ".geometry" / "g.md").write_text(NODE_GEOM)` at line 80'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: agi / "config.json"
  how: '`(agi / "config.json").write_text("{}")` at line 111'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / "GOALS.md"
  how: '`(repo / "GOALS.md").write_text("# Goals\n")` at line 112'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: payload_dir / "thing.py"
  how: '`(payload_dir / "thing.py").write_bytes(PAYLOAD_BYTES)` at line 116'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.write_text(target.read_text().replace("first thought", "FIRST THOUGHT"))`
    at line 189'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: after / ".agi" / "config.json"
  how: '`(after / ".agi" / "config.json").write_text("{}")` at line 235'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: after / "GOALS.md"
  how: '`(after / "GOALS.md").write_text("# Goals\n")` at line 236'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: after / ".agi" / "GOALS.md"
  how: '`(after / ".agi" / "GOALS.md").write_text("# Goals\n")` at line 249'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: after / ".agi" / "config.json"
  how: '`(after / ".agi" / "config.json").write_text("{ this is not json")` at line
    282'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: after / "README.md"
  how: '`(after / "README.md").write_text("just a plain repo\n")` at line 358'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dst
  how: '`dst.write_bytes(src.read_bytes())` at line 110'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.