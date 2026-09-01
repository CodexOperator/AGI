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
  how: '`import locations` at line 48'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.mint_permanent_id
  how: '`from graph_core.identity import mint_permanent_id` at line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.is_valid_mint_id
  how: '`from graph_core.identity import is_valid_mint_id` at line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GOALS_MD
  how: '`GOALS_MD.read_text(encoding="utf-8")` at line 902'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 223'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: md_path
  how: '`md_path.read_text(encoding="utf-8")` at line 426'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GOALS_MD
  how: '`GOALS_MD.read_text(encoding="utf-8")` at line 832'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 223'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 465'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 465'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 430'
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
  how: 'defines public function `ensure_mint_id` at line 77, signature: (fm: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: natural_sort_key
  how: 'defines public function `natural_sort_key` at line 141, signature: (gid: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _id_rest
  how: 'defines private function `_id_rest` at line 171, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _set_project_root
  how: 'defines private function `_set_project_root` at line 182, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: slugify
  how: 'defines public function `slugify` at line 194, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _add_graph_core_to_path
  how: defines private function `_add_graph_core_to_path` at line 201
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _upsert_node_to_db
  how: 'defines private function `_upsert_node_to_db` at line 217, signature: (node_id:
    str, fm: dict, body: str, origin: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: extract_thought
  how: 'defines public function `extract_thought` at line 273, signature: (body: str
    | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: strip_thought
  how: 'defines public function `strip_thought` at line 286, signature: (body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: splice_thought
  how: 'defines public function `splice_thought` at line 305, signature: (new_body:
    str, old_body: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_frontmatter
  how: 'defines public function `write_frontmatter` at line 320, signature: (path:
    Path, fm: dict, body: str, origin: str='''', preserve: dict | None=None, preserve_body:
    str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_existing_nodes
  how: defines public function `load_existing_nodes` at line 412
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _strip_separators
  how: 'defines private function `_strip_separators` at line 447, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: body_cap
  how: defines public function `body_cap` at line 451
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cap_body
  how: 'defines public function `cap_body` at line 471, signature: (body: str, gid:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_goals
  how: 'defines public function `parse_goals` at line 528, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: strip_banner
  how: 'defines public function `strip_banner` at line 606, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_preamble
  how: 'defines public function `parse_preamble` at line 617, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_goals
  how: 'defines public function `render_goals` at line 635, signature: (preamble:
    str, goals: list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collect_parent_refs
  how: 'defines public function `collect_parent_refs` at line 665, signature: (existing:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: report_integrity
  how: 'defines public function `report_integrity` at line 698, signature: (existing:
    dict, refs: dict, known_ids: set[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_preamble_node
  how: 'defines public function `write_preamble_node` at line 747, signature: (preamble:
    str, existing: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_goal_nodes
  how: 'defines public function `load_goal_nodes` at line 767, signature: (existing:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_render
  how: 'defines public function `cmd_render` at line 814, signature: (check: bool,
    strict: bool=False, strict_goals: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 859, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text("\n".join(lines), encoding="utf-8")` at line 409'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GOALS_MD
  how: '`GOALS_MD.write_text(rendered, encoding="utf-8")` at line 846'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_dump
  how: '`yaml.safe_dump( {k: v}, default_flow_style=False, sort_keys=False, allow_unicode=True,
    width=10_000, )` at line 380'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 25 `print()` call(s) at line(s) [100, 236, 512, 518, 693, 727, 733, 738, 827,
    834, 840, 842, 844, 847, 849, 853, 892, 899, 916, 988, 990, 991, 993, 996, 1007]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
