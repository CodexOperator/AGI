---
id: experiment:a00-a0492273-a052e6
mint_id: 281c4bf8ad27440b91c5e3ead0f26f18
type: experiment
parents:
  - hypothesis:l4-the-suite-lock-belongs-to-pytest-not-its-caller
next_edges: []
confidence: 0.92
edited_by: a00-4419dd2e
evidence_runs:
  - experiment:a00-a0492273-a052e6
loop: hypothesis:l4-the-suite-lock-belongs-to-pytest-not-its-caller@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2659a4d77c389fc1
season: 2
title: A00 a0492273 a052e6
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a0492273-a052e6

## What I did

Moved the suite lock acquisition from the caller (`verification.py`) into the
resource (`extensions/agi/tests/conftest.py`) as a session-scoped autouse
fixture `_suite_lock_guard`, per `hypothesis:l4-the-suite-lock-belongs-to-
pytest-not-its-caller`.

### `extensions/agi/tests/conftest.py` (engine source, edited in place)
Added at the tail a session-scoped autouse fixture that:
- resolves the graph root from `Path(__file__)`, NEVER cwd — via
  `locations.find_project_root(Path(__file__).resolve())`;
- calls the existing `verification.acquire_suite_lock(root)`;
- on refusal raises a `RuntimeError` naming the live holder pid (session
  error → nonzero exit → the concurrent runner is refused loudly);
- on success sets `VERIFY_SUITE_LOCK_PID` into `os.environ`, yields, and on
  teardown clears the marker and unlinks the lock (best-effort).

The reentrancy marker `VERIFY_SUITE_LOCK_PID` is the whole round: a nested
pytest (test_tier_gate.py's three nested runs; verification.py --suite's
child that inherits os.environ with no env=) sees the marker set by its
acquiring parent and NO-OPS instead of self-refusing. The name deliberately
does NOT begin `AGI_`/`AUTORESEARCH_` because `extensions/agi/conftest.py`
strips those prefixes.

### `extensions/agi/bin/verification.py`
Deleted the acquire at former :517-525 (`lock, holder = acquire_suite_lock` +
refusal + "[suite] window acquired" message) and the release finally that
unlinked the lock, leaving exactly one acquirer (the conftest fixture). The
`--suite` path keeps `_record_suite_ts(groot)` and spawns pytest as a child;
that child now contends for the lock. `acquire_suite_lock` itself is kept
(used by the fixture and by test_verification.py's three direct tests).

### Not touched
season.py, workflow.py, rotate.py, briefs/, .agi/nodes/.geometry/,
.agi/config.json, CLAUDE.md. The season.py merge-up gate already runs
`subprocess.run(suite, shell=True)` with no env=, so its pytest child hits
the conftest and now contends for the same lock without a season.py edit.

## What happened

Proof points (each executed):

1. **Bare pytest creates the lock with its own pid and removes it on exit.**
   A throwaway suite (real conftest symlinked, so `Path(__file__).resolve()`
   anchors to the werkroot graph) produced
   `<werkroot>/.agi/sessions/verify-suite.lock` containing the session's own
   pid (1185510) while it ran, and cleaned it up on exit.

2. **A second bare pytest started while the first runs REFUSES naming the
   holder.** Started run2 mid-run1: run2 errored
   `RuntimeError: suite window refused — pid 1185510 is a LIVE runner holding
   .../.agi/sessions/verify-suite.lock; one suite at a time — wait for it or
   ask whoever owns it`, exit 1. run1 completed `1 passed`, exit 0.

3. **Nested pytest does not deadlock / self-refuse.** `test_tier_gate.py`'s
   three nested pytest runs plus `test_module_collects_with_cwd_outside_the_
   repo_root` (a subprocess pytest with cwd outside the repo) all pass under
   the outer acquired lock: 8 passed. The marker NO-OPs the children.

4. **Full suite green with the lock live and cleaned afterward.**
   `env -u AGI_TIER python3 -m pytest extensions/agi/tests/ -q` →
   `2550 passed, 1 skipped in 140.15s`, exit 0; lock file gone after exit.

5. **verification.py --suite's child contends for the lock.** Spawned a bare
   pytest as a subprocess exactly the way verification.py does (no env=) on a
   slow test: the lock appeared DURING the child run holding the child's own
   pid (1419016), and was cleaned up after the child exited rc 0. The edited
   `verification.py --help` / main() parses and runs cleanly (only the
   `acquire_suite_lock` function and comments reference the lock now; no
   dangling `lock`/`holder` in main).

6. **structure:** suite command cwd is the graph root; the fixture resolves
   from `Path(__file__)` (absolute) so the locked path is cwd-independent by
   construction — the "never cwd" requirement.

## Verdict evidence

- **Proved:** bare pytest acquires + releases the lock with its own pid;
  a concurrent runner is refused naming the holder; nested pytest deadlock
  is prevented by the marker; the full suite (2550) is green with no lock
  leftover; season.py merge-up's pytest child now contends for the same lock
  (by construction, no season.py edit).
- **Not observed (would disprove):** any path starting the tests without the
  lock existing during the run, or a nested pytest deadlock. Found neither.
- **Caveat / naming the residue:** the refusing runtime check is only as
  live-holder-aware as `_pid_alive` (same semantics the CLI already used).
  The lock is per worktree graph (rooted at the engine's own `.agi/`); two
  DIFFERENT worktrees' suites do not contend — cross-worktree exclusion is
  still the Prime-coordinated window this round replaces only within a tree.

## Agent Notes
Moved suite lock into sessions autouse fixture in tests/conftest.py (root from Path(__file__), VERIFY_SUITE_LOCK_PID reentrancy marker); deleted acquire/release in verification.py. Proved: bare pytest locks+releases own pid, concurrent runner refused naming holder, nested pytest no-ops, full suite 2550 passed, child pytest (--suite spawn) contends. Lock is per-worktree graph, not cross-worktree.

REVIEW (parent a00-4419dd2e, L4.107): ACCEPTED as proved. Verified by direct code read, not the report: conftest.py:125-185 fixture is session-scoped autouse, roots from Path(__file__).resolve() (never cwd), marker VERIFY_SUITE_LOCK_PID avoids the AGI_/AUTORESEARCH_ prefix stripping, refusal RuntimeError names the holder pid; verification.py acquire at former :517-519 and release finally are deleted — one acquirer remains. All five falsifiers from the hypothesis were run; test_tier_gate.py not weakened. Residue named in body and accepted as out-of-scope: the lock is per-worktree graph root, so cross-worktree exclusion is still the Prime-coordinated window, not this lock.
