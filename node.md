---
id: build:src-agi-algos-graph-builder
mint_id: 9b1e22fad0aa4c888713201d491da489
type: build
parents:
  - idea:engine-agi-algos
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/src/agi_algos/graph_builder.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/src/agi_algos/graph_builder.py"
---
`extensions/agi/src/agi_algos/graph_builder.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-agi-algos`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/src/agi_algos/graph_builder.py
parse_ok: true
inputs:
- name: os
  how: '`import os` at line 7'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: functools.lru_cache
  how: '`from functools import lru_cache` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.List
  how: '`from typing import List` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Dict
  how: '`from typing import Dict` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Any
  how: '`from typing import Any` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Optional
  how: '`from typing import Optional` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Tuple
  how: '`from typing import Tuple` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.defaultdict
  how: '`from collections import defaultdict` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pickle
  how: '`import pickle` at line 2454'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 93 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cache_data)` at line 233'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_file
  how: '`open(cache_file, ''rb'')` at line 2496 (mode=''rb'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pickle.load
  how: '`pickle.load(f)` at line 2497'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_file
  how: '`open(graph_file)` at line 677 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.load
  how: '`json.load(f)` at line 678'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: gitnexus_cache_file
  how: '`open(gitnexus_cache_file)` at line 2659 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _GITNEXUS_CACHE_FILE
  how: '`open(_GITNEXUS_CACHE_FILE)` at line 34 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 146 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 187 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 274 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 345 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 414 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 460 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 503 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 556 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 633 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 745 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 962 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1031 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1111 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1182 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1258 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1671 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1810 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1916 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hook_md
  how: '`open(hook_md, ''r'')` at line 2038 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, ''r'')` at line 2149 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, ''r'')` at line 2255 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: skill_md
  how: '`open(skill_md, "r")` at line 830 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1308 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1339 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1388 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1419 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: filepath
  how: '`open(filepath, "r")` at line 1504 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: skill_md
  how: '`open(skill_md, "r")` at line 893 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: init_cache
  how: 'defines public function `init_cache` at line 25, signature: (cache_dir: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _save_cache
  how: 'defines private function `_save_cache` at line 39, signature: (data: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: GraphBuilder
  how: defines public class `GraphBuilder` at line 50
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run_subprocess
  how: 'defines public function `run_subprocess` at line 2440, signature: (cmd: str,
    timeout: int=30)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _get_graph_cache_file
  how: 'defines private function `_get_graph_cache_file` at line 2456, signature:
    (agi_dir: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _get_source_mtimes
  how: 'defines private function `_get_source_mtimes` at line 2462, signature: (hermes_dir:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _try_load_graph_cache
  how: 'defines private function `_try_load_graph_cache` at line 2485, signature:
    (agi_dir: str, source_mtimes: Dict[str, float], gitnexus_cache: Optional[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _save_graph_cache
  how: 'defines private function `_save_graph_cache` at line 2519, signature: (agi_dir:
    str, builder: GraphBuilder, gitnexus_cache: Optional[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _cached_build_builder
  how: 'defines private function `_cached_build_builder` at line 2539, signature:
    (hermes_dir: str, agi_dir: str, gitnexus_hash: int, _cache_ver: int=1)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_graph
  how: 'defines public function `build_graph` at line 2676, signature: (hermes_dir:
    str, agi_dir: str, use_gitnexus: bool=True, gitnexus_cache: Optional[str]=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_file
  how: '`open(cache_file, ''wb'')` at line 2533 (mode=''wb'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pickle.dump
  how: '`pickle.dump(cached, f, protocol=pickle.HIGHEST_PROTOCOL)` at line 2534'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _GITNEXUS_CACHE_FILE
  how: '`open(_GITNEXUS_CACHE_FILE, ''w'')` at line 45 (mode=''w'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 4 `print()` call(s) at line(s) [2842, 2843, 2844, 2845]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.