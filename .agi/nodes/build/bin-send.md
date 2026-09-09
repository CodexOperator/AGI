---
build_kind: code
confidence: 1.0
id: "build:bin-send"
mint_id: 01dcd1503764446e91baa07990399551
origin: build-scan
parents:
  - mvp:bin-modules
payload_ref: extensions/agi/bin/send.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/send.py"
type: build
---

`extensions/agi/bin/send.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:bin-modules`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/send.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 43'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 45'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 46'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 47'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 48'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 49'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: datetime.datetime
  how: '`from datetime import datetime` at line 50'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: datetime.timezone
  how: '`from datetime import timezone` at line 50'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: spawn_gate
  how: '`import spawn_gate` at line 55'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: inbox
  how: '`inbox.read_text()` at line 422'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 271'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: inbox
  how: '`inbox.read_text()` at line 459'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(sp.read_text())` at line 295'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ep.read_text())` at line 846'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(sp.read_text())` at line 856'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ep.read_text())` at line 875'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sp
  how: '`sp.read_text()` at line 295'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(state_file.read_text())` at line 713'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ep
  how: '`ep.read_text()` at line 846'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sp
  how: '`sp.read_text()` at line 856'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ep
  how: '`ep.read_text()` at line 875'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: state_file
  how: '`state_file.read_text()` at line 713'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _project_root
  how: defines private function `_project_root` at line 108
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _inbox_dir
  how: 'defines private function `_inbox_dir` at line 117, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _inbox_path
  how: 'defines private function `_inbox_path` at line 122, signature: (root: Path,
    recipient: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _now
  how: defines private function `_now` at line 127
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _quorum_caller
  how: defines private function `_quorum_caller` at line 131
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _detect_sender
  how: 'defines private function `_detect_sender` at line 140, signature: (from_flag:
    str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _main_graph_root
  how: 'defines private function `_main_graph_root` at line 163, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _default_comms_root
  how: 'defines private function `_default_comms_root` at line 179, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: comms_root
  how: 'defines public function `comms_root` at line 198, signature: (root: Path,
    override: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _dm_pair
  how: 'defines private function `_dm_pair` at line 217, signature: (a: str, b: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _room_path
  how: 'defines private function `_room_path` at line 223, signature: (croot: Path,
    room: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _dm_path
  how: 'defines private function `_dm_path` at line 227, signature: (croot: Path,
    a: str, b: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _block
  how: 'defines private function `_block` at line 232, signature: (ts: str, from_id:
    str, to: str, text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_blocks
  how: 'defines private function `_parse_blocks` at line 236, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_conv
  how: 'defines private function `_read_conv` at line 268, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_transcript
  how: 'defines public function `render_transcript` at line 274, signature: (blocks:
    list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_state
  how: 'defines private function `_load_state` at line 291, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _save_state
  how: 'defines private function `_save_state` at line 301, signature: (path: Path,
    state: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _past
  how: 'defines private function `_past` at line 305, signature: (blocks: list[dict],
    since: str | None, read_count: int, participant: str, path: Path, commit: bool,
    all_: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _after_or_eq
  how: 'defines private function `_after_or_eq` at line 333, signature: (a: str, b:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _norm
  how: 'defines private function `_norm` at line 341, signature: (ts: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _nudge_window
  how: 'defines private function `_nudge_window` at line 352, signature: (tmux_session:
    str | None, window: str, text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: send
  how: 'defines public function `send` at line 392, signature: (root: Path, to: str,
    text: str, sender: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scan_messages
  how: 'defines private function `_scan_messages` at line 411, signature: (inbox:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read
  how: 'defines public function `read` at line 441, signature: (root: Path, me: str,
    sender: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: peek
  how: 'defines public function `peek` at line 469, signature: (root: Path, me: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: send_dm
  how: 'defines public function `send_dm` at line 487, signature: (croot: Path, me:
    str, other: str, text: str, sender: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: send_room
  how: 'defines public function `send_room` at line 511, signature: (croot: Path,
    room: str, text: str, sender: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _conv_blocks
  how: 'defines private function `_conv_blocks` at line 524, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ask
  how: 'defines public function `ask` at line 531, signature: (croot: Path, root:
    Path, me: str, to: str, text: str, sender: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: report
  how: 'defines public function `report` at line 550, signature: (croot: Path, me:
    str, asker: str | None, ref: str, text: str, sender: str | None, room: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: escalate
  how: 'defines public function `escalate` at line 596, signature: (croot: Path, text:
    str, to: str | None, concern: str, sender: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_dm
  how: 'defines public function `read_dm` at line 615, signature: (croot: Path, me:
    str, other: str, since: str | None, sender: str | None, all_: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: peek_dm
  how: 'defines public function `peek_dm` at line 628, signature: (croot: Path, me:
    str, other: str, since: str | None, all_: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_room
  how: 'defines public function `read_room` at line 638, signature: (croot: Path,
    room: str, participant: str, since: str | None, sender: str | None, all_: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: peek_room
  how: 'defines public function `peek_room` at line 648, signature: (croot: Path,
    room: str, participant: str, since: str | None, all_: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: rooms
  how: 'defines public function `rooms` at line 658, signature: (croot: Path, me:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: audience_prime
  how: 'defines public function `audience_prime` at line 689, signature: (croot: Path,
    root: Path, reason: str, sender: str | None, morals: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: audience_quorum
  how: 'defines public function `audience_quorum` at line 734, signature: (croot:
    Path, reason: str, sender: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: vote
  how: 'defines public function `vote` at line 757, signature: (croot: Path, room:
    str, target: str, vision: str, alignment: str, sender: str | None, morals: bool,
    reason: str, round_: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_vote
  how: 'defines private function `_parse_vote` at line 782, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tally_votes
  how: 'defines public function `tally_votes` at line 799, signature: (croot: Path,
    room: str, target: str, round_: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: audience_close
  how: 'defines public function `audience_close` at line 833, signature: (croot: Path,
    round_: str, decision: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prime_excluded
  how: 'defines public function `prime_excluded` at line 868, signature: (croot: Path,
    round_: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 888, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Path(str(path) + STATE_SUFFIX)
  how: '`Path(str(path) + STATE_SUFFIX).write_text(json.dumps(state))` at line 302'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ep
  how: '`ep.write_text(json.dumps(exited))` at line 850'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sp
  how: '`sp.write_text(json.dumps(state))` at line 863'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(state)` at line 302'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: inbox
  how: '`open(inbox, "a")` at line 401 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: inbox
  how: '`inbox.write_text(content + "\n" + READ_MARKER)` at line 466'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`open(path, "a")` at line 503 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`open(path, "a")` at line 519 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: state_file
  how: '`state_file.write_text(json.dumps(state))` at line 725'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(exited)` at line 850'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(state)` at line 863'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(state)` at line 725'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 53 `print()` call(s) at line(s) [112, 408, 447, 453, 454, 475, 480, 481, 496,
    514, 541, 545, 568, 579, 591, 606, 701, 718, 729, 730, 748, 749, 765, 769, 773,
    820, 864, 877, 881, 1028, 1031, 1036, 1039, 1044, 1050, 1061, 1065, 1068, 1079,
    1083, 1086, 1096, 1099, 1105, 1113, 1121, 1132, 1134, 1141, 1144, 1147, 1154,
    1156]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
