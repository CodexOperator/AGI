---
id: experiment:a00-fd36a5c0-72411c
mint_id: 1a9747c6070d4e4cbe7f862b40376abe
type: experiment
parents:
  - hypothesis:harness-arg-builders-are-templates-only
next_edges: []
confidence: 0.95
edited_by: a00-5077faa0
evidence_runs:
  - experiment:a00-fd36a5c0-72411c
line_ceiling: 40
loop: hypothesis:harness-arg-builders-are-templates-only@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe q1: monkeypatched template_dir with top-level argv as str xyz, int 3, and inline table {slot=prompt}; call harness_template.load", "expected": "each non-list argv raises a NAMED HarnessTemplateError, never a silent accept or TypeError", "observed": "all three raised HarnessTemplateError: argv is not a list (got str/int/dict) naming the file and type", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe q1: monkeypatched template_dir with top-level shapes as str x, int 5, list []; call load", "expected": "each non-table shapes raises a NAMED HarnessTemplateError, never AttributeError items", "observed": "all three raised HarnessTemplateError: shapes is not a table (got str/int/list)", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe q1: [shapes] d = x (a shape value that is not a table); call load", "expected": "named HarnessTemplateError, the pre-existing per-shape check must survive", "observed": "HarnessTemplateError: shape d is not a table", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "parent probe q1: [shapes.d] argv as an inline table {a=b} and as str xy; call load", "expected": "each non-list shape argv raises a NAMED HarnessTemplateError, never iterating a dict as keys or a str as chars", "observed": "both raised HarnessTemplateError: shapes.d.argv is not a list (got dict/str)", "result": "held"}
  - {"conjunct": 5, "class": "wire", "cmd": "parent probe q2: rotate.spawn_window(dry_run=True, harness=shapesbad) against a tmp graph root declaring shapesbad, template shapes = x, template_dir patched on BOTH rotate.harness_template and agi.bin.harness_template; plus the three shipped templates loaded and render(claude-code, shape=dispatch) re-read", "expected": "the live seat call site reaches the changed load() bytes and refuses by name with no AttributeError; shipped templates and the dispatch render are unregressed", "observed": "rc=1, shell=empty, stderr ERR: harness template shapesbad is malformed ... HarnessTemplateError: shapes is not a table; and shipped claude-code/copilot-cli/pi load with claude-code dispatch render byte-identical", "result": "held"}
production_lines: 18
profile: balanced
role: kid
scaffold_hash: e98d6c3ff53b788a
season: 2
title: Non-table argv and shapes containers refused by name in load()
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# Failing closed by name for every container `load()` reads

## Experiment

Built on round 1's `roles` guard: made `harness_template.load()` refuse, BY
NAME, each container it reads. Pre-fix, the parent's four reproductions held.
Probe: `.agi/sessions/iter-DH.05/a00-fd36a5c0/probe_prefix.py`, importing
`agi.bin.harness_template` with `template_dir` monkeypatched to a tmp dir:

    argv = "xyz"              -> ACCEPTED, argv='xyz' (walked char by char)
    argv = 3                  -> TypeError 'int' object is not iterable
    shapes = "x"              -> AttributeError 'str' object has no attribute 'items'
    [shapes.d] argv = {a="b"} -> ACCEPTED, dict iterated as keys

Fix in `extensions/agi/bin/harness_template.py` `load()`: guard top-level
`argv` (must be a list), top-level `shapes` (must be a table), keep the
existing `shapes.<name>` table check, and guard every `shapes.<name>.argv`
(must be a list). `roles` untouched from round 1. Post-fix, all four yield a
named `HarnessTemplateError` naming the file and the offending type:

    argv_str:  HarnessTemplateError: .../x.toml: argv is not a list (got str: 'xyz'); write argv = [ ... ]
    argv_int:  HarnessTemplateError: .../x.toml: argv is not a list (got int: 3); write argv = [ ... ]
    shapes_str: HarnessTemplateError: .../x.toml: shapes is not a table (got str: 'x'); write [shapes.<name>]
    shape_argv_dict: HarnessTemplateError: .../x.toml: shapes.d.argv is not a list (got dict: {'a': 'b'})

No `AttributeError` and no `TypeError` escapes the seat path's `except
HarnessTemplateError` catch any more, and no non-list is silently accepted.

## Evidence

- Three regression tests added to `extensions/agi/tests/test_harness_template.py`,
  each parametrized over a string / number / inline table:
  `test_non_list_argv_is_a_named_error`,
  `test_non_table_shapes_is_a_named_error`,
  `test_non_list_shape_argv_is_a_named_error`. Each writes a tmp template with
  `template_dir` monkeypatched and asserts `HarnessTemplateError`.
- Production diff (`git diff --numstat -- extensions/agi/bin/harness_template.py`):
  18 added, 3 removed — under the 40-line ceiling.
- `PYTHONPATH=/tmp/pt python3 -m pytest extensions/agi/tests/test_harness_template.py
  extensions/agi/tests/test_harness_dispatch_shapes.py
  extensions/agi/tests/test_rotate_copilot_harness.py -q` -> **71 passed**.
- Zero `dispatch.py` edits; the `roles` behavior from round 1 untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-5077faa0 (DH.05, round 2). Accepted: the container-validation class is now closed in load().

(1) The instruction said (round 2 brief, carried from the round-1 dispatch order): make load() fail CLOSED BY NAME for every template container it reads -- non-list argv, non-table shapes, non-table shapes.<name>, non-list shapes.<name>.argv -- a named HarnessTemplateError in every case, never AttributeError/TypeError/silent accept.

(2) What the machine does, read off the built file and run: harness_template.py:88-112 now guards top-level argv (isinstance list), roles (round 1), the shapes container (isinstance dict), each shape value, and each shape argv, each raising HarnessTemplateError with file, type and value. The parent's independent probes: 3 argv shapes, 3 shapes shapes, 1 per-shape value, 2 shape-argv shapes -- 9 malformed templates, all named, zero AttributeError/TypeError; 3 healthy controls accepted; shipped claude-code/copilot-cli/pi load and render(claude-code, shape=dispatch) is byte-identical; the live seat call site refuses a config-declared shapes = x harness with rc=1, empty command and a HarnessTemplateError on stderr. dispatch.py mtime 08:20:07, unchanged.

(3) Near miss: a guard only on the string case (the literal pre-fix example) would satisfy the words and still let argv = 3 raise TypeError and argv = {slot=prompt} be iterated as keys into a garbage argv; the probe enumerated int/dict/list, not just str. A guard in render() rather than load() would leave load_all() (which catches every exception and names a broken file) reporting the wrong type name; load() is the one gate every reader passes, which is why the fix is there.

(4) No deviation from a standing rule: no dispatch.py edit, no rotate.py edit, roles from round 1 untouched.
<!-- THOUGHT:END -->

## Agent Notes
load() now fails closed by name for non-table top-level argv and shapes and for non-list argv at each level; parent's four reproductions all yield HarnessTemplateError, 71 tests green, 18 production lines

parent review DH.05 round 2: 9 malformed-container probes + 3 healthy controls + a live seat-path wire probe all held; 71 tests green; 18 production lines; dispatch.py untouched
