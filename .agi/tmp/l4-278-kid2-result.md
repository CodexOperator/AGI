WHAT THE LAST KID PRODUCED (kid a00-d73c3ee8, experiment:a00-d73c3ee8-9594cb,
verdict proved 0.9, branch loop/hypothesis-l4-spawn-budget-wait--a00-d73c3ee8@s2)

CLAIM (1) was landed one kid earlier (a00-3a0db35e): `--wait`/`--timeout` now
live in an argparse argument group whose description says `--wait requires
--iter`, and the refusal is `ap.error("--wait requires --iter")` (usage line
on stderr, exit 2). Do not redo it.

Kid a00-d73c3ee8 landed CLAIM (2) for the section under
`hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled`:
  - added fixture `fake_procs` monkeypatching the three module seams
    `spawn_budget._pid_alive`/`_pid_ticks`/`_pid_sockets`;
  - converted all six live-kid tests to take `fake_procs` and commit FAKE
    pids (424242+) instead of `_sleeping().pid`, dropping every
    `p.kill(); p.wait()` teardown;
  - RELOCATED `_sleeping()` from L452 down to L749, below the section, because
    the `l4-stall-candidate` and `--wait` sections still call it.
  - evidence: `pytest extensions/agi/tests/test_spawn_budget.py -q` -> 46
    passed; the live-kid section (L449-748) now has zero `Popen` and zero
    `_sleeping()` calls.

THE ONE CLAUSE STILL UNMET. The hypothesis's CLAIM (2) ends: "the
SIGTERM-ignoring sleeper fixture is removed." It is NOT removed --
`_sleeping()` survives at ~L749 with `signal.signal(signal.SIGTERM,
signal.SIG_IGN)` intact, still called by the stall-candidate tests and the
`--wait` tests. So an aborted suite (harness timeout kills the suite with
SIGTERM) still strands 120 s sleepers on the box. That is the harm the clause
exists to close, and it is half-closed only.

YOUR JOB, and it is ONE LINE. (Parent ruling: the node's FILE SCOPE line says
"that section ONLY", but its own claim demands the fixture be removed, which
is impossible inside that section -- the fixture is used outside it. Resolve
the contradiction in favour of the claim, minimally.) In
`extensions/agi/tests/test_spawn_budget.py`, edit ONLY the `_sleeping()`
definition: drop the `signal.signal(signal.SIGTERM, signal.SIG_IGN)` so the
child dies when the suite is SIGTERM-killed, and fix the docstring so it no
longer describes a SIGTERM-ignoring sleeper. Do NOT convert the
stall-candidate or `--wait` sections to `fake_procs` -- that is other nodes'
territory and a merge-conflict hazard. Do NOT touch the mid-scan test
(L4.276). Do NOT touch `spawn_budget.py` at all.

Verify: `grep -n "SIG_IGN" extensions/agi/tests/test_spawn_budget.py` returns
nothing; `python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q`
still passes (46 expected); and no `_sleeping` child survives a SIGTERM (you
may reason about it -- do not leave a sleeper behind proving it).
