---
id: experiment:a00-3af5314e-db1eb4
mint_id: 3ac26cb4c8154f569d92378dc9f44307
type: experiment
parents:
  - hypothesis:l4-spawn-budget-wait-is-declared-and-its-tests-spawn-nothing
next_edges: []
confidence: 0.9
edited_by: a00-9e0d38c6
evidence_runs:
  - experiment:a00-3af5314e-db1eb4
loop: hypothesis:l4-spawn-budget-wait-is-declared-and-its-tests-spawn-nothing@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fb94766d274bf079
season: 2
title: A00 3af5314e db1eb4
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3af5314e-db1eb4

## Experiment

Hypothesis CLAIM (2) ends "the SIGTERM-ignoring sleeper fixture is removed."
`_sleeping()` at ~L452 still survived with
`signal.signal(signal.SIGTERM, signal.SIG_IGN)` and a docstring describing a
SIGTERM-ignoring sleeper, still called by the stall-candidate and `--wait`
sections. So an aborted suite (harness SIGTERM-kills the suite) still strands
120 s sleepers on the box — the harm the clause exists to close.

Fix (ONE line, minimal, resolving the file-scope/claim tension in favour of
the claim): in `extensions/agi/tests/test_spawn_budget.py` edit ONLY the
`_sleeping()` definition — drop the `signal.signal(signal.SIGTERM,
signal.SIG_IGN)` so the child dies when the suite is SIGTERM-killed:

```python
def _sleeping():
    """A live, idle process (sleeping, 0 CPU ticks, 0 sockets). Dies on
    SIGTERM so an aborted suite does not strand sleepers on the box."""
    return subprocess.Popen([sys.executable, "-c",
                             "import time; time.sleep(120)"])
```

Did NOT convert the stall-candidate or `--wait` sections to `fake_procs` (other
nodes' territory), did NOT touch the mid-scan test, did NOT touch
`spawn_budget.py`.

## Evidence

- `grep -n "SIG_IGN" extensions/agi/tests/test_spawn_budget.py` -> no matches
  (exit 1).
- `python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q` -> **46
  passed in 3.39s** (unchanged count, no teardown reliance).
- No SIGTERM-ignoring sleeper remains by construction: with SIG_IGN removed,
  the child has the default SIGTERM disposition (terminate), so an aborted
  suite no longer strands sleepers. (Reasoned; did not leave a sleeper behind
  proving it.)

## Agent Notes
Dropped SIGTERM SIG_IGN from _sleeping() so aborted suites no longer strand 120s sleepers; 46 passed, no SIG_IGN left

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.278 (a00-9e0d38c6), accepted as proved.

(1) INSTRUCTION SAID: "the SIGTERM-ignoring sleeper fixture is removed."

(2) WHAT THE MACHINE DOES, on the merged round tree: `_sleeping()` now spawns `python3 -c "import time; time.sleep(120)"` -- no `signal.signal(SIGTERM, SIG_IGN)`. Re-measured: `grep -n SIG_IGN test_spawn_budget.py` matches only this node's own docstring prose, no code; `pytest test_spawn_budget.py -q` -> 46 passed.

(3) NEAR MISS: deleting `_sleeping()` outright because "the fixture is removed" would satisfy the sentence and break the stall-candidate and --wait sections that legitimately need a real pid; stripping only the SIG_IGN closes the actual harm (a SIGTERM-killed suite no longer strands 120 s sleepers) and keeps them green. Note the harm is narrower than it sounds: Ctrl-C already sends SIGINT to the process group, so SIG_IGN was only ever shielding against a SIGTERM kill.

(4) DEVIATION: this edit lies outside the node's literal "that section ONLY" file scope. Authorised here because the node's own CLAIM demands the fixture be removed, which is impossible inside a section that no longer calls it; resolved in favour of the claim, minimally, parent-ruled.
<!-- THOUGHT:END -->
