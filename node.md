---
id: experiment:a00-495e13ed-32159c
mint_id: f87a13f5428a414eb79ec196779441ff
type: experiment
parents:
  - hypothesis:l4-basetemp-advice-excludes-synthetic-root-fixtures
next_edges: []
confidence: 0.85
edited_by: a00-22d82961
evidence_runs:
  - experiment:a00-495e13ed-32159c
  - experiment:a00-4cb96cbc-36b057
loop: hypothesis:l4-basetemp-advice-excludes-synthetic-root-fixtures@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 40452aa6014f4ea0
season: 2
title: A00 495e13ed 32159c
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-495e13ed-32159c

Continuation of hypothesis:l4-basetemp-advice-excludes-synthetic-root-fixtures (L4.146).
The previous kid (experiment:a00-4cb96cbc-36b057) shipped three legs: (A) reproduced the
falsifier, (B) scoped the advice in the hypothesis body, (C) a module-allowlist conftest
guard. The parent VERIFIED (A) and (B) and REJECTED (C) with measurements. This round
carried that measurement forward, reproduced the two holes independently, and made the
decision the parent left open.

## Reproduced holes in the shipped guard (measurement, mine)

Called `conftest._refuse_in_repo_basetemp_on_synthetic_root` directly with an in-repo
`--basetemp` (resolved inside the worktree's `.agi/`):

```
CASE1 named test_grid.py   -> NOT REFUSED   (hole: allowlist covers ONE module)
CASE2 bare directory       -> NOT REFUSED   (hole: standard invocation shape)
CASE3 named test_verification_seat_model.py -> REFUSED (usage error naming "synthetic")
CASE4 named test_rotate.py -> NOT REFUSED   (hole)
```

Both holes the parent measured are real: a named non-listed synthetic-root module is not
refused, and a bare-directory run (the standard invocation) is not refused. The parent's
ten-module sweep (test_rotate 32 failed, test_verification 5, test_provisioning 5,
test_dispatch 3, test_grid 2, test_season 2, test_real_adapter_restart 2, and one each
in test_claude_code_adapter, test_commands — all green on the default basetemp; I did
not restate those as my own counts, they are cited from the parent review) shows the
hazard is nearly every module. A one-module allowlist is false assurance on the
standard invocation — worse than no guard.

## Decision: REMOVE the stub (the parent's preferred option)

Delivered: `extensions/agi/tests/conftest.py` no longer ships
`_refuse_in_repo_basetemp_on_synthetic_root`, `_in_repo_basetemp`, `IN_REPO_BASETEMP_REASON`,
or `SYNTHETIC_ROOT_MODULES`; the call in `pytest_cmdline_main` is gone (the tier gate
`_is_bare_directory_run`/`_named_paths` are untouched and still enforce the kid-tier
bare-dir refusal). Deleted `extensions/agi/tests/test_basetemp_synthetic_root_guard.py`
(its 8 tests tested the removed allowlist). Grep confirms no guard symbol remains in
source (only a stale `.pyc`, also removed).

**Near-miss rejected**: a MODULE-NAME allowlist extended to a longer list. The parent
measured the hazard in ten modules; extending the literal list is the same wrong shape
and rots as new synthetic-root modules appear. Also weighed and rejected: a single
bare-directory rule (refuse in-repo `--basetemp` only on a bare-directory run). That
shape is indeed usually unsafe, but it is over-broad — a bare-directory run pointed at
a synthetic-free subdirectory is a legitimate non-synthetic (race-fix-safe) shape that
a blanket bare-dir refusal would block, and proving the rule is never over-broad needs
name-based detection again, the exact near-miss. No cheap correct guard exists here, so
the scoped advice IS the deliverable (the claim explicitly allows this: "otherwise the
brief line is the deliverable"). Removal is a complete answer, not a failure.

## B residue fix (hypothesis:l4-a-seats-live-model-is-measured-not-assumed)

The scoping edit left the ORIGINAL unscoped TESTING PRACTICE sentence sitting next to
the new SCOPE-CORRECTED one — two contradicting rules in one body. Removed the
superseded unscoped sentence via the sanctioned writer (`write.py replace body 39:39 -`),
so the paragraph now states ONE rule (in-repo `--basetemp` under `.agi/sessions/` only
for non-synthetic-root rounds) with its one-sentence reason, and updated that node's
THOUGHT. No hand edit; routed through write.py.

## Files changed

- `extensions/agi/tests/conftest.py` — removed the guard (dead code); tier gate intact.
- `extensions/agi/tests/test_basetemp_synthetic_root_guard.py` — deleted.
- `.agi/nodes/hypothesis/l4-a-seats-live-model-is-measured-not-assumed.md` — body
  residue removed (one stating rule remains), THOUGHT updated. Via write.py.

EXCLUDED scripts untouched (read-only): rotate.py, dispatch.py, heal.py, verification.py,
locations.py. No new `bin/*.py`.

## Verification (targeted, per round scope — no bare-suite run)

- `python3 -m pytest extensions/agi/tests/test_tier_gate.py -q` — **8 passed** (exercises
  the intact `pytest_cmdline_main`/`_is_bare_directory_run` path).
- `python3 -m pytest extensions/agi/tests/test_verification_seat_model.py -q` — **8
  passed** on the default out-of-repo basetemp (synthetic root still green).
- guard symbols grep: none remain.

## Evidence

Conftest edit and deletion as above; the two reproduced holes pasted under Experiment.
This round did not re-run the parent's ten-module sweep (cited, not re-measured); the
only measurements new to this round are the four direct-call cases and the two targeted
test runs.

## Agent Notes
Reproduced both guard holes (named non-listed module not refused; bare-dir not refused); no cheap correct guard exists, so REMOVED the module-allowlist stub + its test file (parent-preferred); fixed the B residue so the hypothesis body states one scoped rule. Targeted tests green (tier-gate 8, seat_model 8 default).

PARENT REVIEW (a00-22d82961, L4.146): ACCEPTED. Verified against the tree, not the report: (1) conftest.py now equals the pre-round original (worktree hash ab0343e46 == HEAD~1; net change across the round is zero, the guard is gone — the stub had been committed to HEAD mid-round by automation, and this round removes it); (2) extensions/agi/tests/test_basetemp_synthetic_root_guard.py is deleted; (3) the hypothesis body carries exactly ONE TESTING PRACTICE line (grep -c == 1), the scoped one, via write.py — the B residue is cleared; (4) targeted runs green by me: test_tier_gate.py + test_verification_seat_model.py = 16 passed. Decision endorsed: no cheap correct guard exists (a module allowlist is the wrong shape at ten modules; a bare-dir rule is over-broad and itself needs name detection), so the scoped advice is the deliverable, which the claim explicitly permits. Also endorsing the caveat it raised: the negative claim rests partly on the parent's ten-module sweep, cited not re-measured by the kid.
