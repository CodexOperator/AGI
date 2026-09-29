---
id: build:src-graph-core-identity
mint_id: 3d0741824921496fb21882d0711fbb44
type: build
parents:
  - goal:g7.16.1.1.4
  - idea:engine-graph-core
build_kind: code
confidence: 1.0
edited_by: director-general-3
origin: build-scan
payload_ref: extensions/agi/src/graph_core/identity.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/src/graph_core/identity.py"
---
`extensions/agi/src/graph_core/identity.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-graph-core`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
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
- name: sys
  how: '`import sys` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tempfile
  how: '`import tempfile` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: uuid
  how: '`import uuid` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: warnings
  how: '`import warnings` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Any
  how: '`from typing import Any` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Iterable
  how: '`from typing import Iterable` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Mapping
  how: '`from typing import Mapping` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Optional
  how: '`from typing import Optional` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: derive_slug
  how: 'defines public function `derive_slug` at line 44, signature: (source_text:
    str, min_tokens: int=DEFAULT_MIN_TOKENS, max_tokens: int=DEFAULT_MAX_TOKENS)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _build_id
  how: 'defines private function `_build_id` at line 65, signature: (type_prefix:
    str, slug: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: IdRegistry
  how: defines public class `IdRegistry` at line 69
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_id
  how: 'defines public function `mint_id` at line 114, signature: (type_prefix: str,
    source_text: str, registry: Optional[IdRegistry]=None, min_tokens: int=DEFAULT_MIN_TOKENS,
    max_tokens: int=DEFAULT_MAX_TOKENS)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _digest_int
  how: 'defines private function `_digest_int` at line 153, signature: (seed: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _to_base_alphabet
  how: 'defines private function `_to_base_alphabet` at line 167, signature: (value:
    int, width: int, alphabet: str=ALPHABET)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_address
  how: 'defines public function `mint_address` at line 178, signature: (seed: str,
    taken: set[str], *, width: int=DEFAULT_ADDRESS_WIDTH)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: supernode
  how: 'defines public function `supernode` at line 225, signature: (node_id: str,
    level: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: is_valid_address
  how: 'defines public function `is_valid_address` at line 236, signature: (value:
    str, *, width: int=DEFAULT_ADDRESS_WIDTH)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: plan_reid
  how: 'defines public function `plan_reid` at line 241, signature: (nodes: Iterable[Mapping[str,
    Any]], *, width: int=DEFAULT_ADDRESS_WIDTH, group_width: int=DEFAULT_GROUP_WIDTH,
    out_path: Optional[str | Path]=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_permanent_id
  how: defines public function `mint_permanent_id` at line 389
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: is_valid_mint_id
  how: 'defines public function `is_valid_mint_id` at line 427, signature: (value:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ensure_mint_id
  how: 'defines public function `ensure_mint_id` at line 437, signature: (fm: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out_path
  how: '`out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8")` at line 359'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(result, indent=2, sort_keys=True)` at line 359'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 1 `print()` call(s) at line(s) [451]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Council bundle 1 row D (director-general-3, goal:g7.16.1.1.4 via [goal, idea]): assign-if-missing is now ONE function here, ensure_mint_id (moved from snapshot-goals.py). node_writer create + adopt, snapshot-goals and backfill-mint-ids keep only their wrappers and call it. It never overwrites (goal:g2.5). Falsifier 1 over bin+src: 4 -> 1. The BUILD-CONTRACT was regenerated by level3.build_node (residue 13). CARRIED FORWARD from the v2 thought (dropped by 5a828b3ce, sanctuary-master mur wf_a56d005b-d6b residue 14; the full prior text is in the grid): a real design hazard: at a narrow width (e.g. width=1, 36 slots), minting more distinct seeds than there are slots makes mint_address loop forever once every slot is taken, because there is no exhaustion check. Re-measured 09-29: the rehash loop is still an unguarded while True. The production default (width=7, ~78 billion slots) is nowhere near this regime.
<!-- THOUGHT:END -->
