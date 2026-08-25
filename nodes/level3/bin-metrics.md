---
confidence: 1.0
id: "level3:bin-metrics"
mint_id: 2f7402938a954f18b115d44b1a632e6e
origin: level3-scan
parents:
  - idea:engine-metrics
payload_ref: extensions/agi/bin/metrics.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/bin/metrics.py"
type: level3
---

`extensions/agi/bin/metrics.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-metrics`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
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
- name: sys
  how: '`import sys` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.defaultdict
  how: '`from collections import defaultdict` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.DECISIVE_VERDICTS
  how: '`from evidence_gate import DECISIVE_VERDICTS` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.build_corpus
  how: '`from evidence_gate import build_corpus` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.normalize_evidence_runs
  how: '`from evidence_gate import normalize_evidence_runs` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.shadow_verdict_fields
  how: '`from evidence_gate import shadow_verdict_fields` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text(encoding=''utf-8'')` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 227'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 126'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 227'
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
  how: 'defines private function `_load_graph` at line 47, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: longest_chain_length
  how: 'defines public function `longest_chain_length` at line 70, signature: (g)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _iter_frontmatter
  how: 'defines private function `_iter_frontmatter` at line 111, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_stats
  how: 'defines public function `evidence_stats` at line 133, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: config_path
  how: 'defines public function `config_path` at line 213, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_config
  how: 'defines public function `read_config` at line 222, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: primary_metric_name
  how: 'defines public function `primary_metric_name` at line 232, signature: (cfg:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goal_attribution
  how: 'defines public function `goal_attribution` at line 246, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: outcome_coverage
  how: 'defines public function `outcome_coverage` at line 330, signature: (mvp_count:
    int, hypothesis_count: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: compute
  how: 'defines public function `compute` at line 341, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: emit
  how: 'defines public function `emit` at line 381, signature: (root: Path, out=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_root
  how: 'defines private function `_find_root` at line 429, signature: (start: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 439, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 9 `print()` call(s) at line(s) [388, 395, 406, 415, 418, 421, 424, 425, 435]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
