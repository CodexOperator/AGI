---
id: verdict:a01-loop-scoped-ids-disproved
mint_id: 5b1f3c9a2e7d4c8fa1b6d0e9c4f7a123
type: verdict
parents:
  - experiment:a01-7a49270a-a6b875
next_edges: []
confidence: 0.75
evidence_runs:
  - experiment:a01-7a49270a-a6b875
  - experiment:a00-ed477860-8f3343
scaffold_hash: 0000000000000000
title: "Loop-scoped iteration ids: disproved as stated, but the manifest-clobber it worried about is already fixed a different way"
verdict: disproved
---
# verdict:a01-loop-scoped-ids-disproved

## Verdict

`disproved`

Two independent readings (`experiment:a00-ed477860-8f3343`,
`experiment:a01-7a49270a-a6b875`) of `driver.sh`, `cli.py`, `dispatch.py` and
`zoom.py` agree: the `testable_claim` is false as written. There is no
`L<loop>.<nn>` id scheme anywhere in the code — `L1.01..L1.08` are hand-typed
commit-subject and directory-name conventions, never parsed or minted by any
of the four files named. `driver.sh`'s own loop is `for i in $(seq 1
"$MAX_ITERS")`: every fresh invocation restarts at iteration 1 with no
allocator that checks `sessions/` for the next free id. `sessions/iter-001`
holds a fully populated real manifest from an earlier run, so a plain
`driver.sh --max-iters 1` today would target that same path.

What the hypothesis got right in spirit, wrong in mechanism: a clobber guard
*does* exist, but it is narrower than "iteration ids are loop-scoped end to
end." `dispatch.py:335-354` (`goal:s28`) reads any existing `manifest.json`
before writing, preserves its `agents` list, and appends new
uuid-suffixed-id records rather than overwriting — so two dispatches into the
same `iter-NNN` cannot delete each other's agent entries. That guard protects
one field of one file. It does not protect `iter-NNN-graph.json` (plain
overwrite), does not give directories loop-scoped identity, and does nothing
for the actual scenario the hypothesis names: two *separate* loop runs
(months apart, in this case) sharing the same low iteration numbers by
construction.

Net: the specific fix proposed by the hypothesis (loop-scoped ids,
end-to-end, `L<loop>.<nn>`) was never built. The narrower problem it was
worried about (a dispatch overwriting another agent's manifest entry) was
already independently fixed under `goal:s28`, before this hypothesis was
minted, by a different mechanism (merge-not-overwrite) that does not require
loop-scoped ids at all. A follow-on hypothesis, if this is worth pursuing
further, should target the gap this verdict actually found: `driver.sh`'s
own `seq 1 "$MAX_ITERS"` restart, and the un-merged `iter-NNN-graph.json`
overwrite, rather than re-asserting the id format is already loop-scoped.

## Agent Notes


## Agent Notes
No L<loop>.<nn> id scheme exists in code; driver.sh restarts its counter at 1 every run with no next-free-id allocator. The real fix (goal:s28's manifest merge-not-overwrite) protects agents-list entries only, not iter-NNN-graph.json or cross-loop directory reuse.
