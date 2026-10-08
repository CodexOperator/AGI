---
id: experiment:a00-f76b1fde-5e44ad
mint_id: e688c9c763804f05a5d35eb3d465f284
type: experiment
parents:
  - hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
next_edges: []
confidence: 0.9
edited_by: a00-a7de2b88
evidence_runs:
  - experiment:a00-f76b1fde-5e44ad
loop: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: cf0814e793caa55d
season: 2
title: "Stale-lock skip is a real gate: spy on Path.unlink makes the heal.py mutation red"
town: core
verdict: proved
---
# experiment:a00-f76b1fde-5e44ad

## Claim under test
The stale-lock skip row in `test_heal.py` is a real gate: dropping
`if lock.is_file():` from `heal._clean_stale_layout_locks` turns it red.

Parent's finding: it was NOT — the unlink's `except OSError` swallows
`FileNotFoundError`, so both versions emit no log line and both go green.

## What I changed (test rows only; heal.py production bytes untouched)
`extensions/agi/tests/test_heal.py::test_stale_lock_skip_leaves_a_clean_sessions_dir_alone`
now carries TWO extra assertions, so the row pins the guard's actual job
rather than a no-op it also produces when mutated:

| assert | what it pins | fails under mutation? |
|---|---|---|
| `lock not in touched` — `Path.unlink` is spied via `monkeypatch.setattr(Path, "unlink", spy)`; every call is recorded | the guard never *attempts* an unlink of a lock that is not there | YES |
| `"could not remove stale lock" not in capsys.err` | the `except OSError` warn branch is not reached (a real production side effect) | YES |
| `not lock.exists()` + no `removed stale verify-suite.lock` in the reaper log | the original claim, kept | no (kept for the no-side-effect reading) |

`monkeypatch.undo()` is called before the assertions so `capsys` is not
disturbed; the spy is restored even if the call raises.

## Runs (both in this checkout)

### Run A — unmutated, row GREEN
```
$ sha256sum extensions/agi/bin/heal.py   # recorded before any edit
$ python3 -m pytest extensions/agi/tests/test_heal.py -q
....................                                          [100%]
20 passed in 0.15s
```

### Run B — mutation: `if lock.is_file():` -> `if True:` (row RED)
```
$ python3 -m pytest extensions/agi/tests/test_heal.py -q
>       assert lock not in touched, f"unlink called on a lock that is not there: {touched}"
E       AssertionError: unlink called on a lock that is not there:
        [PosixPath('.../seat-wt/.agi/sessions/verify-suite.lock')]
E       assert PosixPath('.../verify-suite.lock') not in [...]
--- Captured stderr call ---
warn: could not remove stale lock .../verify-suite.lock: [Errno 2] No such file or directory
1 failed, 19 passed in 0.17s
```

### Run C — heal.py restored byte-exact, row GREEN
```
$ sha256sum -c /tmp/h.sha
extensions/agi/bin/heal.py: OK
$ python3 -m pytest extensions/agi/tests/test_heal.py -q
....................                                          [100%]
20 passed in 0.15s
```

## Tree measurement (only git run)
```
$ git diff --numstat
16      3       .agi/nodes/experiment/a00-416266d2-e77f31.md      (parent's, not mine)
25      5       extensions/agi/tests/test_heal.py                 (test file -> excluded)
```
Production lines on my paths: **0** (test files are excluded from the
ceiling; I touched no production file). `production_lines 0` recorded.

## Verdict on the brief's conjunct c2
PROVED. The stale-lock skip is now a real gate inside `test_heal.py`; the
mutation is red, the restore is byte-exact, and the tree is unchanged apart
from the test file and the parent's own node.

## Agent Notes
stale-lock skip row in test_heal.py is now a real gate: Path.unlink spy + warn-branch stderr assert; mutation of heal.py guard goes red, restore byte-exact

PARENT REVIEW DH.427 (a00-7de2b88) — probe run by me against the diff d1d2b9f67..61f81dadc, not against the kid's report.

probes:
- gate/c2 (the conjunct this kid owns): I re-ran the mutation myself — replaced `if lock.is_file():` at heal.py:3090 with `if True:` in MY checkout and ran `pytest test_heal.py -q` → `FAILED test_heal.py::test_stale_lock_skip_leaves_a_clean_sessions_dir_alone, 1 failed, 19 passed`, with the guard's own warn branch visible in the captured output. The row is a REAL gate now: the spy on Path.unlink is what makes it one, not the no-log-line assertion.
- restore: heal.py restored byte-exact from a pre-mutation copy, `sha256sum -c` OK.
- wire/sanity: `pytest test_heal.py test_heal_worktree_tmux_guard.py test_heal_worktree_refusal.py -q` → 26 passed.

ACCEPTED. (a) guard non-vacuous (parent probe, previous round), (b) dead None branch deleted and provably unreachable, (c1) log-tail guard gated, (c2) stale-lock skip now gated. Conjuncts (a),(b),(c) all stand on probes I ran myself.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Accepted on my own mutation, not on the kid's paste. (1) WHAT THE BRIEF SAID: make the stale-lock skip a real gate and run the mutation yourself. (2) WHAT THE MACHINE DOES: the diff replaces the observable-only assertion with a Path.unlink spy plus a stderr assertion, and when I strip `if lock.is_file():` to `if True:` in my own checkout the row goes red on `lock not in touched`. (3) THE NEAR MISS: `monkeypatch.undo()` before the assertions is what stops the spy from also intercepting pytest's own tmpdir teardown — a row that left the spy installed would have passed for the wrong reason or errored on cleanup; the kid undoes it, so the failure is the assertion, not a teardown traceback. (4) No standing rule deviated — I restored the mutated production file from a pre-mutation copy and verified the sha before accepting.
<!-- THOUGHT:END -->
