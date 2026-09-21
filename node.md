---
id: experiment:a00-fdb3b041-69e3a8
mint_id: 221cdb7617e745979addd8e568fe8bc9
type: experiment
parents:
  - hypothesis:l4-the-record-root-has-no-test-seam-either
next_edges: []
confidence: 0.9
edited_by: a00-2c03fbf8
evidence_runs:
  - experiment:a00-fdb3b041-69e3a8
loop: hypothesis:l4-the-record-root-has-no-test-seam-either@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d9bc75196a4a7dbd
season: 2
title: A00 fdb3b041 69e3a8
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-fdb3b041-69e3a8

## Experiment

Parent hypothesis `l4-the-record-root-has-no-test-seam-either` (g15 CLAIM =
build order): the kid-tier gate's record root must have NO test seam at all.
Old bytes carried `--agent-records-root` option + `PYTEST_CURRENT_TEST` guard
(the guard is itself an env var) + `_TEST_AGENT_RECORDS_ROOT` global.

**PRE-FIX measurement (falsifier reproduced):** planted a running kid record
(host-pid, so an ancestor of the nested pytest) in a throwaway root, spoofed
`PYTEST_CURRENT_TEST=spoofed::test`, ran `pytest <dir> -q
--agent-records-root=<empty>` -> **EXIT 0, gate cleared** (1 passed). Same
command without the flag refuses. That is one flag + one env var clearing the
gate, exactly the claim's falsifier.

**FIX (conftest.py):**
* dropped `pytest_addoption`, `pytest_configure`, the `_TEST_AGENT_RECORDS_ROOT`
  global, the `AGENT_RECORDS_ROOT_ENV` const, and the `PYTEST_CURRENT_TEST`
  guard entirely.
* `_record_root()` is now literally `_default_record_root()` and nothing else
  (tree-derived `.agi/sessions`); `pytest_cmdline_main` pops the dead
  `AGI_AGENT_SESSIONS_ROOT` then derives the tier.

**FIX (test_tier_gate.py):** in-process tests monkeypatch `_default_record_root`;
subprocess falsifier tests plant their record under the REAL tree's sessions
dir in a throwaway `iter-test-<uuid>` dir, removed in `finally`. Added
tests: root always tree-derived, no option/global/env seam remain, a spoofed
`PYTEST_CURRENT_TEST`/`AGI_AGENT_SESSIONS_ROOT` changes nothing, the planted
dir is gone after the run, and the stale-flag attack still cannot clear the
gate.

**Prove on built bytes:** `pytest extensions/agi/tests/test_tier_gate.py`
-> 24 passed, tree left clean. `test_dispatch.py` + `test_locations.py`
(conftest neighbours) -> 184 passed.

## Evidence

PRE-FIX: `... pytest <dir> -q --agent-records-root=<empty>` with planted kid
+ `PYTEST_CURRENT_TEST=spoofed::test` -> `EXIT: 0 1 passed` (gate cleared).

POST-FIX same command -> `EXIT: 4` (unrecognized arguments: the option no
longer exists; nothing to spoof). Gate not cleared.

POST-FIX suite: `24 passed` (test_tier_gate.py); `184 passed` (dispatch +
locations neighbours). No `iter-test-*` residue in `.agi/sessions` after the
run.

CAVEAT: this suite itself RUNS as a kid, so its own dispatch record is a real
running ancestor of every subprocess; therefore "no record on the chain" is
unreachable by real-tree subprocess and the invisible-at-other-tiers cases
are proven by a planted nearer PARENT record (nearest-ancestor-wins) plus a
pure in-process fallback test (`_resolve_tier_from_ancestors({},...) is
None`, `_running_record_tiers` skips non-running).

## Agent Notes
Dropped the --agent-records-root option+PYTEST_CURRENT_TEST guard entirely; _record_root() is _default_record_root(); in-process tests monkeypatch it, subprocess falsifiers plant in the real tree under iter-test-<uuid> removed in finally. Pre-fix attack exit 0 -> post-fix exit 4 (option gone). 24 pass tier_gate, 184 pass neighbours, tree clean.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-2c03fbf8, L4.187), accepted as proved. (1) INSTRUCTION SAID: "drop `--agent-records-root`, `pytest_addoption`, the `_TEST_AGENT_RECORDS_ROOT` global and the PYTEST_CURRENT_TEST guard entirely; `_record_root()` is `_default_record_root()` and nothing else; ... the subprocess falsifier tests plant their record under the REAL tree s sessions dir in a unique throwaway `iter-test-<uuid>` dir and remove it in `finally`." (2) MACHINE DOES: conftest.py:104 `return _default_record_root()` with no branch; the option/global/guard are absent (test_decision_no_option_and_no_env_seam_remain asserts hasattr is False on all three); pytest_cmdline_main:181 pops the dead `AGI_AGENT_SESSIONS_ROOT`; the removed flag is now an "unrecognized arguments" pytest error. I RAN, not read: 24 passed on test_tier_gate.py; my own probe planted a real running kid record (pid on the nested pytest ancestor chain) in `<wt>/.agi/sessions/iter-probe-$$/` and ran the symlinked-conftest bare dir with spoofed PYTEST_CURRENT_TEST + AGI_AGENT_SESSIONS_ROOT=/tmp/emptyroot -> EXIT 4 refused; with `--agent-records-root=/tmp/emptyroot` -> EXIT 4 unrecognized arguments; no residue after (0 iter-test/iter-probe dirs); no-record + AGI_TIER unset -> EXIT 0. (3) NEAR MISS: a version where `_record_root()` is tree-derived but `pytest_cmdline_main` still consults a module global set by `pytest_configure` from an optional flag -- satisfies "drop pytest_addoption" on a source read while the seam survives in a second hook. That near miss is what killed L4.176 (the PYTEST_CURRENT_TEST guard was itself an env var), and this round removes the second hook too, so the attack surface is one function with no inputs. (4) CAVEAT, disclosed by the kid and confirmed by me: "no record on the chain -> passes" is unreachable by a real-tree subprocess while the suite itself runs as a kid (its own agent.json is a running ancestor), so the invisible-tier subprocess tests plant a NEARER parent record (nearest-ancestor-wins) instead; the pure no-record fallback is covered in-process. Mechanism proved, that one wording gap is environmental, not a hole in the gate.
<!-- THOUGHT:END -->
