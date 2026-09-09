---
build_kind: code
confidence: 1.0
id: "build:tests-test-shared-state-worktree"
mint_id: 817b7662643f4002ad1c45d60d0c7d7f
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_shared_state_worktree.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_shared_state_worktree.py"
type: build
---

`extensions/agi/tests/test_shared_state_worktree.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_shared_state_worktree.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main_sess / "agent.json"
  how: '`(main_sess / "agent.json").read_text()` at line 231'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _git
  how: 'defines private function `_git` at line 36, signature: (cwd: Path, *args:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _make_project_repo
  how: 'defines private function `_make_project_repo` at line 41, signature: (tmp_path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _make_worktree
  how: 'defines private function `_make_worktree` at line 58, signature: (repo: Path,
    tmp_path: Path, name: str=''wt'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_secret
  how: 'defines private function `_write_secret` at line 64, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_env_shared_root_resolves_main_graph_from_a_worktree
  how: 'defines public function `test_env_shared_root_resolves_main_graph_from_a_worktree`
    at line 71, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_envfile_from_a_worktree_reads_the_main_checkout_dot_env
  how: 'defines public function `test_envfile_from_a_worktree_reads_the_main_checkout_dot_env`
    at line 85, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_envfile_shares_secrets_but_keeps_the_working_graph_fork
  how: 'defines public function `test_envfile_shares_secrets_but_keeps_the_working_graph_fork`
    at line 103, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_zoom_refusal_names_the_main_checkout_when_target_exists_there
  how: 'defines public function `test_zoom_refusal_names_the_main_checkout_when_target_exists_there`
    at line 134, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _commit_graph
  how: 'defines private function `_commit_graph` at line 167, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_from_a_worktree_resolves_the_main_session_record
  how: 'defines public function `test_cli_done_from_a_worktree_resolves_the_main_session_record`
    at line 192, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / "README"
  how: '`(repo / "README").write_text("x")` at line 48'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "config.json"
  how: '`(graph / "config.json").write_text(''{"metric_primary": "outcome_coverage"}'')`
    at line 51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo / ".env"
  how: '`(repo / ".env").write_text("OPENROUTER_API_KEY=sk-shared-main\n", encoding="utf-8")`
    at line 65'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: secrets_dir / "secrets.md"
  how: '`(secrets_dir / "secrets.md").write_text( "---\nlocations:\n  env_file:\n    path:
    <source_root>/.env\n" "---\n\n", encoding="utf-8")` at line 115'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hyp / "brand-new-brief.md"
  how: '`(hyp / "brand-new-brief.md").write_text( "---\nid: hypothesis:brand-new-brief\n"
    "type: hypothesis\ntitle: brand new brief\n---\n\nbody\n", encoding="utf-8" )`
    at line 147'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hyp / "h1.md"
  how: '`(hyp / "h1.md").write_text( "---\nid: hypothesis:h1\ntype: hypothesis\n---\n\nbody\n",
    encoding="utf-8")` at line 176'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: exp / "e1.md"
  how: '`(exp / "e1.md").write_text( "---\nid: experiment:e1\ntype: experiment\nparents:\n-
    hypothesis:h1\n" "---\n\nbody\n", encoding="utf-8")` at line 178'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: exp / "backer.md"
  how: '`(exp / "backer.md").write_text( "---\nid: experiment:backer\ntype: experiment\nparents:\n-
    hypothesis:h1\n" "---\n\nbody\n", encoding="utf-8")` at line 181'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main_sess / "agent.json"
  how: '`(main_sess / "agent.json").write_text(_AGENT_JSON, encoding="utf-8")` at
    line 216'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
