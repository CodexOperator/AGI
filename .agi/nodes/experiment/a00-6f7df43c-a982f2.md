---
id: experiment:a00-6f7df43c-a982f2
mint_id: 6ffc6c86dac541f4aca40a50b95bfdc1
type: experiment
parents:
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
confidence: 0.88
edited_by: a00-325f2fa0
evidence_runs:
  - experiment:a00-6f7df43c-a982f2
loop: hypothesis:l4-branches-follow-the-season-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1aa0e7cee54a1b7b
season: 2
title: stale-base integration resolves legacy origin
town: core
verdict: inconclusive_lean_proved:88
---
# experiment:a00-6f7df43c-a982f2

## Experiment

KID B of the four-kid FIX-ONLY round on hypothesis:l4-branches-follow-the-
season-grammar — the stale-base integration-branch resolution in dispatch.py.

MEASURED DEFECT (reproduced by the round's own spawn): `_stale_base_spawn`
took the `if town_branch:` path and built `_ref_candidates = [town_branch]` —
the canonical name ALONE, with no deprecated-alias fallback (the `else` path
below it DID call `branches.ref_candidates`). On a pre-migration tree
`origin/season2/main` does not exist, the `git fetch origin season2/main`
failed, `integration` stayed None and the guard returned `{"status":
"unchecked"}` — FAIL-OPEN for every nested spawn until the live rename. A
canonical town branch from `_current_town_branch` (= `branches.merge_target`
of a town post/loop) hit the same wall.

FIX (dispatch.py only — branches.py, cli.py, heal.py, crons.py untouched):
route `town_branch` through `branches.ref_candidates` and take the first
candidate that resolves on origin. Because the ladder may hand us a branch
that is ALREADY a legacy literal, and because a town main carries a SECOND
legacy spelling (`town/<t>@s<N>`) that `branches.ref_candidates` does NOT
derive back (it derives `town/<t>/season/s<k>`), the candidate list is
built as: as-written name + `ref_candidates(town_branch)` + the extra
`_town_at_legacy(...)` literal, order-preserving-deduped. Canonical-first,
legacy names included, first fetch success wins. Fail-open preserved: an
unreachable origin is still `unchecked`; only a resolvable old name is not.
(`_current_town_branch` needed no change — it already returns the right value.)

TESTS (extensions/agi/tests/test_dispatch.py), hermetic fixture repos sharing
one `_origin_bare` helper (bare clone pruned to carry ONLY named refs):
  (1) test_stale_base_loop_resolves_only_legacy_origin — origin carrying ONLY
      `season/s2`; spawner on a canonical core post/loop; `_current_town_branch`
      resolves `season2/main`; the stale guard reads `behind` by exactly 1,
      NEVER `unchecked`. This is the regression this round exists for.
  (2) test_stale_base_both_names_fetches_canonical_first — origin carrying
      BOTH names; asserts `origin/season2/main` materialises as a
      remote-tracking ref and `origin/season/s2` does NOT (canonical fetched,
      legacy never consulted once the first resolves).
  (3) test_stale_base_canonical_town_main_reaches_legacy_literal_origin —
      town_branch supplied as the canonical town main
      (`season2/streaming-suite/season1/main`) against an origin carrying only
      the literal `town/streaming-suite@s2`; resolves (current), never
      `unchecked`, and the legacy literal ref is fetched.

## Evidence

`env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_dispatch.py -q`
-> 106 passed in 7.20s   (103 existing + 3 new, all green)

`env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_heal.py -q`
-> 120 passed in 7.01s   (heal.py imports the same branches helper)

Verified `branches.ref_candidates`: a canonical town main yields
`['season2/streaming-suite/season1/main', 'town/streaming-suite/season/s1']`
— NOT the `town/streaming-suite@s2` literal form the real pre-migration tree
carries, which is why the extra `_town_at_legacy` spelling is required.
  (3) test_stale_base_canonical_town_main_reaches_legacy_literal_origin —
      town_branch supplied as the canonical town main
      (`season2/streaming-suite/season1/main`) against an origin carrying only
      the literal `town/streaming-suite@s2`; resolves (current), never
      `unchecked`, and the legacy literal ref is fetched.

## Evidence

`env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_dispatch.py -q`
-> 106 passed in 7.20s   (103 existing + 3 new, all green)

`env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_heal.py -q`
-> 120 passed in 7.01s   (heal.py imports the same branches helper)

Verified `branches.ref_candidates`: a canonical town main yields
`['season2/streaming-suite/season1/main', 'town/streaming-suite/season/s1']`
— NOT the `town/streaming-suite@s2` literal form the real pre-migration tree
carries, which is why the extra `_town_at_legacy` spelling is required.

## Agent Notes
KID B region: _stale_base_spawn now routes town_branch through branches.ref_candidates (+ _town_at_legacy for the town/<t>@sN literal), canonical-first, legacy fallback; 3 hermetic fixture tests + pre-fix suite green (106 + 120 incl heal.py).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID (parent brief L4.312, KID B of 4): route the stale-base integration branch through branches.ref_candidates and take the first candidate that resolves on origin; a fixture whose origin carries ONLY season/s2 must read behind/current, never unchecked; a second fixture with both names must fetch the canonical.
WHAT THE MACHINE ACTUALLY DOES, measured by the parent: the reproduction is the round own spawn line -- "note a00-71ee7ec5 slot=0: freshness of base unchecked (origin/season2/main unreachable); spawn proceeds" -- and the fix lands in `_stale_base_spawn`, NOT in `_current_town_branch`. The parent re-ran the kid bytes: pytest test_dispatch.py -> 106 passed; + test_heal.py -> 120 passed. The three new tests assert behind-by-exactly-1 against a legacy-only origin, canonical-fetched-first when both exist, and the canonical-town-main to town/<t>@s2-literal path.
THE NEAR MISS: patching the CITED function (`_current_town_branch`) would satisfy the instruction wording and lose the mechanism -- that function already returns the correct canonical value; the defect is that `_stale_base_spawn` own `if town_branch:` branch bypassed the alias fallback its `else` branch already called. The kid found the right site by reading the code, not the line number.
DEVIATION, and the residue it leaves: the fix adds `_town_at_legacy`, a small second piece of town grammar inside dispatch.py, because `branches.ref_candidates("season2/<t>/season1/main")` yields only `town/<t>/season/s<k>` and NOT the `town/<t>@s<N>` literal the real pre-migration origin carries. The clean home is `branches._canonical_to_old` / `ref_candidates`; that file is outside this kid region, so the parent records the duplication here rather than re-cutting. Whoever next owns branches.py should widen it to emit BOTH legacy town spellings, after which dispatch.py can delete `_town_at_legacy`.
PARENT REVIEW: accepted at inconclusive_lean_proved:88. The claim is a build order and it is built + fixture-proven; the unproven half is the live tree, which this round may not touch.
<!-- THOUGHT:END -->
