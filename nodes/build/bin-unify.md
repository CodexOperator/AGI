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
  how: '`from __future__ import annotations` at line 68'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 70'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 71'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 72'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 73'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 77'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tree_gitignore
  how: '`tree_gitignore.read_text(encoding="utf-8")` at line 466'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine_gitignore
  how: '`engine_gitignore.read_text(encoding="utf-8")` at line 467'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tree_gitignore
  how: '`tree_gitignore.read_text(encoding="utf-8")` at line 529'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine_gitignore
  how: '`engine_gitignore.read_text(encoding="utf-8")` at line 530'
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
  how: defines public class `UnifyError` at line 108
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git
  how: 'defines private function `_git` at line 118, signature: (repo: Path, *args:
    str, check: bool=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _resolve_branch
  how: 'defines private function `_resolve_branch` at line 131, signature: (repo:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: count_grid_refs
  how: 'defines public function `count_grid_refs` at line 149, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_count
  how: 'defines private function `_node_count` at line 157, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _touches_a_real_repo
  how: 'defines private function `_touches_a_real_repo` at line 175, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _refuse
  how: 'defines private function `_refuse` at line 183, signature: (reason: str, detail:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: preflight
  how: 'defines public function `preflight` at line 187, signature: (engine: Path,
    tree: Path, *, force: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graft_graph
  how: 'defines public function `graft_graph` at line 255, signature: (engine: Path,
    tree: Path, *, remote_name: str=REMOTE_NAME)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: relocate_files
  how: 'defines public function `relocate_files` at line 308, signature: (engine:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _gitignore_blocks
  how: 'defines private function `_gitignore_blocks` at line 375, signature: (text:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _block_patterns
  how: 'defines private function `_block_patterns` at line 396, signature: (block:
    list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _filter_graph_block
  how: 'defines private function `_filter_graph_block` at line 400, signature: (block:
    list[str], *, dedupe_against: set[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: merge_gitignore
  how: 'defines public function `merge_gitignore` at line 429, signature: (tree_text:
    str, engine_text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_merged_gitignore
  how: 'defines public function `write_merged_gitignore` at line 458, signature: (engine:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fetch_grid_refs
  how: 'defines public function `fetch_grid_refs` at line 488, signature: (engine:
    Path, tree: Path, *, remote_name: str=REMOTE_NAME)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: remove_temp_remote
  how: 'defines public function `remove_temp_remote` at line 511, signature: (engine:
    Path, remote_name: str=REMOTE_NAME)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _plan
  how: 'defines private function `_plan` at line 521, signature: (engine: Path, tree:
    Path, pre: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _summarize
  how: 'defines private function `_summarize` at line 549, signature: (engine: Path,
    pre: dict, stages: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run_unify
  how: 'defines public function `run_unify` at line 570, signature: (engine: Path,
    tree: Path, *, yes: bool=False, force: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _print_human
  how: 'defines private function `_print_human` at line 606, signature: (report: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 633, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine_gitignore
  how: '`engine_gitignore.write_text(merged, encoding="utf-8")` at line 470'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(report, indent=2, default=str)` at line 661'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 15 `print()` call(s) at line(s) [608, 610, 614, 615, 618, 619, 620, 622, 623,
    625, 626, 628, 629, 657, 661]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
