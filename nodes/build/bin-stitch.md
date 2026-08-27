---
build_kind: code
confidence: 1.0
id: "build:bin-stitch"
mint_id: ad6809b5d43b4983827231158b779f69
origin: build-scan
parents:
  - idea:engine-stitch
payload_ref: extensions/agi/bin/stitch.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/stitch.py"
type: build
---

`extensions/agi/bin/stitch.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-stitch`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/stitch.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 142'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 144'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 145'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 146'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shutil
  how: '`import shutil` at line 147'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 148'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 149'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 150'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.Counter
  how: '`from collections import Counter` at line 151'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 152'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 154'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(yaml_text)` at line 276'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 231'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: md_path
  how: '`md_path.read_text(encoding=''utf-8'')` at line 301'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: StitchSafetyError
  how: defines public class `StitchSafetyError` at line 164
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Level3Node
  how: defines public class `Level3Node` at line 205
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_frontmatter
  how: 'defines private function `_parse_frontmatter` at line 223, signature: (text:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _extract_contract
  how: 'defines private function `_extract_contract` at line 239, signature: (body:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_level3_nodes
  how: 'defines public function `load_level3_nodes` at line 284, signature: (project_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _entry_pairs
  how: 'defines private function `_entry_pairs` at line 342, signature: (entries)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: diff_contract
  how: 'defines public function `diff_contract` at line 348, signature: (stored: dict,
    fresh: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _group_by_payload_ref
  how: 'defines private function `_group_by_payload_ref` at line 375, signature: (nodes:
    list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_well_formed_chain
  how: 'defines private function `_is_well_formed_chain` at line 387, signature: (group:
    list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _chain_order
  how: 'defines private function `_chain_order` at line 420, signature: (group: list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: verify_tree
  how: 'defines public function `verify_tree` at line 425, signature: (project_root:
    Path, engine_root: Path, from_grid: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: has_drift
  how: 'defines public function `has_drift` at line 547, signature: (report: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_within
  how: 'defines private function `_is_within` at line 556, signature: (path: Path,
    root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_is_clean
  how: 'defines private function `_git_is_clean` at line 564, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _guard_out_dir
  how: 'defines private function `_guard_out_dir` at line 575, signature: (out_dir:
    Path, project_root: Path, engine_root: Path, publish: bool=False, from_grid: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _grid_payload
  how: 'defines private function `_grid_payload` at line 629, signature: (project_root:
    Path, node: Level3Node, grid_version: int | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: materialize
  how: 'defines public function `materialize` at line 663, signature: (project_root:
    Path, engine_root: Path, out_dir: Path, force: bool=False, version: int | None=None,
    from_grid: bool=False, publish: bool=False, grid_version: int | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: print_verify_report
  how: 'defines public function `print_verify_report` at line 808, signature: (report:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: print_materialize_report
  how: 'defines public function `print_materialize_report` at line 853, signature:
    (stats: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 887, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 36 `print()` call(s) at line(s) [809, 810, 812, 814, 816, 818, 820, 822, 824,
    826, 828, 829, 832, 835, 838, 842, 844, 845, 848, 850, 854, 855, 857, 860, 862,
    866, 868, 870, 873, 875, 878, 880, 881, 932, 943, 951]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
