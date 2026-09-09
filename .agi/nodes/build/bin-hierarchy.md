---
build_kind: code
confidence: 1.0
id: "build:bin-hierarchy"
mint_id: 4304013ede4a40ac8810e248bbb989a3
origin: build-scan
parents:
  - mvp:bin-modules
payload_ref: extensions/agi/bin/hierarchy.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/hierarchy.py"
type: build
---

`extensions/agi/bin/hierarchy.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:bin-modules`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/hierarchy.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 35'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.persistence.frontmatter
  how: '`from graph_core.persistence import frontmatter as _fm` at line 40'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pin
  how: '`pin.read_text(encoding="utf-8")` at line 116'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: load_seats
  how: 'defines public function `load_seats` at line 66, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_ladder
  how: 'defines public function `load_ladder` at line 79, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_body
  how: 'defines public function `load_body` at line 91, signature: (root: Path, node:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: seat_sessions_dir
  how: 'defines public function `seat_sessions_dir` at line 102, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pin_target
  how: 'defines private function `_pin_target` at line 110, signature: (root: Path,
    name: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _has_pin
  how: 'defines private function `_has_pin` at line 128, signature: (root: Path, name:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_orphan_pins
  how: 'defines public function `check_orphan_pins` at line 135, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_duplicate_transcripts
  how: 'defines public function `check_duplicate_transcripts` at line 156, signature:
    (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_rotated_by
  how: 'defines public function `check_rotated_by` at line 176, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_director_kids
  how: 'defines public function `check_director_kids` at line 191, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_unresolved
  how: 'defines public function `check_unresolved` at line 219, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_separator
  how: 'defines private function `_is_separator` at line 239, signature: (line: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _markdown_tables
  how: 'defines private function `_markdown_tables` at line 246, signature: (body:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _split_cells
  how: 'defines private function `_split_cells` at line 271, signature: (line: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_body_tables
  how: 'defines public function `check_body_tables` at line 275, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run_check
  how: 'defines public function `run_check` at line 351, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render
  how: 'defines public function `render` at line 362, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _resolve_root
  how: 'defines private function `_resolve_root` at line 403, signature: (arg: str
    | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 414, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 3 `print()` call(s) at line(s) [431, 432, 434]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
