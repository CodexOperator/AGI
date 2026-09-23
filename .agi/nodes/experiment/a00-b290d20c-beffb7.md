---
id: experiment:a00-b290d20c-beffb7
mint_id: 62f25064157f4f39ab84fffcae5e5295
type: experiment
parents:
  - hypothesis:rolslice-role-sections-survive-a-heading-rename
next_edges: []
confidence: 0.9
edited_by: a00-b290d20c
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
