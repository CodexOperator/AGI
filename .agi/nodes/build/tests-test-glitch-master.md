---
build_kind: code
confidence: 1.0
id: "build:tests-test-glitch-master"
mint_id: 8439e37ed3f6470cae6f5032b8452195
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_glitch_master.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_glitch_master.py"
type: build
---

`extensions/agi/tests/test_glitch_master.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_glitch_master.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: contextlib
  how: '`import contextlib` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: io
  how: '`import io` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: glitch_master
  how: '`import glitch_master` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: results
  how: '`results.read_text()` at line 78'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(results.read_text())` at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(results.read_text())` at line 142'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: results
  how: '`results.read_text()` at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(results.read_text())` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: results
  how: '`results.read_text()` at line 142'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: results
  how: '`results.read_text()` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdin
  how: reads `sys.stdin` / calls `input()`
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _fixture
  how: 'defines private function `_fixture` at line 25, signature: (iter_id=''L3.99'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _stdin
  how: 'defines private function `_stdin` at line 60, signature: (data)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_format_record_writes_results_json_verbatim
  how: 'defines public function `test_format_record_writes_results_json_verbatim`
    at line 70, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_format_record_prints_one_review_line_per_target
  how: 'defines public function `test_format_record_prints_one_review_line_per_target`
    at line 82, signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_format_record_prints_one_global_line
  how: 'defines public function `test_format_record_prints_one_global_line` at line
    97, signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_format_record_guard_warn_when_guard_output_nonempty
  how: 'defines public function `test_format_record_guard_warn_when_guard_output_nonempty`
    at line 109, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_format_record_guard_warn_says_warn_n
  how: 'defines public function `test_format_record_guard_warn_says_warn_n` at line
    120, signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_format_record_reads_stdin_and_cli_writes_file
  how: 'defines public function `test_format_record_reads_stdin_and_cli_writes_file`
    at line 131, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ns
  how: 'defines private function `_ns` at line 145, signature: (**kw)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(data)` at line 63'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(data)` at line 78'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(data)` at line 136'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
