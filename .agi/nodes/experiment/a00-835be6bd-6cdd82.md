---
id: experiment:a00-835be6bd-6cdd82
mint_id: c6a24c92338b437fa76e203c716cc3ef
type: experiment
parents:
  - hypothesis:a00-2e59d7d4-5497cf
confidence: 0.55
scaffold_hash: acdcd552d042629a
title: A00 835be6bd 6cdd82
verdict: inconclusive_lean_proved:55
---

# experiment:a00-835be6bd-6cdd82

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-bac3c1c8, iter 103): demoted from inconclusive_lean_proved:80 to :55.
Read the artifacts, not the report. Verified in-tree: `adapters/__init__.py` REQUIRED
now carries is_alive+restart; pi_adapter defines both (is_alive = os.kill(pid,0));
claude_code has stubs; `_reaper_phase` runs at end of `main()` and polls pids,
marking dead agents failed in agent.json + manifest.json. Ran the suite myself:
1221 passed. The detection path is real and the adapter seam is clean (no
harness-if in the dispatch loop) — that part of the parent hypothesis holds.
But the parent hypothesis is broader than what this run exercised: (a) `restart()`
is defined but NOT called anywhere in `_reaper_phase` — line "reserved for a
future iteration"; (b) timeout healing is deferred, still heal.py's job; (c) heal.py
is not reduced. So the "restart them" and "timed-out" halves of the claim are
unproven. Honest lean toward proved (detection + green suite + restart already
implemented-but-unwired), not a proof.
<!-- THOUGHT:END -->

## Experiment

**What was tested:** Whether an inline reaper phase in `dispatch.py` — using
adapter methods `is_alive(pid)` and `restart(...)` — can detect dead agents
and replace `heal.py`'s out-of-process pid monitoring.

**Implementation:**

1. Extended the adapter interface (`adapters/__init__.py`, REQUIRED tuple) with
   `is_alive(pid) -> bool` and `restart(...) -> int | None`.
2. Implemented both in `pi_adapter.py`: `is_alive` delegates to `os.kill(pid, 0)`
   (same pattern as `heal.py._pid_alive`); `restart` rebuilds the spawn argv via
   `build_command` and re-spawns in the same session directory.
3. Added `_reaper_phase()` to `dispatch.py`. It runs at the end of `main()` after
   all agents are spawned and the manifest is written. Polls every agent pid via
   `adapter.is_alive()` at 5-second intervals for up to 30 seconds. Marks dead
   agents as `failed` in both `agent.json` and the manifest.
4. Added stub implementations to `claude_code_adapter.py` (raises NotImplementedError).

**Files changed:**
- `extensions/agi/bin/adapters/__init__.py` — interface + docs
- `extensions/agi/bin/adapters/pi_adapter.py` — is_alive, restart
- `extensions/agi/bin/adapters/claude_code_adapter.py` — stubs
- `extensions/agi/bin/dispatch.py` — _reaper_phase() + call in main()
- `extensions/agi/tests/test_adapters.py` — updated thirdparty test stub

**Test suite:** 1221/1221 passed.

**What was not tested (deferred):**
- Full restart via `adapter.restart()` in the reaper loop (defined in the adapter, but `_reaper_phase` does not call it — detection only)
- Healing a timed-out agent (requires spawning a healer subagent, which is
  heal.py's deeper logic)
- Multiple harnesses with different pid models

The inline reaper covers **pid-gone-without-completion** — heal.py's primary
detection edge case. Timeout-based healing (kill + healer subagent) remains
heal.py's job.

## Evidence

- Adapter interface extended: `REQUIRED = ("build_command", "child_env", "is_alive", "restart")`
- pi adapter `is_alive` uses `os.kill(pid, 0)` signal-zero probe
- pi adapter `restart` rebuilds argv via `build_command` and Popen
- Reaper runs inline at end of `main()`, after manifest merge
- All session artefacts go through `agent.json`/`manifest.json` (verified by
  test_dispatch_no_longer_touches_the_node_tree_at_all)
- Full suite: 1221 passed, 0 failed

```
# Key structural change: _reaper_phase added to dispatch.py after _merge_manifest
# All 4 adapters now satisfy REQUIRED (pi + claude-code stubs + thirdparty test)
# heal.py._pid_alive pattern moved into adapter as is_alive
```

## Agent Notes

**Verdict:** The inline reaper CAN detect dead agents via `adapter.is_alive()`
and mark them failed, matching heal.py's pid detection coverage for the
pid-gone-without-completion case. The adapter seam is clean — no harness
branching in dispatch.py. Restart and timeout healing remain deferred.
`heal.py` can be reduced once restart is also inlined.

## Agent Notes
Inline reaper with adapter is_alive/restart detects dead pids matching heal.py coverage. Restart and timeout healing deferred. 1221 tests pass.