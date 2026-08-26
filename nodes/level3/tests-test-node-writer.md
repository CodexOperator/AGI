---
confidence: 1.0
id: "level3:tests-test-node-writer"
mint_id: b945746941aa41bfa3906cfc91deb511
origin: level3-scan
parents:
  - idea:engine-tests
payload_ref: extensions/agi/tests/test_node_writer.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/tests/test_node_writer.py"
type: level3
---

`extensions/agi/tests/test_node_writer.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-tests`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_node_writer.py
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
- name: subprocess
  how: '`import subprocess` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / writer
  how: '`(BIN / writer).read_text()` at line 107'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / 'dispatch.py'
  how: '`(BIN / ''dispatch.py'').read_text()` at line 121'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / writer
  how: '`(BIN / writer).read_text()` at line 131'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: res.path
  how: '`res.path.read_text()` at line 161'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: res.path
  how: '`res.path.read_text()` at line 187'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(res.path.read_text().split(''---'', 2)[1])` at line 212'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: first.path
  how: '`first.path.read_text()` at line 246'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Path(info['path'])
  how: '`Path(info[''path'']).read_text()` at line 358'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Path(info['path'])
  how: '`Path(info[''path'']).read_text()` at line 388'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project / 'nodes' / 'app_purpose' / 'ap.md'
  how: '`(project / ''nodes'' / ''app_purpose'' / ''ap.md'').read_text()` at line
    408'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads((ad / ''agent.json'').read_text())` at line 410'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: res.path
  how: '`res.path.read_text()` at line 198'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(res.path.read_text().split(''---'', 2)[1])` at line 226'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: first.path
  how: '`first.path.read_text()` at line 241'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: again.path
  how: '`again.path.read_text()` at line 251'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: first.path
  how: '`first.path.read_text()` at line 261'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ad / 'agent.json'
  how: '`(ad / ''agent.json'').read_text()` at line 410'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: first.path
  how: '`first.path.read_text()` at line 257'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: BIN / name
  how: '`(BIN / name).read_text()` at line 315'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: res.path
  how: '`res.path.read_text()` at line 212'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: res.path
  how: '`res.path.read_text()` at line 226'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _load
  how: 'defines private function `_load` at line 31, signature: (name, filename=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: project
  how: 'defines public function `project` at line 71, signature: (tmp_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_every_writer_points_at_the_one_routine_the_same_way
  how: 'defines public function `test_every_writer_points_at_the_one_routine_the_same_way`
    at line 100, signature: (writer)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dispatch_no_longer_touches_the_node_tree_at_all
  how: defines public function `test_dispatch_no_longer_touches_the_node_tree_at_all`
    at line 112
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_no_writer_keeps_its_own_type_table_or_prompts
  how: 'defines public function `test_no_writer_keeps_its_own_type_table_or_prompts`
    at line 129, signature: (writer)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_type_table_is_all_underscores
  how: defines public function `test_the_type_table_is_all_underscores` at line 137
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_every_canonical_type_has_a_body_prompt
  how: defines public function `test_every_canonical_type_has_a_body_prompt` at line
    147
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_hyphenated_input_writes_the_canonical_spelling
  how: 'defines public function `test_hyphenated_input_writes_the_canonical_spelling`
    at line 157, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_an_unaliased_hyphen_still_lands_canonical
  how: defines public function `test_an_unaliased_hyphen_still_lands_canonical` at
    line 167
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_rejection_writes_nothing
  how: 'defines public function `test_rejection_writes_nothing` at line 177, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_approval_writes_a_mint_id_and_no_stamp
  how: 'defines public function `test_approval_writes_a_mint_id_and_no_stamp` at line
    184, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_bypass_is_stamped
  how: 'defines public function `test_bypass_is_stamped` at line 195, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unverified_reason_survives_yaml_round_trip
  how: 'defines public function `test_unverified_reason_survives_yaml_round_trip`
    at line 201, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_frontmatter_is_valid_yaml_for_every_type
  how: 'defines public function `test_frontmatter_is_valid_yaml_for_every_type` at
    line 217, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_skip_never_touches_an_existing_file
  how: 'defines public function `test_skip_never_touches_an_existing_file` at line
    236, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_reuse_scaffold_overwrites_an_untouched_scaffold
  how: 'defines public function `test_reuse_scaffold_overwrites_an_untouched_scaffold`
    at line 244, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_reuse_scaffold_preserves_filled_in_work
  how: 'defines public function `test_reuse_scaffold_preserves_filled_in_work` at
    line 254, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_direct_path_is_found
  how: 'defines public function `test_direct_path_is_found` at line 268, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_descriptive_filename_is_found_by_frontmatter
  how: 'defines public function `test_descriptive_filename_is_found_by_frontmatter`
    at line 273, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_abbreviated_prefix_is_found
  how: 'defines public function `test_abbreviated_prefix_is_found` at line 286, signature:
    (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_unknown_id_is_none_not_a_guess
  how: 'defines public function `test_unknown_id_is_none_not_a_guess` at line 297,
    signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_the_index_cannot_go_stale_under_its_own_writer
  how: 'defines public function `test_the_index_cannot_go_stale_under_its_own_writer`
    at line 303, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_both_readers_are_the_same_function
  how: defines public function `test_both_readers_are_the_same_function` at line 311
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dispatch_picks_a_canonically_spelled_step
  how: 'defines public function `test_dispatch_picks_a_canonically_spelled_step` at
    line 344, signature: (level, target, role, expected)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dispatch_scaffold_is_gated_and_canonical
  how: 'defines public function `test_dispatch_scaffold_is_gated_and_canonical` at
    line 348, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_dispatch_scaffold_declines_an_illegal_spawn
  how: 'defines public function `test_dispatch_scaffold_declines_an_illegal_spawn`
    at line 363, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_big_zoom_scaffold_no_longer_writes_an_illegal_hypothesis
  how: 'defines public function `test_big_zoom_scaffold_no_longer_writes_an_illegal_hypothesis`
    at line 378, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: test_cli_scaffold_still_writes_through_the_shared_routine
  how: 'defines public function `test_cli_scaffold_still_writes_through_the_shared_routine`
    at line 397, signature: (project)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp_path / 'agi-tree.config.json'
  how: '`(tmp_path / ''agi-tree.config.json'').write_text(''{}'')` at line 73'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sd / '[shape].md'
  how: '`(sd / ''[shape].md'').write_text(SHAPE)` at line 76'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: first.path
  how: '`first.path.write_text(''---\nid: verdict:keep\n---\n\nREAL WORK\n'')` at
    line 238'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: first.path
  how: '`first.path.write_text(first.path.read_text() + ''\nAn agent actually wrote
    this.\n'')` at line 256'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / 't-001-some-description.md'
  how: '`(d / ''t-001-some-description.md'').write_text(''---\nid: task:thing\ntype:
    task\n---\n\nbody\n'')` at line 281'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / 'abbrev.md'
  how: '`(d / ''abbrev.md'').write_text(''---\nid: exp:abbrev\ntype: experiment\n---\n\nb\n'')`
    at line 293'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ad / 'agent.json'
  how: '`(ad / ''agent.json'').write_text(json.dumps({''id'': ''a1'', ''status'':
    ''run''}))` at line 400'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sd / fname
  how: '`(sd / fname).write_text(f''---\nname: {name}\nspawn:\n  {spawn}\n---\n{name}\n'')`
    at line 79'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / f'{slug}.md'
  how: '`(d / f''{slug}.md'').write_text(f''---\nid: {ntype}:{slug}\ntype: {ntype}\n---\n\nbody\n'')`
    at line 86'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: d / 'x.md'
  how: '`(d / ''x.md'').write_text(''---\nid: exp:x\ntype: experiment\n---\n\nb\n'')`
    at line 322'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({''id'': ''a1'', ''status'': ''run''})` at line 400'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
