---
id: build:tests-test-level3
mint_id: d836169ba7d84493bc008da4cae4a50d
type: build
parents:
  - idea:engine-tests
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/tests/test_level3.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/tests/test_level3.py"
---
`extensions/agi/tests/test_level3.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_level3.py
parse_ok: true
inputs:
- name: ast
  how: '`import ast` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 11'
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
- name: yaml
  how: '`import yaml` at line 16'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph_core.identity
  how: '`from graph_core import identity` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(yaml_block)` at line 141'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.read_text(encoding="utf-8")` at line 424'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Path(__file__).resolve().parents[1] / "bin" / "stitch.py"
  how: '`(Path(__file__).resolve().parents[1] / "bin" / "stitch.py").read_text()`
    at line 612'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])` at line
    131'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 408'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.read_bytes()` at line 411'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 135'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 934'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 131'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: write_engine_tree
  how: 'defines public function `write_engine_tree` at line 93, signature: (root:
    Path, files: dict[str, str] | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine
  how: 'defines public function `engine` at line 107, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 112, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: run
  how: 'defines public function `run` at line 122, signature: (project: Path, engine:
    Path | None, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fm_of
  how: 'defines public function `fm_of` at line 130, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: body_of
  how: 'defines public function `body_of` at line 134, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: contract_of
  how: 'defines public function `contract_of` at line 138, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: level3_nodes
  how: 'defines public function `level3_nodes` at line 144, signature: (project: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_node
  how: 'defines public function `write_node` at line 149, signature: (project: Path,
    rel: str, fm: dict, body: str=''body'', origin: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_default_engine_root_points_at_this_repo
  how: defines public function `test_default_engine_root_points_at_this_repo` at line
    159
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_discovers_every_file_passing_the_g6_8_boundary
  how: 'defines public function `test_discovers_every_file_passing_the_g6_8_boundary`
    at line 168, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_files_scanned_count_matches_the_boundary
  how: 'defines public function `test_files_scanned_count_matches_the_boundary` at
    line 197, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_python_payload_is_honest_about_not_being_parsed
  how: 'defines public function `test_non_python_payload_is_honest_about_not_being_parsed`
    at line 206, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_empty_scope_is_refused_never_treated_as_prune_everything
  how: 'defines public function `test_empty_scope_is_refused_never_treated_as_prune_everything`
    at line 218, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_frontmatter_uses_payload_ref_and_origin_only
  how: 'defines public function `test_frontmatter_uses_payload_ref_and_origin_only`
    at line 238, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_imports_and_top_level_defs_are_derived
  how: 'defines public function `test_imports_and_top_level_defs_are_derived` at line
    259, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_read_write_calls_argv_env_stdout_are_derived
  how: 'defines public function `test_read_write_calls_argv_env_stdout_are_derived`
    at line 281, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_literal_open_mode_is_uncovered_not_guessed
  how: 'defines public function `test_non_literal_open_mode_is_uncovered_not_guessed`
    at line 300, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_syntax_error_file_gets_parse_ok_false_and_empty_contract
  how: 'defines public function `test_syntax_error_file_gets_parse_ok_false_and_empty_contract`
    at line 318, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_empty_file_gets_empty_but_present_contract_lists
  how: 'defines public function `test_empty_file_gets_empty_but_present_contract_lists`
    at line 328, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bin_script_matches_exact_unit_path
  how: 'defines public function `test_bin_script_matches_exact_unit_path` at line
    340, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_src_package_matches_directory_prefix
  how: 'defines public function `test_src_package_matches_directory_prefix` at line
    346, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_matching_unit_is_parentless_and_flagged
  how: 'defines public function `test_no_matching_unit_is_parentless_and_flagged`
    at line 352, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_engine_root_is_noop
  how: 'defines public function `test_missing_engine_root_is_noop` at line 365, signature:
    (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_non_git_engine_root_is_noop
  how: 'defines public function `test_non_git_engine_root_is_noop` at line 373, signature:
    (project, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_missing_engine_root_prunes_nothing
  how: 'defines public function `test_missing_engine_root_prunes_nothing` at line
    382, signature: (project, engine, tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dry_run_writes_nothing
  how: 'defines public function `test_dry_run_writes_nothing` at line 396, signature:
    (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_idempotent_byte_identical
  how: 'defines public function `test_idempotent_byte_identical` at line 406, signature:
    (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_write_twice_round_trip_preserves_foreign_field
  how: 'defines public function `test_write_twice_round_trip_preserves_foreign_field`
    at line 420, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prune_removes_stale_level3_scan_but_spares_others
  how: 'defines public function `test_prune_removes_stale_level3_scan_but_spares_others`
    at line 444, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_node_stamped_with_the_LEGACY_origin_is_never_pruned
  how: 'defines public function `test_a_node_stamped_with_the_LEGACY_origin_is_never_pruned`
    at line 469, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_build_kind_is_derived_from_the_payload_suffix
  how: defines public function `test_build_kind_is_derived_from_the_payload_suffix`
    at line 501
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_project_local_script_lookup_argument_exists
  how: defines public function `test_no_project_local_script_lookup_argument_exists`
    at line 512
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_entry_point_units_can_be_matched_as_parents
  how: 'defines public function `test_entry_point_units_can_be_matched_as_parents`
    at line 521, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _contract_of
  how: 'defines private function `_contract_of` at line 546, signature: (body)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unfilled_entries_are_todo
  how: defines public function `test_unfilled_entries_are_todo` at line 552
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_authored_fields_carry_over
  how: defines public function `test_authored_fields_carry_over` at line 559
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_how_is_always_re_derived_never_carried
  how: defines public function `test_how_is_always_re_derived_never_carried` at line
    570
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_carry_over_survives_a_line_number_change
  how: defines public function `test_carry_over_survives_a_line_number_change` at
    line 579
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_duplicate_names_are_matched_positionally
  how: defines public function `test_duplicate_names_are_matched_positionally` at
    line 590
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_prior_index_tolerates_a_missing_or_broken_contract
  how: defines public function `test_prior_index_tolerates_a_missing_or_broken_contract`
    at line 598
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_extract_contract_is_owned_here_not_in_stitch
  how: defines public function `test_extract_contract_is_owned_here_not_in_stitch`
    at line 607
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_contract_marker_spellings_still_parse
  how: defines public function `test_both_contract_marker_spellings_still_parse` at
    line 617
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_contract_reader_bounds_on_an_embedded_fence
  how: defines public function `test_contract_reader_bounds_on_an_embedded_fence`
    at line 627
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_scan_rewrites_a_retired_node_in_place_not_at_its_old_address
  how: 'defines public function `test_scan_rewrites_a_retired_node_in_place_not_at_its_old_address`
    at line 641, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_scan_does_not_prune_a_retired_node
  how: 'defines public function `test_scan_does_not_prune_a_retired_node` at line
    672, signature: (project, engine)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_node_type_dirs_is_live_first_and_skips_absent
  how: 'defines public function `test_node_type_dirs_is_live_first_and_skips_absent`
    at line 689, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sole_how
  how: 'defines private function `_sole_how` at line 743, signature: (analysis, section)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_how_quotes_the_payload_source_rather_than_re_rendering_it
  how: defines public function `test_how_quotes_the_payload_source_rather_than_re_rendering_it`
    at line 749
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_re_rendering_is_lossy_in_a_version_independent_way
  how: defines public function `test_re_rendering_is_lossy_in_a_version_independent_way`
    at line 775
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_derived_entry_names_are_source_slices_too
  how: defines public function `test_derived_entry_names_are_source_slices_too` at
    line 789
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_how_is_always_one_line_even_when_the_call_is_not
  how: defines public function `test_how_is_always_one_line_even_when_the_call_is_not`
    at line 804
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_one_line_never_touches_whitespace_inside_a_line
  how: defines public function `test_one_line_never_touches_whitespace_inside_a_line`
    at line 820
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_signature_is_the_only_place_ast_unparse_still_runs
  how: defines public function `test_signature_is_the_only_place_ast_unparse_still_runs`
    at line 834
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_scanners_refuse_to_default_the_source
  how: defines public function `test_scanners_refuse_to_default_the_source` at line
    859
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_derived_how_and_name_round_trip_through_the_contract_yaml
  how: 'defines public function `test_derived_how_and_name_round_trip_through_the_contract_yaml`
    at line 873, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_derivation_is_a_fixed_point_over_its_own_output
  how: 'defines public function `test_derivation_is_a_fixed_point_over_its_own_output`
    at line 896, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_engine_signature_contains_an_fstring
  how: defines public function `test_no_engine_signature_contains_an_fstring` at line
    914
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_path
  how: '`node_path.write_text( f"---{head}next_edges:\n  - hyp:graph-core-r1\n" f"embedding_coords:
    [0.1, 0.2]\n---{body}", encoding="utf-8", )` at line 426'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: p
  how: '`p.write_text(content, encoding="utf-8")` at line 100'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.