---
id: build:bin-stitch
mint_id: ad6809b5d43b4983827231158b779f69
type: build
parents:
  - idea:engine-stitch
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/bin/stitch.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/stitch.py"
---
`extensions/agi/bin/stitch.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-stitch`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/stitch.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 142'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 144'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 145'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 146'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shutil
  how: '`import shutil` at line 147'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 148'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 149'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 150'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.Counter
  how: '`from collections import Counter` at line 151'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 152'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 154'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 239'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: md_path
  how: '`md_path.read_text(encoding="utf-8")` at line 277'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: StitchSafetyError
  how: defines public class `StitchSafetyError` at line 164
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Level3Node
  how: defines public class `Level3Node` at line 213
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_frontmatter
  how: 'defines private function `_parse_frontmatter` at line 231, signature: (text:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_level3_nodes
  how: 'defines public function `load_level3_nodes` at line 250, signature: (project_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _entry_pairs
  how: 'defines private function `_entry_pairs` at line 318, signature: (entries)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: diff_contract
  how: 'defines public function `diff_contract` at line 324, signature: (stored: dict,
    fresh: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _group_by_payload_ref
  how: 'defines private function `_group_by_payload_ref` at line 351, signature: (nodes:
    list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_well_formed_chain
  how: 'defines private function `_is_well_formed_chain` at line 363, signature: (group:
    list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _chain_order
  how: 'defines private function `_chain_order` at line 396, signature: (group: list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: verify_tree
  how: 'defines public function `verify_tree` at line 401, signature: (project_root:
    Path, engine_root: Path, from_grid: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: has_drift
  how: 'defines public function `has_drift` at line 545, signature: (report: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_within
  how: 'defines private function `_is_within` at line 554, signature: (path: Path,
    root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_is_clean
  how: 'defines private function `_git_is_clean` at line 562, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _guard_out_dir
  how: 'defines private function `_guard_out_dir` at line 573, signature: (out_dir:
    Path, project_root: Path, engine_root: Path, publish: bool=False, from_grid: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _grid_payload
  how: 'defines private function `_grid_payload` at line 627, signature: (project_root:
    Path, node: Level3Node, grid_version: int | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: materialize
  how: 'defines public function `materialize` at line 661, signature: (project_root:
    Path, engine_root: Path, out_dir: Path, force: bool=False, version: int | None=None,
    from_grid: bool=False, publish: bool=False, grid_version: int | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: print_verify_report
  how: 'defines public function `print_verify_report` at line 806, signature: (report:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: print_materialize_report
  how: 'defines public function `print_materialize_report` at line 851, signature:
    (stats: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 885, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 36 `print()` call(s) at line(s) [807, 808, 810, 812, 814, 816, 818, 820, 822,
    824, 826, 827, 830, 833, 836, 840, 842, 843, 846, 848, 852, 853, 855, 858, 860,
    864, 866, 868, 871, 873, 876, 878, 879, 930, 941, 949]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Makes `missing_payload` ask the grid before calling a payload missing, when
`--from-grid` is set. It already asked the grid for contract staleness thirty
lines below; existence was still answered off the engine tree alone.

**What that cost.** No new engine file could ever be published. `level3.py`
mints a node for a file authored under `payloads/`, `grid.py commit` puts its
bytes in the node's ref, and then this gate refused the publish because the
file was not in the engine tree — which publishing is the only thing that
would fix. Nothing reaches around it: `--publish` is deliberately never a side
effect of `--force`, and `publish-engine.sh` takes no override. So the
sanctioned "write a new file under `payloads/`" workflow could record a file
forever and ship it never. Found by hitting it: `test_publish_alarm.py` was
authored for G7.10 and deadlocked the publish it was written to protect.

**Why this is a one-line-shaped fix and not a redesign.** The correct rule was
already written down here, in the comment above `stale_contracts`: *"with the
engine as the source, a payload edited only in the graph reads as stale until
it is published, which is backwards."* That sentence is about staleness only
because staleness is where it was noticed. It is a statement about direction —
G6.1's arrow — and it applies to existence unchanged. A file the graph holds
and the engine has not received is **unpublished**, not missing, and the two
words point at opposite remedies: unpublished asks you to publish, missing
asks you to go find lost bytes.

**What was deliberately not weakened.** Without `--from-grid` the gate still
reads the tree and still reports the file, which is the whole engine-tree
claim intact — asked about the tree, it answers about the tree. And "missing"
keeps its teeth in grid mode: it now means *neither* source has the bytes, so
a node minted but never grid-committed is still drift. Both directions have a
test, because a gate that stops refusing is only correct if it still refuses
for the right reason.

**Previous thought on this node:** the `build:bin-stitch@v2` reasoning migrated
here under G2.10 (version chains are not duplicate `payload_ref`s). It is one
grid version back — `grid.py diff build:bin-stitch --back 1`. Thought is delta,
rewritten per version rather than accumulated, so the ref is where the chain of
reasoning lives; that is the property that made retiring `@v2` safe.
<!-- THOUGHT:END -->