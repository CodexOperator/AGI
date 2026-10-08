---
id: build:bin-crons
mint_id: 28192386ba0b4fa4915a9ee28f2e1eca
type: build
build_kind: code
confidence: 1.0
edited_by: a00-e8298f7f
origin: build-scan
payload_ref: extensions/agi/bin/crons.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/crons.py"
---
`extensions/agi/bin/crons.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/crons.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 70'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 72'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: difflib
  how: '`import difflib` at line 73'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hashlib
  how: '`import hashlib` at line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 76'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 77'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 80'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 82'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 128'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 135'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text(encoding="utf-8")` at line 362'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: CronsError
  how: defines public class `CronsError` at line 98
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_path
  how: 'defines private function `_node_path` at line 112, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_frontmatter
  how: 'defines private function `_parse_frontmatter` at line 116, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_crons_node
  how: 'defines public function `load_crons_node` at line 143, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _schedule_expr
  how: 'defines private function `_schedule_expr` at line 218, signature: (job: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_branch
  how: 'defines public function `resolve_branch` at line 227, signature: (git_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _require_git_repo
  how: 'defines private function `_require_git_repo` at line 251, signature: (git_dir:
    Path, why: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _require_dir
  how: 'defines private function `_require_dir` at line 256, signature: (path: Path,
    why: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project_hash
  how: 'defines public function `project_hash` at line 264, signature: (repo_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: block_markers
  how: 'defines public function `block_markers` at line 270, signature: (repo_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _log_path
  how: 'defines private function `_log_path` at line 277, signature: (repo_root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_managed_lines
  how: 'defines public function `render_managed_lines` at line 283, signature: (root:
    Path, repo_root: Path, engine_root: Path, node: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_crontab
  how: 'defines public function `read_crontab` at line 354, signature: (crontab_file:
    Path | str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_crontab
  how: 'defines public function `write_crontab` at line 367, signature: (lines: list[str],
    crontab_file: Path | str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: split_managed_block
  how: 'defines public function `split_managed_block` at line 385, signature: (lines:
    list[str], begin: str, end: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _resolve
  how: 'defines private function `_resolve` at line 411, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_apply
  how: 'defines public function `cmd_apply` at line 421, signature: (root: Path, crontab_file:
    Path | str | None=None, dry_run: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_show
  how: 'defines public function `cmd_show` at line 453, signature: (root: Path, crontab_file:
    Path | str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_remove
  how: 'defines public function `cmd_remove` at line 480, signature: (root: Path,
    crontab_file: Path | str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 496, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Path(crontab_file)
  how: '`Path(crontab_file).write_text(text, encoding="utf-8")` at line 378'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 8 `print()` call(s) at line(s) [522, 532, 536, 539, 541, 543, 546, 549]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L4.123 fix-only re-dispatch: crons.py apply now actually RUNS systemctl --user daemon-reload + enable --now / disable --now behind crons_live (residue b); the grid_sync self-reapply line passes --unit-dir so crons_live:false genuinely stops the unit; reconcile_units calls a PATH-resolved systemctl (a fake in tests), written/removes the unit file first, and under --dry-run records intent without running.
<!-- THOUGHT:END -->
