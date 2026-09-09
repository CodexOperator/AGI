---
build_kind: code
confidence: 1.0
id: "build:tests-test-send"
mint_id: 2df5fb9add2945dca17a20ded50a0abd
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_send.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_send.py"
type: build
---

`extensions/agi/tests/test_send.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_send.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 7'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 9'
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
- name: inbox
  how: '`inbox.read_text()` at line 44'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "sessions" / "inbox" / "agent-x.md"
  how: '`(project / "sessions" / "inbox" / "agent-x.md").read_text()` at line 188'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "sessions" / "inbox" / "recip.md"
  how: '`(project / "sessions" / "inbox" / "recip.md").read_text()` at line 194'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: comms / "dm" / "me--you.md"
  how: '`(comms / "dm" / "me--you.md").read_text()` at line 342'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: comms / "room" / "tier3-quorum.md"
  how: '`(comms / "room" / "tier3-quorum.md").read_text()` at line 399'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: inbox
  how: '`inbox.read_text()` at line 469'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: comms / "room" / "tier3-quorum.md"
  how: '`(comms / "room" / "tier3-quorum.md").read_text()` at line 543'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads((comms / "audience" / "state.json").read_text())` at line 604'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: croot / "room" / "quorum.md"
  how: '`(croot / "room" / "quorum.md").read_text()` at line 636'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: inbox
  how: '`inbox.read_text()` at line 657'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 759'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 831'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: reply_path
  how: '`reply_path.read_text()` at line 858'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: inbox
  how: '`inbox.read_text()` at line 103'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: proj / ".agi" / "config.json"
  how: '`(proj / ".agi" / "config.json").read_text()` at line 305'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 317'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: comms / "room" / "tier3-quorum.md"
  how: '`(comms / "room" / "tier3-quorum.md").read_text()` at line 557'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: comms / "audience" / "state.json"
  how: '`(comms / "audience" / "state.json").read_text()` at line 604'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: croot / "room" / "t1.md"
  how: '`(croot / "room" / "t1.md").read_text()` at line 677'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: reply_path
  how: '`reply_path.read_text()` at line 816'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ask_path
  how: '`ask_path.read_text()` at line 875'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: reply_path
  how: '`reply_path.read_text()` at line 889'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: croot / "room" / "quorum-requests.md"
  how: '`( croot / "room" / "quorum-requests.md").read_text()` at line 906'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 930'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 947'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: project
  how: 'defines public function `project` at line 26, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_send_creates_inbox_file
  how: 'defines public function `test_send_creates_inbox_file` at line 39, signature:
    (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_send_prints_inbox_path
  how: 'defines public function `test_send_prints_inbox_path` at line 50, signature:
    (project: Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _fake_tmux
  how: 'defines private function `_fake_tmux` at line 60, signature: (monkeypatch,
    window_names)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_send_nudges_existing_window
  how: 'defines public function `test_send_nudges_existing_window` at line 77, signature:
    (project: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_send_dm_nudges_other_party
  how: 'defines public function `test_send_dm_nudges_other_party` at line 89, signature:
    (project: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_send_skips_nudge_when_no_window
  how: 'defines public function `test_send_skips_nudge_when_no_window` at line 97,
    signature: (project: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_returns_block_once_and_marks_read
  how: 'defines public function `test_read_returns_block_once_and_marks_read` at line
    106, signature: (project: Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_peek_does_not_mark_read
  how: 'defines public function `test_peek_does_not_mark_read` at line 128, signature:
    (project: Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_two_senders_interleave_without_loss
  how: 'defines public function `test_two_senders_interleave_without_loss` at line
    155, signature: (project: Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_two_recipients_independent
  how: 'defines public function `test_two_recipients_independent` at line 168, signature:
    (project: Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_message_has_timestamp
  how: 'defines public function `test_message_has_timestamp` at line 186, signature:
    (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_message_has_from_to_and_text
  how: 'defines public function `test_message_has_from_to_and_text` at line 192, signature:
    (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_empty_inbox
  how: 'defines public function `test_read_empty_inbox` at line 203, signature: (project:
    Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_peek_empty_inbox
  how: 'defines public function `test_peek_empty_inbox` at line 209, signature: (project:
    Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_nonexistent_recipient
  how: 'defines public function `test_read_nonexistent_recipient` at line 218, signature:
    (project: Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_peek_nonexistent_recipient
  how: 'defines public function `test_peek_nonexistent_recipient` at line 224, signature:
    (project: Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_accumulated_reads_after_multiple_sends
  how: 'defines public function `test_accumulated_reads_after_multiple_sends` at line
    233, signature: (project: Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sender_from_flag
  how: 'defines public function `test_sender_from_flag` at line 249, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sender_falls_back_to_env
  how: 'defines public function `test_sender_falls_back_to_env` at line 256, signature:
    (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sender_unknown_when_no_env_no_flag
  how: 'defines public function `test_sender_unknown_when_no_env_no_flag` at line
    261, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sender_env_beats_flag
  how: 'defines public function `test_sender_env_beats_flag` at line 268, signature:
    (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sender_window_name_is_never_an_identity
  how: 'defines public function `test_sender_window_name_is_never_an_identity` at
    line 274, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: comms
  how: 'defines public function `comms` at line 297, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _conf
  how: 'defines private function `_conf` at line 303, signature: (proj: Path, cr:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dm_creates_sorted_file
  how: 'defines public function `test_dm_creates_sorted_file` at line 312, signature:
    (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dm_to_or_from_prime_refused
  how: 'defines public function `test_dm_to_or_from_prime_refused` at line 320, signature:
    (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dm_names_are_sorted
  how: 'defines public function `test_dm_names_are_sorted` at line 332, signature:
    (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dm_writes_block_with_metadata
  how: 'defines public function `test_dm_writes_block_with_metadata` at line 340,
    signature: (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dm_render_shape
  how: 'defines public function `test_dm_render_shape` at line 348, signature: (comms:
    Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dm_read_marks_read_once
  how: 'defines public function `test_dm_read_marks_read_once` at line 358, signature:
    (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dm_peek_does_not_mark_read
  how: 'defines public function `test_dm_peek_does_not_mark_read` at line 368, signature:
    (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dm_since_filter
  how: 'defines public function `test_dm_since_filter` at line 382, signature: (comms:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_room_creates_file_and_appends
  how: 'defines public function `test_room_creates_file_and_appends` at line 396,
    signature: (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_room_render_transcript
  how: 'defines public function `test_room_render_transcript` at line 406, signature:
    (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_room_read_positions_are_per_participant
  how: 'defines public function `test_room_read_positions_are_per_participant` at
    line 417, signature: (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_room_cannot_address_prime
  how: 'defines public function `test_room_cannot_address_prime` at line 428, signature:
    (comms: Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_standing_rooms_constant
  how: defines public function `test_standing_rooms_constant` at line 437
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rooms_lists_rooms_with_unread_counts
  how: 'defines public function `test_rooms_lists_rooms_with_unread_counts` at line
    445, signature: (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_audience_writes_to_prime_inbox
  how: 'defines public function `test_audience_writes_to_prime_inbox` at line 461,
    signature: (project: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_audience_prime_refuses_non_quorum_caller
  how: 'defines public function `test_audience_prime_refuses_non_quorum_caller` at
    line 474, signature: (project: Path, monkeypatch, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_audience_prime_morals_bypasses_quorum_gate
  how: 'defines public function `test_audience_prime_morals_bypasses_quorum_gate`
    at line 489, signature: (project: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_audience_one_per_rotation
  how: 'defines public function `test_audience_one_per_rotation` at line 502, signature:
    (project: Path, monkeypatch, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_audience_morals_bypasses_gate
  how: 'defines public function `test_audience_morals_bypasses_gate` at line 513,
    signature: (project: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_audience_rule_printed_back
  how: 'defines public function `test_audience_rule_printed_back` at line 524, signature:
    (project: Path, monkeypatch, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_vote_posts_structured_line
  how: 'defines public function `test_vote_posts_structured_line` at line 538, signature:
    (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_vote_round_defaults_from_loop
  how: 'defines public function `test_vote_round_defaults_from_loop` at line 552,
    signature: (comms: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_vote_rejects_bad_vision_and_alignment
  how: 'defines public function `test_vote_rejects_bad_vision_and_alignment` at line
    560, signature: (comms: Path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_tally_votes_requires_all_three_visions
  how: 'defines public function `test_tally_votes_requires_all_three_visions` at line
    569, signature: (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_tally_votes_groups_by_vision_last_write_wins
  how: 'defines public function `test_tally_votes_groups_by_vision_last_write_wins`
    at line 579, signature: (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_audience_close_sets_prime_excluded
  how: 'defines public function `test_audience_close_sets_prime_excluded` at line
    597, signature: (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_send_room_single_token_text_is_not_swallowed_by_target
  how: 'defines public function `test_send_room_single_token_text_is_not_swallowed_by_target`
    at line 620, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_send_inbox_target_and_text_both_still_split_correctly
  how: 'defines public function `test_send_inbox_target_and_text_both_still_split_correctly`
    at line 640, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_from_flag_before_subcommand_honored
  how: 'defines public function `test_cli_from_flag_before_subcommand_honored` at
    line 662, signature: (tmp_path, monkeypatch, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_comms_root_before_subcommand_honored
  how: 'defines public function `test_cli_comms_root_before_subcommand_honored` at
    line 680, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_room_all_returns_everything_without_advancing
  how: 'defines public function `test_read_room_all_returns_everything_without_advancing`
    at line 702, signature: (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_dm_all_does_not_advance
  how: 'defines public function `test_read_dm_all_does_not_advance` at line 715, signature:
    (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_peek_all_shows_transcript
  how: 'defines public function `test_peek_all_shows_transcript` at line 724, signature:
    (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _seats_project
  how: 'defines private function `_seats_project` at line 736, signature: (tmp_path:
    Path, rows: list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ask_writes_tagged_dm_to_registered_master
  how: 'defines public function `test_ask_writes_tagged_dm_to_registered_master` at
    line 751, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ask_refuses_non_master_suffix
  how: 'defines public function `test_ask_refuses_non_master_suffix` at line 763,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ask_refuses_unregistered_master_name
  how: 'defines public function `test_ask_refuses_unregistered_master_name` at line
    770, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ask_fails_open_to_suffix_when_registry_absent
  how: 'defines public function `test_ask_fails_open_to_suffix_when_registry_absent`
    at line 779, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_report_refuses_without_matching_ask_from_named_asker
  how: 'defines public function `test_report_refuses_without_matching_ask_from_named_asker`
    at line 790, signature: (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_audience_quorum_writes_tagged_ask_to_request_room
  how: 'defines public function `test_audience_quorum_writes_tagged_ask_to_request_room`
    at line 824, signature: (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_report_room_refuses_without_matching_ask
  how: 'defines public function `test_report_room_refuses_without_matching_ask` at
    line 836, signature: (comms: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_report_quorum_requests_room_refuses_non_quorum_caller
  how: 'defines public function `test_report_quorum_requests_room_refuses_non_quorum_caller`
    at line 863, signature: (comms: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_report_ordinary_room_has_no_quorum_gate
  how: 'defines public function `test_report_ordinary_room_has_no_quorum_gate` at
    line 878, signature: (comms: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_audience_quorum_end_to_end
  how: 'defines public function `test_cli_audience_quorum_end_to_end` at line 892,
    signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_report_requires_exactly_one_of_to_or_room
  how: 'defines public function `test_cli_report_requires_exactly_one_of_to_or_room`
    at line 910, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_escalate_no_to_posts_concern_to_tier3_quorum
  how: 'defines public function `test_escalate_no_to_posts_concern_to_tier3_quorum`
    at line 927, signature: (comms: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_escalate_to_owner_refuses_without_quorum_env
  how: 'defines public function `test_escalate_to_owner_refuses_without_quorum_env`
    at line 933, signature: (comms: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_escalate_to_owner_dms_liaison_never_prime
  how: 'defines public function `test_escalate_to_owner_dms_liaison_never_prime` at
    line 941, signature: (comms: Path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_read_all_flag
  how: 'defines public function `test_cli_read_all_flag` at line 950, signature: (tmp_path,
    monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_comms_root_defaults_to_season_root
  how: 'defines public function `test_comms_root_defaults_to_season_root` at line
    972, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_comms_root_default_ignores_newest_iteration
  how: 'defines public function `test_comms_root_default_ignores_newest_iteration`
    at line 986, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_comms_root_honours_config
  how: 'defines public function `test_comms_root_honours_config` at line 1001, signature:
    (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_comms_root_flag_wins
  how: 'defines public function `test_comms_root_flag_wins` at line 1010, signature:
    (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_comms_root_resolves_to_main_from_a_linked_worktree
  how: 'defines public function `test_comms_root_resolves_to_main_from_a_linked_worktree`
    at line 1023, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: proj / ".agi" / "config.json"
  how: '`(proj / ".agi" / "config.json").write_text(_j.dumps(cfg))` at line 307'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 627'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 647'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 667'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 685'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 741'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nodes / ".geometry" / "seats.md"
  how: '`(nodes / ".geometry" / "seats.md").write_text( "---\nid: config:seats\ntype:
    config\nseats:\n" + seats_yaml + "\n---\n<!-- BODY:BEGIN -->\n")` at line 745'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 897'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 913'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 953'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 977'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "nodes" / ".geometry" / "ladder.md"
  how: '`(root / ".agi" / "nodes" / ".geometry" / "ladder.md").write_text( "---\ncurrent_season:
    7\n---\n")` at line 979'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 990'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "nodes" / ".geometry" / "ladder.md"
  how: '`(root / ".agi" / "nodes" / ".geometry" / "ladder.md").write_text( "---\ncurrent_season:
    2\n---\n")` at line 992'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage", "locations": {"comms_root": "/dev/shm/agi"}}))` at line 1004'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps( {"locations": {"comms_root":
    "/dev/shm/agi"}}))` at line 1013'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / ".agi" / "config.json"
  how: '`(repo / ".agi" / "config.json").write_text(json.dumps( {"metric_primary":
    "outcome_coverage"}))` at line 1035'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / ".agi" / "nodes" / ".geometry" / "ladder.md"
  how: '`(repo / ".agi" / "nodes" / ".geometry" / "ladder.md").write_text( "---\ncurrent_season:
    5\n---\n")` at line 1037'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 627'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 647'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 667'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 685'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 741'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 897'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 913'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 953'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 977'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 990'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage", "locations": {"comms_root":
    "/dev/shm/agi"}})` at line 1004'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"locations": {"comms_root": "/dev/shm/agi"}})` at line 1013'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"metric_primary": "outcome_coverage"})` at line 1035'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
