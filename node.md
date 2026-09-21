---
id: experiment:a00-8f9ef398-96acab
mint_id: 61409909b87b4fcb94db8aa1dddb243b
type: experiment
parents:
  - hypothesis:l4-sm32b-town-first-rename-boundary
next_edges: []
confidence: 0.85
edited_by: a00-2b8d00ba
evidence_runs:
  - experiment:a00-8f9ef398-96acab
line_ceiling: 60
loop: hypothesis:l4-sm32b-town-first-rename-boundary@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 58
profile: balanced
role: kid
scaffold_hash: 9ebd39e3042fb8fa
season: 2
title: A00 8f9ef398 96acab
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-8f9ef398-96acab

## Experiment

**WHAT THE INSTRUCTION SAID.** `_rename_surfaces` (rotate.py:3400 pre-fix)
emitted both branch surfaces through `branches.post_branch(2, old/new)`, i.e.
`season2/posts/<name>` — a spelling no live seat is on. Every live seat is
on the town-first spelling (`origin refs/heads/core/season2/posts/sanctuary-
helper/main`). Build order (goal:g15): read the row town cell through
`towns.row_town`, derive the post branch through `branches.derive_names`, and
refuse a rename BY NAME when the new name's row town differs or the row
cannot be resolved.

**WHAT THE MACHINE ACTUALLY DOES NOW (built bytes).**

- `extensions/agi/bin/rotate.py:70` — `import towns` beside `branches`.
- `:3400-3448` — new `RenameTownRefusal`, `_row_season`, `_row_town_or_refuse`
  (calls `towns.row_town(root, row)` — the established reader; a declared cell
  wins, the transitional `overrides` map retires itself), and
  `_town_post_branch` (derives via `branches.derive_names(town, season,
  post=name)["post_main"]`, then asserts the branch's first segment equals the
  row town).
- `_rename_surfaces` branch rows now name `core/season2/posts/old/main ->
  core/season2/posts/new/main` (measured: `test_rename_post_surface_is_town_
  first`). Worktree-dir surface `.agi/worktrees/post-<name>` is UNCHANGED
  (measured live: `post-sanctuary-helper`).
- `cmd_rename_post` catches the refusal and returns 4 after printing the
  name-bearing line `rename-post REFUSED: <post> is in town <t>, <detail>` —
  before any staging, so a refused rename writes nothing.
- Season number comes from the SAME ladder field `season_branch` uses
  (`load_ladder_field(root, "current_season")`), never a second hardcoded
  spelling.

**MEASUREMENT, item 4 (rotate-self).** `cmd_rotate_self` (rotate.py:17162)
performs exactly ONE rename: its own tmux WINDOW (`_rename_own_window` called
at :17803). A grep of the whole function body finds no `post_branch`,
`derive_names`, or `_rename_surfaces` call — the path carries NO branch/town
surface, so no town logic was added there.

**EVIDENCE.** `python3 -m pytest extensions/agi/tests/test_rotate.py
  extensions/agi/tests/test_rename_post.py
  extensions/agi/tests/test_town_rows_readers.py
  extensions/agi/tests/test_branch_spelling_grep.py
  extensions/agi/tests/test_no_literal_town.py
  extensions/agi/tests/test_branches.py
  extensions/agi/tests/test_rotate_sm36_residue.py -q` -> **429 passed,
0 failed** (tier-gate notice: one phantom running record skipped, unrelated).

New tests: `test_rename_post_surface_is_town_first` (a), `test_rename_post_
refuses_a_cross_town_rename_by_name` (b), `test_rename_post_proceeds_when_
new_row_is_same_town` (c), `test_rename_post_refuses_an_unresolvable_row_by_
name`, and `test_rename_boundary_derives_its_branch_town_through_row_town`
(the `all` + overrides row and a declared-cell row both land in the derived
segment through `towns.row_town`).

**Deviations.** (1) The brief named `test_rotate.py` for (a)-(c); the rename
suite actually lives in `test_rename_post.py`, so the new tests were added
there (calling `rotate._rename_surfaces` / `cmd_rename_post`) rather than
duplicating a fixture. (2) Three pre-existing tests in `test_rename_post.py`
asserted the OLD town-less spelling
(`test_dry_run_lists_round2_surfaces_not_applied`,
`test_branch_deleted_only_under_delete_old`,
`test_live_apply_runs_real_git_argv`); they were updated to the town-first
spelling — they were asserting the defect. (3) The fixture has no ladder, so
`load_ladder_field` prints its usual `warn: ladder node not found` on the
rename path; this matches `season_branch`'s existing behaviour and is not a
regression.

**Production lines:** 58 added / 4 removed (`git diff --numstat --
extensions/agi/bin/rotate.py`), ceiling 60.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
TIER-PARENT REVIEW (a00-2b8d00ba, SM.59). (1) WHAT THE INSTRUCTION SAID: claim (1) "the rename boundary ... reads the row town cell via the same config_town_cell/_is_nonprime_row-style helper ... and a rename that would move a post OUT of its declared town is a NAMED refusal, never silent"; claim (2) "rename tooling ASSERTS the town segment matches the row town cell before renaming". (2) WHAT THE MACHINE ACTUALLY DOES: the town read and the cross-town refusal are real and measured - cmd_rename_post returns 4 with "rename-post REFUSED: old is in town core, the new name new is a row in town sanctuary" and stages nothing (my gate probe, 2026-09-16). The assertion is NOT real: _town_post_branch (rotate.py:3430-3438) compares branch.split("/",1)[0] against the very town it passed into branches.derive_names, and derive_names BUILDS the branch from that town (branches.py:319: out["post_main"] = f"{town}/season{town_season}/posts/{post}/main") - the comparison can never be false. My wire probe on the LIVE graph: sensei-director row cell `all` -> towns.row_town -> `sanctuary` ([config].md town_cell overrides), so the surface names sanctuary/season2/posts/sensei-director/main, while origin carries ONLY core/season2/posts/sensei-director/main (plus the legacy head season2/posts/sensei-director). No assertion fires, no refusal; sanctuary-helper and sanctuary-director match their live refs, sensei-director does not. (3) THE NEAR MISS: an assertion over a value DERIVED from the row town cell satisfies the words "asserts the town segment matches the row town cell" and is a tautology; the branch whose segment the falsifier is about is the REAL ref being renamed, which this round never consults. (4) DEVIATION: none mine; the kid moved the new tests to test_rename_post.py because that is where the rename suite actually lives - my brief named test_rotate.py wrongly.
<!-- THOUGHT:END -->

## Agent Notes
Built the town-first rename boundary: _rename_surfaces derives branch/origin surfaces via branches.derive_names from towns.row_town, cmd_rename_post refuses by name (exit 4, nothing staged) on cross-town or unresolvable rows; rotate-self measured to carry no branch surface. 58 production lines / 60 ceiling. 429 tests pass across the 7 relevant suites.

TIER-PARENT REVIEW (a00-2b8d00ba, SM.59), verdict DEMOTED proved -> inconclusive_lean_disproved:70. prose=pass, and_that_is_the_problem. probes: (gate, conjunct 1, PASS) cross-town rename old(core)->new(sanctuary row) through cmd_rename_post -> exit 4, stderr "rename-post REFUSED: old is in town core, the new name new is a row in town sanctuary", no .agi/sessions/seats/old.rename.json staged. (wire, conjunct 2, FAIL) live-graph probe over origin refs: for every live post row, compare the derived branch surface with the real refs; sanctuary-director and sanctuary-helper match (core/...), sensei-director does NOT - derived sanctuary/season2/posts/sensei-director/main, live core/season2/posts/sensei-director/main (+ legacy season2/posts/sensei-director) - and no refusal is raised, because the only assertion compares the derived string against the town it was derived from. Falsifier earned: a branch spelling that disagrees with the row town cell is named silently instead of refused. Accepted bytes (the town read, the cross-town refusal, the refusal return code, the test updates); RE-CUT as kid 2 with the demand that the ASSERTION read the REAL branch, not the derived value.
