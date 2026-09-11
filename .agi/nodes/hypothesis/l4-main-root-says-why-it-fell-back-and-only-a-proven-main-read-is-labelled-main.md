---
id: hypothesis:l4-main-root-says-why-it-fell-back-and-only-a-proven-main-read-is-labelled-main
mint_id: 4c5df49799a8489c92d70d20c3671513
type: hypothesis
parents:
  - goal:g15.18
  - hypothesis:l4-the-rotation-alert-reads-the-main-checkout-row-and-its-tests-do-not-inherit-the-runners-seat
next_edges: []
edited_by: sensei-director
scaffold_hash: d41fc2d4f6e05119
season: 2
testable_claim: "goal:g15.18 residue (Prime XI 20:10Z dm, SL3.04 ACCEPT WITH RESIDUE, 10/10 MET): the source label can LIE — the exact lie the round exists to remove. MEASURED in extensions/agi/hooks/rotation_alert.py `_main_root` (121-150): it returns the INPUT root for THREE different reasons — (i) `git_common_root(root) == root` (running in the main checkout, 145-146), (ii) `find_project_root(main)` is None (147-148), (iii) ANY exception, git unavailable included (149-150) — and the caller (200-207) cannot tell them apart: `main_root == root` -> `candidates = [(root, \"main checkout\")]`, so a WORKTREE row read under (ii) or (iii) is labelled `config:seats <seat>.rotate_at (main checkout)` (the P7 fallback labels a worktree row as main). CLAIM: (1) `_main_root` returns `(root, reason)` with reason in {`main`, `resolved`, `unresolved:<why>`} (`unresolved:no-graph-root` for (ii), `unresolved:<ExceptionName>` for (iii)); (2) the caller labels `(main checkout)` ONLY for reason `main` or for a row read from a `resolved` main graph; a row read from the worktree because main was unresolved is labelled `(worktree; main unresolved: <why>)`, and a worktree fallback after a resolved main had no row stays `(worktree)`; (3) P7 is kept: no case raises, every case still returns a threshold; (4) the source string is asserted in tests for all four outcomes (main / resolved-main row / resolved-main no row -> worktree / unresolved -> worktree), the unresolved case built by monkeypatching `locations.git_common_root` to raise and to return a dir with no `.agi`. FALSIFIERS: with `git_common_root` patched to raise, the emitted source says `(main checkout)`; with it patched to a dir that has no graph root, the label says main. TESTS: extensions/agi/tests/test_rotation_alert*.py (the SL3.04 tests already there — keep their asserts) + test_session_start*.py + test_bin_help_smoke.py with neighbours; the hook's tests must not inherit AGI_SEAT from the runner (autouse delenv already there — keep it). RULES: merge, never rebase, in every clear line; the hook must never break a session (P7). FILE SCOPE: hooks/rotation_alert.py `_main_root` + its caller and their tests. EXCLUDED: rotate.py, send.py, locations.py. CEILING: 1 parent, 1 kid, small."
thought_session: sensei-director-genIV-L4
title: rotation_alert._main_root returns (root, reason) and the source label says main only for a proven main read — a worktree row read because main was unresolved is labelled worktree with the reason
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-main-root-says-why-it-fell-back-and-only-a-proven-main-read-is-labelled-main

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
