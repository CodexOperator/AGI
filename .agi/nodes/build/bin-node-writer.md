---

id: build:bin-node-writer
mint_id: 125d31c7fdb24e5383883aa2e0fbe3b2
type: build
parents:
  - goal:g7.16.1
  - mvp:dg3-m-marker-strings
  - build
  - code
  - goal:g2.1
build_kind: code
confidence: 1.0
edited_by: director-general-3
origin: build-scan
payload_ref: extensions/agi/bin/node_writer.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/node_writer.py"
---
`extensions/agi/bin/node_writer.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/node_writer.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 52'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: datetime
  how: '`import datetime` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hashlib
  how: '`import hashlib` at line 55'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 56'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 58'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 59'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dataclasses.dataclass
  how: '`from dataclasses import dataclass` at line 60'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dataclasses.field
  how: '`from dataclasses import field` at line 60'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: spawn_gate
  how: '`import spawn_gate` at line 64'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: frontmatter.split_frontmatter
  how: '`from frontmatter import split_frontmatter` at line 65'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.ensure_mint_id
  how: '`from graph_core.identity import ensure_mint_id` at line 71'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load("".join(l + "\n" for l in _render_value(k, "x")))` at line
    452'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.read_bytes()` at line 625'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dest
  how: '`dest.read_bytes()` at line 634'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(yaml_block)` at line 1073'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text(encoding="utf-8")` at line 812'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: canonical_node_type
  how: 'defines public function `canonical_node_type` at line 143, signature: (node_type)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_dir
  how: 'defines public function `node_dir` at line 155, signature: (root, node_type)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _build_id_index
  how: 'defines private function `_build_id_index` at line 166, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_node_file
  how: 'defines public function `find_node_file` at line 185, signature: (root, node_id)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _needs_quoting
  how: 'defines private function `_needs_quoting` at line 253, signature: (sval: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scalar
  how: 'defines private function `_scalar` at line 316, signature: (v)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _escape_yaml_linebreaks
  how: 'defines private function `_escape_yaml_linebreaks` at line 359, signature:
    (jtext: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _render_value
  how: 'defines private function `_render_value` at line 367, signature: (key: str,
    v, indent: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: writer_key_shape
  how: 'defines public function `writer_key_shape` at line 425, signature: (key)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render_frontmatter
  how: 'defines public function `render_frontmatter` at line 468, signature: (fm:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: NodeWrite
  how: defines public class `NodeWrite` at line 488
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: scaffold_hash
  how: 'defines public function `scaffold_hash` at line 530, signature: (body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_untouched_scaffold
  how: 'defines private function `_is_untouched_scaffold` at line 547, signature:
    (text: str, scaffold_body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ensure_payload
  how: 'defines public function `ensure_payload` at line 564, signature: (root, ref:
    str, location: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: replace_payload
  how: 'defines public function `replace_payload` at line 593, signature: (root, ref:
    str, source=None, *, location: str | None=None, data: bytes | None=None, mint_id:
    str='''', log_extra: dict | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_node
  how: 'defines public function `write_node` at line 670, signature: (root, node_type,
    slug, parents=None, *, extra_fm=None, body=None, heading=True, bypass=False, rules=None,
    type_index=None, fm_for_gate=None, on_exists=SKIP, announce=True, stamp=None,
    log_extra=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _stamp_env_fields
  how: 'defines private function `_stamp_env_fields` at line 884, signature: (fm:
    dict, *, current_season: int | None=None, stamp: dict | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: extract_thought
  how: 'defines public function `extract_thought` at line 989, signature: (body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: thought_blocks
  how: 'defines public function `thought_blocks` at line 999, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: thought_text
  how: 'defines public function `thought_text` at line 1004, signature: (body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: strip_thought
  how: 'defines public function `strip_thought` at line 1013, signature: (text: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: replace_thought
  how: 'defines public function `replace_thought` at line 1018, signature: (body:
    str, block: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _carry_thought
  how: 'defines private function `_carry_thought` at line 1029, signature: (old_body:
    str, new_body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _absorb_leading_frontmatter
  how: 'defines private function `_absorb_leading_frontmatter` at line 1041, signature:
    (fm: dict, body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _serialize_node
  how: 'defines private function `_serialize_node` at line 1085, signature: (fm_lines:
    list[str], body: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: assemble_node
  how: 'defines public function `assemble_node` at line 1108, signature: (fm: dict,
    body: str, *, old_body: str | None=None, set_fm: dict | None=None, unset_fm=())'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: update_node
  how: 'defines public function `update_node` at line 1127, signature: (root, node_id,
    *, set_fm=None, unset_fm=(), body=None, validate=True, announce=False, log_extra=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repair_mint
  how: 'defines public function `repair_mint` at line 1237, signature: (root, node_id,
    *, announce=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_project_root
  how: 'defines private function `_node_project_root` at line 1347, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _log_write
  how: 'defines private function `_log_write` at line 1367, signature: (root, operation:
    str, node_id: str, path: Path, text: str='''', *, mint_id: str='''', extra: dict
    | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_write
  how: 'defines public function `log_write` at line 1428, signature: (root, operation:
    str, node_id: str, path: Path, text: str='''', *, mint_id: str='''', extra: dict
    | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _log_relpath
  how: 'defines private function `_log_relpath` at line 1437, signature: (path: Path,
    root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _derive_title
  how: 'defines private function `_derive_title` at line 1447, signature: (slug: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: required_fields
  how: 'defines public function `required_fields` at line 1462, signature: (root,
    node_type)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: missing_required
  how: 'defines public function `missing_required` at line 1483, signature: (root,
    node_type, fm, node_id='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: seed_required
  how: 'defines public function `seed_required` at line 1512, signature: (root, node_type,
    fm, slug)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _section_text
  how: 'defines private function `_section_text` at line 1549, signature: (body: str,
    headings: tuple[str, ...])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: derive_required_from_body
  how: 'defines public function `derive_required_from_body` at line 1578, signature:
    (root, node_id, announce=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.write_text("")` at line 585'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dest
  how: '`dest.write_bytes(new)` at line 651'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(text, encoding="utf-8")` at line 867'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp
  how: '`tmp.write_text(text, encoding="utf-8")` at line 1223'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp
  how: '`tmp.write_text(text, encoding="utf-8")` at line 1299'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`open(log_path, "a")` at line 1422 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(entry, sort_keys=True)` at line 1423'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(i, ensure_ascii=False)` at line 407'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 3 `print()` call(s) at line(s) [840, 1187, 1307]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Council bundle 2 row M (director-general-3, mvp:dg3-m-marker-strings): the THOUGHT marker strings THOUGHT_BEGIN/THOUGHT_END now live in node_writer only, moved verbatim from snapshot-goals.py; snapshot-goals re-exports them and write.py's thought verb imports them. The GOALS render stays byte-identical. Bundle 1's column-0 definition (row B) is unchanged.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: reparented past complete goal:g7.16.1.2.7 -> ['goal:g7.16.1.2', 'mvp:dg3-m-marker-strings', 'build', 'code', 'g2.1']. -->
