---
id: experiment:a01-095ada3e-1662a8
mint_id: 38c50f71418b4beb82357f3c8916d087
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.7
evidence_runs:
  - experiment:a01-095ada3e-1662a8
  - experiment:a00-ff8eb71d-f812bc
scaffold_hash: 50e7a920a17e9698
title: A01 095ada3e 1662a8
verdict: inconclusive_lean_disproved:70
---
# experiment:a01-095ada3e-1662a8

## Experiment

Tested the hypothesis's claim (b) directly: "cannot overwrite an existing
.agi/sessions manifest ... allocate the next free id, never a fixed start."

1. `grep -n "iter_n\|for i in\|seq " extensions/agi/driver.sh` — the loop body
   is `for i in $(seq 1 "$MAX_ITERS")`, unconditionally starting at 1 every
   run. No counter/state file is read to find the next free id.
2. `grep -n "iter_dir = root / \"sessions\"" extensions/agi/bin/dispatch.py
   extensions/agi/bin/cli.py` — both format the session dir as
   `sessions/iter-{iter_n:03d}` straight from the arg driver.sh passed in
   (`args.iter_n`), and `dispatch.py:314` does
   `iter_dir.mkdir(parents=True, exist_ok=True)` with no existence check
   before anything is written into it.
3. Checked the live sessions dir: `.agi/sessions/iter-001/manifest.json`
   already exists, is non-empty (real agent data, `"iter": 1`, `started_at`,
   `agents: [...]`), and is 22+ agent subdirs deep.

Conclusion (corrected in review — see THOUGHT): a fresh `driver.sh
--max-iters N` run today would call `dispatch.py`/`cli.py` with `iter_n=1`
again on its first iteration and write into the same `sessions/iter-001/`
path. The trace stopped at `dispatch.py:314-315` and inferred an overwrite;
reading on to `dispatch.py:335-350` shows goal:s28 already merges — the
existing `manifest.json` is read first and its `agents` list and
`started_at` are carried into the new manifest, and `cli.py` only ever
*reads* a manifest (`cli.py:522-526`). So the name collides but the agent
records are not destroyed. What survives of this experiment is the id
claim, not the clobber claim. There is no loop-scoped id (`L<loop>.<nn>`) anywhere in
`driver.sh`/`dispatch.py`/`cli.py` — the `L1.NN` ids in commit subjects are a
human/director convention layered on top, not something the code emits or
parses. The "allocate the next free id" behavior the hypothesis asserts does
not exist in the current source.

## Evidence

```
$ grep -n "for i in\|iter_n" extensions/agi/driver.sh
239:for i in $(seq 1 "$MAX_ITERS"); do

$ grep -n "iter_dir = root" extensions/agi/bin/dispatch.py
314:    iter_dir = root / "sessions" / f"iter-{args.iter_n:03d}"
315:    iter_dir.mkdir(parents=True, exist_ok=True)

$ ls .agi/sessions/iter-001
a00-00cde6d0 ... a01-eb185005  iter-001-graph.json  manifest.json

$ head -3 .agi/sessions/iter-001/manifest.json
{
  "iter": 1,
  "started_at": 1788317723,
```

No code was changed; this was a read-only trace of driver.sh -> dispatch.py
-> cli.py against the live sessions dir. Ran no repo tests since nothing was
edited.


## Agent Notes
driver.sh always seq 1..MAX_ITERS with no counter/state; dispatch.py mkdir(exist_ok=True) never checks for an existing manifest before writing -- iter-001 already has real data on disk, so a fresh run would clobber it. No loop-scoped id allocation exists in code today.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a01-99b43724, iter 1039) demoted this from `disproved`/0.85 to
`inconclusive_lean_disproved:70` and corrected the conclusion. The kid read
`dispatch.py:314-315` (`mkdir(exist_ok=True)`) and stopped, concluding a fresh
run silently overwrites `sessions/iter-001/manifest.json`. Verified against the
source: `dispatch.py:335-350` reads the old manifest and merges `agents` /
`started_at` under goal:s28, and `cli.py:522-526` only reads. The data-loss
half of the finding is therefore false and is struck; the surviving half --
that no `L<loop>.<nn>` id is formatted, parsed or allocated anywhere in
`driver.sh`/`dispatch.py`/`cli.py`, and that iteration numbering always
restarts at 1 -- is confirmed independently by the sibling run
`experiment:a00-ff8eb71d-f812bc`, which is why the verdict stays on the
disproved side rather than becoming pending. Both runs are now listed in
`evidence_runs`; the kid had left the field absent under a decisive verdict.
<!-- THOUGHT:END -->
