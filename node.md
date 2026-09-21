---
build_kind: code
confidence: 1.0
id: "build:tests-test-links"
mint_id: 1bcc9a08e19b4eb58a24b9cc36efefd0
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_links.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_links.py"
type: build
---

`extensions/agi/tests/test_links.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_links.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_writer
  how: '`import node_writer` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: links
  how: '`import links` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: res.path
  how: '`res.path.read_text()` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: res.path
  how: '`res.path.read_text()` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: res.path
  how: '`res.path.read_text()` at line 106'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 128'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "links.py"
  how: '`(BIN / "links.py").read_text()` at line 262'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes/hypothesis/h1.md"
  how: '`(project / "nodes/hypothesis/h1.md").read_text()` at line 352'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes/hypothesis/h1.md"
  how: '`(project / "nodes/hypothesis/h1.md").read_text()` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 133'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes/hypothesis/h1.md"
  how: '`(project / "nodes/hypothesis/h1.md").read_text()` at line 248'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 398'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 152'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: project
  how: 'defines public function `project` at line 39, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node
  how: 'defines private function `_node` at line 47, signature: (project: Path, node_id:
    str, fm_lines: list[str], body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_update_cannot_destroy_the_authored_thought_region
  how: 'defines public function `test_an_update_cannot_destroy_the_authored_thought_region`
    at line 59, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_new_body_that_brings_its_own_thought_keeps_it
  how: 'defines public function `test_a_new_body_that_brings_its_own_thought_keeps_it`
    at line 81, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_frontmatter_is_merged_not_replaced
  how: 'defines public function `test_frontmatter_is_merged_not_replaced` at line
    97, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unset_drops_a_key
  how: 'defines public function `test_unset_drops_a_key` at line 111, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_update_that_changes_nothing_writes_nothing
  how: 'defines public function `test_an_update_that_changes_nothing_writes_nothing`
    at line 120, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_missing_node_is_rejected_not_created
  how: 'defines public function `test_a_missing_node_is_rejected_not_created` at line
    137, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_unparseable_node_is_rejected_rather_than_rewritten
  how: 'defines public function `test_an_unparseable_node_is_rejected_rather_than_rewritten`
    at line 145, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_absent_link_defaults_to_self_but_says_it_defaulted
  how: defines public function `test_absent_link_defaults_to_self_but_says_it_defaulted`
    at line 159
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_payload_ref_is_read_as_the_predecessor_it_is
  how: defines public function `test_payload_ref_is_read_as_the_predecessor_it_is`
    at line 165
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_link_ref_wins_over_payload_ref
  how: defines public function `test_link_ref_wins_over_payload_ref` at line 172
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_self_resolves_to_the_nodes_own_body_without_branching_on_type
  how: 'defines public function `test_self_resolves_to_the_nodes_own_body_without_branching_on_type`
    at line 177, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_single_read_of_a_missing_link_raises
  how: 'defines public function `test_a_single_read_of_a_missing_link_raises` at line
    188, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_bulk_scan_of_a_missing_link_returns_a_sentinel_and_keeps_going
  how: 'defines public function `test_a_bulk_scan_of_a_missing_link_returns_a_sentinel_and_keeps_going`
    at line 198, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_sentinel_is_falsey_and_is_not_a_string
  how: 'defines public function `test_the_sentinel_is_falsey_and_is_not_a_string`
    at line 215, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_set_link_goes_through_the_gated_writer
  how: 'defines public function `test_set_link_goes_through_the_gated_writer` at line
    227, signature: (project, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_resolver_has_no_type_branch_in_its_executable_lines
  how: defines public function `test_the_resolver_has_no_type_branch_in_its_executable_lines`
    at line 251
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_update_is_judged_on_the_delta_not_the_state
  how: 'defines public function `test_an_update_is_judged_on_the_delta_not_the_state`
    at line 287, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _post_wire
  how: defines private function `_post_wire` at line 321
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_computes_its_delta_by_diffing_not_by_listing
  how: 'defines public function `test_post_wire_computes_its_delta_by_diffing_not_by_listing`
    at line 329, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_writes_nothing_when_nothing_changed
  how: 'defines public function `test_post_wire_writes_nothing_when_nothing_changed`
    at line 357, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_refused_gated_write_still_records_the_wire
  how: 'defines public function `test_a_refused_gated_write_still_records_the_wire`
    at line 373, signature: (project, capsys, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "config.json"
  how: '`(graph / "config.json").write_text("{}")` at line 43'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text("---\n" + "\n".join(fm_lines) + "\n---\n\n" + body)` at line
    51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text("---\nid: [unclosed\n---\nbody\n")` at line 148'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / ".agi" / "config.json"
  how: '`(tmp_path / ".agi" / "config.json").write_text("{}")` at line 191'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / ".agi" / "config.json"
  how: '`(tmp_path / ".agi" / "config.json").write_text("{}")` at line 201'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "schemas" / "[hypothesis].md"
  how: '`(project / "context" / "schemas" / "[hypothesis].md").write_text( "---\nname:
    hypothesis\nvalidation:\n  required: [id, type, mint_id, " "title, testable_claim]\nspawn:\n  allowed_parents:
    [goal]\n" "  min_parents: 1\n  max_parents: 2\n---\...[truncated, 251 chars total]`
    at line 302'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
