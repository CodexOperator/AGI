---
build_kind: code
confidence: 1.0
id: "build:tests-test-spawn-budget"
mint_id: b0cf3ae62aa14fbaa8bcd75380d66544
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_spawn_budget.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_spawn_budget.py"
type: build
---

`extensions/agi/tests/test_spawn_budget.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_spawn_budget.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mp
  how: '`import multiprocessing as mp` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: spawn_budget
  how: '`import spawn_budget` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(lease.path.read_text())` at line 145'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(lease.path.read_text())` at line 360'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(lease.path.read_text())` at line 401'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lease.path
  how: '`lease.path.read_text()` at line 145'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lease.path
  how: '`lease.path.read_text()` at line 360'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lease.path
  how: '`lease.path.read_text()` at line 401'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f"/proc/{pid}/stat"
  how: '`open(f"/proc/{pid}/stat")` at line 178 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: root
  how: 'defines public function `root` at line 34, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_acquire_admits_up_to_the_cap_and_then_refuses
  how: 'defines public function `test_acquire_admits_up_to_the_cap_and_then_refuses`
    at line 43, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_acquire_refuses_while_paused_and_admits_once_resumed
  how: 'defines public function `test_acquire_refuses_while_paused_and_admits_once_resumed`
    at line 51, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_is_paused_reports_reason_and_actor
  how: 'defines public function `test_is_paused_reports_reason_and_actor` at line
    67, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_resume_without_a_prior_pause_is_a_no_op
  how: 'defines public function `test_resume_without_a_prior_pause_is_a_no_op` at
    line 78, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_refusal_while_paused_is_not_a_wait
  how: 'defines public function `test_refusal_while_paused_is_not_a_wait` at line
    83, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_refusal_is_not_a_wait
  how: 'defines public function `test_refusal_is_not_a_wait` at line 93, signature:
    (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_releasing_a_lease_frees_the_slot
  how: 'defines public function `test_releasing_a_lease_frees_the_slot` at line 107,
    signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_dead_agents_lease_is_reclaimed_without_anyone_releasing_it
  how: 'defines public function `test_a_dead_agents_lease_is_reclaimed_without_anyone_releasing_it`
    at line 118, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_reservation_is_held_by_the_dispatcher_until_a_pid_exists
  how: 'defines public function `test_a_reservation_is_held_by_the_dispatcher_until_a_pid_exists`
    at line 137, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_lease_whose_holder_died_before_spawning_is_reclaimed
  how: 'defines public function `test_a_lease_whose_holder_died_before_spawning_is_reclaimed`
    at line 152, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_zombie_lease_is_reclaimed_hypothesis_l3_zombie
  how: 'defines public function `test_a_zombie_lease_is_reclaimed_hypothesis_l3_zombie`
    at line 165, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_corrupt_lease_cannot_wedge_the_budget_shut
  how: 'defines public function `test_a_corrupt_lease_cannot_wedge_the_budget_shut`
    at line 191, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_max_live_prefers_its_own_key_then_falls_back_to_parallel
  how: defines public function `test_max_live_prefers_its_own_key_then_falls_back_to_parallel`
    at line 204
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _grab
  how: 'defines private function `_grab` at line 217, signature: (root_s: str, cap:
    int, n: int, idx: int, peaks)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_live_population_never_exceeds_the_bound_under_concurrency
  how: 'defines public function `test_the_live_population_never_exceeds_the_bound_under_concurrency`
    at line 234, signature: (root: Path, cap: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_second_independent_spawner_counts_against_the_first
  how: 'defines public function `test_a_second_independent_spawner_counts_against_the_first`
    at line 262, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_budget_dir_is_shared_across_a_linked_worktree
  how: 'defines public function `test_budget_dir_is_shared_across_a_linked_worktree`
    at line 291, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_attach_branch_records_branch_base_and_worktree_on_the_lease
  how: 'defines public function `test_attach_branch_records_branch_base_and_worktree_on_the_lease`
    at line 349, signature: (root)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_lease_without_an_iteration_is_loud_in_status
  how: 'defines public function `test_a_lease_without_an_iteration_is_loud_in_status`
    at line 366, signature: (root, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_lease_recorded_with_an_iteration_is_attributed
  how: 'defines public function `test_a_lease_recorded_with_an_iteration_is_attributed`
    at line 381, signature: (root, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_attach_branch_ignores_empty_fields
  how: 'defines public function `test_attach_branch_ignores_empty_fields` at line
    395, signature: (root)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_pause_then_status_shows_the_banner_then_resume_clears_it
  how: 'defines public function `test_cli_pause_then_status_shows_the_banner_then_resume_clears_it`
    at line 412, signature: (root, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_resume_with_nothing_to_resume_says_so
  how: 'defines public function `test_cli_resume_with_nothing_to_resume_says_so` at
    line 439, signature: (root, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "ghost.lease"
  how: '`(d / "ghost.lease").write_text(json.dumps({ "agent_id": "ghost", "holder_pid":
    dead.pid, "agent_pid": None, }))` at line 158'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "half-written.lease"
  how: '`(d / "half-written.lease").write_text("{not json")` at line 195'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / "README"
  how: '`(repo / "README").write_text("x")` at line 314'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "config.json"
  how: '`(graph / "config.json").write_text("{}")` at line 318'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(''{}'')` at line 372'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(''{}'')` at line 386'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(''{}'')` at line 414'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(''{}'')` at line 441'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({ "agent_id": "ghost", "holder_pid": dead.pid, "agent_pid": None,
    })` at line 158'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
