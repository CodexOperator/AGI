---
id: build:tests-test-backfill-mint-ids
mint_id: 121330ced79b44bea0069070f717f35d
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_backfill_mint_ids.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_backfill_mint_ids.py"
---
`extensions/agi/tests/test_backfill_mint_ids.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_backfill_mint_ids.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 6'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 7'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(text.split("---", 2)[1])` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_a
  how: '`node_a.read_bytes()` at line 52'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_b
  how: '`node_b.read_bytes()` at line 83'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_a
  how: '`node_a.read_bytes()` at line 94'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_a
  how: '`node_a.read_bytes()` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_a
  how: '`node_a.read_text()` at line 78'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_b
  how: '`node_b.read_bytes()` at line 87'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_a
  how: '`node_a.read_bytes()` at line 100'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: junk
  how: '`junk.read_text()` at line 114'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: run
  how: 'defines public function `run` at line 23, signature: (project: Path, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fm_of
  how: 'defines public function `fm_of` at line 30, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 36, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_mints_nothing_on_disk
  how: 'defines public function `test_dry_run_mints_nothing_on_disk` at line 50, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_adds_mint_id_and_preserves_every_other_field
  how: 'defines public function `test_write_adds_mint_id_and_preserves_every_other_field`
    at line 63, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_with_existing_mint_id_is_never_touched
  how: 'defines public function `test_node_with_existing_mint_id_is_never_touched`
    at line 81, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_idempotent_second_write_run_changes_nothing
  how: 'defines public function `test_idempotent_second_write_run_changes_nothing`
    at line 91, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unparseable_frontmatter_is_reported_and_skipped
  how: 'defines public function `test_unparseable_frontmatter_is_reported_and_skipped`
    at line 105, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_nodes_dir_errors
  how: 'defines public function `test_missing_nodes_dir_errors` at line 117, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_backfill_function_returns_counts_matching_report
  how: 'defines public function `test_backfill_function_returns_counts_matching_report`
    at line 123, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nodes / "a.md"
  how: '`(nodes / "a.md").write_text( ''---\nconfidence: 1.0\nid: "idea:a"\norigin:
    level3-scan\n'' ''parents:\n  - goal:g2.5\ntags:\n  - t1\n  - t2\ntitle: "A"\ntype:
    idea\n'' ''---\n\nBody text for A, unchanged by backfill.\n'' )` at line 39'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nodes / "b.md"
  how: '`(nodes / "b.md").write_text( ''---\nid: "idea:b"\nmint_id: deadbeefdeadbeefdeadbeefdeadbeef\ntype:
    idea\n---\n\nAlready minted.\n'' )` at line 44'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: junk
  how: '`junk.write_text("no frontmatter delimiter at all\n")` at line 107'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.