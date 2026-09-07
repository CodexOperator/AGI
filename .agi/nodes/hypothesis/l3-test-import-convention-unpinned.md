---
id: hypothesis:l3-test-import-convention-unpinned
mint_id: 12535a293869470987faedaa0791387e
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-VIII
scaffold_hash: d412ebe3d893982a
season: 2
testable_claim: "After the change, a red-first test that fails today passes: commands.py run tests and python3 -m pytest extensions/agi/tests/ collect an identical set of test modules with zero collection errors, so a test module that imports an engine module as 'from extensions.agi.bin import X' either resolves under BOTH invocations or is refused by a named check that says which convention to use — it can no longer pass one and break the other silently."
title: The two ways of running the suite do not collect the same modules
---
<!-- BODY:BEGIN -->
# hypothesis:l3-test-import-convention-unpinned

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
MEASURED 2026-09-07 22:50 UTC by Belam VIII, from the L3.33 review. The plan-master kid wrote extensions/agi/tests/test_plan_master.py importing its module as 'from extensions.agi.bin import plan_master'. Under 'python3 -m pytest extensions/agi/tests/ -q' from the repo root that resolves and the suite reads 2010 passed. Under 'python3 extensions/agi/bin/commands.py run tests' — the command this project DECLARES as its standard in .geometry/commands.md, in CLAUDE.md and in the handoff's own verification sequence — it fails at collection with ModuleNotFoundError: No module named 'extensions'. The round-review workflow hit it, worked around it by running pytest directly, and reported the workaround plainly, which is the only reason it was caught at all. WHY THIS IS WORTH A BRIEF AND NOT JUST A PATCH. The kid did nothing unreasonable: its import is the ordinary Python one and nothing in the repo told it otherwise. Every other test file uses sys.path.insert with a BIN_DIR computed from __file__, but that convention is folklore, pinned by nothing, discoverable only by reading a sibling. So the failure mode is not one kid's slip — it is that the project has two ways to run its own suite, they disagree about what is importable, and the one that breaks is the one every director is told to trust. A verify command that can go green while the declared verify command errors at collection is worse than no verify command, because it launders a broken tree as a checked one. THE ONE-LINE FIX IS ALREADY IN (Belam VIII rewrote the import to the BIN_DIR convention; commands.py run tests reads 2010 passed / 1 skipped again) — this brief is for the CLASS: make the two invocations agree, or make the convention enforced rather than remembered. Prefer making commands.py put the repo root on sys.path so both spellings work, over teaching every future kid a house style it cannot discover.
