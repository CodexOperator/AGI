---
id: build:src-chain-engine-chains
mint_id: d99efcd33c214bf7ba78ee0c4e0a5897
type: build
parents:
  - idea:engine-chain-engine
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/src/chain_engine/chains.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/src/chain_engine/chains.py"
---
`extensions/agi/src/chain_engine/chains.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-chain-engine`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/src/chain_engine/chains.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 2'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.deque
  how: '`from collections import deque` at line 4'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 5'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pickle
  how: '`import pickle` at line 6'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 7'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Iterator
  how: '`from typing import Iterator` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.graph.Graph
  how: '`from graph_core.graph import Graph` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.types.RenderableGraph
  how: '`from graph_core.types import RenderableGraph` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .types.Chain
  how: '`from .types import Chain` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .types.is_valid_transition
  how: '`from .types import is_valid_transition` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 85'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_file
  how: '`open(cache_file, "rb")` at line 69 (mode=''rb'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pickle.load
  how: '`pickle.load(f)` at line 70'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: md_path
  how: '`md_path.read_text(encoding="utf-8", errors="replace")` at line 106'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _get_chain_cache_file
  how: 'defines private function `_get_chain_cache_file` at line 20, signature: (graph_dir:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _save_chain_cache
  how: 'defines private function `_save_chain_cache` at line 36, signature: (graph_dir:
    str, chains: list[Chain], node_count: int, mtime: float, truncated_reason: str
    | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_chain_cache
  how: 'defines private function `_load_chain_cache` at line 60, signature: (graph_dir:
    str, node_count: int, mtime: float)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_next_edges_from_disk
  how: 'defines private function `_load_next_edges_from_disk` at line 88, signature:
    (graph_dir: str, next_edges: dict[str, list[str]])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _warn_truncated
  how: 'defines private function `_warn_truncated` at line 175, signature: (reason:
    str, chains_found: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _make_can_reach_terminal
  how: 'defines private function `_make_can_reach_terminal` at line 183, signature:
    (graph: RenderableGraph, next_edges: dict[str, list[str]], memo: dict[str, bool])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_chains
  how: 'defines public function `find_chains` at line 235, signature: (graph: RenderableGraph,
    graph_dir: str | None=None, *, max_chains: int=DEFAULT_MAX_CHAINS, max_path_len:
    int=DEFAULT_MAX_PATH_LEN, deadline_s: float | None=DEFAULT_DEADLINE_S)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _traverse_iterative
  how: 'defines private function `_traverse_iterative` at line 433, signature: (start_id:
    str, graph: RenderableGraph, next_edges: dict[str, list[str]], spawns_edges: dict[str,
    list[str]], path: Chain, chains: list[Chain], verdict_can_reach_app: dict[str,
    bool], can_reach_terminal: callable, *, max_chains: int=DEFAULT_...[truncated,
    319 chars total])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _get_successors
  how: 'defines private function `_get_successors` at line 538, signature: (node_id:
    str, node, next_edges: dict[str, list[str]], spawns_edges: dict[str, list[str]],
    verdict_can_reach_app: dict[str, bool], can_reach_terminal: callable)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: find_chains_from_node
  how: 'defines public function `find_chains_from_node` at line 580, signature: (graph:
    RenderableGraph, start_id: str, *, max_chains: int=DEFAULT_MAX_CHAINS, max_path_len:
    int=DEFAULT_MAX_PATH_LEN, deadline_s: float | None=DEFAULT_DEADLINE_S)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_file
  how: '`open(cache_file, "wb")` at line 54 (mode=''wb'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pickle.dump
  how: '`pickle.dump(cached, f, protocol=pickle.HIGHEST_PROTOCOL)` at line 55'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 1 `print()` call(s) at line(s) [176]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.