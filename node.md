---
build_kind: code
confidence: 1.0
id: "build:tests-test-workflow"
mint_id: 34a23649621a48258c5941c0d15bc2f5
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_workflow.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_workflow.py"
type: build
---

`extensions/agi/tests/test_workflow.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_workflow.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: io
  how: '`import io` at line 14'
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
- name: re
  how: '`import re` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: workflow
  how: '`import workflow` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: workflow._resolve_knobs
  how: '`from workflow import _resolve_knobs` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: workflow.validate_return
  how: '`from workflow import validate_return` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: workflow.render_stage_prompt
  how: '`from workflow import render_stage_prompt` at line 166'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: workflow._parse_last_json
  how: '`from workflow import _parse_last_json` at line 166'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: workflow._effort_to_thinking
  how: '`from workflow import _effort_to_thinking` at line 166'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: workflow._run_stage_pi
  how: '`from workflow import _run_stage_pi` at line 166'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: WF_DIR / "agi-round-review.js"
  how: '`(WF_DIR / "agi-round-review.js").read_text(encoding="utf-8")` at line 287'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: WF_DIR / "agi-brief-drafting.js"
  how: '`(WF_DIR / "agi-brief-drafting.js").read_text(encoding="utf-8")` at line 294'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(mf.read_text(encoding="utf-8"))` at line 386'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mf
  how: '`mf.read_text(encoding="utf-8")` at line 386'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: js
  how: '`js.read_text(encoding="utf-8")` at line 402'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: script
  how: '`script.read_text(encoding="utf-8")` at line 402'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: test_config_row_overrides_script_defaults
  how: defines public function `test_config_row_overrides_script_defaults` at line
    34
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_args_override_config_row_and_hint
  how: defines public function `test_args_override_config_row_and_hint` at line 42
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_row_falls_back_to_hint_then_raises_on_no_model
  how: defines public function `test_missing_row_falls_back_to_hint_then_raises_on_no_model`
    at line 49
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_config_flip_changes_dispatched_model
  how: defines public function `test_config_flip_changes_dispatched_model` at line
    63
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pi_model_refuses_claude_code_alias_before_spawn
  how: defines public function `test_pi_model_refuses_claude_code_alias_before_spawn`
    at line 94
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_named_workflow_symlinks_resolve_to_repo_files
  how: defines public function `test_named_workflow_symlinks_resolve_to_repo_files`
    at line 119
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_runner_pi_harness_dry_run_prints_one_dispatch_per_stage
  how: defines public function `test_runner_pi_harness_dry_run_prints_one_dispatch_per_stage`
    at line 130
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_stage_return_is_schema_validated
  how: defines public function `test_stage_return_is_schema_validated` at line 148
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_stage_prompt_uses_repeat_item_fields_over_args
  how: defines public function `test_render_stage_prompt_uses_repeat_item_fields_over_args`
    at line 172
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_stage_prompt_missing_field_and_json_braces_pass_through
  how: defines public function `test_render_stage_prompt_missing_field_and_json_braces_pass_through`
    at line 193
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_stage_prompt_requires_prompt_text
  how: defines public function `test_render_stage_prompt_requires_prompt_text` at
    line 203
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parse_last_json_tolerates_preamble_and_trailing_glue
  how: defines public function `test_parse_last_json_tolerates_preamble_and_trailing_glue`
    at line 213
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_effort_to_thinking_map
  how: defines public function `test_effort_to_thinking_map` at line 223
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_run_stage_pi_passes_resolved_model_and_rendered_prompt
  how: defines public function `test_run_stage_pi_passes_resolved_model_and_rendered_prompt`
    at line 231
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_run_stage_pi_rejects_schema_violating_return
  how: defines public function `test_run_stage_pi_rejects_schema_violating_return`
    at line 269
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_review_and_drafting_stage_json_matches_js_prompts
  how: defines public function `test_review_and_drafting_stage_json_matches_js_prompts`
    at line 286
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _write_registry_pair
  how: 'defines private function `_write_registry_pair` at line 309, signature: (wf:
    Path, key: str, script_text: str, stages: list)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_registry_flag_script_without_sibling_manifest
  how: 'defines public function `test_registry_flag_script_without_sibling_manifest`
    at line 316, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_registry_flag_manifest_naming_unimplemented_stage
  how: 'defines public function `test_registry_flag_manifest_naming_unimplemented_stage`
    at line 337, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_register_derives_stages_and_refuses_overwrite
  how: 'defines public function `test_register_derives_stages_and_refuses_overwrite`
    at line 361, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_list_workflows_enumerates_registry
  how: 'defines public function `test_list_workflows_enumerates_registry` at line
    405, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_run_view_summary_has_no_harness_token
  how: defines public function `test_run_view_summary_has_no_harness_token` at line
    427
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_summary_byte_identical_across_harnesses
  how: defines public function `test_summary_byte_identical_across_harnesses` at line
    442
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pi_live_run_renders_tree_through_view
  how: defines public function `test_pi_live_run_renders_tree_through_view` at line
    457
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_claude_code_path_feeds_the_same_view
  how: defines public function `test_claude_code_path_feeds_the_same_view` at line
    483
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wf / f"agi-{key}.js"
  how: '`(wf / f"agi-{key}.js").write_text(script_text, encoding="utf-8")` at line
    310'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wf / f"{key}.json"
  how: '`(wf / f"{key}.json").write_text( json.dumps({"name": key, "script": f"agi-{key}.js",
    "stages": stages}, indent=2) + "\n", encoding="utf-8")` at line 311'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wf / "agi-orphan.js"
  how: '`(wf / "agi-orphan.js").write_text( "phase(''Orphan'')\n" "await agent(''x'',
    {label: ''orphan''})\n", encoding="utf-8")` at line 320'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wf / "ghost.json"
  how: '`(wf / "ghost.json").write_text( json.dumps({"name": "ghost", "script": "agi-ghost.js",
    "stages": []}), encoding="utf-8")` at line 328'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: script
  how: '`script.write_text( "phase(''Draft'')\n" "const drafts = await parallel(briefs.map(b
    => agent(`write {b.slug}`, " "{label: `draft:${b.slug}`, schema: DRAFT_SCHEMA})))\n"
    "phase(''Critic'')\n" "const critic = await agent(prompt, {label: ''critic'',...[truncated,
    317 chars total]` at line 366'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"name": "ghost", "script": "agi-ghost.js", "stages": []})` at
    line 329'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"name": key, "script": f"agi-{key}.js", "stages": stages}, indent=2)`
    at line 312'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
