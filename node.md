---
id: build:bin-viewport
mint_id: b3d2e0e728ff44609a28f351f4ee038c
type: build
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/bin/viewport.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/viewport.py"
---
`extensions/agi/bin/viewport.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/viewport.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 56'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 58'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 59'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 60'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dataclasses.dataclass
  how: '`from dataclasses import dataclass` at line 62'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 63'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 69'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: zoom
  how: '`import zoom` at line 70'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(mf.read_text())` at line 308'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(aj.read_text())` at line 319'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mf
  how: '`mf.read_text()` at line 308'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: aj
  how: '`aj.read_text()` at line 319'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: Frame
  how: defines public class `Frame` at line 97
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _title_of
  how: 'defines private function `_title_of` at line 115, signature: (node, fm: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: frame_stream
  how: 'defines public function `frame_stream` at line 122, signature: (g, fm_by_id:
    dict, anchor: str | None, max_depth: int, agents_at: dict | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _damage_of
  how: 'defines private function `_damage_of` at line 174, signature: (g, node, fm:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _all_ids
  how: 'defines private function `_all_ids` at line 193, signature: (g)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: default_roots
  how: 'defines public function `default_roots` at line 211, signature: (g, fm_by_id:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_human
  how: 'defines public function `render_human` at line 240, signature: (frames: list[Frame],
    top: int, left: int, height: int, width: int, status: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_llm
  how: 'defines public function `render_llm` at line 257, signature: (frames: list[Frame],
    top: int, left: int, height: int, width: int, status: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iteration_points
  how: 'defines public function `iteration_points` at line 286, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: agents_of_iteration
  how: 'defines public function `agents_of_iteration` at line 295, signature: (root:
    Path, iter_name: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: grid_versions
  how: 'defines public function `grid_versions` at line 332, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: interactive
  how: 'defines public function `interactive` at line 349, signature: (root: Path,
    g, fm_by_id, args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 424
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _verify
  how: 'defines private function `_verify` at line 494, signature: (frames: list[Frame],
    args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 15 `print()` call(s) at line(s) [444, 452, 479, 480, 481, 482, 486, 487, 488,
    489, 511, 516, 521, 524, 526]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.