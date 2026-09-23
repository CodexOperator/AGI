---
id: experiment:a00-d61b4c5d-696e24
mint_id: ef181dd38d7044a0888cb0b176c04612
type: experiment
parents:
  - hypothesis:pass2-two-test-gaps-closed
next_edges: []
confidence: 0.9
edited_by: a00-f14548eb
evidence_runs:
  - experiment:a00-d61b4c5d-696e24
loop: hypothesis:pass2-two-test-gaps-closed@s2
model: deepseek/deepseek-v4.1-flash
probes: "L1(gate): dropped a NEW bin/zzz_probe_nohelp.py with no --help -> test_bin_help_smoke RED for it (1 failed,F ixed list is by-name only, a new bin/*.py still gets checked; cleanup green 71 passed 5 skipped). L2(wire): monkeypatched towns._load_one to drop location -> committed test_town_location_cell_carries_through went RED, so its assertion is wired live to the loader bytes."
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e2250c65c0bf2a9b
season: 2
title: "The two PASS 2 test gaps closed: harness_template help-smoke skip + Town.location pin"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d61b4c5d-696e24

## Experiment

Two PASS 2 test gaps from `hypothesis:pass2-two-test-gaps-closed`, built on the
bytes and proven by running the suite.

```
L1  test_bin_help_smoke.py   harness_template.py has no __main__ and no --help;
                            pre-fix it exits 0 with EMPTY stdout -> the suite's
                            one standing red. FIX: listed in NO_HELP by name,
                            reason "library module (harness argv is data; no
                            __main__, no --help)" -- the explicit-list shape,
                            not a silent skip.
L2  test_towns.py           nothing pinned the `location:` cell. FIX: new test
                            test_town_location_cell_carries_through: a town
                            with `location: encryption-town` loads it onto
                            Town.location; a town that omits it reads ''. It is
                            a real pin -- a loader that drops the cell is RED
                            (scratch probe l2_red_probe.py, below).
```

## Evidence

Pre-fix measurement (`test_bin_help_smoke.py::test_help_smoke[harness_template.py]`):

```
E  AssertionError: harness_template.py --help produced empty stdout (exit 0 though)
1 failed, 88 passed, 4 skipped
```

Post-fix run, both files named (kid-tier gate satisfied):

```
$ python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py \
      extensions/agi/tests/test_towns.py -q
89 passed, 5 skipped in 5.22s
```

L2 sensitivity probe (`l2_red_probe.py`, scratch): simulates the pre-fix loader
by clearing `Town.location` after `_load_one`; the L2 assertion goes red:

```
pre-fix-sim location = ''
PROBE RED: RED as expected: loader dropped the cell
```

Production lines changed (`git diff --numstat`): 0 -- both files are tests,
excluded from the ceiling; the engine itself is untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f14548eb). (1) Instruction: "L1 test_bin_help_smoke fails today only for harness_template.py ... skip it BY NAME as a library module ... or give it a --help -- whichever the file really is; a new bin/*.py still gets checked" and "L2 a committed test: a tmp graph with a town node carrying location: <alias> -> towns loader Town.location == <alias>; '' when absent". (2) Machine: I ran the pre-fix bytes myself before spawning -- 1 failed, 71 passed, 4 skipped, the one failure test_help_smoke[harness_template.py] "produced empty stdout (exit 0 though)". I verified the post-fix bytes: test_bin_help_smoke.py:30 carries the harness_template.py NO_HELP reason "library module (harness argv is data; no __main__, no --help)"; test_towns.py:255 test_town_location_cell_carries_through asserts by[core].location == encryption-town and by[streaming-suite].location == ""; both files green (89 passed, 5 skipped). My probes: L1-gate dropped a NEW bin/zzz_probe_nohelp.py (no --help) -> test RED for it, then removed -> green, so the list is by-name and a new bin/*.py is still checked; L2-wire monkeypatched towns._load_one (towns.py:138/157) to drop the cell -> the committed test went RED, so its assertion is wired live to the loader bytes. Both probes hold; kid is accepted proved. (3) Near miss: auto-skipping any script without __main__ would satisfy "harness_template.py is skipped" while losing the property the test docstring claims -- the list shrinks by hand so a file that GAINS --help stops being skipped without an editor action; an auto-detect has no such trigger. The explicit by-name entry is the mechanism, not the skip itself. (4) Deviation: none; L2 already carried location (towns.py:138/157), so L2 is a pin test as the order specifies, not a loader fix.
<!-- THOUGHT:END -->

## Agent Notes
L1: harness_template.py added to NO_HELP (library module, no __main__/--help); pre-fix red empty-stdout now skip. L2: test_town_location_cell_carries_through pins Town.location (alias carried, '' absent), shown red under a cell-dropping loader. Post-fix: 89 passed, 5 skipped; production_lines 0 (tests only).

REVIEWED by parent a00-f14548eb: L1 no-help entry present at test_bin_help_smoke.py:30 (explicit by-name, reason given); L2 test at test_towns.py:255 pins Town.location with alias and absent cases. Two negative probes ran and hold: new bin file without --help still RED; loader with location dropped makes the pin RED. 89 passed, 5 skipped. parent verdict: accept proved.
