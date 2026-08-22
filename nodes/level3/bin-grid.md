---
confidence: 1.0
id: "level3:bin-grid"
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
  how: '`path.read_text(encoding=''utf-8'')` at line 110'
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
  how: 'defines public function `find_project_root` at line 55, signature: (start:
    Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git
  how: 'defines public function `git` at line 63, signature: (root: Path, *args: str,
    input_text: str | None=None, check: bool=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sanitize
  how: 'defines public function `sanitize` at line 73, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_ref
  how: 'defines public function `node_ref` at line 101, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: session_ref
  how: 'defines public function `session_ref` at line 105, signature: (iter_n: str,
    agent: str, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_node_id
  how: 'defines public function `parse_node_id` at line 109, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ref_tip
  how: 'defines public function `ref_tip` at line 114, signature: (root: Path, ref:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ensure_repo
  how: 'defines public function `ensure_repo` at line 122, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_init
  how: 'defines public function `cmd_init` at line 129, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: commit_file
  how: 'defines public function `commit_file` at line 148, signature: (root: Path,
    path: Path, ref: str, msg_prefix: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_node_files
  how: 'defines public function `iter_node_files` at line 169, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_commit
  how: 'defines public function `cmd_commit` at line 173, signature: (root: Path,
    files: list[str], do_all: bool, session: tuple[str, str] | None, prefix: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_ref
  how: 'defines public function `resolve_ref` at line 201, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_log
  how: 'defines public function `cmd_log` at line 208, signature: (root: Path, node_id:
    str, n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_diff
  how: 'defines public function `cmd_diff` at line 213, signature: (root: Path, node_id:
    str, back: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_versions
  how: 'defines public function `cmd_versions` at line 221, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 226, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_sync
  how: 'defines public function `cmd_sync` at line 248, signature: (root: Path, remote:
    str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_log
  how: 'defines public function `cron_log` at line 262, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_lines
  how: 'defines public function `cron_lines` at line 266, signature: (root: Path,
    branch: str, mins: int, log: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_crontab
  how: defines public function `read_crontab` at line 277
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_crontab
  how: 'defines public function `write_crontab` at line 282, signature: (lines: list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_cron
  how: 'defines public function `cmd_cron` at line 290, signature: (root: Path, action:
    str, mins: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 315
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 20 `print()` call(s) at line(s) [137, 139, 141, 145, 152, 182, 186, 197, 198,
    210, 218, 223, 236, 244, 245, 259, 298, 302, 311, 312]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
