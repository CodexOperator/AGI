---
id: experiment:a00-ffe0fd53-7f55fd
mint_id: 76015f9cfc3f4942b73a2ef8d1545bb2
type: experiment
parents:
  - hypothesis:l4-main-root-says-why-it-fell-back-and-only-a-proven-main-read-is-labelled-main
next_edges: []
confidence: 0.9
edited_by: a00-f8597e19
evidence_runs:
  - experiment:a00-ffe0fd53-7f55fd
loop: hypothesis:l4-main-root-says-why-it-fell-back-and-only-a-proven-main-read-is-labelled-main@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 862a71ab88cd4697
season: 2
title: A00 ffe0fd53 7f55fd
town: core
verdict: proved
---
A G15.18 residue build-to-order round (hypothesis:l4-main-root-says-why-it-fell-back-and-only-a-proven-main-read-is-labelled-main). The residue: `rotation_alert._main_root` returned the input `root` for THREE indistinguishable reasons — (i) running in main (git_common_root==root), (ii) `find_project_root(main)` is None, (iii) any exception — and the caller treated every non-identity result the same, so the P7 fallback could label a WORKTREE row `(main checkout)`.

BUILT: `_main_root` now returns `(root, reason)` with reason in {`main`, `resolved`, `unresolved:no-graph-root`, `unresolved:<ExceptionName>`}. The caller maps: reason `main` → single tree `(main checkout)`; reason `resolved` → read main first `(main checkout)`, worktree fallback honestly `(worktree)`; reason `unresolved:*` → read only the worktree row, labelled `(worktree; main unresolved: <why>)` — never `(main checkout)`. P7 intact: no path raises, every case still yields a threshold.

Measured on the bytes via RED-FIRST tests (existing SL3.04 fixtures kept, asserts unchanged):
- test_f: main row 0.4 (resolved) beats stale worktree 0.47 → `(main checkout)`, 0.45 ≥ 0.4 → ROTATION OWED. PASS.
- test_g: main has no row (resolved) → worktree 0.47 `(worktree)`, NO `main checkout`. PASS.
- test_h: non-convention cwd fallback keeps working. PASS.
- NEW test_j: git_common_root RAISES (RuntimeError) → hook exits 0, no traceback, worktree row labelled `(worktree; main unresolved: ` and NOT `(main checkout)`. PASS.
- NEW test_k: git_common_root bounces to a root with no graph → label `(worktree; main unresolved: unresolved:no-graph-root)`, NOT `(main checkout)`. PASS.

Both new tests assert on the emitted SOURCE STRING, giving full four-outcome coverage (main / resolved-main row / resolved-main no row→worktree / unresolved→worktree). Autouse AGI_SEAT delenv retained; whole module green under `env AGI_SEAT=sensei-director`.

## Agent Notes
rotation_alert._main_root returns (root, reason); source label main only for a proven main read; unresolved worktree reads labelled with why. 21/21 rotation tests green incl 2 new unresolved-outcome tests, neighbours green.

Parent review ACCEPTED (a00-f8597e19): residue closed — _main_root returns (root, reason); main label only for a proven main read; unresolved worktree reads labelled with why. Verified on bytes: 21/21 rotation tests green (2 new unresolved-outcome tests j/k assert the source string), 66 neighbour tests green. Parents link resolves. verdict=proved supported by self-cited experiment run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-f8597e19). WHAT THE INSTRUCTION SAID: the target claim demands (1) `_main_root` returns `(root, reason)` in {main, resolved, unresolved:<why>}; (2) the caller labels `(main checkout)` ONLY for a proven main read; (3) P7 kept; (4) the source string asserted for four outcomes. WHAT THE MACHINE ACTUALLY DOES: extensions/agi/hooks/rotation_alert.py:121-161 returns `(root, "main")` on identity (line 155), `(graph, "resolved")` (158), `(root, "unresolved:no-graph-root")` (159), `(root, "unresolved:<ExcName>")` (161 on except). Caller at 219-233 maps main->single `(main checkout)`, resolved->main-then-`(worktree)`, else->`(worktree; main unresolved: <reason>)`. Ran the bytes: test_rotation_alert.py 21 passed; test_session_start_bootstrap.py + test_session_start_seat_pre_spawn.py + test_bin_help_smoke.py 66 passed, 1 skipped. THE NEAR MISS: a two-value return (root-is-main / root-is-not) satisfies the words "returns why" yet cannot distinguish unresolved-no-graph from the worktree fallback, which is exactly the lie the round removes — the child used four named reasons instead, and test_k pins `unresolved:no-graph-root` literally. ACCEPTED as proved; no deviation from a standing rule.
<!-- THOUGHT:END -->
