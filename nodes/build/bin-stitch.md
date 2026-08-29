---
build_kind: code
confidence: 1.0
id: "build:bin-stitch"
mint_id: b973280797364cb297adb83a40c97db3
origin: build-scan
payload_ref: extensions/agi/bin/stitch.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/stitch.py"
type: build
---

`extensions/agi/bin/stitch.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

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
  how: '`yaml.safe_load(parts[1])` at line 239'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: md_path
  how: '`md_path.read_text(encoding="utf-8")` at line 277'
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
  how: defines public class `Level3Node` at line 213
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_frontmatter
  how: 'defines private function `_parse_frontmatter` at line 231, signature: (text:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_level3_nodes
  how: 'defines public function `load_level3_nodes` at line 250, signature: (project_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _entry_pairs
  how: 'defines private function `_entry_pairs` at line 318, signature: (entries)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: diff_contract
  how: 'defines public function `diff_contract` at line 324, signature: (stored: dict,
    fresh: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _group_by_payload_ref
  how: 'defines private function `_group_by_payload_ref` at line 351, signature: (nodes:
    list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_well_formed_chain
  how: 'defines private function `_is_well_formed_chain` at line 363, signature: (group:
    list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _chain_order
  how: 'defines private function `_chain_order` at line 396, signature: (group: list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: verify_tree
  how: 'defines public function `verify_tree` at line 401, signature: (project_root:
    Path, engine_root: Path, from_grid: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: has_drift
  how: 'defines public function `has_drift` at line 545, signature: (report: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_within
  how: 'defines private function `_is_within` at line 554, signature: (path: Path,
    root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_is_clean
  how: 'defines private function `_git_is_clean` at line 562, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _guard_out_dir
  how: 'defines private function `_guard_out_dir` at line 573, signature: (out_dir:
    Path, project_root: Path, engine_root: Path, publish: bool=False, from_grid: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _grid_payload
  how: 'defines private function `_grid_payload` at line 627, signature: (project_root:
    Path, node: Level3Node, grid_version: int | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: materialize
  how: 'defines public function `materialize` at line 661, signature: (project_root:
    Path, engine_root: Path, out_dir: Path, force: bool=False, version: int | None=None,
    from_grid: bool=False, publish: bool=False, grid_version: int | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: print_verify_report
  how: 'defines public function `print_verify_report` at line 806, signature: (report:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: print_materialize_report
  how: 'defines public function `print_materialize_report` at line 851, signature:
    (stats: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 885, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 36 `print()` call(s) at line(s) [807, 808, 810, 812, 814, 816, 818, 820, 822,
    824, 826, 827, 830, 833, 836, 840, 842, 843, 846, 848, 852, 853, 855, 858, 860,
    864, 866, 868, 871, 873, 876, 878, 879, 930, 941, 949]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
