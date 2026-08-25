---
confidence: 1.0
id: "level3:bin-post-wire"
mint_id: 7cdc45cecea04eef914b2972700963e1
origin: level3-scan
parents:
  - idea:engine-post-wire
payload_ref: extensions/agi/bin/post_wire.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/bin/post_wire.py"
type: level3
---

`extensions/agi/bin/post_wire.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-post-wire`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/post_wire.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate
  how: '`import evidence_gate` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: spawn_gate
  how: '`import spawn_gate` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest_path.read_text())` at line 132'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 90'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.read_text()` at line 132'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding=''utf-8'')` at line 182'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parent_path
  how: '`parent_path.read_text(encoding=''utf-8'')` at line 260'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _find_root
  how: 'defines private function `_find_root` at line 36, signature: (cwd: Path |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_graph_core
  how: defines private function `_load_graph_core` at line 45
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _slug_from_node_id
  how: 'defines private function `_slug_from_node_id` at line 59, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_file_path
  how: 'defines private function `_node_file_path` at line 66, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_frontmatter
  how: 'defines private function `_read_frontmatter` at line 82, signature: (body:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_node
  how: 'defines private function `_write_node` at line 94, signature: (path: Path,
    fm: dict, body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _gate
  how: 'defines private function `_gate` at line 102, signature: (agent: dict, fm:
    dict, corpus)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_wire
  how: 'defines public function `cmd_wire` at line 123, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 332
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text(content, encoding=''utf-8'')` at line 99'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_path
  how: '`graph_path.write_text(json.dumps(graph_data, indent=2), encoding=''utf-8'')`
    at line 302'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(graph_data, indent=2)` at line 302'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.dump
  how: '`yaml.dump(dict(fm), default_flow_style=False)` at line 97'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: vpath
  how: '`vpath.write_text(''---\n'' + yaml.dump(fm, default_flow_style=False) + ''---\n\n''
    + (notes or ''''), encoding=''utf-8'')` at line 247'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.dump
  how: '`yaml.dump(fm, default_flow_style=False)` at line 249'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 13 `print()` call(s) at line(s) [129, 305, 306, 308, 309, 311, 313, 315, 321,
    323, 325, 327, 328]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
