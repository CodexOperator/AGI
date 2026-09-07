---
id: experiment:a00-feee859f-5f2eca
mint_id: 30ff4d81194249f5b27df7a775b7458d
type: experiment
parents:
  - hypothesis:l3-node-without-mint-id
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-feee859f-5f2eca
loop: hypothesis:l3-node-without-mint-id@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: ed9f85a6822032f2
season: 2
title: A00 feee859f 5f2eca
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-feee859f-5f2eca

## Experiment

Claim tested (hypothesis:l3-node-without-mint-id): a node minted outside
`node_writer` (a kid writing its own file with its own file tool) gets its
FIRST `mint_id` from the engine — `cli.py done` (the parent-facing repair) or a
`write.py <id> adopt` verb — so `grid.py commit --all` versions it with 0
errors; giving a `mint_id` to a node that already has one stays REFUSED.

The orphan was real: `experiment:a00-230456c1-1abcda` (written by the ladder's
DeepSeek kid, `edited_by: ubuntu`, `verdict: proved`, but NO `mint_id` and NO
`scaffold_hash`), which `grid.py commit --all` refused to version on every
grid_sync tick, and `write.py set mint_id` refused by design (goal:g2.5).

### What I built (the fix shape), then tested

1. **`node_writer.repair_mint(root, node_id)`** — the one sanctioned adoption.
   Mints through the SAME identity source as every mint
   (`mint_permanent_id`, goal:s14: a mint id comes from the writer, never a
   backfill), stamps `scaffold_hash` of the *placeholder* body so the adopted
   node reads COMPLETE under `completion.is_complete` (real content differs
   from the placeholder -> complete, drift-safe against a future BODY_PROMPTS
   change), and logs the final bytes through `_log_write` for the write-guard.
   Returns `UPDATED` (adopted) | `SKIPPED` (refusal: already has a mint_id) |
   `REJECTED` (could not find/parse).

2. **`cli.py done`** now repairs a missing `mint_id` right after the
   L3.15-style `_ensure_frontmatter` repair — keyed from the spawn manifest
   (`agent.json`), the same source the frontmatter repair uses — and fails the
   run if the node cannot be adopted (REJECTED).

3. **`write.py <id> adopt`** — the parent-facing verb. It is the single
   sanctioned exception to the `mint_id` PROTECTION: it does NOT `set`, it
   routes through `node_writer.repair_mint`, which refuses an already-minted
   id. Standalone (cannot share a line with other verbs), `--dry-run` supported,
   so the "no second way to write" invariant in `write.py` is preserved.

### Test results (red-first, then green)

```
$ python3 -m pytest extensions/agi/tests/test_node_writer.py -q -k repair_mint
5 passed
$ python3 -m pytest extensions/agi/tests/test_grid.py -q -k adopted_node_commits
1 passed        # cmd_commit --all reports 0 errors after adoption; mint ref exists
$ python3 -m pytest extensions/agi/tests/test_cli.py -q -k adopts_a_node
1 passed        # done mints mint_id on a no-mint node, verdict still recorded
$ python3 -m pytest extensions/agi/tests/test_write.py -q -k adopt
5 passed        # mint, refuse-when-present, standalone, dry-run, set still refused
$ python3 -m pytest extensions/agi/tests/ -q
1856 passed, 1 skipped (102s)
```

### LIVE PROOF on the real orphan
```
$ python3 extensions/agi/bin/write.py experiment:a00-230456c1-1abcda adopt --root /home/ubuntu/work/agi/.agi
adopted experiment:a00-230456c1-1abcda: minted 50952ab682bc4860bd74a65bf29c2d4a
adopted: experiment:a00-230456c1-1abcda mint_id=50952ab682bc4860bd74a65bf29c2d4a   (exit=0)
$ python3 extensions/agi/bin/write.py experiment:a00-230456c1-1abcda adopt --root .agi
SKIP: ... already carries mint_id 50952ab682bc4860bd74a65bf29c2d4a ... refusing   (exit=1)
$ python3 extensions/agi/bin/completion.py .agi experiment:a00-230456c1-1abcda   (exit=0 = complete)
```
Frontmatter before: `id/type/parents/confidence/edited_by/evidence_runs/title/verdict`
(no mint_id, no scaffold_hash). After: `mint_id` + `scaffold_hash` added, every
pre-existing field and the whole body byte-identical. The orphan now carries a
durable identity, so the next `grid.py commit --all` (0 errors, proven by the
grid test) versions it — no longer refused on every grid_sync tick.

## Evidence

- Red-first tests and their passes above; the full 1856-pass suite.
- `test_adopted_node_commits_with_zero_errors` (test_grid.py) is the live-proof
  half that respects the "agent never runs grid.py" rule: it drives
  `grid.cmd_commit(..., do_all=True)` directly — 0 errors, mint-id ref exists —
  on a node that was previously refused.
- The real orphan `experiment:a00-230456c1-1abcda` adopted in place; re-adopt
  refused; reads complete.

## Agent Notes
Implemented node_writer.repair_mint, wired into cli.py done, added write.py <id> adopt verb. Proved: a kid-written node with no mint_id gets adopted (minted through the same identity source, scaffold_hash stamped, reads complete), and a re-adopt refuses. Live-proofed on the real orphan experiment:a00-230456c1-1abcda (minted 50952ab682bc4860bd74a65bf29c2d4a). 1856-test suite green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-13246e56, L3.20): accepted as proved. Independently verified, not taken from the report: the real orphan experiment:a00-230456c1-1abcda now carries mint_id 50952ab682bc4860bd74a65bf29c2d4a and its pre-existing frontmatter fields and body survived adoption byte-intact; re-adopt via write.py adopt refuses with the goal:g2.5 message (exit 1); node_writer.repair_mint exists at the wired location; full suite re-run by me: 1856 passed, 1 skipped. Caveat from the kid report stands but is acceptable: the 0-errors grid commit was proven inside pytest by driving grid.cmd_commit directly (agent contract forbids running grid.py), so the live orphan is versioned by the next real grid_sync rather than by the agent. evidence_runs names itself, which is legitimate for an experiment — it IS the run.
<!-- THOUGHT:END -->

Parent review ACCEPTED, verdict proved upheld. Verified live: orphan adopted (mint_id present, re-adopt refused), suite 1856 green. No demotion.
