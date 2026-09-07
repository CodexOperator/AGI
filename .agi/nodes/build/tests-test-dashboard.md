---
id: build:tests-test-dashboard
mint_id: c8fc12f318344ac39df3a96eda113819
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_dashboard.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_dashboard.py"
---
`extensions/agi/tests/test_dashboard.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_dashboard.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: signal
  how: '`import signal` at line 21'
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
- name: time
  how: '`import time` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _load
  how: 'defines private function `_load` at line 33, signature: (name, filename=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node
  how: 'defines private function `_node` at line 49, signature: (root, ntype, slug,
    fm_extra='''', parents=())'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 65, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _run
  how: 'defines private function `_run` at line 71, signature: (project, *args, timeout=30)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _snapshot
  how: 'defines private function `_snapshot` at line 82, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_running_the_dashboard_writes_nothing
  how: 'defines public function `test_running_the_dashboard_writes_nothing` at line
    89, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_chain_health_never_passes_a_graph_dir
  how: 'defines public function `test_chain_health_never_passes_a_graph_dir` at line
    123, signature: (monkeypatch, project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_evidence_resolution_is_general_not_a_synthetic_special_case
  how: 'defines public function `test_evidence_resolution_is_general_not_a_synthetic_special_case`
    at line 150, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bare_integer_evidence_runs_fails_closed
  how: 'defines public function `test_bare_integer_evidence_runs_fails_closed` at
    line 173, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pending_excluded_but_inconclusive_counts_as_asserting
  how: 'defines public function `test_pending_excluded_but_inconclusive_counts_as_asserting`
    at line 194, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dangling_parent_reference_detected
  how: 'defines public function `test_dangling_parent_reference_detected` at line
    209, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_dangling_when_parent_resolves
  how: 'defines public function `test_no_dangling_when_parent_resolves` at line 216,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_duplicate_ids_on_disk_detected
  how: 'defines public function `test_duplicate_ids_on_disk_detected` at line 224,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_duplicates_in_a_clean_corpus
  how: 'defines public function `test_no_duplicates_in_a_clean_corpus` at line 238,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goal_with_no_descendants_is_a_stub
  how: 'defines public function `test_goal_with_no_descendants_is_a_stub` at line
    248, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goal_with_descendants_is_real_and_reports_furthest_stage
  how: 'defines public function `test_goal_with_descendants_is_real_and_reports_furthest_stage`
    at line 259, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_seed_that_does_not_resolve_is_counted_separately
  how: 'defines public function `test_seed_that_does_not_resolve_is_counted_separately`
    at line 274, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_metrics_section_matches_metrics_py_directly
  how: 'defines public function `test_metrics_section_matches_metrics_py_directly`
    at line 290, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_section_flag_prints_only_that_section
  how: 'defines public function `test_section_flag_prints_only_that_section` at line
    305, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_invalid_section_name_is_rejected
  how: 'defines public function `test_invalid_section_name_is_rejected` at line 315,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_color_flag_strips_ansi
  how: 'defines public function `test_no_color_flag_strips_ansi` at line 321, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_piped_output_has_no_ansi_even_without_the_flag
  how: 'defines public function `test_piped_output_has_no_ansi_even_without_the_flag`
    at line 328, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_project_config_errors_cleanly
  how: 'defines public function `test_missing_project_config_errors_cleanly` at line
    336, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_watch_exits_cleanly_on_sigint
  how: 'defines public function `test_watch_exits_cleanly_on_sigint` at line 344,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_watch_default_interval_is_ten_seconds
  how: 'defines public function `test_watch_default_interval_is_ten_seconds` at line
    363, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_empty_corpus_does_not_crash
  how: 'defines public function `test_empty_corpus_does_not_crash` at line 373, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_narrow_terminal_does_not_crash
  how: 'defines public function `test_narrow_terminal_does_not_crash` at line 379,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_project_without_git_falls_back_to_mtime
  how: 'defines public function `test_project_without_git_falls_back_to_mtime` at
    line 392, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f"{slug}.md"
  how: '`(d / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")` at line
    60'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 66'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f"{slug}.md"
  how: '`(d / f"{slug}.md").write_text( ''---\nid: "idea:dup"\ntype: idea\n---\nbody\n'',
    encoding="utf-8")` at line 228'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.