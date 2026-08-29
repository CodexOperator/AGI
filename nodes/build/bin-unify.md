---
build_kind: code
confidence: 1.0
id: "build:bin-unify"
mint_id: 542fc6b7c6f24573a06bff7f623dea17
origin: build-scan
payload_ref: extensions/agi/bin/unify.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/unify.py"
type: build
---

`extensions/agi/bin/unify.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/unify.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 93'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hashlib
  how: '`import hashlib` at line 94'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 95'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 96'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 97'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: datetime.datetime
  how: '`from datetime import datetime` at line 98'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: datetime.timezone
  how: '`from datetime import timezone` at line 98'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 99'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 102'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.persistence.frontmatter.load_node_file
  how: '`from graph_core.persistence.frontmatter import load_node_file` at line 109'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.persistence.frontmatter.FrontmatterError
  how: '`from graph_core.persistence.frontmatter import FrontmatterError` at line
    109'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding="utf-8")` at line 355'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`open(path, "rb")` at line 370 (mode=''rb'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tree_gitignore
  how: '`tree_gitignore.read_text(encoding="utf-8")` at line 803'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine_gitignore
  how: '`engine_gitignore.read_text(encoding="utf-8")` at line 804'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(path.read_text(encoding="utf-8"))` at line 896'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tree_gitignore
  how: '`tree_gitignore.read_text(encoding="utf-8")` at line 1100'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine_gitignore
  how: '`engine_gitignore.read_text(encoding="utf-8")` at line 1101'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 896'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: UnifyError
  how: defines public class `UnifyError` at line 161
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git
  how: 'defines private function `_git` at line 171, signature: (repo: Path, *args:
    str, check: bool=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_stdin
  how: 'defines private function `_git_stdin` at line 184, signature: (repo: Path,
    args: list[str], stdin_text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_ancestor
  how: 'defines private function `_is_ancestor` at line 199, signature: (repo: Path,
    ancestor: str, descendant: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _all_refs
  how: 'defines private function `_all_refs` at line 210, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _resolve_branch
  how: 'defines private function `_resolve_branch` at line 226, signature: (repo:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: count_grid_refs
  how: 'defines public function `count_grid_refs` at line 244, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_count
  how: 'defines private function `_node_count` at line 252, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_payload_refs
  how: 'defines public function `iter_payload_refs` at line 259, signature: (tree:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_missing_payloads
  how: 'defines public function `find_missing_payloads` at line 285, signature: (tree:
    Path, engine: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_stale_payloads
  how: 'defines public function `find_stale_payloads` at line 302, signature: (tree:
    Path, engine: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_mint_id
  how: 'defines private function `_read_mint_id` at line 350, signature: (node_path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sha256_file
  how: 'defines private function `_sha256_file` at line 366, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _touches_a_real_repo
  how: 'defines private function `_touches_a_real_repo` at line 390, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _refuse
  how: 'defines private function `_refuse` at line 415, signature: (reason: str, detail:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: preflight
  how: 'defines public function `preflight` at line 419, signature: (engine: Path,
    tree: Path, *, force: bool=False, allow_real: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graft_graph
  how: 'defines public function `graft_graph` at line 537, signature: (engine: Path,
    tree: Path, *, remote_name: str=REMOTE_NAME)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_file_mode
  how: 'defines private function `_git_file_mode` at line 588, signature: (repo: Path,
    relpath: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: relocate_files
  how: 'defines public function `relocate_files` at line 602, signature: (engine:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _gitignore_blocks
  how: 'defines private function `_gitignore_blocks` at line 712, signature: (text:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _block_patterns
  how: 'defines private function `_block_patterns` at line 733, signature: (block:
    list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _filter_graph_block
  how: 'defines private function `_filter_graph_block` at line 737, signature: (block:
    list[str], *, dedupe_against: set[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: merge_gitignore
  how: 'defines public function `merge_gitignore` at line 766, signature: (tree_text:
    str, engine_text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_merged_gitignore
  how: 'defines public function `write_merged_gitignore` at line 795, signature: (engine:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fetch_grid_refs
  how: 'defines public function `fetch_grid_refs` at line 825, signature: (engine:
    Path, tree: Path, *, remote_name: str=REMOTE_NAME)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: remove_temp_remote
  how: 'defines public function `remove_temp_remote` at line 848, signature: (engine:
    Path, remote_name: str=REMOTE_NAME)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prestate_path
  how: 'defines public function `prestate_path` at line 858, signature: (engine: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_prestate
  how: 'defines public function `write_prestate` at line 867, signature: (engine:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_prestate
  how: 'defines public function `read_prestate` at line 884, signature: (engine: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _head_reachable_from_any_remote
  how: 'defines private function `_head_reachable_from_any_remote` at line 904, signature:
    (engine: Path, head: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: preflight_rollback
  how: 'defines public function `preflight_rollback` at line 918, signature: (engine:
    Path, *, force: bool=False, allow_real: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: perform_rollback
  how: 'defines public function `perform_rollback` at line 993, signature: (engine:
    Path, pre: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run_rollback
  how: 'defines public function `run_rollback` at line 1038, signature: (engine: Path,
    *, yes: bool=False, force: bool=False, allow_real: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _would_relocate
  how: 'defines private function `_would_relocate` at line 1072, signature: (tree:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _plan
  how: 'defines private function `_plan` at line 1092, signature: (engine: Path, tree:
    Path, pre: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _summarize
  how: 'defines private function `_summarize` at line 1116, signature: (engine: Path,
    pre: dict, stages: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run_unify
  how: 'defines public function `run_unify` at line 1139, signature: (engine: Path,
    tree: Path, *, yes: bool=False, force: bool=False, allow_real: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _print_human
  how: 'defines private function `_print_human` at line 1180, signature: (report:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _print_human_rollback
  how: 'defines private function `_print_human_rollback` at line 1209, signature:
    (report: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 1233, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine_gitignore
  how: '`engine_gitignore.write_text(merged, encoding="utf-8")` at line 807'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: prestate_path(engine)
  how: '`prestate_path(engine).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")`
    at line 880'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(data, indent=2)` at line 880'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(report, indent=2, default=str)` at line 1284'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 27 `print()` call(s) at line(s) [1182, 1184, 1188, 1189, 1192, 1193, 1194,
    1196, 1197, 1199, 1200, 1202, 1203, 1205, 1211, 1213, 1216, 1217, 1218, 1220,
    1223, 1224, 1225, 1226, 1228, 1280, 1284]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
