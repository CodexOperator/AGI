---
build_kind: code
confidence: 1.0
id: "build:tests-test-real-adapter-restart"
mint_id: 89cef23647a349daa4dd055fa76ef73a
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_real_adapter_restart.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_real_adapter_restart.py"
type: build
---

`extensions/agi/tests/test_real_adapter_restart.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_real_adapter_restart.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: signal
  how: '`import signal` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: uuid
  how: '`import uuid` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: adapters
  how: '`import adapters` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: spawn_budget
  how: '`import spawn_budget` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 769'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.read_text()` at line 844'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 772'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 846'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pwd_marker
  how: '`pwd_marker.read_text()` at line 137'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: f"/proc/{proc.pid}/stat"
  how: '`open(f"/proc/{proc.pid}/stat")` at line 247 (mode=''r'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _load_dispatch
  how: defines private function `_load_dispatch` at line 34
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mock_pi_bin
  how: 'defines public function `mock_pi_bin` at line 58, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project_root
  how: 'defines public function `project_root` at line 67, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: TestPiAdapterRestartWithRealProcess
  how: defines public class `TestPiAdapterRestartWithRealProcess` at line 86
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pi_bin
  how: '`pi_bin.write_text(MOCK_PI)` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "config.json"
  how: '`(graph / "config.json").write_text(json.dumps({ "agent_dispatch": {"provider":
    "openrouter", "model": "test-model"}, }))` at line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({ "agent_dispatch": {"provider": "openrouter", "model": "test-model"},
    })` at line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sess_dir / "context.md"
  how: '`(sess_dir / "context.md").write_text("ctx")` at line 107'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pwd_pi
  how: '`pwd_pi.write_text( f"#!/bin/bash\npwd > {pwd_marker}\nexit 0\n")` at line
    111'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ctx_file
  how: '`ctx_file.write_text("Test context")` at line 170'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sleep_pi
  how: '`sleep_pi.write_text("#!/bin/bash\nsleep 30\necho done\n")` at line 270'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sess_dir / "context.md"
  how: '`(sess_dir / "context.md").write_text("ctx")` at line 276'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ctx_file
  how: '`ctx_file.write_text("Test context for real-agent restart")` at line 313'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_file
  how: '`log_file.write_text("")` at line 315'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sleep_bin
  how: '`sleep_bin.write_text("#!/bin/bash\nsleep 30\necho done\n")` at line 323'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sess_dir / "agent.json"
  how: '`(sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))`
    at line 342'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ctx_file
  how: '`ctx_file.write_text("Test context")` at line 410'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sleep_bin
  how: '`sleep_bin.write_text("#!/bin/bash\nsleep 30\necho done\n")` at line 413'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text("""--- id: experiment:exp-complete-test type: experiment
    --- Already done. """)` at line 467'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sleep_bin
  how: '`sleep_bin.write_text("#!/bin/bash\nsleep 60\necho done\n")` at line 483'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sleep_bin
  how: '`sleep_bin.write_text("#!/bin/bash\nsleep 60\necho done\n")` at line 534'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(f"""--- id: {node_id} type: experiment parents: - hypothesis:test-root
    scaffold_hash: abcdef1234567890 --- # {node_id} ## Experiment ## Evidence """)`
    at line 589'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ctx_file
  how: '`ctx_file.write_text("Test context")` at line 611'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sleep_bin
  how: '`sleep_bin.write_text("#!/bin/bash\nsleep 30\necho done\n")` at line 623'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sess_dir / "agent.json"
  how: '`(sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))`
    at line 641'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_root / "nodes" / "hypothesis" / "test-root.md"
  how: '`(graph_root / "nodes" / "hypothesis" / "test-root.md").write_text( """---
    id: hypothesis:test-root type: hypothesis --- Root.""")` at line 715'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_root / "config.json"
  how: '`(graph_root / "config.json").write_text(json.dumps({}))` at line 723'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(f"""--- id: {node_id} type: experiment parents: - hypothesis:test-root
    --- # {node_id} ## Experiment Ran a test. """)` at line 727'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: agent_json
  how: '`agent_json.write_text(json.dumps({ "id": "a00-fixb-test", "status": "running",
    "pid": 12345, "started_at": 1234567890, }))` at line 742'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_root / "sessions" / "iter-L2.13" / "manifest.json"
  how: '`(graph_root / "sessions" / "iter-L2.13" / "manifest.json").write_text( json.dumps({"iter":
    "L2.13", "agents": [{"id": "a00-fixb-test"}]}))` at line 746'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / ".agi" / "config.json"
  how: '`(root / ".agi" / "config.json").write_text(json.dumps({}))` at line 792'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hyp_file
  how: '`hyp_file.write_text("""--- id: hypothesis:parent-test type: hypothesis ---
    Parent.""")` at line 795'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_file
  how: '`node_file.write_text(f"""--- id: {node_id} type: experiment parents: - hypothesis:parent-test
    --- # {node_id} ## Experiment Ran it.""")` at line 804'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(agent_record, indent=2)` at line 342'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(agent_record, indent=2)` at line 641'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({})` at line 723'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({ "id": "a00-fixb-test", "status": "running", "pid": 12345, "started_at":
    1234567890, })` at line 742'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"iter": "L2.13", "agents": [{"id": "a00-fixb-test"}]})` at line
    747'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({})` at line 792'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
