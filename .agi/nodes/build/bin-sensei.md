---
build_kind: code
confidence: 1.0
id: "build:bin-sensei"
mint_id: 7c11872781b84492832143ea0153b5fa
origin: build-scan
parents:
  - mvp:bin-modules
payload_ref: extensions/agi/bin/sensei.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/sensei.py"
type: build
---

`extensions/agi/bin/sensei.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:bin-modules`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/sensei.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text(encoding="utf-8")` at line 66'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 151'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(text)` at line 157'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ln)` at line 173'
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
  how: 'defines public function `load_seats` at line 55, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: seat_row
  how: 'defines public function `seat_row` at line 90, signature: (rows: list[dict],
    name: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _direct_supervisor
  how: 'defines private function `_direct_supervisor` at line 100, signature: (row:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _required_threads
  how: 'defines private function `_required_threads` at line 116, signature: (row:
    dict | None, target: str, supervisor_flag: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_ledger_rows
  how: 'defines public function `load_ledger_rows` at line 140, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pick_worst
  how: 'defines public function `pick_worst` at line 182, signature: (rows: list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _normts
  how: 'defines private function `_normts` at line 213, signature: (ts: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _after
  how: 'defines private function `_after` at line 218, signature: (block_ts: str,
    since: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _has_reply
  how: 'defines private function `_has_reply` at line 224, signature: (croot: Path,
    thread: tuple[str, str], since: str, *, me: str=SENSEI)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: apply_note
  how: 'defines public function `apply_note` at line 245, signature: (root: Path,
    node_id: str, change: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_propose
  how: 'defines public function `cmd_propose` at line 261, signature: (root: Path,
    croot: Path, args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_apply
  how: 'defines public function `cmd_apply` at line 285, signature: (root: Path, croot:
    Path, args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _draft_for_owner
  how: 'defines private function `_draft_for_owner` at line 328, signature: (root:
    Path, croot: Path, args, threads: list[tuple[str, str]])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 352, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text(body, encoding="utf-8")` at line 340'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 17 `print()` call(s) at line(s) [265, 268, 280, 281, 289, 293, 297, 301, 308,
    319, 322, 324, 344, 345, 355, 399, 401]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
