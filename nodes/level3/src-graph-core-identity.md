---
confidence: 1.0
id: "level3:src-graph-core-identity"
mint_id: 3d0741824921496fb21882d0711fbb44
origin: level3-scan
parents:
  - idea:engine-graph-core
payload_ref: extensions/agi/src/graph_core/identity.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/src/graph_core/identity.py"
type: level3
---

`extensions/agi/src/graph_core/identity.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-graph-core`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/src/graph_core/identity.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hashlib
  how: '`import hashlib` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tempfile
  how: '`import tempfile` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: uuid
  how: '`import uuid` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: warnings
  how: '`import warnings` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Any
  how: '`from typing import Any` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Iterable
  how: '`from typing import Iterable` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Mapping
  how: '`from typing import Mapping` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Optional
  how: '`from typing import Optional` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: derive_slug
  how: 'defines public function `derive_slug` at line 43, signature: (source_text:
    str, min_tokens: int=DEFAULT_MIN_TOKENS, max_tokens: int=DEFAULT_MAX_TOKENS)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _build_id
  how: 'defines private function `_build_id` at line 64, signature: (type_prefix:
    str, slug: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: IdRegistry
  how: defines public class `IdRegistry` at line 68
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_id
  how: 'defines public function `mint_id` at line 113, signature: (type_prefix: str,
    source_text: str, registry: Optional[IdRegistry]=None, min_tokens: int=DEFAULT_MIN_TOKENS,
    max_tokens: int=DEFAULT_MAX_TOKENS)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _digest_int
  how: 'defines private function `_digest_int` at line 152, signature: (seed: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _to_base_alphabet
  how: 'defines private function `_to_base_alphabet` at line 166, signature: (value:
    int, width: int, alphabet: str=ALPHABET)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_address
  how: 'defines public function `mint_address` at line 177, signature: (seed: str,
    taken: set[str], *, width: int=DEFAULT_ADDRESS_WIDTH)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: supernode
  how: 'defines public function `supernode` at line 224, signature: (node_id: str,
    level: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: is_valid_address
  how: 'defines public function `is_valid_address` at line 235, signature: (value:
    str, *, width: int=DEFAULT_ADDRESS_WIDTH)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: plan_reid
  how: 'defines public function `plan_reid` at line 240, signature: (nodes: Iterable[Mapping[str,
    Any]], *, width: int=DEFAULT_ADDRESS_WIDTH, group_width: int=DEFAULT_GROUP_WIDTH,
    out_path: Optional[str | Path]=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_permanent_id
  how: defines public function `mint_permanent_id` at line 388
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: is_valid_mint_id
  how: 'defines public function `is_valid_mint_id` at line 426, signature: (value:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out_path
  how: '`out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + ''\n'',
    encoding=''utf-8'')` at line 358'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(result, indent=2, sort_keys=True)` at line 358'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
