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
  how: '`json.loads(ap.read_text())` at line 167'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 245'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 431'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest.read_text())` at line 491'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 167'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 245'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 291'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest
  how: '`manifest.read_text()` at line 491'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(text.split("---", 2)[1])` at line 78'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 291'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 329'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 381'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap.read_text())` at line 495'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 387'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.read_text()` at line 495'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(fm_text)` at line 339'
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
  how: 'defines public function `cmd_pending` at line 239, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_scaffold
  how: 'defines public function `cmd_scaffold` at line 254, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _find_node_file
  how: 'defines private function `_find_node_file` at line 299, signature: (root:
    Path, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _claim_node
  how: 'defines private function `_claim_node` at line 312, signature: (root: Path,
    node_id: str, session_id: str, force: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _detect_stale
  how: 'defines private function `_detect_stale` at line 373, signature: (root: Path,
    threshold_seconds: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_claim
  how: 'defines public function `cmd_claim` at line 403, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_detect_stale
  how: 'defines public function `cmd_detect_stale` at line 410, signature: (args:
    argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_reclaim
  how: 'defines public function `cmd_reclaim` at line 421, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _append_verdict_to_node
  how: 'defines private function `_append_verdict_to_node` at line 428, signature:
    (node_file: Path, verdict: str, confidence: float, notes: str, next_edge: str
    | None=None, gate=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 484, signature: (args: argparse.Namespace)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 500
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 186'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 249'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(new_fm + "\n" + body)` at line 468'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 186'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 249'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap
  how: '`ap.write_text(json.dumps(rec, indent=2))` at line 294'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lock_file
  how: '`open(lock_file, "a")` at line 326 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 294'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp
  how: '`tmp.write_text(new_content)` at line 366'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`open(node_file, "a")` at line 480 (mode=''a'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 22 `print()` call(s) at line(s) [53, 108, 119, 125, 130, 157, 194, 226, 233,
    235, 243, 250, 277, 284, 286, 406, 414, 417, 424, 489, 492, 496]
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
