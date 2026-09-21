---
id: experiment:a00-e0776cd1-9c1fd7
mint_id: 4d0b40a4a4874af7ab79a72b0cbd3ee3
type: experiment
parents:
  - hypothesis:l3-dispatch-role-default
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-e0776cd1-9c1fd7
loop: hypothesis:l3-dispatch-role-default@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: dad3efd92865d1f8
season: 2
title: A00 e0776cd1 9c1fd7
verdict: proved
---
# experiment:a00-e0776cd1-9c1fd7

## Experiment

**Claim under test (hypothesis:l3-dispatch-role-default):** `dispatch.py --role`
defaulted to `kid` whatever `--tier` said, so a director's bare `--tier parent`
spawn resolved through `resolve_role_spec` the **tier-0 kid row** and loaded the
deepseek kid model instead of the parent model. The fix: derive the default
role from `--tier` when `--role` is not given (tier parent ⇒ role parent, tier
kid ⇒ role kid), with an explicit `--role` still winning, and a red-first test
pinning the mapping.

**What I did:**

1. **Red first** — added two failing tests to `extensions/agi/tests/test_dispatch.py`:
   - `test_default_role_follows_tier` — `_default_role_for_tier("parent")=="parent"`,
     `"kid"→"kid"`, `"prime_director"→"prime_director"`.
   - `test_parent_tier_without_role_resolves_parent_row` — resolving the role
     that `_default_role_for_tier("parent")` returns against the roles table
     must yield the tier-1 parent row (`~z-ai/glm-flash-latest`), NOT the tier-0
     kid model (`~deepseek/deepseek-v4-flash-latest`).
   
   Confirmed **red**: `AttributeError: module 'agi_dispatch' has no attribute
   '_default_role_for_tier'` on both.

2. **Fix** in `extensions/agi/bin/dispatch.py`:
   - Added `_default_role_for_tier(tier)` returning `tier or "kid"`.
   - Changed `--role` argparse default from `"kid"` to `None`, and in `main()`
     after `parse_args`: `if args.role is None: args.role = _default_role_for_tier(args.tier)`.
   - Updated the `--role` help text to say the default derives from `--tier`.

3. **Green** — ran the two new tests only: 5 passed. Ran full `test_dispatch.py`
   suite: **44 passed** (including the pre-existing `--list-rows`, ladder-row,
   and config-fallback tests — none regressed).

4. **Repo suite** — `python3 -m pytest extensions/agi/tests/ -q`: 1766 passed,
   1 skipped, **1 failed** (`test_ladder_node.py::test_ladder_node_current_season`
   asserts `current_season == 1` but the ladder node now holds `2`). This failure
   is **pre-existing and unrelated** to the dispatch change — the ladder's
   `current_season` advanced after the test was written. My dispatch change does
   not touch season.

## Evidence

**Red run (before fix):**
```
FAILED extensions/agi/tests/test_dispatch.py::test_default_role_follows_tier
FAILED extensions/agi/tests/test_dispatch.py::test_parent_tier_without_role_resolves_parent_row
E   AttributeError: module 'agi_dispatch' has no attribute '_default_role_for_tier'
```

**Green run (after fix), targeted:**
```
5 passed, 39 deselected in 0.07s
```

**Full dispatch suite:**
```
44 passed in 0.48s
```

**`--list-rows` unchanged** — the dry runner still prints all 7 declared rows,
including `tier=1 role=parent harness=pi model=~z-ai/glm-flash-latest` and
`tier=0 role=kid model=~deepseek/deepseek-v4-flash-latest`.

**`--role --help` now reads:**
```
--role ROLE  Ladder role to spawn (kid|parent|director|prime_director);
             resolved against the ladder's roles table (default: derived from
             --tier, so a parent tier means role parent)
```

**Not run:** a live `dispatch --tier parent` spawn (would mint provisioning keys
and spawn paid agents). The unit test `test_parent_tier_without_role_resolves_
parent_row` exercises the exact resolution path (`_default_role_for_tier` →
`_default_tier_for_role` → `resolve_role_spec`) the live dry dispatch would take,
which is the mechanism the VERIFY asks about.

## Agent Notes
dispatch --role now derives from --tier (parent tier -> role parent), so a bare --tier parent resolves the tier-1 parent row (glm) not the tier-0 kid deepseek model; explicit --role still wins. Red-first tests added; 44 dispatch tests pass. Repo suite: 1 pre-existing unrelated failure (test_ladder_node season 2 vs expected 1).

REVIEW(parent a00-dcf8a1e4) ACCEPT proved. Read artifact, not report: dispatch.py diff adds _default_role_for_tier(tier)=tier or "kid", wire main() to set args.role from args.tier when --role is None; explicit --role still wins. resolve_role_spec then sees role=parent, tier_eff=_default_tier_for_role("parent")=1 -> tier-1 glm-flash-latest row, never the tier-0 deepseek kid row. Red-first tests confirmed (AttributeError before fix). Ran repo: 44/44 test_dispatch pass, green; --list-rows intact (parent=glm tier1, kid=deepseek tier0). Only repo-suite failure test_ladder_node_current_season (season 1 vs 2) is pre-existing and unrelated to dispatch. parents links exist; evidence_runs cites existing node. No evidence_gate bypass. Proved is warranted.
