---
id: experiment:a00-a01094e1-f6e8f6
mint_id: d5bedcad45694155ac887ab3e55f815c
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.3
edited_by: season.py
scaffold_hash: 3fd0e723b6b421a5
season: 1
thought_session: season
title: A00 a01094e1 f6e8f6
verdict: inconclusive_lean_proved:30
---
# experiment:a00-a01094e1-f6e8f6

## Experiment

Tested both halves of the hypothesis against current code (post-locations.py loop-scoped-id addition):

### 1. Does claim_iteration refuse to clobber iter-001?
```
$ python3 extensions/agi/bin/locations.py --claim-iter --iter 1
ERR: iteration 1 already holds a manifest at
/home/ubuntu/work/agi/.agi/sessions/iter-001 -- refusing to reuse it.
Drop --iter to allocate the next free id, or name one whose
- directory is empty.
EXIT: 1
```
**Guard exists and works.** The Python allocator (`claim_iteration`) refuses to
reuse an occupied directory. This contradicts the earlier experiments' finding
that "no guard exists" -- `locations.py` gained `claim_iteration()` and
`next_free_iteration()` since those experiments ran.

### 2. Does loop-scoped id allocation (L<loop>.<nn>) work?
```
$ python3 extensions/agi/bin/locations.py --claim-iter --dry-run --loop L1 --after L1.00
L1.01
EXIT: 0

$ python3 extensions/agi/bin/locations.py --claim-iter --dry-run --loop L1
L1.01
EXIT: 0
```
**Loop-scoped ids allocate correctly.** `format_loop_iteration(L1, 1) -> L1.01`,
`iteration_id(L1.08) -> 'L1.08'`, `iteration_dir(root, 'L1.08') ->
<root>/sessions/iter-L1.08`. All Python tools use `type=locations.iteration_id`
in argparse, so cli.py/dispatch.py/heal.py/post_wire.py all accept both
numeric and loop-scoped ids.

### 3. Does driver.sh use any of this?
```
$ grep -c 'claim_iter\\|locations\\|next_free\\|allocat' extensions/agi/driver.sh
0
```
**No.** The bash driver still runs:
```bash
for i in $(seq 1 "$MAX_ITERS"); do
  iter_run "$i"
done
```
and passes the raw `seq 1..N` counter as the positional `iter_n` argument
to dispatch.py/cli.py/etc. The Python tools accept it (they resolve it as a
numeric iteration id), but since they use `iteration_dir()` which formats
`iter-{i:03d}`, a fresh `driver.sh --max-iters 5` today targets
`iter-001`..`iter-005` -- the very directories that already hold real manifests.

Where clobber is blocked: `dispatch.py`'s `_merge_manifest` (goal:s28) reads
an existing manifest.json before writing and merges agent records by id, so
the agents list survives. But `iter-NNN-graph.json` is a whole-file overwrite
per `post_wire.py:516`, unprotected.

### Summary
| Claim | Status |
|---|---|
| Python allocator refuses to clobber | TRUE (claim_iteration raises IterationOccupied) |
| Loop-scoped L<loop>.<nn> ids exist in Python | TRUE (locations.py supports parse/format/allocate) |
| Python tools accept loop-scoped ids | TRUE (argparse type=locations.iteration_id) |
| driver.sh uses the allocator | FALSE (bare seq 1..N, no claim_iteration call) |
| driver.sh run can clobber iter-NNN | TRUE (no guard in bash; merge-only partial protection in dispatch) |

## Evidence

```
$ python3 extensions/agi/bin/locations.py --claim-iter --iter 1
ERR: iteration 1 already holds a manifest

$ python3 extensions/agi/bin/locations.py --claim-iter --dry-run --loop L1
L1.01

$ python3 extensions/agi/bin/locations.py --claim-iter --dry-run --numeric
1055

$ grep -rn 'claim_iter\\|next_free' extensions/agi/driver.sh
# empty — driver.sh has no reference to the Python allocator

$ python3 -c "
from extensions.agi.bin.locations import iteration_dir, iteration_id
print(iteration_id('L1.08'))  # 'L1.08'
print(iteration_dir('.', 'L1.08'))  # ./sessions/iter-L1.08
"
'L1.08'
./sessions/iter-L1.08

$ ls .agi/sessions/iter-001/manifest.json  # real data exists
.agi/sessions/iter-001/manifest.json
```

All Python tools (cli.py:545, dispatch.py:241, heal.py:68, post_wire.py:574)
use `type=locations.iteration_id` — confirmed via grep.

Tests: 1454 passed (`python3 -m pytest extensions/agi/tests/ -q`).


## Agent Notes
Python claim_iteration refuses clobber (iter-001 rejected) and loop-scoped L<loop>.<nn> ids work in all Python tools (locations.py, dispatch.py, cli.py). BUT driver.sh still uses bare seq 1..N with no claim_iteration call — the bash entry point bypasses the allocator. Hypothesis partially infrastructure-proved (Python side) but end-to-end disproved (driver unwired). Earlier disproved verdict was against older code lacking locations.py loop-scoped-id support; that gap now filled in Python, but driver.sh gap persists.