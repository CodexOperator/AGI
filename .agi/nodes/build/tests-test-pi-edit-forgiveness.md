---
build_kind: code
confidence: 1.0
id: "build:tests-test-pi-edit-forgiveness"
mint_id: b8cdeb0230cf4400ad756521f0d23887
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_pi_edit_forgiveness.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_pi_edit_forgiveness.py"
type: build
---

`extensions/agi/tests/test_pi_edit_forgiveness.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_pi_edit_forgiveness.py
parse_ok: true
inputs:
- name: sys
  how: '`import sys` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pi_adapter
  how: '`import pi_adapter` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pf
  how: '`import pi_edit_forgiveness as pf` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Path(resolved[0])
  how: '`Path(resolved[0]).read_text(encoding="utf-8")` at line 70'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.read_text(encoding="utf-8")` at line 94'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.read_text(encoding="utf-8")` at line 99'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.read_bytes()` at line 113'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.read_bytes()` at line 118'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.read_text(encoding="utf-8")` at line 133'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.read_text(encoding="utf-8")` at line 209'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.read_text(encoding="utf-8")` at line 147'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _real_install_text
  how: defines private function `_real_install_text` at line 63
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _strip_marker
  how: 'defines private function `_strip_marker` at line 73, signature: (code: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_install_missing_the_patch_is_reapplied
  how: 'defines public function `test_install_missing_the_patch_is_reapplied` at line
    87, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_install_already_patched_is_a_noop
  how: 'defines public function `test_install_already_patched_is_a_noop` at line 108,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unanchored_install_fails_loudly_instead_of_guessing
  how: 'defines public function `test_unanchored_install_fails_loudly_instead_of_guessing`
    at line 121, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_reapply_is_idempotent_when_run_twice
  how: 'defines public function `test_reapply_is_idempotent_when_run_twice` at line
    136, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _kid_command
  how: 'defines private function `_kid_command` at line 153, signature: (**kw)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_build_command_gates_the_installed_tool_every_spawn
  how: 'defines public function `test_build_command_gates_the_installed_tool_every_spawn`
    at line 165, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_build_command_raises_loudly_when_the_gate_cannot_reapply
  how: 'defines public function `test_build_command_raises_loudly_when_the_gate_cannot_reapply`
    at line 180, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_live_install_currently_carries_the_forgiveness_monkeypatch
  how: 'defines public function `test_live_install_currently_carries_the_forgiveness_monkeypatch`
    at line 196, signature: (monkeypatch, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.write_text(_strip_marker(_real_install_text() or _PRE_PATCH_STUB),
    encoding="utf-8")` at line 92'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.write_text(_PATCHED_STUB, encoding="utf-8")` at line 112'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.write_text("function somethingElse(x) { return x; }\n", encoding="utf-8")`
    at line 126'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.write_text(_PRE_PATCH_STUB, encoding="utf-8")` at line 140'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: target
  how: '`target.write_text(source, encoding="utf-8")` at line 204'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
