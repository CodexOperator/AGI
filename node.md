---
id: experiment:a00-f9f1399d-3984ce
mint_id: 8d155da72c48460487f8da882d284f9f
type: experiment
parents:
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
confidence: 0.9
edited_by: a00-325f2fa0
evidence_runs:
  - experiment:a00-f9f1399d-3984ce
loop: hypothesis:l4-branches-follow-the-season-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e48839af257c08c4
season: 2
title: "\"L4.312 KID D: verification.py town-branch read resolves canonical-first (stamp survives the rename) + crons runbook note + town_branches proposal\""
town: core
verdict: proved
---
# experiment:a00-f9f1399d-3984ce

## Experiment

L4.312, KID D of the four-kid FIX-ONLY round on g15 line I (hypothesis:l4-branches-follow-the-season-grammar). My region: verification.py's `_integration_branch` read + the crons runbook note + a PROPOSAL for the Prime's `town_branches` geometry cells. The engine fix lands; the ladder cells are the Prime's and the PROPOSAL is the deliverable for that half.

### (8) verification.py — the readability of the integration-branch read

The defect: `_integration_branch` returned the ladder's `town_branches` value VERBATIM. Today that value is the legacy `season/s2` (ladder.md:59-62), so `_stamp_context` compared `cur != branch` exactly and, the moment the live rename flips the tree to the canonical `season2/main`, the comparison stops matching and the never-lower node-count baseline silently stops stamping.

The fix (extensions/agi/bin/verification.py) routes the read through the season grammar, canonical-first with the legacy spelling as a one-season fallback (branches.ref_candidates), exactly as KID B's `_stale_base_spawn` does on the dispatch side:

  - `_integration_branch_candidates(groot)` reads `town_branches` and returns `branches.ref_candidates(declared)` — `[canonical, legacy]`, or None when no branch is declared.
  - `_integration_branch(groot)` returns `cands[0]` (the CANONICAL name), so the tip label and `origin/<branch>` keep using ONE stable name.
  - `_stamp_context` accepts `cur` if it matches ANY candidate (canonical or legacy), and treats the read as pushed if HEAD is an ancestor of ANY `origin/<candidate>` — so BOTH rename directions stamp: a legacy-declared ladder on a canonical-checked-out tree, and a canonical-declared ladder on a still-legacy tree.
  - the `status` tip line resolves the FIRST candidate whose origin ref actually exists, so a pre-rename tree (pushed only under `origin/season/s2`) still shows a real tip rather than an unresolved canonical.

The season is never hardcoded: `ref_candidates` derives the canonical from whatever the declared value resolves to (goal:g10.2 "never hardcoded").

Tests added to extensions/agi/tests/test_verification_kept_merge.py (fixtures built with a split helper whose declared-ladder branch and checked-out-git branch can DIFFER):
  - legacy declared `season/s2`, tree checked out on canonical `season2/main` -> STAMPS (the defect, flipped and pinned).
  - legacy declared `season/s2`, tree on `season/s2` -> STAMPS (pre-rename steady state, the acquire-while-you-can window).
  - canonical declared `season2/main`, tree on `season2/main` -> STAMPS.
  - canonical declared `season2/main`, tree still on `season/s2` -> STAMPS (the reverse rename window).

### (9) the runbook note (defect the mechanism does NOT touch)

`crons.py` `branch_push` renders the checked-out branch at APPLY time — correct and deliberately unchanged. What was missing is the OPERATOR note: a rename needs one `crons.py apply` within the 5-minute `grid_sync` window, else `branch_push` keeps pushing the old name. Written into the I node body under a `## Runbook` heading via the sanctioned writer.

## PROPOSAL for the Prime — `.agi/nodes/.geometry/ladder.md` `town_branches:`

The cell edits below are the Prime's (the write guard refuses them to an agent). Exact before/after:

```
# BEFORE (ladder.md:59-62)
town_branches:
  core: season/s2
  streaming-suite: town/streaming-suite@s2
  web-app-suite: town/web-app-suite@s2

# AFTER
town_branches:
  core: season2/main
  streaming-suite: season2/streaming-suite/season1/main
  web-app-suite: season2/web-app-suite/season1/main
```

These are the canonical names the grammar module produces (`branches.season_main(2)`, `branches.town_main(2, <town>, 1)`); they match the clause-(5) council `controls` proposal already on the hypothesis node. With the verification.py fix landed, the stamp SURVIVES the flip regardless of which spelling the ladder declares, so the Prime's edit is a clean cut.

## Evidence

Last line of the test file I touched (after the fix):

```
python3 -m pytest extensions/agi/tests/test_verification_kept_merge.py -q
19 passed in 1.06s
```

Union of the files covering my region (verification + the town_branches readers):

```
python3 -m pytest extensions/agi/tests/test_verification_kept_merge.py extensions/agi/tests/test_verification_window.py extensions/agi/tests/test_dispatch.py -q
127 passed in 8.13s
python3 -m pytest extensions/agi/tests/test_season.py extensions/agi/tests/test_spawn_gate.py -q
137 passed in 18.82s
```

(The 19-run was initially caught by test_verification_window's tip test BEFORE I fixed the tip path — that existing test is the guard that kept a canonical-only tip from regressing the pre-rename tree. All green after the tip path also resolves through candidates.)

Sanctioned writer output for the runbook note into the I node body:

```
updated: hypothesis:l4-branches-follow-the-season-grammar
```

Raw output, screenshots, logs.

## Agent Notes
verification.py _integration_branch now resolves canonical-first via branches.ref_candidates (stamp survives the season rename both ways: legacy-declared/canonical-tree AND canonical-declared/legacy-tree); 4 fixture tests; crons runbook note landed under ## Runbook; town_branches BEFORE/AFTER proposal written for the Prime.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID (parent brief L4.312, KID D of 4): "(8) the node-count baseline stops stamping after the rename (ladder.md:60 names season/s2) -- read the season MAIN through branches.season_main / ref_candidates so the stamp survives the flip; (9) crons.py branch_push line bakes the branch name at apply time -- do NOT change the mechanism, write the runbook note ... into the I node body under a `## Runbook` heading via write.py note".
WHAT THE MACHINE ACTUALLY DOES, measured by the parent on the kid bytes: `pytest test_verification_kept_merge.py` -> 19 passed; `verification.py` `_stamp_context` now accepts HEAD on ANY of `branches.ref_candidates(declared)` and treats the read as pushed when HEAD is an ancestor of ANY `origin/<candidate>`; `render_window` tip resolves the first candidate whose origin ref exists; the `## Runbook` paragraph is in the I node body (I read it at the line, not in the report); the `town_branches` BEFORE/AFTER proposal is in the node. `crons.py` itself is byte-unchanged, which was the instruction.
THE NEAR MISS: canonicalising the ladder read to `season2/main` ONLY would satisfy "the stamp survives the flip" in the post-rename direction and BREAK the pre-rename direction -- a tree still on `season/s2` whose ladder now declares the canonical would stop stamping, which is the same defect moved one day forward. The kid accepts BOTH directions and pins all four combinations, which is the property that makes the fix a fix rather than a swap of which side is broken.
DEVIATION: none from the brief; the edit is larger than the minimal diff (86 lines) but stays inside verification.py and its test file.
PARENT REVIEW: accepted at proved-with-caveats; kept at `proved` because the node IS the run, the bytes exist, and the fixture evidence pins all four stamping combinations. CAVEAT: `_integration_branch` (singular) now has NO caller in the tree -- `_integration_branch_candidates` is the live path and the singular survives only as a documented accessor; a follow-up should either delete it or name its caller. Second caveat: this work is green in ISOLATION; the merged-round union suite is owed at merge-up, because the parent may not run git or merge.
<!-- THOUGHT:END -->
