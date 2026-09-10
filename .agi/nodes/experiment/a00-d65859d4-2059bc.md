---
id: experiment:a00-d65859d4-2059bc
mint_id: 93653001b1b9491ab9b4c9ede82cedec
type: experiment
parents:
  - hypothesis:l4-the-mode-is-declared-not-remembered
next_edges: []
confidence: 0.72
edited_by: a00-745e8b48
evidence_runs:
  - experiment:a00-d65859d4-2059bc
loop: hypothesis:l4-the-mode-is-declared-not-remembered@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6ae41a3b2c5da995
season: 2
title: The operating mode is declared in config and rendered into every brief
verdict: inconclusive_lean_proved:72
---
<!-- BODY:BEGIN -->
# experiment:a00-d65859d4-2059bc

## Experiment

Implemented the hypothesis: the operating arrangement is DECLARED in
`.agi/config.json` and RENDERED into every brief, no longer remembered in
prose by whatever prompt assembled it.

1. **Config declaration** — added top-level `operating_modes` (the three
   arrangements, each with its name, seats, models where the owner named
   them, and a source citation) plus `active_operating_mode`. The live
   declaration marks `enhanced_survival` IN FORCE (it is the unnamed third
   arrangement that is actually running — Prime + point director + helper,
   per `goal:g17.1`, owner verbatim at :26/:28).
2. **Rendering in `brief.py`** — added `_operating_mode_block(project_root)`
   which reads the declaration and renders an `OPERATING MODE` block (marker,
   ACTIVE, SEATS, MODELS, SOURCE). Absent / unreadable / undeclared-active
   config returns `""` and raises nothing (fail-open: an undeclared project
   is byte-unchanged). Added `_prepend_head` as the single choke point that
   inserts the constitution head then the mode block into EVERY `assemble()`
   branch (kid, parent, director, prime_director, advisor, liaison,
   survival/ultimate_survival) — the 7 returns now route through it, no
   second copy of the prose in code.
3. **Tests** — added 4 to `test_brief.py` (`json` import added): fixture
   renders the ACTIVE declaration; **flipping `active_operating_mode` in the
   same fixture config changes the render** (the one that proves it is read,
   not hardcoded); absent declaration renders `` and raises nothing; the
   live assembled brief for every tier carries `OPERATING MODE` +
   `enhanced survival`. No existing test was edited.
4. **Gates** — `test_brief.py` + `test_dispatch.py` GREEN, 195 passed.

CONSTRAINT NOTE on requirement (g) `commands.py run verify`: NOT run by this
kid. `commands.py` resolves `verify` to `verification.py` running the
workflow `smoke -> tests -> goals-check -> viewport-verify -> grid-commit`;
`tests` is the FULL pytest suite and `grid-commit` is `grid.py commit --all`
— the harness rules forbid a kid to run the full suite's OOM exposure and
forbid grid.py/git entirely (`cli.py done` is the only command a kid runs;
a grid-commit would sweep other agents' uncommitted work). The verify
workflow is the director's merge-up gate. The two test files this round
actually changed are green, which is the check that belongs to the work.

## Evidence

`python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_dispatch.py -q`
→ `195 passed in 9.86s` (192 pre-existing + 3 new mode tests; the 4th new
test, the live-brief carry, is in the same 195).

Live config still declares enhanced survival in force (requirement e):

```json
"active_operating_mode": "enhanced_survival",
"operating_modes": { "survival": {…, "in_force": false},
  "ultimate_survival": {…, "in_force": false},
  "enhanced_survival": {…, "in_force": true} }
```

Rendered block (`brief.assemble(tier="kid")`):

```
─── OPERATING MODE (declared in .agi/config.json) ───
ACTIVE: enhanced survival
SEATS: Prime + point director (sanctuary-director) + helper director
       (sanctuary-helper) — the Texas two-step formation, three seats…
MODELS: Prime claude-opus-5; point director claude-opus-5 max; helper
        director claude-sonnet-5 max (owner verbatim…)
SOURCE: goal:g17.1:26 (…) and :28 (…)
```

Sources used, verbatim from the owner: `doc:l4-owner-decisions:265`
("only two persistent seats active each helping the other to conserve the
resource that matters most"; "They can drop down to ultimate survival where
Prime is powered by opus and single remaining director runs off sonnet or
even openrouter") and `:311`; `goal:g17.1:26` ("spawn a second director kid…
Let the current director take point though and the other one is like a
helper… Helper director kid runs sonnet btw.") and `:28`.

## Agent Notes
Declared three operating arrangements (survival/ultimate_survival/enhanced_survival) in .agi/config.json, rendered the active one into every brief via brief.py _prepend_head (single choke point, no duplicated prose), flip-of-active-in-fixture test proves it is read not hardcoded, absent renders empty no raise. test_brief+test_dispatch 195 green. verify workflow g (includes grid-commit+full suite) not run as a kid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-745e8b48, L4.83): accepted as-is. Verified against the working tree, not the report: .agi/config.json declares all three arrangements each with seats/models/source, enhanced_survival in_force=true (survival + ultimate_survival false) — nothing invented, nothing folded; brief.py routes every assemble() return through _prepend_head -> _operating_mode_block, so the prose lives in config and code holds none; test_brief.py diff is import json + 4 new tests, no existing test edited; pytest test_brief+test_dispatch re-run by parent: 195 passed. Requirement (c) the flip-in-fixture test is present and asserts the strong fact (render changes with the declaration, both directions). Requirement (g) commands.py run verify remains the director merge-up gate — kid refusal to run it (grid-commit inside) is correct, not a gap in the node. Verdict inconclusive_lean_proved:72 stands: the only thing between this and proved is the full merge-up verify on the merged tree.
<!-- THOUGHT:END -->

Review accepted: mode declared in config + rendered in brief, flip-test proves read-not-hardcoded, 195 green, no test edited, verify gate deferred to director merge-up.
