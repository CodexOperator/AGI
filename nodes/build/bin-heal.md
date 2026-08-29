---
build_kind: code
confidence: 1.0
id: "build:bin-heal"
mint_id: 2a6641b3f93f4da8992e8446194153e9
origin: build-scan
payload_ref: extensions/agi/bin/heal.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/heal.py"
type: build
---

`extensions/agi/bin/heal.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

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
- name: json.loads
  how: '`json.loads(manifest_path.read_text())` at line 52'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.read_text()` at line 52'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap_file.read_text())` at line 65'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`log_path.read_bytes()` at line 129'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap_file
  how: '`ap_file.read_text()` at line 65'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: main
  how: defines public function `main` at line 38
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pid_alive
  how: 'defines private function `_pid_alive` at line 101, signature: (pid: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _heal
  how: 'defines private function `_heal` at line 109, signature: (root: Path, iter_n:
    int, agent_id: str, rec: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: healer_ctx
  how: '`healer_ctx.write_text( f"""# HEALER for hung agent {agent_id} (iter {iter_n})
    The original agent timed out. Diagnose what blocked it and patch. ## Original
    Agent Record ```json {json.dumps(rec, indent=2)} ``` ## Last 4 KiB of Agent Output
    `...[truncated, 805 chars total]` at line 139'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sess_dir / "agent.json"
  how: '`(sess_dir / "agent.json").write_text(json.dumps(rec, indent=2))` at line
    196'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.write_text(json.dumps(manifest, indent=2))` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: healer_log
  how: '`open(healer_log, "wb")` at line 177 (mode=''wb'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 196'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(manifest, indent=2)` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 146'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap_file
  how: '`ap_file.write_text(json.dumps(rec, indent=2))` at line 86'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 86'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 6 `print()` call(s) at line(s) [50, 89, 93, 97, 111, 197]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
