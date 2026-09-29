---
id: build:bin-snapshot-goals
mint_id: aa00705c2b644965a9cba7e91c411188
type: build
parents:
  - goal:g7.16.1.2.7
  - idea:engine-snapshot-goals
build_kind: code
confidence: 1.0
edited_by: director-general-3
origin: build-scan
payload_ref: extensions/agi/bin/snapshot-goals.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/snapshot-goals.py"
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
- name: hashlib
  how: '`import hashlib` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 58'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_writer
  how: '`import node_writer` at line 59'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_writer.log_write
  how: '`from node_writer import log_write` at line 60'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: spawn_gate.nearest_vision_town
  how: '`from spawn_gate import nearest_vision_town` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: spawn_gate.vision_scope
  how: '`from spawn_gate import vision_scope` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.ensure_mint_id
  how: '`from graph_core.identity import ensure_mint_id as _ensure_mint_id` at line
    87'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: frontmatter.split_frontmatter
  how: '`from frontmatter import split_frontmatter` at line 88'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GOALS_MD
  how: '`GOALS_MD.read_text(encoding="utf-8")` at line 1147'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GOALS_MD
  how: '`GOALS_MD.read_text(encoding="utf-8")` at line 1005'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 215'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: md_path
  how: '`md_path.read_text(encoding="utf-8")` at line 419'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 215'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 458'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 458'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parted[0])` at line 423'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 990'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: natural_sort_key
  how: 'defines public function `natural_sort_key` at line 133, signature: (gid: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _id_rest
  how: 'defines private function `_id_rest` at line 163, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _set_project_root
  how: 'defines private function `_set_project_root` at line 174, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: slugify
  how: 'defines public function `slugify` at line 186, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _add_graph_core_to_path
  how: defines private function `_add_graph_core_to_path` at line 193
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _upsert_node_to_db
  how: 'defines private function `_upsert_node_to_db` at line 209, signature: (node_id:
    str, fm: dict, body: str, origin: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: extract_thought
  how: 'defines public function `extract_thought` at line 263, signature: (body: str
    | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: strip_thought
  how: 'defines public function `strip_thought` at line 275, signature: (body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: splice_thought
  how: 'defines public function `splice_thought` at line 294, signature: (new_body:
    str, old_body: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_frontmatter
  how: 'defines public function `write_frontmatter` at line 309, signature: (path:
    Path, fm: dict, body: str, origin: str='''', preserve: dict | None=None, preserve_body:
    str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_existing_nodes
  how: defines public function `load_existing_nodes` at line 405
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _strip_separators
  how: 'defines private function `_strip_separators` at line 440, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: body_cap
  how: defines public function `body_cap` at line 444
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cap_body
  how: 'defines public function `cap_body` at line 464, signature: (body: str, gid:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_goals
  how: 'defines public function `parse_goals` at line 521, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: strip_banner
  how: 'defines public function `strip_banner` at line 636, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_preamble
  how: 'defines public function `parse_preamble` at line 647, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_goals
  how: 'defines public function `render_goals` at line 665, signature: (preamble:
    str, goals: list[dict])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collect_parent_refs
  how: 'defines public function `collect_parent_refs` at line 748, signature: (existing:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: report_integrity
  how: 'defines public function `report_integrity` at line 781, signature: (existing:
    dict, refs: dict, known_ids: set[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_preamble_node
  how: 'defines public function `write_preamble_node` at line 830, signature: (preamble:
    str, existing: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_goal_nodes
  how: 'defines public function `load_goal_nodes` at line 850, signature: (existing:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: warn_premature_complete
  how: 'defines public function `warn_premature_complete` at line 917, signature:
    (existing: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _source_digest
  how: 'defines private function `_source_digest` at line 966, signature: (existing:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _compare_rendered
  how: 'defines private function `_compare_rendered` at line 996, signature: (rendered:
    str, n_goals: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _check_with_race_guard
  how: 'defines private function `_check_with_race_guard` at line 1021, signature:
    (existing: dict, rendered: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _goal_count
  how: 'defines private function `_goal_count` at line 1065, signature: (existing:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_render
  how: 'defines public function `cmd_render` at line 1071, signature: (check: bool,
    strict: bool=False, strict_goals: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 1104, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text(text, encoding="utf-8")` at line 399'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GOALS_MD
  how: '`GOALS_MD.write_text(rendered, encoding="utf-8")` at line 1090'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_dump
  how: '`yaml.safe_dump( {k: v}, default_flow_style=False, sort_keys=False, allow_unicode=True,
    width=10_000, )` at line 369'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 26 `print()` call(s) at line(s) [228, 505, 511, 776, 810, 816, 821, 959, 1007,
    1013, 1015, 1017, 1052, 1084, 1091, 1094, 1098, 1137, 1144, 1161, 1258, 1260,
    1261, 1263, 1266, 1277]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Council bundle 2 row M (director-general-3, mvp:dg3-m-marker-strings): the THOUGHT marker strings THOUGHT_BEGIN/THOUGHT_END now live in node_writer only, moved verbatim from snapshot-goals.py; snapshot-goals re-exports them and write.py's thought verb imports them. The GOALS render stays byte-identical. Bundle 1's column-0 definition (row B) is unchanged.
<!-- THOUGHT:END -->
