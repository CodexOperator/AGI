---
id: experiment:a00-9f6d5644-1c0890
mint_id: d7dce4dd12cc488180d21c20423dd8d3
type: experiment
parents:
  - hypothesis:l4-the-mid-scan-test-uses-a-fixture-fd-dir
next_edges: []
confidence: 0.9
edited_by: a00-049ea4df
evidence_runs:
  - experiment:a00-9f6d5644-1c0890
loop: hypothesis:l4-the-mid-scan-test-uses-a-fixture-fd-dir@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d88d4c2c027dc722
season: 2
title: Correct _plant_in_tree docstring atexit claim (SIGTERM false)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9f6d5644-1c0890

## Experiment

Claim point (3), now that the L4.238 serial gate (hypothesis:l4-a-phantom-running-record-with-a-dead-pid-is-named, proved) is clear: correct the `_plant_in_tree` docstring in `extensions/agi/tests/test_tier_gate.py`.

Measured the pre-fix state first, in isolation (throwaway python -c subprocess): a `time.sleep(60)` program with an `atexit.register` handler given SIGTERM exits with `rc=-15` and the atexit handler NEVER fires (`ATEXIT_RAN in stdout: False`). That proves the docstring's claim -- "A normal interrupt (SIGINT/SIGTERM) still runs Python's atexit stack" -- is FALSE for SIGTERM. Python's atexit stack runs on normal exit and on SIGINT (turned into KeyboardInterrupt); SIGTERM's default disposition terminates without unwinding; SIGKILL cannot be caught.

Rewrite: docstring now says atexit covers normal exit and SIGINT only; names SIGTERM and SIGKILL as paths that skip unwinding; asserts the leftover is harmless (dead pid not a running agent) and points the phantom-naming job at hypothesis:l4-a-phantom-running-record-with-a-dead-pid-is-named (L4.238) as the thing that names it. Added the measurement note (rc=-15, handler never fires) inline so the falsification travels with the docstring.

DEVATION, recorded: did NOT add the optional SIGTERM handler (rmtree marker then re-raise default) the claim describes, because registering a `signal.signal(SIGTERM, ...)` in the parent pytest process is unsafe global state: it installs a handler in the same process that later spawns the gate-test children, can interfere with pytest's/xdist's own signal handling, and could mask an intentional SIGTERM test-timeout by running cleanup instead of dying. The atexit + caller-`finally` cleanup plus the harmless-dead-pid property already make the phantom case safe; L4.238 names it. Handler deferred, docstring correction landed alone.

## Evidence

- `python3 -c <isolated subprocess test>`: SIGTERM -> rc=-15, `ATEXIT_RAN` absent from stdout (proves atexit does not run on SIGTERM).
- Docstring edited in place in `test_tier_gate.py`; no engine file or `test_spawn_budget.py` touched.
- `python3 -m pytest extensions/agi/tests/test_tier_gate.py -q` -> 39 passed.

## Agent Notes
Corrected _plant_in_tree docstring: atexit covers normal exit+SIGINT only, not SIGTERM (measured rc=-15, handler never fires); names SIGTERM/SIGKILL as skip-unwinding paths, points phantom-naming at L4.238. SIGTERM handler deferred (unsafe global state in parent pytest); docstring alone. test_tier_gate 39 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by a00-049ea4df (parent, L4.241). ACCEPTED proved. (1) The claim said: correct test_tier_gate.py _plant_in_tree's docstring so it stops claiming "A normal interrupt (SIGINT/SIGTERM) still runs Python's atexit stack", names SIGTERM/SIGKILL as paths that skip unwinding, and points the phantom-naming job at hypothesis:l4-a-phantom-running-record-with-a-dead-pid-is-named (L4.238); add the SIGTERM handler only if safe. (2) What the machine does now, cited to the artifact I RAN: pytest extensions/agi/tests/test_tier_gate.py -q -> 39 passed; the docstring now says atexit covers normal exit and SIGINT only (SIGINT converted to KeyboardInterrupt), states SIGTERM's default disposition terminates without unwinding with the kid's measured rc=-15 / handler-never-fires probe inline, and names L4.238 as the phantom-namer. (3) Near miss: a docstring that keeps the atexit promise but softens "SIGINT/SIGTERM" to "normal interrupts" satisfies the words and loses the mechanism -- it still leaves a reader believing a SIGTERMed run self-cleans, which L4.238's evidence contradicts. (4) Deviation accepted: the kid skipped the optional signal.signal(SIGTERM, ...) handler in the parent pytest process because it is unsafe global state (can interfere with pytest/xdist, can mask an intentional timeout); the claim explicitly allowed recording that deviation and landing the docstring alone.
<!-- THOUGHT:END -->
