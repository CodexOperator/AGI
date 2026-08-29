---
build_kind: code
confidence: 1.0
id: "build:bin-metrics"
mint_id: 2f7402938a954f18b115d44b1a632e6e
origin: build-scan
parents:
  - idea:engine-metrics
payload_ref: extensions/agi/bin/metrics.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/metrics.py"
type: build
---

`extensions/agi/bin/metrics.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-metrics`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/metrics.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.defaultdict
  how: '`from collections import defaultdict` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.DECISIVE_VERDICTS
  how: '`from evidence_gate import DECISIVE_VERDICTS` at line 36'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.build_corpus
  how: '`from evidence_gate import build_corpus` at line 36'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.normalize_evidence_runs
  how: '`from evidence_gate import normalize_evidence_runs` at line 36'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.shadow_verdict_fields
  how: '`from evidence_gate import shadow_verdict_fields` at line 36'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(root.joinpath(*PUBLISH_STATE_PATH).read_text(encoding="utf-8"))`
    at line 311'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text(encoding="utf-8")` at line 207'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text(encoding="utf-8")` at line 245'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root.joinpath(*PUBLISH_STATE_PATH)
  how: '`root.joinpath(*PUBLISH_STATE_PATH).read_text(encoding="utf-8")` at line 311'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 579'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 216'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 579'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: reads `sys.argv` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _load_graph
  how: 'defines private function `_load_graph` at line 137, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: longest_chain_length
  how: 'defines public function `longest_chain_length` at line 160, signature: (g)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _iter_frontmatter
  how: 'defines private function `_iter_frontmatter` at line 201, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: thought_stats
  how: 'defines public function `thought_stats` at line 227, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_lifecycle_stats
  how: 'defines public function `node_lifecycle_stats` at line 260, signature: (nodes_dir:
    Path, node_count: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: normalize_reason
  how: 'defines public function `normalize_reason` at line 289, signature: (value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_publish_state
  how: 'defines public function `read_publish_state` at line 303, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: publish_stats
  how: 'defines public function `publish_stats` at line 317, signature: (root: Path,
    now: float | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_out
  how: 'defines private function `_git_out` at line 365, signature: (repo: Path, *args:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: unpushed_commits
  how: 'defines public function `unpushed_commits` at line 382, signature: (repo:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: push_gap_stats
  how: 'defines public function `push_gap_stats` at line 448, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_stats
  how: 'defines public function `evidence_stats` at line 485, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: config_path
  how: 'defines public function `config_path` at line 565, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_config
  how: 'defines public function `read_config` at line 574, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: primary_metric_name
  how: 'defines public function `primary_metric_name` at line 584, signature: (cfg:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goal_attribution
  how: 'defines public function `goal_attribution` at line 598, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: outcome_coverage
  how: 'defines public function `outcome_coverage` at line 682, signature: (mvp_count:
    int, hypothesis_count: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: compute
  how: 'defines public function `compute` at line 693, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: emit
  how: 'defines public function `emit` at line 749, signature: (root: Path, out=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_root
  how: 'defines private function `_find_root` at line 854, signature: (start: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 864, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 13 `print()` call(s) at line(s) [756, 763, 774, 783, 801, 813, 828, 840, 843,
    846, 849, 850, 860]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
