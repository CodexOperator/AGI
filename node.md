---
build_kind: code
confidence: 1.0
id: "build:tests-test-git-commit-guard"
mint_id: b1cddb63029140bd9414ee3321a88c8c
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_git_commit_guard.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_git_commit_guard.py"
type: build
---

`extensions/agi/tests/test_git_commit_guard.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_git_commit_guard.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shlex
  how: '`import shlex` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tempfile
  how: '`import tempfile` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ilu
  how: '`import importlib.util as _ilu` at line 41'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "dispatch.py"
  how: '`(BIN / "dispatch.py").read_text()` at line 417'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "dispatch.py"
  how: '`(BIN / "dispatch.py").read_text()` at line 425'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "dispatch.py"
  how: '`(BIN / "dispatch.py").read_text()` at line 433'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.read_text()` at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: hook_env
  how: defines public function `hook_env` at line 25
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_repo
  how: 'defines public function `temp_repo` at line 52, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: with_hook
  how: 'defines public function `with_hook` at line 65, signature: (repo: Path, hook_name:
    str=''pre-commit'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo_toplevel
  how: 'defines public function `repo_toplevel` at line 88, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_commit_allows_human_when_no_tier
  how: 'defines public function `test_pre_commit_allows_human_when_no_tier` at line
    101, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_commit_rejects_kid_in_project_repo
  how: 'defines public function `test_pre_commit_rejects_kid_in_project_repo` at line
    114, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: g11_repo
  how: 'defines public function `g11_repo` at line 130, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _graph_root
  how: 'defines private function `_graph_root` at line 148, signature: (g11_repo:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_commit_rejects_kid_in_g11_layout
  how: 'defines public function `test_pre_commit_rejects_kid_in_g11_layout` at line
    159, signature: (g11_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_push_rejects_kid_in_g11_layout
  how: 'defines public function `test_pre_push_rejects_kid_in_g11_layout` at line
    178, signature: (g11_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_commit_allows_kid_in_non_project_repo
  how: 'defines public function `test_pre_commit_allows_kid_in_non_project_repo` at
    line 194, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_commit_allows_kid_when_project_root_unset
  how: 'defines public function `test_pre_commit_allows_kid_when_project_root_unset`
    at line 216, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_commit_rejects_parent
  how: 'defines public function `test_pre_commit_rejects_parent` at line 236, signature:
    (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_commit_allows_parent_on_loop_branch
  how: 'defines public function `test_pre_commit_allows_parent_on_loop_branch` at
    line 251, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_commit_still_rejects_parent_on_loop_branch_in_wrong_repo
  how: 'defines public function `test_pre_commit_still_rejects_parent_on_loop_branch_in_wrong_repo`
    at line 277, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_commit_still_rejects_kid_on_loop_branch
  how: 'defines public function `test_pre_commit_still_rejects_kid_on_loop_branch`
    at line 299, signature: (g11_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_push_script_rejects_kid_in_project_repo
  how: 'defines public function `test_pre_push_script_rejects_kid_in_project_repo`
    at line 319, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_push_script_allows_kid_in_non_project_repo
  how: 'defines public function `test_pre_push_script_allows_kid_in_non_project_repo`
    at line 334, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pre_push_script_allows_human
  how: defines public function `test_pre_push_script_allows_human` at line 350
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_git_read_commands_work_despite_hook
  how: 'defines public function `test_git_read_commands_work_despite_hook` at line
    362, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_hook_exits_zero_for_human_on_pre_push
  how: 'defines public function `test_hook_exits_zero_for_human_on_pre_push` at line
    393, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_env_contains_AGI_TIER
  how: defines public function `test_spawn_env_contains_AGI_TIER` at line 415
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_env_contains_GIT_CONFIG_for_kid
  how: defines public function `test_spawn_env_contains_GIT_CONFIG_for_kid` at line
    423
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_spawn_env_contains_AGI_PROJECT_ROOT_for_kid
  how: defines public function `test_spawn_env_contains_AGI_PROJECT_ROOT_for_kid`
    at line 431
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_git_config_hooks_path_rejects_commit_in_project
  how: 'defines public function `test_git_config_hooks_path_rejects_commit_in_project`
    at line 452, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_git_config_hooks_path_allows_commit_outside_project
  how: 'defines public function `test_git_config_hooks_path_allows_commit_outside_project`
    at line 476, signature: (temp_repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_dispatch
  how: defines private function `_load_dispatch` at line 510
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / "readme.md"
  how: '`(repo / "readme.md").write_text("# test")` at line 59'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dst
  how: '`dst.write_text(src.read_text())` at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_repo / "file2.md"
  how: '`(temp_repo / "file2.md").write_text("change")` at line 104'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_repo / "file3.md"
  how: '`(temp_repo / "file3.md").write_text("kid change")` at line 118'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Path(repo) / "readme.md"
  how: '`(Path(repo) / "readme.md").write_text("# test")` at line 138'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_dir / "config.json"
  how: '`(graph_dir / "config.json").write_text(''{"metric_primary": "x", "metric_unit":
    "", "best_direction": "higher"}'')` at line 144'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: g11_repo / "file_g11.md"
  how: '`(g11_repo / "file_g11.md").write_text("kid change in g11 repo")` at line
    165'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_repo / "file3.md"
  how: '`(temp_repo / "file3.md").write_text("kid change outside project")` at line
    204'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_repo / "file_no_root.md"
  how: '`(temp_repo / "file_no_root.md").write_text("no project root")` at line 224'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_repo / "file4.md"
  how: '`(temp_repo / "file4.md").write_text("parent change")` at line 240'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_repo / "file_loop.md"
  how: '`(temp_repo / "file_loop.md").write_text("parent loop-branch commit")` at
    line 265'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_repo / "file_loop2.md"
  how: '`(temp_repo / "file_loop2.md").write_text("change")` at line 287'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: g11_repo / "file_kid_loop.md"
  how: '`(g11_repo / "file_kid_loop.md").write_text("kid change on loop branch")`
    at line 306'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_repo / "file_status.md"
  how: '`(temp_repo / "file_status.md").write_text("staged change")` at line 365'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_repo / "file_gitcfg.md"
  how: '`(temp_repo / "file_gitcfg.md").write_text("git config test")` at line 456'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_repo / "file_outside.md"
  how: '`(temp_repo / "file_outside.md").write_text("outside project test")` at line
    487'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
