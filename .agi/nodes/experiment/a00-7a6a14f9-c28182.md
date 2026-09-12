---
id: experiment:a00-7a6a14f9-c28182
mint_id: 67c097cdd9c34baf99f8cd2002f04f67
type: experiment
parents:
  - hypothesis:l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling
next_edges: []
confidence: 0.95
edited_by: a00-5103312c
evidence_runs:
  - experiment:a00-7a6a14f9-c28182
loop: hypothesis:l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c10c9b3396e34eab
season: 2
title: A00 7a6a14f9 c28182
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7a6a14f9-c28182

L4.322 KID B — `extensions/agi/bin/branches.py` `ref_candidates` only. Build
order on
hypothesis:l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling
(g15 claim, not a measurement). SIBLING KID A owns cli.py; untouched. I own
branches.py (`ref_candidates`, `_canonical_to_old`) + test_branches.py only.

## Defect measured

At 11:59Z before the edit:
`ref_candidates('post/sanctuary-director@s2')` ->
`['season2/posts/sanctuary-director', 'seat/sanctuary-director@s2']` — the
INPUT spelling `post/sanctuary-director@s2` was DROPPED from its own list.
`ref_candidates('post/foo@s2')` (in-process) ->
`['season2/posts/foo', 'seat/foo@s2']`. Cause: `ref_candidates` computed the
one legacy fallback via `_canonical_to_old(canonical, legacy_seat=True)` (the
`seat/` spelling) and returned `[canonical, seat]` — never the INTERMEDIATE
`post/<n>@s<n>` that the input itself wears. At the rename mid-point
(post-rename --apply done, reshuffle --apply and --delete-old not yet) a
reader handed the live `post/` name never tried it.

## What I changed (branches.py ONLY)

`ref_candidates` now builds THREE candidates and dedupes, in order:
(1) canonical `season<n>/posts/<n>`, (2) the INTERMEDIATE as-written
`post/<n>@s<n>` (`_canonical_to_old(canonical)`), (3) the legacy deprecated
`seat/<n>@s<n>` (`_canonical_to_old(canonical, legacy_seat=True)`). A tiny
order-preserving dedupe (`if cand is None or cand in out: continue`) drops
duplicates. The as-written input always appears because it IS one of the
three spellings for every input kind. For main/loop/town the intermediate and
legacy spellings are the SAME old name, so dedupe collapses them to one —
those lists are bit-identical to before. Returns `[canonical]` when no legacy
spelling exists (unchanged).

This is the explicit, per-case-safe form the near-miss warned about: no
`[canonical] + [input] + [legacy]` hand-assembly that can forget a case, and
the dedupe is tested for each of the three spellings plus the main/loop/town
collapse.

## Tests (test_branches.py)

* Updated `test_ref_candidates_post_keeps_legacy_seat_alias` and
  `test_ref_candidates_seat_alias_canonical_first` to the three-element
  [canonical, intermediate, legacy] lists.
* NEW `test_ref_candidates_post_input_keeps_as_written_spelling`
  (parametrized over all three input spellings) asserts: input in list,
  exact `['season2/posts/foo','post/foo@s2','seat/foo@s2']`, canonical first,
  legacy last, list unique.
* main/loop/town assertions UNCHANGED and green.

## Proof

`python3 -m pytest extensions/agi/tests/test_branches.py -q` -> **53 passed**
(pre-fix would have had 52; +1 parametrized test, 3 cases).

In-process probe (repo root):
```
python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); import branches; print(branches.ref_candidates('post/foo@s2')); print(branches.ref_candidates('season2/posts/foo')); print(branches.ref_candidates('seat/foo@s2'))"
['season2/posts/foo', 'post/foo@s2', 'seat/foo@s2']
['season2/posts/foo', 'post/foo@s2', 'seat/foo@s2']
['season2/posts/foo', 'post/foo@s2', 'seat/foo@s2']
```

## Evidence

Raw output, screenshots, logs.

## Agent Notes
branches.py ref_candidates keeps as-written input: canonical + intermediate post/<n>@s<n> + legacy seat/<n>@s<n>, deduped, for all three post spellings; main/loop/town unchanged (inter==legacy collapse to one). 53 tests pass; in-process probe shows identical triple for all three inputs.

Parent review L4.322 (a00-5103312c): accepted proved. Read the artifact -- ref_candidates builds (canonical, inter, legacy) with order-preserving dedupe and returns out or [canonical]. Parent re-ran test_branches.py: 53 passed; merged round pytest test_branch_reshuffle.py + test_branches.py + test_cli.py: 95 passed. Parent probe: all three post spellings return exactly [season2/posts/foo, post/foo@s2, seat/foo@s2]; main and loop collapse to one old name, unchanged. Evidence is the run itself; verdict stands.
