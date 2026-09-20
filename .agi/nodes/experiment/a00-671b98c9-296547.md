---
id: experiment:a00-671b98c9-296547
mint_id: 74b0c8ebd6fe485fb28e8ce2cce89920
type: experiment
parents:
  - hypothesis:harness-arg-builders-are-templates-only
next_edges: []
confidence: 0.88
edited_by: a00-2ccfbc74
evidence_runs:
  - experiment:a00-671b98c9-296547
line_ceiling: 40
loop: hypothesis:harness-arg-builders-are-templates-only@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe-k2.py: synthetic template dir with BOTH roles flipped (claude-code source=row, copilot-cli source=ladder) + synthetic ladder.md and config rows where ladder/row values DIFFER; call rotate._resolve_seat_role(root, hid, director, None, None, None)", "expected": "each harness resolves from its TEMPLATE-DECLARED source; a hidden harness-name branch would produce the opposite", "observed": "claude-code(source=row) -> CC-ROW/CC-EFF; copilot-cli(source=ladder) -> LADDER-DIR/LADDER-EFFORT (+ ladder settings ultracode). Field decides for model+effort", "result": "HELD"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe-k2.py: template with [roles] source = cosmic; role_source(bogus)", "expected": "a NAMED error, never a silent default to ladder", "observed": "HarnessTemplateError: bogus: unknown roles.source cosmic; known: [ladder, row]", "result": "HELD"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe-k2.py control: REAL templates, same synthetic root; _resolve_seat_role(None and copilot-cli)", "expected": "claude absent -> ladder; copilot -> its own row (the pre-change sources), no byte drift", "observed": "claude(None) -> LADDER-DIR/LADDER-EFFORT; copilot -> COP-ROW/COP-EFF", "result": "HELD"}
production_lines: 74
profile: balanced
role: kid
scaffold_hash: d2d8700e7a7d2d38
season: 2
title: "Seat role resolution is template data: [roles] source, no harness-name branch"
town: core
verdict: inconclusive_lean_proved:88
---
<!-- BODY:BEGIN -->
# experiment:a00-671b98c9-296547
## What I did

Moved the per-harness SEAT role resolution (model / effort / settings) out of
`spawn_window` and into template data — the last harness-NAME branch on the
seat path (`if harness and harness != "claude-code":`, rotate.py@38423879f
L1758) is gone.

- `extensions/agi/templates/harness/claude-code.toml`:
  `[roles] source = "ladder"`.
- `extensions/agi/templates/harness/copilot-cli.toml`:
  `[roles] source = "row"`.
- `harness_template.role_source(id)` — the ONE reader; closed vocabulary
  `ROLE_SOURCES = ("ladder", "row")`, an omitted field defaults to `ladder`
  (claude's behaviour byte-for-byte), an unknown source is a NAMED
  `HarnessTemplateError`.
- `rotate._resolve_seat_role(root, harness, tier, model, effort, settings)`
  dispatches on the declared source: `ladder` -> the existing `load_role`
  (ladder roles table -> `harnesses.claude-code` -> `DEFAULT_CC_ROLES`),
  `row` -> `_harness_row`'s own `models`/`effort`. `spawn_window` calls it for
  every harness; a template error is printed as `ERR:` and returns rc 1.

`DEFAULT_CC_ROLES` deliberately stayed in rotate.py (the brief's optional
half): `test_rotate.py` monkeypatches `load_role`, and moving the constants
would have rippled without adding a falsifiable claim.

## Falsifiers (all four green)

1. grep — 0 hits in the resolution region. One hit remains at L980,
   `_validate_harness`'s fast-accept (`if not harness or harness ==
   "claude-code": return 0, ""`), which is the unknown-harness REFUSAL gate,
   not model/effort/settings resolution. `resolution_region_hits: 0`.
2. Byte identity — 16-case frozen matrix through `spawn_window(..., dry_run=True)`
   (claude-code/copilot-cli × tier director/parent × caller model/effort
   absent/present; ladder rows + config rows; copilot row model != claude's):
   `diff before.json after.json` → `BYTE_IDENTICAL`.
3. Wire flip — copy the template dir, flip copilot's `[roles] source`:
   `ladder` → `--model LADDER-MODEL`, `row` → `--model ROW-MODEL`, rc 0 both,
   `flip_changes_resolved_model: true`. The field decides, not the name.
4. Unknown source — `source = "cosmic"` →
   `"cosmic: unknown roles.source 'cosmic'; known: ['ladder', 'row']"`, never a
   silent default. A synthetic 4th template with `source = "row"` resolves
   `--model ROW4` from its own row with no rotate.py edit.

Probe JSON: `.agi/sessions/iter-DH.03/a00-671b98c9/probe_wire.json`;
matrices `before.json` / `after.json` in the same dir; tests in
`test_harness_template.py` and `test_rotate_copilot_harness.py` (44 + 405
passed across the touched suites; K1's frozen-literal seat tests stay green).

## Evidence

```
$ python3 .agi/sessions/.../frozen_matrix.py > after.json
$ diff before.json after.json && echo BYTE_IDENTICAL
BYTE_IDENTICAL

$ cat probe_wire.json
{"1_grep_resolution_region": {"resolution_region_hits": 0, ...},
 "3_wire_flip": {"copilot_source_ladder_model": "LADDER-MODEL",
                 "copilot_source_row_model": "ROW-MODEL",
                 "flip_changes_resolved_model": true},
 "4_unknown_source_named_error": "cosmic: unknown roles.source 'cosmic'; known: ['ladder', 'row']"}

$ PYTHONPATH=/tmp/pytestenv /tmp/pytestenv/bin/pytest \
    extensions/agi/tests/test_harness_template.py \
    extensions/agi/tests/test_rotate_copilot_harness.py -q
44 passed in 0.87s
$ PYTHONPATH=/tmp/pytestenv /tmp/pytestenv/bin/pytest \
    extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rotate_templates.py \
    extensions/agi/tests/test_harness_dispatch_shapes.py \
    extensions/agi/tests/test_rotate_verb.py extensions/agi/tests/test_rotate_verb_resolvers.py -q
405 passed in 96.53s
```

Production diff: 74 added / 21 deleted across the production paths
(`git diff --numstat`); non-blank non-comment added lines 55. Over the 40
ceiling, under the 80 (2x) stop line — recorded in frontmatter, no re-brief.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2ccfbc74, DH.03 K2). (1) INSTRUCTION: the orders say "move model effort into templates" and the goal invariant says "dispatch.py does not grow harness string branches; it resolves a template (or thin hook) the same way for every harness". (2) MACHINE, read off the diff 38423879f..94f962962: rotate.py had `if harness and harness != "claude-code":` at the seat resolution (old L1758) -- a harness-NAME branch. The kid deleted it and added `_resolve_seat_role`, which reads `harness_template.role_source(hid)`; the field lives in claude-code.toml (source=ladder) and copilot-cli.toml (source=row); harness_template.py:111-122 is the one reader with closed vocabulary ROLE_SOURCES. I ran my own adversarial wire probe (probe-k2.py): I flipped BOTH directions at once (claude declares row, copilot declares ladder) against a synthetic ladder+config whose values differ -- claude resolved CC-ROW/CC-EFF and copilot resolved LADDER-DIR/LADDER-EFFORT, i.e. each followed its declared field; a surviving name branch would have produced the reverse. A synthetic source=cosmic raised a NAMED HarnessTemplateError, never a silent ladder. With the REAL templates the sources are unchanged (claude->ladder, copilot->row). grep: the only remaining `harness == "claude-code"` (L980) is in _validate_harness, the refuse-by-name gate, NOT model/effort resolution. (3) NEAR MISS: the plausible move that satisfies the words and loses the mechanism is an if/else on the harness NAME pushed down into a helper -- the branch survives, the words "resolution moved" are true, and a fourth harness still needs the file edited. My both-directions flip is exactly what distinguishes the helper-branch from template data; a one-direction flip (copilot only) would not, because a hidden name branch still yields copilot its row. (4) DEVIATION: none by the kid. CEILING NOTE: the node frontmatter line_ceiling is 40 (the dispatch slice) while my orders stated <=90 production lines; the kid measured 74 gross and stayed under the ceiling it was actually given, so this is not an overage against the brief -- but the dispatch slice and the parent brief disagreed, and the harvest should read the order, not the stale field. VERDICT kept at inconclusive_lean_proved:88: the source-field claim is proved on the seat path; the parent hypothesis itself is not claimed here.
<!-- THOUGHT:END -->

## Agent Notes
Seat model/effort/settings now resolve from each template's [roles] source (ladder|row); the last harness-name branch is gone, argv byte-identical on a 16-case frozen matrix, wire flip proves the field decides, unknown source is a named error.
