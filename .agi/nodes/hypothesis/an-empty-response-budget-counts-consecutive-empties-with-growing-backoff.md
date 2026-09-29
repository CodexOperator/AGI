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


## CORRECTIVE DH.EG.200 -- closes mur-eg-x457729-e9deed EG.187-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-an-empty-response-bud-a00-e3044c6f tip c71d768f8 (branch de-base-EG.200; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Third copy of the locations config loader in one file -- extensions/agi/bin/pi_trajectory.py:76
2. testable_claim omits the new total ceiling that bounds its finishing guarantee -- .agi/nodes/hypothesis/an-empty-response-budget-counts-consecutive-empties-with-growing-backoff.md:9
3. SECOND RECORD SITE the first reviewer did not name: it is not only testable_claim (:12) that the new ceiling falsifies -- the hypothesis body's CLAIM (:25, 'a run with more total empties than the bound finishes as long as no more than the bound arrive in a row') and FALSIFIER 1 (:31) are now bounded by the total ceiling too, so falsifier 1 is no longer falsifiable by a long run: under the shipped code that run is CUT at 4*(max_retries+1) attempts instead of finishing. The THOUGHT at :60 names the ceiling, so this is one drift with two unamended sites, not two defects.
4. UNNAMED OPERATIONAL CONSEQUENCE: the trunk cells are values.pi_retry = {empty_response_max_retries: 12, empty_response_backoff_s: 60.0} (git show c71d768f8:.agi/config.json), so the derived default at pi_trajectory.py:91 is 52 attempts, and the node's proposal (.agi/nodes/experiment/a00-bbed0550-2e8a23.md:85) is to leave empty_response_max_attempts_total absent -- which is what the trunk will get. The F4 shape the ceiling exists to stop therefore parks a town seat for up to 52 real pi invocations, ~51 min at the flat 60 s backoff, and ~100 min if the proposed factor 1.5 / cap 120 (:83-84) are written. Bounded, so not a defect, but no node states the number and the landing mind should.
5. (carried from murq282 mur-eg-x48288-b95cc5 EG.186-k1) extensions/agi/bin/pi_trajectory.py _attempt: return annotation `-> tuple[int, bool]` vs the 3-tuple it returns and its 3-item docstring -- fix the annotation
6. (carried from murq282 mur-eg-x48288-b95cc5 EG.186-k1) extensions/agi/bin/pi_trajectory.py module header docstring still says the empty response is retried a BOUNDED number of times and ends the round as before -- restate it for the consecutive bound + growing backoff + the total ceiling cell
7. (carried from murq282 mur-eg-x48288-b95cc5 EG.186-k1) the retry line prints the CONSECUTIVE count only: add the total-attempt ordinal (_RETRY line), re-pin F1's expected lines accordingly
8. (carried from murq282 mur-eg-x48288-b95cc5 EG.186-k1) F1 vs the derived total default: paste the F1 attempt count and the derived default for F1's settings; if the default turns F1 red, F1 sets the total cell explicitly
DEMOTED   by the director at triage: murq283 generated items 1 (ceiling) and 4 (collision), not the items numbered above -- item 1 = the ceiling breach is RECORDED on the node (TMM.315: a recorded residue, never a prose-only corrective); item 4 = merge-up collision REFUTED by the bytes: git merge-tree --write-tree c71d768f8 local-maxxing/season2/main (67adcd0f6) exits 0, no conflict
PROPOSE   the total-attempt default: paste the derived value at the live cells (values.pi_retry 12 x 60 s) and the worst-case wall time it implies; PROPOSE a values.pi_retry.empty_response_max_attempts_total value with one sentence why, on your node -- NEVER write .agi/config.json (thought-master writes it at landing, TMM.360)
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_pi_trajectory_retry.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/pi_trajectory.py · extensions/agi/tests/test_pi_trajectory_retry.py · .agi/nodes/experiment/a00-bbed0550-2e8a23.md · .agi/nodes/hypothesis/an-empty-response-budget-counts-consecutive-empties-with-growing-backoff.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over c71d768f8 · <= 40 test lines net over c71d768f8 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat c71d768f8 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.200: mur-eg-x457729-e9deed EG.187-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
