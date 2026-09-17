---
id: experiment:a00-9807ae1f-90fa06
mint_id: bb4b81125bdd449ab80a4792b65e7f84
type: experiment
parents:
  - hypothesis:l4-the-done-tier-gate-resolves-its-sessions-root-through-the-registered-resolver-and-never-reads-the-live-checkout-under-pytest
next_edges: []
confidence: 0.8
edited_by: a00-9807ae1f
evidence_runs:
  - experiment:a00-9807ae1f-90fa06
line_ceiling: 15
loop: hypothesis:l4-the-done-tier-gate-resolves-its-sessions-root-through-the-registered-resolver-and-never-reads-the-live-checkout-under-pytest@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 22
profile: balanced
role: kid
scaffold_hash: 2abfdc3e340f2ad5
season: 2
title: "narrowed done-tier-gate root: resolve from invoking tree via sessions_dir, refuse only a scratch nested under the live graph"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-9807ae1f-90fa06

## Experiment

BUILD ORDER (g15 claim implements behaviour, does not just measure). Started from the PRE-FIX tree (HEAD cf8973d68, prior SM.99 fix HELD/not merged). Implemented the NARROWED done-tier-gate root fix:

**Claim 1 (resolve from invoking tree through the registered resolver).** `_default_record_root()` in `tests/conftest.py` now resolves from `Path.cwd()` (the invoking tree), not a walk-up from `Path(__file__)` (the engine file), and the JOIN goes through the registered resolver `_PROD_SESSIONS_DIR = locations.sessions_dir`, captured BEFORE the autouse fixture rebinds `locations.sessions_dir` under tmp (WRITE-rehome) — so the tier-gate READ always sees the real join. This closes the measured leak: a fixture run whose cwd is a throwaway tree no longer ascends into the live `.agi/sessions`.

**Claim 2 (narrowed plain-scratch refusal).** New `locations.refuse_live_sessions_from_plain_scratch(sessions_root)` refused a session root landing on the live checkout ONLY when the invocation is a genuine scratch — `Path.cwd()` a proper DESCENDANT of the resolved live graph root (nested under `.agi/sessions`, etc.) — never a real checkout source-tree run. The too-broad predecessor refused any cwd without a `.git` AT ITSELF, which wrongly tripped legitimate nested pytest subprocesses invoked from a checkout SUBDIRECTORY (cwd=extensions/agi, `.git` up-tree): the 4 named full-suite regressions.

**Reproduction/verification of the 4 named regressions (too-broad bytes, branch 7d2d3cfc4, prior SM.99):** director finding cf8973d68 measured them; I confirmed the root cause by tracing — the two differential children (`test_rotate::...stands_the_stub_down`, `test_stream_master...flag_survives`) run `pytest` with `cwd=extensions/agi` (a source sibling, no `.git` AT cwd), so the too-broad `(cwd/".git").exists()` refusal fired. My narrowed guard passes them (verified).

## Evidence

- `test_tier_gate.py`: 43 passed — includes the two kept guard tests `test_throwaway_nested_under_live_agi_never_reads_live_sessions` (claim 1+3: no live-root path, no `tier-gate: phantom`, refused before any scan) and `test_plain_scratch_refusal_fires_only_under_the_live_graph` (claim 2: scratch nested under the live graph refuses BY NAME; non-live join silent).
- The 4 named guard regressions: `test_stream_master...flag_survives` and `test_rotate...stands_the_stub_down` PASS with the narrowed guard.
- FULL SUITE `python3 -m pytest <all 182 test files> -q`: **5152 passed, 2 failed, 16 skipped** (667s). The 2 failures are PRE-EXISTING and guard-independent, proven by removing the guard call entirely (dispatch still fails):
  1. `test_dispatch.py::test_openrouter_preflight_prints_the_sub_floor_notice_before_the_account_refusal` — a pending sibling test (a00-93b7761e) whose strict `spawned == []` mock captures dispatch-path `locations.git_common_root` git Popen calls; fails on base with the guard fully absent.
  2. `test_evidence_gate.py::test_no_live_node_carries_an_out_of_range_lean` — a sibling graph node `a00-6e4cec62-f1256a.md` carries `verdict: inconclusive_lean_disproved` (missing the `:N` percent), which the hygiene scan flags; unrelated to this code.
- Production line measure: `git diff --numstat` locations.py +12, conftest.py +10 = **22 gross added** (ceiling 15 → 1.47×, disclosed; under the 2x hard-stop of 30).
- Note: the pre-fix tree already had a real live phantom record at `.agi/sessions/iter-L3.39/rescued-kid-logs/.../agent.json pid=1459751 (dead)`; the suite's legitimate scan announces it on stderr once — gate trace, not a failure, and not my change.

## Agent Notes
Narrowed done-tier-gate root fix built: resolve from invoking tree via registered sessions_dir resolver, refuse only a scratch nested under the live graph. 43 tier-gate tests + both kept guard tests + the 4 named regressions pass. Full suite 5152 passed / 2 failed (both PRE-EXISTING, proven guard-independent: a pending sibling dispatch test's strict spawned==[] mock captures dispatch-path git calls; and a sibling malformed graph node verdict). 22 gross prod lines vs 15 ceiling (disclosed).
