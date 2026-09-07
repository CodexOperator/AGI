---
id: build:bin-cli
mint_id: 42b7b4a44a7c4f56825daffc9fa0ced2
type: build
parents:
  - idea:engine-cli
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/bin/cli.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/cli.py"
---
`extensions/agi/bin/cli.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-cli`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/cli.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate
  how: '`import evidence_gate` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_writer
  how: '`import node_writer` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.VERDICT_HELP
  how: '`from evidence_gate import VERDICT_HELP` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.VERDICT_RE
  how: '`from evidence_gate import VERDICT_RE` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 172'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 252'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 438'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest.read_text())` at line 498'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 172'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 252'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 298'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest
  how: '`manifest.read_text()` at line 498'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(text.split("---", 2)[1])` at line 78'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 298'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 336'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 388'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 502'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 394'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 502'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(fm_text)` at line 346'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _find_root
  how: defines private function `_find_root` at line 44
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _agent_path
  how: 'defines private function `_agent_path` at line 58, signature: (root: Path,
    iter_n: int, agent_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_evidence_runs_raw
  how: 'defines private function `_node_evidence_runs_raw` at line 62, signature:
    (root: Path, node_id: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _normalize_confidence
  how: 'defines private function `_normalize_confidence` at line 84, signature: (value:
    float)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_done
  how: 'defines public function `cmd_done` at line 117, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_pending
  how: 'defines public function `cmd_pending` at line 246, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_scaffold
  how: 'defines public function `cmd_scaffold` at line 261, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_node_file
  how: 'defines private function `_find_node_file` at line 306, signature: (root:
    Path, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _claim_node
  how: 'defines private function `_claim_node` at line 319, signature: (root: Path,
    node_id: str, session_id: str, force: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _detect_stale
  how: 'defines private function `_detect_stale` at line 380, signature: (root: Path,
    threshold_seconds: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_claim
  how: 'defines public function `cmd_claim` at line 410, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_detect_stale
  how: 'defines public function `cmd_detect_stale` at line 417, signature: (args:
    argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_reclaim
  how: 'defines public function `cmd_reclaim` at line 428, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _append_verdict_to_node
  how: 'defines private function `_append_verdict_to_node` at line 435, signature:
    (node_file: Path, verdict: str, confidence: float, notes: str, next_edge: str
    | None=None, gate=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 491, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 507
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 193'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 256'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(new_fm + "\n" + body)` at line 475'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 193'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 256'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 301'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lock_file
  how: '`open(lock_file, "a")` at line 333 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 301'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp
  how: '`tmp.write_text(new_content)` at line 373'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`open(node_file, "a")` at line 487 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 22 `print()` call(s) at line(s) [53, 108, 119, 125, 130, 162, 201, 233, 240,
    242, 250, 257, 284, 291, 293, 413, 421, 424, 431, 496, 499, 503]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
`_append_verdict_to_node` wrote the agent's notes into the body bare, with no
heading, while `post_wire` separately appended the same text under
`## Agent Notes`. Both run on every kid, so every node carried the notes twice —
once loose, once headed — and re-running `done` after an evidence-gate demotion
made three.

The kid contract blamed kids for this by name and by count for long enough that
someone counted to four. No kid was writing it. Two engine writers were, neither
aware of the other.

Both now emit the same section and neither writes when the body already carries
the text, so `done` is idempotent and re-wiring accumulates nothing.
<!-- THOUGHT:END -->