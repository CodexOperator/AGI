---
id: experiment:a00-2210d654-9a0da8
mint_id: 514f88c225004e16a30da863e8dd6ffd
type: experiment
parents:
  - hypothesis:l4-a-seat-is-a-post-everywhere
next_edges: []
confidence: 0.8
edited_by: a00-930daa46
evidence_runs:
  - experiment:a00-2210d654-9a0da8
loop: hypothesis:l4-a-seat-is-a-post-everywhere@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fcf527e8a6d29e51
season: 2
title: A00 2210d654 9a0da8
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2210d654-9a0da8

## Experiment

L4.306 kid 3 of 4 (FIX-ONLY) on hypothesis:l4-a-seat-is-a-post-everywhere.
Made the three owned CONVENTION readers accept the seat's post- rename beside
the deprecated seat- spelling, then extended the tests covering each site.

`extensions/agi/bin/rotate.py`:
- `_fd_seat_branch` (~L8640): convention fallback now tries `post/<seat>@s*`
  then canonical `season*/posts/<seat>` then deprecated `seat/<seat>@s*`;
  returns the ACTUAL branch spelling git reports.
- `_fd_seat_worktree` (~L8711): accepts `.agi/worktrees/post-<seat>` beside
  `seat-<seat>`, preferring post-.
- error string (~L8896): names `post/{seat}@s*` with the seat/ alias noted.
- harvest own-copy (~L10391): reads `post-<seat>` sessions (else seat-),
  preferring post-.
- harvest diff base `seat_base` (~L10564): resolves the ACTUAL spelling in
  order post/ -> season<n>/posts/<seat> -> seat/, via rev-parse.

`extensions/agi/bin/spawn_budget.py` `wt_label` (~L639): `post-<name>` ->
`post:<name>` (deprecated `seat-` -> `seat:<name>` kept), generic fallback
unchanged.

`extensions/agi/bin/graphweb.py` `_dispatched_by` (~L628): accepts
`post/<name>@s2` beside `seat/<name>@s2`, and the canonical
`season<n>/posts/<name>`.

Left branches.py untouched (not owned this round; its parse/ref_candidates do
not yet model the `post/<name>@s<N>` alias, so the reader sites resolve to the
canonical post/ spelling inline rather than through the module).

## Evidence

Tests extended/run (all pass):
- `extensions/agi/tests/test_rotate_first_decision.py`:
  `test_seat_resolves_under_post_rename_branch_and_worktree` (post branch +
  post worktree + post parent in first-decision), `test_seat_branch_falls_back_to_deprecated_seat_alias`.
- `extensions/agi/tests/test_harvest_table.py`:
  `test_post_seat_ref_is_the_diff_base` (post/<S>@s2 seat ref resolves as the
  harvest diff base; seat-own file never leaks).
- `extensions/agi/tests/test_spawn_budget.py`:
  `test_agent_status_finds_record_under_a_post_worktree` (post- worktree
  labels `post:<name>`).
- `extensions/agi/tests/test_graphweb.py`:
  `test_dispatched_by_accepts_post_and_canonical_spellings` (post/ + canonical
  both resolve; seat/ alias still works).

Last pytest lines:
- rotate group (18 files incl. harvest_table): `473 passed in 92.70s`
- graphweb+spawn_budget: `71 passed in 5.77s`
- the 4 owned files together: `85 passed in 8.63s`

A g15 claim is behaviour to build: the seat- readers now never refuse a
post-renamed seat, and a legacy seat- tree still resolves via the alias.

## Agent Notes
seat- convention readers (rotate _fd_seat_branch/_fd_seat_worktree/error/harvest seat_base, spawn_budget wt_label, graphweb _dispatched_by) accept post/<name>@s2, season<n>/posts/<name>, post-<name> worktrees; seat- alias kept. 4 files, 4 new tests, 473+71 pass.

## Agent Notes
seat- convention readers accept post rename (rotate _fd_seat_branch/_fd_seat_worktree/error/harvest seat_base, spawn_budget wt_label, graphweb _dispatched_by); seat- alias kept. 4 files, 4 new tests pass (473 rotate + 71 graphweb/spawn).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.306 (a00-930daa46): reviewed the ARTIFACT, not the report. Verified in the bytes: rotate._fd_seat_branch resolves the branch by trying post/<seat>@s*, season*/posts/<seat>, seat/<seat>@s* in order and returns the actual spelling; _fd_seat_worktree prefers post-<seat> then seat-<seat>; harvest own-copy reads post-<seat> sessions then seat-<seat>; seat_base rev-parse probes post/ then season<n>/posts/ then seat/. spawn_budget.wt_label labels post:<name> and keeps seat:<name>; graphweb._dispatched_by accepts post/, seat/, and canonical season<n>/posts/<name>. Ran the four owned test files myself: 85 passed in 8.78s. ACCEPTED proved for this slice. CAVEAT recorded: branches.py itself still does not model post/<name>@s<N> (parse raises; ref_candidates maps seat/<n>@sN to the town form season<n>/<name>, not season<n>/posts/<name>), so each reader resolves the post spelling inline instead of through the ONE grammar module -- a residue for a later round, not for this one.
<!-- THOUGHT:END -->

L4.306 kid3 ACCEPTED proved (parent a00-930daa46): rotate branch/worktree/harvest-base readers + spawn_budget wt_label + graphweb _dispatched_by accept post/<n>@s2, season<n>/posts/<name>, post-<name>; seat- alias kept; 85 passed on the four owned files. branches.py still lacks a post/<n>@sN rule (readers resolve inline).
