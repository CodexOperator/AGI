---
id: verdict:dg2b4-w1b
mint_id: 9b3623c450024b2080b95a126124a257
type: verdict
parents:
  - experiment:dg2b4-w1b-baseline
  - hypothesis:a-write-is-its-own-commit-behind-the-gate
next_edges: []
confidence: 0.7
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w1b-baseline
scaffold_hash: 273b7ae2709cb394
season: 2
title: "W1b: lean proved at 75 -- write.py makes 0 commits today; a 22-line commit in main() works, but NEVER inside submit() (rotate/send call it on shared posts.md)"
town: core
verdict: inconclusive_lean_proved:75
---
# verdict:dg2b4-w1b

## Verdict: inconclusive_lean_proved:75 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w1b-baseline) | decided by |
|---|---|---|
| (1) gate -> write -> commit by exact path, one call | FALSE: 0 git calls; 8/8 write verbs leave the node dirty | test_write_guard.py::test_b4_w1b_every_write_verb_is_its_own_exact_path_commit |
| (2) --dry-run and a refused gate commit nothing | TRUE today (vacuously: nothing ever commits) | test_write_guard.py::test_b4_w1b_dry_run_and_a_refused_gate_commit_nothing (passing guard, must stay green) |
| (3) verify-suite.lock refuses by name | FALSE: write.py reads no lock | test_write_guard.py::test_b4_w1b_the_suite_lock_refuses_the_commit_by_name |
| (4) never -a, never another post's staged file | TRUE today (vacuously) | the foreign-stage asserts in the first and third rows |

Lean proved: a 22-line prototype in `main()` (ceiling 40) turns every row green. Two traps sit outside the fixture:
- `submit()` is a library that rotate.py:9629 and send.py call on the SHARED posts.md. Put the commit in main() or make it opt-in, never in submit().
- `submit()` also writes unpark carriers (write.py:2387). The goal must say whether they ride the commit or stay out.

The config-cell commit template is not pinned. CORRECTION: none to the line refs. "29 DG1 nodes untracked" is a crash-time count; the handoff db3e22e55 holds 29 files, 26 of them new nodes.
