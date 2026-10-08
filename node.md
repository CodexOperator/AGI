---
id: hypothesis:a00-93414710-7b19d2
mint_id: 3b1ab74dd2274197be227f8eb2e087b3
type: hypothesis
parents:
  - goal:g7.33.11
next_edges: []
edited_by: director-engine
loop: goal:g7.33.11@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 1f47dc4cfde322f3
season: 2
title: Changed-tip batching still needs a post-split boundary
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:a00-93414710-7b19d2

## Measured

- `crons.py:554-559` renders one `git push` with `grid.push_spec_for(root)`; `grid.py:171` expands that helper to `<trunk>/*:<trunk>/*`, so each tick asks the host to validate the entire namespace in one operation.
- The configured local-maxxing trunk has thousands of refs while the failed cron has accumulated 967 host validation rejections; the change is selection and batching, not a different storage shape.

## CLAIM

A failed grid-ref push can leave the local namespace intact and advance nothing remotely: a pure selector can compare the configured trunk's local ref tips with the remote's tips, omit matching and obsolete remote-only names, partition the remaining refspecs into batches no larger than the configured limit, and stop before a later batch after a push failure. Thus a clean run advances only changed tips and a failed run retries only the unfinished batches, without deleting a local ref.

## Dispatch line

config-max: put the maximum refs per push in the `grid` section, beside `storage_trunk`. code: one grid resolver returns ordered `(ref, local_oid)` rows from `for-each-ref` and remote rows from `ls-remote`; one selector emits exact refspecs; crons invokes the shared batching helper rather than a wildcard.

## FALSIFIERS

- A matching local/remote tip appears in a push plan, a remote-only name is targeted, or a batch exceeds the configured limit.
- Any rejection causes a later batch to run, or retry/resume logic is forced to mutate or delete local refs.
- A successful push changes remote storage away from `refs/grid/*`, or the default unconfigured tree's rendered cron changes.

## TESTS

Add focused cases beside `test_grid.py` and `test_crons.py`: 401 changed tips produce 200 + 200 + 1; matching tips are omitted; remote-only names are omitted; a synthetic middle-batch failure is surfaced and the final batch is not invoked; the default storage trunk and cron shape remain compatible. A local bare-remote integration test verifies the pushed namespace, not only rendered argv.

## FILE SCOPE

`extensions/agi/bin/grid.py`, `extensions/agi/bin/crons.py`, their two named test files, and the `grid` config section only when a batch-limit cell is needed. No branch migration, ref deletion, or log rewrite belongs to this hypothesis.

## CEILING

1 kid · 40 production lines · 0 USD cap · no GPU.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 18: this claim is now fully satisfied -- landed this session as hypothesis:grid-push-batch-limit-is-a-config-cell (same underlying mechanism: crons.py:556 push-changed, grid.py push_batch_limit/push_batches/cmd_push_changed), not as a separate round under this id. Every TESTS bullet here is covered: the 401-tips-to-200+200+1 case (test_push_batches_401_changes_split_into_three_batches), matching/remote-only omission (pre-existing test_push_batches_omit_matching_and_remote_only_refs), a synthetic middle-batch failure stopping before the next batch (pre-existing test_push_changed_stops_after_failed_batch, an orphaned test fixed last session), and a local bare-remote integration proof of a retry after failure verified via git ls-remote, not just argv (test_push_changed_retries_after_a_failed_batch_against_a_real_remote, new this session). push_batch_limit is now a grid config cell beside storage_trunk, exactly as the Dispatch line asked. No local ref is ever deleted or mutated by the retry path -- push_batches recomputes fresh from git state every call. See experiment:grid-push-batch-limit-is-a-config-cell-fix for the full red/green record. This residues first sentence (about the PASS 5 residue tables overstating remote atomicity) is a wording concern on the OTHER hypothesis, not a gap in this ones own claim or tests.
<!-- THOUGHT:END -->
