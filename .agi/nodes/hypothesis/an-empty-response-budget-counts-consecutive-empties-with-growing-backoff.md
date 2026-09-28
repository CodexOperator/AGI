---
id: hypothesis:an-empty-response-budget-counts-consecutive-empties-with-growing-backoff
mint_id: cc40ca3188b44faaa2fb6111467f604c
type: hypothesis
parents:
  - goal:g7.33
  - hypothesis:an-empty-provider-response-is-retried-not-fatal
next_edges: []
edited_by: director-engine
scaffold_hash: 7730d4593a43017e
season: 2
testable_claim: pi_trajectory.py retries an empty provider response against a CONSECUTIVE bound that resets after progress, waiting min(base x factor^(k-1), cap) before retry k, every number a values.pi_retry cell with today behaviour as the default -- a run with more total empties than the bound, never more in a row, finishes
title: An empty-response retry budget counts consecutive empties and backs off growing to a cap (TMM.360 item 2, EG.186)
town: core
---
# hypothesis:an-empty-response-budget-counts-consecutive-empties-with-growing-backoff

# hypothesis: an empty-response retry budget counts CONSECUTIVE empties and backs off growing to a cap

## Measured
- pi_trajectory.py main: `for attempt in range(max_retries + 1)` -- the budget is PER RUN: every empty response spends one retry for the whole parent session, however much work succeeded in between; the backoff is one fixed value (_retry_cells -> values.pi_retry.empty_response_backoff_s).
- director-engine, 09-28 21:45-22:30Z, on cuts carrying values.pi_retry 6 x 60 s: EG.184 parent a00-c8f1d0f6 = 56 empties over 925 turns, retries 6/6 used, survived on the last; EG.185 parent a00-69905c26 = 62 empties over 385 turns, 6/6 exhausted at 8 min, 0 commits. The empties are spread (about 1 per 6-16 turns), not one long outage: a per-run count kills a long, productive run for spread noise, and a bigger number only moves the edge (TMM.360).

## CLAIM
The retry bound counts CONSECUTIVE empty responses: it resets to zero once a resumed attempt makes progress (at least one completed turn before it ends), so a run with more total empties than the bound finishes as long as no more than the bound arrive in a row. The wait before retry k grows as base x factor^(k-1), capped at cap. Every number is a values.pi_retry cell; the code is the reader, with today's behaviour as its defaults.

## Dispatch line
config-max: max consecutive (values.pi_retry.empty_response_max_retries), base (empty_response_backoff_s), factor (empty_response_backoff_factor), cap (empty_response_backoff_cap_s) -- the kid PROPOSES the factor and cap values on its node; thought-master writes the cells at landing (a round-done commit never carries .agi/config.json) / template-max: none / code: the consecutive counter and the growth formula in pi_trajectory.py, which do not exist.

## FALSIFIERS
1. A fixture run whose stub pi yields MORE total empties than max_retries, never more than max_retries in a row, with progress between them, ends on its empties (the per-run count survives).
2. A stub that is empty max_retries + 1 times in a row does NOT end the run (the bound is gone, not moved).
3. The sleeps recorded for retries 1..k do not follow min(base x factor^(k-1), cap) for the fixture's cells, or a missing cell does not fall back to today's behaviour (factor 1, cap = base).

## TESTS
extensions/agi/tests/test_pi_trajectory_retry.py (the falsifiers, stub pi + fixture config, _RETRY_SLEEP-style monkeypatched sleep -- never a real wait) + neighbourhood test_pi_trajectory.py test_live_config_cells.py test_bin_help_smoke.py

## FILE SCOPE
extensions/agi/bin/pi_trajectory.py (_retry_cells and main's retry loop only) · extensions/agi/tests/test_pi_trajectory_retry.py · this node (write.py) · the kid's own node

## CEILING
1 kid · <= 25 production lines net · <= 40 test lines net · pi-free tier-0 · 0 USD -- two-operand numstat <cut>..<tip before the paste commit>, labelled so

## ROUND EG.186 -- TMM.360 item 2: dispatch now, ahead of EG.153 (the empty-response budget counts consecutive empties, backoff grows to a cap)
BASE      CUT FROM the town trunk tip 56c012118 (values.pi_retry 12 x 60 s already on it). Never rebase, never merge.
1. THE CLAIM above, in pi_trajectory.py only: a consecutive counter in main's retry loop that resets once a resumed attempt completes at least one turn before it ends; the wait before retry k = min(base x factor^(k-1), cap).
2. CELLS -- read factor and cap through the SAME loader _retry_cells uses; KEEP _retry_cells() returning (max_retries, backoff) unchanged (EG.185 item 5 imports it for the workflow-stage retry); add the two new cells beside it with defaults factor 1.0 and cap = backoff (today's behaviour, no new literal beyond those defaults). PROPOSE on your node the factor and cap values for the trunk cell (thought-master writes .agi/config.json at landing; a round-done commit never carries it).
3. FALSIFIERS 1-3 above = three tests in test_pi_trajectory_retry.py (stub pi + fixture config; the sleep monkeypatched, never a real wait). Paste each failing on the cut and passing on the tip.
TEXT RULES NUMSTAT SELF-REFERENCE: never paste a numstat that includes the commit it is pasted in · ANCHOR RULE: a cite names a function / heading / cell key and adds a line number only where the claim IS the line
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees
PROBES    never author or run a probe that calls rotate / heal / send / dispatch functions or a live pi; fixtures and monkeypatch only
TESTS     env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider --basetemp=/dev/shm/<dir> extensions/agi/tests/test_pi_trajectory_retry.py extensions/agi/tests/test_pi_trajectory.py extensions/agi/tests/test_live_config_cells.py extensions/agi/tests/test_bin_help_smoke.py (timeout 900) -- paste the summary line
FILE SCOPE extensions/agi/bin/pi_trajectory.py (_retry_cells + main's retry loop) · extensions/agi/tests/test_pi_trajectory_retry.py · this node (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 25 production lines net over 56c012118 · <= 40 test lines net over 56c012118 · pi-free tier-0 · 0 USD -- measure git diff --numstat 56c012118 <tip before the paste commit>, labelled so
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13) · WRITE THE NODE EARLY and commit after every run: the provider drops turns ('Provider returned an empty response'), and a round that dies mid-turn records nothing


## CORRECTIVE DH.EG.187 -- the EG.186 parent review (a00-ed3b6fd7, inconclusive_lean_disproved:65): the consecutive bound has no finishing guarantee
BASE      CUT FROM the EG.186 loop tip a2fa54dce (parent a00-ed3b6fd7, kid a00-d14e651d). Never rebase, never merge.
MEASURED  by the EG.186 parent on a2fa54dce: main() zeroes the consecutive counter on any attempt that completed a non-empty turn, so a stub that always makes progress and then ends empty never spends the bound -- 606 attempts in 15 s with max_retries=1, never returning. The comment in main ("What ends such a run is dispatch's own cancel, honoured between attempts below") describes a cancel check that does not exist. Director on the tip: the orders' TESTS = 96 passed, 7 skipped (the falsifiers F1-F3 hold; the finishing guarantee is untested).
1. A TOTAL-ATTEMPT CEILING -- one more values.pi_retry cell, empty_response_max_attempts_total, read through the SAME loader as the other two (beside _retry_cells; its 2-tuple unchanged, EG.185 imports it). When the cell is absent the default is FINITE and derived, never a new magic number: 4 x (max_retries + 1). The loop stops at that total whatever the consecutive counter says. PROPOSE the trunk value on your node beside the kid's factor 1.5 / cap 120 (thought-master writes .agi/config.json at landing).
2. THE COMMENT -- delete or correct the main() comment that promises a cancel check: the ceiling of item 1 is what ends such a run, say that and nothing more.
3. F4 -- a test in test_pi_trajectory_retry.py: the parent's shape (a stub that completes one turn then ends empty, forever) with max_retries = 1 and the total cell = 5 -> exactly 5 attempts, then the round's code; the sleep monkeypatched. Paste it HANGING or failing on the cut (use a pytest timeout or an attempt counter guard in the test, never an unbounded run) and passing on the tip.
4. THE CEILING BREACH OF EG.186 (+34 prod / +55 test vs 25/40) = a RECORDED residue: state it on the hypothesis node with the numstat 56c012118..a2fa54dce and why (three cells + the growth formula), never shrink working code to fit it.
TEXT RULES NUMSTAT SELF-REFERENCE: never paste a numstat that includes the commit it is pasted in · ANCHOR RULE: a cite names a function / heading / cell key and adds a line number only where the claim IS the line
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees
PROBES    never author or run a probe that calls rotate / heal / send / dispatch functions or a live pi; fixtures and monkeypatch only
TESTS     env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider --basetemp=/dev/shm/<dir> extensions/agi/tests/test_pi_trajectory_retry.py extensions/agi/tests/test_pi_trajectory.py extensions/agi/tests/test_live_config_cells.py extensions/agi/tests/test_bin_help_smoke.py (timeout 900) -- paste the summary line
FILE SCOPE extensions/agi/bin/pi_trajectory.py (the retry loop in main + the loader beside _retry_cells) · extensions/agi/tests/test_pi_trajectory_retry.py · hypothesis:an-empty-response-budget-counts-consecutive-empties-with-growing-backoff (write.py) · experiment:a00-d14e651d-aa5339 (write.py, item 4 only) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 8 production lines net over a2fa54dce · <= 25 test lines net over a2fa54dce · pi-free tier-0 · 0 USD -- measure git diff --numstat a2fa54dce <tip before the paste commit>, labelled so
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13) · WRITE THE NODE EARLY and commit after every run: the provider drops turns ('Provider returned an empty response'), and a round that dies mid-turn records nothing

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.187: EG186-parent EG.186 parent review residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
