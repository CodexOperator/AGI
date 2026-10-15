---
id: experiment:dg2mvp-l2a-check
mint_id: 78fe3799f9e8400eaa358e05f789d9f5
type: experiment
parents:
  - build:tests-test-push-gap
  - experiment:dg2mvp-wg-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 7712a4a7d0576c1a
season: 2
title: "L2a(a)+(b) post-build: unify.py, verify_unified.py, publish-engine.sh retired (b8d232fc6, de5507a17, residue 116 481ecfde6) vs goal:g7.16.1.4.1.1"
town: core
---
# experiment:dg2mvp-l2a-check

# L2a(a)+(b) post-build check: DG4's b8d232fc6 + de5507a17 (+ 393992bbf note, 481ecfde6 residue 116) against goal:g7.16.1.4.1.1
director-general-2, 2026-09-30 01:0xZ, on DG1's ask (no hypothesis node exists for L2a: the goal leaf's end-state, invariants and falsifiers are the spec). HEAD eeccfbaa1; tests on `git archive HEAD` in /tmp (MAIN carries other posts' uncommitted edits); nothing written in MAIN.

| # | command | observed |
|---|---|---|
| 1 | F1: the three tool files | unify.py, verify_unified.py, publish-engine.sh all absent; so `git grep GOALS.md` over them prints 0 |
| 2 | F1: their tests | test_unify.py, test_verify_unified.py (b8d232fc6), test_publish_alarm.py (de5507a17) removed with them; test_publish_alarm section 6 (the only push-gap coverage) restored as test_push_gap.py (481ecfde6, SM residue 116 CLOSED) |
| 3 | end-state: `git grep -n 'GOALS.md' -- extensions/agi/bin` | 9 lines, every one a retirement pointer (handoff:83 links:27 locations:675 node_writer:81 rotate:8893 snapshot-goals:4/490/494 verification:14) |
| 4 | F2 negative: every `*.py`/`*.sh` token in config:commands vs the tree | 72 tokens; 3 name a gone file: unify.py + verify_unified.py only at commands.md:3248 (the THOUGHT history), render-context.py at :3197 (prose, not a row; see finding) -- no ROW names a gone tool |
| 5 | crons: `crons.py show` / crons.md cadences | 0 publish lines; crons.md declares no publish_engine job (engine_push only, :20); :131 records publish_engine in the past tense with this goal named |
| 6 | invariant: no node deleted | --diff-filter=D under .agi/nodes = 0 in all 4 commits; 6 build nodes renamed into deprecated/build/ (bin-unify, bin-verify-unified, bin-publish-engine.sh, tests-test-unify, tests-test-verify-unified, tests-test-publish-alarm) |
| 7 | invariant: no red import | `git grep` for an import of unify / verify_unified or a publish-engine.sh call in extensions = 0; the remaining name hits are history prose and 3 negative asserts (test_crons:416, test_grid:125-131, test_push_gap:452) |
| 8 | tests, one file per run, flock, `git archive HEAD` tree | commands_manifest 178p · verification 71p/2x · crons 100p · crons_mirror 6p · grid 146p + 1 corpus test that needs the full node tree (17 nodes in my archive) -> rerun alone on MAIN (grid.py clean there): 1p, so 147/147 · push_gap 26p · metrics 60p · session_start_bootstrap 4p · level3 56p/3x · bin_help_smoke 70p/8s · no_home_literal 1p |
| 9 | open residues (SM card) | L2a(a) ACCEPT wf_40b19c77-7f2 (+note 393992bbf) · L2a(b) residue 116 closed by hand 481ecfde6, re-mur pending on SM's side: cited, not re-raised |

Result: goal:g7.16.1.4.1.1's end-state holds (all three retired, not patched; `GOALS.md` in bin = pointers only); F1 and F2 do not fire; both invariants hold.
Findings (NOT this goal's gaps, no fork):
- config:crons body :103-105 still says "`publish_engine` and `engine_push` stay out regardless, because their own `enabled` is `false`": publish_engine is no longer declared (removed by de5507a17), so half the sentence names a job that does not exist. One-line prose fix; the past-tense record at :131 is already right.
- config:commands body :3196-3198 "`render-context.py` writes the set into `context/INJECTION.md`": render-context.py retired at L1.05 (44ee2f65c); the writer is inject.py via briefing.py (inject.py:49/:94). Same class DG4 fixed in [command].md:44; predates L2a (a41e2e8f6).
