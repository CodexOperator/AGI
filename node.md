---
id: experiment:a00-bfab1241-d55055
mint_id: ae6d1cc0910043ae8011bbc5617912b6
type: experiment
parents:
  - hypothesis:l4-sm32b-town-first-rename-boundary
next_edges: []
confidence: 0.65
edited_by: sensei-director
evidence_runs:
  - experiment:a00-bfab1241-d55055
line_ceiling: 60
loop: hypothesis:l4-sm32b-town-first-rename-boundary@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 63
profile: balanced
role: kid
scaffold_hash: 09d09f707c00e9be
season: 2
title: A00 bfab1241 d55055
town: core
verdict: inconclusive_lean_disproved:65
---
# experiment:a00-bfab1241-d55055

## Experiment

**WHAT THE INSTRUCTION SAID.** The round-1 assertion was a tautology: `_town_post_branch` compared the town segment of a branch it had just derived from that same town (`rotate.py` round-1, ~:3430-3438). The parent's live probe proved it: `sensei-director` has row town `sanctuary` but its real local ref is `core/season2/posts/sensei-director/main`, and no refusal fired. Build order (goal:g15): make the boundary read the REAL branch and refuse BY NAME when its town segment disagrees with the row town cell.

**WHAT THE MACHINE ACTUALLY DOES NOW (built bytes).**

- `extensions/agi/bin/rotate.py:3428-3438` — new module-level reader `_local_branches(root)`: `_git_lines(root, "for-each-ref", "--format=%(refname:short)", "refs/heads")` inside `try/except`, returning `None` when git cannot answer. `None` means CANNOT ANSWER (a gitless fixture), never `no refs`; that case is commented and keeps the pre-fix derive-and-proceed.
- `:3440-3481` — `_town_post_branch(root, town, name, reader=None)`: derives the town-first spelling as before, then reads the post's REAL local refs. Every name goes through the ONE grammar (`branches.parse`); refs whose `kind` is `post`/`v3_post` and whose `name` equals the post are kept.
  - real branch town segment != row town cell -> `RenameTownRefusal` naming BOTH towns, the real ref, and the derived spelling, before anything is staged;
  - real branches disagreeing with each other (distinct `(town, town_season)` tuples) -> `RenameTownRefusal` naming every ref;
  - exactly one agreeing real tuple -> THAT ref string is returned (not a re-derived string);
  - no real ref for the post (first seating/migration) -> derived spelling.
- `:3483-3488` — `_rename_post_segment(branch, name)`: the new branch keeps the SAME `(town, town_season)` tuple via `branches.derive_names` — a rename never moves a post's season (the ladder's `current_season` is not consulted for a real ref).
- `_rename_surfaces(root, old, new, branches_reader=None)` gained the injectable reader; `cmd_rename_post` keeps calling it with the default (real git). The cross-town refusal (`:3511-3517`) and the unresolvable-row refusal (`_row_town_or_refuse`) are UNCHANGED.

**MEASUREMENT (live-shape probe, scratch `probe-p42cp3_f/`).** Injected reader `["core/season2/posts/sensei-director/main"]`, row cell `sanctuary`:
`rc = 4`; stderr `rename-post REFUSED: sensei-director is in town sanctuary (row cell), the real branch core/season2/posts/sensei-director/main carries town core (derived spelling sanctuary/season2/posts/sensei-director/main)`; `sessions/seats/` empty (nothing staged). Under the round-1 bytes this probe exited 0 with the fabricated `sanctuary/...` spelling.

**TESTS (real counts, named files).**

- `extensions/agi/tests/test_rename_post.py` — 5 new round-2 tests: live-shape mismatch refuses (rc 4, both towns, both spellings, nothing staged); agreeing real branch is the carried spelling AND the new branch keeps its season (real ref `core/season7/posts/old/main` -> `core/season7/posts/new/main`, never the ladder's `season2`); `None` reader keeps the derived spelling; reader answers with no ref for the post keeps the derived spelling; disagreeing real branches refuse by name.
- `extensions/agi/tests/test_rotate.py` — one new test on the REAL git fixture `_git_with_post_branch`: the DEFAULT reader reaches the changed bytes (a real ref `season2/posts/adv` with no town segment against row cell `core` is refused, rc 4, nothing staged). 311 passed.
- Suites: `test_rename_post.py` + `test_town_rows_readers.py` = **40 passed**; `test_rotate.py` = **311 passed**.

**DEVIATION (one, forced).** `test_default_apply_calls_subprocess_zero_times` asserted the default path ran `subprocess.run` ZERO times — incompatible with a real-ref read. Its actual safety property is "no real rename without `--live`", so the guard is narrowed to zero MUTATING subprocess (a read-only `for-each-ref` is allowed and asserted to have run). Documented in the test docstring. The `--live` executor behaviour is untouched (`test_live_apply_runs_real_git_argv` passes).

**PRODUCTION LINES.** `git diff --numstat -- extensions/agi/bin/rotate.py` = **63 added / 13 removed** (net +50). Ceiling 60, so 3 lines over the added-column reading; under the 2x=120 stop rule, no re-brief. The overage is docstring, not control flow.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rename_post.py extensions/agi/tests/test_town_rows_readers.py -q` -> `40 passed in 0.44s`
- `python3 -m pytest extensions/agi/tests/test_rotate.py -q` -> `311 passed in 58.26s`
- `git diff --numstat -- extensions/agi/bin/rotate.py` -> `63\t13\textensions/agi/bin/rotate.py`
- live-shape probe above: `rc = 4`, refusal line names both towns and both spellings, `staged: none`

## Agent Notes
Real-ref gate: rename boundary reads LOCAL refs via injectable _local_branches (None=cannot answer keeps derived); a real branch whose town segment disagrees with the row cell is a NAMED REFUSAL naming both towns + both spellings before staging; agreeing ref is the carried spelling; disagreeing refs refuse. Live-shape probe rc=4, nothing staged. 5 new tests in test_rename_post.py, 1 real-git test in test_rotate.py (40 + 311 passed). Production 63/13 numstat, ceiling 60.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
TIER-PARENT REVIEW (a00-2b8d00ba, SM.59). (1) WHAT THE INSTRUCTION SAID: claim (2) "rename tooling ASSERTS the town segment matches the row town cell before renaming", falsifier "a branch created whose town path segment disagrees with the row town cell"; the re-cut brief said make the assertion read the REAL branch, not the value derived from the cell. (2) WHAT THE MACHINE ACTUALLY DOES: rotate.py:3428-3462 now lists LOCAL refs via _git_lines(for-each-ref refs/heads) behind a reader seam (None = cannot answer keeps the derived spelling), parses each through branches.parse, keeps kind post/v3_post with the same name, and RAISES RenameTownRefusal naming both the row town cell and the real branch town when they differ, or when two real branches disagree; an agreeing real branch IS the spelling the surface carries (:3462 returns real[0][0]); _rename_post_segment (:3465) keeps the renamed post on its own (town, town_season). My live probe (.agi graph, 2026-09-16): sensei-director -> REFUSED, "sensei-director is in town sanctuary (row cell), the real branch core/season2/posts/sensei-director/main carries town core (derived spelling sanctuary/season2/posts/sensei-director/main)"; sanctuary-helper and sanctuary-director proceed with core/season2/posts/<name>/main, the real refs. (3) THE NEAR MISS: the PREVIOUS round asserted branch.split("/",1)[0] == the town it had just passed to branches.derive_names, which branches.py:319 builds the branch FROM - a tautology that names sanctuary/season2/posts/sensei-director/main, a ref that does not exist, with no refusal. This round rereads reality; the assertion is now falsifiable, which is why it fired on a live row. (4) DEVIATION: 63 production lines against the 60 ceiling (5 percent over) - accepted, the seam plus the refusal text cost it; no config node touched, so the DATA divergence (row cell sanctuary vs branch core for sensei-director) is surfaced as a named refusal, not fixed here, and rename-post for that post is fail-closed until the Prime reconciles the row or the ref.
<!-- THOUGHT:END -->

TIER-PARENT REVIEW (a00-2b8d00ba, SM.59): ACCEPT, verdict proved CONFIRMED at the parent with probes: (gate, conjunct 1) cross-town rename through cmd_rename_post -> exit 4, "rename-post REFUSED: old is in town core, the new name new is a row in town sanctuary", nothing staged. (wire, conjunct 2, LIVE graph) sensei-director -> REFUSED naming row town sanctuary vs real branch core/season2/posts/sensei-director/main; sanctuary-helper/sanctuary-director proceed with their real refs. (gate, conjunct 2) two disagreeing real branches -> refusal. (wire, conjunct 2, real git reader) a repo whose only local post branch is core/... with a row cell resolving to sanctuary -> REFUSED by the default reader, not only the injected one. Sanity (not evidence): test_rename_post.py + test_town_rows_readers.py + test_rotate.py = 351 passed, 0 failed. Residue for the Prime: the config [config].md town_cell override still says sensei-director -> sanctuary while every ref for that post is core, so rename-post for that post now fails closed until the row or the branch is reconciled; the tool does what the claim asks and names the disagreement instead of silently renaming the wrong branch. Also: the reader reads LOCAL refs only, so a post whose branch exists on origin but not locally keeps the derived spelling.

Demoted per SM.69 item 3c (kid experiment:a00-5389cf29-16a80f) and the belam gen-26 split ruling on 9d90c43c2: this experiments proved verdict evidenced the t_town != town comparison in the rename boundary, which hypothesis:l4-rename-boundary-preserves-the-real-branch-project-town-and-never-compares-it-to-the-home-town claim (4) has since DELETED (not bypassed) per the SM.62 owner ruling that a posts sanctuary home town and its branchs project town are expected to differ. The mechanism this experiment proved no longer exists in the code; demoted rather than left reading proved for a deleted comparison. Landed directly by the director (graph-only repair, per belam split ruling 23:27Z) since the kids own uncommitted edit never reached a commit.
