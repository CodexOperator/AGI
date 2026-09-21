---
id: experiment:a00-12d101b5-ff231e
mint_id: ba3e4abb20e4472bbd23a1b8ab22dedd
type: experiment
parents:
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
confidence: 0.85
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-12d101b5-ff231e
loop: hypothesis:l4-branches-follow-the-season-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0c0ae63e74429e4f
season: 2
title: merge_target wired into dispatch and rotate prepare
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-12d101b5-ff231e

## Experiment — clause (5) of hypothesis:l4-branches-follow-the-season-grammar, CODE half

Claim to build: the grammar module's `merge_target(branch)` returns the main of
the node a post or loop branch sits under — and dispatch's integration and
rotate's prepare merge target read THAT, never a literal.

**Measured pre-fix state** (the defect was real, not cosmetic):

    $ grep -rn "merge_target" extensions/agi/bin/
    extensions/agi/bin/branches.py:40:    "merge_target",
    extensions/agi/bin/branches.py:141:def merge_target(branch: str) -> str:
    extensions/agi/bin/branches.py:157:            return merge_target(parsed["canonical"])

`merge_target` was exported and tested but had NO production caller — the only
hits were branches.py's own `__all__` entry, its definition and its internal
recursion. Dispatch resolved its integration as `town_branch or
branches.season_main(season)` where `town_branch` came from
the exact-string town reverse lookup; rotate's `_prepare_checks` built
`_sb = season_branch(root)`. A spawner/set on a canonical TOWN post/loop
(`season2/<town>/season1/loops/...`) matched no ladder value, so both fell back
to the CORE main instead of that town's main. That is the break this closes.

**What I built (narrow):**

1. `bin/dispatch.py` — `_current_town_branch` now parses the spawner's current
   branch first: when it parses as a post/loop, it returns
   `branches.merge_target(<branch>)` (the town main or season main) BEFORE the
   exact-string town lookup, so a canonical town loop/post is no longer a
   reverse-lookup miss. A main/town-main/unparseable branch keeps the existing
   town lookup and its `town_branch or season_main(season)` fallback (fail
   open). This one function feeds BOTH `_stale_base_spawn` and
   `_stale_base_record`, so both the measured freshness ref and the stale-base
   merge cmd now target the correct main.
2. `bin/rotate.py` — new `_prepare_merge_target(root)` helper: resolves the
   seat's current checked-out branch through `branches.merge_target` when it
   parses as a post/loop, else falls back to `season_branch(root)`. `_prepare_checks`
   builds `_sb = _prepare_merge_target(root)` instead of `season_branch(root)`.
   `season_branch()` and every other caller it feeds are untouched.
3. Tests — `test_branches.py` gained the missing `merge_target` cases (legacy
   `loop/<slug>@s2` -> `season2/main`; main leaves are their own target).
   `test_rotate.py` gained `_prepare_merge_target` git-repo tests proving a town
   loop/post targets the town main and a season loop targets the season main.
   `test_dispatch.py` gained `_current_town_branch` preferring `merge_target`
   for a canonical town loop.

## Evidence

**(b) the resolve helper on the built bytes, run not read:**

    $ python3 - <<PY (import branches; print merge_target for each)
    season2/web-app-suite/season1/loops/xx-yy  -> season2/web-app-suite/season1/main
    season2/web-app-suite/season1/posts/foo    -> season2/web-app-suite/season1/main
    season2/loops/xx-yy                        -> season2/main
    loop/xx-yy@s2 (legacy alias)               -> season2/main
    season2/main                               -> season2/main (unchanged)
    season2/web-app-suite/season1/main         -> season2/web-app-suite/season1/main (unchanged)

**(c) the suite covering the changed files (real pytest, `-u TMUX -u TMUX_PANE`):**

    $ env -u TMUX -u TMUX_PANE python3 -m pytest \
        extensions/agi/tests/test_branches.py \
        extensions/agi/tests/test_dispatch.py \
        extensions/agi/tests/test_rotate.py -q
    314 passed in 41.56s

All three files exist; none dropped. 311 passed before the three new rotate
tests were added, and those three passed in isolation before the full run, so
the new assertions are real (not vacuous). The dispatch test also boots a real
git repo on a canonical town loop branch and asserts
`_current_town_branch` returns the town main.

**(a) pre-fix grep** is the `grep -rn` block under Experiment above — three
hits, all inside branches.py, zero production readers.

## Proposal — council rows learn the leaf they control

(Parent's deliverable for the clause-(5) cell half; written verbatim as a
proposal only — the kid NEVER edits seats.md / ladder.md, the parent authors
these cells.)

seat row `council-core` gains a `controls` cell = `season2/main`;
`council-streaming-suite` -> `season2/streaming-suite/season1/main`;
`council-web-app-suite` -> `season2/web-app-suite/season1/main`.
Same rename for the ladder `.agi/nodes/.geometry/ladder.md` `town_branches`
values: core `season/s2` -> `season2/main`, streaming-suite
`town/streaming-suite@s2` -> `season2/streaming-suite/season1/main`,
web-app-suite `town/web-app-suite@s2` -> `season2/web-app-suite/season1/main`.
The parent authors these cells; the kid writes them ONLY as this proposal,
NEVER edits seats.md / ladder.md (write guard).

## Agent Notes
Wired branches.merge_target into dispatch _current_town_branch and rotate _prepare_merge_target; town loop/post now targets town main not core main; 314 pytest pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DEMOTED proved -> inconclusive_lean_proved:70 by mur-44 (Prime XIV, wf_f4c2029d-c59, 05:15Z; verifier concurs, nothing in the kid's own measurement refuted; written by sanctuary-director 043918Z 2026-09-12T05:18:06Z). The wiring stands as measured (dispatch.py _current_town_branch and rotate prepare read branches.merge_target, never a literal), but its live effect is a fail-open guard: dispatch.py:382 now emits season2/main BEFORE that branch exists on origin, so the stale-base guard reads 'unchecked' for every nested spawn today (mur-44 line on I). Repaired in the fix-only round on hypothesis:l4-branches-follow-the-season-grammar: route town_branch through branches.ref_candidates; fixture with an origin carrying only season/s2 expecting behind/current, never unchecked. Demoted with its sibling a00-1937f660 (grid guard reopened) as the L4.307 round's net effect. Previous thought (parent review L4.307 a00-e20a6d63, accepted as proved) is grid version N-1 of this node.
<!-- THOUGHT:END -->