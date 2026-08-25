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
- name: spawn_gate
  how: '`import spawn_gate` at line 22'
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
- name: graph_core.identity.mint_permanent_id
  how: '`from graph_core.identity import mint_permanent_id` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 136'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 225'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 486'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest.read_text())` at line 537'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 136'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 225'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 326'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest
  how: '`manifest.read_text()` at line 537'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(text.split(''---'', 2)[1])` at line 94'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 326'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 384'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 436'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 541'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 356'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 442'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 541'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(fm_text)` at line 394'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(fm_text)` at line 359'
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
  how: defines private function `_find_root` at line 63
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _agent_path
  how: 'defines private function `_agent_path` at line 74, signature: (root: Path,
    iter_n: int, agent_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_evidence_runs_raw
  how: 'defines private function `_node_evidence_runs_raw` at line 78, signature:
    (root: Path, node_id: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_done
  how: 'defines public function `cmd_done` at line 100, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_pending
  how: 'defines public function `cmd_pending` at line 219, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_scaffold
  how: 'defines public function `cmd_scaffold` at line 234, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_node_file
  how: 'defines private function `_find_node_file` at line 334, signature: (root:
    Path, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _claim_node
  how: 'defines private function `_claim_node` at line 367, signature: (root: Path,
    node_id: str, session_id: str, force: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _detect_stale
  how: 'defines private function `_detect_stale` at line 428, signature: (root: Path,
    threshold_seconds: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_claim
  how: 'defines public function `cmd_claim` at line 458, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_detect_stale
  how: 'defines public function `cmd_detect_stale` at line 465, signature: (args:
    argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_reclaim
  how: 'defines public function `cmd_reclaim` at line 476, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _append_verdict_to_node
  how: 'defines private function `_append_verdict_to_node` at line 483, signature:
    (node_file: Path, verdict: str, confidence: float, notes: str, next_edge: str
    | None=None, gate=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 530, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 546
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 150'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 229'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(''\n''.join(fm_lines) + body)` at line 320'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(new_fm + ''\n'' + body)` at line 523'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 150'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 229'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 329'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lock_file
  how: '`open(lock_file, ''a'')` at line 381 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: vfile
  how: '`vfile.write_text(''\n''.join(fm_lines) + f''\n\n{body}\n'')` at line 212'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 329'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp
  how: '`tmp.write_text(new_content)` at line 421'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`open(node_file, ''a'')` at line 526 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 20 `print()` call(s) at line(s) [70, 102, 108, 126, 158, 177, 213, 215, 223,
    230, 269, 281, 321, 461, 469, 472, 479, 535, 538, 542]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
