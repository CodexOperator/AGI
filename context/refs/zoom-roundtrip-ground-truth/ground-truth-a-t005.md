# Ground truth claim list — Subject A: task:t-005

Source: `nodes/task/t-005-procedural-dungeon-gen-rooms.md` (full file, frontmatter + body).
Built by the opus orchestrator BEFORE any decomposition ran. Not shown to any haiku agent.

Categories: DESC = description, INV = invariant citation, DEP = dependency,
PATH = file path, ACC = acceptance criterion.

| id | cat | atomic claim |
|----|-----|--------------|
| A-D1 | DESC | The generator is seeded (takes a seed as input) |
| A-D2 | DESC | It produces rooms |
| A-D3 | DESC | It produces corridors that connect the rooms |
| A-D4 | DESC | Output is rendered as floor/wall meshes |
| A-D5 | DESC | Generation is deterministic per seed |
| A-D6 | DESC | The task identifier is T-005 / task:t-005 |
| A-D7 | DESC | Effort is L |
| A-D8 | DESC | Tier is 0 |
| A-D9 | DESC | Status is pending |
| A-D10 | DESC | Origin is build-site |
| A-P1 | DEP | blocked_by is empty — the task declares no blocking dependencies |
| A-F1 | PATH | Code lives under `src/dungeon/` |
| A-A1 | ACC | Same seed run twice must yield an identical layout |
| A-A2 | ACC | Verification includes eyeballing the result in a browser |

Totals: DESC 10, INV 0 (subject cites no invariants), DEP 1, PATH 1, ACC 2. n = 14.

Note recorded up front: subject A is category-degenerate. INV n=0 and DEP n=1 mean
per-category comparison for this subject is weak; pooled numbers across both subjects
are the meaningful figure. A-P1 is an absence-claim ("declares no blockers") and is
recorded as such — it is the hardest possible kind of claim to survive a round trip.

## Scoring rule (fixed before seeing any output)

A claim counts as RECOVERED if the reconstruction asserts it explicitly or in an
unambiguous paraphrase. Partial/vague gestures (e.g. "has metadata", "lives in the
source tree") do NOT count. A path counts only if the actual path string is present.
An invariant citation counts only if the identifier (e.g. §V4) is present; restating
the rule without the id counts as a DESC-level recovery, not an INV recovery — this
is scored separately as "content-without-citation".
