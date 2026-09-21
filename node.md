---
id: build:tests-test-metrics
mint_id: b7c5dfcda1084e4eaf29fdcefbb40aa3
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_metrics.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_metrics.py"
---
`extensions/agi/tests/test_metrics.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_metrics.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: io
  how: '`import io` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _node
  how: 'defines private function `_node` at line 34, signature: (root, ntype, slug,
    fm_extra='''', parents=())'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 48, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_default_primary_is_not_the_gameable_metric
  how: defines public function `test_default_primary_is_not_the_gameable_metric` at
    line 57
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_primary_falls_back_to_default_when_config_omits_it
  how: defines public function `test_primary_falls_back_to_default_when_config_omits_it`
    at line 62
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_primary_honours_config
  how: defines public function `test_primary_honours_config` at line 68
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_gameable_primary_emits_a_warning
  how: 'defines public function `test_gameable_primary_emits_a_warning` at line 73,
    signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_emit_prints_primary_name_and_value
  how: 'defines public function `test_emit_prints_primary_name_and_value` at line
    84, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_evidence_fraction_counts_only_asserting_verdicts
  how: 'defines public function `test_evidence_fraction_counts_only_asserting_verdicts`
    at line 100, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_sentinel_evidence_runs_does_not_count_as_backed
  how: 'defines public function `test_sentinel_evidence_runs_does_not_count_as_backed`
    at line 113, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pending_without_evidence_does_not_lower_the_score
  how: 'defines public function `test_pending_without_evidence_does_not_lower_the_score`
    at line 123, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unevidenced_decisive_counter_is_the_gate_violation_alarm
  how: 'defines public function `test_unevidenced_decisive_counter_is_the_gate_violation_alarm`
    at line 133, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_resolvable_reference_still_counts_as_evidence
  how: 'defines public function `test_a_resolvable_reference_still_counts_as_evidence`
    at line 145, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_empty_corpus_is_zero_not_a_crash
  how: 'defines public function `test_empty_corpus_is_zero_not_a_crash` at line 155,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_shadow_counter_catches_a_status_that_contradicts_its_verdict
  how: 'defines public function `test_shadow_counter_catches_a_status_that_contradicts_its_verdict`
    at line 162, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_shadow_counter_catches_a_verdict_expressed_only_as_status
  how: 'defines public function `test_shadow_counter_catches_a_verdict_expressed_only_as_status`
    at line 174, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_shadow_counter_ignores_a_status_its_verdict_agrees_with
  how: 'defines public function `test_shadow_counter_ignores_a_status_its_verdict_agrees_with`
    at line 185, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_shadow_counter_ignores_lifecycle_statuses
  how: 'defines public function `test_shadow_counter_ignores_lifecycle_statuses` at
    line 191, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_shadow_counter_ignores_tags
  how: 'defines public function `test_shadow_counter_ignores_tags` at line 199, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_metrics_shares_evidence_gates_normalize_function
  how: defines public function `test_metrics_shares_evidence_gates_normalize_function`
    at line 206
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_gate_and_metrics_agree_on_the_same_input
  how: 'defines public function `test_gate_and_metrics_agree_on_the_same_input` at
    line 214, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_adding_hops_cannot_inflate_evidence_fraction
  how: 'defines public function `test_adding_hops_cannot_inflate_evidence_fraction`
    at line 225, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_compute_emits_the_full_metric_set
  how: 'defines public function `test_compute_emits_the_full_metric_set` at line 240,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_evidence_weighted_depth_is_zero_without_evidence
  how: 'defines public function `test_evidence_weighted_depth_is_zero_without_evidence`
    at line 252, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_deep_chain_does_not_blow_the_stack
  how: 'defines public function `test_deep_chain_does_not_blow_the_stack` at line
    261, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cycle_in_parents_terminates
  how: 'defines public function `test_cycle_in_parents_terminates` at line 275, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _goal
  how: 'defines private function `_goal` at line 285, signature: (root, gid, status)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_retired_goal_chains_stop_scoring_but_stay_attributable
  how: 'defines public function `test_retired_goal_chains_stop_scoring_but_stay_attributable`
    at line 289, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_horizon_goals_still_score
  how: 'defines public function `test_horizon_goals_still_score` at line 312, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unattributed_nodes_keep_scoring
  how: 'defines public function `test_unattributed_nodes_keep_scoring` at line 321,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_shared_with_a_live_goal_still_scores
  how: 'defines public function `test_node_shared_with_a_live_goal_still_scores` at
    line 334, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goal_status_counts_are_emitted
  how: 'defines public function `test_goal_status_counts_are_emitted` at line 344,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_completing_a_goal_does_not_move_the_metric
  how: 'defines public function `test_completing_a_goal_does_not_move_the_metric`
    at line 366, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_retiring_a_goal_removes_its_closed_chain_from_both_terms
  how: 'defines public function `test_retiring_a_goal_removes_its_closed_chain_from_both_terms`
    at line 388, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_retiring_a_goal_with_no_chain_changes_nothing
  how: 'defines public function `test_retiring_a_goal_with_no_chain_changes_nothing`
    at line 409, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_retiring_cannot_launder_unconverted_hypotheses_out_of_the_ratio
  how: 'defines public function `test_retiring_cannot_launder_unconverted_hypotheses_out_of_the_ratio`
    at line 427, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_legacy_phasing_out_still_reads_as_retired
  how: 'defines public function `test_legacy_phasing_out_still_reads_as_retired` at
    line 453, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_exceeding_max_goals_active_warns_but_does_not_refuse
  how: 'defines public function `test_exceeding_max_goals_active_warns_but_does_not_refuse`
    at line 465, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_within_max_goals_active_is_silent
  how: 'defines public function `test_within_max_goals_active_is_silent` at line 480,
    signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goal_cycle_does_not_hang_attribution
  how: 'defines public function `test_goal_cycle_does_not_hang_attribution` at line
    489, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_deprecated_nodes_are_counted
  how: 'defines public function `test_deprecated_nodes_are_counted` at line 505, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_count_does_not_drop_when_a_node_is_deprecated
  how: 'defines public function `test_node_count_does_not_drop_when_a_node_is_deprecated`
    at line 514, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_graph_with_no_deprecations_reads_zero_not_absent
  how: 'defines public function `test_a_graph_with_no_deprecations_reads_zero_not_absent`
    at line 531, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_lifecycle_count_is_not_goal_attribution
  how: 'defines public function `test_lifecycle_count_is_not_goal_attribution` at
    line 540, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_deprecated_status_tolerates_case_and_whitespace
  how: 'defines public function `test_deprecated_status_tolerates_case_and_whitespace`
    at line 562, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_other_statuses_are_not_deprecation
  how: 'defines public function `test_other_statuses_are_not_deprecation` at line
    568, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_lifecycle_counts_reach_the_metric_lines
  how: 'defines public function `test_lifecycle_counts_reach_the_metric_lines` at
    line 577, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f"{slug}.md"
  how: '`(d / f"{slug}.md").write_text("\n".join(lines))` at line 44'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 49'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "agi-tree.config.json"
  how: '`(project / "agi-tree.config.json").write_text( json.dumps({"metric_primary":
    "longest_chain_length"}) )` at line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "agi-tree.config.json"
  how: '`(project / "agi-tree.config.json").write_text( json.dumps({"metric_primary":
    "evidence_fraction"}) )` at line 85'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "agi-tree.config.json"
  how: '`(project / "agi-tree.config.json").write_text( json.dumps({"cc_dispatch":
    {"max_goals_active": 1}}) )` at line 468'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "agi-tree.config.json"
  how: '`(project / "agi-tree.config.json").write_text( json.dumps({"cc_dispatch":
    {"max_goals_active": 3}}) )` at line 481'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"metric_primary": "longest_chain_length"})` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"metric_primary": "evidence_fraction"})` at line 86'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"cc_dispatch": {"max_goals_active": 1}})` at line 469'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"cc_dispatch": {"max_goals_active": 3}})` at line 482'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.