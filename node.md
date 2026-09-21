---
id: build:tests-test-brief
mint_id: 184e21275db745fe8fd795b97a15f8ec
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_brief.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_brief.py"
---
`extensions/agi/tests/test_brief.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_brief.py
parse_ok: true
inputs:
- name: sys
  how: '`import sys` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: brief
  how: '`import brief` at line 19'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: evidence_gate
  how: '`import evidence_gate` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pi_adapter
  how: '`import pi_adapter` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "adapters" / "pi_adapter.py"
  how: '`(BIN / "adapters" / "pi_adapter.py").read_text()` at line 133'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _text
  how: 'defines private function `_text` at line 31, signature: (tier, **kw)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_and_kid_get_different_briefs
  how: defines public function `test_parent_and_kid_get_different_briefs` at line
    38
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_unknown_tier_raises_instead_of_defaulting
  how: defines public function `test_an_unknown_tier_raises_instead_of_defaulting`
    at line 51
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verdict_taxonomy_is_derived_not_retyped
  how: 'defines public function `test_verdict_taxonomy_is_derived_not_retyped` at
    line 60, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_brief_carries_the_grandchild_bound
  how: defines public function `test_parent_brief_carries_the_grandchild_bound` at
    line 77
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_brief_forbids_committing_and_bypassing
  how: defines public function `test_parent_brief_forbids_committing_and_bypassing`
    at line 91
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_parent_with_no_target_still_gets_a_usable_brief
  how: defines public function `test_a_parent_with_no_target_still_gets_a_usable_brief`
    at line 97
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _cmd
  how: 'defines private function `_cmd` at line 108, signature: (tier, **kw)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_adapter_selects_the_tier_model_and_the_tier_brief
  how: defines public function `test_adapter_selects_the_tier_model_and_the_tier_brief`
    at line 118
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_adapter_holds_no_brief_text_of_its_own
  how: defines public function `test_the_adapter_holds_no_brief_text_of_its_own` at
    line 129
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_signals_done_with_owns_not_node_id
  how: defines public function `test_parent_signals_done_with_owns_not_node_id` at
    line 142
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_brief_sends_review_prose_to_the_kids_thought_block
  how: defines public function `test_parent_brief_sends_review_prose_to_the_kids_thought_block`
    at line 150
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_brief_names_the_thought_stopgap_as_temporary
  how: defines public function `test_parent_brief_names_the_thought_stopgap_as_temporary`
    at line 157
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_kid_brief_is_untouched_by_the_parent_artefact_change
  how: defines public function `test_kid_brief_is_untouched_by_the_parent_artefact_change`
    at line 165
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_kid_brief_forbids_git_and_requires_the_suite
  how: defines public function `test_kid_brief_forbids_git_and_requires_the_suite`
    at line 171
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_tiers_are_told_not_to_commit
  how: defines public function `test_both_tiers_are_told_not_to_commit` at line 182
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.