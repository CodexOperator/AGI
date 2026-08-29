---
build_kind: code
confidence: 1.0
id: "build:tests-test-evidence-gate"
mint_id: 407c136809684d1cbfecf88fc7654c1d
origin: build-scan
payload_ref: extensions/agi/tests/test_evidence_gate.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_evidence_gate.py"
type: build
---

`extensions/agi/tests/test_evidence_gate.py` — level-3 code node (one file, one canonical node).

Census parent: none — **flagged**. No `idea:engine-*` census unit's `unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) covers this file. Left parentless rather than guessed.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_evidence_gate.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads( (project / "sessions" / "iter-001" / "a1" / "agent.json").read_text()
    )` at line 342'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 372'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "experiment" / "e1.md"
  how: '`(root / "nodes" / "experiment" / "e1.md").read_text()` at line 514'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "experiment" / "e1.md"
  how: '`(root / "nodes" / "experiment" / "e1.md").read_text()` at line 524'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "experiment" / "e1.md"
  how: '`(root / "nodes" / "experiment" / "e1.md").read_text()` at line 534'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "verdict" / "a1.md"
  how: '`(root / "nodes" / "verdict" / "a1.md").read_text()` at line 564'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "experiment" / "e1.md"
  how: '`(root / "nodes" / "experiment" / "e1.md").read_text()` at line 575'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "experiment" / "e1.md"
  how: '`(root / "nodes" / "experiment" / "e1.md").read_text()` at line 578'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "experiment" / "e1.md"
  how: '`(root / "nodes" / "experiment" / "e1.md").read_text()` at line 588'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "sessions" / "iter-001" / "a1" / "agent.json"
  how: '`(project / "sessions" / "iter-001" / "a1" / "agent.json").read_text()` at
    line 343'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node
  how: '`node.read_text()` at line 356'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node
  how: '`node.read_text()` at line 357'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 387'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 443'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 459'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 473'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / "verdict" / "experiment_e1.md"
  how: '`( project / "nodes" / "verdict" / "experiment_e1.md").read_text()` at line
    483'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.read_text()` at line 552'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _load
  how: 'defines private function `_load` at line 19, signature: (name, filename=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_taxonomy_is_valid
  how: 'defines public function `test_taxonomy_is_valid` at line 46, signature: (verdict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_uses_the_shared_taxonomy
  how: defines public function `test_cli_uses_the_shared_taxonomy` at line 50
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_invalid_verdicts_rejected
  how: 'defines public function `test_invalid_verdicts_rejected` at line 56, signature:
    (bad)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_decisive_without_evidence_is_demoted
  how: 'defines public function `test_decisive_without_evidence_is_demoted` at line
    61, signature: (verdict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_decisive_with_evidence_passes
  how: 'defines public function `test_decisive_with_evidence_passes` at line 71, signature:
    (verdict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_uncertain_verdicts_permitted_without_evidence
  how: 'defines public function `test_uncertain_verdicts_permitted_without_evidence`
    at line 82, signature: (verdict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bypass_is_loud_and_preserves_verdict
  how: defines public function `test_bypass_is_loud_and_preserves_verdict` at line
    89
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bypass_is_a_noop_when_evidence_exists
  how: defines public function `test_bypass_is_a_noop_when_evidence_exists` at line
    97
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_normalize_evidence_runs_scalars_never_count
  how: 'defines public function `test_normalize_evidence_runs_scalars_never_count`
    at line 106, signature: (value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unverifiable_attestation_is_reported_not_destroyed
  how: 'defines public function `test_unverifiable_attestation_is_reported_not_destroyed`
    at line 124, signature: (value, unverifiable)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_normalize_evidence_runs_lists_need_a_corpus
  how: 'defines public function `test_normalize_evidence_runs_lists_need_a_corpus`
    at line 135, signature: (value)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_normalize_evidence_runs_sentinel_string_counts_zero_not_one
  how: defines public function `test_normalize_evidence_runs_sentinel_string_counts_zero_not_one`
    at line 143
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_normalize_evidence_runs_resolves_a_real_id
  how: defines public function `test_normalize_evidence_runs_resolves_a_real_id` at
    line 149
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_normalize_evidence_runs_unresolvable_id_shaped_entry_counts_zero
  how: defines public function `test_normalize_evidence_runs_unresolvable_id_shaped_entry_counts_zero`
    at line 154
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_normalize_evidence_runs_mixed_list_counts_only_resolvable
  how: defines public function `test_normalize_evidence_runs_mixed_list_counts_only_resolvable`
    at line 161
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_evidence_runs_violations
  how: 'defines public function `test_evidence_runs_violations` at line 184, signature:
    (value, violations)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_is_node_id_shaped
  how: defines public function `test_is_node_id_shaped` at line 188
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_build_corpus_reads_declared_ids
  how: 'defines public function `test_build_corpus_reads_declared_ids` at line 196,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_build_corpus_missing_dir_is_empty_not_a_crash
  how: 'defines public function `test_build_corpus_missing_dir_is_empty_not_a_crash`
    at line 205, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sentinel_evidence_rejects_a_decisive_verdict_not_demotes
  how: defines public function `test_sentinel_evidence_rejects_a_decisive_verdict_not_demotes`
    at line 212
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_empty_evidence_still_demotes_not_rejects
  how: defines public function `test_empty_evidence_still_demotes_not_rejects` at
    line 224
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_resolvable_evidence_passes
  how: defines public function `test_resolvable_evidence_passes` at line 232
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bypass_overrides_rejection
  how: defines public function `test_bypass_overrides_rejection` at line 239
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sentinel_evidence_does_not_reject_uncertain_verdicts
  how: 'defines public function `test_sentinel_evidence_does_not_reject_uncertain_verdicts`
    at line 249, signature: (verdict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_stamp_records_demotion
  how: defines public function `test_stamp_records_demotion` at line 260
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_stamp_demotes_status_shadow_in_lockstep
  how: 'defines public function `test_stamp_demotes_status_shadow_in_lockstep` at
    line 272, signature: (decisive)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_stamp_never_touches_a_lifecycle_status
  how: 'defines public function `test_stamp_never_touches_a_lifecycle_status` at line
    286, signature: (lifecycle)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_stamp_leaves_status_alone_when_nothing_was_demoted
  how: defines public function `test_stamp_leaves_status_alone_when_nothing_was_demoted`
    at line 294
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_stamp_leaves_tags_alone
  how: defines public function `test_stamp_leaves_tags_alone` at line 303
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_shadow_verdict_fields_matches_what_stamp_rewrites
  how: defines public function `test_shadow_verdict_fields_matches_what_stamp_rewrites`
    at line 310
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 324, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _via_subprocess
  how: 'defines private function `_via_subprocess` at line 334, signature: (project,
    argv)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _agent_rec
  how: 'defines private function `_agent_rec` at line 341, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_demotes_unevidenced_proved
  how: 'defines public function `test_cli_done_demotes_unevidenced_proved` at line
    347, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_demotes_status_shadow_on_an_existing_node
  how: 'defines public function `test_cli_done_demotes_status_shadow_on_an_existing_node`
    at line 360, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_keeps_a_lifecycle_status_on_an_existing_node
  how: 'defines public function `test_cli_done_keeps_a_lifecycle_status_on_an_existing_node`
    at line 379, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_accepts_evidenced_proved
  how: 'defines public function `test_cli_done_accepts_evidenced_proved` at line 390,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_permits_pending_and_leans_without_evidence
  how: 'defines public function `test_cli_done_permits_pending_and_leans_without_evidence`
    at line 404, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_rejects_invalid_verdict
  how: 'defines public function `test_cli_done_rejects_invalid_verdict` at line 414,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_infers_evidence_from_node_frontmatter
  how: 'defines public function `test_cli_done_infers_evidence_from_node_frontmatter`
    at line 420, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_rejects_sentinel_evidence_runs
  how: 'defines public function `test_cli_done_rejects_sentinel_evidence_runs` at
    line 446, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_no_evidence_gate_bypasses_sentinel_rejection
  how: 'defines public function `test_cli_done_no_evidence_gate_bypasses_sentinel_rejection`
    at line 463, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_escape_hatch_is_loud
  how: 'defines public function `test_cli_done_escape_hatch_is_loud` at line 476,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wired_project
  how: 'defines public function `wired_project` at line 491, signature: (tmp_path,
    monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _wire
  how: 'defines private function `_wire` at line 504, signature: (iter_dir, agent)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_demotes_unevidenced_proved
  how: 'defines public function `test_post_wire_demotes_unevidenced_proved` at line
    510, signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_keeps_evidenced_proved
  how: 'defines public function `test_post_wire_keeps_evidenced_proved` at line 519,
    signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_permits_lean_without_evidence
  how: 'defines public function `test_post_wire_permits_lean_without_evidence` at
    line 529, signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_falls_back_to_node_frontmatter_evidence
  how: 'defines public function `test_post_wire_falls_back_to_node_frontmatter_evidence`
    at line 539, signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_creates_demoted_verdict_node_when_file_missing
  how: 'defines public function `test_post_wire_creates_demoted_verdict_node_when_file_missing`
    at line 555, signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_rejects_sentinel_evidence_runs
  how: 'defines public function `test_post_wire_rejects_sentinel_evidence_runs` at
    line 570, signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_sentinel_does_not_reject_uncertain_verdicts
  how: 'defines public function `test_post_wire_sentinel_does_not_reject_uncertain_verdicts`
    at line 583, signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "e1.md"
  how: '`(d / "e1.md").write_text(''---\nid: "exp:e1"\ntype: experiment\n---\n\nbody\n'')`
    at line 199'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "e2.md"
  how: '`(d / "e2.md").write_text("---\ntype: experiment\n---\n\nno id field\n")`
    at line 200'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 325'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sess / "agent.json"
  how: '`(sess / "agent.json").write_text(json.dumps({"id": "a1", "status": "running"}))`
    at line 329'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.write_text( "---\nid: experiment:e1\ntype: experiment\nstatus: proved\n"
    "tags:\n  - proved\n---\n\nbody\n" )` at line 365'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.write_text( "---\nid: experiment:e1\ntype: experiment\nstatus: pending\n---\n\nbody\n"
    )` at line 381'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / "experiment" / "e0.md"
  how: '`(project / "nodes" / "experiment" / "e0.md").write_text( ''---\nid: "experiment:e0"\ntype:
    experiment\n---\n\nbody\n'')` at line 394'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / "experiment" / "run-a.md"
  how: '`(project / "nodes" / "experiment" / "run-a.md").write_text( ''---\nid: "experiment:run-a"\ntype:
    experiment\n---\n\nrun a\n'' )` at line 428'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / "experiment" / "run-b.md"
  how: '`(project / "nodes" / "experiment" / "run-b.md").write_text( ''---\nid: "experiment:run-b"\ntype:
    experiment\n---\n\nrun b\n'' )` at line 431'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.write_text( "---\nid: experiment:e1\ntype: experiment\n" "evidence_runs:\n  -
    experiment:run-a\n  - experiment:run-b\n---\n\nran it twice\n" )` at line 435'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.write_text( "---\nid: experiment:e1\ntype: experiment\n" "evidence_runs:\n  -
    synthetic\n---\n\nbody\n" )` at line 451'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.write_text( "---\nid: experiment:e1\ntype: experiment\n" "evidence_runs:\n  -
    synthetic\n---\n\nbody\n" )` at line 465'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 492'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: exp / "e1.md"
  how: '`(exp / "e1.md").write_text( ''---\nid: "experiment:e1"\ntype: experiment\n---\n\nbody\n''
    )` at line 495'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_dir / "manifest.json"
  how: '`(iter_dir / "manifest.json").write_text(json.dumps({"agents": [agent]}))`
    at line 505'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: root / "nodes" / "experiment" / "r1.md"
  how: '`(root / "nodes" / "experiment" / "r1.md").write_text( ''---\nid: "experiment:r1"\ntype:
    experiment\n---\n\nbody\n'' )` at line 544'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: nf
  how: '`nf.write_text(''---\nid: "experiment:e1"\ntype: experiment\n'' "evidence_runs:\n  -
    experiment:r1\n---\n\nbody\n")` at line 548'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"id": "a1", "status": "running"})` at line 329'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"agents": [agent]})` at line 505'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
