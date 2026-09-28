---
id: experiment:a00-1b0bb960-64b6b0
mint_id: f20383479a0844fd954eccbb6f2c188e
type: experiment
parents:
  - hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
next_edges: []
confidence: 0.65
edited_by: a00-aa84faa3
evidence_runs:
  - experiment:a00-1b0bb960-64b6b0
loop: hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow@s2
model: stealth/space-bunny-alpha
production_lines: 69
profile: balanced
role: kid
scaffold_hash: 6efb15f5d997b262
season: 2
title: Execute and commit-gate a round parent
town: core
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-1b0bb960-64b6b0

## Experiment — execute and commit-gate a round parent

Implemented the next smallest slice of the parent workflow: `kind: round` now dispatches exactly one detached parent with the declared tier/role/ladder/branch flags, parses the spawned agent identity, polls that round's record, and succeeds only when the record is `done` **or** the recorded branch has advanced past its base. Dispatch refusal and terminal parent failure return a failed stage; timeout fails closed. The returned structured value is threaded through the existing stage persistence/chaining path.

The composed-stage order inherited from the previous experiment was stale for the live claim: inherited review stages ran before the prelude round. Composition now materializes **round prelude → inherited review stages → child stages**, and automatically makes inherited review stages depend on every round prelude label. A failed round is therefore skipped by name through the existing dependency mechanism, without copying or changing review prompts.

| Input / fault | Result |
|---|---|
| dispatch rc 0 + agent id + branch commit | rc 0 with target, parent, branch |
| dispatch rc 3 | rc 3, no retry |
| review inherits from round manifest | `round-parent` precedes `review`; review depends on round |
| no done status or branch commit before wall | rc 2, fail closed |

## Evidence

```text
python3 -m pytest extensions/agi/tests/test_workflow.py -q -p no:cacheprovider
120 passed in 132.25s (0:02:12)

git diff --numstat -- extensions/agi/bin/workflow.py extensions/agi/workflows/
60      9      extensions/agi/bin/workflow.py
```

Measured production footprint is **69 changed lines** across the production scope, under the 2×80-line re-brief threshold (and including the 18-line composition slice inherited in the shared diff). Tests are excluded.

## Limits carried forward

- The structured round return is intentionally minimal (`target`, `parent`, `branch`); the hypothesis's complete harvest (`hypothesis`, `experiments`, `files`, merge-base/new-tip, verdict) remains open.
- The poll reads the dispatch session's `manifest.json`; the worktree-local status divergence documented in `dispatch._reap_one_impl` is not yet reconciled.
- A dead PID is currently bounded by the stage timeout rather than classified immediately, and a `subprocess.run` timeout during dispatch propagates instead of becoming a stage return.

## Agent Notes
Round stages now dispatch one detached parent, gate on status or branch commit, and fail review closed; full harvest and worktree-local status remain open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: instruction was one detached parent with explicit flags, identity from dispatch output, and fail-closed status/commit gate. Machine bytes at workflow.py:2129-2158 dispatch the exact flags and consume ^spawned identity; my auth probe returned (3,None) for dispatch rc 3, and my wire probe created a live iteration manifest with status=done and observed (0,{target,parent,branch}) from _run_round_stage. The near miss is guessing a run id or accepting dispatch rc 0 without an identity/status; that would look successful while losing the gate. I did not test the remaining full harvest or dead-PID classification, so the 65% lean is accepted only for this slice, not the parent claim. probes: auth=dispatch rc 3 refused by return code 3; wire=live status done reached return code 0 and structured parent branch.
<!-- THOUGHT:END -->
