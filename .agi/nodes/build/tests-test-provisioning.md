---
build_kind: code
confidence: 1.0
id: "build:tests-test-provisioning"
mint_id: b308abe0539a4aeca66c792ac3af0eb5
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_provisioning.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_provisioning.py"
type: build
---

`extensions/agi/tests/test_provisioning.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_provisioning.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: provisioning
  how: '`import provisioning` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: spawn_budget
  how: '`import spawn_budget` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: lease.path
  how: '`lease.path.read_text()` at line 211'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(on_disk)` at line 214'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(on_disk)` at line 213'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: test_availability_is_false_without_a_key_and_never_raises
  how: 'defines public function `test_availability_is_false_without_a_key_and_never_raises`
    at line 41, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_returns_none_rather_than_raising_when_unavailable
  how: 'defines public function `test_mint_returns_none_rather_than_raising_when_unavailable`
    at line 47, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_provisioning_key_is_scrubbed_from_child_environments
  how: 'defines public function `test_the_provisioning_key_is_scrubbed_from_child_environments`
    at line 64, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_settings_come_from_config_not_from_constants
  how: defines public function `test_settings_come_from_config_not_from_constants`
    at line 86
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_settings_fall_back_to_small_defaults
  how: defines public function `test_settings_fall_back_to_small_defaults` at line
    91
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_key_name_carries_the_iteration_and_the_agent
  how: defines public function `test_a_key_name_carries_the_iteration_and_the_agent`
    at line 98
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_reap_only_ever_touches_keys_this_engine_minted
  how: 'defines public function `test_reap_only_ever_touches_keys_this_engine_minted`
    at line 105, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_workspace_is_read_from_config_and_absent_means_absent
  how: defines public function `test_workspace_is_read_from_config_and_absent_means_absent`
    at line 124
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_settings_signature_is_unchanged_by_the_workspace_addition
  how: defines public function `test_settings_signature_is_unchanged_by_the_workspace_addition`
    at line 134
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_sends_workspace_id_only_when_one_is_configured
  how: 'defines public function `test_mint_sends_workspace_id_only_when_one_is_configured`
    at line 142, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_reaper_will_not_cross_a_workspace_boundary
  how: 'defines public function `test_the_reaper_will_not_cross_a_workspace_boundary`
    at line 168, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_only_the_hash_is_written_to_the_lease_never_the_secret
  how: 'defines public function `test_only_the_hash_is_written_to_the_lease_never_the_secret`
    at line 203, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_swept_lease_surrenders_its_credential_hash
  how: 'defines public function `test_a_swept_lease_surrenders_its_credential_hash`
    at line 218, signature: (tmp_path, monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_credit_balance_returns_none_when_key_is_absent
  how: 'defines public function `test_credit_balance_returns_none_when_key_is_absent`
    at line 244, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_can_fund_passes_when_key_is_absent
  how: 'defines public function `test_can_fund_passes_when_key_is_absent` at line
    250, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_refuses_when_credits_are_exhausted
  how: 'defines public function `test_mint_refuses_when_credits_are_exhausted` at
    line 258, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_proceeds_when_credits_are_sufficient
  how: 'defines public function `test_mint_proceeds_when_credits_are_sufficient` at
    line 289, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_credit_balance_live
  how: defines public function `test_credit_balance_live` at line 313
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_live_can_fund_passes_with_sufficient_balance
  how: defines public function `test_live_can_fund_passes_with_sufficient_balance`
    at line 325
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_minted_key_is_capped_and_expires_and_can_be_revoked
  how: defines public function `test_a_minted_key_is_capped_and_expires_and_can_be_revoked`
    at line 340
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_expires_in_seconds_is_silently_ignored_and_we_do_not_use_it
  how: defines public function `test_expires_in_seconds_is_silently_ignored_and_we_do_not_use_it`
    at line 360
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_mint_refuses_to_hand_out_a_key_with_no_ttl
  how: 'defines public function `test_mint_refuses_to_hand_out_a_key_with_no_ttl`
    at line 384, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_list_keys_asks_for_the_workspace_it_was_given
  how: 'defines public function `test_list_keys_asks_for_the_workspace_it_was_given`
    at line 406, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_list_all_keys_unions_every_workspace
  how: 'defines public function `test_list_all_keys_unions_every_workspace` at line
    434, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pi_harness_needs_a_credential
  how: defines public function `test_pi_harness_needs_a_credential` at line 458
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_claude_code_harness_does_not_need_a_credential
  how: defines public function `test_claude_code_harness_does_not_need_a_credential`
    at line 463
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dispatch_mints_only_for_harnesses_that_need_it
  how: 'defines public function `test_dispatch_mints_only_for_harnesses_that_need_it`
    at line 468, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_removing_the_harness_check_restores_unconditional_minting
  how: 'defines public function `test_removing_the_harness_check_restores_unconditional_minting`
    at line 489, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _fake_key_usage
  how: 'defines private function `_fake_key_usage` at line 526, signature: (label=''agg-live'',
    limit=10.0, remaining=8.0)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_key_usage_decodes_limit_usage_remaining_from_the_key_endpoint
  how: 'defines public function `test_key_usage_decodes_limit_usage_remaining_from_the_key_endpoint`
    at line 535, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_key_usage_reports_uncapped_key_as_unlimited
  how: 'defines public function `test_key_usage_reports_uncapped_key_as_unlimited`
    at line 553, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_prints_key_limit_usage_remaining
  how: 'defines public function `test_status_prints_key_limit_usage_remaining` at
    line 569, signature: (monkeypatch, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_status_says_unlimited_when_no_limit
  how: 'defines public function `test_status_says_unlimited_when_no_limit` at line
    583, signature: (monkeypatch, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dispatch_refuses_below_floor_naming_the_key
  how: 'defines public function `test_dispatch_refuses_below_floor_naming_the_key`
    at line 591, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dispatch_spawns_when_remaining_above_floor
  how: 'defines public function `test_dispatch_spawns_when_remaining_above_floor`
    at line 604, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_check_fails_open_on_network_error
  how: 'defines public function `test_check_fails_open_on_network_error` at line 612,
    signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_floor_reads_from_config_with_default
  how: 'defines public function `test_floor_reads_from_config_with_default` at line
    623, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / ".agi" / "config.json"
  how: '`(tmp_path / ".agi" / "config.json").write_text("{}")` at line 43'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / ".agi" / "config.json"
  how: '`(tmp_path / ".agi" / "config.json").write_text("{}")` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "ghost.lease"
  how: '`(d / "ghost.lease").write_text(json.dumps( {"agent_id": "ghost", "holder_pid":
    999_999_999, "agent_pid": None, "key_hash": "h-orphan"}))` at line 228'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / ".agi" / "config.json"
  how: '`(tmp_path / ".agi" / "config.json").write_text("{}")` at line 246'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / ".agi" / "config.json"
  how: '`(tmp_path / ".agi" / "config.json").write_text("{}")` at line 252'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(env)` at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps( {"agent_id": "ghost", "holder_pid": 999_999_999, "agent_pid":
    None, "key_hash": "h-orphan"})` at line 228'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
