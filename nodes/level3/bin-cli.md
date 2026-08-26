---
confidence: 1.0
id: "level3:bin-cli"
mint_id: 42b7b4a44a7c4f56825daffc9fa0ced2
origin: level3-scan
parents:
  - idea:engine-cli
payload_ref: extensions/agi/bin/cli.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/bin/cli.py"
type: level3
---

`extensions/agi/bin/cli.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-cli`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
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
  how: '`json.loads(ap.read_text())` at line 120'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 193'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 399'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest.read_text())` at line 450'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 120'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 193'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 239'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest
  how: '`manifest.read_text()` at line 450'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(text.split(''---'', 2)[1])` at line 78'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 239'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 297'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 349'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 454'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 269'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 355'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 454'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(fm_text)` at line 307'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(fm_text)` at line 272'
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
  how: 'defines public function `cmd_pending` at line 187, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_scaffold
  how: 'defines public function `cmd_scaffold` at line 202, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_node_file
  how: 'defines private function `_find_node_file` at line 247, signature: (root:
    Path, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _claim_node
  how: 'defines private function `_claim_node` at line 280, signature: (root: Path,
    node_id: str, session_id: str, force: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _detect_stale
  how: 'defines private function `_detect_stale` at line 341, signature: (root: Path,
    threshold_seconds: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_claim
  how: 'defines public function `cmd_claim` at line 371, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_detect_stale
  how: 'defines public function `cmd_detect_stale` at line 378, signature: (args:
    argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_reclaim
  how: 'defines public function `cmd_reclaim` at line 389, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _append_verdict_to_node
  how: 'defines private function `_append_verdict_to_node` at line 396, signature:
    (node_file: Path, verdict: str, confidence: float, notes: str, next_edge: str
    | None=None, gate=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 443, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 459
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 134'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 197'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(new_fm + ''\n'' + body)` at line 436'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 134'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 197'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 242'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lock_file
  how: '`open(lock_file, ''a'')` at line 294 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 242'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp
  how: '`tmp.write_text(new_content)` at line 334'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`open(node_file, ''a'')` at line 439 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 20 `print()` call(s) at line(s) [54, 86, 92, 110, 142, 174, 181, 183, 191,
    198, 225, 232, 234, 374, 382, 385, 392, 448, 451, 455]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
