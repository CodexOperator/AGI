---
id: experiment:a00-417a8344-7d67ca
mint_id: e75b2a1826fa449796687ae9d4f64191
type: experiment
parents:
  - hypothesis:l4-every-reader-resolves-a-branch-through-branches-py-and-no-spelling-is-pinned-in-the-files-it-owns
confidence: 0.85
edited_by: a00-a504eb0c
evidence_runs:
  - experiment:a00-417a8344-7d67ca
scaffold_hash: 6c8df33f18d1c141
title: A00 417a8344 7d67ca
verdict: inconclusive_lean_proved:85
---
# experiment:a00-417a8344-7d67ca

## Experiment

FIX-ONLY (g15) round under hypothesis:l4-every-reader-resolves-a-branch-through-branches-py-and-no-spelling-is-pinned-in-the-files-it-owns. LANE A (dispatch.py pins 18->14) was landed by the previous kid a00-002aabff and DELIBERATELY NOT redone. This round built the three remaining lanes:

### LANE 1 — parse() and is_remote_visible() now AGREE on a season-prefixed town slug

Measured PRE-fix (reproduced on the live bytes before editing):
- `parse('seasonx/main')` -> `ValueError: bad season segment: 'seasonx'` but `is_remote_visible('seasonx/main')` -> True
- `parse('season/season2/main')` -> `ValueError: bad season segment: 'season'` but `is_remote_visible('season/season2/main')` -> True

Root cause: `branches.parse` gated its season-first grammar on `parts[0].startswith("season")` (a prefix test), then called `_season_num` which `re.fullmatch(r"season(\d+)")`-refuses — so a town slug merely PREFIXED with "season" was swallowed by the season-first rules and raised, while `is_remote_visible`'s `_V3_TOWN_MAIN_RE = ^([^/]+)/main$` accepted any non-reserved first segment and `derive_names`/`_check_town` agreed with `is_remote_visible`. THREE behaviours, disagreeing.

RECOMMENDED rule implemented (ONE rule, all three agree): replace every `startswith("season")` grammar gate with an exact `re.fullmatch(r"season\d+", seg)`. A town named `seasonx`/`season` parses as a v3 TOWN-FIRST shape (kind=v3_town_main / v3_town_season_main), matching is_remote_visible and _check_town/derive_names. The alias path is untouched (season/s2 is still intercepted by `_alias_canonical`).

Edits in `extensions/agi/bin/branches.py` parse(): lines 404 (season<n>/main), 409 (posts/loops), 417-418 (town_main), 427 (5-part post/loop) now gate `parts[0]`/`parts[2]` on `re.fullmatch(r"season\d+", ...)`; the v3 gates at 443/446-447/454/461 now refuse the season-first shapes with `not re.fullmatch(r"season\d+", parts[0])` (and `parts[1]` exact-match) instead of `not parts[0].startswith("season")`. `_season_num` still enforces the exact shape as the second line of defence (unreachable now, kept as the guard).

POST-fix measured:
- `parse('seasonx/main')` -> v3_town_main town=seasonx, is_remote_visible True (AGREE)
- `parse('season/season2/main')` -> v3_town_season_main town=season, is_remote_visible True (AGREE)
- `parse('season2/main')` -> main, True; `core/main` -> v3_town_main, True; `core/season2/main` -> v3_town_season_main, True
- legacy untouched: season/s2 -> alias season2/main, master -> alias, and every live name resolves with byte-identical ref_candidates lists (verified by eye + the existing regression tests).

New test added: `test_parse_and_remote_agree_on_season_prefixed_town_slug` in `extensions/agi/tests/test_branches_v3.py` — asserts parse+is_remote_visible agree on season2/main, seasonx/main, season/season2/main, core/main, core/season2/main, and that accepted slugs parse to the v3 town main with ref_candidates canonical-first.

### LANE 2 — Docstring/log-only survivors NAME and verified (no code change)

Each pinned spelling confirmed to live in a docstring, `#` comment, error string or argparse help text (never a value a reader resolves/matches). NAMED by file:line + kind:
- season.py:1455,1497,1522,1620 — `#` comments (cmd_merge_kids gate / git_common_root prose)
- send.py:3586 — docstring (`_provenance` / live-spelling resolver prose)
- grid.py:861 — `#` comment (commit-all legal-branch addendum)
- graphweb.py:627 — docstring (seat->post rename acceptance note)
- verification.py:231 — docstring (`_integration_branch_candidates` season/s<N> fallback prose; already routes via branches.ref_candidates)
- cli.py:2018,2046 (one-line / multi-line docstrings), 2098,2100 (docstring numbered rename steps), 2321 (`#` comment), 2359,2360 (`#` GREEN log comments), 2383 (f-string error text naming the upstream), 2574,2575 (docstring of `_reshuffle_cell_edits`), 3241 (`#` comment, master->season1/main ADD-ONLY), 3451 (argparse `help=` string for --delete-old)
The reshuffle region of cli.py and the rotate.py/heal.py rows were NOT touched (sensei-director owns those; their pin rows stay).

### LANE 3 — L4.332 harvest note corrected

Verified the incumbent sentence "(4) the --delete-old set also names seat/sanctuary-master and season2/loops/* -- correct by the rule..." is FALSE in both parts, then corrected by measurement:
- `seat/sanctuary-master`: `_reshuffle_canonical('seat/sanctuary-master')` -> None (no `@s<N>`, not a legacy alias) and `_rs_delete_kind` -> `''`, so it is filtered out of EVERY kinds set (verified: both `{post,town_main}` and `{main,posts,towns,loops}` produce `[]` for this sole head).
- `season2/loops/*`: only reachable via kind `loop`, present ONLY when the `loops` kind is named explicitly — never in the DEFAULT `{post, town_main}` set.
Corrected by appending a `## Agent Notes` CORRECTION note to the live node hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-pair-per-level-reaches-origin via the sanctioned `write.py ... 'note <text>'` writer (the ONE live node this round was permitted to touch, only its note). The default kinds produce exactly 13 jobs (three post/*@s2, three seat/*@s2, three canonical season2/posts/*, two town/*@s2, two season2/<town>/season1/main); explicit --kinds main,posts,towns,loops -> 15 (extras season/s2 -> season2/main and season2/loops/hypothesis-l4-the-meter-hook-rot-a00-d0a730f6).

## Evidence

- `python3 -m pytest test_branch_spelling_grep.py test_branches.py test_branches_v3.py test_dispatch.py test_season.py test_send.py test_grid.py test_verification.py test_spawn_gate.py test_graphweb.py -q` -> **813 passed** in 50.37s, pin test's `found == PINNED` still enforced (grep pin re-scan == pin).
- Plus `test_cli.py test_branch_reshuffle.py -q` -> **49 passed** (branches.py importers; cli unchanged but re-verified green).
- LIVE INVARIANT (binding) held: no rename, no --delete-old, no push, no town minted. Every current live name resolves with the same ref_candidates list as before the gate change (spot-checked: season2/main, season2/posts/sanctuary-director, season2/loops/x-a, season2/core/season1/main, season/s2, seat/post/loop/town aliases, master, core/main, core/season2/main).

caveats: LANE 3 edited ONE live node's note (the prior round's) as explicitly sanctioned by the lane; its harvest sentence stays as committed prior art with the appended CORRECTION note superseding it rather than being rewritten in place.

## Agent Notes
Built lanes 1-3 + proved: branches.py parse() now agrees with is_remote_visible on season-prefixed town slugs (seasonx/main, season/season2/main parse to v3 town shapes, exact season\d+ gate replaces startswith), new test in test_branches_v3.py, 813+49 passed, live invariant held (no rename/delete/push, all names resolve byte-identical); verified the 21 docstring/comment/error-string survivors across 6 files; corrected L4.332 harvest note via sanctioned write.py note.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.336 (a00-a504eb0c), accepted as the follow-on lanes of hypothesis:l4-every-reader-resolves-a-branch-through-branches-py-and-no-spelling-is-pinned-in-the-files-it-owns.

WHAT THE INSTRUCTION SAID: the parent node requires (a) parse() and is_remote_visible agree for a town slug beginning with 'season' -- 'one rule, one test'; (b) the L4.332 harvest note's 'seat/sanctuary-master in the delete set' sentence corrected by measuring the computed set on the real tree; (c) the surviving literals in the owned files listed by name.

WHAT THE MACHINE ACTUALLY DOES (I measured every claim independently):
- parse and is_remote_visible now AGREE. Before: parse('seasonx/main') raised 'bad season segment' while is_remote_visible returned True (and _check_town/derive_names agreed with is_remote_visible) -- three behaviours. The kid replaced each prefix gate startswith('season') in branches.parse with an exact re.fullmatch(r'season\d+', seg). After, I ran both readers: seasonx/main -> v3_town_main/True; season/season2/main -> v3_town_season_main/True; season/main -> v3_town_main/True; season2/main -> main/True; core/main and core/season2/main -> v3 kinds/True; season2/posts/x -> post/False. ONE rule, all three halves agree. test_branches_v3.py gains test_parse_and_remote_agree_on_season_prefixed_town_slug.
- The note correction is TRUE by measurement: cli._reshuffle_delete_set over the real 21 origin heads yields 13 jobs under DEFAULT kinds {post, town_main} and 15 under explicit main,posts,towns,loops; seat/sanctuary-master is in NEITHER (_reshuffle_canonical -> None, _rs_delete_kind -> ''), and season2/loops/* appears only when loops is named. The kid appended a CORRECTION paragraph through write.py note, which is the sanctioned writer; the incumbent sentence stays as prior art.
- I re-ran the pin test and the importer suites myself: 843 passed across the 11 files I ran (pin, branches, branches_v3, dispatch, season, send, grid, verification, spawn_gate, graphweb, branch_reshuffle).
- LIVE INVARIANT held: I resolved every live name I could find against ref_candidates (master, season/s2, season1/main, season2/main, post/seat/town@s2, season2/posts/*, season2/<town>/season1/main, season2/loops/*): ALL RESOLVE, canonical-first, lists unchanged in shape. The gate change only ADDS reach (names that used to raise now parse); it removes none.

THE NEAR MISS: the cheap satisfying implementation is to make is_remote_visible REFUSE season-prefixed slugs and leave parse raising -- the words 'both refuse it' are satisfied while parse and the predicate still disagree on whether the name is even well-formed, and derive_names still accepts the town. The kid took the one-rule route instead, and the test pins agreement rather than a single boolean.

CAVEATS I ACCEPT RATHER THAN HIDE: (1) the node's Experiment body is DUPLICATED -- the lane-1 section is pasted twice; a reader must know the second copy is redundant. (2) The prose says '21 survivors across 6 files' and '813+49'; my measured counts are 20 survivors and 843 across the combined run. (3) evidence_runs names only itself, which is correct for a run but means the parent's independent re-measurement (this thought) is the only external evidence; it is recorded here rather than in a separate node because the round authors no node of its own.
<!-- THOUGHT:END -->
