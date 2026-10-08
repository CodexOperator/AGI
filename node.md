---
build_kind: code
confidence: 1.0
id: "build:tests-test-claude-code-adapter"
mint_id: f514f22dc6e7418abd795f65ee750b49
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_claude_code_adapter.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_claude_code_adapter.py"
type: build
---

`extensions/agi/tests/test_claude_code_adapter.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_claude_code_adapter.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: adapters
  how: '`import adapters` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: provisioning
  how: '`import provisioning` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: rig["sess"] / "system-prompt.md"
  how: '`(rig["sess"] / "system-prompt.md").read_text()` at line 180'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: rig["sess"] / "system-prompt.md"
  how: '`(rig["sess"] / "system-prompt.md").read_text()` at line 194'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prompt_file
  how: '`prompt_file.read_text()` at line 252'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Path(value(args, "--append-system-prompt-file"))
  how: '`Path(value(args, "--append-system-prompt-file")).read_text()` at line 269'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log
  how: '`log.read_text()` at line 612'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(args[i + 1])` at line 69'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(args_d[args_d.index("--settings") + 1])` at line 80'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: rig
  how: 'defines public function `rig` at line 42, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_settings_flag_when_absent
  how: 'defines public function `test_no_settings_flag_when_absent` at line 56, signature:
    (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_settings_ultracode_appends_settings_flag
  how: 'defines public function `test_settings_ultracode_appends_settings_flag` at
    line 62, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_settings_per_tier_map
  how: 'defines public function `test_settings_per_tier_map` at line 72, signature:
    (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_effort_and_settings_combine
  how: 'defines public function `test_effort_and_settings_combine` at line 83, signature:
    (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ultracode_tier_sets_env_var
  how: 'defines public function `test_ultracode_tier_sets_env_var` at line 91, signature:
    (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_ultracode_tier_no_env_var
  how: 'defines public function `test_non_ultracode_tier_no_env_var` at line 100,
    signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ultracode_tier_keyword_opens_user_turn
  how: 'defines public function `test_ultracode_tier_keyword_opens_user_turn` at line
    116, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_ultracode_tier_no_keyword
  how: 'defines public function `test_non_ultracode_tier_no_keyword` at line 127,
    signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build
  how: 'defines public function `build` at line 134, signature: (rig, tier=''kid'',
    harness=HARNESS, **kw)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: value
  how: 'defines public function `value` at line 145, signature: (args, flag)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: variadic_values
  how: 'defines public function `variadic_values` at line 149, signature: (args, flag)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_adapter_threads_brief_tier_while_keeping_the_model_tier
  how: 'defines public function `test_adapter_threads_brief_tier_while_keeping_the_model_tier`
    at line 165, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_adapter_brief_tier_defaults_to_the_spawn_tier
  how: 'defines public function `test_adapter_brief_tier_defaults_to_the_spawn_tier`
    at line 189, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_adapter_implements_the_whole_interface_not_a_stub
  how: defines public function `test_adapter_implements_the_whole_interface_not_a_stub`
    at line 202
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_config_entry_resolves_to_this_adapter
  how: defines public function `test_config_entry_resolves_to_this_adapter` at line
    212
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_headless_and_the_model_follows_the_tier
  how: 'defines public function `test_headless_and_the_model_follows_the_tier` at
    line 223, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_tier_is_a_named_error_not_a_fallback
  how: 'defines public function `test_missing_tier_is_a_named_error_not_a_fallback`
    at line 231, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_models_block_passes_no_model_flag
  how: 'defines public function `test_no_models_block_passes_no_model_flag` at line
    237, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_every_brief_segment_lands_in_one_system_prompt_file
  how: 'defines public function `test_every_brief_segment_lands_in_one_system_prompt_file`
    at line 242, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_tier_gets_the_parent_brief_on_the_parent_model
  how: 'defines public function `test_parent_tier_gets_the_parent_brief_on_the_parent_model`
    at line 265, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_closing_line_is_fenced_behind_a_double_dash
  how: 'defines public function `test_closing_line_is_fenced_behind_a_double_dash`
    at line 275, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_context_is_an_error_not_a_quiet_omission
  how: 'defines public function `test_missing_context_is_an_error_not_a_quiet_omission`
    at line 287, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_output_streams_so_a_killed_agent_leaves_a_log
  how: 'defines public function `test_output_streams_so_a_killed_agent_leaves_a_log`
    at line 297, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_add_dir_is_the_repo_root_so_edits_outside_dot_agi_are_allowed
  how: 'defines public function `test_add_dir_is_the_repo_root_so_edits_outside_dot_agi_are_allowed`
    at line 307, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mcp_servers_are_off_unless_the_harness_names_them
  how: 'defines public function `test_mcp_servers_are_off_unless_the_harness_names_them`
    at line 314, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_tools_are_a_closed_list_with_no_agent_and_git_writes_are_refused
  how: 'defines public function `test_tools_are_a_closed_list_with_no_agent_and_git_writes_are_refused`
    at line 321, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_tool_lists_come_from_config_when_declared
  how: 'defines public function `test_tool_lists_come_from_config_when_declared` at
    line 336, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_optional_knobs_are_omitted_unless_set
  how: 'defines public function `test_optional_knobs_are_omitted_unless_set` at line
    346, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_kid_with_role_keeps_the_full_default_block_list
  how: 'defines public function `test_kid_with_role_keeps_the_full_default_block_list`
    at line 364, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _advisor_tools
  how: 'defines private function `_advisor_tools` at line 375, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_advisor_parent_at_tier3_adds_ultracode_tools
  how: 'defines public function `test_advisor_parent_at_tier3_adds_ultracode_tools`
    at line 386, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_advisor_parent_at_tier3_drops_dispatch_rule_but_keeps_others
  how: 'defines public function `test_advisor_parent_at_tier3_drops_dispatch_rule_but_keeps_others`
    at line 393, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_director_at_tier1_gets_the_same_tools_as_advisor
  how: 'defines public function `test_director_at_tier1_gets_the_same_tools_as_advisor`
    at line 405, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_privileged_only_for_the_exact_role_and_tier
  how: 'defines public function `test_privileged_only_for_the_exact_role_and_tier`
    at line 418, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_role_given_keeps_todays_behaviour
  how: 'defines public function `test_no_role_given_keeps_todays_behaviour` at line
    426, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_per_role_config_override_wins_over_flat_and_default
  how: 'defines public function `test_per_role_config_override_wins_over_flat_and_default`
    at line 435, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_per_role_override_only_claims_the_named_role
  how: 'defines public function `test_per_role_override_only_claims_the_named_role`
    at line 446, signature: (rig)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_effort_may_be_a_per_tier_map
  how: defines public function `test_effort_may_be_a_per_tier_map` at line 457
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_session_id_from_stream_json_log
  how: defines public function `test_session_id_from_stream_json_log` at line 474
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_session_id_from_stream_json_log
  how: 'defines public function `test_session_id_from_stream_json_log` at line 497,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_session_id_from_stream_json_log
  how: 'defines public function `test_session_id_from_stream_json_log` at line 517,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_record_session_pin_derives_transcript_then_meter_reads_it
  how: 'defines public function `test_record_session_pin_derives_transcript_then_meter_reads_it`
    at line 532, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_limit_from_result_text_detects_subscription_limit
  how: defines public function `test_limit_from_result_text_detects_subscription_limit`
    at line 582
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_scan_log_for_session_limit_yields_no_retry_and_one_limit_line
  how: 'defines public function `test_scan_log_for_session_limit_yields_no_retry_and_one_limit_line`
    at line 592, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_close_session_limit_releases_the_lease
  how: 'defines public function `test_close_session_limit_releases_the_lease` at line
    616, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_finished_child_leaves_no_zombie_not_a_real_spawn
  how: defines public function `test_finished_child_leaves_no_zombie_not_a_real_spawn`
    at line 637
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_is_alive_still_true_for_a_live_pid
  how: defines public function `test_is_alive_still_true_for_a_live_pid` at line 655
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ctx
  how: '`ctx.write_text("# ZOOM CONTEXT MARKER\nsome map\n")` at line 50'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: skill
  how: '`skill.write_text("SKILL PROMPT MARKER\n")` at line 52'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log
  how: '`log.write_text( ''{"type":"assistant","session_id":"abc-123","message":{"role":"assistant","usage":{"input_tokens":1}}}\n''
    ''{"type":"assistant","session_id":"ignored","message":{"role":"assistant","usage":{"input_tokens":2}}}\n''
    )` at line 479'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: empty
  how: '`empty.write_text("not json\n")` at line 486'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log
  how: '`log.write_text( ''{"type":"assistant","session_id":"abc-123","message":{"role":"assistant","usage":{"input_tokens":1}}}\n''
    ''{"type":"assistant","session_id":"ignored","message":{"role":"assistant","usage":{"input_tokens":2}}}\n''
    )` at line 502'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: empty
  how: '`empty.write_text("not json\n")` at line 508'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log
  how: '`log.write_text( ''{"type":"assistant","session_id":"abc-123","message":{"role":"assistant","usage":{"input_tokens":1}}}\n''
    ''{"type":"assistant","session_id":"ignored","message":{"role":"assistant","usage":{"input_tokens":2}}}\n''
    )` at line 522'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: empty
  how: '`empty.write_text("not json\n")` at line 528'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "config.json"
  how: '`(graph / "config.json").write_text("{}")` at line 544'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: logf
  how: '`logf.write_text(''{"type":"assistant","session_id":"own-sess-1","message":{"role":"assistant","usage":{"input_tokens":5000}}}\n'')`
    at line 548'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: own
  how: '`own.write_text(''{"message":{"role":"assistant","usage":{"input_tokens":5000,"cache_read_input_tokens":0,"cache_creation_input_tokens":0}}}\n'')`
    at line 554'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: foreign
  how: '`foreign.write_text(''{"message":{"role":"assistant","usage":{"input_tokens":99500,"cache_read_input_tokens":0,"cache_creation_input_tokens":0}}}\n'')`
    at line 556'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log
  how: '`log.write_text("".join(_json.dumps(e) + "\n" for e in events))` at line 604'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
