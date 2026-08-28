---
build_kind: code
confidence: 1.0
id: "build:bin-cli"
mint_id: 42b7b4a44a7c4f56825daffc9fa0ced2
origin: build-scan
parents:
  - idea:engine-cli
payload_ref: extensions/agi/bin/cli.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/cli.py"
type: build
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
- name: node_writer
  how: '`import node_writer` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.VERDICT_HELP
  how: '`from evidence_gate import VERDICT_HELP` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate.VERDICT_RE
  how: '`from evidence_gate import VERDICT_RE` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 129'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 207'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 393'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest.read_text())` at line 444'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 129'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 207'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 253'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest
  how: '`manifest.read_text()` at line 444'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(text.split("---", 2)[1])` at line 78'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 253'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 291'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 343'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 448'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 349'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 448'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(fm_text)` at line 301'
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
  how: defines private function `_find_root` at line 47
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
- name: cmd_done
  how: 'defines public function `cmd_done` at line 84, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_pending
  how: 'defines public function `cmd_pending` at line 201, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_scaffold
  how: 'defines public function `cmd_scaffold` at line 216, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_node_file
  how: 'defines private function `_find_node_file` at line 261, signature: (root:
    Path, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _claim_node
  how: 'defines private function `_claim_node` at line 274, signature: (root: Path,
    node_id: str, session_id: str, force: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _detect_stale
  how: 'defines private function `_detect_stale` at line 335, signature: (root: Path,
    threshold_seconds: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_claim
  how: 'defines public function `cmd_claim` at line 365, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_detect_stale
  how: 'defines public function `cmd_detect_stale` at line 372, signature: (args:
    argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_reclaim
  how: 'defines public function `cmd_reclaim` at line 383, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _append_verdict_to_node
  how: 'defines private function `_append_verdict_to_node` at line 390, signature:
    (node_file: Path, verdict: str, confidence: float, notes: str, next_edge: str
    | None=None, gate=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 437, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 453
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 148'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 211'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(new_fm + "\n" + body)` at line 430'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 148'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 211'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 256'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lock_file
  how: '`open(lock_file, "a")` at line 288 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 256'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp
  how: '`tmp.write_text(new_content)` at line 328'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`open(node_file, "a")` at line 433 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 20 `print()` call(s) at line(s) [54, 86, 92, 119, 156, 188, 195, 197, 205,
    212, 239, 246, 248, 368, 376, 379, 386, 442, 445, 449]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
