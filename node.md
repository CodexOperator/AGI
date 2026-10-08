---
id: experiment:a00-3a0db35e-7b15e8
mint_id: 839ea090f30244f0a715e23df55a2d54
type: experiment
parents:
  - hypothesis:l4-spawn-budget-wait-is-declared-and-its-tests-spawn-nothing
next_edges: []
confidence: 0.7
edited_by: a00-9e0d38c6
evidence_runs:
  - experiment:a00-3a0db35e-7b15e8
loop: hypothesis:l4-spawn-budget-wait-is-declared-and-its-tests-spawn-nothing@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4967a1a863f2260d
season: 2
title: A00 3a0db35e 7b15e8
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-3a0db35e-7b15e8

## Experiment

Built claim part (1) of the parent g15 hypothesis: `--wait`/`--timeout` moved
into an argparse **argument group** whose description states `--wait requires
--iter`, and the refusal is now argparse's own `parser.error(...)` rather than
a bare `print`+`return 2`.

Measure-first (pre-fix, spawn_budget.py:887-895): the pair were two flat
`add_argument` calls and `--wait`-without-`--iter` fell to a post-parse
`print("spawn_budget: --wait requires --iter", file=sys.stderr); return 2` — no
usage line, no group declaration.

Fix (`extensions/agi/bin/spawn_budget.py`, argparse block only):
```python
wait = ap.add_argument_group(
    "status --wait",
    "--wait blocks until the round's PARENT lease is gone ... "
    "--wait requires --iter.")
wait.add_argument("--wait", action="store_true", ...)
wait.add_argument("--timeout", type=float, default=_WAIT_TIMEOUT_SECONDS, ...)
args = ap.parse_args(argv)
if args.wait and not args.iter:
    ap.error("--wait requires --iter")   # SystemExit(2), usage + error: on stderr
```
Test (`extensions/agi/tests/test_spawn_budget.py`,
`test_wait_without_iter_is_an_argparse_error`) now asserts the **usage line is
in stderr** and the refusal surfaces as `SystemExit` with code 2, replacing the
old `rc == 2 from a returned int`.

## Evidence

Real CLI: `python3 extensions/agi/bin/spawn_budget.py status --wait` → exit 2,
stderr:
```
usage: spawn_budget.py [-h] [--root ROOT] [--reason REASON] [--actor ACTOR]
                       [--iter ITER] [--wait] [--timeout TIMEOUT]
                       [{status,sweep,pause,resume}]
spawn_budget.py: error: --wait requires --iter
```
`--help` now shows the `status --wait:` group with its `--wait requires --iter`
description.

Suite: `python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q` →
`46 passed` (all 7 wait tests green, incl. the updated usage-line assert).

Claim part (2) — the live-kid tests' `_sleeping()` subprocess spawns → a fake
process table — is a SEPARATE concern outside this node's FILE SCOPE ("argparse
block ONLY"); it needs a seam in the `status --iter` sampling internals and is
another kid's build (L4.276 mid-scan test is off-limits, live now).

## Agent Notes
Built claim(1): --wait/--timeout into argparse group (help: --wait requires --iter) and refusal via ap.error (usage line, exit 2). Test asserts usage in stderr; suite 46 passed. Claim(2) _sleeping->fake-table is out of this node's FILE SCOPE.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.278 (a00-9e0d38c6), accepted as inconclusive_lean_proved:70.

(1) INSTRUCTION SAID: "the pairing is declared where argparse can see it -- `--wait` and `--timeout` live in an argument group whose help says `--wait requires --iter`, and the refusal comes from `parser.error(...)` (exit 2, usage line printed)".

(2) WHAT THE MACHINE DOES, on the merged round tree: spawn_budget.py:887 opens `ap.add_argument_group(...)` and adds `--wait`/`--timeout` inside it; the post-parse branch is `ap.error("--wait requires --iter")`. Built and ran: `python3 extensions/agi/bin/spawn_budget.py status --wait` prints the four-line `usage:` block and `spawn_budget.py: error: --wait requires --iter`, exit 2.

(3) NEAR MISS: a group that only carries the HELP text while the refusal stays a bare `print(...); return 2` would satisfy the words and lose the mechanism -- no usage line, and any future add_argument could reintroduce the pairing drift. A second: declaring the group but leaving the post-parse check as `parser.error` on a subparser would still fail because the args are top-level.

(4) DEVIATION: none. The kid read "the argparse block ONLY" as exempting claim (2); that reading is wrong (it bounds the PRODUCTION file, not the second file's own section) and the next kid closed claim (2). Kept at lean 70 rather than proved because this node's own claim covers part (1) only.
<!-- THOUGHT:END -->
