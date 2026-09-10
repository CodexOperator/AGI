---
id: build:bin-rotate
mint_id: 37e33a765afd451797fcceff54c3157b
type: build
parents:
  - mvp:bin-modules
build_kind: code
confidence: 1.0
edited_by: a00-a62d7cef
origin: build-scan
payload_ref: extensions/agi/bin/rotate.py
tags:
  - build
  - code
  - g2.1
thought_session: sanctuary-director-genVI
title: "Build: extensions/agi/bin/rotate.py"
---
`extensions/agi/bin/rotate.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:bin-modules`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/rotate.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 45'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 47'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 48'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 49'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 50'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shlex
  how: '`import shlex` at line 51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shutil
  how: '`import shutil` at line 52'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 53'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tempfile
  how: '`import tempfile` at line 55'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 56'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: urllib.error
  how: '`import urllib.error` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: urllib.request
  how: '`import urllib.request` at line 58'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: datetime.datetime
  how: '`from datetime import datetime` at line 59'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 60'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: types.SimpleNamespace
  how: '`from types import SimpleNamespace` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 65'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.persistence.frontmatter
  how: '`from graph_core.persistence import frontmatter` at line 66'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`open(path, encoding="utf-8", errors="replace")` at line 387 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`open(path, encoding="utf-8", errors="replace")` at line 413 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(path.read_text(encoding="utf-8"))` at line 507'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hp
  how: '`hp.read_text(encoding="utf-8", errors="replace")` at line 1716'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 507'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Path(prompt_file)
  how: '`Path(prompt_file).read_text(encoding="utf-8")` at line 711'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: env_path
  how: '`env_path.read_text(encoding="utf-8")` at line 770'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pin
  how: '`pin.read_text(encoding="utf-8")` at line 297'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(line)` at line 393'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(raw)` at line 423'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(args.settings)` at line 1155'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(args.settings)` at line 1260'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(args.settings)` at line 2218'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(resp.read().decode("utf-8"))` at line 783'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`open(p, encoding="utf-8", errors="replace")` at line 1205 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text(encoding="utf-8")` at line 2055'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(p.read_text())` at line 1917'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text(encoding="utf-8")` at line 588'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 1917'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text(encoding="utf-8")` at line 2069'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _normalize_settings
  how: 'defines private function `_normalize_settings` at line 145, signature: (val)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_project_root
  how: defines public function `find_project_root` at line 163
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_ladder_field
  how: 'defines public function `load_ladder_field` at line 169, signature: (root:
    Path, field: str, default)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_newest_cc_transcript
  how: 'defines public function `find_newest_cc_transcript` at line 194, signature:
    (slug: str=CC_PROJECT_SLUG)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _derive_cc_slug
  how: 'defines private function `_derive_cc_slug` at line 216, signature: (cwd: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sessions_dir
  how: 'defines private function `_sessions_dir` at line 227, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_pin_log
  how: 'defines public function `find_pin_log` at line 258, signature: (root: Path,
    seat: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_pin_record
  how: 'defines private function `_parse_pin_record` at line 286, signature: (pin:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_pin_target
  how: 'defines private function `_read_pin_target` at line 312, signature: (pin:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_transcript
  how: 'defines public function `resolve_transcript` at line 321, signature: (*, root:
    Path, session_log: str | None=None, env=None, seat: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_usage_from_cc_transcript
  how: 'defines public function `parse_usage_from_cc_transcript` at line 380, signature:
    (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_usage_from_rc_log
  how: 'defines public function `parse_usage_from_rc_log` at line 406, signature:
    (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: calculate_fraction
  how: 'defines public function `calculate_fraction` at line 431, signature: (usage:
    dict, context_tokens: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: usage_source_name
  how: 'defines public function `usage_source_name` at line 443, signature: (source:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _check_branch_guard
  how: 'defines private function `_check_branch_guard` at line 459, signature: (root:
    Path | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _config_json
  how: 'defines private function `_config_json` at line 501, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ladder_roles_table
  how: 'defines private function `_ladder_roles_table` at line 512, signature: (root:
    Path | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_role
  how: 'defines public function `load_role` at line 529, signature: (root: Path |
    None, tier: str, field: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_ultracode
  how: 'defines private function `_is_ultracode` at line 565, signature: (settings)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _existing_windows
  how: 'defines private function `_existing_windows` at line 579, signature: (tmux_session:
    str, window_path: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _roman_value
  how: 'defines private function `_roman_value` at line 612, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_roman
  how: 'defines private function `_is_roman` at line 624, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _int_to_roman
  how: 'defines private function `_int_to_roman` at line 632, signature: (n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _split_roman_suffix
  how: 'defines private function `_split_roman_suffix` at line 642, signature: (w:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _derive_successor_name
  how: 'defines private function `_derive_successor_name` at line 659, signature:
    (windows: list[str], prefix: str=''belam'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _build_claude_command
  how: 'defines private function `_build_claude_command` at line 687, signature: (name:
    str, prompt_text: str, debug_file: str, model=None, effort=None, settings=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _successor_command
  how: 'defines private function `_successor_command` at line 706, signature: (*,
    name: str, tier: str, prompt_file: str, model, effort, settings, debug_file: str,
    extra: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _assembled_successor_command
  how: 'defines private function `_assembled_successor_command` at line 725, signature:
    (*, name: str, tier: str, model, effort, settings, debug_file: str, extra: str='''',
    dispatch_py: str=''extensions/agi/bin/dispatch.py'', cli_py: str=''extensions/agi/bin/cli.py'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _openrouter_key
  how: 'defines private function `_openrouter_key` at line 757, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _openrouter_get
  how: 'defines private function `_openrouter_get` at line 776, signature: (url: str,
    key: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fresh_spend_status
  how: 'defines public function `fresh_spend_status` at line 788, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_meter
  how: 'defines public function `cmd_meter` at line 823, signature: (args: argparse.Namespace,
    root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _shell_cmd
  how: 'defines private function `_shell_cmd` at line 964, signature: (claude_cmd:
    list[str], settings)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _launch_window
  how: 'defines private function `_launch_window` at line 990, signature: (tmux_session:
    str, name: str, shell_cmd: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: spawn_window
  how: 'defines public function `spawn_window` at line 1042, signature: (*, name:
    str, tier: str, prompt_file: str, model=None, effort=None, settings=None, tmux_session:
    str=DEFAULT_TMUX_SESSION, window_path: str | None=None, root: Path | None=None,
    dry_run: bool=False, debug_file: str | None=None, extra: str=''''...[truncated,
    273 chars total])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_spawn
  how: 'defines public function `cmd_spawn` at line 1135, signature: (args: argparse.Namespace,
    root: Path | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_log_noise
  how: 'defines private function `_is_log_noise` at line 1171, signature: (line: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_first_reply
  how: 'defines private function `_read_first_reply` at line 1188, signature: (path:
    str | Path, timeout: int=120, start_offset: int=0)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_loop
  how: 'defines public function `cmd_loop` at line 1219, signature: (args: argparse.Namespace,
    root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 1337, signature: (args: argparse.Namespace,
    root: Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_seats
  how: 'defines private function `_load_seats` at line 1417, signature: (root: Path
    | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_seat
  how: 'defines private function `_find_seat` at line 1435, signature: (root: Path
    | None, name: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _seats_that_launch
  how: 'defines private function `_seats_that_launch` at line 1453, signature: (rows:
    list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_seats_launch
  how: 'defines public function `cmd_seats_launch` at line 1464, signature: (args:
    argparse.Namespace, root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: partition_tiles
  how: 'defines public function `partition_tiles` at line 1525, signature: (n: int,
    x: int, y: int, width: int, height: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_tile
  how: 'defines public function `cmd_tile` at line 1550, signature: (args: argparse.Namespace,
    root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _screen_tool
  how: defines private function `_screen_tool` at line 1590
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _wm_tool_argv
  how: 'defines private function `_wm_tool_argv` at line 1598, signature: (tool: str,
    name: str, rect: tuple)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _place_windows
  how: 'defines private function `_place_windows` at line 1616, signature: (rects:
    dict, tool: str | None, run=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _live_window_names
  how: 'defines private function `_live_window_names` at line 1649, signature: (root:
    Path | None, window_path: str | None, tmux_session: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _cmd_tile_apply
  how: 'defines private function `_cmd_tile_apply` at line 1666, signature: (args:
    argparse.Namespace, root: Path, w: int, h: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _seat_hands
  how: 'defines private function `_seat_hands` at line 1699, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_generation
  how: 'defines private function `_read_generation` at line 1708, signature: (root:
    Path, name: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_handoff
  how: 'defines private function `_write_handoff` at line 1727, signature: (root:
    Path, name: str, generation: int, predecessor_session: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rotations_dir
  how: 'defines private function `_rotations_dir` at line 1751, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _observed_windows
  how: 'defines private function `_observed_windows` at line 1761, signature: (tmux_session:
    str, window_path: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_rotation_record
  how: 'defines private function `_write_rotation_record` at line 1779, signature:
    (root: Path, record: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rotate_self_record
  how: 'defines private function `_rotate_self_record` at line 1795, signature: (*,
    seat: str, result: str, refusal: str | None=None, gen_before: int | None=None,
    gen_after: int | None=None, succ=None, pred=None, readback_log=None, cursor_offset:
    int | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _loop_record
  how: 'defines private function `_loop_record` at line 1842, signature: (*, name:
    str, result: str, refusal: str | None=None, succ=None, readback_log=None, reply_decision:
    str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _seq_file
  how: 'defines private function `_seq_file` at line 1903, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _current_sequence
  how: 'defines private function `_current_sequence` at line 1907, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _next_sequence
  how: 'defines private function `_next_sequence` at line 1923, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _compose_announcement
  how: 'defines private function `_compose_announcement` at line 1937, signature:
    (*, seat, successor, gen_before, gen_after, trigger, handoff_path, in_flight,
    seq=0)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _derive_receivers
  how: 'defines private function `_derive_receivers` at line 1953, signature: (root:
    Path, *, seat: str, live_names: list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _announce_rotation
  how: 'defines private function `_announce_rotation` at line 1975, signature: (*,
    root: Path, croot, seat: str, successor: str, gen_before, gen_after, trigger:
    str, handoff_path: str, in_flight: str, live_names: list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_sequence
  how: 'defines public function `cmd_sequence` at line 2019, signature: (args: argparse.Namespace,
    root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rename_own_window
  how: 'defines private function `_rename_own_window` at line 2029, signature: (seat:
    str, new_name: str, tmux_session: str, window_path: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _replace_window_name
  how: 'defines private function `_replace_window_name` at line 2049, signature: (window_path:
    str, old: str, new: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _kill_window
  how: 'defines private function `_kill_window` at line 2060, signature: (name: str,
    tmux_session: str, window_path: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _seat_fraction
  how: 'defines private function `_seat_fraction` at line 2082, signature: (root:
    Path, row: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_alarms
  how: 'defines public function `cmd_alarms` at line 2110, signature: (args: argparse.Namespace,
    root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_rotate_self
  how: 'defines public function `cmd_rotate_self` at line 2157, signature: (args:
    argparse.Namespace, root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 2322, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hp
  how: '`hp.write_text( f"seat: {name}\n" f"generation: {generation}\n" f"rotated_at:
    {datetime.utcnow().isoformat()}Z\n" f"predecessor_session: {predecessor_session}\n",
    encoding="utf-8", )` at line 1734'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")` at
    line 1791'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _seq_file(root)
  how: '`_seq_file(root).write_text(json.dumps({"sequence": nxt}) + "\n", encoding="utf-8")`
    at line 1932'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("\n".join(out) + "\n", encoding="utf-8")` at line 2057'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(new + "\n", encoding="utf-8")` at line 2053'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(settings)` at line 701'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pinp
  how: '`pinp.write_text(f"{cur_gen}\t{log_path}\n", encoding="utf-8")` at line 900'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pinp
  how: '`pinp.write_text(str(log_path) + "\n", encoding="utf-8")` at line 902'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(record, indent=2)` at line 1791'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"sequence": nxt})` at line 1932'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("\n".join(lines) + "\n", encoding="utf-8")` at line 2071'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 77 `print()` call(s) at line(s) [177, 184, 189, 828, 841, 860, 870, 881, 910,
    928, 932, 951, 1027, 1031, 1036, 1071, 1108, 1120, 1126, 1141, 1163, 1164, 1229,
    1234, 1241, 1269, 1288, 1304, 1323, 1329, 1330, 1348, 1363, 1372, 1375, 1379,
    1386, 1408, 1410, 1478, 1505, 1516, 1519, 1563, 1569, 1575, 1578, 1641, 1645,
    1679, 1689, 1692, 1695, 1998, 2002, 2011, 2014, 2025, 2131, 2135, 2142, 2145,
    2170, 2174, 2187, 2202, 2208, 2227, 2230, 2231, 2232, 2252, 2265, 2284, 2313,
    2315, 2547]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L4.112 kid1 (A)(C)(E) on top of L4.110 kid1: (A) moved _resolve_template to the TOP of cmd_rotate_self before the started record / handoff / rename, so an absent rotations.md refuses before any side effect; (C) spawn consumes tmpl.brief_file as the successor prompt ({seat} substituted) when --prompt-file is absent, steps_reached markers derive from tmpl.steps via _rs_mark, telemetry surfaced to the operator (bootstrap write is 0b); (E) cmd_ack held callable but deprecated in --help. (B) shipped briefs/rotations.geometry.md: director brief is .agi/sessions/quorum/{seat}.md, prime stays static, parent/kid dropped. Handover (D) is kid 2; handover wall + ack read-back untouched.
<!-- THOUGHT:END -->