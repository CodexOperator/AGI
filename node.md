---
build_kind: code
confidence: 1.0
id: "build:bin-season"
mint_id: 2e990ee477294ab982ad6af5b9489187
origin: build-scan
parents:
  - mvp:bin-modules
payload_ref: extensions/agi/bin/season.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/season.py"
type: build
---

`extensions/agi/bin/season.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:bin-modules`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/season.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.Counter
  how: '`from collections import Counter` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dataclasses.dataclass
  how: '`from dataclasses import dataclass` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dataclasses.field
  how: '`from dataclasses import field` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 33'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.persistence.frontmatter
  how: '`from graph_core.persistence import frontmatter` at line 34'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fp
  how: '`fp.read_text(encoding="utf-8")` at line 769'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(record_path.read_text())` at line 1038'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: record_path
  how: '`record_path.read_text()` at line 1038'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: env:AGI_SEASON
  how: reads `os.environ`/`os.getenv` for literal key 'AGI_SEASON'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: Tier
  how: defines public class `Tier` at line 58
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: TierStats
  how: defines public class `TierStats` at line 70
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_ladder
  how: 'defines private function `_load_ladder` at line 89, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_tiers
  how: 'defines private function `_load_tiers` at line 99, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _get_current_season
  how: 'defines private function `_get_current_season` at line 116, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _get_caps
  how: 'defines private function `_get_caps` at line 122, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _plan_type_for_kind
  how: 'defines private function `_plan_type_for_kind` at line 128, signature: (kind:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _kind_from_goal_type
  how: 'defines private function `_kind_from_goal_type` at line 146, signature: (plan_type:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _collect_stats
  how: 'defines private function `_collect_stats` at line 163, signature: (root: Path,
    tiers: list[Tier], season: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _shell_out_write
  how: 'defines private function `_shell_out_write` at line 235, signature: (root:
    Path, node_id: str, set_fm: dict | None=None, note: str | None=None, actor: str=''season.py'',
    session: str=''season'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 273, signature: (root: Path,
    args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_judge
  how: 'defines public function `cmd_judge` at line 331, signature: (root: Path, args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_retag
  how: 'defines public function `cmd_retag` at line 604, signature: (root: Path, args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _season_nodes
  how: 'defines private function `_season_nodes` at line 720, signature: (root: Path,
    season: int, node_type: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _unjudged_overviews
  how: 'defines private function `_unjudged_overviews` at line 737, signature: (root:
    Path, season: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _load_vision_sources
  how: 'defines private function `_load_vision_sources` at line 754, signature: (arg:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _mint_vision
  how: 'defines private function `_mint_vision` at line 786, signature: (root: Path,
    source: dict, season_overviews: list[str], new_season: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_git_root
  how: 'defines private function `_find_git_root` at line 806, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_rollover
  how: 'defines public function `cmd_rollover` at line 817, signature: (root: Path,
    args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git
  how: 'defines private function `_git` at line 1019, signature: (root: Path, *args:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _current_branch
  how: 'defines private function `_current_branch` at line 1025, signature: (root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _recorded_field
  how: 'defines private function `_recorded_field` at line 1033, signature: (record_path:
    Path | None, key: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_merge_up
  how: 'defines public function `cmd_merge_up` at line 1045, signature: (root: Path,
    args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 1166, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(v, separators=('','', '':''))` at line 246'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 111 `print()` call(s) at line(s) [93, 264, 279, 280, 281, 286, 293, 294, 298,
    300, 305, 307, 310, 312, 314, 316, 319, 320, 321, 322, 380, 389, 429, 466, 467,
    481, 515, 520, 530, 574, 576, 577, 578, 580, 582, 583, 586, 652, 653, 654, 655,
    657, 659, 663, 702, 703, 705, 767, 852, 853, 855, 861, 863, 865, 867, 868, 874,
    878, 884, 886, 887, 888, 889, 890, 891, 892, 893, 895, 896, 903, 905, 907, 908,
    909, 910, 913, 915, 916, 917, 922, 945, 949, 952, 971, 972, 978, 984, 987, 989,
    990, 991, 992, 1049, 1059, 1073, 1078, 1081, 1087, 1090, 1097, 1103, 1110, 1113,
    1129, 1135, 1139, 1149, 1152, 1155, 1157, 1251]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
