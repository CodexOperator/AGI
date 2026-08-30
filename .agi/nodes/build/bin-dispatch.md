---
build_kind: code
confidence: 1.0
id: "build:bin-dispatch"
mint_id: b3cae0bec6424ea4ab04beeb44ca70aa
origin: build-scan
parents:
  - idea:engine-dispatch
payload_ref: extensions/agi/bin/dispatch.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/dispatch.py"
type: build
---

`extensions/agi/bin/dispatch.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-dispatch`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/dispatch.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: random
  how: '`import random` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shlex
  how: '`import shlex` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: uuid
  how: '`import uuid` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 40'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_writer
  how: '`import node_writer` at line 41'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 93'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 93'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 222'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 323'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 222'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 323'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ccf
  how: '`ccf.read_text()` at line 214'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: closed_chains_file
  how: '`closed_chains_file.read_text()` at line 315'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _scrubbed_env
  how: defines private function `_scrubbed_env` at line 67
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 73
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _research_pipeline_targets
  how: 'defines private function `_research_pipeline_targets` at line 188, signature:
    (root: Path, n: int, iter_dir: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pick_targets
  how: 'defines private function `_pick_targets` at line 287, signature: (root: Path,
    n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_type_for
  how: 'defines private function `_node_type_for` at line 445, signature: (level:
    str, target: str | None, role: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scaffold_node_for_agent
  how: 'defines private function `_scaffold_node_for_agent` at line 481, signature:
    (root: Path, iter_n: int, agent_id: str, level: str, target: str | None, role:
    str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _build_pi_args
  how: 'defines private function `_build_pi_args` at line 512, signature: (cfg: dict,
    context_file: str, agent_id: str, iter_n: int, sess_dir: Path, scaffold_info:
    dict | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_dir / "manifest.json"
  how: '`(iter_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))`
    at line 183'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sess_dir / "agent.json"
  how: '`(sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))`
    at line 179'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(manifest, indent=2)` at line 183'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_file
  how: '`open(log_file, "wb")` at line 152 (mode=''wb'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(agent_record, indent=2)` at line 179'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 6 `print()` call(s) at line(s) [91, 106, 147, 181, 184, 506]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
