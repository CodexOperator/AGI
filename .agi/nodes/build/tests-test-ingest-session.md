---
id: build:tests-test-ingest-session
mint_id: fcd809931ac9420cb1516eaff672db20
type: build
parents:
  - mvp:tests
build_kind: code
confidence: 1.0
edited_by: a00-4c9e6d97
origin: build-scan
payload_ref: extensions/agi/tests/test_ingest_session.py
tags:
  - build
  - code
  - g2.1
thought_session: iter-DT.90
title: "Build: extensions/agi/tests/test_ingest_session.py"
---
`extensions/agi/tests/test_ingest_session.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_ingest_session.py
parse_ok: true
inputs:
- name: json
  how: '`import json` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shutil
  how: '`import shutil` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: files[0]
  how: '`files[0].read_text(encoding="utf-8")` at line 60'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text(encoding="utf-8")` at line 112'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text(encoding="utf-8")` at line 132'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node
  how: '`node.read_text(encoding="utf-8")` at line 69'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: files[0]
  how: '`files[0].read_text(encoding="utf-8")` at line 76'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _fixture
  how: 'defines private function `_fixture` at line 27, signature: (path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph
  how: 'defines public function `graph` at line 39, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run
  how: 'defines public function `run` at line 46, signature: (session, root, *extra)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_fresh_ingest_mints_one_node_under_nodes
  how: 'defines public function `test_fresh_ingest_mints_one_node_under_nodes` at
    line 52, signature: (graph, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_reingest_is_idempotent
  how: 'defines public function `test_reingest_is_idempotent` at line 65, signature:
    (graph, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_malformed_input_is_refused_by_name
  how: 'defines public function `test_malformed_input_is_refused_by_name` at line
    80, signature: (graph, tmp_path, body)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _fixture_id
  how: 'defines private function `_fixture_id` at line 90, signature: (path, sid)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_distinct_ids_never_collapse_to_one_node
  how: 'defines public function `test_distinct_ids_never_collapse_to_one_node` at
    line 98, signature: (graph, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_reversible_suffix_separates_hash_colliding_pair
  how: 'defines public function `test_reversible_suffix_separates_hash_colliding_pair`
    at line 118, signature: (graph, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_overlong_id_is_refused_by_name_not_truncated
  how: 'defines public function `test_overlong_id_is_refused_by_name_not_truncated`
    at line 138, signature: (graph, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_slug_length_boundary_is_accept_at_limit_refuse_above
  how: 'defines public function `test_slug_length_boundary_is_accept_at_limit_refuse_above`
    at line 150, signature: (graph, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_dict_shape_is_refused_by_name_not_traceback
  how: 'defines public function `test_non_dict_shape_is_refused_by_name_not_traceback`
    at line 176, signature: (graph, tmp_path, body, reason)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_string_text_is_refused_by_name_not_traceback
  how: 'defines public function `test_non_string_text_is_refused_by_name_not_traceback`
    at line 192, signature: (graph, tmp_path, value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_valid_session_with_no_message_records_still_ingests
  how: 'defines public function `test_valid_session_with_no_message_records_still_ingests`
    at line 211, signature: (graph, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_canonical_uuid_keeps_bare_slug_and_case_is_idempotent
  how: 'defines public function `test_canonical_uuid_keeps_bare_slug_and_case_is_idempotent`
    at line 226, signature: (graph, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scope_check
  how: 'defines private function `_scope_check` at line 242, signature: (*own)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_residue_node_is_committable_exactly_when_owned
  how: defines public function `test_residue_node_is_committable_exactly_when_owned`
    at line 251
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")`
    at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: bad
  how: '`bad.write_text(body, encoding="utf-8")` at line 82'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")`
    at line 94'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: bad
  how: '`bad.write_text(body, encoding="utf-8")` at line 182'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: bad
  how: '`bad.write_text(body, encoding="utf-8")` at line 202'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: good
  how: '`good.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")`
    at line 219'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(value)` at line 199'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(r)` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(r)` at line 94'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(r)` at line 219'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
