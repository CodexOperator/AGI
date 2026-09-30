---
id: experiment:a00-6b761b8c-b6ae8b
mint_id: 731a15a7dcec4063b2ce5ea2218be01c
type: experiment
parents:
  - hypothesis:l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-full-suite
next_edges: []
confidence: 0.85
edited_by: a00-75ddec76
evidence_runs:
  - experiment:a00-6b761b8c-b6ae8b
loop: hypothesis:l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-full-suite@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: "probes: gate-positive — pytest extensions/agi/tests/test_workflow.py <scratch probe test> with the probe calling workflow._track_run into a NON-tmp scratch root (shared_project_root patched to that scratch dir, no production row written) -> \"69 passed, 1 error in 69.56s\", \"ERROR at teardown of test_zzz_parent_probe_tracks_a_row\" (the last collected item), AssertionError naming probe-scratch/sessions/workflows. Proves the guard still fires on a real leak and that the ERROR attaches to the last collected test.\nprobes: gate-negative — same invocation with the tracked root under tempfile.gettempdir() -> \"69 passed in 69.11s\", 0 errors. Proves test-owned tmp writes stay silent.\nprobes: wire/concurrent-seat — same invocation with a CHILD PROCESS (fresh interpreter, own workflow module object) calling _track_run into a non-tmp scratch dir while the suite ran -> \"69 passed in 71.29s\", 0 errors, and probe-scratch/sessions/workflows/parent-other-process.jsonl exists on disk. Proves a different process cannot enter the ledger.\nprobes: wire/patch-reachability — grep: workflow.py's only _track_run call sites are unqualified module globals (1575, 1620, 1625); no module-level `from workflow import _track_run` anywhere in the tree, and test_workflow.py's in-body by-name imports (1500, 1523, 1561, 1581) execute after the fixture's setup, so they bind the wrapper. Measured, not read from the source: probe 1 fired through that path."
profile: balanced
role: kid
scaffold_hash: 55b12c1f9da5c319
season: 2
title: A00 6b761b8c b6ae8b
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:a00-6b761b8c-b6ae8b

## Verdict in one line

The parent's leading mechanism is **refuted**, and the real colliding state is
named, fixed, and proved: `test_workflow.py`'s session-scoped leak guard
compared **line counts** of the **live shared** `<main>/.agi/sessions/workflows/*.jsonl`
and called any change a test leak, so a *concurrent seat's* real workflow run
turned the session teardown into an `ERROR` reported against whichever test
pytest collected **last** — the "only inside the full suite, only on the last
test" signature.

## (A) The colliding state, named — with a deterministic reproduction

**State:** `<main-graph>/.agi/sessions/workflows/*.jsonl` is **live production
state**. Every seat on this box writes it via `workflow.py run` →
`workflow.py:907 _track_run` → `_loc.shared_project_root(root)`
(`locations.shared_project_root`, resolved through `git_common_root`, so every
worktree resolves the *same* main dir). `extensions/agi/tests/test_workflow.py:996`
`_real_workflow_jsonl_counts()` snapshotted those counts at session start and
`test_workflow.py:1020 _no_workflow_row_leaks_to_real_sessions` re-read them at
session end and asserted **any** change was a leak. It cannot tell this
process's writes from another process's.

**Natural experiment (this box, this worktree, no injected writes).** I ran the
full suite pre-fix and its ONE error was:

```
________________ ERROR at teardown of test_errors_do_not_abort _________________
    @pytest.fixture(scope="session", autouse=True)
    def _no_workflow_row_leaks_to_real_sessions():
        before = _real_workflow_jsonl_counts()
        yield
        after = _real_workflow_jsonl_counts()
        changed = {p for p, c in before.items() if after.get(p) != c}
        changed |= {p for p in after if p not in before}
>       assert not changed, (
E       AssertionError: workflow tests leaked rows into the real sessions dir
    (changed/added: ['<home>/work/agi/.agi/sessions/workflows/merge-up-review.jsonl']);
    a non-dry workflow run test must redirect tracking to a tmp root via
    _tmp_session_root, never run against the real project root.
extensions/agi/tests/test_workflow.py:1033: AssertionError
...
3 failed, 4995 passed, 15 skipped, 1 xfailed, 1619 warnings, 1 error in 726.88s (0:12:06)
```

The changed file's last row is not a test artefact — it is a **live season
merge-up review run by another seat**, written 28 s before my suite ended:

```
$ tail -1 <home>/work/agi/.agi/sessions/workflows/merge-up-review.jsonl
{"failed": 1, "harness": "pi", "harness_id": [], "ok": 0, "returns": {},
 "run_key": "mur-sm-36", "stages": {"review:SM.36": "failed", "verify:SM.36": "pending"},
 "timestamp": "2026-09-16T11:57:04.916706+00:00", "workflow": "merge-up-review"}
$ ls -l --time-style=full-iso .../workflows/merge-up-review.jsonl
-rw-rw-r-- 1 <user> <user> 97105 2026-09-16 07:57:04.916399446 -0400
```

Suite ended 07:57:32 local; no test in `test_workflow.py` mints `mur-sm-36`
(tests use `run_key="mur-39"` and window `"t1"` — `test_workflow.py:1493`).
**Why the ERROR lands on the last test:** the failing fixture is
*session-scoped*, so pytest reports its teardown against whichever test it
collected last. That is the whole "errors only inside the full suite" shape:
`test_zoom.py` sorts last in a bare-directory run (`/tmp/mergeup-suite-sl233.log:20`,
`/tmp/stamp-suite-window.log:20`), and `schema_registry/test_validation.py`
sorted last in my invocation.

**Corroboration across three independent runs** (the two logs the parent
cited, plus mine). Each run's log mtime is when the suite ended, and in each
case a live `merge-up-review` row landed in the shared dir under a minute
before that:

| run | suite ended (local) | live row just before it |
|---|---|---|
| `/tmp/mergeup-suite-sl233.log` | 2026-09-16 05:42:43 | `mur-gen22-mu2` @ 05:41:34 (-69 s) |
| `/tmp/stamp-suite-window.log` | 2026-09-16 06:29:17 | `mur-gen22-mu4` @ 06:28:10 (-67 s) |
| this run, pre-fix | 2026-09-16 07:57:32 | `mur-sm-36` @ 07:57:04 (-28 s) |

**Deterministic reproduction** (scratch, no production row written — a scratch
`scratch-workflows/` stands in for the shared dir; the pre-fix predicate is
copied verbatim from `test_workflow.py`, only the directory changes). A
background "concurrent seat" appends one `mur-sm-36` row while the session runs:

```
$ cd .agi/sessions/iter-SM.43/a00-6b761b8c/probe/prefix
$ python3 -m pytest test_guard_race.py -q --tb=short
..E
=================== ERRORS ====================
___________ ERROR at teardown of test_last_consumer ____________
test_guard_race.py:45: in _no_workflow_row_leaks_to_real_sessions
    assert not changed, (
E   AssertionError: workflow tests leaked rows into the real sessions dir
    (changed/added: [.../scratch-workflows/merge-up-review.jsonl]); ...
2 passed, 1 error in 3.03s
```

Exact signature reproduced: `2 passed, 1 error`, `ERROR at teardown of
<HEAD>` — the *last* test — with the fixture's own message.

## Why the parent's mechanism is refuted

The parent's leading mechanism was a pytest temp-root collision
(`/tmp/pytest-of-<user>/pytest-<N>` shared by every worktree; a concurrent
session's `cleanup_numbered_dir` pruning a live session's basetemp). That is
**not** what happened here:

1. The traceback above is a *workflow fixture teardown*, not a `tmp_path`
   setup failure. Nothing in it mentions a temp dir.
2. `_pytest.pathlib.LOCK_TIMEOUT` in the installed pytest 9.0.2 is
   **259200 s (3 days)**, and `make_numbered_dir_with_cleanup` computes
   `consider_lock_dead_if_created_before = p.stat().st_mtime - lock_timeout`
   for the *new* dir; `ensure_deletable` therefore only removes a candidate
   whose `.lock` is older than ~3 days (or that has no lock). The parent's
   premise — "a ten-minute suite's own `.lock` is stale by that rule well
   before it ends" — is false, so a concurrent session cannot prune a live
   suite's basetemp minutes in.
3. A basetemp that *is* removed does produce the ERROR signature (I reproduced
   that too: `probe/repro.log`, `1 passed, 1 error`, `ERROR at setup of
   test_second_consumer_after_basetemp_removed`) — which is exactly why a
   plausible-looking mechanism has to be checked against the real traceback
   rather than matched by its summary line.

Consequence: **no temp-root change was made.** The known-bad in-repo
`--basetemp` shape (`hypothesis:l4-basetemp-advice-excludes-synthetic-root-
fixtures`) is not needed, and the synthetic-root modules are untouched.

## (B) The fix

**Root layer — `extensions/agi/tests/test_workflow.py`** (the file/fixture
measured to emit the ERROR). `_no_workflow_row_leaks_to_real_sessions` no
longer compares file counts; it wraps `workflow._track_run` for the session and
records any write **this process** makes whose resolved sessions dir is outside
`tempfile.gettempdir()`. A concurrent seat runs in its own process and can
never enter the wrapper, so it is invisible; a real leak is still caught, and
only a real leak. `_real_workflow_jsonl_counts` (the unsound comparison) is
removed. Net: ~30 lines in the fixture, ~22 removed.

Ownership is now explicit: the **per-process ledger owns the guarantee**; the
file path itself (`<main>/.agi/sessions/workflows/`) is now known to be live
production state, not suite-owned state.

**Local layer — `extensions/agi/tests/test_zoom.py:603`**:
`test_no_source_comment_cites_an_unresolvable_tier_node_id` requested `tmp_path`
and never used it. Dropped. This is cleanup, not the guarantee: it only means
*that* test can no longer be the last test the teardown error is attached to.

## Limits of the fix

The ledger is **process-local**, so a *future* test that shells out to
`workflow.py run` as a child process would not be recorded (no test in
`test_workflow.py` does that today — `grep -n "workflow.py" test_workflow.py`
finds none, and `run_workflow` is imported and called in-process only). The
count guard would have caught such a write, but only by being unable to tell it
from a concurrent seat's, which is the defect this node fixes.

## (C) Proof

**Gate probe — same concurrent writer, pre-fix vs post-fix.** Post-fix ledger
(scratch copy of the new shape) with the identical concurrent `mur-sm-36`
writer:

```
$ cd .agi/sessions/iter-SM.43/a00-6b761b8c/probe/postfix
$ python3 -m pytest test_guard_race.py -q --tb=line
..                                                                       [100%]
2 passed in 3.02s
```

Positive control — a write from **this** process to a non-tmp dir is still
caught:

```
$ PROBE_LEAK=1 python3 -m pytest test_guard_race.py -q --tb=line
E   AssertionError: workflow tests leaked rows into the real sessions dir
    (changed/added: ['.../probe/postfix/scratch-workflows/sessions/workflows']); ...
ERROR test_guard_race.py::test_last_consumer - AssertionError: ...
2 passed, 1 error in 3.01s
```

**Regression — the synthetic-`.agi`-root module named in the g17.1 caveat:**

```
$ python3 -m pytest extensions/agi/tests/test_verification_seat_model.py -q
8 passed in 0.26s
```

**Targeted:**

```
$ python3 -m pytest extensions/agi/tests/test_workflow.py extensions/agi/tests/test_zoom.py -q
109 passed in 83.84s (0:01:23)
```

**End-to-end**, same invocation shape as the pre-fix baseline:

```
$ python3 -m pytest $(ls extensions/agi/tests/test_*.py) extensions/agi/tests/chain_engine \
    extensions/agi/tests/embeddings extensions/agi/tests/graph_core \
    extensions/agi/tests/renderers extensions/agi/tests/schema_registry --tb=long -q
2 failed, 4996 passed, 15 skipped, 1 xfailed, 1619 warnings in 585.42s (0:09:45)
```

**Pre-existing failures, untouched lanes** (present pre-fix in this same
invocation, and in the parent's runs): `test_rotate_launch_wrapper.py::test_wrapper_tty_hangup_forwards_to_the_child`,
`test_rotate_verb_resolvers.py::test_unkeyed_post_refuses_keygen`,
`test_ws_raw.py::test_cancel_frees_the_slot`. The parent's baseline reported
`test_unkeyed_post_refuses_keygen` as pre-existing too.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS B3 review (goal:g1.31.3.1.1, hypothesis:pb3-node-verdicts-match-bytes-1-6-13-46, run mur-pb3chunk18of20/verify_l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-ful.json — box-local under .agi/sessions/workflows/runs/, gitignored; prior THOUGHT in git at the pre-review commit). Scope of the lean is NARROWED to what this node actually measured: the three gate/wire probes recorded in its own frontmatter probes: field — (1) gate-positive, a real leak tracked into a non-tmp scratch root, suite text "69 passed, 1 error in 69.56s" with the ERROR attached to the last collected item; (2) gate-negative, the same write under tempfile.gettempdir(), "69 passed", 0 errors; (3) wire/concurrent-seat, a child process writing into a non-tmp scratch dir while the suite ran, "69 passed", 0 errors, ledger file present on disk — plus a grep reachability check. On those three the claim stands, so the verdict is proved-in-substance but demoted to inconclusive_lean_proved:85 rather than flat proved, because the only FULL-SUITE rows this node carries are RED: "3 failed, 4995 passed, 1 error" (pre-fix) and the kids own "2 failed, 4996 passed" (post-fix). Those rows were NOT re-run in this review (stated in its DEVIATION FROM A STANDING RULE), so they are recorded here as an unresolved negative, not as support. A red suite and an unrun suite are the same evidentiary hole: the probe evidence is real but it is scoped to the probes, so the flat form would overstate what the bytes show.
<!-- THOUGHT:END -->

## Agent Notes
Refuted the parent's /tmp/pytest-of-<user> basetemp theory: the full-suite ERROR is test_workflow.py's session-scoped leak guard comparing LINE COUNTS of the LIVE shared .agi/sessions/workflows/*.jsonl, so a concurrent seat's own workflow row (mur-sm-36, 07:57:04 local, 28s before the run ended) is misread as a test leak and reported as ERROR at teardown of whichever test pytest collected LAST -- the only-inside-the-full-suite signature. Fixed per-PROCESS: the guard now wraps workflow._track_run and records only writes THIS process makes to a non-tmp dir (unsound _real_workflow_jsonl_counts removed); test_zoom.py's unused tmp_path param dropped as local cleanup. Post-fix full suite: 2 failed, 4996 passed, 15 skipped, 1 xfailed, 1619 warnings in 585.42s (0:09:45) -- 0 errors; both failures pre-existing other-lane (test_rotate_launch_wrapper, test_rotate_verb_resolvers::test_unkeyed_post_refuses_keygen).

PARENT REVIEW (a00-e2977dc6, SM.43). ACCEPTED, verdict kept at proved / 0.85. Read the diff, not the node: test_workflow.py's session-scoped autouse guard no longer diffs LINE COUNTS of the LIVE shared .agi/sessions/workflows/*.jsonl (a concurrent seat's row was being read as a test leak, surfacing as a session-fixture teardown ERROR on whichever test pytest collected LAST -> "errors only inside the full suite"); it now wraps workflow._track_run and records only writes THIS process makes to a non-tmp sessions dir. test_zoom.py:603 drops the unused tmp_path it never used. The parent's own briefed mechanism (shared /tmp/pytest-of-<user> basetemp) was REFUTED by the kid with a measured constant and correctly NOT implemented. Three probes run by the parent on the changed bytes: gate-positive (real non-tmp write from this process -> 69 passed, 1 error, ERROR at teardown of the last collected item), gate-negative (same write under tempfile.gettempdir() -> 69 passed, 0 errors), and the concurrent-seat direction (a CHILD PROCESS wrote to a non-tmp scratch dir mid-suite -> 69 passed, 0 errors, row on disk). Full suite post-fix: 2 failed, 4996 passed, 15 skipped, 1 xfailed, 1619 warnings in 585.42s, 0 errors; both failures pre-existing other-lane (test_rotate_launch_wrapper::test_wrapper_tty_hangup_forwards_to_the_child, test_rotate_verb_resolvers::test_unkeyed_post_refuses_keygen). Residue: the guard's whitelist is a path-PREFIX test against tempfile.gettempdir(), so a repo living under the temp root would silence it; the ledger is per-process by design and cannot see a leak from a subprocess a future test spawns (not a regression). Parent's 60 s LOCK_TIMEOUT claim in the brief was false (measured 259200). No production code changed; no git run by the parent.

PB3.2 (agent a00-afb177f9, 2026-09-30): the box user from the live `box.user` cell on the 5 lines of this node (4 pytest basetempaths, 1 ls -l owner/group pair) is now <user>, a placeholder form, so the graph carries no box user. This is a SUBSTITUTION, not a redaction: no measurement, id, verdict or count changed, and the authored parent review THOUGHT (NEAR MISS) is left whole -- it is a parent review, not a scrub note. Goal:g1.31.3.2 item (+), hypothesis:pb3-hw-name-scrubbed-and-four-lost-corrections-restored; the value was read from the cell, never typed. Sixth and last of six.
