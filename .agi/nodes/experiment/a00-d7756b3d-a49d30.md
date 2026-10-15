---
id: experiment:a00-d7756b3d-a49d30
mint_id: 9a29dad9197849708b39f0efd5119fcd
type: experiment
parents:
  - hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-pair-per-level-reaches-origin
next_edges: []
confidence: 0.95
edited_by: a00-6e5b8ea4
evidence_runs:
  - experiment:a00-d7756b3d-a49d30
loop: hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-pair-per-level-reaches-origin@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 16fda2b490161bcd
season: 2
title: A00 d7756b3d a49d30
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d7756b3d-a49d30

## Experiment

Region A slice: built the two new public v3 TOWN-FIRST functions plus the
refusal-by-name helper in `extensions/agi/bin/branches.py`, and pinned them in
a new `extensions/agi/tests/test_branches_v3.py` (the file did not exist, so
"new file", as the slice allowed). The live SEASON-FIRST functions
(`parse`, `_alias_canonical`, `_ALIASES`, `ref_candidates`, `_canonical_to_old`,
`merge_target`, `is_legal_branch`, `season_main`, `town_main`, `post_branch`,
`loop_branch`) are UNCHANGED — v3 is added alongside, a reader still resolves both.

Added:
- `derive_names(town, town_season, post=None, round=None, agent=None) -> dict`
  derives ALL v3 names from the ONE tuple: town_main `<town>/main`,
  town_season_main `<town>/season<m>/main`, post_main
  `<town>/season<m>/posts/<post>/main` (only when post given), loop
  `<town>/season<m>/posts/<post>/loops/<round>/<agent>` (only when post AND
  round AND agent given). `town` through the module's own `_check_town`
  (RESERVED = main/posts/loops refused); `town_season` int >= 1. Every level
  is a DIR with a `main` leaf (git forbids leaf+dir).
- `is_remote_visible(name) -> bool` — True for EXACTLY master, season<n>/main,
  `<town>/main`, `<town>/season<m>/main`; every sub-top-level shape, a bare
  town, and a non-string/empty name is False. Never raises. Derived from the
  same trunk shapes as the builder (module-level `_SEASON_MAIN_RE` mirrors the
  spell parse()/_canonical_to_old() use; `_V3_TOWN_MAIN_RE`/`_V3_TOWN_SEASON_RE`
  guard towns with RESERVED) — no second hand-spelled shape list.
- `assert_remote_visible(name) -> None` — RAISES ValueError naming the branch
  AND the rule (`<town>/season<m>/posts/<post>/main` is refused by name);
  returns None on a visible branch. The falsifier for "push of any
  sub-top-level name to refs/heads is refused by name".
- All three documented in `__all__`.

### Test hooks (tests/test_branches_v3.py)
(a) `test_derive_names_full_tuple` asserts the exact 4-key dict for
   ("core", 2, "sanctuary-director", "L4.332", "a00-x").
(b) `test_derive_names_partial_inputs` / `_loop_requires_round_and_agent` /
   `_reserved_town_raises` / `_town_season_int_ge1` — 2 keys for (core,2),
   3 for (core,2,post="p"), loop only with post+round+agent, reserved town
   raises, town_season int>=1.
(c) `test_is_remote_visible_true` / `_false` / `_never_raises_on_garbage` —
   True exactly master/seasonN/main/core/main/core/season2/main; False for
   core/season2/posts/x/main, .../loops/L4.332/a00-x, season2/posts/x,
   season2/loops/x-a, bare "core", reserved towns, season/s2, garbage, None.
(d) `test_assert_remote_visible_refuses_and_names_branch` — ValueError message
   contains the branch; `_ok_returns_none`.
(e) `test_regression_season_first_still_parses` / `_ref_candidates_current_name_first`
   — copied/fixed from the existing suite (see struggles).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_branches.py extensions/agi/tests/test_branches_v3.py -q
92 passed in 0.19s
```

File:line anchors added this round:
- extensions/agi/bin/branches.py: `__all__` (derive_names/is_remote_visible/
  assert_remote_visible added); `_SEASON_MAIN_RE`/`_V3_TOWN_MAIN_RE`/
  `_V3_TOWN_SEASON_RE`; `derive_names`; `is_remote_visible`;
  `assert_remote_visible`.
- extensions/agi/tests/test_branches_v3.py: whole new file.

### Measured contradiction (documented, not papered over)
The live SEASON-FIRST town main `season<n>/<town>/season<k>/main` is a real
Council trunk leaf (parse kind == "town_main"), yet `is_remote_visible` returns
False for it — v3 spells the town trunk TOWN-FIRST (`<town>/main`,
`<town>/season<m>/main`), and the predicate as specced recognizes only those.
This round ADDS v3 alongside WITHOUT renaming the live tree, so a season-first
town main still resolves via parse/ref_candidates but is refused by name under
is_remote_visible. Carrying the live tree onto the v3 spelling is the rename
work of a later slice/round — pinned by
`test_measured_contradiction_season_first_town_main_vs_v3_remote` so it cannot
silently drift.

## Agent Notes
v3 TOWN-FIRST grammar built in branches.py: derive_names (one-tuple -> 4 keys), is_remote_visible (exactly master/season<n>/main/<town>/main/<town>/season<m>/main), assert_remote_visible (refusal by name). New tests/test_branches_v3.py (a)-(e) + measured season-first town-main contradiction. 92 passed. Live season-first spellings untouched, v3 adds alongside.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-6e5b8ea4, L4.332, kid 1/4). ACCEPTED, verdict kept proved. I re-ran the probe myself, not the kid's report: derive_names("core",2,"sanctuary-director","L4.332","a00-x") returns exactly the four keys PROOF (a) names, and is_remote_visible is True for exactly master/season2/main/core/main/core/season2/main and False for the post_main, loop, season2/posts/x, season2/loops/x-a, bare "core", season/s2 and "". `pytest extensions/agi/tests/test_branches.py extensions/agi/tests/test_branches_v3.py -q` = 92 passed. Live season-first functions are unchanged (I read branches.py:parse/_alias_canonical/ref_candidates before and after; only __all__ and three new regexes + three new functions were added), so the LIVE INVARIANT holds: a reader still resolves every current name. NEAR MISS I checked for and did not find: is_remote_visible derived from a SECOND hand-spelled shape list beside parse() — it reuses _SEASON_MAIN_RE and two v3 trunk regexes, which is the one-tuple derivation the round exists for. Caveat recorded: the kid's "measured contradiction" (season-first town main resolves via parse but is refused by is_remote_visible) is not a contradiction with the ruling — the ruling lists exactly four remote-visible shapes and season-first town main is not one of them; it is the rename that a later slice owns, and the kid pinned it rather than papering it over, which is the right call. NEXT: kid 2 takes cli.py branch-reshuffle v3.
<!-- THOUGHT:END -->
