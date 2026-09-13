---
id: experiment:a00-27ad5b26-e45988
mint_id: ae5a09f574e74c96929ba4505ff5116a
type: experiment
parents:
  - hypothesis:l4-the-legacy-job-stream-yields-to-the-v3-plan-and-no-push-leaves-the-trunk-pair
next_edges: []
confidence: 0.9
edited_by: a00-7a20d346
evidence_runs:
  - experiment:a00-27ad5b26-e45988
loop: hypothesis:l4-the-legacy-job-stream-yields-to-the-v3-plan-and-no-push-leaves-the-trunk-pair@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: bc01159fc67a886c
season: 2
title: A00 27ad5b26 e45988
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-27ad5b26-e45988

## Experiment

g15 fix-only — close the yield's coherence hole in `cli.py` `branch-reshuffle`
(hypothesis:l4-the-legacy-job-stream-yields-to-the-v3-plan-and-no-push-leaves-
the-trunk-pair, building directly on KID A's `experiment:a00-8f68bdd1-ef2193`).
Measured, not inferred: on the live tree `_reshuffle_jobs` returns 328 jobs
(`Counter({loop:318, post:6, main:2, town_main:2})`), and the 6 post/seat alias
branches (`post/{sanctuary-director,sanctuary-helper,sensei-director}@s2` +
`seat/{...}@s2`) appeared NOWHERE in the `--dry-run` plan — the target's own
coherence clause ("each legacy branch appears in exactly one section with its
fate") was VIOLATED. Pre-fix they at least got a wrong-but-visible rename+push.

Root cause: `_rs_v3_posts_renames` (cli.py ~L3098) folds a legacy post/seat
alias into the v3 LOCAL rename only when its derived post_main target is FREE,
deduping by target so "two refs never land on one name". On the live tree a
canonical `season2/posts/<p>` branch already renames to each target, so the
fold-in dedupe dropped all 6 aliases. Step-1's `continue` for kind=post never
printed them either. The collision is real: `post/x@s2` and `seat/x@s2` BOTH
canonicalize to the same `season2/posts/x` — renaming each onto the derived
post main would collide.

Implemented (file scope: `extensions/agi/bin/cli.py` branch-reshuffle region
only + `extensions/agi/tests/test_branch_reshuffle_v3.py`):
1. Before step-1, when v3 is on and `post` in kinds, compute
   `_post_folded_olds` = the set of OLD names `_rs_v3_posts_renames` ACTUALLY
   folds in (read from the same list the plan section prints, so step-1 and
   the v3 posts section can never disagree).
2. In step-1's kind=post branch (cli.py ~L3517): a post-kind job whose old IS
   in `_post_folded_olds` stays a silent `continue` (it appears in the v3
   posts rename section, exactly once). A post-kind job whose old is NOT
   folded (target already owned by a canonical branch, or a same-target
   sibling) is a DEPRECATED DUPLICATE: it prints a routing line BY NAME —
   `legacy post <old> -> duplicate of <new>; left to --delete-old (no push,
   upstream unchanged)` — never renamed onto a target another ref already
   owns and never pushed.

Chosen fate: routing-line (option 2 of the brief) for every alias. Since each
target is owned by its canonical `season2/posts/<p>` branch here, no alias
could be the "surviving old-name" that renames — renaming one of the two
colliding siblings onto the target the canonical already renames to would
still be two refs -> one name. `--delete-old` genuinely removes them
(`_reshuffle_delete_set` derives origin refs/heads that fail
`branches.is_remote_visible`, and the fixture's post/seat names are delete
candidates), so "left to --delete-old" is a true fate, not a guess.

Tests added (extensions/agi/tests/test_branch_reshuffle_v3.py):
- `_v3_yield_collision_repo`: real-tree-shaped fixture (declared town set,
  remote names, a canonical `season2/posts/legacy-post` + BOTH `post/` and
  `seat/` aliases colliding onto it).
- `test_v3_yield_every_job_old_named_at_least_once`: count over ALL jobs via
  `cli._reshuffle_jobs` — every job's old name must appear somewhere in the
  dry-run stdout (a vanished alias fails).
- `test_v3_yield_colliding_post_seat_aliases_named_duplicate_each`: both
  colliding aliases appear exactly once as a named duplicate, no alias renamed
  or pushed, the canonical is the ONE rename source, the derived post_main is
  never pushed.

At-least-once (not literal exactly-once) for the all-jobs assertion, because a
legacy name can legitimately repeat inside PROSE: the v3 main-keep notice
contains the word `master` and ladder/rotations cell re-spelling proposals can
echo a town alias's name. Those are not a second fate in a second section. The
strong, hole-catching assertion is: no job may be ABSENT.

## Evidence

Real-tree, read-only, before + after:

```
$ python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run --kinds main,towns,posts,loops
branch-reshuffle (season=2): 328 legacy branch(es); v3 YIELD active (declared town set)
  legacy post post/sanctuary-director@s2 -> duplicate of season2/posts/sanctuary-director; left to --delete-old (no push, upstream unchanged)
  legacy post post/sanctuary-helper@s2   -> duplicate of season2/posts/sanctuary-helper;  left to --delete-old (no push, upstream unchanged)
  legacy post post/sensei-director@s2    -> duplicate of season2/posts/sensei-director;   left to --delete-old (no push, upstream unchanged)
  legacy post seat/sanctuary-director@s2 -> duplicate of season2/posts/sanctuary-director; left to --delete-old (no push, upstream unchanged)
  legacy post seat/sanctuary-helper@s2   -> duplicate of season2/posts/sanctuary-helper;  left to --delete-old (no push, upstream unchanged)
  legacy post seat/sensei-director@s2    -> duplicate of season2/posts/sensei-director;   left to --delete-old (no push, upstream unchanged)
```

Push set UNCHANGED — exactly the eight, all remote-visible:

```
git push origin master:season1/main          git push -u origin core/main
git push origin season2/main                 git push -u origin core/season2/main
git push -u origin streaming-suite/main      git push -u origin streaming-suite/season1/main
git push -u origin web-app-suite/main        git push -u origin web-app-suite/season1/main
```

Coherence proof (in-process read-only, live tree):

```
total jobs: 328            alias(post-kind) jobs: 6
  post/sanctuary-director@s2 count= 1        seat/sanctuary-director@s2 count= 1
  post/sanctuary-helper@s2   count= 1        seat/sanctuary-helper@s2   count= 1
  post/sensei-director@s2    count= 1        seat/sensei-director@s2    count= 1
ANY job absent from plan: 0
```

Clean side rails: `git for-each-ref refs/heads` byte-identical before/after;
no `sessions/*.json` plan written; no push performed (dry). Suite green:
`python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py
extensions/agi/tests/test_branch_reshuffle.py -q` -> **53 passed** (51 prior +
2 new).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The parent brief (KID B, L4.339) described the hole (6 post/seat aliases absent from the plan) and offered two acceptable fates. I chose the routing line over folding the ONE surviving alias to rename, because on this tree every alias target is already owned by a canonical season2/posts/<p> branch that renames to it — no alias could rename without colliding, so the true fate for all six is deprecated duplicate left to --delete-old. Deviation from the brief literal assert each old appears exactly once: I assert at-least-once for the all-jobs count and exactly-once for the colliding aliases, because master genuinely appears twice in the plan (push line + the main-keep notice prose) and a town alias name can repeat inside ladder/rotations cell re-spelling proposals — prose echoes, not a second fate section, and the hole this closes is absent-names, which at-least-once catches exactly.
<!-- THOUGHT:END -->

## Agent Notes
Closed the yield coherence hole: all 6 post/seat aliases now appear exactly once as named 'duplicate of <canonical>; left to --delete-old' routing lines (no rename onto an owned target, no push); 8-push set unchanged, refs byte-identical, no plan file; added collision fixture + a count-over-all-jobs coherence test. 53 tests pass.

PARENT REVIEW (a00-7a20d346, L4.339): ACCEPTED, verdict stays proved. Verified independently against the built bytes: real-tree `branch-reshuffle --dry-run --kinds main,towns,posts,loops` rc 0, header "v3 YIELD active (declared town set)", exactly 8 branch-push lines (master:season1/main, season2/main, core/main, core/season2/main, streaming-suite/main, streaming-suite/season1/main, web-app-suite/main, web-app-suite/season1/main), 6 "legacy post <old> -> duplicate of <new>; left to --delete-old" routing lines (one per alias), 2 legacy-town routing lines. Independent coherence check: cli._reshuffle_jobs returns 328 jobs and 0 old names absent from the plan. 53 tests green. No branch-reshuffle plan JSON written (only the dispatch manifest). The hole I found in Kid A is closed; the at-least-once vs exactly-once deviation is correct for the stated reason (master appears in both its push line and the main-keep prose; ladder/rotations cell proposals echo legacy tokens). Standing deviation kept and documented: assert_remote_visible is scoped to the v3-on pushes, not the preserved v3-off town-less stream — the target itself permits the old season-first-only behaviour there and the header says the yield is inert.
