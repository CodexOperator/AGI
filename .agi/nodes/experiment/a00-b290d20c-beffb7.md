---
id: experiment:a00-b290d20c-beffb7
mint_id: 62f25064157f4f39ab84fffcae5e5295
type: experiment
parents:
  - hypothesis:rolslice-role-sections-survive-a-heading-rename
next_edges: []
confidence: 0.9
edited_by: a00-6a6f912b
evidence_runs:
  - experiment:a00-b290d20c-beffb7
loop: hypothesis:rolslice-role-sections-survive-a-heading-rename@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 47
profile: balanced
role: kid
scaffold_hash: 1b723d3fed05f8d9
season: 2
title: rolslice resolves role sections from a goal-id-free stable key
town: core
verdict: proved
---
# experiment:a00-b290d20c-beffb7

## Experiment

Built the rolslice stable-key fix under
`hypothesis:rolslice-role-sections-survive-a-heading-rename`.

**Pre-fix (measured by parent, reproduced here):**
`python3 -m pytest extensions/agi/tests/test_rolslice.py -q` -> 4 failed, 1 passed.
`build_slice` raised
`ValueError: rolslice: section(s) not found in SKILL.md: ['Every node edit goes through \`write.py\` (\`goal:g13.1\`)']`
at `rolslice.py:161`, because `ROLE_SECTIONS` held a second full-text literal of
the SKILL.md heading while `skills/agi/SKILL.md:272` already read
`(\`goal:g4.19\`)` after the Prime's goal-id sweep.

**Fix (`extensions/agi/bin/rolslice.py`):**

| change | effect |
|---|---|
| added `stable_key(heading)` + `_GOAL_ID_RE` | strips a trailing parenthesised goal id once |
| `ROLE_SECTIONS` / `CORE` keys | now carry the heading text WITHOUT the id |
| `build_slice` | builds `by_key` via `stable_key` and matches `want` on it; document order unchanged; `missing` ValueError kept |
| body selection | iterates sections, matching `stable_key(heading)` |

No second full-text literal of a SKILL.md heading remains (grep for `goal:g`
finds only the docstring/comment that explains the sweep and the regex).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rolslice.py extensions/agi/tests/test_rolslice_rename.py -q
9 passed in 0.14s

$ python3 -m pytest extensions/agi/tests/test_rolslice*.py extensions/agi/tests/test_brief*.py -q
1 failed, 192 passed
  FAILED extensions/agi/tests/test_brief.py::test_g15_rule_with_no_project_root_keeps_the_current_fallback
  (KNOWN red, core R3, not this round)

$ git diff --numstat -- extensions/agi/bin/rolslice.py
36	11	extensions/agi/bin/rolslice.py      (production_lines = 47)
```

**New test** `extensions/agi/tests/test_rolslice_rename.py`: builds a small
fixture SKILL.md from the map's own keys, renames every heading's paren id to
`(goal:g4.19)`, and asserts `build_slice` still finds the section for kid,
parent and director; a second test asserts a genuinely deleted heading still
raises ValueError. RED on pre-fix bytes: the fixture heading
`... (\`goal:g4.19\`)` could not match the pre-fix literal
`... (\`goal:g13.1\`)`, so `build_slice` raised — the same failure the parent
measured on the real SKILL.md. Existing `test_rolslice.py` (the 4 reds) is green.

## Agent Notes
rolslice.py now keys role sections on stable_key(heading) (heading text minus trailing goal id) for both the map and the actual headings; no second full-text literal remains; test_rolslice_rename.py renames a fixture heading's goal id and still finds the section, existing test_rolslice.py 4 reds now green

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by parent a00-6a6f912b (EF.47), accepted with one caveat.

Diff read (not the result file): extensions/agi/bin/rolslice.py 36+/11-, new extensions/agi/tests/test_rolslice_rename.py 66 lines. The fix adds stable_key() (re \s*\(`?goal:[^)`]+`?\)\s*$) and applies it to BOTH the map keys and the actual `## ` headings; ROLE_SECTIONS/CORE keys no longer carry a goal id; the loud missing-ValueError stays.

Parent-run negative probes (one per claim conjunct, on real bytes):
  P1 class=wire conjunct=1 -- all CORE/ROLE_SECTIONS keys pass stable_key unchanged; the only goal-id strings left in rolslice.py are the docstring/comment explaining the sweep and the regex -> HELD.
  P2 class=gate conjunct=2 -- copy the REAL skills/agi/SKILL.md, rename the write.py heading id g4.19 -> g77.77; build_slice for kid/parent/director still carries 'Every node edit goes through `write.py`' -> HELD.
  P3 class=gate conjunct=3 -- load the PRE-FIX rolslice (git show adab78a2d9:extensions/agi/bin/rolslice.py) and run it on the kid's own fixture (id-free keys, headings id g4.19): raises ValueError for kid/parent/director -> the committed test IS red on the pre-fix bytes -> HELD.
Tests after the change: test_rolslice*.py + test_brief*.py = 192 passed, 1 failed (test_brief.py::test_g15_rule_with_no_project_root_keeps_the_current_fallback = the KNOWN core R3 red, not this round).

CAVEAT (why the verdict still stands): P3's red is BROADER than the target bug -- the fixture appends a goal id to EVERY heading, including CORE headings the pre-fix map never carried an id for, so pre-fix already fails on 'CLI' before reaching the write.py literal. P2 on the real SKILL.md isolates the actual claim (only the write.py id renamed) and holds, so the proof is real; a tighter fixture would id only the write.py heading.
WIRE CAVEAT (not a defect of this node): a repo-wide grep finds NO consumer of rolslice.build_slice outside its own tests and CLI -- the slicing mechanism is not yet wired into brief assembly, so this fix is correct but currently unexercised by the loop.
<!-- THOUGHT:END -->
