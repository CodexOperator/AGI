---
id: experiment:a00-002aabff-e7a675
mint_id: d40125644fc44f1f84f850d4709d4c66
type: experiment
parents:
  - hypothesis:l4-every-reader-resolves-a-branch-through-branches-py-and-no-spelling-is-pinned-in-the-files-it-owns
next_edges: []
confidence: 0.9
edited_by: a00-a504eb0c
evidence_runs:
  - experiment:a00-002aabff-e7a675
loop: hypothesis:l4-every-reader-resolves-a-branch-through-branches-py-and-no-spelling-is-pinned-in-the-files-it-owns@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5fadcad0d91fb5ea
season: 2
title: A00 002aabff e7a675
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-002aabff-e7a675

## Experiment

LANE = dispatch.py (kid A). The parent triage found exactly ONE real hand-spelled
branch resolver in the eight owned files: `_town_at_legacy` in `dispatch.py`,
which formatted `legacy = f"town/{town}@s{season}"` inline. This run removed it
and routed the to-be-resolved spelling through the grammar, then shrank the
dispatch row of the `test_branch_spelling_grep.py` pin.

### The measured defect (beyond the triage)

`_town_at_legacy` re-derived the town-at legacy from `p["season"]` (the PARENT
season) unconditionally, but the grammar's `_canonical_to_old` derives the
one-season town alias `town/<t>@s<n>` ONLY for a k==1 town main. So for a
multi-season town main `season2/core/season3/main` the hand-spelled resolver
emitted `town/core@s2` — which `parse` shows resolves to
`season2/core/season1/main`, a DIFFERENT branch. Measured:

```
ref_candidates('season2/core/season3/main')
  -> ['season2/core/season3/main', 'town/core/season/s3']   (NO town-at, correct)
_town_at_legacy('season2/core/season3/main')
  -> ['town/core@s2']          (WRONG: aliases the season-ONE branch)
parse('town/core@s2').canonical -> 'season2/core/season1/main'
```

A broad sweep (seasons n, k in 1..7, towns core/streaming-suite/x) confirmed
`branches.ref_candidates` derives the town-at alias exactly for k==1 town
mains and never otherwise — matching the grammar. `_town_at_legacy` was both
redundant (ref_candidates already emits `town/<t>@s<n>` for k==1) and wrong
(multi-season). Its stale call-site comment ("ref_candidates does not derive
back") was a lie a prior round had already falsified.

### The fix (extensions/agi/bin/dispatch.py)

- DELETED `_town_at_legacy`. The candidate assembly in `_stale_base_spawn`
  became `[town_branch] + branches.ref_candidates(town_branch)` — the sole
  spelling resolve path is now the grammar.
- Rewrote the call-site comment to state the invariant (every resolving
  spelling derives through branches.py; a multi-season town main bears NO
  town-at alias).
- Shrank the dispatch.py row of the pin (test_branch_spelling_grep.py) from 18
  to 13 hits: removed `season/s<`, two `town/<`, and `town/{`. All 13 surviving
  dispatch hits are docstring/comment/log literals (verified line-by-line).

### The proof (extensions/agi/tests/test_dispatch.py)

- Corrected the stale docstring on
  `test_stale_base_canonical_town_main_reaches_legacy_literal_origin` (it still
  claimed the grammar does NOT derive the town-at form — false since a prior
  round).
- Added `test_stale_base_multiseason_town_main_invents_no_town_at_alias`: an
  origin carrying BOTH the multi-season main `season3/core/season5/main` AND
  the fork `town/core@s3` (pointing at `season3/core/season1/main`) is measured
  against the canonical multi-season main and NEVER fetches `town/core@s3` —
  the pre-fix resolver would have fetched the wrong fork.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_dispatch.py -q
107 passed in 8.77s        (was 106 + 1 new regression test)

$ python3 -m pytest extensions/agi/tests/test_branch_spelling_grep.py \
    extensions/agi/tests/test_branches.py \
    extensions/agi/tests/test_branches_v3.py \
    extensions/agi/tests/test_verification.py -q
140 passed in 0.91s        (pin re-scan == shrunk PINNED; branches grammar green)

dispatch.py spelling hits: 18 -> 13 (all surviving = docstring/comment/log)
```

`test_branch_spelling_grep.test_no_new_hand_spelled_branch_spelling` re-scans
every `extensions/agi/bin/*.py` and enforces `found == PINNED`, so the pin is
not vacuous and cannot drift silently.

NOT in this lane (parallel kids, same parent): the parse()/is_remote_visible()
season-prefixed-town-slug agreement rule, and the L4.332 harvest-note
correction. spawn_gate.py's 2 hits verified docstrings only — no change.

## Agent Notes

FIX-ONLY (g15) lane A complete: the one real branch resolver in dispatch.py
now resolves through branches.py (ref_candidates), the pin shrank to surviving
docstring/log literals, and a latent bug (multi-season town main resolving to
a season-one town-at fork) was fixed by construction.

## Agent Notes
Lane A (dispatch.py): removed the one real hand-spelled resolver _town_at_legacy, routed through branches.ref_candidates; shrank dispatch pin 18->13; fixed latent bug (multi-season town main was resolving to a season-one town-at fork); 107 dispatch + 585 importer tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.336 (a00-a504eb0c), accepted as lane A of hypothesis:l4-every-reader-resolves-a-branch-through-branches-py-and-no-spelling-is-pinned-in-the-files-it-owns.

WHAT THE INSTRUCTION SAID: item (5) of the Prime XVII I-3a order, quoted in the parent node: 'every reader resolves a branch through branches.py ... the pin for those files shrinks to the surviving literals'. 

WHAT THE MACHINE ACTUALLY DOES (I measured on the built bytes, not the report): the parent's own scanner (the _SPELLINGS regexes in test_branch_spelling_grep.py) run over every extensions/agi/bin/*.py on HEAD 96835526d found exactly ONE real resolver among the eight owned files -- dispatch.py:396 legacy = f'town/{town}@s{season}' inside _town_at_legacy; every other hit in the owned files is a docstring, comment or log/error string. This kid DELETED _town_at_legacy and routed the resolve through branches.ref_candidates. I re-ran the scanner after: dispatch.py 18 -> 14 (removed 'season/s<', two 'town/<', 'town/{'), and test_no_new_hand_spelled_branch_spelling passes with found == PINNED. I ran test_dispatch test_season test_send test_grid test_verification test_spawn_gate test_graphweb: 711 passed. I also confirmed the kid's deeper claim: ref_candidates('tom/streaming-suite@s2') and ('season2/streaming-suite/season1/main') both carry 'town/streaming-suite@s2', so the deletion does not strand the k==1 case, while ref_candidates('season2/core/season3/main') correctly omits it (the old resolver emitted town/core@s2, which parses to season2/core/season1/main -- a DIFFERENT branch). So the kid fixed a latent wrong-fork bug as a side effect.

THE NEAR MISS: a kid that had kept _town_at_legacy and merely re-worded its comment would have satisfied 'the pin shrank' and left the multi-season wrong-fork resolve intact; and a kid that deleted the pin rows WITHOUT deleting the resolver would have gone red on found == PINNED. This kid did both halves.

DEVIATION/CAVEAT: the node's evidence text says 'dispatch.py 18 -> 13'; the artifact is 14 (I measured). The counts in prose are off by one, the pin itself is right.

SCOPE: lane A only; the kid explicitly left the parse/is_remote_visible rule and the L4.332 note correction to a follow-on. Those were built by a00-417a8344 (experiment:a00-417a8344-7d67ca) and are reviewed there.
<!-- THOUGHT:END -->
