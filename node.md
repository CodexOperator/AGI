---
id: experiment:a00-3d83d11b-01d6b3
mint_id: 3ab637b7c6a7418098703a9d1f61bbc8
type: experiment
parents:
  - hypothesis:l4-the-town-create-gate-refuses-what-the-loader-refuses-and-every-vision-id-must-exist
next_edges: []
confidence: 0.95
edited_by: a00-4895b300
evidence_runs:
  - experiment:a00-3d83d11b-01d6b3
loop: hypothesis:l4-the-town-create-gate-refuses-what-the-loader-refuses-and-every-vision-id-must-exist@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: dcae1de263f087f1
season: 2
title: A00 3d83d11b 01d6b3
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3d83d11b-01d6b3

## Experiment

Kid B, FIX-ONLY round on hypothesis:l4-the-town-create-gate-refuses-what-
the-loader-refuses-and-every-vision-id-must-exist. Kid A landed the write.py
create-gate region (untouched here). This slice: the LOADER (towns.py) +
the two vacuous tests.

CHANGE — `extensions/agi/bin/towns.py`:
- (2) `_resolve_visions` now checks every EXPLICIT vision id against
  `_all_vision_ids(root)` (reused, not reinvented) and RAISES TownError
  naming the dangling id and the town. Previously it only checked duplicate
  claims — a typo'd vision id resolved silently.
- (3) `_resolve_visions` counts towns that spell `visions: auto` and refuses
  a SECOND by name ("at most one town may spell `visions: auto`, found
  2 ('core', 'streaming-suite')"). Previously nothing counted AUTO towns.
- (4) `_load_one` wraps the non-int season coercion in try/except and raises
  `TownError("non-integer season refused: town:<slug> season='abc'")`
  instead of the bare `int(season)` ValueError traceback on `season: abc`.
  `season: None` still defaults to 0; int-coercible floats keep working.

CHANGE — two vacuous tests de-vacuumed (brief item 6):
- `test_town_mint_final.py` and `test_town_mint_lines.py`
  `test_why_meaning_the_negative_is_cited_not_duplicated` each replaced
  `assert True` with a real assertion: they read the sibling
  `test_town_mint.py` source and assert the cited
  `test_season_set_is_overridden_at_mint_time` still exists AND its body
  really asserts the season override (`assert`, `== 2`, a `_mint` call) —
  so the citation cannot drift into a name that asserts nothing.

CHANGE — fixtures aligned (existing fixtures were inconsistent with
production): the loader's new existence check exposed that
`test_towns._graph` and `test_town_mint._fixture` minted reporting-suite /
web-app-suite vision ids without creating the vision nodes. Both now create
all five vision nodes (a, b, c, streaming-suite, web-app-suite). No live
town node edited; all new tests use tmp fixtures.

## Evidence

New tests (each proves the refusal fires BY NAME on a fixture):
- `test_towns.py::test_refusal_dangling_vision_id` — core claims
  `vision:ghost` (not in fixture nodes/vision) -> TownError naming
  vision:ghost and core.
- `test_towns.py::test_refusal_second_auto_town` — two towns spell `auto`
  -> TownError naming both.
- `test_towns.py::test_refusal_non_int_season` — `_town_node(..., "abc")`
  -> TownError "non-integer season refused ... town:core" rather than a
  traceback.

Command (touched suites, named files):

    python3 -m pytest extensions/agi/tests/test_towns.py \
        extensions/agi/tests/test_town_schema.py \
        extensions/agi/tests/test_town_mint_final.py \
        extensions/agi/tests/test_town_mint_lines.py \
        extensions/agi/tests/test_town_mint.py -q

Observed tail (32 passed):

    32 passed in 1.32s

Live invariant held: no live town node edited or minted; streaming-suite.md
and web-app-suite.md (reporting/web-app) were read-only fixtures only.

## Agent Notes
Loader (towns.py) refuses dangling explicit vision ids BY NAME (reuses _all_vision_ids), refuses a SECOND visions:auto town BY NAME, and refuses a non-int season as TownError; two vacuous assert-True tests now assert the cited negative really asserts. 32 passed on named suites.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-4895b300 L4.338: accepted, proved stands. WHAT THE INSTRUCTION SAID: the loader "checks every explicit vision id resolves to a live-or-deprecated vision node and refuses a dangling one by name"; "at most ONE town may spell visions: auto -- a second is refused by name"; "a non-int season is refused by name, never a traceback"; and "the two assert-True tests assert the behaviour". WHAT THE MACHINE DOES: read towns.py: _resolve_visions L178-212 computes _all_vision_ids first, counts auto_towns and raises TownError naming both slugs, then raises on a vid not in all_vision_ids; _load_one L128-136 wraps the int coercion in try/except TypeError/ValueError raising TownError. Ran pytest on the five town suites: 32 passed. Ran `python3 extensions/agi/bin/towns.py` on the LIVE tree: three towns, zero refusals. grep for `assert True` in the town tests: zero hits. NEAR MISS: a dangling check written against nodes/vision only, without the deprecated sibling, would pass its fixture and silently refuse a legitimately retired vision on the real tree; the reuse of _all_vision_ids is what keeps live and deprecated in one set. No deviation. One cost noted: the two fixtures had to mint vision nodes they had been asserting about without creating -- existing fixtures were inconsistent with production, which is its own defect worth knowing.
<!-- THOUGHT:END -->
