---
id: experiment:grid-push-batch-limit-is-a-config-cell-fix
mint_id: 7f01f65a44b44bf5a1b8f329d6e1de8c
type: experiment
parents:
  - hypothesis:grid-push-batch-limit-is-a-config-cell
next_edges: []
confidence: 0.95
edited_by: director-engine
evidence_runs:
  - experiment:grid-push-batch-limit-is-a-config-cell-fix
scaffold_hash: 844094f7544e36d6
season: 2
tags:
  - local-maxxing
  - engine
  - grid
testable_claim: .agi/config.json carries grid.push_batch_limit; grid.py reads it with no literal fallback (absent = a named refusal); the batched push is tested at 401 changes and on a retry after one failed batch.
title: grid push_batch_limit is now a refused-if-absent config cell, with 401-boundary and retry tests
town: core
verdict: proved
---
# experiment:grid-push-batch-limit-is-a-config-cell-fix

# experiment:grid-push-batch-limit-is-a-config-cell-fix

## Experiment

Implemented `hypothesis:grid-push-batch-limit-is-a-config-cell` directly (PASS 5 chunk 3 /
PASS 6 residue: "the grid push batch limit is a code default (200), not a config cell; the
401-change three-batch case and a partial-failure retry are untested").

Production change in `extensions/agi/bin/grid.py`'s `push_batch_limit()`: dropped the
`.get("push_batch_limit", 200)` literal fallback. Absence of `grid.push_batch_limit` in
config.json now refuses by name (`sys.exit`) rather than silently defaulting to 200. Since
`grid.py push-changed` is live infrastructure (crons.py:556 chains it after `commit --all` in
the 5-minute grid_sync cron line), added `"push_batch_limit": 200` to THIS repo's own
`.agi/config.json` `grid` block in the same commit -- same value as the old literal default, so
the live cron's behaviour is unchanged, not merely un-broken.

Three new tests in `test_grid.py`:
- `test_push_batch_limit_refuses_when_the_cell_is_absent` -- the actual fix.
- `test_push_batches_401_changes_split_into_three_batches` -- the named boundary
  (ceil(401/200) = 3, last batch a singleton). The nearest pre-existing coverage
  (`..._omit_matching_and_remote_only_refs`) starts from 402 SOURCE rows and excludes two,
  landing on 400 changed refs, never 401.
- `test_push_changed_retries_after_a_failed_batch_against_a_real_remote` -- two real grid refs
  against a real bare remote, `push_batch_limit=1` so each is its own batch; the second push
  call is made to fail once, then an ordinary second `cmd_push_changed` call (the retry —
  exactly what the next cron tick does) finishes the job. Both refs verified against the remote
  via `git ls-remote`, not against the CLI's own report text.

Also fixed one now-failing pre-existing test: `test_push_changed_advances_real_bare_remote`
called `cmd_push_changed` against the shared `project` fixture, whose config never set
`push_batch_limit` -- it relied on the literal default this round removes. Added the cell to
that test's own config write, matching every other push-batch test's existing convention.

## Evidence

RED (grid.py reverted via a saved patch, config.json and the three new tests kept): only the
absence-refusal test fails, exactly as expected -- the 401-boundary and retry tests both PASS
even pre-fix, because `push_batches`' batching arithmetic and `cmd_push_changed`'s
recompute-from-git-state design were already correct. The PASS 5/6 residue's "untested" was
accurate; "broken" was not the finding for those two cases -- recorded honestly rather than
claiming three bugs where there was one.

```text
$ python3 -m pytest extensions/agi/tests/test_grid.py -q -k "push_batch_limit_refuses or 401_changes or retries_after_a_failed"
1 failed, 2 passed
```

GREEN (patch re-applied):

```text
$ python3 -m pytest extensions/agi/tests/test_grid.py -q
146 passed
```

Did NOT run `grid.py push-changed` live against this repo's real origin to smoke-test the
config change end-to-end -- director-engine's own standing rule is NEVER `git push`, any form,
from this worktree, and `push-changed` shells out to a real `git push`. The three new tests
against real local bare remotes are the verification; the live cron is the real-origin proof,
already running every 5 minutes.

## Agent Notes
assigned: director-engine (PASS 5/6 residue, belam-S2-L5-V/VI 09-25)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE HYPOTHESIS ASKED: a config cell with no literal fallback, plus tests at the 401-change
boundary and for a partial-failure retry. WHAT THE MACHINE ACTUALLY DOES: verified all three
directly. The one genuine defect was the literal fallback -- fixed, and reverting just that one
function (config.json and the tests left in place) is what isolated it cleanly: only the
absence-refusal test went red, proving the other two named risks were already handled by the
existing design (batches computed by plain slicing; retry safe because push_batches always
recomputes from a live git diff rather than persisting progress). Named this distinction plainly
rather than writing a triumphant "fixed 3 bugs" line the bytes do not support. The live-cron
consequence (this repo's own config lacked the cell, so removing the fallback outright would
have broken grid_sync every five minutes) was not stated anywhere in the hypothesis and required
tracing crons.py's own cron-line construction to find -- worth recording because a future
reader applying the same "no literal fallback" pattern elsewhere should check for a live caller
before deleting a default, not after.
<!-- THOUGHT:END -->
