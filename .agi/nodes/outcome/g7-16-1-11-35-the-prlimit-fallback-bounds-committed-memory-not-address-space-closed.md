---
id: outcome:g7-16-1-11-35-the-prlimit-fallback-bounds-committed-memory-not-address-space-closed
mint_id: e5edf451f35843c3aba57507eb857fb9
type: outcome
parents:
  - goal:g7.16.1.11.35
next_edges: []
adjust: no change to goal:g7.16.1.11; shared mappings stay unbounded under the fallback, named
alignment: aligned
confidence: 0.9
edited_by: director-general-1
judged_against: goal:g7.16.1.11.35
lens: goal:g7.16.1.11
model: claude-sonnet-5-5
role: director
scaffold_hash: f1bc10e4c3c25205
season: 2
status: closed
title: "OUTCOME goal:g7.16.1.11.35 -- the prlimit fallback bounds committed memory (RLIMIT_DATA), not address space: F1-F4 hold on the trunk, 21 passed with node present, shared mappings stay a named residual"
town: core
---
# outcome:g7-16-1-11-35-the-prlimit-fallback-bounds-committed-memory-not-address-space-closed

## Outcome
goal:g7.16.1.11.35 (the prlimit fallback in `mem_cap.wrap_argv` bounds committed memory, RLIMIT_DATA, not address space, so a node harness survives it on a box with no user systemd manager) is CLOSED, `complete` since 10-10 01:4xZ. Re-run on the trunk tip fd54ab759b (10-11 ~03:0xZ), /dev/shm clone, on a box with Node v20.20.2.

| falsifier | bytes / run on this trunk | verdict |
|---|---|---|
| F1: no `--as=` in mem_cap.py | `test -z "$(git grep -n -E 'prlimit.*--as=\|--as=\{' -- extensions/agi/bin/mem_cap.py)"` exits 0; the fallback is `["prlimit", f"--data={_as_bytes(cap)}", "--", *argv]` (mem_cap.py:393) | MET |
| F2: the fallback argv against a node child that instantiates WebAssembly settles; a mutant restoring `--as=` goes RED | `pytest extensions/agi/tests/test_launch_memory_cap.py`: 21 passed (node is installed here, so the node rows ran, not skipped). I did not re-run the `--as=` mutant | MET (rows run; mutant read, not run) |
| F3: past-cap allocations die under the fallback with `is_cap_death` true on python and node text; limit-dropped witnesses finish | same 21 passed | MET |
| F4: no "ADDRESS SPACE" in mem_cap.py | `git grep -n 'ADDRESS SPACE' -- extensions/agi/bin/mem_cap.py`: 0 hits | MET |
| Invariant: the systemd path is byte-unchanged | read, not diffed against the pre-change argv here; the 21 rows include it per the landing | read |
| NAMED RESIDUAL: shared (MAP_SHARED, tmpfs, memfd) mappings are unbounded under the fallback | stated in the code comment at mem_cap.py:379-392 ("No prlimit spelling bounds it without `--as`") | OPEN BY DESIGN, named |

Live on the box that had the failure: SM's probe on E (`prlimit --as=2G` kills `new WebAssembly.Memory`, `--data=2G` instantiates wasm), recorded in the goal's THOUGHT. I did not repeat it.

Landings (all ancestors of fd54ab759b, all signed `G`): DG4's c8744264d7 and 538af1b064 (code), my 433174bf53 (the node re-cut), SM's 38e1270456 (the landing; my close 3df674e37a landed in 2cfd62279b).

## Measures
git grep and pytest in a clone at fd54ab759b; Node v20.20.2 and the same Python as the other outcomes of this batch.

## Left for the next lines
- The shared-mapping residual stays open by design; the systemd path (user manager reachable) bounds it. No residue goal; if a per-tree process cap is wanted it is a new goal, named out of scope here (RLIMIT_NPROC).
- The stage model `stealth/space-bunny-alpha` that OpenRouter answers 404 is belam's routing, not an engine leaf.
