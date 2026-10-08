---
id: build:bin-post-wire
mint_id: 7cdc45cecea04eef914b2972700963e1
type: build
parents:
  - idea:engine-post-wire
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/bin/post_wire.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/post_wire.py"
---
`extensions/agi/bin/post_wire.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-post-wire`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
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
- name: importlib.util
  how: '`import importlib.util` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: completion
  how: '`import completion` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate
  how: '`import evidence_gate` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_writer
  how: '`import node_writer` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: spawn_gate
  how: '`import spawn_gate` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest_path.read_text())` at line 270'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(path.read_text())` at line 204'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.read_text()` at line 270'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 133'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 204'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding="utf-8")` at line 351'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parent_path
  how: '`parent_path.read_text(encoding="utf-8")` at line 435'
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
  how: 'defines private function `_find_root` at line 49, signature: (cwd: Path |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_graph_core
  how: defines private function `_load_graph_core` at line 57
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _slug_from_node_id
  how: 'defines private function `_slug_from_node_id` at line 71, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_file_path
  how: 'defines private function `_node_file_path` at line 78, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: MalformedNode
  how: defines public class `MalformedNode` at line 92
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_frontmatter
  how: 'defines private function `_read_frontmatter` at line 102, signature: (body:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_node
  how: 'defines private function `_write_node` at line 143, signature: (path: Path,
    fm: dict, body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _merged_agent
  how: 'defines private function `_merged_agent` at line 163, signature: (iter_dir:
    Path, entry: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _gate
  how: 'defines private function `_gate` at line 213, signature: (agent: dict, fm:
    dict, corpus)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_wire
  how: 'defines public function `cmd_wire` at line 261, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 520
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_path
  how: '`graph_path.write_text(json.dumps(graph_data, indent=2), encoding="utf-8")`
    at line 482'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(graph_data, indent=2)` at line 482'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 16 `print()` call(s) at line(s) [206, 267, 485, 486, 488, 489, 491, 493, 495,
    501, 503, 508, 511, 513, 515, 516]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Three changes on 2026-09-01, and two of them were repairs to the first.

**Completion became a graph event** (`goal:g4.6` clause 5). The agent filter was
`status != "done" -> continue`, i.e. gated on `cli.py done` having run. It now
also admits an agent whose node `is_complete`, so a kid that filled its node and
then died — API error, content filter, killed pid — is no longer discarded.
That is not hypothetical: it happened to the kid that wrote `completion.py`.
Admissions print, because a silent recovery would hide both the rescue and
whatever killed the kid.

**Then the same change broke two things, found by a kid's `struggles:` line.**
Making frontmatter primary meant re-wiring read back the normalized COUNT that
`evidence_gate.stamp` writes (`evidence_runs: 1`), and `goal:g7.3` resolves a
bare int to zero evidence on purpose — so a second wire silently demoted an
earned `proved`. And `fm.get("verdict") or agent.get(...)` treated `pending` as
a claim, letting a scaffold's placeholder outrank a verdict the agent actually
reported. Only a list counts as an evidence claim now, and `pending` counts as
the absence of one.

**Notes stopped landing twice.** This module appended `## Agent Notes`
unconditionally while `cli.py` separately appended the same text bare; both run
on every kid. The kid contract blamed kids for it by name and count. No kid was
doing it.
<!-- THOUGHT:END -->