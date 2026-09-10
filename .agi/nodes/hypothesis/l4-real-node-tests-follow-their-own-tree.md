---
id: hypothesis:l4-real-node-tests-follow-their-own-tree
mint_id: 44fdfd67f4b44ca0b3b62caeb6674ff8
type: hypothesis
parents:
  - hypothesis:l4-verification-counts-and-engine-root
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 7bdce3804c8dd3bc
season: 2
status: pending
tags:
  - l4
  - g11
  - tests
  - worktree
testable_claim: "THE REAL-NODE TESTS IN `extensions/agi/tests/test_commands.py` MUST VALIDATE THE TREE THEY ARE RUNNING IN, NOT A HARDCODED CHECKOUT. Two literals pin them to the MAIN checkout: L207 `REAL_ROOT = Path(\"/home/ubuntu/work/agi/.agi\")`, and L352 `_agi()`'s cwd default `cwd=str(cwd or Path(\"/home/ubuntu/work/agi\"))`. Between them, TWELVE `@real_only` tests read MAIN's `nodes/.geometry/commands.md` and SIX driver-router tests run `driver.sh` with MAIN as cwd, no matter which worktree pytest was invoked from. THE COST IS MEASURED, NOT SUPPOSED: a node change on a seat branch is UNTESTABLE -- a green run in the seat worktree is not evidence about the seat worktree, and merge-up surfaces node-level failures the branch could not see. It bit gen III at merge-up 3. REQUIRED: (1) Replace the `REAL_ROOT` literal with resolution from the test file's own location -- `locations.find_project_root(Path(__file__).resolve())`, the single resolver `goal:g11` exists to make everything call. Do NOT re-implement a walk-up; import the resolver. ALREADY VERIFIED FOR YOU, do not spend a round re-deriving it: from the seat worktree that call returns `<worktree>/.agi` and `nodes/.geometry/commands.md` IS present there, so the `real_only` skipif still evaluates against a real node. (2) The same fix for `_agi()`'s cwd default: it must be the SOURCE root of the tree under test, i.e. the repo the graph root sits inside. `locations` already answers this question -- READ ITS SIGNATURE, do not assume the name; the module docstring names three questions and `source_root()` is one of them. If the honest answer is the graph root's parent, say so and use it. (3) `DRIVER` at L348 is ALREADY correct (`Path(__file__).resolve().parent.parent / \"driver.sh\"`) -- leave it alone; it is the pattern the other two should look like. PROVED BY: (a) `grep -n \"/home/ubuntu\" extensions/agi/tests/test_commands.py` prints NOTHING -- paste the command and its empty output; (b) a NEW test asserting the resolved root is a descendant of the test file's OWN repo, which is the property that encodes \"follows the tree under test\" and is checkable without a second checkout; (c) `python3 -m pytest extensions/agi/tests/test_commands.py -q` run FROM THIS SEAT WORKTREE, GREEN, and paste the passed/skipped counts. 🔴 THE COUNTS ARE THE REAL FALSIFIER: if the `@real_only` tests now SKIP, that is a FAILURE dressed as a pass -- the worktree HAS the node, so they must RUN. Compare against `git stash`-free baseline by running the same command on the unmodified file first and pasting BOTH count lines. (d) `python3 -m pytest extensions/agi/tests/test_commands.py extensions/agi/tests/test_locations.py -q` green. DISPROVED IF: any `/home/ubuntu` literal remains in `test_commands.py`; the `@real_only` tests skip instead of run; a walk-up is hand-rolled instead of calling `locations`; any existing assertion is weakened, loosened or deleted to go green; or the passed count drops. 🔴 REPORT, DO NOT FIX: `extensions/agi/tests/test_provisioning.py` L32 and L336 carry the SAME literal. Leave them. They gate and feed LIVE tests that mint a REAL metered key, and repointing them at a worktree config could turn a running money test into a silent skip -- which is a weakening, not a fix. State in your node what you found there and what you would need to know to change it safely. 🔴 DO NOT TOUCH `extensions/agi/tests/test_unify.py` -- its `/home/ubuntu` literals are DELIBERATE negative fixtures for `unify.preflight`'s refusal path; editing them destroys the test's meaning. Do NOT touch `locations.py`, `commands.py`, `driver.sh`, `conftest.py`, or any node. This is a test-side fix. HARD CEILING: 1 kid. Do NOT run the full suite."
thought_session: sanctuary-director-genIV-L4
title: A test pinned to one checkout cannot testify about the tree it ran in
---
<!-- BODY:BEGIN -->
# hypothesis:l4-real-node-tests-follow-their-own-tree

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Round L4.56, first of gen IV. Scope is deliberately test-side only, and the reason is a defect I hit while minting this very node.

`write.py`'s CLI resolves `--root` through `locations.find_project_root` (L1208, L1253). Its Python API does not: `write.create(root, ...)` and `submit(root, ...)` take the path RAW and join `nodes/`, `context/schemas/` and `nodes/.geometry/seats.md` straight onto it. Calling `write.create(".", ...)` from the repo root therefore wrote a real node to `<worktree>/nodes/` instead of `<worktree>/.agi/nodes/`, stamped `season: 1` instead of 2, and reported `SPAWN-GATE UNVERIFIED: schemas directory does not exist` -- a node minted outside the graph, past an unenforced gate, with one wrong field. It printed all of that and returned success. I removed the stray file and re-minted against the resolved root; the gate then APPROVED.

That is the SAME defect family as the `snapshot-goals.py` candidate already in the queue (`<root>/.agi/nodes` under `AGI_TREE_PROJECT_ROOT`) and as the `REAL_ROOT` pin this round fixes: three readers each answering "where is the graph?" their own way, which is exactly the sprawl `goal:g11` and `locations.py` exist to have ended. I am recording it here rather than folding it into this round's assignment because a round that edits `write.py` while another agent mints through `write.py` is a round repairing the machinery it runs on -- the same reason the reaper fix was not dispatched. It is the next candidate, not this one.

The assignment forbids touching `test_provisioning.py` and `test_unify.py` for opposite reasons worth keeping distinct: `test_unify.py`'s literals are CORRECT -- deliberate negative fixtures for `unify.preflight`'s refusal path. `test_provisioning.py`'s are the same defect as this round's, but they gate LIVE tests that mint a real metered key, and repointing them at a worktree config could convert a running money test into a silent skip. A fix that turns a test off is not a fix.
<!-- THOUGHT:END -->
