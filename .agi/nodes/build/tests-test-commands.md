---
build_kind: code
confidence: 1.0
id: "build:tests-test-commands"
mint_id: 08d01f7eca254a63aee232b71eba5462
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_commands.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_commands.py"
type: build
---

`extensions/agi/tests/test_commands.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_commands.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 15'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 17'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.machinery
  how: '`import importlib.machinery` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: commands
  how: '`import commands` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / ".geometry" / "commands.md"
  how: '`(project / "nodes" / ".geometry" / "commands.md").read_text()` at line 94'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: script
  how: '`script.read_text()` at line 196'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: project
  how: 'defines public function `project` at line 69, signature: (tmp_path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_commands_resolve_from_the_node
  how: 'defines public function `test_commands_resolve_from_the_node` at line 77,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_command_with_no_argv_list_is_skipped_not_half_resolved
  how: 'defines public function `test_a_command_with_no_argv_list_is_skipped_not_half_resolved`
    at line 83, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_placeholders_are_substituted_so_the_node_holds_no_absolute_paths
  how: 'defines public function `test_placeholders_are_substituted_so_the_node_holds_no_absolute_paths`
    at line 89, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_argv_is_a_list_so_nothing_is_reparsed_by_a_shell
  how: 'defines public function `test_argv_is_a_list_so_nothing_is_reparsed_by_a_shell`
    at line 100, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_unknown_command_names_what_is_available
  how: 'defines public function `test_an_unknown_command_names_what_is_available`
    at line 112, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_absent_node_is_a_supported_state
  how: 'defines public function `test_absent_node_is_a_supported_state` at line 119,
    signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_node_that_exists_but_cannot_be_read_says_so
  how: 'defines public function `test_a_node_that_exists_but_cannot_be_read_says_so`
    at line 126, signature: (project, capsys)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_only_a_declared_ordered_workflow_is_rendered_as_a_sequence
  how: 'defines public function `test_only_a_declared_ordered_workflow_is_rendered_as_a_sequence`
    at line 139, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_injected_lines_carry_the_runnable_command
  how: 'defines public function `test_the_injected_lines_carry_the_runnable_command`
    at line 149, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_render_table_preserves_placeholders
  how: 'defines public function `test_render_table_preserves_placeholders` at line
    155, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_every_declared_command_points_at_something_that_exists
  how: defines public function `test_every_declared_command_points_at_something_that_exists`
    at line 175
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _declared_subcommands
  how: 'defines private function `_declared_subcommands` at line 186, signature: (script:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_every_declared_command_accepts_its_own_subcommand
  how: defines public function `test_every_declared_command_accepts_its_own_subcommand`
    at line 218
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_declaration_stays_small
  how: defines public function `test_the_declaration_stays_small` at line 272
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _agi
  how: 'defines private function `_agi` at line 290, signature: (*args, cwd=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_a_bare_first_word_runs_a_declared_command
  how: defines public function `test_a_bare_first_word_runs_a_declared_command` at
    line 298
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_flags_still_reach_the_driver_untouched
  how: defines public function `test_flags_still_reach_the_driver_untouched` at line
    311
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_unknown_verb_names_what_is_declared_and_points_at_the_node
  how: defines public function `test_an_unknown_verb_names_what_is_declared_and_points_at_the_node`
    at line 320
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_pass_through_flags_reach_the_command_not_the_router
  how: defines public function `test_pass_through_flags_reach_the_command_not_the_router`
    at line 330
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_view_commands_are_declared_in_the_graph
  how: defines public function `test_the_view_commands_are_declared_in_the_graph`
    at line 342
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "config.json"
  how: '`(graph / "config.json").write_text("{}")` at line 72'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: graph / "nodes" / ".geometry" / "commands.md"
  how: '`(graph / "nodes" / ".geometry" / "commands.md").write_text(NODE)` at line
    73'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / "nodes" / ".geometry" / "commands.md"
  how: '`(project / "nodes" / ".geometry" / "commands.md").write_text( "---\nnot:
    [valid\n---\nbody\n")` at line 129'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
