---
id: build:bin-spawn-gate
mint_id: 79cb1a7ee8f949d8b272e894bb4e7a7e
type: build
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/bin/spawn_gate.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/spawn_gate.py"
---
`extensions/agi/bin/spawn_gate.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/spawn_gate.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 73'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dataclasses.dataclass
  how: '`from dataclasses import dataclass` at line 76'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dataclasses.field
  how: '`from dataclasses import field` at line 76'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 77'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 81'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 226'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 235'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: reads `sys.argv` / builds an `argparse.ArgumentParser` (module-wide, no single
    call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: canonical_type
  how: 'defines public function `canonical_type` at line 103, signature: (name)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Rule
  how: defines public class `Rule` at line 118
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: SpawnSchema
  how: defines public class `SpawnSchema` at line 141
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Geometry
  how: defines public class `Geometry` at line 176
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: SpawnRules
  how: defines public class `SpawnRules` at line 209
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_frontmatter
  how: 'defines private function `_read_frontmatter` at line 221, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_min_by_type
  how: 'defines private function `_parse_min_by_type` at line 241, signature: (raw,
    allowed: frozenset, max_p: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_parent_shapes
  how: 'defines private function `_parse_parent_shapes` at line 285, signature: (raw,
    allowed: frozenset, min_p: int, max_p: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_rule
  how: 'defines private function `_parse_rule` at line 328, signature: (block, variant:
    str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _display
  how: 'defines private function `_display` at line 362, signature: (path: Path, root:
    Path | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_spawn_rules
  how: 'defines public function `load_spawn_rules` at line 371, signature: (schemas_dir,
    root=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_geometry
  how: 'defines private function `_parse_geometry` at line 455, signature: (fm: dict,
    src: str, rules: SpawnRules)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _shape_key
  how: 'defines private function `_shape_key` at line 477, signature: (type_name:
    str, variant: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: canonical_shape_key
  how: 'defines public function `canonical_shape_key` at line 482, signature: (value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _check_against_geometry
  how: 'defines private function `_check_against_geometry` at line 501, signature:
    (schema: SpawnSchema, geo: Geometry)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_type_index
  how: 'defines public function `build_type_index` at line 523, signature: (nodes_dir)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_nodes_root
  how: 'defines public function `resolve_nodes_root` at line 545, signature: (root,
    schemas_dir=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: SpawnResult
  how: defines public class `SpawnResult` at line 574
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_spawn
  how: 'defines public function `check_spawn` at line 598, signature: (node_type,
    parents, *, rules: SpawnRules, type_index: dict | None=None, fm: dict | None=None,
    node_id: str='''', bypass: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _reject_message
  how: 'defines private function `_reject_message` at line 819, signature: (res: SpawnResult,
    shape: str, schema: SpawnSchema)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: announce
  how: 'defines public function `announce` at line 826, signature: (res: SpawnResult,
    stream=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: announce_schema_errors
  how: 'defines public function `announce_schema_errors` at line 851, signature: (rules:
    SpawnRules, stream=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stamp
  how: 'defines public function `stamp` at line 859, signature: (fm: dict, res: SpawnResult)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: gate_for_root
  how: 'defines public function `gate_for_root` at line 875, signature: (root, nodes_dir=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _cli
  how: 'defines private function `_cli` at line 884, signature: (argv)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_root
  how: defines private function `_find_root` at line 946
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 15 `print()` call(s) at line(s) [837, 839, 842, 845, 847, 855, 912, 913, 914,
    918, 920, 923, 926, 930, 950]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.