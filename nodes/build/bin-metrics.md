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
- name: re
  how: '`import re` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.defaultdict
  how: '`from collections import defaultdict` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.DECISIVE_VERDICTS
  how: '`from evidence_gate import DECISIVE_VERDICTS` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.build_corpus
  how: '`from evidence_gate import build_corpus` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.normalize_evidence_runs
  how: '`from evidence_gate import normalize_evidence_runs` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.shadow_verdict_fields
  how: '`from evidence_gate import shadow_verdict_fields` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(root.joinpath(*PUBLISH_STATE_PATH).read_text(encoding="utf-8"))`
    at line 264'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text(encoding="utf-8")` at line 160'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text(encoding="utf-8")` at line 198'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root.joinpath(*PUBLISH_STATE_PATH)
  how: '`root.joinpath(*PUBLISH_STATE_PATH).read_text(encoding="utf-8")` at line 264'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 412'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 169'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 412'
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
  how: 'defines private function `_load_graph` at line 90, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: longest_chain_length
  how: 'defines public function `longest_chain_length` at line 113, signature: (g)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _iter_frontmatter
  how: 'defines private function `_iter_frontmatter` at line 154, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: thought_stats
  how: 'defines public function `thought_stats` at line 180, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_lifecycle_stats
  how: 'defines public function `node_lifecycle_stats` at line 213, signature: (nodes_dir:
    Path, node_count: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: normalize_reason
  how: 'defines public function `normalize_reason` at line 242, signature: (value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_publish_state
  how: 'defines public function `read_publish_state` at line 256, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: publish_stats
  how: 'defines public function `publish_stats` at line 270, signature: (root: Path,
    now: float | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_stats
  how: 'defines public function `evidence_stats` at line 318, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: config_path
  how: 'defines public function `config_path` at line 398, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_config
  how: 'defines public function `read_config` at line 407, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: primary_metric_name
  how: 'defines public function `primary_metric_name` at line 417, signature: (cfg:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goal_attribution
  how: 'defines public function `goal_attribution` at line 431, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: outcome_coverage
  how: 'defines public function `outcome_coverage` at line 515, signature: (mvp_count:
    int, hypothesis_count: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: compute
  how: 'defines public function `compute` at line 526, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: emit
  how: 'defines public function `emit` at line 577, signature: (root: Path, out=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_root
  how: 'defines private function `_find_root` at line 655, signature: (start: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 665, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 11 `print()` call(s) at line(s) [584, 591, 602, 611, 629, 641, 644, 647, 650,
    651, 661]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
