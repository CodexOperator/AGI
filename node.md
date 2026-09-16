---
id: hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp
mint_id: 714368b9a3374a1c82f5537fcceb7197
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: e4df65a03519a581
season: 2
testable_claim: "SM.69 (belam gen 25 20:1xZ + 20:2xZ residue for the SM lane after the owner moved every review to pi; MEASURED mur-sl7-137 20:02Z: on the pi harness both merge-up-review stages returned PROSE -- the reviewer markdown, the refuter a yaml fence -- so the router marked them `unstructured` and kept only a 200-char view line; the whole review was unreadable. Prime direct write 98eeae2fd persists every pi stage's WHOLE return to sessions/workflows/runs/<run_key>/<label>.json, best effort, never failing the run. Also measured by SM (mur-sm-60 19:22Z): a one-round/15-item review timed out at 1800 s and was reported as 'could not start pi'). CLAIM: (1) 98eeae2fd gets its fixture test: one fake-pi stage returning prose -> the file is present under runs/<run_key>/<label>.json with the FULL text, run rc 0, and the jsonl row points at it; (2) a pi review stage returns a STRUCTURED report: either the merge-up-review manifest prompt states the JSON schema as the ONLY allowed output (no fence, no prose before or after) or `_resolve_lenient_return` lifts a fenced ```json / ```yaml block into the structured return -- measured on ONE real pi stage (deepseek-v4-flash) whose row reads structured, not `unstructured`; (3) a stage that hits its timeout is reported as 'timed out after N s' FIRST, never as 'could not start' (the TimeoutExpired text led the line, the prompt is never echoed). (4) MEASURED SM stamp run 2 (20:0xZ): a concurrent pytest in the same tree errored all 5247 tests at setup in 47 s -- pytest's shared /tmp/pytest-of-<user> basetemp prune (keeps 3) deleted the runner's tree mid-run (12 stale basetemps sat there); run 4 with PYTEST_ADDOPTS=--basetemp=<private> was the fix. CLAIM (4): verification.py's suite runner passes its OWN --basetemp under the session dir (a runner-owned dir it creates and removes), never the shared default and never a shell habit; a fixture test asserts the argv carries it. FALSIFIERS: a fake-prose stage with no persisted file or a truncated one; a real pi review row still `unstructured` after (2); a timeout line that begins 'could not start'. TESTS (<=4, fixtures + one real pi stage for (2)): prose persisted whole; fenced json lifted; timeout wording; real-stage row structured. FILE SCOPE: workflow.py (persist test, lenient return, timeout wording), extensions/agi/workflows/merge-up-review.json (prompt), test_workflow.py, verification.py (suite argv basetemp) + its test. CEILING: <=50 production lines across 3 kids ((1)+(3) one kid, (2) one kid with the real-stage measurement, (4) one kid <=10 lines), re-brief SM past 2x. Until (2) lands the Prime reads the persisted prose."
title: L4 pi review stages return structured reports persisted whole with timeouts named and a private basetemp
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
ITEM (5), belam gen 26 21:42Z, measured on mur-sl7-138-r2 21:40Z: when the per-run mint FAILS (the workspace 403) workflow.py :1231 logs '[credential] inherited env (<reason>)' and RUNS the stage on the inherited OPENROUTER_API_KEY -- the owner-deleted 401 key -- so the reviewer spins to the 1800 s cap on a dead credential, spending nothing and reporting nothing. CLAIM (5): a failed mint REFUSES the stage by name (rc 3, the mint error verbatim) unless the inherited key is proven usable (provisioning.check_runtime_key_usable) -- never a silent fallback onto a credential nothing verified. FALSIFIER: a stage that starts on an inherited key after a mint failure without a usable-check line. TEST: fake mint failure + fake unusable inherited key -> rc 3 with the mint error; fake mint failure + usable key -> stage runs with a named '[credential] inherited env, verified' line. Same kid as items (1)+(3); ceiling +10. ALSO carried onto this node's first kid from node A (SM ruling 21:4xZ): the cap_headroom refusal line names limit-sum and used-sum beside live; the expired-1.50 + live-1.50-used-1.00 -> 0.50 test; the tmp_path-length bound in test_ack_cell_printer.
