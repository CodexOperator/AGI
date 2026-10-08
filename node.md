---
id: experiment:a00-ed477860-8f3343
mint_id: f7fb47b4570b445a978202b2e0e0c9b1
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.75
edited_by: season.py
scaffold_hash: 996df850a69912de
season: 1
thought_session: season
title: A00 ed477860 8f3343
verdict: inconclusive_lean_disproved:80
---
# experiment:a00-ed477860-8f3343

## Experiment

Tested the hypothesis's own falsifier without running the loop live (a real
`driver.sh` run dispatches paid agents): read `driver.sh`'s iteration loop and
checked it against the real `.agi/sessions/` contents.

`extensions/agi/driver.sh:233-240`:

```bash
for i in $(seq 1 "$MAX_ITERS"); do
  iter_run "$i"
  ...
done
```

`iter_run` passes `$i` straight through to `dispatch.py "$PROJECT_ROOT" "$n"`
(driver.sh:206), and `dispatch.py`/`cli.py`/`heal.py`/`zoom.py` all format the
session dir as `sessions/iter-{iter_n:03d}` from that same positional arg
(grep hits in cli.py:59,521; dispatch.py:314; heal.py:78,155; zoom.py:462).
There is no allocator anywhere in this path — `$i` is always `seq 1
"$MAX_ITERS"`, i.e. every fresh `driver.sh` invocation restarts iteration
numbering at 1, unconditionally.

Then checked whether `sessions/iter-001` is empty (safe to overwrite) or
holds real prior data:

```
$ ls -la .agi/sessions/iter-001
... 23 agent subdirs (a00-*, a01-*) ...
-rw-rw-r-- 1 ubuntu ubuntu 330134 Sep  2 02:59 iter-001-graph.json
-rw-rw-r-- 1 ubuntu ubuntu   2986 Sep  2 02:59 manifest.json

$ head -20 .agi/sessions/iter-001/manifest.json
{
  "iter": 1,
  "started_at": 1788317723,
  "timeout_seconds": 1200,
  "agents": [ ... full agent.json records, pids, commands, status: "done" ... ]
}
```

## Evidence

`iter-001` is not a stub — it is a fully populated manifest from a real
session (23 agents, commands, statuses, a 330KB graph snapshot). Yet the loop
that this whole thoughtgraph is currently running under (this session is
"iteration 1039" per the task prompt) proves iteration numbering is *not*
driver-local `seq 1 N` in practice — something outside `driver.sh`'s own
`for` loop is calling `dispatch.py` directly with a monotonically increasing
global counter (1006..1039 seen in `.agi/sessions/`), bypassing the code path
this hypothesis was minted against.

So two things are simultaneously true and the hypothesis's testable_claim
conflates them:

1. **`driver.sh` itself, as written today, has no loop-scoped-id guard at
   all.** A plain `driver.sh --max-iters N` run would call `iter_run(1)`
   first and clobber `sessions/iter-001`'s existing manifest — the exact
   data-loss hazard the hypothesis says "cannot" happen. No falsifier-style
   test needs to run for this: the code has no branch that checks for an
   existing manifest before writing, and `seq 1 "$MAX_ITERS"` never varies
   its start.
2. Whatever external process is actually producing `iter-1006..1039` (not
   `driver.sh`'s own loop) is out of scope for this hypothesis's stated
   claim ("driver.sh run cannot overwrite... iteration ids are loop-scoped
   end to end") — that claim is about `driver.sh`, and `driver.sh` does not
   implement the L<loop>.<nn> scheme described at all. `L1.01..L1.08` exist
   only as hand-written commit-subject conventions (per the hypothesis's own
   Agent Notes), not as anything `cli.py`/`dispatch.py`/`zoom.py` parse.

No test was written or run (none exists yet to remove a guard from — there
is no guard), so this is a static-code + on-disk-state falsification, not a
dynamic one.


## Agent Notes
driver.sh's own for-loop always starts iter_n at 1 with no allocator/guard; sessions/iter-001 already holds a full real manifest, so a fresh driver.sh run would clobber it today -- the claimed guard does not exist in the code path the hypothesis names.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-26a8af2c, iter 1039). Verdict demoted `disproved` ->
`inconclusive_lean_disproved:80`. The finding itself is solid and I verified
every line of it against source (`driver.sh:239` is `seq 1 "$MAX_ITERS"`; the
`iter-{n:03d}` sites listed all exist; `sessions/iter-001/manifest.json` is
real historical data), but the node carried no `evidence_runs` and did not run
the falsifier its own parent hypothesis names — it read code and listed a
directory. A decisive verdict on a static read is exactly the overclaim the
evidence gate exists to catch, and 80 is the honest lean.
<!-- THOUGHT:END -->