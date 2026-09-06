---
id: build:bin-decompose-engine
mint_id: 4dc15a3c05bf481d849bbce250b7880c
type: build
parents:
  - idea:engine-decompose-engine
build_kind: code
confidence: 1.0
edited_by: director
origin: build-scan
payload_ref: extensions/agi/bin/decompose-engine.py
tags:
  - build
  - code
  - g2.1
thought_session: doc-pass-2026-09-06
title: "Build: extensions/agi/bin/decompose-engine.py"
---
`extensions/agi/bin/decompose-engine.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-decompose-engine`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/decompose-engine.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 45'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 47'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 48'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 49'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 50'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 52'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 53'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text(encoding="utf-8")` at line 337'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(path.read_text(encoding="utf-8"))` at line 356'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 356'
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
  how: 'defines private function `_set_project_root` at line 75, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git_ls_files
  how: 'defines public function `git_ls_files` at line 164, signature: (engine_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: discover_units
  how: 'defines public function `discover_units` at line 180, signature: (engine_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _extract_py_docstring
  how: 'defines private function `_extract_py_docstring` at line 293, signature: (text:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _extract_sh_header
  how: 'defines private function `_extract_sh_header` at line 303, signature: (text:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _extract_block_comment
  how: 'defines private function `_extract_block_comment` at line 323, signature:
    (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: extract_doc
  how: 'defines public function `extract_doc` at line 332, signature: (engine_root:
    Path, doc_source: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_goal_map
  how: 'defines public function `load_goal_map` at line 352, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_node
  how: 'defines public function `build_node` at line 372, signature: (unit: dict,
    doc: str | None, goal_id: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _tokens
  how: 'defines private function `_tokens` at line 412, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _overlaps
  how: 'defines private function `_overlaps` at line 417, signature: (a_tokens: list[str],
    b_tokens: list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: report_stale_domain_nodes
  how: 'defines public function `report_stale_domain_nodes` at line 421, signature:
    (existing: dict, units: list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 447, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 19 `print()` call(s) at line(s) [358, 363, 438, 470, 481, 507, 518, 529, 546,
    549, 553, 554, 556, 558, 559, 560, 562, 563, 564]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Doc pass 2026-09-06: seven pre-agi entry points and three cavekit-era context directories retired from the census tables; their build nodes are deprecated and the files are gone, the grid keeps every version. Presence was already checked against git ls-files, so the rows were dead weight.
<!-- THOUGHT:END -->
