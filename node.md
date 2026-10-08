---
build_kind: code
confidence: 1.0
id: "build:tests-test-hierarchy"
mint_id: d2bfd2b735c8455f93b800968f4f6e99
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_hierarchy.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_hierarchy.py"
type: build
---

`extensions/agi/tests/test_hierarchy.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_hierarchy.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "nodes" / ".geometry" / "seats.md"
  how: '`(tmp_path / "nodes" / ".geometry" / "seats.md").read_text()` at line 130'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "nodes" / ".geometry" / "seats.md"
  how: '`(tmp_path / "nodes" / ".geometry" / "seats.md").read_text()` at line 156'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "nodes" / ".geometry" / "seats.md"
  how: '`(tmp_path / "nodes" / ".geometry" / "seats.md").read_text()` at line 178'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _write
  how: 'defines private function `_write` at line 60, signature: (root: Path, rel:
    str, text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _clean_seed
  how: 'defines private function `_clean_seed` at line 66, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _maybe_mkdir_config
  how: 'defines private function `_maybe_mkdir_config` at line 73, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _check
  how: 'defines private function `_check` at line 78, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pin
  how: 'defines private function `_pin` at line 85, signature: (root: Path, name:
    str, transcript: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_orphan_pin_nonzero
  how: 'defines public function `test_orphan_pin_nonzero` at line 94, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_orphan_pin_ignores_agent_ids
  how: 'defines public function `test_orphan_pin_ignores_agent_ids` at line 103, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_duplicate_transcript_nonzero
  how: 'defines public function `test_duplicate_transcript_nonzero` at line 114, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotated_by_nonzero
  how: 'defines public function `test_rotated_by_nonzero` at line 128, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotated_by_roleclass_allowed
  how: 'defines public function `test_rotated_by_roleclass_allowed` at line 140, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_director_kids_over_cap_nonzero
  how: 'defines public function `test_director_kids_over_cap_nonzero` at line 150,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unresolved_nonzero
  how: 'defines public function `test_unresolved_nonzero` at line 172, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_body_table_nonzero
  how: 'defines public function `test_body_table_nonzero` at line 191, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_clean_seed_zero
  how: 'defines public function `test_clean_seed_zero` at line 207, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(text, encoding="utf-8")` at line 63'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "sessions" / f"{name}.meter"
  how: '`(root / "sessions" / f"{name}.meter").write_text(transcript, encoding="utf-8")`
    at line 87'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tx
  how: '`tx.write_text("", encoding="utf-8")` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"name": "dir-x", "role": "director", "tier": 1, "model": "claude-sonnet-5",
    "effort": "max", "session_kind": "tty", "rotated_by": "sanctuary-master", "owning_goal":
    "goal:g99"})` at line 157'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"name": "mystery", "role": "wizard", "tier": 2, "harness": "claude-code",
    "model": "", "effort": "", "session_kind": "tty", "rotated_by": "quorum", "owning_goal":
    ""})` at line 174'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(r, sort_keys=True)` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(r, sort_keys=True)` at line 56'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
