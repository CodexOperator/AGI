---
id: build:tests-test-completion
mint_id: ea4f76ba9b95431ebd64380ec8b187c4
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_completion.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_completion.py"
---
`extensions/agi/tests/test_completion.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_completion.py
parse_ok: true
inputs:
- name: ast
  how: '`import ast` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(path.read_text().split("---", 2)[1])` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: res.path
  how: '`res.path.read_text()` at line 321'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_text()` at line 392'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 96'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "completion.py"
  how: '`(BIN / "completion.py").read_text(encoding="utf-8")` at line 218'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text()` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _load
  how: 'defines private function `_load` at line 32, signature: (name)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 65, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _scaffold
  how: 'defines private function `_scaffold` at line 82, signature: (project, slug=''exp1'',
    parent=''hypothesis:h1'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _fm
  how: 'defines private function `_fm` at line 89, signature: (path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _fill
  how: 'defines private function `_fill` at line 94, signature: (path, body)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _agent_done
  how: 'defines private function `_agent_done` at line 100, signature: (iter_dir,
    agent_id, node_id)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_writer_stamps_the_scaffold_identity
  how: 'defines public function `test_writer_stamps_the_scaffold_identity` at line
    116, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_untouched_scaffold_is_not_complete
  how: 'defines public function `test_untouched_scaffold_is_not_complete` at line
    128, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_killed_after_writing_is_complete
  how: 'defines public function `test_killed_after_writing_is_complete` at line 133,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_done_on_untouched_scaffold_is_not_complete
  how: 'defines public function `test_done_on_untouched_scaffold_is_not_complete`
    at line 140, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_completion_does_not_depend_on_which_report_path_existed
  how: 'defines public function `test_completion_does_not_depend_on_which_report_path_existed`
    at line 147, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_node_is_not_complete
  how: 'defines public function `test_missing_node_is_not_complete` at line 158, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_template_drift_keeps_untouched_scaffold_incomplete
  how: 'defines public function `test_template_drift_keeps_untouched_scaffold_incomplete`
    at line 166, signature: (project, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_legacy_node_without_stamp_uses_current_placeholder
  how: 'defines public function `test_legacy_node_without_stamp_uses_current_placeholder`
    at line 175, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _code_tokens
  how: 'defines private function `_code_tokens` at line 194, signature: (src)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_completion_code_names_no_harness_and_no_process_state
  how: defines public function `test_completion_code_names_no_harness_and_no_process_state`
    at line 217
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_gate_reads_the_node_before_the_record
  how: defines public function `test_post_wire_gate_reads_the_node_before_the_record`
    at line 223
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _wire_failed_agent
  how: 'defines private function `_wire_failed_agent` at line 245, signature: (project,
    agent_id, node_id, status=''failed'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_failed_kid_with_a_filled_node_is_wired_anyway
  how: 'defines public function `test_failed_kid_with_a_filled_node_is_wired_anyway`
    at line 265, signature: (project, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_failed_kid_with_an_untouched_scaffold_is_not_wired
  how: 'defines public function `test_failed_kid_with_an_untouched_scaffold_is_not_wired`
    at line 280, signature: (project, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_notes_land_once_even_when_both_writers_run
  how: 'defines public function `test_notes_land_once_even_when_both_writers_run`
    at line 301, signature: (project, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rewire_does_not_demote_an_earned_proved
  how: defines public function `test_rewire_does_not_demote_an_earned_proved` at line
    331
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pending_in_the_node_does_not_outrank_a_reported_verdict
  how: defines public function `test_pending_in_the_node_does_not_outrank_a_reported_verdict`
    at line 349
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_malformed_frontmatter_is_not_complete_and_does_not_raise
  how: 'defines public function `test_malformed_frontmatter_is_not_complete_and_does_not_raise`
    at line 359, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_malformed_node_is_never_rewritten
  how: 'defines public function `test_malformed_node_is_never_rewritten` at line 378,
    signature: (project, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_malformed_shapes_raise_one_catchable_class
  how: defines public function `test_both_malformed_shapes_raise_one_catchable_class`
    at line 395
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 67'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sd / "[shape].md"
  how: '`(sd / "[shape].md").write_text(SHAPE)` at line 70'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.write_text(f"---\n{parts[1]}---\n{body}")` at line 97'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "agent.json"
  how: '`(d / "agent.json").write_text(json.dumps( {"id": agent_id, "status": "done",
    "node_id": node_id, "verdict": "inconclusive_lean_proved:65"}))` at line 104'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_dir / "manifest.json"
  how: '`(iter_dir / "manifest.json").write_text(json.dumps( {"timeout_seconds": 600,
    "agents": [{"id": agent_id, "status": "done"}]}))` at line 107'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text( f"---\nid: {nid}\nmint_id: deadbeef\ntype: experiment\n" f"parents:\n  -
    hypothesis:h1\n---\n" f"# {nid}\n\n{nw.BODY_PROMPTS[''experiment'']}")` at line
    181'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_dir / agent_id / "agent.json"
  how: '`(iter_dir / agent_id / "agent.json").write_text(json.dumps( {"id": agent_id,
    "status": status, "node_id": node_id, "fail_reason": "pid disappeared without
    completion signal"}))` at line 254'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_dir / "manifest.json"
  how: '`(iter_dir / "manifest.json").write_text(json.dumps( {"timeout_seconds": 600,
    "agents": [{"id": agent_id, "status": status, "node_id": node_id, "parent": "hypothesis:h1"}]}))`
    at line 257'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text("---\nfoo: [unclosed\n---\n\nreal looking body\n")` at line
    369'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(original)` at line 389'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sd / fname
  how: '`(sd / fname).write_text(f"---\nname: {name}\nspawn:\n  {spawn}\n---\n{name}\n")`
    at line 73'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f"{slug}.md"
  how: '`(d / f"{slug}.md").write_text(f"---\nid: {ntype}:{slug}\ntype: {ntype}\n---\n\nbody\n")`
    at line 78'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"id": agent_id, "status": "done", "node_id": node_id, "verdict":
    "inconclusive_lean_proved:65"})` at line 104'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"timeout_seconds": 600, "agents": [{"id": agent_id, "status":
    "done"}]})` at line 107'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"id": agent_id, "status": status, "node_id": node_id, "fail_reason":
    "pid disappeared without completion signal"})` at line 254'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"timeout_seconds": 600, "agents": [{"id": agent_id, "status":
    status, "node_id": node_id, "parent": "hypothesis:h1"}]})` at line 257'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_dir / "a1" / "agent.json"
  how: '`(iter_dir / "a1" / "agent.json").write_text(json.dumps( {"id": "a1", "status":
    "done", "node_id": res.node_id, "notes": notes, "verdict": "pending"}))` at line
    311'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_dir / "manifest.json"
  how: '`(iter_dir / "manifest.json").write_text(json.dumps( {"timeout_seconds": 600,
    "agents": [ {"id": "a1", "status": "done", "node_id": res.node_id, "parent": "hypothesis:h1",
    "notes": notes}]}))` at line 314'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"id": "a1", "status": "done", "node_id": res.node_id, "notes":
    notes, "verdict": "pending"})` at line 311'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"timeout_seconds": 600, "agents": [ {"id": "a1", "status": "done",
    "node_id": res.node_id, "parent": "hypothesis:h1", "notes": notes}]})` at line
    314'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.