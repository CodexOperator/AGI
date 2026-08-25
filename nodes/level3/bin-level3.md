---
confidence: 1.0
id: "level3:bin-level3"
mint_id: 59ccbfe63daf4e1bbccbe88d4e3e73b3
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
- name: hashlib
  how: '`import hashlib` at line 72'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 73'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 76'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 77'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 78'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 80'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: abs_path
  how: '`abs_path.read_bytes()` at line 478'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: abs_path
  how: '`abs_path.read_bytes()` at line 464'
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
  how: 'defines private function `_set_project_root` at line 102, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: grid_payload_for
  how: 'defines public function `grid_payload_for` at line 139, signature: (project_root:
    Path, node_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git_ls_files
  how: 'defines public function `git_ls_files` at line 166, signature: (engine_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: discover_files
  how: 'defines public function `discover_files` at line 182, signature: (engine_root:
    Path, payload_root: Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: discover_payload_only_files
  how: 'defines public function `discover_payload_only_files` at line 215, signature:
    (engine_root: Path, payload_root: Path | None, already: set[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _cap
  how: 'defines private function `_cap` at line 271, signature: (s: str | None, limit:
    int=_CAP_LEN)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _unparse_safe
  how: 'defines private function `_unparse_safe` at line 286, signature: (node: ast.AST
    | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scan_imports
  how: 'defines private function `_scan_imports` at line 295, signature: (tree: ast.Module)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scan_top_level_defs
  how: 'defines private function `_scan_top_level_defs` at line 316, signature: (tree:
    ast.Module)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scan_io_calls
  how: 'defines private function `_scan_io_calls` at line 337, signature: (tree: ast.Module)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scan_cli_and_env
  how: 'defines private function `_scan_cli_and_env` at line 401, signature: (tree:
    ast.Module)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scan_stdout
  how: 'defines private function `_scan_stdout` at line 445, signature: (tree: ast.Module)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _content_sha256
  how: 'defines private function `_content_sha256` at line 456, signature: (abs_path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: analyze_file
  how: 'defines public function `analyze_file` at line 469, signature: (abs_path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: analyze_source
  how: 'defines public function `analyze_source` at line 485, signature: (data: bytes,
    suffix: str, name: str=''<payload>'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_census_units
  how: 'defines public function `load_census_units` at line 549, signature: (existing:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_parent
  how: 'defines public function `find_parent` at line 579, signature: (rel_path: str,
    units: list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: slug_for
  how: 'defines public function `slug_for` at line 601, signature: (rel_path: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _fill_entries
  how: 'defines private function `_fill_entries` at line 621, signature: (entries:
    list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_node
  how: 'defines public function `build_node` at line 629, signature: (rel_path: str,
    abs_path: Path, parent_id: str | None, payload: bytes | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 700, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_dump
  how: '`yaml.safe_dump(contract, sort_keys=False, default_flow_style=False, allow_unicode=True)`
    at line 668'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 18 `print()` call(s) at line(s) [247, 726, 740, 783, 793, 809, 835, 841, 844,
    846, 847, 849, 850, 851, 853, 855, 858, 859]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
