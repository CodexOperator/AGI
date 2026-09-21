---
build_kind: code
confidence: 1.0
id: "build:tests-test-write-guard"
mint_id: 1531ef12e86c44fd8b7f1785f897d425
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_write_guard.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_write_guard.py"
type: build
---

`extensions/agi/tests/test_write_guard.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_write_guard.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 9'
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
- name: node_file
  how: '`node_file.read_text()` at line 231'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(last_line)` at line 344'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: context_doc
  how: '`context_doc.read_text()` at line 535'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(node_file.read_text().split("---", 2)[1])` at line 634'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: schema
  how: '`schema.read_text()` at line 653'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(line)` at line 114'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 132'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(line)` at line 137'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 151'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(l)` at line 156'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 481'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: n_file
  how: '`n_file.read_text()` at line 507'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: context_doc
  how: '`context_doc.read_text()` at line 542'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 546'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(l)` at line 631'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`log_path.read_text()` at line 111'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 131'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 150'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`log_path.read_text()` at line 173'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(line)` at line 174'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`log_path.read_text()` at line 342'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 409'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: new
  how: '`new.read_text()` at line 455'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Path(res.path)
  how: '`Path(res.path).read_text()` at line 545'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: context_doc
  how: '`context_doc.read_text()` at line 560'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 614'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / ".agi" / "sessions" / "write-log.jsonl"
  how: '`(project / ".agi" / "sessions" / "write-log.jsonl").read_text()` at line
    630'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`log_path.read_text()` at line 136'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 634'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`log_path.read_text()` at line 156'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`log_path.read_text()` at line 299'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`log_path.read_text()` at line 304'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _load
  how: 'defines private function `_load` at line 19, signature: (name, filename=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 61, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_node_logs
  how: 'defines public function `test_write_node_logs` at line 102, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_log_carries_mint_id
  how: 'defines public function `test_write_log_carries_mint_id` at line 121, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_update_log_carries_mint_id
  how: 'defines public function `test_update_log_carries_mint_id` at line 142, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_update_node_logs
  how: 'defines public function `test_update_node_logs` at line 162, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _check
  how: 'defines private function `_check` at line 183, signature: (project, extra_args=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _check_capture
  how: 'defines private function `_check_capture` at line 192, signature: (project,
    extra_args=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_guard_silent_after_sanctioned_write
  how: 'defines public function `test_write_guard_silent_after_sanctioned_write` at
    line 202, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_guard_strict_ok_after_sanctioned_write
  how: 'defines public function `test_write_guard_strict_ok_after_sanctioned_write`
    at line 211, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_guard_warns_after_direct_edit
  how: 'defines public function `test_write_guard_warns_after_direct_edit` at line
    224, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_guard_warns_on_edited_payload
  how: 'defines public function `test_write_guard_warns_on_edited_payload` at line
    241, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_hook_output
  how: defines public function `test_hook_output` at line 266
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rejected_write_does_not_log
  how: 'defines public function `test_rejected_write_does_not_log` at line 285, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_guard_no_git
  how: 'defines public function `test_write_guard_no_git` at line 315, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ensure_payload_logs
  how: 'defines public function `test_ensure_payload_logs` at line 332, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_guard_silent_after_ensure_payload
  how: 'defines public function `test_write_guard_silent_after_ensure_payload` at
    line 351, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_guard_ignores_lock_files
  how: 'defines public function `test_write_guard_ignores_lock_files` at line 381,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_git_mv_logged_node_stays_silent
  how: 'defines public function `test_git_mv_logged_node_stays_silent` at line 419,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_hand_edit_after_git_mv_still_warns
  how: 'defines public function `test_hand_edit_after_git_mv_still_warns` at line
    440, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_log_follows_node_path_not_caller_root
  how: 'defines public function `test_write_log_follows_node_path_not_caller_root`
    at line 465, signature: (tmp_path, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_foreign_bare_file_is_not_leaked_into_caller_log
  how: 'defines public function `test_foreign_bare_file_is_not_leaked_into_caller_log`
    at line 489, signature: (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: context_doc
  how: 'defines public function `context_doc` at line 520, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_create_doc_stamps_link_ref_to_context_file
  how: 'defines public function `test_write_create_doc_stamps_link_ref_to_context_file`
    at line 533, signature: (project, context_doc)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_guard_warns_on_hand_edit_under_context
  how: 'defines public function `test_write_guard_warns_on_hand_edit_under_context`
    at line 552, signature: (project, context_doc)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_guard_silent_after_write_py_payload_edit
  how: 'defines public function `test_write_guard_silent_after_write_py_payload_edit`
    at line 566, signature: (project, context_doc)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_guard_silent_after_same_bytes_payload_relog
  how: 'defines public function `test_write_guard_silent_after_same_bytes_payload_relog`
    at line 579, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_guard_silent_on_hand_edit_to_schema_file
  how: 'defines public function `test_write_guard_silent_on_hand_edit_to_schema_file`
    at line 642, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: agi / "config.json"
  how: '`(agi / "config.json").write_text("{}")` at line 71'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sd / "[shape].md"
  how: '`(sd / "[shape].md").write_text(SHAPE)` at line 76'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nd2 / "i1.md"
  how: '`(nd2 / "i1.md").write_text( "---\nid: idea:i1\ntype: idea\n---\n\nbody\n")`
    at line 87'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(original + "\nExtra text\n")` at line 232'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: payload_file
  how: '`payload_file.write_text("#!/bin/bash\necho hello\n")` at line 247'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: payload_file
  how: '`payload_file.write_text("#!/bin/bash\necho modified\n")` at line 256'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / ".agi" / "config.json"
  how: '`(tmp_path / ".agi" / "config.json").write_text("{}")` at line 318'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / ".agi" / "sessions" / "write-log.jsonl"
  how: '`(tmp_path / ".agi" / "sessions" / "write-log.jsonl").write_text( ''{"sha256":
    "abc123", "path": "nodes/x.md"}\n'')` at line 320'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lock_file
  how: '`lock_file.write_text("")` at line 398'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(node_file.read_text() + "\nExtra\n")` at line 409'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: new
  how: '`new.write_text(new.read_text() + "\nHand edited.\n")` at line 455'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text( "---\nid: hypothesis:hv\ntype: hypothesis\n---\n\nbody\n")`
    at line 477'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: real_root / "config.json"
  how: '`(real_root / "config.json").write_text("{}")` at line 500'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: n_file
  how: '`n_file.write_text("---\nid: build:x\ntype: build\n---\n\nbody\n")` at line
    504'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.write_text("# bottom line\n\nfirst design-doc bytes.\n")` at line 525'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: context_doc
  how: '`context_doc.write_text(context_doc.read_text() + "\nHand edit.\n")` at line
    560'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: payload_file
  how: '`payload_file.write_text("#!/bin/bash\necho kid\n")` at line 594'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: payload_file
  how: '`payload_file.write_text("#!/bin/bash\necho kid changed\n")` at line 613'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(node_file.read_text() + "\nsome kid body\n")` at line
    614'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: schema
  how: '`schema.write_text(before + "# engine-edit note\n")` at line 654'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sd / fname
  how: '`(sd / fname).write_text( f"---\nname: {name}\nspawn:\n  {spawn}\n---\n{name}\n")`
    at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
