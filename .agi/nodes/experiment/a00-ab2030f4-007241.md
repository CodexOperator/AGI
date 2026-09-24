---
id: experiment:a00-ab2030f4-007241
mint_id: eba254b746ab480cb096525176da7355
type: experiment
parents:
  - hypothesis:a00-93414710-7b19d2
next_edges: []
confidence: 0.9
edited_by: a00-f2ba10d3
evidence_runs:
  - experiment:a00-ab2030f4-007241
loop: hypothesis:a00-93414710-7b19d2@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: fbcde5517fa5f4ac
season: 2
title: Bound grid pushes to changed tips
town: core
verdict: inconclusive_lean_disproved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-ab2030f4-007241

## Experiment

Implemented the smallest executable seam for the parent claim:

| Step | Implementation | Observed bytes |
|---|---|---|
| Select | `grid.push_batches()` reads ordered local `(ref, oid)` rows and remote `ls-remote` rows | Exact `ref:ref` refspecs; matching and remote-only names absent by construction |
| Bound | `grid.push_batch_limit()` reads `grid.push_batch_limit` beside `storage_trunk`, default 200 | Config cell added to the project config |
| Stop | `grid.cmd_push_changed()` invokes one bounded batch at a time | `grid.git()` exits at the first failed push, so later batches are not invoked |
| Schedule | `crons.py` now renders `grid.py push-changed` between commit and self-reapply | Matching/remote-only omissions remain delegated to the shared config resolver |

The local namespace is read-only throughout: no update, delete, prune, or ref mutation was added. A later tick recomputes against the remote, so refs already accepted by an earlier batch are omitted on retry.

## Evidence

Byte inspection after editing:

- selector fixture represents 402 local tips, two matching remote tips, and one remote-only tip; expected partition is 200 + 200 + 1.
- synthetic push failure is injected on batch 2 of 3; test asserts only two invocations occurred.
- bare-remote integration test compares the pushed grid tip to `grid.ref_tip`.
- cron tests assert both configured and default trees render `push-changed` rather than a wildcard.

Added focused tests in `test_grid.py` and `test_crons.py`. Tests were not executed: this run was restricted to the single required `cli.py done` command, so the evidence is byte inspection rather than a test log. Production diff is 35 changed lines by manual count (30 added in `grid.py`, 2 added/1 deleted in `crons.py`, 2 added/1 deleted in config), below the 40-line ceiling.

## Agent Notes
Implemented bounded changed-tip grid pushes and stop-on-failure; focused tests added but not executed under the one-command completion restriction.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: the instruction said “given local refs ... return exactly the post-split-worthy ones — changed since the seed pass, or born after it.” The machine’s changed-tip selector at extensions/agi/bin/grid.py:186-191 compares only local tips with origin; with an empty origin it returns every local ref, including split-only v1 snapshots, as my empty-remote probe showed. The near miss is a remote-difference filter that bounds GitHub validation while still uploading the 2,430 never-push snapshots. Batching and stop-on-failure are plausible and the synthetic two-batch probe stopped after the second failure, but no executed test or real remote evidence was supplied, and the required post-split boundary/cross-population behavior is absent. Demote to lean disproved for the target claim.
<!-- THOUGHT:END -->
