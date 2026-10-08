---
id: hypothesis:l4-the-sigterm-stale-record-test-waits-on-what-the-child-emits-never-on-wall-clock
mint_id: 6640962ae2e9447ca195aef7a97857ca
type: hypothesis
parents:
  - goal:g6.16
next_edges: []
edited_by: belam
scaffold_hash: d2532344c5ab32b4
season: 2
testable_claim: "belam ruling 13:00Z (suite run 12:50-12:59Z, load 4.0): test_tier_gate.py::test_sigterm_kill_leaves_no_stale_record_under_aborted_subprocess (:542-590 at a51f8deee) failed once inside the full suite (4997/1) and passes alone (0.25 s x2) and 14/14 under four CPU burners - a TIMING BUG in the test, not noise. MECHANISM from the bytes: the child (:553-559) plants the marker via _plant_in_tree (handler installed :~185: rmtree -> SIG_DFL -> re-raise), prints the marker path, then time.sleep(120); the parent then waits on WALL CLOCK twice - (ii) :572-575 polls marker.exists() for 5 s at 50 ms, (iii) :578 proc.wait(timeout=10) after SIGTERM - and only then asserts rc<0 and marker gone (:579-584). Neither wait is on something the child EMITS: the parent infers handler readiness from the printed path and cleanup completion from process exit, and the commands.py summary records no traceback (the failing step is unrecorded). CLAIM, one kid, test file only (tier_gate.py untouched unless the kid proves the gate itself races): (1) the child prints `armed <marker>` only AFTER the handler is installed and `cleaned` from INSIDE the handler after rmtree and before the re-raise; the parent reads those two lines (blocking reads under ONE overall deadline on the observable, e.g. select/poll on the pipe) instead of polling the filesystem and instead of a bare proc.wait timeout, then asserts rc<0 and marker absent; (2) every assertion names its step so a future red names the step in the one-line suite summary; (3) the kid reproduces BEFORE the fix under the suite real conditions (cwd = the .agi graph root exactly as commands.py run tests sets it, the full test file in a loop under load) and records the failing step; after the fix 30 loops green under the same conditions. Falsifier: the reproduction under suite conditions never fails (then the flake is in the gate sweep, not the test: name it and stop) or the fix adds any sleep or a longer timeout. Never a longer sleep (belam)."
thought_session: dissolve-legacy-2026-09-19
title: L4 the sigterm stale record test waits on what the child emits never on wall clock
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-sigterm-stale-record-test-waits-on-what-the-child-emits-never-on-wall-clock

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by master-sensei gen 8 on belam ruling 13:00Z after two granted suite runs (12:50Z red 4997/1 on this test; 13:01Z green 11/11, stamp a51f8deee). (1) INSTRUCTION: "name the mechanism from the bytes (what the test waits on after SIGTERM) and fix it in-loop with a deterministic seam or a bounded wait on the observable, never a longer sleep". (2) MECHANISM: read at :542-590 - two wall-clock waits (5 s marker poll, proc.wait 10 s) stand in for two observables the child could emit (handler armed, marker cleaned); the summary log carries no traceback, so which wait broke is unrecorded; 14/14 pass under four CPU burners, so pure CPU load is not the reproduction - the suite differs by cwd (.agi graph root) and by what runs before it. (3) NEAR MISS: raising the timeouts, or sleeping before SIGTERM - satisfies "passes" and loses the mechanism; ruled out by name. (4) DEVIATION: none; ceiling test file only unless the kid proves the gate sweep itself races, in which case it names it and stops.
<!-- THOUGHT:END -->
