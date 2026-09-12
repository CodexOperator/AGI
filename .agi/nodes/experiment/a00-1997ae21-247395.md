---
id: experiment:a00-1997ae21-247395
mint_id: 3be48f945b674994accebd9bfd231369
type: experiment
parents:
  - hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-pair-per-level-reaches-origin
next_edges: []
confidence: 0.72
edited_by: a00-6e5b8ea4
evidence_runs:
  - experiment:a00-1997ae21-247395
loop: hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-pair-per-level-reaches-origin@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a5d30ea5770632f0
season: 2
title: A00 1997ae21 247395
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1997ae21-247395

## Experiment
Region D (sections 1 + 2) of the L4 round. Built, measured pre-fix, proved on the built bytes.

## 1. ref_candidates resolves the v3 TOWN-FIRST names

MEASURED PRE-FIX GAP (confirmed, the assignment's claim is true): `parse("core/season2/main")` RAISED `unrecognised branch name`, so `ref_candidates("core/season2/main")` returned `["core/season2/main"]` alone — a reader handed a v3 name had NO season-first fallback while the live tree still carries season-first spellings.

FIX in branches.py:
- parse() now recognises the four v3 TOWN-FIRST shapes as NEW kinds (`v3_town_main`, `v3_town_season_main`, `v3_post`, `v3_loop`), reached only when parts[0] is NOT a season prefix, so no existing season-first kind/behaviour changed (`kind == "main"` contract for is_legal_branch / verification intact).
- new `_v3_season_first(parsed)` maps each v3 record onto the season-first spelling(s) a live (not-yet-renamed) tree may still carry, from the SAME ONE tuple: `<town>/season<m>/...` -> `season<m>/...` with the town dropped for posts/loops.
- ref_candidates() appends, for a v3 input, the as-written spelling FIRST (already the rule), then the season-first spelling(s), then each of THEIR one-season aliases, deduped.

Derived answers (verified):
- `ref_candidates("core/main")` -> `["core/main"]`. A bare v3 town main carries NO season number; inventing a parent/town season would be a guess, and no season-first branch is implied by a season-less name. Documented rather than invented.
- `ref_candidates("core/season2/main")` -> `["core/season2/main", "season2/core/season2/main", "town/core/season/s2"]` (the tuple's ONE season fills both parent and town season of the season-first town main).
- `ref_candidates("core/season2/posts/p/main")` -> `["core/season2/posts/p/main", "season2/posts/p", "post/p@s2", "seat/p@s2"]`.
- `ref_candidates("core/season2/posts/p/loops/L4.332/a00-x")` -> `["core/season2/posts/p/loops/L4.332/a00-x", "season2/loops/L4.332-a00-x", "loop/L4.332-a00-x@s2"]` (round/agent rejoin with a dash in the season-first loop spelling).

Byte-identical invariant pinned: EVERY existing season-first input's candidate list unchanged (existing test_ref_candidates_every_input_kind_in_own_list and the v3 regression tests still pass).

is_remote_visible cross-check: every candidate a reader would push is honestly classified — season-first town main `season2/core/season2/main` and season-first `season2/posts/p` are is_remote_visible FALSE (the v3 ruling), asserted rather than hidden.

## 2. The grep test (durable artifact)

Grep every extensions/agi/bin/*.py for a HAND-SPELLED branch SPELLING (season<n>/..., season/s<n>, town/..., post/...@s, loop/...@s) OUTSIDE branches.py. FULL INVENTORY (file:line) — the finding:

cli.py: 2018 2046 2098 2100 2321 2359 2360 2383 2574 2575 3241 3451
dispatch.py: 227 229 253 257 290 292 298 374 376 396 429 434 435 451 454 1309 2694
graphweb.py: 627
grid.py: 861
heal.py: 497 527
rotate.py: 42 225 231 233 241 249 251 571 600 10648 10649
season.py: 1455 1497 1522 1620
send.py: 3586
spawn_gate.py: 637 678
verification.py: 231
(52 lines, 10 files. `master` constant token excluded: it has no derivable spelling to centralize. Sample literals: dispatch.py:451 `season2/<town>/season1/loops/...`, rotate.py:10648 `season2/<town>/season1/loops/...`, season.py:1457 `^loop/.+-[0-9a-fA-F]{8}@s\d+$`.)

TRIAGE per hit: all are (i) resolvers or (ii) genuine non-resolver literals, but EVERY one lives in a FROZEN file this round (dispatch/rotate/heal/season/send/spawn_gate/grid) or in cli.py's reshuffle/prune regions owned by kids 2/3, or in verification.py:231 which is a DOCSTRING, not a resolver (verification already routes `_integration_branch_candidates` through branches.ref_candidates — confirmed). So NO hit is fixable this round without rewriting a frozen reader; the rename that flips them is a later Prime-only pass while the owner holds the tree. The test pins the exact (file, line) inventory so a NEW hand-spelled shape FAILS and a shrink of the debt is visible, not silently accepted. Docstring states the frozen list is debt, not a licence.

## 3. Validate

Behaviour preserved: existing season-first tests byte-identical (131 branch/reshuffle tests). New tests green.

Commands run (exact summary line):
  python3 -m pytest extensions/agi/tests/test_branches.py extensions/agi/tests/test_branches_v3.py extensions/agi/tests/test_branch_reshuffle_v3.py extensions/agi/tests/test_cli_loop_prune.py -q
  -> 111 passed in 8.38s
  python3 -m pytest extensions/agi/tests/test_branches.py extensions/agi/tests/test_branches_v3.py extensions/agi/tests/test_branch_reshuffle.py extensions/agi/tests/test_branch_reshuffle_v3.py extensions/agi/tests/test_cli_loop_prune.py -q
  -> 135 passed in 36.60s
  python3 -m pytest extensions/agi/tests/test_verify_unified.py extensions/agi/tests/test_branch_reshuffle.py extensions/agi/tests/test_branch_spelling_grep.py -q
  -> 52 passed in 20.35s
  New: extensions/agi/tests/test_branch_spelling_grep.py (grep pin), +6 tests in test_branches_v3.py (v3 ref_candidates). Grep test verified to detect an injected new spelling.

## Evidence

Grep test detects drift (verified by injecting a temp rogue.py with a `post/rogue@s2` literal — _scan found it and the assertion rejected the changed inventory, then removed).

No --apply, no prune, no ref rename, no git, no edits to cli.py reshuffle/prune or dispatch/rotate/send/heal/season/spawn_gate. Changed files: extensions/agi/bin/branches.py, extensions/agi/tests/test_branches_v3.py, extensions/agi/tests/test_branch_spelling_grep.py, this node.

## Agent Notes
ref_candidates now resolves v3 TOWN-FIRST names (season-first fallback + aliases); grep test pins the frozen hand-spelled-spelling inventory; season-first byte-identical

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-6e5b8ea4, L4.332, kid 4/4). ACCEPTED, verdict kept proved, confidence kept 0.72 (the kid's own number; I agree it is the weakest of the four because its central change is a grammar widening in the file three earlier kids had been told to hold still). I verified the two claims that matter myself, on the built bytes. (1) The v3 bridge: `branches.ref_candidates` now returns, for the four v3 inputs — core/main -> ["core/main"]; core/season2/main -> [itself, season2/core/season2/main, town/core/season/s2]; core/season2/posts/p/main -> [itself, season2/posts/p, post/p@s2, seat/p@s2]; core/season2/posts/p/loops/L4.332/a00-x -> [itself, season2/loops/L4.332-a00-x, loop/L4.332-a00-x@s2]. As-written input first, then the season-first spelling, then the aliases, deduped — the ONE resolver now resolves both grammars, which is what the live invariant asks for, and it does it in branches.py instead of rewriting seven frozen readers. (2) The live invariant itself: every existing season-first input returns EXACTLY its previous list (season2/main -> [season2/main, season/s2]; master -> [season1/main, season/s1, master]; season2/posts/p -> [season2/posts/p, post/p@s2, seat/p@s2]; town/core@s2 -> [season2/core/season1/main, town/core/season/s1, town/core@s2]) and `is_legal_branch` still accepts season2/main and master and still refuses core/main, core/season2/main, season2/posts/p and core/season2/posts/p/main. I also ran 621 tests across branches.py's actual importers (test_dispatch, test_season, test_send, test_verification, test_grid, test_heal) — all pass, which is the evidence the widening did not leak into a reader. (3) The grep artifact is NOT vacuous: test_branch_spelling_grep.py asserts an exact (file,line) inventory, plus `assert total >= 40` and `assert PINNED`, and the kid verified drift detection by injecting a rogue `post/rogue@s2` literal. Caveat I am recording rather than hiding: the inventory is 52 lines in 10 files and the test passes by PINNING them, so the round has frozen the hand-spelled debt, not removed it — that is the honest outcome while the owner holds the rename, and the test docstring says so. NEAR MISS I checked: a v3 parser reached through the season-first branch and silently reclassifying `kind` — parse() reaches the v3 kinds only when parts[0] is not a season prefix, and is_legal_branch (which keys on kind == "main") is unchanged on every input I probed. NON-BLOCKING NOTE on the kid's derived answer for `core/main`: it refuses to invent a season and returns [core/main] alone. That is right — a bare v3 town main carries no season, and the alternative (guessing season1) would have been a fabrication.
<!-- THOUGHT:END -->
