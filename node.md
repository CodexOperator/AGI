---
build_kind: code
confidence: 1.0
id: "build:tests-test-dispatch-dry-run"
mint_id: bc3102f78e1f4b8bae64170193784b20
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_dispatch_dry_run.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_dispatch_dry_run.py"
type: build
---

`extensions/agi/tests/test_dispatch_dry_run.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_dispatch_dry_run.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 21'
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
outputs:
- name: project
  how: 'defines public function `project` at line 59, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _run
  how: 'defines private function `_run` at line 68, signature: (project: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pi_dry_run_resolves_the_spawn_and_exits_zero
  how: 'defines public function `test_pi_dry_run_resolves_the_spawn_and_exits_zero`
    at line 75, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pi_dry_run_creates_no_session_dir
  how: 'defines public function `test_pi_dry_run_creates_no_session_dir` at line 87,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prompt_file_threads_the_carry_forward_addendum_into_the_command
  how: 'defines public function `test_prompt_file_threads_the_carry_forward_addendum_into_the_command`
    at line 94, signature: (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prompt_file_absent_adds_no_addendum_and_does_not_name_the_segment
  how: 'defines public function `test_prompt_file_absent_adds_no_addendum_and_does_not_name_the_segment`
    at line 118, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_claude_advisor_dry_run_resolves_model_effort_and_env
  how: 'defines public function `test_claude_advisor_dry_run_resolves_model_effort_and_env`
    at line 129, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_claude_advisor_dry_run_creates_no_session_dir
  how: 'defines public function `test_claude_advisor_dry_run_creates_no_session_dir`
    at line 155, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_takes_no_budget_slot
  how: 'defines public function `test_dry_run_takes_no_budget_slot` at line 164, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_explicit_harness_flag_wins_over_ladder_row
  how: 'defines public function `test_explicit_harness_flag_wins_over_ladder_row`
    at line 173, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_ladder_row_wins_without_harness_flag
  how: 'defines public function `test_ladder_row_wins_without_harness_flag` at line
    194, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_seat_row_wins_over_both_harness_and_ladder
  how: 'defines public function `test_seat_row_wins_over_both_harness_and_ladder`
    at line 205, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_exports_identity_and_readers_agree
  how: 'defines public function `test_dry_run_exports_identity_and_readers_agree`
    at line 222, signature: (project, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "config.json"
  how: '`(graph / "config.json").write_text(json.dumps(CONFIG))` at line 63'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "nodes" / ".geometry" / "ladder.md"
  how: '`(graph / "nodes" / ".geometry" / "ladder.md").write_text(LADDER)` at line
    64'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: add
  how: '`add.write_text("KID1 disproved hypothesis:x\nline two with && and \"quotes\"")`
    at line 104'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: seats
  how: '`seats.write_text("---\nseats:\n" "  - {name: liaison, tier: 1, role: parent,
    " "harness: pi, model: ~z-ai/glm-flash-latest, " "effort: \"\", settings: \"\"}\n---\n")`
    at line 210'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(CONFIG)` at line 63'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
