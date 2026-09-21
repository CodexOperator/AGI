---
id: build:bin-handoff
mint_id: c0e8c4384c364991b032753f317c32f4
type: build
parents:
  - mvp:bin-modules
build_kind: code
confidence: 1.0
edited_by: sanctuary-director
origin: build-scan
payload_ref: extensions/agi/bin/handoff.py
tags:
  - build
  - code
  - g2.1
thought_session: SD.16-director
title: "Build: extensions/agi/bin/handoff.py"
---
`extensions/agi/bin/handoff.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:bin-modules`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/handoff.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 47'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 49'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: errno
  how: '`import errno` at line 50'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fcntl
  how: '`import fcntl` at line 51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 52'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 53'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 55'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tempfile
  how: '`import tempfile` at line 56'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: contextlib.contextmanager
  how: '`from contextlib import contextmanager` at line 58'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 59'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: handoff_path(root)
  how: '`handoff_path(root).read_text()` at line 194'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 302'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 362'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 435'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(p.read_text())` at line 152'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: args.content_file
  how: '`args.content_file.read_text()` at line 487'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 152'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdin
  how: reads `sys.stdin` / calls `input()`
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: handoff_path
  how: 'defines public function `handoff_path` at line 78, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: claims_dir
  how: 'defines public function `claims_dir` at line 92, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_sections
  how: 'defines public function `parse_sections` at line 108, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: section_by_name
  how: 'defines public function `section_by_name` at line 126, signature: (secs: list[dict],
    name: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: estimate_tokens
  how: 'defines public function `estimate_tokens` at line 133, signature: (byte_count:
    int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _claim_path
  how: 'defines private function `_claim_path` at line 141, signature: (d: Path, section:
    str, holder: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_claims
  how: 'defines private function `_read_claims` at line 146, signature: (d: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _claim_stale
  how: 'defines private function `_claim_stale` at line 158, signature: (rec: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _touch_claim
  how: 'defines private function `_touch_claim` at line 173, signature: (root: Path,
    section: str, holder: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: claim
  how: 'defines public function `claim` at line 184, signature: (root: Path, section:
    str, holder: str, *, write: bool=False, force: bool=False, pid: int | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: release
  how: 'defines public function `release` at line 223, signature: (root: Path, section:
    str, holder: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: show_claims
  how: 'defines public function `show_claims` at line 233, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_json
  how: 'defines private function `_write_json` at line 241, signature: (path: Path,
    rec: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _claims_lock
  how: 'defines private function `_claims_lock` at line 253, signature: (d: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _file_lock
  how: 'defines private function `_file_lock` at line 270, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_section
  how: 'defines public function `read_section` at line 293, signature: (root: Path,
    section: str, holder: str | None=None, *, prime: bool=False, whole: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_section
  how: 'defines public function `write_section` at line 327, signature: (root: Path,
    section: str, content: str, holder: str | None=None, *, prime: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _atomic_write
  how: 'defines private function `_atomic_write` at line 379, signature: (path: Path,
    text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 395, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lock_path
  how: '`open(lock_path, "w")` at line 261 (mode=''w'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lock_path
  how: '`open(lock_path, "w")` at line 281 (mode=''w'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dump
  how: '`json.dump(rec, fh)` at line 245'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 20 `print()` call(s) at line(s) [437, 438, 440, 448, 452, 453, 454, 455, 461,
    463, 471, 473, 475, 476, 481, 493, 495, 501, 505, 508]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.