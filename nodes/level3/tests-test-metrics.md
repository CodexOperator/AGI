---
confidence: 1.0
id: "level3:tests-test-metrics"
mint_id: b7c5dfcda1084e4eaf29fdcefbb40aa3
origin: level3-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_metrics.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/tests/test_metrics.py"
type: level3
---

`extensions/agi/tests/test_metrics.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
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
- name: test_empty_corpus_is_zero_not_a_crash
  how: 'defines public function `test_empty_corpus_is_zero_not_a_crash` at line 142,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_metrics_shares_evidence_gates_normalize_function
  how: defines public function `test_metrics_shares_evidence_gates_normalize_function`
    at line 148
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_gate_and_metrics_agree_on_the_same_input
  how: 'defines public function `test_gate_and_metrics_agree_on_the_same_input` at
    line 156, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_adding_hops_cannot_inflate_evidence_fraction
  how: 'defines public function `test_adding_hops_cannot_inflate_evidence_fraction`
    at line 167, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_compute_emits_the_full_metric_set
  how: 'defines public function `test_compute_emits_the_full_metric_set` at line 182,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_evidence_weighted_depth_is_zero_without_evidence
  how: 'defines public function `test_evidence_weighted_depth_is_zero_without_evidence`
    at line 194, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_deep_chain_does_not_blow_the_stack
  how: 'defines public function `test_deep_chain_does_not_blow_the_stack` at line
    203, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cycle_in_parents_terminates
  how: 'defines public function `test_cycle_in_parents_terminates` at line 217, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _goal
  how: 'defines private function `_goal` at line 227, signature: (root, gid, status)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_retired_goal_chains_stop_scoring_but_stay_attributable
  how: 'defines public function `test_retired_goal_chains_stop_scoring_but_stay_attributable`
    at line 231, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_horizon_goals_still_score
  how: 'defines public function `test_horizon_goals_still_score` at line 251, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unattributed_nodes_keep_scoring
  how: 'defines public function `test_unattributed_nodes_keep_scoring` at line 260,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_shared_with_a_live_goal_still_scores
  how: 'defines public function `test_node_shared_with_a_live_goal_still_scores` at
    line 273, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goal_status_counts_are_emitted
  how: 'defines public function `test_goal_status_counts_are_emitted` at line 283,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_exceeding_max_goals_active_warns_but_does_not_refuse
  how: 'defines public function `test_exceeding_max_goals_active_warns_but_does_not_refuse`
    at line 293, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_within_max_goals_active_is_silent
  how: 'defines public function `test_within_max_goals_active_is_silent` at line 308,
    signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goal_cycle_does_not_hang_attribution
  how: 'defines public function `test_goal_cycle_does_not_hang_attribution` at line
    317, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f'{slug}.md'
  how: '`(d / f''{slug}.md'').write_text(''\n''.join(lines))` at line 44'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'agi-tree.config.json'
  how: '`(tmp_path / ''agi-tree.config.json'').write_text(''{}'')` at line 49'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'agi-tree.config.json'
  how: '`(project / ''agi-tree.config.json'').write_text(json.dumps({''metric_primary'':
    ''longest_chain_length''}))` at line 74'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'agi-tree.config.json'
  how: '`(project / ''agi-tree.config.json'').write_text(json.dumps({''metric_primary'':
    ''evidence_fraction''}))` at line 85'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'agi-tree.config.json'
  how: '`(project / ''agi-tree.config.json'').write_text(json.dumps({''cc_dispatch'':
    {''max_goals_active'': 1}}))` at line 296'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'agi-tree.config.json'
  how: '`(project / ''agi-tree.config.json'').write_text(json.dumps({''cc_dispatch'':
    {''max_goals_active'': 3}}))` at line 309'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({''metric_primary'': ''longest_chain_length''})` at line 75'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({''metric_primary'': ''evidence_fraction''})` at line 86'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({''cc_dispatch'': {''max_goals_active'': 1}})` at line 297'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({''cc_dispatch'': {''max_goals_active'': 3}})` at line 310'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
