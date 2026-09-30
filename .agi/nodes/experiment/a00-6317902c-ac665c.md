---
id: experiment:a00-6317902c-ac665c
mint_id: b87e6d334893445aba79c139cea132e2
type: experiment
parents:
  - hypothesis:an-empty-response-budget-counts-consecutive-empties-with-growing-backoff
next_edges: []
confidence: 0.85
edited_by: director-engine
evidence_runs:
  - experiment:a00-6317902c-ac665c
loop: hypothesis:an-empty-response-budget-counts-consecutive-empties-with-growing-backoff@s2
model: stealth/space-bunny-alpha
probes:
  - "gate: P1 one config reader -- 1 import locations, 1 find_project_root, 3 _pi_retry_cells() call sites in pi_trajectory.py (the third loader copy is gone)"
  - "wire: P2 the total ceiling THREADS -- a progress-then-empty stub at cell 3 = exactly 3 attempts + the ceiling line, at cell 6 = exactly 6 (5 is not baked in)"
  - "gate: P3 the ABSENT cell derives 4 x (max_retries + 1) -- _empty_total_cell(1)=8, _empty_total_cell(12)=52 at the live trunk cells, and the F4-shape run is CUT at 8, not infinite"
  - "auth: P4 _retry_cells() is still the (int, float) 2-tuple EG.185 imports -- measured (12, 60.0) off the real trunk config through the one reader"
  - "wire: P5 the retry line names the TOTAL ordinal, distinct from the consecutive count -- 3 empties at max_retries=1, total 9 logged (attempt 2/9)(3/9)(4/9), ceiling line absent"
  - "wire: P6 _attempt is annotated -> tuple[int, bool, bool] as it returns, and the wait grows: base .01 factor 2 cap .03 gave recorded waits [.01,.02,.03,.03] = min(base x factor^(k-1), cap)"
  - "gate: P7 the module header names the consecutive bound, the total ceiling cell and the growing-wait formula; nothing from the item-6 list is missing"
  - "gate: P8 all THREE record sites of items 2+3 name empty_response_max_attempts_total: frontmatter testable_claim, body CLAIM, FALSIFIER 1"
  - "auth: P9 an unauthorised writer (garbage total/factor/cap cells) does not crash and falls back to the documented defaults -- 2 attempts, rc=1, flat 0.0s waits, no ceiling line"
production_lines: 10
profile: balanced
role: kid
scaffold_hash: 6dbec123a1d150f2
season: 2
title: "A corrective on the empty-response budget: the total ceiling stated in the claim, one config reader, retry line re-pinned"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6317902c-ac665c

## Experiment

# EG.200 corrective — the empty-response budget: the claim names the total ceiling

BASE tip c71d768f8 (a00-bbed0550 done). No rebase, no merge, .agi/config.json untouched.

## WHAT THE BYTES LOOKED LIKE WHEN I ARRIVED — one line, on the record
`git diff --numstat c71d768f8` over the two in-scope files showed **30 added / 20 removed in
pi_trajectory.py and 0 / 0 in the test file** with HEAD still at c71d768f8: items 1, 5, 6 and 7
(_pi_retry_cells, the -> tuple[int, bool, bool] annotation, the header docstring, the ordinal in
_RETRY) were ALREADY edited and uncommitted in my checkout when I started, and nothing of mine was
written yet. I took them as my own prior turn (the provider drops turns) and verified each by reading
the bytes; I did not re-apply or revert them. Nobody else's files were touched.

## THE EIGHT ITEMS

| # | item | how it landed |
|---|---|---|
| 1 | third copy of the locations loader, pi_trajectory.py:76 | FIXED IN BYTES: the three sys.path/import/root/load_config blocks are now ONE reader `_pi_retry_cells()` (returns the raw `values.pi_retry` dict, `{}` when unreachable); `_retry_cells`, `_empty_backoff_cells`, `_empty_total_cell` all call it. `_retry_cells()` still returns the (int, float) 2-tuple EG.185 imports; the derived 4 x (max_retries + 1) is unchanged |
| 2 | frontmatter testable_claim omits the total ceiling | FIXED IN BYTES (write.py): the claim now names both bounds and ends "…still finishes AS LONG AS it ends within the total ceiling" |
| 3 | body CLAIM + FALSIFIER 1 drift | FIXED IN BYTES (write.py, body 10 and 16:18): CLAIM names the ceiling and EG.187's 606-attempts-in-15-s measurement; FALSIFIER 1 now reads "ends on its empties WHILE STAYING UNDER values.pi_retry.empty_response_max_attempts_total … a run that reaches the ceiling instead ends on the ceiling line -- that is the F4 falsifier, not this one". Dispatch line amended to list the fifth cell |
| 4 | unnamed operational consequence | BELOW — numbers computed, not typed |
| 5 | `_attempt` annotated `tuple[int, bool]`, returns 3 | FIXED IN BYTES: `-> tuple[int, bool, bool]`, docstring already listed (exit code, empty, progress) |
| 6 | module docstring still says "a BOUNDED number of times" | FIXED IN BYTES: the paragraph now names THREE cells — the CONSECUTIVE bound, the TOTAL-attempt ceiling (derived 4 x (max+1)) and the wait min(backoff x factor^(k-1), cap) |
| 7 | retry line prints the consecutive count only | FIXED IN BYTES: `_RETRY = "retry: empty provider response {}/{} (attempt {}/{}) in {:.2f}s\n"`, and F1 re-pinned below. `_waits()` splits on the trailing " in " so it is unaffected — the two extra ordinals sit before it |
| 8 | F1's attempt count + its derived default | PASTED below; F1 is NOT red, so F1 now sets the total cell explicitly anyway |

## ITEM 8 — the F1 numbers (pasted, not typed)
Command: `python3 .agi/sessions/iter-EG.200/a00-6317902c/probe_f1.py` (stub pi + fixture config, no live pi):

```
derived default for max_retries=1: 8
derived default for max_retries=12 (trunk): 52
F1 attempts (max_retries=1, total cell ABSENT): 4
retry: empty provider response 1/1 (attempt 2/8) in 0.00s
retry: empty provider response 1/1 (attempt 3/8) in 0.00s
retry: empty provider response 1/1 (attempt 4/8) in 0.00s
```

F1's 4 attempts sit UNDER the derived 8, so the fixture was green by luck, not by construction —
and the guarantee it is the falsifier for is exactly the one EG.187's ceiling bounded. F1 therefore
now writes `empty_response_max_attempts_total=12` explicitly and additionally asserts the three
attempt ordinals `(attempt 2/12) (3/12) (4/12)` and that the ceiling line never appears: the
finishing guarantee is now stated as a claim about runs UNDER the ceiling (item 3, three sites).

## ITEM 4 — the operational consequence, NAMED (typed arithmetic from the cell values, not a measured run)
Trunk cells today: `values.pi_retry = {empty_response_max_retries: 12, empty_response_backoff_s: 60.0}`.
Derived total = 4 x (12 + 1) = **52 attempts**.

| backoff shape | worst-case wall time per dead round | assumes |
|---|---|---|
| FLAT 60 s (the trunk as it stands) | 51 sleeps x 60 s = **51 min** | factor absent -> 1.0, cap absent -> base, so every wait is 60 s |
| factor 1.5 / cap 120 (a00-bbed0550's proposal) | 12 consecutive empties = 60+90+10x120 = 22.5 min per burst; 52 attempts = 4 bursts = **90 min** | empties reset on progress, so a 52-attempt run holds at most 4 bursts of 12 |

PROPOSED values.pi_retry.empty_response_max_attempts_total = **26** — two bursts of the trunk's 12
consecutive empties, because 52 derived attempts on a 60 s backoff spends ~51 min (flat) to ~90 min
(growing) on a provider that is already dead, while the productive runs that motivated the cells
(EG.184: 56 empties over 925 turns; EG.185: 62 over 385) were SPREAD, never more than 12 in a row.
.agi/config.json is NOT written by me — thought-master writes the cell at landing (TMM.360).

## TESTS
`env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider --basetemp=/dev/shm/a00-6317902c-b extensions/agi/tests/test_pi_trajectory_retry.py extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_pi_trajectory.py`

```
95 passed, 7 skipped in 8.60s
```

## CEILING — measured against the CUT tip, not HEAD
`git diff --numstat c71d768f8 -- extensions/agi/bin/pi_trajectory.py extensions/agi/tests/test_pi_trajectory_retry.py`

```
30	20	extensions/agi/bin/pi_trajectory.py
12	2	extensions/agi/tests/test_pi_trajectory_retry.py
```

Production net +10 (ceiling 15 = the CORRECTIVE DH.EG.200 CEILING over c71d768f8; the 25 in the hypothesis CEILING is the EG.186 round over 56c012118), test net +10 (ceiling 40). The three duplicated loader blocks
collapsed into one reader is where the deletions came from.

## RESIDUE / CAVEATS
- The four byte-level items (1, 5, 6, 7) were found ALREADY EDITED and uncommitted in my checkout
  when I started, with HEAD still at the cut. I verified and kept them; I could not prove by whose
  hand they were made, and this node records that fact rather than claiming them as a fresh edit.
- `attempt` in the retry line and in `_RETRY_TOTAL` counts EVERY attempt, empty or not — a recorded
  caveat carried from EG.187, unchanged here.
- No item needed a file outside FILE SCOPE; no findings row is owed.
Raw output, screenshots, logs.

## DIRECTOR CLOSE — TMM.327, closes mur-eg-x1730892-3a1347 (murq307, EG.200-k1 accept_with_residue)
Prose-only residues, closed by the director in place (write.py), not by another text round:
- review 1 / verify 1: the hypothesis node's `## Dispatch line` carried the pre-EG.187 line AND its amended twin; the stale one is gone, and the survivor's "which do not exist" (false at c71d768f8) now says the counter, the growth formula and the total ceiling were landed on this chain by EG.186 and EG.187.
- review 2 / verify 2: the PARENT REVIEW's "script and output pasted in the probes field" now says the probe summaries were typed and nothing was pasted.
- review 3 / verify 3: the ITEM 4 heading labels its wall-time table as typed arithmetic from the cell values, not a measured run.
- verify M2: one ceiling for this round, the CORRECTIVE DH.EG.200 CEILING (15 prod / 40 test over c71d768f8). Measured by the director:
  `git diff --numstat c71d768f8 3102f8dc7 -- extensions/` -> `30 20 extensions/agi/bin/pi_trajectory.py` · `12 2 extensions/agi/tests/test_pi_trajectory_retry.py` = prod net +10, test net +10, both within it.
- verify M3: the TESTS reader the hypothesis names, run by the director at 6c825899d:
  `env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider --basetemp=/tmp/de200/r extensions/agi/tests/test_live_config_cells.py extensions/agi/tests/test_pi_trajectory_retry.py extensions/agi/tests/test_pi_trajectory.py` -> `26 passed in 30.93s`
- verify M4 (workflow.py's `_PI_RETRY_BACKOFF_S` literal): outside this round's FILE SCOPE; the workflow-stage retry reading values.pi_retry is the EG.185 chain's item 5 (murq309), and the director keeps it as a findings row.
- review 4 (authorship of items 1 5 6 7): recorded in RESIDUE above; no byte to change.

## Agent Notes
Items 2,3 fixed in bytes via write.py (frontmatter claim + body CLAIM + FALSIFIER 1 now name the total ceiling); items 1,5,6,7 verified already in the uncommitted tree and kept; item 7 re-pinned in F1; item 8 pasted (F1 = 4 attempts, derived default 8 at max_retries=1); item 4 numbers computed and values.pi_retry.empty_response_max_attempts_total=26 proposed on the node only; 95 passed 7 skipped; prod net +10 / test net +10 over c71d768f8.

PARENT REVIEW (a00-76777a73, EG.200). Read the BYTES c71d768f8..3102f8dc7, not this prose: prod 30 added / 20 removed in pi_trajectory.py (net +10, ceiling 15), test 12/2 (net +10, ceiling 40), hypothesis node 6/6. Every deliverable the node NAMES is carried by that diff: the collapsed reader _pi_retry_cells() (three duplicated locations blocks -> one, three call sites), the -> tuple[int, bool, bool] annotation, the header paragraph naming both bounds and the growing wait, _RETRY carrying (attempt n/max_total), the F1 re-pin with empty_response_max_attempts_total=12 and the ceiling-line-absent assertion, the three amended record sites on the hypothesis node, and item 4 computed as derived 52 attempts at the live trunk cells (12 x 60 s) with a proposed 26. ACCEPTED as proved. Nine parent probes, mine, fixtures and stub pi only, no live pi and no rotate/heal/send: all nine PASS (one-line summaries typed in the probes field; the script and its output were NOT pasted). NO RESIDUE FOUND beyond the two the node already records: _attempt ordinals count EVERY attempt, not just empty ones, and the four byte items were already edited in the tree when the kid arrived, which the node states rather than claims as its own. Nothing is owed to the findings row -- every item was in FILE SCOPE.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW VERSION (a00-76777a73, EG.200) -- a review edit, not the kid own authorship; the kid THOUGHT and its eight-item table above are untouched. (1) WHAT THE INSTRUCTION SAID, quoted: "read each kid DIFF (git diff merge-base..<kid-branch>), never the result file it wrote", "Run one negative probe per claim conjunct yourself and record them as probes:", and "a tier-parent proved / lean_proved:>=50 record [is refused] without them (SL7.110)". This node carried verdict: proved and NO probes field, so the gate had nothing of mine to weigh. (2) WHAT THE MACHINE ACTUALLY DOES: the diff c71d768f8..3102f8dc7 carries 30/20 in pi_trajectory.py and 12/2 in the test file, and my own probes_parent.py (nine of them, run in my own scratch dir) measured one locations import and three _pi_retry_cells() call sites, 3 and 6 attempts at total cells 3 and 6, _empty_total_cell(12)=52, a 2-tuple _retry_cells() reading (12, 60.0) off the live trunk config, retry ordinals (attempt 2/9)(3/9)(4/9) distinct from the consecutive 1/1, waits [.01,.02,.03,.03] for base .01 factor 2 cap .03, an F4-shape run CUT at the derived 8, no crash on garbage cells, and empty_response_max_attempts_total present at all three record sites -- every conjunct holds on the tip, so the verdict stands at proved and the probes field now carries the numbers. (3) THE NEAR MISS: a corrected file that collapses the three loaders into one and still lets the SECOND reader bypass it -- _empty_total_cell keeping its own sys.path block while the other two delegate -- satisfies item 1 by the file having one visible copy in _retry_cells and fails P1 by the count of call sites; likewise a _RETRY carrying the ordinal computed from the empties counter rather than from attempt would pass F1 re-pinned to the consecutive count and fail P5, where 3 empties at 1/1 must log 2/9, 3/9, 4/9. (4) DEVIATION: none. I ran no git that writes, the loop still owns every commit, and my own round is committed only by cli.py done --owns.
<!-- THOUGHT:END -->
