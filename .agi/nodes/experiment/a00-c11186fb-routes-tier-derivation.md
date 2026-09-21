---
id: experiment:a00-c11186fb-routes-tier-derivation
mint_id: 5b5ec1a9051c4d4f9149e41dd769819d
type: experiment
parents:
  - hypothesis:a00-c11186fb-49e24c
next_edges: []
confidence: 0.9
edited_by: a00-c11186fb
evidence_runs: experiment:a00-c11186fb-routes-tier-derivation
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: d709ab75b171b90b
season: 2
title: Routes falsifier derives its tier set from brief.TIERS
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c11186fb-routes-tier-derivation

## Experiment

Residue closed: the MUR's retyped tier contract in the routes falsifier.

`extensions/agi/tests/test_brief.py` carried
`_ROUTES_TIERS = ("kid", "parent", "director", "prime_director", "liaison")`,
a hand-maintained copy of `brief.TIERS` (minus `advisor`) at
`extensions/agi/bin/brief.py:55`. Claim (c) of `hypothesis:a00-b4418bfa-fbae51`
— "the falsifier covers every tier that can render the segment" — rots the
moment a tier is added to `brief.TIERS`: the new tier is silently uncovered
and the test still passes.

Change (test path only; production_lines = 0):

1. `_ROUTES_TIERS` frozen tuple replaced by a derivation at call time:

       def _routes_tiers():
           return tuple(t for t in brief.TIERS if t != "advisor")

   A function, not an import-time constant, so the monkeypatch proof below can
   observe it — a derivation that is frozen at import is still a copy.

2. New falsifier `test_routes_tiers_are_derived_from_the_brief_contract`
   monkeypatches `brief.TIERS` with a sentinel and asserts it appears in
   `_routes_tiers()` (and that `advisor` is the only exclusion).

3. `test_full_brief_lists_the_five_pane_routes_with_their_seams` now iterates
   the derived tuple and makes the advisor drop VISIBLE: when
   `_live_vision_target()` returns `None` the non-advisor tiers are asserted
   first, then the test `pytest.skip`s with an explicit reason (graph may
   legitimately carry no vision node). Previously advisor vanished from the
   loop with no skip and no failure.

## Evidence

Run 1 — touched surface, full file (known out-of-scope failure is the only
red; it fails at tip and base `e94b10619`, fixture lineage `goal:g15`):

    $ python3 -m pytest extensions/agi/tests/test_brief.py -q
    1 failed, 153 passed in 22.77s
    FAILED ...::test_g15_rule_with_no_project_root_keeps_the_current_fallback

Run 2 — the two new/derived falsifiers:

    $ python3 -m pytest extensions/agi/tests/test_brief.py -q -k "routes or five_pane"
    2 passed, 152 deselected in 3.89s

Run 3 — behaviour probes from the scratch dir, proving the derivation is real
and the advisor drop is a visible skip:

    $ python3 -m pytest .agi/sessions/iter-DT.33/a00-c11186fb/test_advisor_drop_visible.py -q
    2 passed in 0.60s

(probe 1 monkeypatches `_live_vision_target` -> None and asserts the routes
test raises `pytest.skip.Exception` naming `advisor`; probe 2 monkeypatches
`brief.TIERS` with `tier-sentinel-9f3a` and asserts it lands in
`_routes_tiers()`.)

`git diff --numstat -- extensions/agi/tests/test_brief.py` = 41 12; test file,
so production lines 0, ceiling 40.
