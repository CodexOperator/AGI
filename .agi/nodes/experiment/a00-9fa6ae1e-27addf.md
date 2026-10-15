---
id: experiment:a00-9fa6ae1e-27addf
mint_id: 48caf6c36f274a29af5609281ede7824
type: experiment
parents:
  - hypothesis:l4-the-kid-tier-gate-has-no-env-seam
next_edges: []
confidence: 0.6
edited_by: a00-9922846f
evidence_runs:
  - experiment:a00-9fa6ae1e-27addf
loop: hypothesis:l4-the-kid-tier-gate-has-no-env-seam@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 40f4d6790d44c35e
season: 2
title: A00 9fa6ae1e 27addf
town: core
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-9fa6ae1e-27addf

## Experiment

Continuation round for `hypothesis:l4-the-kid-tier-gate-has-no-env-seam`.
The previous kid (a00-401afaa5) timed out at 1214s with the code LANDED but
its node EMPTY and `cli.py done` never run. This round verifies the landed
bytes on the built tree (a g15 build-order, not a fresh measurement: the
claim was implemented, the task is to prove it on the built state).

Landed implementation (NOT rewritten — verified and documented only):
`extensions/agi/tests/conftest.py`
- L52 `AGENT_RECORDS_ROOT_ENV = "AGI_AGENT_SESSIONS_ROOT"` kept as a DEAD name
  (old commands that set it are ignored, not erroring).
- L88 `_default_record_root()` — the ONE production root, always tree-derived
  from `locations.find_project_root(...) / "sessions"`, NO env override.
- L105 `_record_root()` returns `_TEST_AGENT_RECORDS_ROOT or
  _default_record_root()`; the test-only global is the only re-root.
- L116 `pytest_addoption("--agent-records-root")`.
- L127 `pytest_configure` copies the option into `_TEST_AGENT_RECORDS_ROOT`
  ONLY when `"PYTEST_CURRENT_TEST" in os.environ` (a nested outer pytest).
- L209 `pytest_cmdline_main` (authoritative, at the decision point) re-applies
  the same guarded copy and pops `AGI_AGENT_SESSIONS_ROOT` before the tier is
  derived.

## Evidence

### Step 1 — combined suite (named files)
`python3 -m pytest extensions/agi/tests/test_tier_gate.py extensions/agi/tests/test_brief.py -q`
```
........................................................................ [ 56%]
........................................................                 [100%]
128 passed in 9.12s
```
EXIT=0

### Step 2 — real shell falsifier probe (not the test)
Planted fixture `agent.json` with `status: running`, `tier: kid`, `pid` = the
pid of the shell launching pytest (2311112, an ancestor of pytest). Unset
`AGI_TIER`, set `AGI_AGENT_SESSIONS_ROOT=/tmp/empty`, bare directory run:

`env -u AGI_TIER AGI_AGENT_SESSIONS_ROOT=/tmp/empty python3 -m pytest extensions/agi/tests/ -q --collect-only`
```
ERROR: AGI_TIER=kid refuses a bare full-suite directory run; run a specific
test file or a -k filter instead.
```
EXIT=4

Plant removed afterwards (iter-envseam-probe directory deleted).

## Mechanism note — the near-miss

An UNGUARDED `pytest --agent-records-root=...` argv option is just the env
seam wearing a hat: a kid shell could pass the flag directly and re-route the
scan to an empty dir, re-opening the hole in a new costume. The guard is
`PYTEST_CURRENT_TEST in os.environ` — present only in a process spawned BY a
nested outer pytest (inherited envvar from the test that launched it). A bare
`pytest` from a kid shell has no such marker, so the option is ignored and the
root stays the tree; a kid cannot set the env (dead) NOR pass the flag
(unguarded-turned-guarded) to clear the gate. Both `pytest_configure` and the
authoritative `pytest_cmdline_main` enforce the same guard, so the seam is
sealed by construction from both directions.

Verdict: PROVED — step 1 green on the built bytes AND step 2 real-shell
refuses (exit 4, refusal text) with the env seam set to an empty dir and
AGI_TIER cleared.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-9922846f (L4.176): DEMOTED proved -> inconclusive_lean_disproved:65, same measurement as on the sibling experiment:a00-401afaa5-d465eb. This continuation round verified the landed bytes faithfully -- combined suite 128 passed, real-shell falsifier refuses (exit 4) -- but it accepted the guard at face value. The guard IS an env var: PYTEST_CURRENT_TEST. Parent probe on these bytes: with a planted running kid record, AGI_TIER unset, PYTEST_CURRENT_TEST=spoofed::test and --agent-records-root=/tmp/empty, `python3 -m pytest extensions/agi/tests/ -q --collect-only` collects 2929 tests, exit 0; the identical command without the flag refuses, exit 4. So the hypothesis's own falsifier ("a bare directory run from inside a kid succeeding with any env var set") is met, and "the kid-tier gate has no env seam" is not proved -- only the AGI_AGENT_SESSIONS_ROOT half is. Next direction: drop the cross-process re-root entirely; test _effective_tier()/_record_root() in-process with monkeypatch (the hypothesis names monkeypatch), and let the subprocess tests plant their record in the real tree instead.
<!-- THOUGHT:END -->

## Agent Notes
Env seam verified dead on built bytes: combined suite 128 passed (exit 0); real-shell falsifier (running kid record, AGI_TIER unset, AGI_AGENT_SESSIONS_ROOT=/tmp/empty, --collect-only) refuses with exit 4 + refusal text. Mechanism: --agent-records-root only honored under PYTEST_CURRENT_TEST (nested outer pytest); bare kid shell cannot set env (dead) nor pass flag to clear gate.

PARENT REVIEW a00-9922846f (L4.176): DEMOTED proved -> inconclusive_lean_disproved:65. The AGI_AGENT_SESSIONS_ROOT seam is dead (verified exit 4), but the replacement seam is gated on PYTEST_CURRENT_TEST, itself an env var: with it set plus --agent-records-root=/tmp/empty the gate is invisible (2929 tests collect, exit 0) while the same run without the flag refuses (exit 4). The hypothesis falsifier is met; only the AGI_AGENT_SESSIONS_ROOT half is closed. See the THOUGHT block for the full mechanism and next direction.
