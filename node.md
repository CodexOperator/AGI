---
id: build:tests-test-chain-engine
mint_id: b7687dadb494470c8d4758b9e499f42a
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_chain_engine.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_chain_engine.py"
---
`extensions/agi/tests/test_chain_engine.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_chain_engine.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pickle
  how: '`import pickle` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.edge.Edge
  how: '`from graph_core.edge import Edge` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.graph.Graph
  how: '`from graph_core.graph import Graph` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.node.Node
  how: '`from graph_core.node import Node` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: chain_engine.chains.CHAIN_CACHE_VERSION
  how: '`from chain_engine.chains import CHAIN_CACHE_VERSION` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: chain_engine.chains.DEFAULT_MAX_CHAINS
  how: '`from chain_engine.chains import DEFAULT_MAX_CHAINS` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: chain_engine.chains.DEFAULT_MAX_PATH_LEN
  how: '`from chain_engine.chains import DEFAULT_MAX_PATH_LEN` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: chain_engine.chains.DEFAULT_DEADLINE_S
  how: '`from chain_engine.chains import DEFAULT_DEADLINE_S` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: chain_engine.chains._make_can_reach_terminal
  how: '`from chain_engine.chains import _make_can_reach_terminal` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: chain_engine.chains.find_chains
  how: '`from chain_engine.chains import find_chains` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: chain_engine.chains.find_chains_from_node
  how: '`from chain_engine.chains import find_chains_from_node` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache
  how: '`cache.read_bytes()` at line 316'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nodes / ".chain_cache.pkl"
  how: '`(nodes / ".chain_cache.pkl").read_bytes()` at line 375'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _link
  how: 'defines private function `_link` at line 38, signature: (g: Graph, src: str,
    tgt: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _deep_chain_graph
  how: 'defines private function `_deep_chain_graph` at line 42, signature: (hops:
    int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_deep_2000_hop_chain_completes_quickly_with_default_bounds
  how: 'defines public function `test_deep_2000_hop_chain_completes_quickly_with_default_bounds`
    at line 66, signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_deep_2000_hop_chain_found_when_path_cap_raised
  how: defines public function `test_deep_2000_hop_chain_found_when_path_cap_raised`
    at line 78
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_can_reach_terminal_is_iterative_on_deep_chain
  how: defines public function `test_can_reach_terminal_is_iterative_on_deep_chain`
    at line 89
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _build_from_frontmatter
  how: 'defines private function `_build_from_frontmatter` at line 111, signature:
    (tmp_path: Path, typed: dict[str, str], edges: dict[str, list[str]])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cycle_in_next_edges_terminates
  how: 'defines public function `test_cycle_in_next_edges_terminates` at line 142,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_self_loop_in_next_edges_terminates
  how: 'defines public function `test_self_loop_in_next_edges_terminates` at line
    163, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _fan_graph
  how: 'defines private function `_fan_graph` at line 176, signature: (width: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_max_chains_cap_returns_partial_output
  how: 'defines public function `test_max_chains_cap_returns_partial_output` at line
    200, signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_max_chains_not_hit_returns_everything
  how: 'defines public function `test_max_chains_not_hit_returns_everything` at line
    209, signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_max_path_len_cap_returns_partial_output
  how: 'defines public function `test_max_path_len_cap_returns_partial_output` at
    line 216, signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_max_path_len_does_not_starve_later_roots
  how: 'defines public function `test_max_path_len_does_not_starve_later_roots` at
    line 224, signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_deadline_cap_returns_partial_output
  how: 'defines public function `test_deadline_cap_returns_partial_output` at line
    241, signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_deadline_none_disables_clock_guard
  how: defines public function `test_deadline_none_disables_clock_guard` at line 251
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bound_defaults_are_the_documented_ones
  how: defines public function `test_bound_defaults_are_the_documented_ones` at line
    256
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_results_are_deterministic
  how: defines public function `test_results_are_deterministic` at line 266
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_find_chains_from_node_is_bounded
  how: 'defines public function `test_find_chains_from_node_is_bounded` at line 274,
    signature: (capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_find_chains_from_node_returns_deep_chain_when_uncapped
  how: defines public function `test_find_chains_from_node_returns_deep_chain_when_uncapped`
    at line 283
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_graph_dir_none_writes_no_cache
  how: 'defines public function `test_graph_dir_none_writes_no_cache` at line 300,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_graph_dir_positional_round_trips_cache
  how: 'defines public function `test_graph_dir_positional_round_trips_cache` at line
    306, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cache_path_is_per_directory
  how: 'defines public function `test_cache_path_is_per_directory` at line 321, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _deep_frontmatter_chain
  how: 'defines private function `_deep_frontmatter_chain` at line 335, signature:
    (tmp_path: Path, hops: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_truncated_result_rewarns_on_every_cache_hit
  how: 'defines public function `test_truncated_result_rewarns_on_every_cache_hit`
    at line 349, signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_complete_result_stays_silent_on_cache_hit
  how: 'defines public function `test_complete_result_stays_silent_on_cache_hit` at
    line 361, signature: (tmp_path, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_truncation_reason_is_persisted
  how: 'defines public function `test_truncation_reason_is_persisted` at line 371,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unversioned_cache_is_refused
  how: 'defines public function `test_unversioned_cache_is_refused` at line 380, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nodes / ".chain_cache.pkl"
  how: '`(nodes / ".chain_cache.pkl").write_bytes(pickle.dumps({ "chains": [["idea:stale"]],
    "node_count": len(md), "mtime": max(f.stat().st_mtime for f in md), "saved_at":
    time.time(), }))` at line 384'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f"{i}.md"
  how: '`(d / f"{i}.md").write_text( f''---\nid: "{nid}"\ntype: {ntype}\n{block}---\n\nbody\n''
    )` at line 128'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.