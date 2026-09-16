---
id: experiment:a00-f6520184-3ff123
mint_id: 0ce8330d40f747d8804d58a877a65cf5
type: experiment
parents:
  - hypothesis:l4-rename-boundary-preserves-the-real-branch-project-town-and-never-compares-it-to-the-home-town
next_edges: []
confidence: 0.85
edited_by: a00-529d51a2
evidence_runs:
  - experiment:a00-f6520184-3ff123
line_ceiling: 30
loop: hypothesis:l4-rename-boundary-preserves-the-real-branch-project-town-and-never-compares-it-to-the-home-town@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent_probes.py P1: row home town=core, injected REAL ref web-app-suite/season3/posts/old/main (a project town the SM.59 derivation could never reach)", "expected": "no RenameTownRefusal; branch src = the real ref, dst keeps the project town AND season", "observed": "src=web-app-suite/season3/posts/old/main dst=web-app-suite/season3/posts/new/main", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent_probes.py P2: reader answers (season2/main, core/main) with NO ref for the post; plus the CLI dry-run on a gitless root", "expected": "no branch / branch (origin) surface, stderr names the post, dry-run exit 0, no derived posts/<old> spelling anywhere", "observed": "no_branch_surface=True reason='rename-post: no real branch for old: nothing to rename'; cli rc=0 reason='cannot read local refs for old: nothing to rename'", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent_probes.py P3: (a) new-name row in a different HOME town; (b) two disagreeing real refs; (c) control = new-name row SAME home town but a project town that differs from the row cell", "expected": "(a) and (b) raised by name; (c) proceeds and keeps the real project town", "observed": "(a) REFUSED old in town core, new is a row in town sanctuary; (b) REFUSED 'real branches that disagree'; (c) dst=sanctuary/season9/posts/new/main", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent_probes.py P4: towns.row_town patched to LIE (returns sanctuary) while the real ref says core and the new name is not an existing row; plus a byte grep of _town_post_branch", "expected": "branch spelling unchanged by the row town; the t_town != town comparison and the derived fallback absent from the live bytes", "observed": "src=core/season2/posts/old/main dst=core/season2/posts/new/main; deleted_comparison_present=False", "result": "pass"}
production_lines: 5
profile: balanced
role: kid
scaffold_hash: c5f0c58e700f7e8c
season: 2
title: A00 f6520184 3ff123
town: core
verdict: proved
---
## Experiment

SM.62 build order (g15 claim = behaviour to build, not a hypothesis to
measure). Measured the SM.59 pre-fix state, IMPLEMENTED the four conjuncts,
then proved them on the built bytes.

**Pre-fix measurement (main 7ae85886c, SM.59 bytes):** `_town_post_branch(root,
old_town, old, reader)` derived `branches.derive_names(town, ...)` and, when the
real local ref was `core/season2/posts/<post>/main` while `towns.row_town`
resolved `<post>` to `sanctuary`, raised `RenameTownRefusal` (exit 4) -- the
very rename the owner ordered. The row town cell and the branch project town
were welded into ONE axis.

**Built (rotate.py):**
1. `_town_post_branch(root, name, reader)` no longer takes or compares the row
   `town`. It reads the REAL local refs and returns the single real ref
   spelling -- the `(project town, town_season)` tuple is preserved VERBATIM
   through `_rename_post_segment` (kept). Several real refs that disagree still
   raise the same named refusal.
2. A post with NO real ref (or a reader that cannot answer) has NO branch
   surface: `branch` / `branch (origin)` are omitted and the reason is printed
   skipped-by-name -- `rename-post: no real branch for <post>: nothing to
   rename` / `cannot read local refs for <post>: nothing to rename`. The
   derived-spelling fallback is DELETED, not bypassed.
3. The surviving town refusals: (a) two real branches that disagree (unchanged),
   (b) a new-name row whose HOME town (`towns.row_town`) differs from the old
   row's (unchanged).
4. `towns.row_town` is read for (3b) and nothing else on this path.

**Judgement call (stated):** a `None` reader (git cannot answer) ALSO skips the
branch surfaces by name -- the deleted fallback means a spelling cannot be
invented from a ref nobody can see. It gets its own reason text so a
cannot-answer is distinguishable from a no-refs answer.

**Deviation from the brief (documented):** `_rename_post_segment` is NOT kept
byte-for-byte. A legacy town-less real ref (`season2/posts/<name>`, `kind:
post`, no `town` key) crashed `p["town"]` under the new no-fallback path. A
three-line arm preserves that legacy shape verbatim
(`season2/posts/<name>` -> `season2/posts/<new>`); the real ref is never
re-spelled into a town-first one. This is what "preserve the real tuple
verbatim" means for a ref that has no town segment.

**Test scope deviation (documented):** `extensions/agi/tests/test_rotate.py`
also encoded the deleted comparison in
`test_rename_post_default_reader_is_real_git_and_refuses_by_name` (a real
town-less ref + a `core` row cell -> refusal). The brief listed only
test_rename_post.py and test_town_rows_readers.py; this fourth assertion lived
elsewhere, so it was rewritten in place (now
`..._preserves_the_real_ref`: real git reader, staged `season2/posts/adv2`).
Leaving it would have left the suite red.

## Evidence

Suite runs (`python3 -m pytest ... -q`):

- `extensions/agi/tests/test_rename_post.py` -- **33 passed**.
- `extensions/agi/tests/test_town_rows_readers.py` + `test_rotate.py` -- **318
  passed** (the one rewritten test green).
- The wider rotate set (`test_rotate.py`, `test_post_rename.py`,
  `test_rotate_sm36_residue.py`, `test_branches.py`, `test_rotate_handover.py`,
  `test_rotate_tail.py`) -- **493 passed, 0 failed**.

First-hand live shape (`.agi/sessions/iter-SM.62/a00-f6520184/probe_live_shape.py`):
row cell `sensei-director -> sanctuary`, real local ref
`core/season2/posts/sensei-director/main`, `rename-post sensei-director
director-sanctuary --dry-run` -> **rc = 0**, table emits
`branch: core/season2/posts/sensei-director/main ->
core/season2/posts/director-sanctuary/main` and `branch (origin):
origin/core/...`; `HAS_SANCTUARY_SPELLING: False`.

Falsifiers, each a test:
- `test_a_sanctuary_home_post_on_a_core_branch_proceeds` -- the SM.59 live
  shape now proceeds, keeps the real `season7` season, never re-spells town.
- `test_no_real_branch_for_the_post_skips_the_branch_surfaces_by_name` --
  no-ref post -> no branch surface, reason names the post, dry-run exit 0.
- `test_a_reader_that_cannot_answer_skips_the_branch_surfaces_by_name` -- the
  judgement call, pinned.
- `test_real_branches_that_disagree_with_each_other_refuse` and
  `test_rename_post_refuses_a_cross_town_rename_by_name` -- the two surviving
  refusals, unchanged.
- `test_rename_boundary_never_derives_a_branch_from_the_row_town`
  (test_town_rows_readers.py, rewritten) -- no branch surface is derived from
  `towns.row_town`.

Production diff: `git diff --numstat -- extensions/agi/bin/rotate.py` ->
**29 insertions, 24 deletions (net +5)** against a ceiling of 30.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW VERSION (a00-529d51a2, SM.62). Instruction: "Run one negative probe per claim conjunct yourself and record them as probes; a kid that passes its own suite but fails your probe is lean_disproved with the probe named." Byte check I actually ran (not the result file): git diff 7f72882f5..HEAD — _town_post_branch no longer takes or compares a row town, the t_town != town refusal and the derived fallback are absent (grepped the live range between def _town_post_branch and def _rename_post_segment), and _rename_surfaces guards `if old_branch is not None` so branch/branch (origin) are simply not emitted. I then RAN four of my own probes (parent_probes.py, this session dir), one per conjunct, all pass: P1 conjunct-1 wire = a project town the derivation could never reach (web-app-suite/season3) survives verbatim with its season; P2 conjunct-2 gate = reader answers with no ref for the post -> no branch surface, the reason names the post, dry-run exit 0, and no surface carries posts/<old>; P3 conjunct-3 gate = the two surviving refusals (new-name home-town, disagreeing real refs) plus a negative control where the new-name row is the SAME home town but a DIFFERENT project town, which proceeds; P4 conjunct-4 wire = towns.row_town patched to LIE (sanctuary) while the ref says core, and the branch spelling is unchanged. Near miss: the kid rewrote its own tests, so those tests are the claim, and none of them proves the row town CANNOT reach the spelling — P4 supplies exactly that falsifying case, and it is the one probe here whose failure mode (a surviving row-town-to-branch channel) would otherwise ride until a later harvest. Deviations from the kid brief, both documented above and both accepted: (a) _rename_post_segment gained a 3-line legacy arm because a town-less real ref (p["town"] is None) crashed under the new no-fallback path — "verbatim" required it; (b) extensions/agi/tests/test_rotate.py was rewritten because a fourth assertion of the deleted comparison lived there and would have left the suite red. Kept as proved; the one weak spot is prose only — _local_branches docstring still says "the caller keeps the derived spelling", which is no longer true, so it is named as a caveat rather than re-cut.
<!-- THOUGHT:END -->

## Agent Notes
Built the four SM.62 conjuncts: _town_post_branch no longer takes/compares the row town; the real ref tuple is preserved verbatim; no-ref/cannot-answer posts skip branch surfaces by name; towns.row_town read only for the new-name home-town refusal. rotate.py net +5 lines (ceiling 30). 493 rotate-set tests pass; first-hand live shape exits 0 and emits core/season2/posts/director-sanctuary/main.
