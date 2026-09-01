---
build_kind: code
confidence: 1.0
id: "build:tests-test-dispatch"
mint_id: 25741ab35bf440b99b59f7fde7f74ffa
origin: build-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_dispatch.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_dispatch.py"
type: build
---

`extensions/agi/tests/test_dispatch.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_dispatch.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 11'
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
outputs:
- name: _load_dispatch
  how: defines private function `_load_dispatch` at line 21
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build
  how: 'defines public function `build` at line 31, signature: (cfg: dict, tmp_path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: flag_value
  how: 'defines public function `flag_value` at line 35, signature: (args: list[str],
    flag: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_model_and_provider_reach_the_command_line
  how: 'defines public function `test_model_and_provider_reach_the_command_line` at
    line 39, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_thinking_is_passed_when_set
  how: 'defines public function `test_thinking_is_passed_when_set` at line 46, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_absent_or_empty_keys_pass_no_flag
  how: 'defines public function `test_absent_or_empty_keys_pass_no_flag` at line 60,
    signature: (cfg, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_flags_precede_the_prompt_arguments
  how: 'defines public function `test_flags_precede_the_prompt_arguments` at line
    70, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_binary_is_still_first
  how: 'defines public function `test_binary_is_still_first` at line 81, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: scaffold
  how: 'defines public function `scaffold` at line 89, signature: (parent: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_flag_is_emitted_when_there_is_a_parent
  how: 'defines public function `test_parent_flag_is_emitted_when_there_is_a_parent`
    at line 93, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parentless_node_emits_no_bare_parent_flag
  how: 'defines public function `test_parentless_node_emits_no_bare_parent_flag` at
    line 101, signature: (parent, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_zoom_command_always_states_the_runtime
  how: 'defines public function `test_zoom_command_always_states_the_runtime` at line
    116, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_zoom_command_passes_target_only_for_small
  how: 'defines public function `test_zoom_command_passes_target_only_for_small` at
    line 124, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_zoom_command_small_without_target_omits_the_flag
  how: 'defines public function `test_zoom_command_small_without_target_omits_the_flag`
    at line 131, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_aimed_slot_carries_the_target
  how: defines public function `test_aimed_slot_carries_the_target` at line 147
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_aim_defaults_to_small_because_big_zoom_discards_a_target
  how: defines public function `test_aim_defaults_to_small_because_big_zoom_discards_a_target`
    at line 152
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_every_slot_is_aimed_at_the_same_node
  how: defines public function `test_every_slot_is_aimed_at_the_same_node` at line
    160
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_explicit_level_is_honoured
  how: defines public function `test_explicit_level_is_honoured` at line 166
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_aiming_does_not_scaffold_a_parentless_idea
  how: defines public function `test_aiming_does_not_scaffold_a_parentless_idea` at
    line 171
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
