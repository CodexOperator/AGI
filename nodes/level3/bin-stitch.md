---
confidence: 1.0
id: "level3:bin-stitch"
origin: level3-scan
parents:
  - idea:engine-stitch
payload_ref: extensions/agi/bin/stitch.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/bin/stitch.py"
type: level3
---

`extensions/agi/bin/stitch.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-stitch`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/stitch.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 115'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 118'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 119'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shutil
  how: '`import shutil` at line 120'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 121'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 122'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.Counter
  how: '`from collections import Counter` at line 123'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 124'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 126'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(yaml_text)` at line 227'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 182'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: md_path
  how: '`md_path.read_text(encoding=''utf-8'')` at line 252'
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
  how: defines public class `StitchSafetyError` at line 136
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Level3Node
  how: defines public class `Level3Node` at line 160
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_frontmatter
  how: 'defines private function `_parse_frontmatter` at line 174, signature: (text:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _extract_contract
  how: 'defines private function `_extract_contract` at line 190, signature: (body:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_level3_nodes
  how: 'defines public function `load_level3_nodes` at line 235, signature: (project_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _entry_pairs
  how: 'defines private function `_entry_pairs` at line 276, signature: (entries)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: diff_contract
  how: 'defines public function `diff_contract` at line 282, signature: (stored: dict,
    fresh: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: verify_tree
  how: 'defines public function `verify_tree` at line 309, signature: (project_root:
    Path, engine_root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: has_drift
  how: 'defines public function `has_drift` at line 389, signature: (report: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_within
  how: 'defines private function `_is_within` at line 398, signature: (path: Path,
    root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _guard_out_dir
  how: 'defines private function `_guard_out_dir` at line 406, signature: (out_dir:
    Path, project_root: Path, engine_root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: materialize
  how: 'defines public function `materialize` at line 416, signature: (project_root:
    Path, engine_root: Path, out_dir: Path, force: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: print_verify_report
  how: 'defines public function `print_verify_report` at line 480, signature: (report:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: print_materialize_report
  how: 'defines public function `print_materialize_report` at line 513, signature:
    (stats: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 533, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 25 `print()` call(s) at line(s) [481, 482, 484, 486, 488, 490, 492, 494, 496,
    498, 500, 502, 506, 508, 510, 514, 515, 517, 519, 521, 524, 526, 527, 562, 568]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
