---
confidence: 1.0
id: "level3:tests-test-grid"
origin: level3-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_grid.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/tests/test_grid.py"
type: level3
---

`extensions/agi/tests/test_grid.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_grid.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 3'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 4'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 5'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 6'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.read_text()` at line 68'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.read_text()` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: project
  how: 'defines public function `project` at line 17, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: versions
  how: 'defines public function `versions` at line 29, signature: (root, node_id)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_init_idempotent_and_refuses_non_repo
  how: 'defines public function `test_init_idempotent_and_refuses_non_repo` at line
    34, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_commit_creates_version_and_skips_unchanged
  how: 'defines public function `test_commit_creates_version_and_skips_unchanged`
    at line 40, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_grid_refs_stay_out_of_branch_listing
  how: 'defines public function `test_grid_refs_stay_out_of_branch_listing` at line
    48, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_edit_makes_v2_and_diff_shows_it
  how: 'defines public function `test_edit_makes_v2_and_diff_shows_it` at line 54,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_session_branch_is_separate_dimension
  how: 'defines public function `test_session_branch_is_separate_dimension` at line
    65, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_without_id_is_skipped
  how: 'defines public function `test_node_without_id_is_skipped` at line 75, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_commit_prefix_marks_auto_snapshots
  how: 'defines public function `test_commit_prefix_marks_auto_snapshots` at line
    81, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_refuses_ref_hostile_chars
  how: defines public function `test_sanitize_refuses_ref_hostile_chars` at line 89
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cron_lines_are_cwd_proof
  how: 'defines public function `test_cron_lines_are_cwd_proof` at line 94, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sync_pushes_grid_refs_and_sets_fetch_spec
  how: 'defines public function `test_sync_pushes_grid_refs_and_sets_fetch_spec` at
    line 105, signature: (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_find_project_root_accepts_canonical_and_legacy_config
  how: 'defines public function `test_find_project_root_accepts_canonical_and_legacy_config`
    at line 121, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_only_the_first_colon_separates
  how: defines public function `test_only_the_first_colon_separates` at line 138
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_node_ref_is_a_path_prefix_of_another
  how: defines public function `test_no_node_ref_is_a_path_prefix_of_another` at line
    151
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sanitize_is_injective_across_colon_and_dash
  how: defines public function `test_sanitize_is_injective_across_colon_and_dash`
    at line 161
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_escape_alphabet_cannot_be_forged
  how: defines public function `test_escape_alphabet_cannot_be_forged` at line 166
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'agi-tree.config.json'
  how: '`(tmp_path / ''agi-tree.config.json'').write_text(''{}'')` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / 'x.md'
  how: '`(d / ''x.md'').write_text(''---\nid: "idea:x"\ntype: idea\n---\n\nfirst thought\n'')`
    at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'agi-tree.config.json'
  how: '`(tmp_path / ''agi-tree.config.json'').write_text(''{}'')` at line 35'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.write_text(f.read_text().replace(''first thought'', ''second thought''))`
    at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f
  how: '`f.write_text(f.read_text() + ''\ndraft addition\n'')` at line 68'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'nodes' / 'idea' / 'noid.md'
  how: '`(project / ''nodes'' / ''idea'' / ''noid.md'').write_text(''no frontmatter
    here\n'')` at line 76'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: canonical / 'agi-tree.config.json'
  how: '`(canonical / ''agi-tree.config.json'').write_text(''{}'')` at line 129'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: legacy / 'autoresearch-tree.config.json'
  how: '`(legacy / ''autoresearch-tree.config.json'').write_text(''{}'')` at line
    130'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
