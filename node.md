---
id: build:bin-zoom
mint_id: 748058ed9c1e41a7acc8c44672c6088e
type: build
parents:
  - idea:engine-zoom
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/bin/zoom.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/zoom.py"
---
`extensions/agi/bin/zoom.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-zoom`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/zoom.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 48'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 50'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 52'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 53'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 58'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_writer
  how: '`import node_writer` at line 59'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 83'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 333'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 83'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 333'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: inject_path
  how: '`inject_path.read_text(encoding="utf-8")` at line 476'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: default_runtime
  how: 'defines public function `default_runtime` at line 70, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: completion_contract
  how: 'defines public function `completion_contract` at line 89, signature: (runtime:
    str, iter_n, agent_id, target: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ZoomUnavailable
  how: defines public class `ZoomUnavailable` at line 202
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _add_graph_core_to_path
  how: 'defines private function `_add_graph_core_to_path` at line 298, signature:
    (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_wired_graph
  how: 'defines private function `_load_wired_graph` at line 315, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _bfs_neighbors
  how: 'defines private function `_bfs_neighbors` at line 361, signature: (g, target:
    str, hops: int=2)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _frontmatter_for
  how: 'defines private function `_frontmatter_for` at line 379, signature: (root:
    Path, dir_name: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 409
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _unavailable_message
  how: 'defines private function `_unavailable_message` at line 501, signature: (level:
    int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _compose_big
  how: 'defines private function `_compose_big` at line 512, signature: (inject_text:
    str, args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_path_hint
  how: 'defines private function `_node_path_hint` at line 535, signature: (root:
    Path, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _compose_small
  how: 'defines private function `_compose_small` at line 566, signature: (root: Path,
    args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _render_level
  how: 'defines private function `_render_level` at line 618, signature: (root: Path,
    args: argparse.Namespace, level: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out_path
  how: '`out_path.write_text(content, encoding="utf-8")` at line 496'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 7 `print()` call(s) at line(s) [443, 451, 467, 474, 480, 486, 497]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The kid contract was wrong in four ways, all found by kids obeying it.

**It never mentioned the verdict step.** `Acceptable: spawn one child node`
listed `mvp from exp` — advertising exactly the shortcut `goal:s22` closes —
and omitted `verdict` entirely, so no kid was ever told that step exists. Now
the full chain, `verdict from exp` and `mvp from verdict` both present, checked
by a test that reads the contract and the spawn gate together and asserts every
route advertised is a route the gate approves.

**`--evidence-runs` was absent from the `done` template.** It is load-bearing:
without it the gate reads no evidence and a `proved` is silently demoted. A kid
had to discover an undocumented flag to make a decisive verdict stick. That is a
live candidate explanation for `evidence_fraction` sitting near 0.21 corpus-wide
— an unusable interface, not indiscipline. The template now carries the flag,
what it takes, and that unresolvable ids and bare counts buy nothing.

**It accused kids of a bug in this engine.** "Do not also write that sentence
into the body — four kids in a row did, and it lands twice" shipped to every
agent, with a count. The duplication was two engine writers appending
unconditionally. Replaced with a statement of the behaviour.

**Cite the run, not yourself** is new, and words are all it is: the gate still
accepts `evidence_runs: [<my own id>]`, which is the `goal:g7.3` hole one
substitution later.
<!-- THOUGHT:END -->