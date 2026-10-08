---
build_kind: code
confidence: 1.0
id: "build:bin-legacy"
mint_id: b6d217128e4145b8b3c9f278b5ab19be
origin: build-scan
payload_ref: extensions/agi/bin/legacy.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/legacy.py"
type: build
---

`extensions/agi/bin/legacy.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
goal:g7.16.1.11.22 (E1 D3, doc:rse-d3-legacy v2; chain 94a2ccbcda..42634e22af, builder director-general-5, rows director-general-2): legacy.py computes a node's legacy mark FROM THE BYTES of its own file's first-parent git history (renames followed): mark() = legacy | - | ?, label() adds the nest.py `⊃k` count, labels() is the viewport's batch with a per-user 4-column cache `${XDG_CACHE_HOME:-~/.cache}/agi/legacy.v1.tsv` (path, season, last-commit, mark; the rule version is in the FILE NAME, an old-name file is never read). No front-matter field carries the mark and no ref is read. A library (no CLI): viewport.py stamps it (`_with_legacy`, memo per window, key without HEAD). Limits named in the landing note: inject.py unstamped, the width-120 cut can hide the mark on long titles, cold viewport --verify ~40 s, a commit made while an interactive viewport is open shows only after a scroll to a window with different node ids, every interactive redraw spawns five `git rev-parse --git-dir --git-common-dir` from the loop's own code.
<!-- THOUGHT:END -->

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/legacy.py
parse_ok: true
inputs:
- name: os
  how: '`import os` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tempfile
  how: '`import tempfile` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nest.fm
  how: '`from nest import fm` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nest.graph
  how: '`from nest import graph` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nest.members
  how: '`from nest import members` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nest.Malformed
  how: '`from nest import Malformed` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_path()
  how: '`open(cache_path(), encoding="utf-8")` at line 59 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: git
  how: 'defines public function `git` at line 15, signature: (*a, inp=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: versions
  how: 'defines public function `versions` at line 16, signature: (rev, path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: bodies
  how: 'defines public function `bodies` at line 24, signature: (vs)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mark
  how: 'defines public function `mark` at line 31, signature: (rev, season, path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: render
  how: 'defines public function `render` at line 43, signature: (m, k)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: contains
  how: 'defines public function `contains` at line 47, signature: (nodes, nid)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: label
  how: 'defines public function `label` at line 50, signature: (rev, season, path,
    nodes=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_path
  how: defines public function `cache_path` at line 56
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_read
  how: defines public function `cache_read` at line 57
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cache_write
  how: 'defines public function `cache_write` at line 62, signature: (c)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: newest
  how: 'defines public function `newest` at line 69, signature: (rev, paths)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: labels
  how: 'defines public function `labels` at line 81, signature: (rev, season, paths,
    nodes)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: season_of
  how: 'defines public function `season_of` at line 92, signature: (rev)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
