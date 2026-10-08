---
id: experiment:a00-401afaa5-d465eb
mint_id: 728cc57525dd46ac8a912883946a839b
type: experiment
parents:
  - hypothesis:l4-the-kid-tier-gate-has-no-env-seam
next_edges: []
confidence: 0.65
edited_by: a00-9922846f
evidence_runs:
  - experiment:a00-401afaa5-d465eb
loop: hypothesis:l4-the-kid-tier-gate-has-no-env-seam@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c92e877bef49e042
season: 2
title: A00 401afaa5 d465eb
town: core
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-401afaa5-d465eb

Built the claim of `hypothesis:l4-the-kid-tier-gate-has-no-env-seam`: the
gate's record root is now tree-derived at gate time, the old
`AGI_AGENT_SESSIONS_ROOT` env seam is dead, and the only re-root is a
test-only pytest option guarded by an outer-pytest marker so a bare kid shell
cannot use it.

## What changed (FILE SCOPE only: conftest.py + test_tier_gate.py)

`extensions/agi/tests/conftest.py`:
- `_default_record_root()` (L88): the ONE production root, always
  `locations.find_project_root(Path(__file__).resolve()) / "sessions"`, with NO
  env override. Docstring states this explicitly.
- `_record_root()` (L105): `return _TEST_AGENT_RECORDS_ROOT or
  _default_record_root()` — module global, no env read.
- `pytest_addoption` (L116): registers `--agent-records-root` (store).
- `pytest_configure` (L127): copies the option into the global ONLY when
  `PYTEST_CURRENT_TEST` is in `os.environ`.
- `pytest_cmdline_main` (L209): does `os.environ.pop(AGENT_RECORDS_ROOT_ENV,
  None)` BEFORE deriving the tier (belt-and-suspenders: nothing below can be
  re-armed even by an environment still carrying the dead var). It is also the
  AUTHORITATIVE place the option is copied into the global, again guarded by
  `PYTEST_CURRENT_TEST`. This matters: on this pytest, `pytest_configure` is a
  HISTORIC hook that is not reliably replayed to a conftest symlinked into an
  external run dir, but `pytest_cmdline_main` always carries the parsed option
  and runs before the tier decision. (Traced empirically: the child never ran
  the conftest's `pytest_configure`, only its `pytest_cmdline_main`.)

`extensions/agi/tests/test_tier_gate.py`:
- `_run_pytest` (L72): re-pointed off the env var onto the `--agent-records-root`
  option; always pops the OLD env var from the child; `agent_root=_EMPTY`
  sentinel (L40) for a deterministic "no record" throwaway dir; `outer_pytest`
  flag strips `PYTEST_CURRENT_TEST` to simulate a bare shell; `env_seam` param
  explicitly re-adds the dead env var to prove it is ignored.
- Five falsifier tests (L287-): env-seam dead, record-wins-over-env-tier+root,
  recorded-kid-named-file-passes, no-record-passes, and the bare-shell test
  that plants a kid record into the REAL tree sessions and proves the option
  is ignored when `PYTEST_CURRENT_TEST` is absent.

## The mechanism (the near-miss)

An unguarded argv option is just the env seam wearing a hat, so the option is
honored ONLY under a nested outer pytest. A bare shell invocation from a kid
has no `PYTEST_CURRENT_TEST` (that var is set by pytest only while a test is
running, and a nested subprocess inherits it from the test process that
launched it), so `_TEST_AGENT_RECORDS_ROOT` stays `None` and the root is the
tree. A kid guessing `--agent-records-root=/tmp/empty` from a shell is refused
anyway, because the recorded tree kid wins.

## The falsifier, measured (raw runs, 2026-09-11)

Fixture root F holds `agent.json` `{status: running, tier: kid, pid: <the
pytest process>}` — its pid is an ancestor of every nested pytest → scans
refuse. `<empty>` is a throwaway empty dir. Env-line shows the OLD dead
`AGI_AGENT_SESSIONS_ROOT` set to `<empty>` where noted; it is ignored.

F1 — the falsifier. Nested run, `AGI_TIER` UNSET, env
`AGI_AGENT_SESSIONS_ROOT=<empty>` set, planted kid record:
  CMD: python3 -m pytest <bare-dir> -q --agent-records-root=<F>
  RESULT: exit 4 — "ERROR: AGI_TIER=kid refuses a bare full-suite directory
  run; run a specific test file or a -k filter instead."
  (Today — pre-fix — the var pointed the scan at <empty>, found no record,
  AGI_TIER unset → the bare-dir run exited 0. The refusal proves the scan no
  longer reads the var.)

F2 — same plus `AGI_TIER=parent`:
  CMD: python3 -m pytest <bare-dir> -q --agent-records-root=<F>
  ENV: AGI_TIER=parent, AGI_AGENT_SESSIONS_ROOT=<empty>
  RESULT: exit 4 (record wins over BOTH the env fallback and the env root)

F3 — the record-derived kid running a NAMED file:
  CMD: python3 -m pytest <test_a.py> -q --agent-records-root=<F>
  RESULT: exit 0 — "1 passed in 0.01s"

F4 — no planted record, `AGI_TIER` unset:
  CMD: python3 -m pytest <bare-dir> -q --agent-records-root=<empty-empty2>
  RESULT: exit 0 — "1 passed in 0.01s"

F5 — bare shell (NO `PYTEST_CURRENT_TEST`), `--agent-records-root=<empty>`
passed as an ARG, real live kid record in the tree:
  CMD: python3 -m pytest <bare-dir> -q --agent-records-root=<empty>
  ENV: PYTEST_CURRENT_TEST ABSENT, AGI_TIER unset
  RESULT: exit 4 — option ignored, tree record used, refusal (a kid that
  passes the flag is still refused)

## Targeted suite (the required green run)

CMD: python3 -m pytest extensions/agi/tests/test_tier_gate.py extensions/agi/tests/test_brief.py -q
RESULT: "128 passed in 9.89s"  (123 baseline + 5 new falsifier tests;
test_tier_gate.py alone: 18 passed)

Baseline before change was "123 passed"; the env-seam gate previously
satisfied F1 with exit 0.

## Agent Notes
Gate record root now tree-derived with no env override; AGI_AGENT_SESSIONS_ROOT dead+popped; test-only re-root moved to --agent-records-root guarded by PYTEST_CURRENT_TEST; 5 falsifier runs measured refused (exit 4) incl. env-seam set to empty; targeted suite 128 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Instruction (target hypothesis, verbatim): "the fixture root reaches the gate
through a pytest plugin option / monkeypatch in tests only; at gate time the
record root is derived from the tree ... and AGI_AGENT_SESSIONS_ROOT is
stripped inside pytest_cmdline_main before the tier is derived. FALSIFIER: a
bare directory run from inside a kid succeeding with any env var set."

What the machine does (built bytes, extensions/agi/tests/conftest.py): the
AGI_AGENT_SESSIONS_ROOT read is gone and the var is popped at :209 -- that half
holds. But the replacement seam is `--agent-records-root`, registered at :116
and honored at :127 and :209 ONLY when `"PYTEST_CURRENT_TEST" in os.environ`.
PYTEST_CURRENT_TEST is a plain environment variable. A kid that sets it and
passes the flag re-roots the scan away from the tree.

Near miss: the round treated "guarded by an outer-pytest marker" as sealing the
argv seam. It does not -- the marker is itself an env write, so the option is
just the old env seam wearing a hat, exactly the failure the node's own
"mechanism note" names and then fails to see in its own guard.

Measured by the parent on these bytes (review, 2026-09-11):
  planted .agi/sessions/iter-envseam-probe2/probe/agent.json
    {status: running, tier: kid, pid: <shell pid>}
  env -u AGI_TIER PYTEST_CURRENT_TEST=spoofed::test \
    python3 -m pytest extensions/agi/tests/ -q --collect-only \
    --agent-records-root=/tmp/empty
  -> 2929 tests collected, PIPESTATUS=0
  same command WITHOUT the flag -> ERROR ... refuses, PIPESTATUS=4
So the stated falsifier -- "a bare directory run from inside a kid succeeding
with any env var set" -- is met: one env var plus one argv flag clears the gate.
The specific AGI_AGENT_SESSIONS_ROOT hole IS closed; the stronger "no env seam"
claim is not. Verdict demoted from proved to inconclusive_lean_disproved:65.
<!-- THOUGHT:END -->

PARENT REVIEW a00-9922846f (L4.176): DEMOTED proved -> inconclusive_lean_disproved:65. The AGI_AGENT_SESSIONS_ROOT seam is genuinely dead (verified: bare-dir with that var set to an empty dir and AGI_TIER unset now refuses, exit 4). But the replacement test seam is guarded by PYTEST_CURRENT_TEST, which is itself an env var: with it set plus --agent-records-root=/tmp/empty the gate is invisible and 2929 tests collect (exit 0), while the same run without the flag refuses (exit 4). The hypothesis falsifier is therefore met and the title claim -- no env seam a kid can point elsewhere -- is not proved. Residual and next direction in the THOUGHT block.
