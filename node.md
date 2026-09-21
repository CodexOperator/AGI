---
id: build:tests-graph-core-test-identity
mint_id: 7763285db3cd4cf9a68a670d138374a7
type: build
parents:
  - idea:engine-tests-graph-core
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/graph_core/test_identity.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/graph_core/test_identity.py"
---
`extensions/agi/tests/graph_core/test_identity.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests-graph-core`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/graph_core/test_identity.py
parse_ok: true
inputs:
- name: json
  how: '`import json` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shutil
  how: '`import shutil` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: warnings
  how: '`import warnings` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.ALPHABET
  how: '`from graph_core.identity import ALPHABET` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.IdRegistry
  how: '`from graph_core.identity import IdRegistry` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.derive_slug
  how: '`from graph_core.identity import derive_slug` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.is_valid_address
  how: '`from graph_core.identity import is_valid_address` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.is_valid_mint_id
  how: '`from graph_core.identity import is_valid_mint_id` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.mint_address
  how: '`from graph_core.identity import mint_address` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.mint_id
  how: '`from graph_core.identity import mint_id` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.mint_permanent_id
  how: '`from graph_core.identity import mint_permanent_id` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.plan_reid
  how: '`from graph_core.identity import plan_reid` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity.supernode
  how: '`from graph_core.identity import supernode` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(out.read_text())` at line 233'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out
  how: '`out.read_text()` at line 233'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: test_slug_kebab_case_lowercase
  how: defines public function `test_slug_kebab_case_lowercase` at line 29
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_slug_caps_at_max_tokens
  how: defines public function `test_slug_caps_at_max_tokens` at line 35
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_id_format
  how: defines public function `test_mint_id_format` at line 41
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_collision_yields_suffix
  how: defines public function `test_collision_yields_suffix` at line 47
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_long_id_emits_user_warning
  how: defines public function `test_long_id_emits_user_warning` at line 58
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_stability_across_registries
  how: defines public function `test_stability_across_registries` at line 69
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_empty_source_yields_untitled
  how: defines public function `test_empty_source_yields_untitled` at line 79
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_alphabet_is_36_lowercase_alphanumeric
  how: defines public function `test_alphabet_is_36_lowercase_alphanumeric` at line
    88
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_address_known_seed_is_a_constant
  how: defines public function `test_mint_address_known_seed_is_a_constant` at line
    96
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_address_is_width_and_alphabet_bound
  how: defines public function `test_mint_address_is_width_and_alphabet_bound` at
    line 107
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_address_stable_under_insertion
  how: defines public function `test_mint_address_stable_under_insertion` at line
    113
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_address_collision_probe_is_deterministic
  how: defines public function `test_mint_address_collision_probe_is_deterministic`
    at line 136
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_plan_reid_collision_resolution_is_order_independent
  how: 'defines public function `test_plan_reid_collision_resolution_is_order_independent`
    at line 144, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_address_alphabet_only_and_git_ref_safe
  how: defines public function `test_mint_address_alphabet_only_and_git_ref_safe`
    at line 173
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_is_valid_address_rejects_wrong_width_and_bad_chars
  how: defines public function `test_is_valid_address_rejects_wrong_width_and_bad_chars`
    at line 193
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_supernode_truncation_round_trips
  how: defines public function `test_supernode_truncation_round_trips` at line 201
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_plan_reid_is_idempotent
  how: 'defines public function `test_plan_reid_is_idempotent` at line 210, signature:
    (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_plan_reid_writes_no_input_and_reports_references
  how: 'defines public function `test_plan_reid_writes_no_input_and_reports_references`
    at line 219, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_plan_reid_supernode_stats_match_manual_grouping
  how: 'defines public function `test_plan_reid_supernode_stats_match_manual_grouping`
    at line 237, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_plan_reid_rejects_duplicate_ids
  how: defines public function `test_plan_reid_rejects_duplicate_ids` at line 249
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_permanent_id_format
  how: defines public function `test_mint_permanent_id_format` at line 257
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_permanent_id_is_fresh_every_call_not_derived
  how: defines public function `test_mint_permanent_id_is_fresh_every_call_not_derived`
    at line 267
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_permanent_id_takes_no_seed_and_is_non_deterministic
  how: defines public function `test_mint_permanent_id_takes_no_seed_and_is_non_deterministic`
    at line 275
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_is_valid_mint_id_rejects_wrong_shape
  how: defines public function `test_is_valid_mint_id_rejects_wrong_shape` at line
    282
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_permanent_id_is_a_valid_git_ref_component
  how: defines public function `test_mint_permanent_id_is_a_valid_git_ref_component`
    at line 292
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.