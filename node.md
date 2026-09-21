---
id: build:bin-dashboard
mint_id: 5c4a3bad7e7445b6879446a105bc0165
type: build
parents:
  - idea:engine-dashboard
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/bin/dashboard.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/dashboard.py"
---
`extensions/agi/bin/dashboard.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-dashboard`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/dashboard.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 42'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 44'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: io
  how: '`import io` at line 45'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 46'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shutil
  how: '`import shutil` at line 47'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 48'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 49'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: textwrap
  how: '`import textwrap` at line 50'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.Counter
  how: '`from collections import Counter` at line 52'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: contextlib.redirect_stderr
  how: '`from contextlib import redirect_stderr` at line 53'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: metrics
  how: '`import metrics` at line 62'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate
  how: '`import evidence_gate` at line 63'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.read_text(encoding="utf-8", errors="replace")` at line 294'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: Palette
  how: defines public class `Palette` at line 89
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_root
  how: 'defines public function `find_root` at line 120, signature: (explicit: str
    | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _descendants
  how: 'defines private function `_descendants` at line 136, signature: (g, node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _stage_rank
  how: 'defines private function `_stage_rank` at line 155, signature: (node_type:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collect_goals
  how: 'defines public function `collect_goals` at line 162, signature: (g, fm_by_id:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _goal_sort_key
  how: 'defines private function `_goal_sort_key` at line 194, signature: (goal_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _naive_evidence_count
  how: 'defines private function `_naive_evidence_count` at line 202, signature: (value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolved_evidence_stats
  how: 'defines public function `resolved_evidence_stats` at line 228, signature:
    (nodes_dir: Path, g)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_duplicate_ids
  how: 'defines public function `find_duplicate_ids` at line 279, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dangling_and_orphans
  how: 'defines public function `dangling_and_orphans` at line 308, signature: (g)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: chain_health
  how: 'defines public function `chain_health` at line 320, signature: (g, nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: recent_activity
  how: 'defines public function `recent_activity` at line 353, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _wrap
  how: 'defines private function `_wrap` at line 409, signature: (text: str, width:
    int, indent: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_goals
  how: 'defines public function `render_goals` at line 414, signature: (g, fm_by_id:
    dict, pal: Palette, width: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_metrics
  how: 'defines public function `render_metrics` at line 471, signature: (m: dict,
    cfg: dict, resolved: dict, width: int, pal: Palette)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_health
  how: 'defines public function `render_health` at line 556, signature: (g, nodes_dir:
    Path, pal: Palette, width: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_activity
  how: 'defines public function `render_activity` at line 625, signature: (act: dict,
    width: int, pal: Palette)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: gather
  how: 'defines public function `gather` at line 643, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render
  how: 'defines public function `render` at line 662, signature: (root: Path, data:
    dict, pal: Palette, width: int, section: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_parser
  how: defines public function `build_parser` at line 693
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 709, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 4 `print()` call(s) at line(s) [124, 721, 733, 736]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.