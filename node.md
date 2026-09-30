---
id: build:bin-verify-unified
mint_id: 8e9e1ffd6c214a768cc3b6cc0cdc6673
type: build
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/bin/verify_unified.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/verify_unified.py"
---
`extensions/agi/bin/verify_unified.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/verify_unified.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 60'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 62'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hashlib
  how: '`import hashlib` at line 63'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 64'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 65'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 66'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 67'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Any
  how: '`from typing import Any` at line 68'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Callable
  how: '`from typing import Callable` at line 68'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 71'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 73'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8", errors="replace")` at line 146'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 155'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`open(path, "rb")` at line 163 (mode=''rb'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(config_path.read_text(encoding="utf-8"))` at line 440'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: config_path
  how: '`config_path.read_text(encoding="utf-8")` at line 440'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: CheckResult
  how: defines public class `CheckResult` at line 81
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git
  how: 'defines private function `_git` at line 100, signature: (repo: Path, *args:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rev_parse
  how: 'defines private function `_rev_parse` at line 114, signature: (repo: Path,
    rev: str=''HEAD'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _grid_refs
  how: 'defines private function `_grid_refs` at line 123, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_frontmatter
  how: 'defines private function `_read_frontmatter` at line 139, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sha256_file
  how: 'defines private function `_sha256_file` at line 161, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_files
  how: 'defines private function `_node_files` at line 169, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_hash_map
  how: 'defines private function `_node_hash_map` at line 181, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_node_count
  how: 'defines public function `check_node_count` at line 191, signature: (before:
    Path, after: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_node_bytes
  how: 'defines public function `check_node_bytes` at line 203, signature: (before:
    Path, after: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_grid_refs
  how: 'defines public function `check_grid_refs` at line 230, signature: (before:
    Path, after: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_histories
  how: 'defines public function `check_histories` at line 258, signature: (before:
    Path, after: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_resolver
  how: 'defines public function `check_resolver` at line 313, signature: (after: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_goals_location
  how: 'defines public function `check_goals_location` at line 354, signature: (after:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _count_payload_refs
  how: 'defines private function `_count_payload_refs` at line 369, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_payload_refs
  how: 'defines public function `check_payload_refs` at line 379, signature: (before:
    Path, after: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_config
  how: 'defines public function `check_config` at line 431, signature: (after: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _safe
  how: 'defines private function `_safe` at line 470, signature: (name: str, fn: Callable[...,
    CheckResult], *args: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run_all
  how: 'defines public function `run_all` at line 483, signature: (before: Path, after:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 494, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({ "ok": ok, "before": str(before.resolve()), "after": str(after.resolve()),
    "checks": [r.to_dict() for r in results], }, indent=2)` at line 523'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 7 `print()` call(s) at line(s) [511, 515, 523, 532, 535, 536, 537]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.