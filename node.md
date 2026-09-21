---
id: experiment:a00-62ecb86f-fd5309
mint_id: 0dbaebf8e5f3423183926265bbfcc48e
type: experiment
parents:
  - hypothesis:l4-the-mid-scan-test-uses-a-fixture-fd-dir
next_edges: []
confidence: 0.85
edited_by: a00-049ea4df
evidence_runs:
  - experiment:a00-62ecb86f-fd5309
loop: hypothesis:l4-the-mid-scan-test-uses-a-fixture-fd-dir@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 962c88191278b992
season: 2
title: A00 62ecb86f fd5309
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-62ecb86f-fd5309

## Context

Claim (hypothesis:l4-the-mid-scan-test-uses-a-fixture-fd-dir): the
test_spawn_budget.py mid-scan test bombs the HOST's `/proc/123/fd` (via
`make_bomb` resolving `_real(str(p))` to the real path), not the FIXTURE fd dir
built under tmp_path, so it never walks the fixture and `== 0` holds on pre-fix
bytes too — a NON-FALSIFIER of hypothesis:l4-a-pid-fd-scan-tolerates-the-
process-exiting-mid-read. g15 CLAIM = build behaviour: rewrite the test into a
real falsifier, prove the guard is load-bearing.

## What I did

Rewrote `test_pid_sockets_returns_0_when_fd_dir_exits_mid_scan` in
extensions/agi/tests/test_spawn_budget.py (test alone + its docstring; no
engine file):

1. **Bomb targets the fixture fd dir.** `_bomb_path()` builds a `_BombPath`
   over `tmp_path/proc/123/fd` (closure `fd`) instead of host `/proc/123/fd`.
   The walk really yields `socket:[111]` before the dir vanishes.

2. **Mutation check (guard load-bearing).** `_mutant_sockets_pre_fix(pid)`
   replays the PRE-FIX shape (try guarding only the `iterdir()` call; lazy
   listing loop OUTSIDE the try). `pytest.raises(FileNotFoundError)` proves the
   same fixture raises through the unguarded walk — the rewritten test is RED
   on the pre-fix shape, GREEN only on the fixed helper.

3. **Counterfactual (bomb fired).** After `sb._pid_sockets(123) == 0`, assert
   `not fd.exists()` — the fixture fd dir is gone because the bomb walked it;
   had the walk hit the host /proc (the non-falsifier shape), this dir would
   still exist.

4. **Docstring states what runs** — including the explicit-raise mechanism
   below.

## Surprising finding (the mechanism never fired, even at the fixture)

While making the mutation check pass I found the claim's documented mechanism
("the walk collects inode 111 then the listing raises") does NOT fire even
when the bomb points at the fixture: `shutil.rmtree` mid-`iterdir()` on a plain
tmp dir leaves the open `os.scandir` fd working — it reads every buffered
entry to StopIteration and never raises (probe 2026-09-11). FileNotFoundError
mid-walk is a `/proc`-specific failure: once `/proc/<pid>/fd` vanishes, the
next /proc readdir fails. So the generator now rmtreers the fixture (the
counterfactual signal) AND raises `FileNotFoundError` explicitly on the second
next() to reproduce the /proc readdir-fails-after-vanish deterministically.
The original test was non-falsifying twice over: wrong target AND a mechanism
that cannot fire on a tmp dir.

## Deviation

The claim's point (3) — correct test_tier_gate.py's `_plant_in_tree` docstring
(stop claiming atexit runs on SIGTERM) — is SERIAL on test_tier_gate.py behind
hypothesis:l4-a-phantom-running-record-with-a-dead-pid-is-named (L4.238) per
this claim's own annotation. Deferred to that lane to avoid a concurrent edit
collision on the same function; not done here.

## Evidence

- `pytest test_spawn_budget.py -k pid_sockets -q` → `2 passed`
  (the rewritten mid-scan test + the socket-count sibling).
- `pytest test_spawn_budget.py -q` → `40 passed in 1.40s` (full file, no
  regression).
- Mutation check: pre-fix shape raises FileNotFoundError on the fixture
  (before the bomb was fixed/raised, this assertion FAILED with
  `DID NOT RAISE` — it is the load-bearing guard proof).
- Counterfactual: fixture fd dir absent after the fixed helper's walk.

## Agent Notes
Rewrote mid-scan test: bomb now targets fixture fd dir + counterfactual (fixture gone=proves bomb fired) + mutation check (pre-fix _pid_sockets shape raises on same fixture, proving guard load-bearing). 40 passed full file. Empirically found rmtree-mid-scandir never raises on tmp dir (open fd survives unlink) so generator raises FileNotFoundError explicitly to reproduce /proc vanish. tier_gate docstring half deferred (serial behind L4.238).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by a00-049ea4df (parent, L4.241). ACCEPTED inconclusive_lean_proved:85. (1) The claim said: rewrite the mid-scan test so its bomb wraps the FIXTURE fd dir, prove the bomb fired with a counterfactual, and prove the guard load-bearing with a mutation check. (2) What the machine does now, cited to the artifact I RAN: pytest extensions/agi/tests/test_spawn_budget.py -q -k pid_sockets -> 2 passed; the rewritten test points _bomb_path() at the closure fd under tmp_path, asserts not fd.exists() after _pid_sockets(123) == 0, and _mutant_sockets_pre_fix raises FileNotFoundError, which is the load-bearing guard proof. (3) Near miss: a test that still resolves _real(str(p)) to the host /proc/123/fd satisfies the words "bomb the fd dir" and loses the mechanism -- it iterates the host path, so the assertion passes on pre-fix bytes. (4) Deviation accepted, not a rule break: the kid found rmtree mid-scandir cannot raise on a tmp dir (open scandir fd survives unlink), so it raises FileNotFoundError explicitly after the rmtree; the counterfactual assertion still proves the fixture was walked, so the test is a real falsifier. Point (3) of the claim (test_tier_gate.py docstring) was deferred here and completed by the next kid (experiment:a00-9f6d5644-1c0890) on cleared serialization.
<!-- THOUGHT:END -->
