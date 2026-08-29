---
build_kind: code
confidence: 1.0
id: "build:bin-snapshot-goals"
mint_id: aa00705c2b644965a9cba7e91c411188
origin: build-scan
parents:
  - idea:engine-snapshot-goals
payload_ref: extensions/agi/bin/snapshot-goals.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/snapshot-goals.py"
type: build
---

`extensions/agi/bin/snapshot-goals.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-snapshot-goals`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
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
- name: locations
  how: '`import locations` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.mint_permanent_id
  how: '`from graph_core.identity import mint_permanent_id` at line 66'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.is_valid_mint_id
  how: '`from graph_core.identity import is_valid_mint_id` at line 66'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GOALS_MD
  how: '`GOALS_MD.read_text(encoding="utf-8")` at line 840'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 182'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: md_path
  how: '`md_path.read_text(encoding="utf-8")` at line 365'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GOALS_MD
  how: '`GOALS_MD.read_text(encoding="utf-8")` at line 770'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 182'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 404'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 404'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 369'
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
  how: 'defines public function `ensure_mint_id` at line 69, signature: (fm: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: config_path
  how: 'defines public function `config_path` at line 99, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _id_rest
  how: 'defines private function `_id_rest` at line 130, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _set_project_root
  how: 'defines private function `_set_project_root` at line 141, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: slugify
  how: 'defines public function `slugify` at line 153, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _add_graph_core_to_path
  how: defines private function `_add_graph_core_to_path` at line 160
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _upsert_node_to_db
  how: 'defines private function `_upsert_node_to_db` at line 176, signature: (node_id:
    str, fm: dict, body: str, origin: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: extract_thought
  how: 'defines public function `extract_thought` at line 232, signature: (body: str
    | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: strip_thought
  how: 'defines public function `strip_thought` at line 245, signature: (body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: splice_thought
  how: 'defines public function `splice_thought` at line 264, signature: (new_body:
    str, old_body: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_frontmatter
  how: 'defines public function `write_frontmatter` at line 279, signature: (path:
    Path, fm: dict, body: str, origin: str='''', preserve: dict | None=None, preserve_body:
    str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_existing_nodes
  how: defines public function `load_existing_nodes` at line 351
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _strip_separators
  how: 'defines private function `_strip_separators` at line 386, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: body_cap
  how: defines public function `body_cap` at line 390
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cap_body
  how: 'defines public function `cap_body` at line 410, signature: (body: str, gid:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_goals
  how: 'defines public function `parse_goals` at line 467, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: strip_banner
  how: 'defines public function `strip_banner` at line 542, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_preamble
  how: 'defines public function `parse_preamble` at line 553, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_goals
  how: 'defines public function `render_goals` at line 571, signature: (preamble:
    str, goals: list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collect_parent_refs
  how: 'defines public function `collect_parent_refs` at line 599, signature: (existing:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: report_integrity
  how: 'defines public function `report_integrity` at line 632, signature: (existing:
    dict, refs: dict, known_ids: set[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_preamble_node
  how: 'defines public function `write_preamble_node` at line 681, signature: (preamble:
    str, existing: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_goal_nodes
  how: 'defines public function `load_goal_nodes` at line 701, signature: (existing:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_render
  how: 'defines public function `cmd_render` at line 752, signature: (check: bool,
    strict: bool=False, strict_goals: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 797, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text("\n".join(lines), encoding="utf-8")` at line 348'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GOALS_MD
  how: '`GOALS_MD.write_text(rendered, encoding="utf-8")` at line 784'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 25 `print()` call(s) at line(s) [92, 195, 451, 457, 627, 661, 667, 672, 765,
    772, 778, 780, 782, 785, 787, 791, 830, 837, 854, 926, 928, 929, 931, 934, 945]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
