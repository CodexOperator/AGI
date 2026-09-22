---
id: experiment:a00-8c0c4372-z-branch-live-pid
mint_id: 6ed3ae012d5e4659ba209306ea4ec27b
type: experiment
parents:
  - hypothesis:a00-149468fd-b66795
next_edges: []
confidence: 0.9
edited_by: a00-8c0c4372
evidence_runs: experiment:a00-8c0c4372-z-branch-live-pid
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 67f344799bf03692
season: 2
testable_claim: A hermetic builtins.open seam reporting stat state Z for a LIVE pid makes grok.is_alive return False (reaching the == "Z" branch), and the same live pid with state S returns True.
title: A hermetic builtins.open seam reaches the zombie Z branch of grok.is_alive for a LIVE pid
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8c0c4372-z-branch-live-pid

The matching run for the Z-branch claim carried by
`hypothesis:a00-149468fd-b66795` (DT.81 MUR R1). The parent's `proved` was
certified by `experiment:a00-f470a6c4-grok-bot-adapter-tests-hermetic`, whose
`testable_claim` is the hermetic/no-real-OS claim, NOT the Z-branch claim.
This experiment's claim is exactly the Z-branch claim, so the parent has a run
whose scope it can cite.

## What was done

The adapter's zombie check is `extensions/agi/bin/adapters/grok_bot_adapter.py:115`:

```python
with open(f"/proc/{pid}/stat", encoding="utf-8") as fh:
    if fh.read().rsplit(") ", 1)[1].split()[0] == "Z":
        return False
```

The test below keeps the pid LIVE (`os.getpid()`) and only monkeypatches
`builtins.open` so the `/proc/<pid>/stat` read reports synthetic state. With
state `Z`, the `== "Z"` line is the ONLY way `is_alive` can return False: the
pid is live, so the fall-through `os.kill(pid, 0)` answers true. The paired
state `S` is the negative control (alive).

## Run

```
env -u TMUX -u TMUX_PANE python3 -m pytest \
  extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider
```

Verbatim output (tip `909e6bcdb` + this branch's test tightenings D3a/D3b):

```
tier-gate: phantom running record /data/work/agi/.agi/worktrees/a00-7f12739a/.agi/sessions/iter-DT.57/a00-81f1fa98/agent.json pid=4060042 (dead) -- skipped
............................                                             [100%]
28 passed in 0.23s
```

The Z/s pair lives in
`test_is_alive_reads_a_zombie_stat_state_as_dead`
(`extensions/agi/tests/test_grok_bot_adapter.py:227`):

```python
monkeypatch.setattr(builtins, "open", _stat_reader(live_pid, "Z"))
assert grok.is_alive(live_pid) is False, (...)
monkeypatch.setattr(builtins, "open", _stat_reader(live_pid, "S"))
assert grok.is_alive(live_pid) is True, (...)
```

## Bite proof (the run is falsifiable)

A COPY of the adapter was built in scratch with the branch character
neutralised, `== "Z"` -> `== "Q"`, at the exact line (copy:
`.agi/sessions/iter-DT.89/a00-8c0c4372/bite/extensions/agi/bin/adapters/grok_bot_adapter.py:115`;
real adapter `extensions/agi/bin/adapters/grok_bot_adapter.py:115`). The real
adapter was never edited.

With the copy on `sys.path`, the SAME test fails:

```
$ cd .../bite && env -u TMUX -u TMUX_PANE python3 -m pytest \
    extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider -k zombie
>       assert grok.is_alive(live_pid) is False, (
            "a live pid whose stat state is Z must read DEAD; if this is True "
            "the == 'Z' branch was removed or inverted")
E       AssertionError: a live pid whose stat state is Z must read DEAD; if this is True the == 'Z' branch was removed or inverted
E       assert True is False
E        +  where True = <function is_alive at 0x7cfedca83d80>(2981782)
E        +    where <function is_alive at 0x7cfedca83d80> = grok.is_alive

extensions/agi/tests/test_grok_bot_adapter.py:227: AssertionError
=========================== short test summary info ============================
FAILED extensions/agi/tests/test_grok_bot_adapter.py::test_is_alive_reads_a_zombie_stat_state_as_dead
1 failed, 27 deselected in 0.26s
```

So the green run above certifies the `== "Z"` branch specifically: remove it
and the run goes red.

## Evidence

- Run: the 28-passed output above, from this branch, command quoted verbatim.
- Bite: Z-neutralised copy fails the same test at the same line.
- Files: `extensions/agi/bin/adapters/grok_bot_adapter.py:113-118` (is_alive),
  `extensions/agi/tests/test_grok_bot_adapter.py:203-235` (reader + test).

## Scope / honesty

The run is hermetic by design: no child process is forked, killed or reaped,
and the pid stays this interpreter's live pid. `os.kill(live_pid, 0)` IS
executed on the alive control paths (a signal-0 self-query -- no state change,
deterministic because the pid cannot exit mid-test); D3a documents this as
intentional and benign (DT.81 MUR R2). It is not a claim about a real zombie
process on a real fork.
