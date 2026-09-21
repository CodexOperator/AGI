---
build_kind: code
confidence: 1.0
id: "build:tests-test-rotate"
mint_id: 2ed744c891d3432fb062d8e6882d2fd8
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_rotate.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_rotate.py"
type: build
---

`extensions/agi/tests/test_rotate.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_rotate.py
parse_ok: true
inputs:
- name: json
  how: '`import json` at line 1'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 2'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 3'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 4'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 5'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: types.SimpleNamespace
  how: '`from types import SimpleNamespace` at line 6'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: agi.bin.rotate
  how: '`from agi.bin import rotate` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: agi.bin.brief
  how: '`from agi.bin import brief` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(records[-1].read_text(encoding="utf-8"))` at line 1236'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(records[-1].read_text(encoding="utf-8"))` at line 1276'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(records[-1].read_text(encoding="utf-8"))` at line 1305'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(records[-1].read_text(encoding="utf-8"))` at line 1337'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fake_transcript
  how: '`fake_transcript.read_text()` at line 51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dms[0]
  how: '`dms[0].read_text(encoding="utf-8")` at line 905'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: script
  how: '`script.read_text()` at line 1181'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: records[-1]
  how: '`records[-1].read_text(encoding="utf-8")` at line 1236'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: records[-1]
  how: '`records[-1].read_text(encoding="utf-8")` at line 1276'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: records[-1]
  how: '`records[-1].read_text(encoding="utf-8")` at line 1305'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: records[-1]
  how: '`records[-1].read_text(encoding="utf-8")` at line 1337'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(seq_file.read_text())` at line 1698'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: seq_file
  how: '`seq_file.read_text()` at line 1698'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`win.read_text(encoding="utf-8")` at line 937'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: fake_ladder
  how: 'defines public function `fake_ladder` at line 16, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fake_transcript
  how: 'defines public function `fake_transcript` at line 36, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_meter_uses_cc_transcript
  how: 'defines public function `test_meter_uses_cc_transcript` at line 47, signature:
    (monkeypatch, tmp_path, fake_ladder, fake_transcript, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_meter_check_threshold
  how: 'defines public function `test_meter_check_threshold` at line 63, signature:
    (monkeypatch, tmp_path, fake_ladder, fake_transcript, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_dry_run
  how: 'defines public function `test_spawn_dry_run` at line 88, signature: (monkeypatch,
    tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_refuses_existing_window
  how: 'defines public function `test_spawn_refuses_existing_window` at line 107,
    signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_window_reusable_for_non_prime_name
  how: 'defines public function `test_spawn_window_reusable_for_non_prime_name` at
    line 130, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_loop_uses_spawn_window
  how: 'defines public function `test_loop_uses_spawn_window` at line 149, signature:
    (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _proj
  how: 'defines private function `_proj` at line 178, signature: (tmp_path, ladder_roles='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_resolves_role_model_effort_settings
  how: 'defines public function `test_spawn_resolves_role_model_effort_settings` at
    line 193, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_normalizes_string_settings_word
  how: 'defines public function `test_spawn_normalizes_string_settings_word` at line
    220, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_ultracode_prefixes_env_and_keyword
  how: 'defines public function `test_spawn_ultracode_prefixes_env_and_keyword` at
    line 247, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_plain_role_no_env_no_keyword
  how: 'defines public function `test_spawn_plain_role_no_env_no_keyword` at line
    279, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_falls_back_to_defaults_without_table
  how: 'defines public function `test_spawn_falls_back_to_defaults_without_table`
    at line 304, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_successor_prompt_prepends_constitution_head
  how: defines public function `test_successor_prompt_prepends_constitution_head`
    at line 323
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ladder_roles_table_has_a_liaison_row
  how: defines public function `test_ladder_roles_table_has_a_liaison_row` at line
    335
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_tier_liaison_resolves_sonnet_high_from_the_new_row
  how: 'defines public function `test_spawn_tier_liaison_resolves_sonnet_high_from_the_new_row`
    at line 349, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_liaison_prompt_sources_the_assembled_brief_not_the_static_file
  how: 'defines public function `test_spawn_liaison_prompt_sources_the_assembled_brief_not_the_static_file`
    at line 371, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_prime_director_static_path_is_unchanged
  how: 'defines public function `test_spawn_prime_director_static_path_is_unchanged`
    at line 397, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_derive_successor_name
  how: defines public function `test_derive_successor_name` at line 417
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_default_name_derives_from_window_path
  how: 'defines public function `test_spawn_default_name_derives_from_window_path`
    at line 436, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_loop_below_threshold_holds
  how: 'defines public function `test_loop_below_threshold_holds` at line 455, signature:
    (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_loop_over_threshold_rotates_and_continue
  how: 'defines public function `test_loop_over_threshold_rotates_and_continue` at
    line 474, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_loop_fails_loud_when_no_successor_window
  how: 'defines public function `test_loop_fails_loud_when_no_successor_window` at
    line 513, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_loop_readback_never_uses_caller_session_log
  how: 'defines public function `test_loop_readback_never_uses_caller_session_log`
    at line 542, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_transcripts
  how: 'defines private function `_write_transcripts` at line 572, signature: (projects_dir,
    pinned_usage, foreign_usage, pinned_name=''pinned.jsonl'', foreign_name=''foreign.jsonl'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _fake_cc_projects
  how: 'defines private function `_fake_cc_projects` at line 596, signature: (tmp_path,
    monkeypatch, pinned_usage=2000, foreign_usage=40000)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_pin
  how: 'defines private function `_write_pin` at line 605, signature: (root, target,
    name=''prime.meter'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_seat_pin_stable_across_two_rotations_same_name
  how: 'defines public function `test_seat_pin_stable_across_two_rotations_same_name`
    at line 616, signature: (monkeypatch, tmp_path, fake_ladder, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_seat_pin_refuses_predecessors_generation
  how: 'defines public function `test_seat_pin_refuses_predecessors_generation` at
    line 634, signature: (monkeypatch, tmp_path, fake_ladder, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_seat_pin_same_generation_reads_clean
  how: 'defines public function `test_seat_pin_same_generation_reads_clean` at line
    658, signature: (monkeypatch, tmp_path, fake_ladder, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_meter_pin_file_wins_over_newer_foreign
  how: 'defines public function `test_meter_pin_file_wins_over_newer_foreign` at line
    674, signature: (monkeypatch, tmp_path, fake_ladder, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_meter_agi_session_log_env_uses_pinned
  how: 'defines public function `test_meter_agi_session_log_env_uses_pinned` at line
    686, signature: (monkeypatch, tmp_path, fake_ladder, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_meter_explicit_session_log_wins
  how: 'defines public function `test_meter_explicit_session_log_wins` at line 696,
    signature: (monkeypatch, tmp_path, fake_ladder, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_meter_fallback_warns_and_picks_newest
  how: 'defines public function `test_meter_fallback_warns_and_picks_newest` at line
    705, signature: (monkeypatch, tmp_path, fake_ladder, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_loop_uses_same_resolver
  how: 'defines public function `test_loop_uses_same_resolver` at line 716, signature:
    (monkeypatch, tmp_path, fake_ladder, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pin_path_never_doubles_agi_dir
  how: 'defines public function `test_pin_path_never_doubles_agi_dir` at line 732,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_is_log_noise_markers
  how: defines public function `test_is_log_noise_markers` at line 752
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_readback_skips_bracketed_log_lines
  how: 'defines public function `test_readback_skips_bracketed_log_lines` at line
    762, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_readback_reports_diff_when_no_continue
  how: 'defines public function `test_readback_reports_diff_when_no_continue` at line
    777, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_readback_never_returns_a_bracketed_line
  how: 'defines public function `test_readback_never_returns_a_bracketed_line` at
    line 789, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sessions_dir_resolves_to_main_from_a_worktree
  how: 'defines public function `test_sessions_dir_resolves_to_main_from_a_worktree`
    at line 806, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_seats_sheet
  how: 'defines private function `_write_seats_sheet` at line 841, signature: (root,
    rows)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pin_seat_transcript
  how: 'defines private function `_pin_seat_transcript` at line 853, signature: (root,
    name, tokens)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rotate_self_args
  how: 'defines private function `_rotate_self_args` at line 867, signature: (tmp_path,
    **over)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_alarms_once_holds_below_threshold
  how: 'defines public function `test_alarms_once_holds_below_threshold` at line 876,
    signature: (fake_ladder, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_alarms_once_dms_holder_when_due_then_stops
  how: 'defines public function `test_alarms_once_dms_holder_when_due_then_stops`
    at line 891, signature: (fake_ladder, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotate_self_dry_run_reuses_plain_name_no_roman
  how: 'defines public function `test_rotate_self_dry_run_reuses_plain_name_no_roman`
    at line 908, signature: (fake_ladder, tmp_path, capsys, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotate_self_renames_window_before_respawn
  how: 'defines public function `test_rotate_self_renames_window_before_respawn` at
    line 928, signature: (fake_ladder, tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotate_self_kills_own_window_after_continue
  how: 'defines public function `test_rotate_self_kills_own_window_after_continue`
    at line 952, signature: (fake_ladder, tmp_path, capsys, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_seat_handoff_generation_bumps_on_rotation
  how: 'defines public function `test_seat_handoff_generation_bumps_on_rotation` at
    line 977, signature: (fake_ladder, tmp_path, capsys, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_seats_flag_lists_fraction_and_age
  how: 'defines public function `test_status_seats_flag_lists_fraction_and_age` at
    line 1000, signature: (fake_ladder, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotate_self_cursor_ignores_stale_predecessor_continue
  how: 'defines public function `test_rotate_self_cursor_ignores_stale_predecessor_continue`
    at line 1014, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_window_successor_argv_override_replaces_claude
  how: 'defines public function `test_spawn_window_successor_argv_override_replaces_claude`
    at line 1038, signature: (tmp_path, capsys, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_window_default_still_real_claude
  how: 'defines public function `test_spawn_window_default_still_real_claude` at line
    1057, signature: (tmp_path, capsys, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotate_self_throwaway_skips_registry
  how: 'defines public function `test_rotate_self_throwaway_skips_registry` at line
    1070, signature: (fake_ladder, tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotate_self_without_throwaway_still_refuses_unregistered
  how: 'defines public function `test_rotate_self_without_throwaway_still_refuses_unregistered`
    at line 1097, signature: (fake_ladder, tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotate_self_throwaway_forwards_successor_argv
  how: 'defines public function `test_rotate_self_throwaway_forwards_successor_argv`
    at line 1112, signature: (fake_ladder, tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_launch_window_returns_tmux_failure_instead_of_swallowing_it
  how: 'defines public function `test_launch_window_returns_tmux_failure_instead_of_swallowing_it`
    at line 1138, signature: (monkeypatch, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_launch_window_hands_tmux_a_short_argv_for_a_long_command
  how: 'defines public function `test_launch_window_hands_tmux_a_short_argv_for_a_long_command`
    at line 1157, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_launch_window_leaves_a_short_command_inline
  how: 'defines public function `test_launch_window_leaves_a_short_command_inline`
    at line 1185, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotate_self_writes_record_with_five_observations
  how: 'defines public function `test_rotate_self_writes_record_with_five_observations`
    at line 1212, signature: (fake_ladder, tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotate_self_refuses_when_successor_window_absent
  how: 'defines public function `test_rotate_self_refuses_when_successor_window_absent`
    at line 1258, signature: (fake_ladder, tmp_path, monkeypatch, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotate_self_refuses_when_predecessor_window_gone
  how: 'defines public function `test_rotate_self_refuses_when_predecessor_window_gone`
    at line 1281, signature: (fake_ladder, tmp_path, monkeypatch, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_loop_writes_durable_record
  how: 'defines public function `test_loop_writes_durable_record` at line 1310, signature:
    (fake_ladder, tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_seats_launch_resolves_one_per_remote_seat
  how: 'defines public function `test_seats_launch_resolves_one_per_remote_seat` at
    line 1348, signature: (tmp_path, capsys, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_seats_launch_read_back_confirms_all_windows
  how: 'defines public function `test_seats_launch_read_back_confirms_all_windows`
    at line 1388, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_seats_launch_no_remote_seats_returns_1
  how: 'defines public function `test_seats_launch_no_remote_seats_returns_1` at line
    1417, signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_tiler_partitions_full_screen_no_overlap_no_gaps
  how: defines public function `test_tiler_partitions_full_screen_no_overlap_no_gaps`
    at line 1430
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_tile_command_dry_run_prints_one_rect_per_window
  how: 'defines public function `test_tile_command_dry_run_prints_one_rect_per_window`
    at line 1446, signature: (monkeypatch, tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_tile_apply_places_live_windows_via_wmctrl
  how: 'defines public function `test_tile_apply_places_live_windows_via_wmctrl` at
    line 1465, signature: (monkeypatch, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_tile_apply_degrades_gracefully_without_wm
  how: 'defines public function `test_tile_apply_degrades_gracefully_without_wm` at
    line 1503, signature: (monkeypatch, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_compose_announcement_carries_all_five_fields
  how: defines public function `test_compose_announcement_carries_all_five_fields`
    at line 1531
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_derive_receivers_drops_gone_window_and_self
  how: 'defines public function `test_derive_receivers_drops_gone_window_and_self`
    at line 1546, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_announce_rotation_dms_every_derived_recipient
  how: 'defines public function `test_announce_rotation_dms_every_derived_recipient`
    at line 1558, signature: (monkeypatch, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_announce_rotation_prime_routes_to_alert_room_never_quorum
  how: 'defines public function `test_announce_rotation_prime_routes_to_alert_room_never_quorum`
    at line 1580, signature: (monkeypatch, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_loop_success_announces_exactly_once_refusal_never
  how: 'defines public function `test_loop_success_announces_exactly_once_refusal_never`
    at line 1601, signature: (fake_ladder, tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rotate_self_success_announces_once_refusal_never
  how: 'defines public function `test_rotate_self_success_announces_once_refusal_never`
    at line 1648, signature: (fake_ladder, tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sequence_counter_is_monotonic_and_durable
  how: 'defines public function `test_sequence_counter_is_monotonic_and_durable` at
    line 1686, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_announce_stamps_payload_with_seq_and_writes_sequence_file
  how: 'defines public function `test_announce_stamps_payload_with_seq_and_writes_sequence_file`
    at line 1701, signature: (monkeypatch, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cmd_sequence_is_the_seat_visible_one_read
  how: 'defines public function `test_cmd_sequence_is_the_seat_visible_one_read` at
    line 1723, signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_refused_loop_does_not_advance_sequence
  how: 'defines public function `test_refused_loop_does_not_advance_sequence` at line
    1753, signature: (fake_ladder, tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_openrouter_key_env_file_found_via_repo_root_not_graph_root
  how: 'defines public function `test_openrouter_key_env_file_found_via_repo_root_not_graph_root`
    at line 1790, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_openrouter_key_prefers_env_var_over_dotenv_file
  how: 'defines public function `test_openrouter_key_prefers_env_var_over_dotenv_file`
    at line 1806, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_openrouter_key_none_when_neither_configured
  how: 'defines public function `test_openrouter_key_none_when_neither_configured`
    at line 1814, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_fresh_spend_status_shows_both_key_and_account_labelled
  how: 'defines public function `test_fresh_spend_status_shows_both_key_and_account_labelled`
    at line 1821, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_fresh_spend_status_none_when_network_fails
  how: 'defines public function `test_fresh_spend_status_none_when_network_fails`
    at line 1845, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_fresh_spend_status_none_without_a_key
  how: 'defines public function `test_fresh_spend_status_none_without_a_key` at line
    1854, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_meter_pin_claim_prints_spend_status
  how: 'defines public function `test_meter_pin_claim_prints_spend_status` at line
    1861, signature: (monkeypatch, tmp_path, fake_ladder, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_meter_read_without_pin_does_not_print_spend_status
  how: 'defines public function `test_meter_read_without_pin_does_not_print_spend_status`
    at line 1875, signature: (monkeypatch, tmp_path, fake_ladder, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: transcript
  how: '`transcript.write_text( """ {"message": {"role": "assistant", "usage": {"input_tokens":
    1000, "cache_read_input_tokens": 200, "cache_creation_input_tokens": 300}}} {"message":
    {"role": "assistant", "usage": {"input_tokens": 2000, "cache_read...[truncated,
    302 chars total]` at line 38'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dst
  how: '`dst.write_text(fake_transcript.read_text())` at line 51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`log_path.write_text( """ USAGE: {"input_tokens": 40000, "cache_read_input_tokens":
    10000, "cache_creation_input_tokens": 0} """ )` at line 71'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prompt
  how: '`prompt.write_text("Hello {name}")` at line 90'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prompt
  how: '`prompt.write_text("Hello {name}")` at line 109'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prompt
  how: '`prompt.write_text("You are {name}\n")` at line 134'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / ".geometry" / "ladder.md"
  how: '`(root / "nodes" / ".geometry" / "ladder.md").write_text("\n".join(lines))`
    at line 189'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prompt
  how: '`prompt.write_text("You are {name}\n")` at line 204'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prompt
  how: '`prompt.write_text("You are {name}\n")` at line 232'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prompt
  how: '`prompt.write_text("You are {name}\n")` at line 262'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prompt
  how: '`prompt.write_text("You are {name}\n")` at line 290'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prompt
  how: '`prompt.write_text("You are {name}\n")` at line 308'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sentinel
  how: '`sentinel.write_text("STATIC PRIME BODY {name}\n")` at line 384'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sentinel
  how: '`sentinel.write_text("STATIC PRIME BODY {name}\n")` at line 402'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prompt
  how: '`prompt.write_text("hi {name}")` at line 439'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wins
  how: '`wins.write_text("belam-S1-L3\n")` at line 441'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "successor.md"
  how: '`(tmp_path / "successor.md").write_text("you are {name}\n")` at line 481'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: reply
  how: '`reply.write_text("continue\n")` at line 486'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wins
  how: '`wins.write_text("")` at line 488'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: reply
  how: '`reply.write_text("continue\n")` at line 522'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wins
  how: '`wins.write_text("")` at line 524'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: succ
  how: '`succ.write_text("")` at line 551'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: caller
  how: '`caller.write_text("the CALLER just wrote a line containing bare continue\n")`
    at line 553'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wins
  how: '`wins.write_text("belam-III\n")` at line 555'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pinned
  how: '`pinned.write_text( f''{{"message": {{"role": "assistant", "usage": '' f''{{"input_tokens":
    {pinned_usage}, "cache_read_input_tokens": 0, '' f''"cache_creation_input_tokens":
    0}}}}}}\n'' )` at line 577'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: foreign
  how: '`foreign.write_text( f''{{"message": {{"role": "assistant", "usage": '' f''{{"input_tokens":
    {foreign_usage}, "cache_read_input_tokens": 0, '' f''"cache_creation_input_tokens":
    0}}}}}}\n'' )` at line 583'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pin
  how: '`pin.write_text(str(target) + "\n", encoding="utf-8")` at line 612'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pin
  how: '`pin.write_text("/tmp/some-transcript.jsonl\n", encoding="utf-8")` at line
    742'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log
  how: '`log.write_text( "[DEBUG] MDM settings load completed in 1ms\n" "2026-09-07T06:04:41.633Z
    [WARN] [bridge] continuing as before\n" "continue\n", encoding="utf-8", )` at
    line 768'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log
  how: '`log.write_text( "[DEBUG] MDM settings load completed in 1ms\n" "valuable
    diff line\n", encoding="utf-8", )` at line 781'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log
  how: '`log.write_text( "[DEBUG] MDM settings load completed in 1ms\n" "2026-09-07T06:04:41.633Z
    [WARN] [bridge] no anchor\n", encoding="utf-8", )` at line 793'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / ".agi" / "config.json"
  how: '`(repo / ".agi" / "config.json").write_text(''{"metric_primary": "x"}'')`
    at line 819'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nodes / "seats.md"
  how: '`(nodes / "seats.md").write_text(body, encoding="utf-8")` at line 850'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: transcript
  how: '`transcript.write_text(json.dumps({ "message": {"role": "assistant", "usage":
    {"input_tokens": tokens, "cache_read_input_tokens": 0, "cache_creation_input_tokens":
    0}}, }) + "\n", encoding="utf-8")` at line 856'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "sessions" / f"{name}.meter"
  how: '`(root / "sessions" / f"{name}.meter").write_text( str(transcript) + "\n",
    encoding="utf-8")` at line 862'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`win.write_text("adv-alive\n", encoding="utf-8")` at line 934'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`win.write_text("adv-alive\n", encoding="utf-8")` at line 959'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hand / "adv-alive.handoff.md"
  how: '`(hand / "adv-alive.handoff.md").write_text( "seat: adv-alive\ngeneration:
    3\n", encoding="utf-8")` at line 985'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log
  how: '`log.write_text("continue\nvalid successor line\n", encoding="utf-8")` at
    line 1020'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`win.write_text("adv-alive\n", encoding="utf-8")` at line 1078'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mk / "seats.md"
  how: '`(mk / "seats.md").write_text("---\nid: config:seats\ntype: config\n---\n",
    encoding="utf-8")` at line 1104'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`win.write_text("adv-alive\n", encoding="utf-8")` at line 1117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`win.write_text("adv-alive\n", encoding="utf-8")` at line 1218'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`win.write_text("adv-alive\n", encoding="utf-8")` at line 1263'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`win.write_text("adv-alive\n", encoding="utf-8")` at line 1287'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: reply
  how: '`reply.write_text("continue\n")` at line 1318'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wins
  how: '`wins.write_text("")` at line 1320'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wpath
  how: '`wpath.write_text("belam\ntty-one\n", encoding="utf-8")` at line 1404'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wpath
  how: '`wpath.write_text("tty-one\n", encoding="utf-8")` at line 1412'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wpath
  how: '`wpath.write_text("belam\ntty-one\n", encoding="utf-8")` at line 1476'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wpath
  how: '`wpath.write_text("belam\n", encoding="utf-8")` at line 1510'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: success_reply
  how: '`success_reply.write_text("continue\n")` at line 1612'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wins
  how: '`wins.write_text("")` at line 1614'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wins
  how: '`wins.write_text("")` at line 1634'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`win.write_text("adv-alive\n", encoding="utf-8")` at line 1651'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`win.write_text("adv-alive\n", encoding="utf-8")` at line 1672'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: seq_file
  how: '`seq_file.write_text("not json\n", encoding="utf-8")` at line 1746'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wins
  how: '`wins.write_text("")` at line 1764'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / ".env"
  how: '`(tmp_path / ".env").write_text("OPENROUTER_API_KEY=sk-or-v1-test123\n")`
    at line 1802'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / ".env"
  how: '`(tmp_path / ".env").write_text("OPENROUTER_API_KEY=sk-or-v1-fromfile\n")`
    at line 1809'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wins
  how: '`wins.write_text(name + "\n")` at line 493'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`win.write_text("adv-alive\n", encoding="utf-8")` at line 1291'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wins
  how: '`wins.write_text(n + "\n", encoding="utf-8")` at line 1323'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wins
  how: '`wins.write_text(n + "\n", encoding="utf-8")` at line 1617'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({ "message": {"role": "assistant", "usage": {"input_tokens": tokens,
    "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}}, })` at line
    856'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`open(win, "a", encoding="utf-8")` at line 939 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`open(win, "a", encoding="utf-8")` at line 963 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`open(win, "a", encoding="utf-8")` at line 1081 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`open(win, "a", encoding="utf-8")` at line 1120 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`open(win, "a", encoding="utf-8")` at line 1222 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: win
  how: '`open(win, "a", encoding="utf-8")` at line 1654 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(r)` at line 848'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
