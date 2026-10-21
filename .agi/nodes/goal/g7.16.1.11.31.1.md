---
id: goal:g7.16.1.11.31.1
mint_id: f2523f787fdf4e60b243c2d4c80fd895
type: goal
parents:
  - goal:g7.16.1.11.31
next_edges: []
confidence: 0.5
edited_by: director-general-3
goal_id: G7.16.1.11.31.1
goal_kind: subgoal
origin: goal
seeds: []
tags: []
season: 3
status: complete
title: "G7.16.1.11.31.1: test_warm_load_second_call_fast is green on a loaded box when nothing is broken -- its fixed-ms threshold becomes load-aware, or the test moves to a perf lane"
town: core
---
# goal:g7.16.1.11.31.1

## Why this exists
goal:g7.16.1.11.31 (the engine FULL suite has a baseline, a named owner for each remaining red): at L27 (SM gen 44, 03:22Z 10-16) the council banked 3/3 that `extensions/agi/tests/graph_core/test_warm_load.py::test_warm_load_second_call_fast` is RED on the LIVE trunk. SM measured it solo at 03:18Z: 6.09-6.54 ms against the < 5.0 ms bound at load average 5.5. So a fixed-ms threshold on a loaded box reports the trunk suite red when nothing is broken. It already takes the best of 5 samples (the SL2#24 merge-up), and that is not enough at this load.

## Target end-state
The council's words, via SM: "Fix: load-aware, or a perf lane." The council designs which.

## Invariants
- A genuinely slow warm path still fails the test or its lane.

## Falsifier
1. `python3 -B -m pytest extensions/agi/tests/graph_core/test_warm_load.py::test_warm_load_second_call_fast` exits 0 on the live trunk (a counting spy loader: 1 cold get + 5 warm gets -> the loader ran once and the cache hit five times; counted, not timed), AND the same file run against a COPIED tree whose `cache.get` never hits (it calls the loader every time) FAILS with `loader called 6x over 1 cold + 5 warm gets`. The in-file mutant `test_warm_load_fw1_mutant_that_always_calls_the_loader_is_red` runs the same check on a subclass.
2. Negative: `grep -nE '< 5\.0|<= 1ms|perf_counter|import time|time\.time|monotonic' extensions/agi/tests/graph_core/test_warm_load.py` has zero hits (the file asserts it on its own text, with the needles built from pieces).
Dropped by the design's own rule (rho = min(warm)/min(cold), worst 0.441 > 0.4): Fw2 (a load-aware ratio) and Fw5.

## Out of scope
The other reds on goal:g7.16.1.11.31.

## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 (belam 03:2xZ 10-16): cut on the council's BANK 3/3 (SM L27 mail 03:22Z). The parent is .31, the suite-baseline goal; it had no children, so this is .31.1, season 3. belam adds no design (owner 10-15: "we always let council do design work first").
v2 (director-general-3 10-16, council design 3/3 alive 03:27:20Z, SM placement 03:27:44Z): BUILT in extensions/agi/tests/graph_core/test_warm_load.py only (cache.py untouched). Cause, from the bytes: get() runs directory_digest(base) (os.walk + read_bytes + sha256 of every file) on EVERY call before the lookup, so a hit costs D and a miss D + L; the old fixed 5.0 ms bound timed the digest walk, which scales with box load, and its docstring said "<= 1ms" over an assert of "< 5.0". Fw1 (the carrier, no timing): a counting spy loader, 1 cold get + 5 warm gets -> spy calls 1, hits 5; mutant = a get() that always calls the loader -> 6 calls, RED (in-file, deterministic). Fw3: the file holds no "< 5.0", no "<= 1ms", no stopwatch (a test asserts it on its own text). Fw2 DROPPED, Fw5 with it, by the design's own rule: rho = min(warm)/min(cold) over interleaved cold/warm pairs on the test's 20-node tree, 20 pairs per batch, 11 batches at GATE LOAD (load 8-10, nice 10, the box running SM's gates): 0.393 0.387 0.441 | 0.345 0.394 0.404 0.401 0.418 0.341 0.389 0.387; worst 0.441 > 0.4. The QUIET batch was not taken (SM 03:29:44Z: a quiet batch can only add a number, never lower the worst). NO tree growth to manufacture separation (D and L scale together). Digest speed is NOT pinned by this goal: a slower digest raises both arms; if the owner wants it pinned that is a separate bank for a perf lane. GOAL FALSIFIER, 03:57Z 10-16, 10 solo runs each, nice 10, one at a time: load 6.3-6.5, agi.slice 4586 MiB at the start (the gate: < 4600) and 4575-4649 MiB across the 20 runs (SM's gates and my own runs moved it); real file 10/10 pass; the same file against a COPIED tree whose cache.get never hits (always calls the loader) 10/10 fail with 'loader called 6x'. (An earlier mutant attempt via PYTHONPATH read 0/10 because extensions/agi/conftest.py inserts the real src at sys.path[0]; that is why the mutant is a copied tree.)
v3 (director-general-3 10-21, the CLOSE, on the falsifier as written (skill agi-goal §2); SM ask 14:13Z, council APPROVE 3/3 14:10:20Z): Fw1 and Fw3 RE-RUN at 3443b86b88 (belam's L37 merge on core/season3/main), on `git archive` exports of extensions/agi in a scratch dir, nice 10, one at a time, env -u TMUX: the real file's test_warm_load_second_call_fast 10/10 pass; the same file in a COPIED tree whose cache.get never hits (the hit branch replaced by `if False:`) 10/10 FAIL with 'AssertionError: loader called 6x over 1 cold + 5 warm gets'; the whole test_warm_load.py 9 passed; the Fw3 grep 0 hits. Box at the end of the runs: load 7.4, agi.slice anon+shmem 2941 MiB. GATE102 FULL on the land 3642842faf = merge-tree(4bd6d1bd7f, 412b1f9f27): 9257 passed, 0 failed, 44 skipped, 26 xfailed, ALL 60 lanes 0 FAIL (SM 14:07Z). Both falsifiers as written pass, so status complete; the Falsifier section was cut from the council's design at this close (it read 'None yet'), Fw2 and Fw5 are recorded in it as DROPPED, and nothing was rewritten to fit what was built.
<!-- THOUGHT:END -->
