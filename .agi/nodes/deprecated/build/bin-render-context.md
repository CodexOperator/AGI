---
id: build:bin-render-context
mint_id: 9a16b6fc89254e53b9d6ca297b3afbb4
type: build
parents:
  - idea:engine-render-context
build_kind: code
confidence: 1.0
edited_by: director
origin: build-scan
payload_ref: extensions/agi/bin/render-context.py
status: deprecated
tags:
  - build
  - code
  - g2.1
thought_session: L1.05
title: "Build: extensions/agi/bin/render-context.py"
---
`extensions/agi/bin/render-context.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-render-context`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/render-context.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.defaultdict
  how: '`from collections import defaultdict` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: datetime.datetime
  how: '`from datetime import datetime` at line 58'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: datetime.timezone
  how: '`from datetime import timezone` at line 58'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.Node
  how: '`from graph_core import Node` at line 60'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.edge.Edge
  how: '`from graph_core.edge import Edge` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.graph.Graph
  how: '`from graph_core.graph import Graph` at line 62'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.loader.load_directory
  how: '`from graph_core.loader import load_directory` at line 63'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _ilu
  how: '`import importlib.util as _ilu` at line 64'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: renderers.build_representation
  how: '`from renderers import build_representation` at line 67'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: renderers.render_ascii
  how: '`from renderers import render_ascii` at line 67'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: metrics.DEFAULT_METRIC_PRIMARY
  how: '`from metrics import DEFAULT_METRIC_PRIMARY` at line 72'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: metrics.GAMEABLE_METRICS
  how: '`from metrics import GAMEABLE_METRICS` at line 72'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: metrics.outcome_coverage
  how: '`from metrics import outcome_coverage` at line 72'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: metrics.primary_metric_name
  how: '`from metrics import primary_metric_name` at line 72'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: metrics.read_config
  how: '`from metrics import read_config` at line 72'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 114'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 114'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: reads `sys.argv` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _LiveOnly
  how: defines private class `_LiveOnly` at line 82
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_graph_sqlite
  how: 'defines private function `_load_graph_sqlite` at line 108, signature: (nodes_dir:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 124
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _count_descendants
  how: 'defines private function `_count_descendants` at line 306, signature: (g:
    Graph, root: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out_path
  how: '`out_path.write_text("\n".join(out_lines), encoding="utf-8")` at line 301'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 7 `print()` call(s) at line(s) [127, 135, 138, 171, 173, 175, 302]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Retired 2026-09-03 (L1.05). bin/inject.py replaces it: the injected map now comes from the viewport own frame stream, so what a session is handed and what viewport --emit llm shows are the same object rather than two renderers that happen to agree. The nine briefing sections this file used to own as literal text moved to bin/briefing.py in L1.04, and INJECTION.md came out byte-identical -- which is what made this a deletion rather than a migration. Moved to deprecated/ rather than git rm -ed, per the standing rule: the mint id outlives the file, and deleting the node would leave its grid ref and any supersedes edges pointing at nothing. payload_ref is KEPT and still names the deleted path, because [build] requires it and the write gate refused to remove it -- correctly. Recovery, checked rather than asserted: grid.py payload build:bin-render-context --version N returns the file at v5, v8, v10-v13; the last is the 268-line version as it stood after the briefing extraction. It does NOT resolve at v1, which predates payloads being recorded at all -- so the honest claim is every version since payload recording began, not every version. Retiring this node is also what surfaced that broken_links and the deprecation convention had never been reconciled: a retired payload is not damage, and the metric now says so.
<!-- THOUGHT:END -->