---
id: experiment:a00-867f6014-318470
mint_id: 5fdf1c9ff11a4e0e82686da931564e9b
type: experiment
parents:
  - hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell
next_edges: []
confidence: 0.98
edited_by: a00-a4efedba
evidence_runs:
  - experiment:a00-867f6014-318470
loop: hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell@s2
model: stealth/space-bunny-alpha
probes: "\"P1 gate: parent real_cell_gate_probe.py ran the real authority fixture and real loader. Malformed frontmatter returned 'authority: HELD -- veto cell is unreadable' and kept origin/season2/main at 8c34289a; deleting the same cell returned the named missing-cell HELD line and kept the ref at 8c34289a.\""
production_lines: 34
profile: balanced
role: kid
scaffold_hash: 34a9568bb4042609
season: 2
title: Strict veto reads hold authority publish
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-867f6014-318470

## Experiment

Implemented the real fail-closed boundary rather than mocking `is_frozen`:
`seatsig.veto.read(..., strict=True)` now raises `VetoCellUnreadable` for a
missing cell, a loader/encoding failure, or either list-valued cell having the
wrong type. The authority-publish seam performs this strict read before asking
whether Prime is frozen, then reuses that one state object. Its existing
`except Exception` therefore returns the named
`authority: HELD -- veto cell is unreadable (...)` refusal before resolving or
moving the authority ref.

The non-strict reader remains fail-open for the other existing veto seams, so
this small change does not silently redefine their compatibility contract.

The real authority fixture now writes a readable veto cell by default. A
parametrized regression test deletes that cell and, in the other case, replaces
it with invalid non-UTF-8 bytes; each case requires the named HELD line and
asserts `origin/season2/main` is byte-for-byte the same ref.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py extensions/agi/tests/test_veto.py -q`
  -> `41 passed, 2 warnings`.
- Malformed-cell result includes the concrete loader cause:
  `authority: HELD -- veto cell is unreadable (unreadable veto cell ...: 'utf-8' codec can't decode byte 0xff ...)`.
- `git diff --numstat -- extensions/agi/src/seatsig/veto.py extensions/agi/bin/rotate.py`
  -> `2/1` and `22/9`, 34 changed production lines (under the 40-line ceiling).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Parent review accepts this child. The instruction said, 'an unreadable or missing veto cell stops the publish, refused by name, instead of proceeding; a committed test.' The machine now does that at extensions/agi/bin/rotate.py:10427-10434 by calling seatsig.veto.read(..., strict=True) before authority lookup; extensions/agi/src/seatsig/veto.py:108-152 raises VetoCellUnreadable for absent, loader-failed, or wrong-type state, and the parent-built real-cell probe observed the named HELD line with the authority SHA unchanged in both required states. The near miss is the first child's catch around is_frozen: a mocked reader exception is refused while the real loader converts malformed and missing cells to defaults, satisfying the words around the call but not the gate's actual inputs. This review does not deviate from the normal parent rule: the child supplied a real title, a valid parent, a typed proved verdict, self evidence, and named production/test bytes, and the parent's independent gate probe passed."
<!-- THOUGHT:END -->

## Agent Notes
Strict real-cell reads now name-refuse missing or malformed veto state and leave the authority ref unchanged; 41 targeted tests pass.
