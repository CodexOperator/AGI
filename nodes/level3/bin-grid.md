---
confidence: 1.0
id: "level3:bin-grid"
mint_id: 0c772dbafc4845e7ad419180519d4243
origin: level3-scan
parents:
  - idea:engine-grid
payload_ref: extensions/agi/bin/grid.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/bin/grid.py"
type: level3
---

`extensions/agi/bin/grid.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-grid`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
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
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 287'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 220'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 228'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 236'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.read_bytes()` at line 876'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dst
  how: '`dst.read_bytes()` at line 835'
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
  how: 'defines public function `find_project_root` at line 88, signature: (start:
    Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git
  how: 'defines public function `git` at line 96, signature: (root: Path, *args: str,
    input_text: str | None=None, check: bool=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _encode_component
  how: 'defines private function `_encode_component` at line 106, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sanitize
  how: 'defines public function `sanitize` at line 160, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sanitize_legacy
  how: 'defines private function `_sanitize_legacy` at line 189, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_ref
  how: 'defines public function `node_ref` at line 207, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_ref_legacy
  how: 'defines private function `_node_ref_legacy` at line 211, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: session_ref
  how: 'defines public function `session_ref` at line 215, signature: (iter_n: str,
    agent: str, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_node_id
  how: 'defines public function `parse_node_id` at line 219, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_mint_id
  how: 'defines public function `parse_mint_id` at line 224, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_payload_ref
  how: 'defines public function `parse_payload_ref` at line 232, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: default_engine_root
  how: defines public function `default_engine_root` at line 243
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_payload
  how: 'defines public function `resolve_payload` at line 251, signature: (root: Path,
    payload_ref: str, engine_root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_parents
  how: 'defines public function `parse_parents` at line 278, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_node_ref
  how: 'defines public function `mint_node_ref` at line 318, signature: (mint_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: MissingMintIdError
  how: defines public class `MissingMintIdError` at line 330
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_ref_for
  how: 'defines public function `write_ref_for` at line 340, signature: (path: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_id_index
  how: 'defines public function `build_id_index` at line 359, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_parent_mint_trailer
  how: 'defines public function `build_parent_mint_trailer` at line 371, signature:
    (path: Path, id_index: dict[str, Path])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ref_tip
  how: 'defines public function `ref_tip` at line 396, signature: (root: Path, ref:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git_mode
  how: 'defines public function `git_mode` at line 413, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hash_path
  how: 'defines public function `hash_path` at line 428, signature: (root: Path, path:
    Path, *, write: bool=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_tree_entry
  how: 'defines public function `read_tree_entry` at line 443, signature: (root: Path,
    rev: str, name: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: materialize_entry
  how: 'defines public function `materialize_entry` at line 462, signature: (dst:
    Path, mode: str, data: bytes)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tree_entries
  how: 'defines public function `tree_entries` at line 480, signature: (root: Path,
    path: Path, payload: Path | None, *, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_tree
  how: 'defines public function `build_tree` at line 499, signature: (root: Path,
    path: Path, payload: Path | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_tree
  how: 'defines public function `read_tree` at line 506, signature: (root: Path, rev:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ensure_repo
  how: 'defines public function `ensure_repo` at line 519, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_init
  how: 'defines public function `cmd_init` at line 526, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: commit_file
  how: 'defines public function `commit_file` at line 545, signature: (root: Path,
    path: Path, ref: str, msg_prefix: str, *, trailer: str | None=None, payload: Path
    | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_node_files
  how: 'defines public function `iter_node_files` at line 585, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_commit
  how: 'defines public function `cmd_commit` at line 589, signature: (root: Path,
    files: list[str], do_all: bool, session: tuple[str, str] | None, prefix: str='''',
    engine_root: Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _resolve_read_ref
  how: 'defines private function `_resolve_read_ref` at line 672, signature: (root:
    Path, path: Path, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_ref
  how: 'defines public function `resolve_ref` at line 690, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_log
  how: 'defines public function `cmd_log` at line 709, signature: (root: Path, node_id:
    str, n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_diff
  how: 'defines public function `cmd_diff` at line 714, signature: (root: Path, node_id:
    str, back: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_versions
  how: 'defines public function `cmd_versions` at line 722, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: version_rev
  how: 'defines public function `version_rev` at line 739, signature: (root: Path,
    ref: str, node_id: str, version: int | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_payload
  how: 'defines public function `cmd_payload` at line 756, signature: (root: Path,
    node_id: str, version: int | None, out: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine_tracked_files
  how: 'defines public function `engine_tracked_files` at line 781, signature: (engine_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_checkout
  how: 'defines public function `cmd_checkout` at line 788, signature: (root: Path,
    node_ids: list[str], do_all: bool, dest: str | None, engine_root: Path | None=None,
    unmanaged: bool=True, force: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 894, signature: (root: Path,
    engine_root: Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rename_ref
  how: 'defines private function `_rename_ref` at line 928, signature: (root: Path,
    old_ref: str, new_ref: str, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_migrate_refs
  how: 'defines public function `cmd_migrate_refs` at line 978, signature: (root:
    Path, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_migrate_mint_refs
  how: 'defines public function `cmd_migrate_mint_refs` at line 1039, signature: (root:
    Path, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_sync
  how: 'defines public function `cmd_sync` at line 1134, signature: (root: Path, remote:
    str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_log
  how: 'defines public function `cron_log` at line 1148, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_lines
  how: 'defines public function `cron_lines` at line 1152, signature: (root: Path,
    branch: str, mins: int, log: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_crontab
  how: defines public function `read_crontab` at line 1163
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_crontab
  how: 'defines public function `write_crontab` at line 1168, signature: (lines: list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_cron
  how: 'defines public function `cmd_cron` at line 1176, signature: (root: Path, action:
    str, mins: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 1201
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dst
  how: '`dst.write_bytes(data)` at line 476'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 37 `print()` call(s) at line(s) [534, 536, 538, 542, 568, 632, 636, 647, 656,
    667, 668, 711, 719, 733, 778, 846, 852, 858, 884, 889, 915, 924, 925, 1020, 1025,
    1029, 1034, 1104, 1116, 1120, 1124, 1129, 1145, 1184, 1188, 1197, 1198]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
