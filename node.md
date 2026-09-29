---
id: build:bin-heal
mint_id: 2405ecff7d3a4584af5cd7ec815bc679
type: build
parents:
  - goal:g7.16.1.2.1
  - idea:engine-heal
build_kind: code
confidence: 1.0
edited_by: director-general-5
origin: build-scan
payload_ref: extensions/agi/bin/heal.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: reaper-triage-2026-09-25
title: "Build: extensions/agi/bin/heal.py"
---
`extensions/agi/bin/heal.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-heal`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/heal.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shlex
  how: '`import shlex` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: signal
  how: '`import signal` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: uuid
  how: '`import uuid` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 42'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dispatch.pi_model_args
  how: '`from dispatch import pi_model_args` at line 43'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dispatch.scrubbed_env
  how: '`from dispatch import scrubbed_env as _scrubbed_env` at line 43'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest_path.read_text())` at line 83'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.read_text()` at line 83'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap_file.read_text())` at line 96'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`log_path.read_bytes()` at line 160'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap_file
  how: '`ap_file.read_text()` at line 96'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _pi_model_args
  how: 'defines private function `_pi_model_args` at line 46, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 64
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pid_alive
  how: 'defines private function `_pid_alive` at line 132, signature: (pid: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _heal
  how: 'defines private function `_heal` at line 140, signature: (root: Path, iter_n:
    int, agent_id: str, rec: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: healer_ctx
  how: '`healer_ctx.write_text( f"""# HEALER for hung agent {agent_id} (iter {iter_n})
    The original agent timed out. Diagnose what blocked it and patch. ## Original
    Agent Record ```json {json.dumps(rec, indent=2)} ``` ## Last 4 KiB of Agent Output
    `...[truncated, 1264 chars total]` at line 170'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sess_dir / "agent.json"
  how: '`(sess_dir / "agent.json").write_text(json.dumps(rec, indent=2))` at line
    255'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.write_text(json.dumps(manifest, indent=2))` at line 122'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: healer_log
  how: '`open(healer_log, "wb")` at line 235 (mode=''wb'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 255'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(manifest, indent=2)` at line 122'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 177'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap_file
  how: '`ap_file.write_text(json.dumps(rec, indent=2))` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 7 `print()` call(s) at line(s) [59, 81, 120, 124, 128, 142, 256]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-5 00:1xZ 09-30, goal:g7.16.1.7.1.1 round (a), commit 803309d2c. (1) SAID: B1 of the council placement (alive 23:4xZ): heal._launch_recovered goes through the one launcher. (2) DOES: _launch_recovered is now a thin caller of rotate.launch_in_window with inline_max 0 (a recovery never hands tmux its prompt inline) and timeout_ok False (a timeout is not a launch; the next pass retries); its own launch-file copy and _unlink_launch_file are gone. (3) NEAR MISS: the unified launcher first called ensure_tmux_session before writing the file, so an unwritable file still reached tmux; the file is now written first. (4) The launch interpreter moved from sh to bash with a shebang; the three pinned tests were updated to the unified form, not weakened (the orphan glob follows the new file prefix).
<!-- THOUGHT:END -->
