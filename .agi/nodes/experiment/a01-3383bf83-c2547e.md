---
id: experiment:a01-3383bf83-c2547e
mint_id: 51001da10a904e1587b14d1d8f66f52f
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.7
scaffold_hash: ce4e7197c257b610
title: A01 3383bf83 c2547e
verdict: inconclusive_lean_disproved:70
---
# experiment:a01-3383bf83-c2547e

## Experiment

Traced every place `driver.sh`, `bin/cli.py`, `bin/dispatch.py` and
`bin/zoom.py` format or parse an iteration id, to check whether the
hypothesis's premise (fresh `driver.sh` run clobbers an existing
`.agi/sessions` manifest because ids are not loop-scoped or allocated) still
holds today.

Findings:
- `extensions/agi/driver.sh:238` drives the whole run with
  `for i in $(seq 1 "$MAX_ITERS"); do iter_run "$i"; done` — `i` always
  restarts at `1` on a fresh invocation. There is no read of the existing
  `sessions/` dir to pick a free id.
- `iter_run` passes that same raw `$n` straight into
  `dispatch.py "$PROJECT_ROOT" "$n"` (driver.sh:217) and
  `cli.py status "$n"` (driver.sh:229).
- `bin/dispatch.py:314` and `bin/cli.py:521,59` both format it as
  `sessions/iter-{args.iter_n:03d}` with no existence check and no loop
  prefix (`L<loop>.<nn>` from the hypothesis's own claim is not implemented
  anywhere in these four files — grepped for `iter-` and for `L\d` prefixing,
  found none).
- `bin/zoom.py:462` reads the same unscoped `iter-{n:03d}` path.

Reproduced the clobber precondition directly against this repo's own
`.agi/sessions`:

```
$ ls .agi/sessions/iter-001
iter-001-graph.json  manifest.json
$ cat .agi/sessions/iter-001/manifest.json | head -c 200
{... real agent dispatch data from a past run ...}
```

`iter-001` already holds a real manifest with real dispatch data. Nothing
in `driver.sh`, `dispatch.py` or `cli.py` stops a fresh
`bash driver.sh --max-iters 1` from writing `iter-001` again — `iter_n=1`
is derived from a bash loop counter, not from the contents of `sessions/`,
so the write is a plain overwrite with no guard, no allocator, and no id
higher than what the loop counter says. This is the exact hazard the
hypothesis names, and confirms it is **still live**: the loop-scoped,
allocate-next-free-id, never-clobber behavior the hypothesis proposes does
not exist yet in the code path that actually runs.

(Separately, iteration ids like `1039`, `L1.09-g13` etc. visible under
`.agi/sessions/` come from a different harness — the pi/CC dispatch layer
that invoked *this* run — not from `driver.sh`'s own loop. That harness
already allocates non-clashing ids by convention/coordination, but
`driver.sh`'s bash loop itself has no such allocator, so the hazard
persists specifically for anyone running `driver.sh` directly.)

## Evidence

```
$ grep -n "iter-" extensions/agi/driver.sh extensions/agi/bin/cli.py \
    extensions/agi/bin/dispatch.py extensions/agi/bin/zoom.py
extensions/agi/bin/cli.py:59:      root / "sessions" / f"iter-{iter_n:03d}" / agent_id / "agent.json"
extensions/agi/bin/cli.py:521:     iter_dir = root / "sessions" / f"iter-{args.iter_n:03d}"
extensions/agi/bin/dispatch.py:5:  Writes session manifest at <project>/sessions/iter-NNN/manifest.json
extensions/agi/bin/dispatch.py:314: iter_dir = root / "sessions" / f"iter-{args.iter_n:03d}"
extensions/agi/bin/zoom.py:462:    sess_dir = root / "sessions" / f"iter-{args.iter_n:03d}" / args.agent_id

$ sed -n '238,244p' extensions/agi/driver.sh
for i in $(seq 1 "$MAX_ITERS"); do
  iter_run "$i"
  ...
done

$ ls .agi/sessions/iter-001
iter-001-graph.json  manifest.json
```

No test in `extensions/agi/tests/` covers this path (searched for
`iter_n`, `iter-00`, `sessions` in the test dir — no clobber-guard test
exists). Ran `python3 -m pytest extensions/agi/tests/ -q` (pre-existing,
unmodified suite) to confirm this investigation did not touch any code:
329 passed, unrelated to this finding.


## Agent Notes
Traced driver.sh/cli.py/dispatch.py/zoom.py: no loop-scoped id, no free-id allocator, no clobber guard exists yet -- driver.sh's own seq-1..N loop restarts at iter-001 every run and would overwrite the real manifest already sitting there. Hazard confirmed still live, fix not yet implemented.
