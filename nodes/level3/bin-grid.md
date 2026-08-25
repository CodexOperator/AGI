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
  how: '`import argparse` at line 39'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 40'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 41'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 42'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 43'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 215'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 194'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 202'
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
  how: 'defines public function `find_project_root` at line 62, signature: (start:
    Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git
  how: 'defines public function `git` at line 70, signature: (root: Path, *args: str,
    input_text: str | None=None, check: bool=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _encode_component
  how: 'defines private function `_encode_component` at line 80, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sanitize
  how: 'defines public function `sanitize` at line 134, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sanitize_legacy
  how: 'defines private function `_sanitize_legacy` at line 163, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_ref
  how: 'defines public function `node_ref` at line 181, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_ref_legacy
  how: 'defines private function `_node_ref_legacy` at line 185, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: session_ref
  how: 'defines public function `session_ref` at line 189, signature: (iter_n: str,
    agent: str, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_node_id
  how: 'defines public function `parse_node_id` at line 193, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_mint_id
  how: 'defines public function `parse_mint_id` at line 198, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_parents
  how: 'defines public function `parse_parents` at line 206, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_node_ref
  how: 'defines public function `mint_node_ref` at line 246, signature: (mint_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: MissingMintIdError
  how: defines public class `MissingMintIdError` at line 258
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_ref_for
  how: 'defines public function `write_ref_for` at line 268, signature: (path: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_id_index
  how: 'defines public function `build_id_index` at line 287, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_parent_mint_trailer
  how: 'defines public function `build_parent_mint_trailer` at line 299, signature:
    (path: Path, id_index: dict[str, Path])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ref_tip
  how: 'defines public function `ref_tip` at line 324, signature: (root: Path, ref:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ensure_repo
  how: 'defines public function `ensure_repo` at line 332, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_init
  how: 'defines public function `cmd_init` at line 339, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: commit_file
  how: 'defines public function `commit_file` at line 358, signature: (root: Path,
    path: Path, ref: str, msg_prefix: str, *, trailer: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_node_files
  how: 'defines public function `iter_node_files` at line 390, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_commit
  how: 'defines public function `cmd_commit` at line 394, signature: (root: Path,
    files: list[str], do_all: bool, session: tuple[str, str] | None, prefix: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _resolve_read_ref
  how: 'defines private function `_resolve_read_ref` at line 448, signature: (root:
    Path, path: Path, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_ref
  how: 'defines public function `resolve_ref` at line 466, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_log
  how: 'defines public function `cmd_log` at line 485, signature: (root: Path, node_id:
    str, n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_diff
  how: 'defines public function `cmd_diff` at line 490, signature: (root: Path, node_id:
    str, back: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_versions
  how: 'defines public function `cmd_versions` at line 498, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 512, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rename_ref
  how: 'defines private function `_rename_ref` at line 539, signature: (root: Path,
    old_ref: str, new_ref: str, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_migrate_refs
  how: 'defines public function `cmd_migrate_refs` at line 589, signature: (root:
    Path, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_migrate_mint_refs
  how: 'defines public function `cmd_migrate_mint_refs` at line 650, signature: (root:
    Path, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_sync
  how: 'defines public function `cmd_sync` at line 745, signature: (root: Path, remote:
    str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_log
  how: 'defines public function `cron_log` at line 759, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_lines
  how: 'defines public function `cron_lines` at line 763, signature: (root: Path,
    branch: str, mins: int, log: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_crontab
  how: defines public function `read_crontab` at line 774
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_crontab
  how: 'defines public function `write_crontab` at line 779, signature: (lines: list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_cron
  how: 'defines public function `cmd_cron` at line 787, signature: (root: Path, action:
    str, mins: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 812
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 30 `print()` call(s) at line(s) [347, 349, 351, 355, 372, 422, 426, 436, 444,
    445, 487, 495, 509, 527, 535, 536, 631, 636, 640, 645, 715, 727, 731, 735, 740,
    756, 795, 799, 808, 809]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
