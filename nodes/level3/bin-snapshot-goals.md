---
confidence: 1.0
id: "level3:bin-snapshot-goals"
mint_id: aa00705c2b644965a9cba7e91c411188
origin: level3-scan
parents:
  - idea:engine-snapshot-goals
payload_ref: extensions/agi/bin/snapshot-goals.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/bin/snapshot-goals.py"
type: level3
---

`extensions/agi/bin/snapshot-goals.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-snapshot-goals`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/snapshot-goals.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.mint_permanent_id
  how: '`from graph_core.identity import mint_permanent_id` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.is_valid_mint_id
  how: '`from graph_core.identity import is_valid_mint_id` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GOALS_MD
  how: '`GOALS_MD.read_text(encoding=''utf-8'')` at line 470'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 172'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: md_path
  how: '`md_path.read_text(encoding=''utf-8'')` at line 261'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 172'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 299'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 299'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 265'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: ensure_mint_id
  how: 'defines public function `ensure_mint_id` at line 64, signature: (fm: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: config_path
  how: 'defines public function `config_path` at line 94, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _id_rest
  how: 'defines private function `_id_rest` at line 120, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _set_project_root
  how: 'defines private function `_set_project_root` at line 131, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: slugify
  how: 'defines public function `slugify` at line 143, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _add_graph_core_to_path
  how: defines private function `_add_graph_core_to_path` at line 150
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _upsert_node_to_db
  how: 'defines private function `_upsert_node_to_db` at line 166, signature: (node_id:
    str, fm: dict, body: str, origin: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_frontmatter
  how: 'defines public function `write_frontmatter` at line 197, signature: (path:
    Path, fm: dict, body: str, origin: str='''', preserve: dict | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_existing_nodes
  how: defines public function `load_existing_nodes` at line 252
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _strip_separators
  how: 'defines private function `_strip_separators` at line 281, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: body_cap
  how: defines public function `body_cap` at line 285
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cap_body
  how: 'defines public function `cap_body` at line 305, signature: (body: str, gid:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_goals
  how: 'defines public function `parse_goals` at line 362, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collect_parent_refs
  how: 'defines public function `collect_parent_refs` at line 415, signature: (existing:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 448, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text(''\n''.join(lines), encoding=''utf-8'')` at line 249'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 16 `print()` call(s) at line(s) [87, 185, 346, 352, 443, 467, 480, 539, 545,
    550, 562, 564, 565, 567, 570, 581]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
