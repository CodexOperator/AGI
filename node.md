---
id: build:tests-test-adapters
mint_id: be981e6e78554a498f5eed6984759582
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_adapters.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_adapters.py"
---
`extensions/agi/tests/test_adapters.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_adapters.py
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
- name: sys
  how: '`import sys` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: adapters
  how: '`import adapters` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "dispatch.py"
  how: '`(BIN / "dispatch.py").read_text()` at line 186'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: test_load_returns_a_module_with_the_required_interface
  how: defines public function `test_load_returns_a_module_with_the_required_interface`
    at line 32
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_harness_names_the_directory_not_just_the_module
  how: defines public function `test_unknown_harness_names_the_directory_not_just_the_module`
    at line 39
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_adapters_own_missing_import_is_not_reported_as_unknown_harness
  how: defines public function `test_an_adapters_own_missing_import_is_not_reported_as_unknown_harness`
    at line 48
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_incomplete_adapter_is_rejected_at_load_not_at_spawn
  how: defines public function `test_incomplete_adapter_is_rejected_at_load_not_at_spawn`
    at line 61
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_declared_but_unimplemented_harness_raises_where_the_work_goes
  how: defines public function `test_declared_but_unimplemented_harness_raises_where_the_work_goes`
    at line 72
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_legacy_config_synthesizes_pi_and_is_the_mainline_path
  how: defines public function `test_legacy_config_synthesizes_pi_and_is_the_mainline_path`
    at line 85
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_legacy_synthesis_populates_both_tiers_explicitly
  how: defines public function `test_legacy_synthesis_populates_both_tiers_explicitly`
    at line 96
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_declared_harnesses_win_and_spawn_harness_selects
  how: defines public function `test_declared_harnesses_win_and_spawn_harness_selects`
    at line 105
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_several_harnesses_and_no_choice_is_an_error_not_a_guess
  how: defines public function `test_several_harnesses_and_no_choice_is_an_error_not_a_guess`
    at line 114
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_single_declared_harness_needs_no_spawn_block
  how: defines public function `test_a_single_declared_harness_needs_no_spawn_block`
    at line 120
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_adapter_name_defaults_from_the_harness_name_with_dashes_mapped
  how: defines public function `test_adapter_name_defaults_from_the_harness_name_with_dashes_mapped`
    at line 125
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parallelism_prefers_spawn_but_reads_the_legacy_key
  how: defines public function `test_parallelism_prefers_spawn_but_reads_the_legacy_key`
    at line 131
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_tier_selects_the_model
  how: defines public function `test_tier_selects_the_model` at line 140
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_tier_is_an_error_naming_the_tier_not_a_silent_fallback
  how: defines public function `test_unknown_tier_is_an_error_naming_the_tier_not_a_silent_fallback`
    at line 147
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_absent_keys_pass_no_flags_so_pis_own_settings_win
  how: defines public function `test_absent_keys_pass_no_flags_so_pis_own_settings_win`
    at line 156
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pi_bin_env_var_wins_over_config
  how: 'defines public function `test_pi_bin_env_var_wins_over_config` at line 160,
    signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_child_env_passes_the_scrubbed_base_through
  how: defines public function `test_child_env_passes_the_scrubbed_base_through` at
    line 167
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_child_env_can_inject_harness_specific_values
  how: defines public function `test_child_env_can_inject_harness_specific_values`
    at line 173
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dispatch_is_not_keyed_on_any_harness_name
  how: defines public function `test_dispatch_is_not_keyed_on_any_harness_name` at
    line 182
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_adding_a_harness_touches_only_config_and_one_file
  how: defines public function `test_adding_a_harness_touches_only_config_and_one_file`
    at line 196
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.write_text("import a_module_that_does_not_exist_anywhere\n")` at line
    53'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.write_text("NAME = ''incomplete''\ndef build_command(**kw):\n    return
    []\n")` at line 63'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.write_text( "NAME = ''thirdparty''\n" "def build_command(**kw):\n" "    return
    [''third'', kw[''tier''], kw[''agent_id'']]\n" "def child_env(*, harness, base):\n"
    "    return base\n" "def is_alive(pid):\n" "    return True\n" "def restart(**kw)...[truncated,
    266 chars total]` at line 200'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.