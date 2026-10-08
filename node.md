---
build_kind: code
confidence: 1.0
id: "build:bin-spawn-budget"
mint_id: ebfdaf4de89948b9b6d6219c2e47bc79
origin: build-scan
parents:
  - mvp:bin-modules
payload_ref: extensions/agi/bin/spawn_budget.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/spawn_budget.py"
type: build
---

`extensions/agi/bin/spawn_budget.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:bin-modules`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/spawn_budget.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: errno
  how: '`import errno` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fcntl
  how: '`import fcntl` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 35'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tempfile
  how: '`import tempfile` at line 36'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 37'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: contextlib.contextmanager
  how: '`from contextlib import contextmanager` at line 38'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dataclasses.dataclass
  how: '`from dataclasses import dataclass` at line 39'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 40'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 42'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(_pause_flag_path(root).read_text())` at line 103'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f"/proc/{pid}/stat"
  how: '`open(f"/proc/{pid}/stat")` at line 213 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(lease.path.read_text())` at line 375'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(lease.path.read_text())` at line 395'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(lease.path.read_text())` at line 408'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 498'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pause_flag_path(root)
  how: '`_pause_flag_path(root).read_text()` at line 103'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lease.path
  how: '`lease.path.read_text()` at line 375'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lease.path
  how: '`lease.path.read_text()` at line 395'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lease.path
  how: '`lease.path.read_text()` at line 408'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 498'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(p.read_text())` at line 258'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 258'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: budget_dir
  how: 'defines public function `budget_dir` at line 48, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pause_flag_path
  how: 'defines private function `_pause_flag_path` at line 81, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: is_paused
  how: 'defines public function `is_paused` at line 93, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pause
  how: 'defines public function `pause` at line 109, signature: (root: Path, reason:
    str='''', actor: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resume
  how: 'defines public function `resume` at line 120, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: max_live
  how: 'defines public function `max_live` at line 128, signature: (cfg: dict, default:
    int=DEFAULT_MAX_LIVE)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parent_max_kids
  how: 'defines public function `parent_max_kids` at line 145, signature: (cfg: dict,
    default: int=4)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Lease
  how: defines public class `Lease` at line 165
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _budget_lock
  how: 'defines private function `_budget_lock` at line 178, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pid_alive
  how: 'defines private function `_pid_alive` at line 196, signature: (pid: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _lease_is_live
  how: 'defines private function `_lease_is_live` at line 235, signature: (rec: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_leases
  how: 'defines private function `_read_leases` at line 251, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sweep_locked
  how: 'defines private function `_sweep_locked` at line 268, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _revoke_all
  how: 'defines private function `_revoke_all` at line 289, signature: (root: Path,
    hashes: list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: live_agents
  how: 'defines public function `live_agents` at line 309, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: live_count
  how: 'defines public function `live_count` at line 317, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: acquire
  how: 'defines public function `acquire` at line 321, signature: (root: Path, cap:
    int, agent_id: str, tier: str=''kid'', iter_n: int | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: attach_credential
  how: 'defines public function `attach_credential` at line 363, signature: (lease:
    Lease, key_hash: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: attach_branch
  how: 'defines public function `attach_branch` at line 382, signature: (lease: Lease,
    branch_ref: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: commit
  how: 'defines public function `commit` at line 404, signature: (lease: Lease, agent_pid:
    int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: release
  how: 'defines public function `release` at line 416, signature: (lease: Lease)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_lease
  how: 'defines private function `_write_lease` at line 433, signature: (path: Path,
    rec: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _atomic_write_json
  how: 'defines private function `_atomic_write_json` at line 438, signature: (path:
    Path, rec: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 452, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lock_path
  how: '`open(lock_path, "w")` at line 188 (mode=''w'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dump
  how: '`json.dump(rec, fh)` at line 445'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 8 `print()` call(s) at line(s) [336, 477, 484, 490, 492, 505, 507, 518]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
