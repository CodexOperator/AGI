---
confidence: 1.0
id: "level3:bin-level3"
origin: level3-scan
parents:
  - idea:engine-level3
payload_ref: extensions/agi/bin/level3.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/bin/level3.py"
type: level3
---

`extensions/agi/bin/level3.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-level3`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/level3.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 68'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 70'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ast
  how: '`import ast` at line 71'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 72'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 73'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 76'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 77'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: abs_path
  how: '`abs_path.read_text(encoding=''utf-8'')` at line 408'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _set_project_root
  how: 'defines private function `_set_project_root` at line 101, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git_ls_files
  how: 'defines public function `git_ls_files` at line 137, signature: (engine_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: discover_files
  how: 'defines public function `discover_files` at line 153, signature: (engine_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _cap
  how: 'defines private function `_cap` at line 202, signature: (s: str | None, limit:
    int=_CAP_LEN)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _unparse_safe
  how: 'defines private function `_unparse_safe` at line 217, signature: (node: ast.AST
    | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scan_imports
  how: 'defines private function `_scan_imports` at line 226, signature: (tree: ast.Module)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scan_top_level_defs
  how: 'defines private function `_scan_top_level_defs` at line 247, signature: (tree:
    ast.Module)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scan_io_calls
  how: 'defines private function `_scan_io_calls` at line 268, signature: (tree: ast.Module)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scan_cli_and_env
  how: 'defines private function `_scan_cli_and_env` at line 332, signature: (tree:
    ast.Module)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scan_stdout
  how: 'defines private function `_scan_stdout` at line 376, signature: (tree: ast.Module)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: analyze_file
  how: 'defines public function `analyze_file` at line 387, signature: (abs_path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_census_units
  how: 'defines public function `load_census_units` at line 430, signature: (existing:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_parent
  how: 'defines public function `find_parent` at line 453, signature: (rel_path: str,
    units: list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: slug_for
  how: 'defines public function `slug_for` at line 471, signature: (rel_path: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _fill_entries
  how: 'defines private function `_fill_entries` at line 491, signature: (entries:
    list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_node
  how: 'defines public function `build_node` at line 499, signature: (rel_path: str,
    abs_path: Path, parent_id: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 555, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_dump
  how: '`yaml.safe_dump(contract, sort_keys=False, default_flow_style=False, allow_unicode=True)`
    at line 523'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 15 `print()` call(s) at line(s) [574, 588, 614, 624, 640, 658, 661, 663, 664,
    666, 667, 668, 669, 672, 673]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
