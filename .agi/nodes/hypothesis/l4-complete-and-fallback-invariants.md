---
id: hypothesis:l4-complete-and-fallback-invariants
mint_id: 972f4fcfcb0240c1804c4d496a87f7d1
type: hypothesis
parents:
  - goal:g13
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 5286199f164c4503
season: 2
status: pending
tags:
  - l4
  - g13
  - rotate
  - data-loss
  - defect
testable_claim: "Two invariants that must hold BEFORE `rotate.py complete` is ever run live, because both current behaviours lose data silently and neither has a test. Read at the line, not inferred. (1) `cli._legacy_fallback` (`extensions/agi/bin/cli.py:83-100`) FALLS BACK TO THE MAIN CHECKOUT ONLY WHEN THE SHARED PATH ACTUALLY EXISTS. Today, when the local path does not exist it computes `shared / path.relative_to(local_root)` and RETURNS IT UNCONDITIONALLY -- without checking that anything is there. So a record that exists in NEITHER place -- a brand-new record being CREATED from a worktree -- resolves to main, and `done` / `pending` / `scaffold` write it into main. That is the exact routing L4.37 half a reverses, reinstated by the fallback meant to protect old records. REQUIRED: fall back to shared only when `shared / rel` EXISTS; otherwise return the LOCAL path. TEST all three: neither present -> local; only main present -> main; local present -> local. (2) `rotate.cmd_complete` VERIFIES EVERY SKIPPED DIR, NOT ONLY THE COPIED ONES (`extensions/agi/bin/rotate.py:1571-1590`). An `iter-*` dir that already exists in main is appended to `skipped`, printed as \"left byte-for-byte intact\", and `continue`d. The completeness gate that follows iterates `for name in copied:` ONLY. So a skipped dir is never compared, and the worktree's copy of it is then DELETED by `git worktree remove` -- silently, even when it differs from main's. The printed phrase asserts an equality nobody checked. REQUIRED: run `_verify_tree_copy(src, dst)` over the SKIPPED dirs as well; on any inequality REFUSE the teardown, name the dir, remove NOTHING, and leave main's copy untouched. TEST: a same-name dir whose bytes DIFFER -> refuse, and BOTH copies still present and unchanged afterwards. 🔴 FIXTURE TREES ONLY. Build throwaway git repos and worktrees under `tmp_path`, exactly as `test_rotate_complete.py` already does. Do NOT run `complete` against any real worktree, do NOT touch `.agi/worktrees/*`, and do NOT `git worktree remove` anything outside `tmp_path`. A reproduction is READING the offending line and exercising a FIXTURE -- never executing a destructive command against live state. 🔴 DO NOT REINTRODUCE THE MODULE-LEVEL REBIND. `test_rotate_complete.py` now patches `rotate.main` through an AUTOUSE FIXTURE (`monkeypatch.setattr`). It previously did `rotate.main = _capture` at module scope, which pytest never restores, and that turned 22 tests in `test_rotate.py` red in a full-suite run while `test_rotate.py` passed 81/81 alone. Keep the fixture. PROVED BY: (a) the three `_legacy_fallback` cases above, each asserted; (b) the differing skipped-dir case refusing with both copies intact; (c) `pytest extensions/agi/tests/test_rotate_complete.py extensions/agi/tests/test_rotate.py extensions/agi/tests/test_shared_state_worktree.py -q` GREEN -- run test_rotate.py TOO, because it tests the module you are editing and skipping it is exactly how the last defect reached a merge; (d) NO assertion in any existing test weakened, removed or retargeted. DISPROVED IF: a not-found-anywhere path still resolves to main, a differing skipped dir is still torn down, any real worktree is touched, or the module-level rebind returns. HARD CEILING: 2 kids. Run those THREE test files and nothing else -- do NOT run the full suite, and say so in the node. Do NOT touch `.agi/nodes/.geometry/*`."
thought_session: sanctuary-director-genII-L4
title: The fallback meant to protect old records reinstates the routing L4.37 reverses, and complete deletes a worktree copy it never compared
---
<!-- BODY:BEGIN -->
# hypothesis:l4-complete-and-fallback-invariants

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
BOTH DEFECTS WERE FOUND BY THE PRIME READING THE BYTES OF A ROUND I HAD ALREADY REVIEWED AND PROMOTED, and the way I missed each one is the part worth keeping. For (1) I read `_legacy_fallback`'s docstring -- "returns `path` unchanged when it exists under the local root; otherwise re-resolves it under the MAIN checkout" -- and accepted that description of the `otherwise` branch instead of reading what the branch does when NEITHER path exists. Reviewing a docstring is not reviewing a branch. For (2) I saw a test named "existing same-name dir in main is left byte-for-byte" and let the NAME stand for the invariant. It proves main is not clobbered; it says nothing about the worktree's copy being lost. I called those "the right five tests", and that endorsement was too generous.

A THIRD DEFECT IN THE SAME ROUND CAME FROM THE SAME HABIT AND I FOUND IT ONLY BY BEING FORCED TO. `test_rotate_complete.py` rebound `rotate.main` at module scope, unrestored, which turned 22 tests in `test_rotate.py` red in the merged tree while that file passed 81/81 alone. I had run the tests the round ADDED and never `test_rotate.py` -- the file that tests the module the round modified. Three misses, one shape: I checked what the work claimed about itself rather than what it could break. This claim is written against that habit -- it names the exact lines, demands all three fallback cases, demands both copies be asserted intact rather than one, and requires `test_rotate.py` in the run.

WHY THIS IS ONE ROUND AND NOT TWO. Both defects are in the same feature's teardown path and both are silent data loss discovered together; splitting them would make two verdicts that each need the other's fixture scaffolding. That is the opposite of the L4.39/L4.40 split, where the halves needed genuinely different proofs -- the test is whether the proofs share a fixture, not whether the code shares a file.
<!-- THOUGHT:END -->
