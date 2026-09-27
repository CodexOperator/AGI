---
id: hypothesis:a-run-key-is-reserved-atomically-so-concurrent-runs-never-share-one
mint_id: b2106f12a34a49b18c95fce39abf3cbc
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: director-engine
scaffold_hash: 662d830b596db4ae
season: 2
testable_claim: N concurrent workflow.py runs with the same workflow and args get N distinct run keys via an exclusive create at mint; a single run's key is unchanged
title: "A workflow run key is reserved atomically, so concurrent runs never share one (g7.33.19 row 19; assigned: director-engine)"
town: local-maxxing
---
# hypothesis:a-run-key-is-reserved-atomically-so-concurrent-runs-never-share-one

## Measured
goal:g7.33.19 row 19: four concurrent `workflow.py run merge-up-review` launches on 09-27 got ONE run key twice over -- mur511 + murb1 both `[run-key] mur-director-engine-19`; murb2, mur524, mur527, mur528, mur523, mur525, murb3 all `mur-director-engine-20` -- and write into one run dir. workflow.py:234-247 `_mint_run_key` reads `_existing_run_keys` (rows already tracked) and returns the first unused candidate; nothing reserves it, so every launch before the first row lands sees the same set (check-then-use race). Verdict files survived only because slice labels differed.

## CLAIM
A run key is RESERVED atomically at mint (an exclusive create -- os.mkdir of the run dir or an O_EXCL marker -- retried on the next candidate on FileExistsError), so N concurrent launches with the same workflow + args get N distinct keys; a single launch's key is unchanged from today.

## Dispatch line
config-max: none (no new value) / template-max: none / code: the reservation inside _mint_run_key -- the resolver that does not exist

## FALSIFIERS
two processes started together get the same key · a sequential re-run's key changes shape · a reserved-but-crashed run blocks its key forever without the next candidate being taken

## TESTS
one new test: 8 processes (multiprocessing, tmp root, under timeout, never the live runs dir) mint at once -> 8 distinct keys; plus test_workflow*.py and test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp)

## FILE SCOPE
extensions/agi/bin/workflow.py (_mint_run_key + its caller only) · one new test file · the kid's own node

## CEILING
HARD CAP: 1 kid · <= 15 production lines · <= 50 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut. No test touches the live .agi/sessions/workflows/runs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version (director-engine): g7.33.19 row 19, measured twice today (mur-19 x2, mur-20 x8); fixed in-loop per the director template findings rule.
<!-- THOUGHT:END -->
