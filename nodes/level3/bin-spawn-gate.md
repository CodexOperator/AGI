---
confidence: 1.0
id: "level3:bin-spawn-gate"
mint_id: 79cb1a7ee8f949d8b272e894bb4e7a7e
origin: level3-scan
payload_ref: extensions/agi/bin/spawn_gate.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/bin/spawn_gate.py"
type: level3
---

`extensions/agi/bin/spawn_gate.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
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
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 185'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 194'
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
  how: 'defines public function `canonical_type` at line 99, signature: (name)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Rule
  how: defines public class `Rule` at line 114
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: SpawnSchema
  how: defines public class `SpawnSchema` at line 124
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Geometry
  how: defines public class `Geometry` at line 159
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: SpawnRules
  how: defines public class `SpawnRules` at line 168
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_frontmatter
  how: 'defines private function `_read_frontmatter` at line 180, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_rule
  how: 'defines private function `_parse_rule` at line 200, signature: (block, variant:
    str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _display
  how: 'defines private function `_display` at line 221, signature: (path: Path, root:
    Path | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_spawn_rules
  how: 'defines public function `load_spawn_rules` at line 230, signature: (schemas_dir,
    root=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_geometry
  how: 'defines private function `_parse_geometry` at line 314, signature: (fm: dict,
    src: str, rules: SpawnRules)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _shape_key
  how: 'defines private function `_shape_key` at line 331, signature: (type_name:
    str, variant: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: canonical_shape_key
  how: 'defines public function `canonical_shape_key` at line 336, signature: (value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _check_against_geometry
  how: 'defines private function `_check_against_geometry` at line 355, signature:
    (schema: SpawnSchema, geo: Geometry)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_type_index
  how: 'defines public function `build_type_index` at line 377, signature: (nodes_dir)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_nodes_root
  how: 'defines public function `resolve_nodes_root` at line 399, signature: (root,
    schemas_dir=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: SpawnResult
  how: defines public class `SpawnResult` at line 428
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_spawn
  how: 'defines public function `check_spawn` at line 452, signature: (node_type,
    parents, *, rules: SpawnRules, type_index: dict | None=None, fm: dict | None=None,
    node_id: str='''', bypass: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _reject_message
  how: 'defines private function `_reject_message` at line 605, signature: (res: SpawnResult,
    shape: str, schema: SpawnSchema)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: announce
  how: 'defines public function `announce` at line 612, signature: (res: SpawnResult,
    stream=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: announce_schema_errors
  how: 'defines public function `announce_schema_errors` at line 637, signature: (rules:
    SpawnRules, stream=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stamp
  how: 'defines public function `stamp` at line 645, signature: (fm: dict, res: SpawnResult)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: gate_for_root
  how: 'defines public function `gate_for_root` at line 661, signature: (root, nodes_dir=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _cli
  how: 'defines private function `_cli` at line 670, signature: (argv)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_root
  how: defines private function `_find_root` at line 735
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 15 `print()` call(s) at line(s) [623, 625, 628, 631, 633, 641, 698, 699, 700,
    704, 706, 709, 712, 716, 741]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
