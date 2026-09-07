---
id: build:tests-test-spawn-gate
mint_id: aecd41f39ffc49b0827e8ae22de44cfc
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_spawn_gate.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_spawn_gate.py"
---
`extensions/agi/tests/test_spawn_gate.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_spawn_gate.py
parse_ok: true
inputs:
- name: importlib.util
  how: '`import importlib.util` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: textwrap
  how: '`import textwrap` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wired_project / "nodes" / "verdict" / "bypassed.md"
  how: '`(wired_project / "nodes" / "verdict" / "bypassed.md").read_text()` at line
    507'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wired_project / "nodes" / "bigger_outcome" / "bo.md"
  how: '`(wired_project / "nodes" / "bigger_outcome" / "bo.md").read_text()` at line
    522'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wired_project / "nodes" / "verdict" / "exp_nonexistent.md"
  how: '`(wired_project / "nodes" / "verdict" / "exp_nonexistent.md").read_text()`
    at line 550'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / "post_wire.py"
  how: '`(BIN / "post_wire.py").read_text()` at line 563'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: zoom_py
  how: '`zoom_py.read_text()` at line 667'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node
  how: '`node.read_text()` at line 498'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node
  how: '`node.read_text()` at line 499'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _load
  how: 'defines private function `_load` at line 33, signature: (name, filename=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 131, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: gate
  how: 'defines public function `gate` at line 159, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_loads_every_active_schema_and_no_inactive_one
  how: 'defines public function `test_loads_every_active_schema_and_no_inactive_one`
    at line 168, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_geometry_comes_from_shape_md
  how: 'defines public function `test_geometry_comes_from_shape_md` at line 177, signature:
    (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_shape_key_canonicalises_type_half_only
  how: defines public function `test_shape_key_canonicalises_type_half_only` at line
    185
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_config_md_is_actually_read_for_nodes_root
  how: 'defines public function `test_config_md_is_actually_read_for_nodes_root` at
    line 194, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_config_falls_back_to_nodes
  how: 'defines public function `test_missing_config_falls_back_to_nodes` at line
    204, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_min_parents_zero_outside_the_whitelist_is_a_schema_error
  how: 'defines public function `test_min_parents_zero_outside_the_whitelist_is_a_schema_error`
    at line 213, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_max_parents_above_the_ceiling_is_a_schema_error
  how: 'defines public function `test_max_parents_above_the_ceiling_is_a_schema_error`
    at line 225, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_verdict_with_no_parent_is_rejected_naming_rule_and_schema
  how: 'defines public function `test_verdict_with_no_parent_is_rejected_naming_rule_and_schema`
    at line 239, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_task_with_three_parents_is_rejected
  how: 'defines public function `test_task_with_three_parents_is_rejected` at line
    251, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_legal_spawn_is_explicitly_approved
  how: 'defines public function `test_legal_spawn_is_explicitly_approved` at line
    262, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_wrong_parent_type_is_rejected
  how: 'defines public function `test_wrong_parent_type_is_rejected` at line 276,
    signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_idea_may_be_parentless
  how: 'defines public function `test_idea_may_be_parentless` at line 289, signature:
    (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goal_roots_may_be_parentless
  how: 'defines public function `test_goal_roots_may_be_parentless` at line 297, signature:
    (gate, kind)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_subgoal_may_not_be_parentless
  how: 'defines public function `test_subgoal_may_not_be_parentless` at line 304,
    signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_subgoal_with_one_goal_parent_is_approved
  how: 'defines public function `test_subgoal_with_one_goal_parent_is_approved` at
    line 314, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_discriminator_is_unverified_not_approved
  how: 'defines public function `test_missing_discriminator_is_unverified_not_approved`
    at line 321, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_type_is_unverified_and_written
  how: 'defines public function `test_unknown_type_is_unverified_and_written` at line
    332, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_schema_without_spawn_block_is_unverified
  how: 'defines public function `test_schema_without_spawn_block_is_unverified` at
    line 339, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unresolvable_parent_is_unverified_never_invented
  how: 'defines public function `test_unresolvable_parent_is_unverified_never_invented`
    at line 346, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_type_index_declines_to_approve
  how: 'defines public function `test_no_type_index_declines_to_approve` at line 355,
    signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bypass_is_loud_and_stamped
  how: 'defines public function `test_bypass_is_loud_and_stamped` at line 363, signature:
    (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_approval_is_not_stamped
  how: 'defines public function `test_approval_is_not_stamped` at line 373, signature:
    (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unverified_is_stamped_with_a_reason
  how: 'defines public function `test_unverified_is_stamped_with_a_reason` at line
    379, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_spellings_resolve_to_one_rule
  how: 'defines public function `test_both_spellings_resolve_to_one_rule` at line
    392, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_parent_typed_with_a_hyphen_still_validates
  how: 'defines public function `test_parent_typed_with_a_hyphen_still_validates`
    at line 409, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_announce_prints_on_approval_too
  how: 'defines public function `test_announce_prints_on_approval_too` at line 433,
    signature: (gate, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_announce_prints_on_rejection
  how: 'defines public function `test_announce_prints_on_rejection` at line 441, signature:
    (gate, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _run_cli
  how: 'defines private function `_run_cli` at line 453, signature: (project, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wired_project
  how: 'defines public function `wired_project` at line 461, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_scaffold_rejects_a_parentless_verdict
  how: 'defines public function `test_cli_scaffold_rejects_a_parentless_verdict` at
    line 469, signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_scaffold_rejects_a_task_with_three_parents
  how: 'defines public function `test_cli_scaffold_rejects_a_task_with_three_parents`
    at line 480, signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_scaffold_approves_and_says_so
  how: 'defines public function `test_cli_scaffold_approves_and_says_so` at line 489,
    signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_scaffold_bypass_is_stamped
  how: 'defines public function `test_cli_scaffold_bypass_is_stamped` at line 502,
    signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_scaffold_canonicalises_the_type_spelling
  how: 'defines public function `test_cli_scaffold_canonicalises_the_type_spelling`
    at line 511, signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_gates_its_fallback_verdict_node
  how: 'defines public function `test_cli_done_gates_its_fallback_verdict_node` at
    line 529, signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_done_fallback_writes_mint_id_when_approved
  how: 'defines public function `test_cli_done_fallback_writes_mint_id_when_approved`
    at line 542, signature: (wired_project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_post_wire_reaches_the_gate_through_the_one_writer
  how: defines public function `test_post_wire_reaches_the_gate_through_the_one_writer`
    at line 556
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_shipped_schemas_load_without_error
  how: defines public function `test_shipped_schemas_load_without_error` at line 575
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _shipped_schemas_dir
  how: defines private function `_shipped_schemas_dir` at line 601
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _flat_or_variants
  how: 'defines private function `_flat_or_variants` at line 618, signature: (schema)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_goal_may_not_parent_mvp_or_experiment
  how: defines public function `test_goal_may_not_parent_mvp_or_experiment` at line
    625
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_kid_contract_advertises_only_gate_legal_routes
  how: defines public function `test_kid_contract_advertises_only_gate_legal_routes`
    at line 652
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: converging
  how: 'defines public function `converging` at line 711, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _check
  how: 'defines private function `_check` at line 723, signature: (project, ntype,
    parents, **kw)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_min_by_type_approves_one_of_each
  how: 'defines public function `test_min_by_type_approves_one_of_each` at line 728,
    signature: (converging)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_min_by_type_rejects_right_arity_wrong_mix
  how: 'defines public function `test_min_by_type_rejects_right_arity_wrong_mix` at
    line 734, signature: (converging)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_min_by_type_shortfall_names_every_missing_kind
  how: 'defines public function `test_min_by_type_shortfall_names_every_missing_kind`
    at line 745, signature: (converging)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_min_by_type_unresolvable_parent_is_unverified_not_rejected
  how: 'defines public function `test_min_by_type_unresolvable_parent_is_unverified_not_rejected`
    at line 752, signature: (converging)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _schema_err
  how: 'defines private function `_schema_err` at line 759, signature: (project, body,
    fname=''[bigger_outcome].md'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_min_by_type_requiring_a_forbidden_type_is_a_schema_error
  how: 'defines public function `test_min_by_type_requiring_a_forbidden_type_is_a_schema_error`
    at line 765, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_min_by_type_exceeding_max_parents_is_a_schema_error
  how: 'defines public function `test_min_by_type_exceeding_max_parents_is_a_schema_error`
    at line 774, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_min_by_type_zero_is_a_schema_error_not_a_silent_noop
  how: 'defines public function `test_min_by_type_zero_is_a_schema_error_not_a_silent_noop`
    at line 783, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_broken_min_by_type_schema_is_not_enforced
  how: 'defines public function `test_a_broken_min_by_type_schema_is_not_enforced`
    at line 791, signature: (converging)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_absent_min_by_type_changes_nothing
  how: 'defines public function `test_absent_min_by_type_changes_nothing` at line
    800, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_scheduling_edges_are_not_traversable
  how: 'defines public function `test_scheduling_edges_are_not_traversable` at line
    826, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_undeclared_edge_field_stays_traversable
  how: 'defines public function `test_undeclared_edge_field_stays_traversable` at
    line 834, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_absent_edge_fields_leaves_every_edge_traversable
  how: 'defines public function `test_absent_edge_fields_leaves_every_edge_traversable`
    at line 841, signature: (gate)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / "agi-tree.config.json"
  how: '`(tmp_path / "agi-tree.config.json").write_text("{}")` at line 133'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sd / "mvp.md"
  how: '`(sd / "mvp.md").write_text( "---\nname: mvp\nspawn:\n  allowed_parents: []\n"
    "  min_parents: 0\n  max_parents: 9\n---\ninactive\n" )` at line 143'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "schemas" / "[config].md"
  how: '`(project / "context" / "schemas" / "[config].md").write_text( CONFIG.replace("<graph_root>/nodes",
    "<graph_root>/elsewhere") )` at line 198'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "schemas" / "[task].md"
  how: '`(project / "context" / "schemas" / "[task].md").write_text( TASK.replace("min_parents:
    1", "min_parents: 0") )` at line 214'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "schemas" / "[task].md"
  how: '`(project / "context" / "schemas" / "[task].md").write_text( TASK.replace("max_parents:
    1", "max_parents: 5") )` at line 226'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sd / "[bigger_outcome].md"
  how: '`(sd / "[bigger_outcome].md").write_text( "---\nname: bigger_outcome\nspawn:\n"
    "  allowed_parents: [outcome, mvp]\n  min_parents: 1\n" "  max_parents: 2\n---\nb\n"
    )` at line 394'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / "outcome" / "o1.md"
  how: '`(project / "nodes" / "outcome" / "o1.md").write_text( "---\nid: outcome:o1\ntype:
    outcome\n---\n\nb\n")` at line 400'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sd / "[app_purpose].md"
  how: '`(sd / "[app_purpose].md").write_text( "---\nname: app_purpose\nspawn:\n"
    "  allowed_parents: [bigger_outcome, outcome]\n  min_parents: 1\n" "  max_parents:
    2\n---\na\n" )` at line 414'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "b1.md"
  how: '`(d / "b1.md").write_text( "---\nid: bigger-outcome:b1\ntype: bigger-outcome\n---\n\nb\n")`
    at line 421'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ad / "agent.json"
  how: '`(ad / "agent.json").write_text(json.dumps({"id": "a1", "status": "run"}))`
    at line 465'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: wired_project / "context" / "schemas" / "[bigger_outcome].md"
  how: '`(wired_project / "context" / "schemas" / "[bigger_outcome].md").write_text(
    "---\nname: bigger_outcome\nspawn:\n  allowed_parents: [outcome, mvp]\n" "  min_parents:
    1\n  max_parents: 2\n---\nb\n")` at line 512'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / "o1.md"
  how: '`(d / "o1.md").write_text("---\nid: outcome:o1\ntype: outcome\n---\n\nb\n")`
    at line 517'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "schemas" / "[bigger_outcome].md"
  how: '`(project / "context" / "schemas" / "[bigger_outcome].md").write_text(BIGGER_OUTCOME)`
    at line 713'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "schemas" / fname
  how: '`(project / "context" / "schemas" / fname).write_text(body)` at line 760'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: converging / "context" / "schemas" / "[bigger_outcome].md"
  how: '`(converging / "context" / "schemas" / "[bigger_outcome].md").write_text(
    BIGGER_OUTCOME.replace("min_parents_by_type: {verdict: 1, outcome: 1}", "min_parents_by_type:
    [verdict, outcome]"))` at line 793'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "schemas" / "[shape].md"
  how: '`(project / "context" / "schemas" / "[shape].md").write_text(SHAPE_WITH_EDGES)`
    at line 827'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "context" / "schemas" / "[shape].md"
  how: '`(project / "context" / "schemas" / "[shape].md").write_text(SHAPE_WITH_EDGES)`
    at line 836'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sd / fname
  how: '`(sd / fname).write_text(body)` at line 141'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f"{slug}.md"
  how: '`(d / f"{slug}.md").write_text( f"---\nid: {ntype}:{slug}\ntype: {ntype}\n---\n\nbody\n"
    )` at line 152'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({"id": "a1", "status": "run"})` at line 465'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f"{slug}.md"
  how: '`(d / f"{slug}.md").write_text( f"---\nid: {ntype}:{slug}\ntype: {ntype}\n---\n\nbody\n"
    )` at line 717'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.