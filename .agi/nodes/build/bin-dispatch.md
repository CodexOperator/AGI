---
id: build:bin-dispatch
mint_id: b3cae0bec6424ea4ab04beeb44ca70aa
type: build
parents:
  - idea:engine-dispatch
build_kind: code
confidence: 1.0
edited_by: director
origin: build-scan
payload_ref: extensions/agi/bin/dispatch.py
tags:
  - build
  - code
  - g2.1
thought_session: agi-master-2026-09-06
title: "Build: extensions/agi/bin/dispatch.py"
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
- name: fcntl
  how: '`import fcntl` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: random
  how: '`import random` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shlex
  how: '`import shlex` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tempfile
  how: '`import tempfile` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: uuid
  how: '`import uuid` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: contextlib.contextmanager
  how: '`from contextlib import contextmanager` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: adapters
  how: '`import adapters` at line 43'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 44'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_writer
  how: '`import node_writer` at line 45'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 254'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 254'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 566'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 692'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest_path.read_text())` at line 307'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest_path.read_text())` at line 491'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 566'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 692'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest_path.read_text())` at line 175'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.read_text()` at line 307'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.read_text()` at line 491'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(agent_json_path.read_text())` at line 503'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ccf
  how: '`ccf.read_text()` at line 558'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: closed_chains_file
  how: '`closed_chains_file.read_text()` at line 684'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.read_text()` at line 175'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: agent_json_path
  how: '`agent_json_path.read_text()` at line 503'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: scrubbed_env
  how: defines public function `scrubbed_env` at line 71
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: zoom_command
  how: 'defines public function `zoom_command` at line 87, signature: (root: Path,
    iter_n: int, agent_id: str, level: str, target: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pi_model_args
  how: 'defines public function `pi_model_args` at line 110, signature: (cfg: dict,
    tier: str=''kid'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _manifest_lock
  how: 'defines private function `_manifest_lock` at line 127, signature: (iter_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _merge_manifest
  how: 'defines private function `_merge_manifest` at line 159, signature: (iter_dir:
    Path, base: dict, new_records: list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 208
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _reaper_phase
  how: 'defines private function `_reaper_phase` at line 462, signature: (root: Path,
    iter_dir: Path, adapter: object, timeout_s: int=600, max_wait_s: int=30)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _research_pipeline_targets
  how: 'defines private function `_research_pipeline_targets` at line 532, signature:
    (root: Path, n: int, iter_dir: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _explicit_targets
  how: 'defines private function `_explicit_targets` at line 631, signature: (target:
    str, level: str | None, strategy: str, n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pick_targets
  how: 'defines private function `_pick_targets` at line 656, signature: (root: Path,
    n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_type_for
  how: 'defines private function `_node_type_for` at line 814, signature: (level:
    str, target: str | None, role: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scaffold_node_for_agent
  how: 'defines private function `_scaffold_node_for_agent` at line 850, signature:
    (root: Path, iter_n: int, agent_id: str, level: str, target: str | None, role:
    str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _build_pi_args
  how: 'defines private function `_build_pi_args` at line 881, signature: (cfg: dict,
    context_file: str, agent_id: str, iter_n: int, sess_dir: Path, scaffold_info:
    dict | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sess_dir / "agent.json"
  how: '`(sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))`
    at line 424'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_file
  how: '`open(log_file, "wb")` at line 395 (mode=''wb'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(agent_record, indent=2)` at line 424'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.write_text(json.dumps(manifest, indent=2))` at line 524'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dump
  how: '`json.dump(merged, fh, indent=2)` at line 200'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: agent_json_path
  how: '`agent_json_path.write_text(json.dumps(rec, indent=2))` at line 518'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(manifest, indent=2)` at line 524'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 518'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 16 `print()` call(s) at line(s) [179, 252, 264, 277, 282, 286, 311, 343, 358,
    364, 391, 433, 445, 521, 529, 875]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-06 director hand fix: L2.06 kid (hypothesis:l2w2-writer-stamps) added a call to spawn_gate.read_ladder_season in main() without importing spawn_gate; every dispatch died with NameError at line 325 and the suite stayed green because nothing calls main(). One import line added. The class of bug goes to goal:g15 as hypothesis:l2-bin-help-smoke.
<!-- THOUGHT:END -->
