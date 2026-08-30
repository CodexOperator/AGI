---
build_kind: code
confidence: 1.0
id: "build:bin-spawn-gate"
mint_id: 79cb1a7ee8f949d8b272e894bb4e7a7e
origin: build-scan
payload_ref: extensions/agi/bin/spawn_gate.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/spawn_gate.py"
type: build
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
  how: '`path.read_text(encoding="utf-8")` at line 219'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 228'
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
  how: defines public class `SpawnSchema` at line 134
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Geometry
  how: defines public class `Geometry` at line 169
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: SpawnRules
  how: defines public class `SpawnRules` at line 202
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_frontmatter
  how: 'defines private function `_read_frontmatter` at line 214, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_min_by_type
  how: 'defines private function `_parse_min_by_type` at line 234, signature: (raw,
    allowed: frozenset, max_p: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_rule
  how: 'defines private function `_parse_rule` at line 278, signature: (block, variant:
    str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _display
  how: 'defines private function `_display` at line 306, signature: (path: Path, root:
    Path | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_spawn_rules
  how: 'defines public function `load_spawn_rules` at line 315, signature: (schemas_dir,
    root=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_geometry
  how: 'defines private function `_parse_geometry` at line 399, signature: (fm: dict,
    src: str, rules: SpawnRules)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _shape_key
  how: 'defines private function `_shape_key` at line 421, signature: (type_name:
    str, variant: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: canonical_shape_key
  how: 'defines public function `canonical_shape_key` at line 426, signature: (value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _check_against_geometry
  how: 'defines private function `_check_against_geometry` at line 445, signature:
    (schema: SpawnSchema, geo: Geometry)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_type_index
  how: 'defines public function `build_type_index` at line 467, signature: (nodes_dir)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_nodes_root
  how: 'defines public function `resolve_nodes_root` at line 489, signature: (root,
    schemas_dir=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: SpawnResult
  how: defines public class `SpawnResult` at line 518
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_spawn
  how: 'defines public function `check_spawn` at line 542, signature: (node_type,
    parents, *, rules: SpawnRules, type_index: dict | None=None, fm: dict | None=None,
    node_id: str='''', bypass: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _reject_message
  how: 'defines private function `_reject_message` at line 734, signature: (res: SpawnResult,
    shape: str, schema: SpawnSchema)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: announce
  how: 'defines public function `announce` at line 741, signature: (res: SpawnResult,
    stream=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: announce_schema_errors
  how: 'defines public function `announce_schema_errors` at line 766, signature: (rules:
    SpawnRules, stream=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stamp
  how: 'defines public function `stamp` at line 774, signature: (fm: dict, res: SpawnResult)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: gate_for_root
  how: 'defines public function `gate_for_root` at line 790, signature: (root, nodes_dir=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _cli
  how: 'defines private function `_cli` at line 799, signature: (argv)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_root
  how: defines private function `_find_root` at line 861
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 15 `print()` call(s) at line(s) [752, 754, 757, 760, 762, 770, 827, 828, 829,
    833, 835, 838, 841, 845, 865]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
