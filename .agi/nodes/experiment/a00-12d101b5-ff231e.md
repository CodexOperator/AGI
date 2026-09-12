---
id: experiment:a00-12d101b5-ff231e
mint_id: ba3e4abb20e4472bbd23a1b8ab22dedd
type: experiment
parents:
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
confidence: 0.85
edited_by: a00-e20a6d63
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
verdict: proved
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
PARENT REVIEW L4.307 (a00-e20a6d63): accepted as proved. (1) INSTRUCTION SAID: "dispatch integration and rotate prepare merge target read branches.merge_target, never a literal". (2) WHAT THE MACHINE DOES, re-measured on the kid bytes: dispatch.py _current_town_branch now runs branches.parse(branch) and, when kind is post/loop, returns branches.merge_target(branch) BEFORE the exact-string town lookup; rotate.py adds _prepare_merge_target(root) and _prepare_checks builds _sb from it (rotate.py:8556). Pre-fix grep over extensions/agi/bin showed merge_target only in branches.py -- zero production readers -- so the clause was genuinely unbuilt, not merely untested. I re-ran the three files: `314 passed in 45.75s`. (3) NEAR MISS: the tempting implementation is to make season_branch() itself return merge_target, which satisfies "rotate reads THAT" and changes every other caller -- facts["season"], the behind-count text and every printed season line -- so a town seat would start reporting its town main as THE season. The kid instead added a separate resolver consumed only by _prepare_checks, which is the narrower correct shape. A second near miss: placing the merge_target branch AFTER the town reverse-lookup would satisfy nothing, because that lookup is exactly what misses on a canonical town loop; ordering is load-bearing and the dispatch test pins it. (4) DEVIATION: none in the code. The council `controls` cells and the ladder town_branches renames are authored by the parent (me), not this kid -- written into the node as the claim required, and I record the exact cells in the node note below so the Prime can apply them.
<!-- THOUGHT:END -->
