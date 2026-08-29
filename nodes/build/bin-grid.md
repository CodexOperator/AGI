---
build_kind: code
confidence: 1.0
id: "build:bin-grid"
mint_id: 8e373f3131c74d8bb2602ba9986b9450
origin: build-scan
payload_ref: extensions/agi/bin/grid.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/grid.py"
type: build
---

`extensions/agi/bin/grid.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/grid.py
parse_ok: true
inputs:
- name: argparse
  how: '`import argparse` at line 45'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 46'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 47'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stat
  how: '`import stat` at line 48'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 49'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 50'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 56'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 309'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 242'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 250'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 258'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.read_bytes()` at line 904'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dst
  how: '`dst.read_bytes()` at line 863'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: find_project_root
  how: 'defines public function `find_project_root` at line 93, signature: (start:
    Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git
  how: 'defines public function `git` at line 118, signature: (root: Path, *args:
    str, input_text: str | None=None, check: bool=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _encode_component
  how: 'defines private function `_encode_component` at line 128, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sanitize
  how: 'defines public function `sanitize` at line 182, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sanitize_legacy
  how: 'defines private function `_sanitize_legacy` at line 211, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_ref
  how: 'defines public function `node_ref` at line 229, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_ref_legacy
  how: 'defines private function `_node_ref_legacy` at line 233, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: session_ref
  how: 'defines public function `session_ref` at line 237, signature: (iter_n: str,
    agent: str, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_node_id
  how: 'defines public function `parse_node_id` at line 241, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_mint_id
  how: 'defines public function `parse_mint_id` at line 246, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_payload_ref
  how: 'defines public function `parse_payload_ref` at line 254, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: default_engine_root
  how: defines public function `default_engine_root` at line 265
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_payload
  how: 'defines public function `resolve_payload` at line 273, signature: (root: Path,
    payload_ref: str, engine_root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_parents
  how: 'defines public function `parse_parents` at line 300, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_node_ref
  how: 'defines public function `mint_node_ref` at line 340, signature: (mint_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: MissingMintIdError
  how: defines public class `MissingMintIdError` at line 352
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_ref_for
  how: 'defines public function `write_ref_for` at line 362, signature: (path: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_id_index
  how: 'defines public function `build_id_index` at line 381, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_parent_mint_trailer
  how: 'defines public function `build_parent_mint_trailer` at line 393, signature:
    (path: Path, id_index: dict[str, Path])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ref_tip
  how: 'defines public function `ref_tip` at line 418, signature: (root: Path, ref:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git_mode
  how: 'defines public function `git_mode` at line 435, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hash_path
  how: 'defines public function `hash_path` at line 450, signature: (root: Path, path:
    Path, *, write: bool=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_tree_entry
  how: 'defines public function `read_tree_entry` at line 465, signature: (root: Path,
    rev: str, name: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: materialize_entry
  how: 'defines public function `materialize_entry` at line 490, signature: (dst:
    Path, mode: str, data: bytes)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tree_entries
  how: 'defines public function `tree_entries` at line 508, signature: (root: Path,
    path: Path, payload: Path | None, *, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_tree
  how: 'defines public function `build_tree` at line 527, signature: (root: Path,
    path: Path, payload: Path | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_tree
  how: 'defines public function `read_tree` at line 534, signature: (root: Path, rev:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ensure_repo
  how: 'defines public function `ensure_repo` at line 547, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_init
  how: 'defines public function `cmd_init` at line 554, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: commit_file
  how: 'defines public function `commit_file` at line 573, signature: (root: Path,
    path: Path, ref: str, msg_prefix: str, *, trailer: str | None=None, payload: Path
    | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_node_files
  how: 'defines public function `iter_node_files` at line 613, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_commit
  how: 'defines public function `cmd_commit` at line 617, signature: (root: Path,
    files: list[str], do_all: bool, session: tuple[str, str] | None, prefix: str='''',
    engine_root: Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _resolve_read_ref
  how: 'defines private function `_resolve_read_ref` at line 700, signature: (root:
    Path, path: Path, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_ref
  how: 'defines public function `resolve_ref` at line 718, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_log
  how: 'defines public function `cmd_log` at line 737, signature: (root: Path, node_id:
    str, n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_diff
  how: 'defines public function `cmd_diff` at line 742, signature: (root: Path, node_id:
    str, back: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_versions
  how: 'defines public function `cmd_versions` at line 750, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: version_rev
  how: 'defines public function `version_rev` at line 767, signature: (root: Path,
    ref: str, node_id: str, version: int | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_payload
  how: 'defines public function `cmd_payload` at line 784, signature: (root: Path,
    node_id: str, version: int | None, out: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine_tracked_files
  how: 'defines public function `engine_tracked_files` at line 809, signature: (engine_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_checkout
  how: 'defines public function `cmd_checkout` at line 816, signature: (root: Path,
    node_ids: list[str], do_all: bool, dest: str | None, engine_root: Path | None=None,
    unmanaged: bool=True, force: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 922, signature: (root: Path,
    engine_root: Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rename_ref
  how: 'defines private function `_rename_ref` at line 956, signature: (root: Path,
    old_ref: str, new_ref: str, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_migrate_refs
  how: 'defines public function `cmd_migrate_refs` at line 1006, signature: (root:
    Path, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_migrate_mint_refs
  how: 'defines public function `cmd_migrate_mint_refs` at line 1067, signature: (root:
    Path, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_sync
  how: 'defines public function `cmd_sync` at line 1162, signature: (root: Path, remote:
    str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_log
  how: 'defines public function `cron_log` at line 1176, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_lines
  how: 'defines public function `cron_lines` at line 1180, signature: (root: Path,
    branch: str, mins: int, log: Path, publish_engine: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_crontab
  how: defines public function `read_crontab` at line 1227
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_crontab
  how: 'defines public function `write_crontab` at line 1232, signature: (lines: list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_cron
  how: 'defines public function `cmd_cron` at line 1240, signature: (root: Path, action:
    str, mins: int, publish_engine: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 1267
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dst
  how: '`dst.write_bytes(data)` at line 504'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 37 `print()` call(s) at line(s) [562, 564, 566, 570, 596, 660, 664, 675, 684,
    695, 696, 739, 747, 761, 806, 874, 880, 886, 912, 917, 943, 952, 953, 1048, 1053,
    1057, 1062, 1132, 1144, 1148, 1152, 1157, 1173, 1249, 1253, 1263, 1264]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
