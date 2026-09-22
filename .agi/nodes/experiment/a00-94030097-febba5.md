---
id: experiment:a00-94030097-febba5
mint_id: 9fcde5bdb5e14de8b7eba7be6e0782b7
type: experiment
parents:
  - hypothesis:harness-arg-builders-are-templates-only
next_edges: []
confidence: 0.9
edited_by: a00-5077faa0
evidence_runs:
  - experiment:a00-94030097-febba5
line_ceiling: 40
loop: hypothesis:harness-arg-builders-are-templates-only@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe p1: template_dir monkeypatched to tmp files whose top-level roles is a non-table in five shapes -- str ladder, int 7, list [ladder], bool false, empty str; call harness_template.load AND harness_template.role_source on each", "expected": "every non-table roles node raises a NAMED HarnessTemplateError, never a bare AttributeError", "observed": "all five shapes raised HarnessTemplateError naming the file, the python type and the value, from BOTH load and role_source", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe p1 controls: a [roles] source = row table, and a template with roles OMITTED entirely; call load and role_source", "expected": "row resolves to row and the omitted node resolves to ladder; the new guard must not break the healthy paths", "observed": "both load and role_source returned OK; role_source returned row for the table and ladder for the omitted template", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "parent probe p3: rotate.spawn_window(dry_run=True, harness=nontable) against a tmp graph root whose config.json declares nontable, with a tmp template roles = ladder; template_dir patched on BOTH rotate.harness_template and agi.bin.harness_template so the changed bytes are the ones on the live path", "expected": "the live seat call site reaches the changed load() bytes and refuses by name: rc != 0, empty command, a HarnessTemplateError line on stderr, no AttributeError anywhere", "observed": "rc=1, shell=empty, stderr ERR: harness template nontable is malformed, excluded from the seat set: HarnessTemplateError: <path>: roles is not a table (got str: ladder) -- refused by name at _validate_harness/load_all, ahead of _resolve_seat_role", "result": "held"}
production_lines: 9
profile: balanced
role: kid
scaffold_hash: f9352f11456d3106
season: 2
title: Roles as a non-table is a named refusal, not an AttributeError
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# Roles as a non-table is a NAMED refusal, not an AttributeError

## Experiment

Fix-only round under hypothesis:harness-arg-builders-are-templates-only.
The parent's pre-fix reproduction (experiment:a00-671b98c9-296547) covered
`[roles] source = "cosmic"` but missed `roles` ITSELF being a non-table:
with `roles = "ladder"` at top level, `load()` accepted it and
`role_source()` did `roles.get(...)` on a string, raising a bare
`AttributeError` that escaped the seat path's `except HarnessTemplateError`.
Reproduced in this checkout before any edit:

```
load ok: {'id': 'bad', 'bin': 'b', 'roles': 'ladder'}
role_source raised AttributeError 'str' object has no attribute 'get'
```

### Built (not just measured)

1. `harness_template.load()` now validates the `roles` node shape: a present
   `roles` that is not a dict raises `HarnessTemplateError` naming the file,
   the offending type and value — the same discipline `_check_parts` applies
   to `argv` and `shapes`.
2. `harness_template.role_source()` fails closed by name too: an
   `isinstance(roles, dict)` guard before `.get`, so a caller that bypasses
   `load`'s validation still gets `HarnessTemplateError`, never
   `AttributeError`.
3. No `rotate.py` edit was needed — the existing catch at rotate.py:1806
   (`except harness_template.HarnessTemplateError`) now turns the template
   into `return 1, ""` with `ERR: ...` on stderr. Zero `dispatch.py` edits.

### Regression tests added

- `test_harness_template.py::test_non_table_roles_is_a_named_error` —
  `load("bad")` AND `role_source("bad")` both raise
  `HarnessTemplateError`, neither `AttributeError`.
- `test_rotate_copilot_harness.py::test_non_table_roles_refuses_the_seat_by_name_not_a_crash`
  — the seat path returns `rc != 0`, `shell == ""`, `roles is not a table`
  on stderr.

Healthy controls held: `[roles] source = "ladder"` and `"row"` tables, and
`roles` OMITTED (pi) still resolves to `"ladder"`.

## Evidence

Post-fix probe on the built bytes:

```
load(bad) -> HarnessTemplateError .../bad.toml: roles is not a table (got str: 'ladder'); write [roles] source = ...
role_source(bad) -> HarnessTemplateError .../bad.toml: roles is not a table (got str: 'ladder'); write [roles] source = ...
control plain (roles omitted): ladder
control row  ([roles] source=row): row
```

Test gate:

```
$ PYTHONPATH=/tmp/pt python3 -m pytest \
    extensions/agi/tests/test_harness_template.py \
    extensions/agi/tests/test_harness_dispatch_shapes.py \
    extensions/agi/tests/test_rotate_copilot_harness.py -q
64 passed in 3.70s
```

Production diff: `git diff --numstat -- extensions/agi/bin/harness_template.py`
-> `9  0` (9 added lines, ceiling 40). Tests excluded from that count.

## Agent Notes
roles as a non-table now raises named HarnessTemplateError in load() and role_source(); seat path refuses by name (rc!=0, empty cmd, ERR on stderr); 64 tests green, 9 production lines

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-5077faa0 (DH.05). Accepted: the corrective claim is carried by the bytes.

(1) The instruction said: "non-table `roles` in a harness template must raise named HarnessTemplateError (not AttributeError) from role_source/load validation (harness_template.py:138-139 + rotate.py:1806 catch). Add regression test covering roles as a non-table string."

(2) What the machine does, read off the built file: load() now refuses `roles is not None and not isinstance(roles, dict)` with HarnessTemplateError (harness_template.py:91-95), and role_source() repeats the isinstance guard before `.get("source")` (harness_template.py:143-147). Both regression tests exist and the parent ran three independent probes: five non-table shapes (str/int/list/bool/empty) are refused by name from BOTH readers, the row/omitted controls still resolve, and the live seat call site (rotate.spawn_window, dry_run, a config-declared non-table harness) returns rc=1 with an empty command and a HarnessTemplateError line on stderr. dispatch.py mtime is 08:20:07, unchanged by the round.

(3) Near miss: a guard only in role_source() would satisfy the words and still let load() hand a non-table `roles` to every other reader; the kid put it in both, and I measured both. A guard only on str would pass the dispatch order's literal example and miss list/int/bool; the probe enumerated them.

(4) Residual, NOT a falsifier of this claim: `load()` still reads the `shapes` CONTAINER unguarded -- `(data.get("shapes") or {}).items()` raises AttributeError: 'str' object has no attribute 'items' for a template with `shapes = "x"`. That is the same failure class one key over, outside the roles conjunct this round owns; it is carried forward as kid 2's brief, not left to ride.
<!-- THOUGHT:END -->

parent review DH.05 round 1: ACCEPTED; three independent probes held (five non-table roles shapes, row/omitted controls, live seat-path refusal by name); residual shapes container carried to experiment:a00-fd36a5c0-72411c and closed there
