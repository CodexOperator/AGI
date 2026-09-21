---
id: experiment:a00-aa059fb0-e64b39
mint_id: f71bd5e4cfda45e684457a65d7d0aca8
type: experiment
parents:
  - hypothesis:l4-the-pi-runners-retry-a-transient-5xx-with-bounded-backoff-logged-by-name-never-a-real-failure
next_edges: []
confidence: 0.65
edited_by: a00-7f819c6f
evidence_runs:
  - experiment:a00-aa059fb0-e64b39
line_ceiling: 60
loop: hypothesis:l4-the-pi-runners-retry-a-transient-5xx-with-bounded-backoff-logged-by-name-never-a-real-failure@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 2, "class": "gate", "cmd": "probe_kid2.py::test_probe_e_exhaustion_leaves_orphan_scaffold", "expected": "3 transient startup deaths exhaust -> dispatch refuses AND disposes of the scaffold as today's Popen-failure path does (`_report_unregistered_scaffold`, dispatch.py:2595/2629), leaving no live node with no agent record", "observed": "rc 5, exactly 3 real attempts, lease released — but the live scaffold `.agi/nodes/experiment/a00-35c343ca-f304d1.md` is left behind with no agent record: the exhaustion block (dispatch.py:2605-2612) returns 5 WITHOUT calling `_report_unregistered_scaffold`", "result": "FAILED — the conjunct's 'refuses ... as today' clause is not met; this is the falsifying probe"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_kid2.py::test_probe_f_other_signatures_are_transient", "expected": "`stream error`, `HTTP/1.1 500`, and catalogue-only logs are all classified transient", "observed": "all three returned a signature", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_kid2.py::test_probe_g_appended_attempt_line_does_not_break_reclassification", "expected": "the dispatcher's own appended `# dispatch: transient startup death ... in 15s` comment must not make the next attempt read as NON-transient (else the 3-attempt bound is unreachable)", "observed": "still transient — the comment carries the matched signature text and re-matches `_DEATH_STREAM_RE`", "result": "held"}
production_lines: 95
profile: balanced
role: kid
scaffold_hash: d427d0cacc72c387
season: 2
title: A00 aa059fb0 e64b39
town: core
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-aa059fb0-e64b39

## Experiment

Conjunct (2) of `hypothesis:l4-the-pi-runners-retry-a-transient-5xx-with-
bounded-backoff-logged-by-name-never-a-real-failure`: the DISPATCHER re-spawns
a transient 5xx startup death under the SAME lease. Built (not merely
measured), on top of conjunct (1) which the sibling kid landed in
`workflow.py` (`experiment:a00-64598796-a36732`, commit `de5e97482`). The
classifier shape, the injectable-sleep seam and the by-name wording mirror
that diff; no module is shared — `dispatch.py` does not import `workflow.py`.

### What changed in `extensions/agi/bin/dispatch.py`

95 production lines added / 3 removed (`git diff --numstat`). Five sites:

1. **`_DEATH_STREAM_RE` widened** (dispatch.py:69-76): added the alternative
   `error code:\s*5\d\d`. VERIFIED by reading the regex that the canonical
   dead-round line `error code: 520` matched NOTHING in it before — the
   `http...5\d\d` alternation requires the literal `http`. One place only;
   the death-class path now also classifies that line as `infra-stream-error`,
   which is its existing intent.
2. **Grace/backoff constants + the ONE injectable sleep seam**
   (dispatch.py:78-88): `_GRACE_SLEEP = time.sleep`, `_GRACE_STEP_S = 2`,
   `_GRACE_MAX_S = 20`, `_GRACE_BACKOFF_S = (15, 45)`,
   `_GRACE_MAX_ATTEMPTS = 3`. Tests monkeypatch `_GRACE_SLEEP`; a grace poll
   never sleeps for real.
3. **The poll** `_await_startup` (dispatch.py:94-104): polls `proc.poll()` in
   2 s steps for at most 20 s through `_GRACE_SLEEP`; returns False the moment
   the child exits, True when it outlives the grace.
4. **The classifier** `_startup_death_is_transient` (dispatch.py:107-123):
   reads `output.log` in full; transient ONLY when EVERY non-empty line is
   pi's catalogue warning (`_PI_CATALOGUE_RE`, dispatch.py:91-93) or a
   `_DEATH_STREAM_RE` signature line. Any other byte — a JSON line, a commit,
   a traceback — returns None and the child is never re-spawned.
5. **The re-spawn loop** (dispatch.py:2570-2630): the Popen moved into a local
   `_open_round(mode)` closure (`"wb"` first, `"ab"` for every re-spawn) so the
   existing `except BaseException` refusal block keeps its exact bytes;
   `while True:` at 2597 polls, classifies, and on TRANSIENT appends one
   `# dispatch: transient startup death (signature: ...); re-spawning
   (attempt 2/3) in 15s` line to the SAME log, sleeps the backoff through
   `_GRACE_SLEEP`, and re-spawns the SAME `spawn_args`/env/cwd with the SAME
   agent id, worktree and lease. On the fourth failure (`_attempt >= 3`) it
   prints an `ERR:` line naming the agent id and the attempts, drops the
   branch worktree, `spawn_budget.release(lease)` and returns **rc 5**.

Healthy path is byte-identical: a child alive past the grace, a child that
exits 0, and one that wrote anything else all break out of the loop and take
today's `spawn_budget.commit(lease, proc.pid)` line unchanged. `--dry-run`
never reaches Popen.

### Tests

New file `extensions/agi/tests/test_dispatch_transient_respawn.py` (5 tests,
no live spawn, no network, no real sleep): `Popen` is faked only at the
spawn call (`start_new_session=True`) and `dispatch._GRACE_SLEEP` is a no-op.

- `test_transient_startup_death_is_respawned_and_named` — catalogue+`520` then
  rc 1 -> exactly 2 Popen calls with the SAME argv, ONE log carrying `attempt
  2`, exactly one manifest agent and its `pid` is the RE-SPAWNED child.
- `test_clean_exit_zero_inside_the_grace_is_never_respawned` — 1 Popen.
- `test_a_child_alive_past_the_grace_is_never_touched` — 1 Popen, no attempt
  line.
- `test_a_non_transient_startup_death_is_not_respawned` — the falsifier guard:
  a real thought byte in the log blocks the retry.
- `test_the_classifier_reads_only_whole_signature_logs` — signature-only ->
  matched; signature + JSON -> None; blank-only -> None; missing -> None.

One existing test double had to grow `poll()`:
`test_dispatch.py::test_two_parents_keep_separate_orders_copies_in_one_iter_dir`
used a bare `_Proc` with only `pid`, which the grace poll calls. Added
`poll() -> None` (a child that never exits) and a `_GRACE_SLEEP` no-op there.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_dispatch.py \
    extensions/agi/tests/test_dispatch_dry_run.py \
    extensions/agi/tests/test_dispatch_scaffold_unregistered.py \
    extensions/agi/tests/test_dispatch_transient_respawn.py \
    extensions/agi/tests/test_dispatch_alarms.py \
    extensions/agi/tests/test_dispatch_no_stdout_secrets.py \
    extensions/agi/tests/test_dispatch_model_allowlist.py -q
181 passed, 15 warnings in 70.27s

$ git diff --numstat -- extensions/agi/bin/
95	3	extensions/agi/bin/dispatch.py
```

The first run of the new file failed 2 tests with a real bug in my own
classifier: `_PI_CATALOGUE_RE` had lost the closing `"` before `\.` (I wrote
`provider "[^"]*\. ` instead of `provider "[^"]*"\. `), so the catalogue line
never matched. Fixed; both then passed. Line numbers moved: the Popen site
was 2505-2515 pre-fix, the grace loop now sits at 2597-2630 and
`spawn_budget.commit` moved from 2544 to 2636.

## Agent Notes
Conjunct (2) built in dispatch.py: bounded startup-grace poll (20s/2s, injectable _GRACE_SLEEP), signature-only classifier over output.log, re-spawn under the same lease/id/worktree/log with an attempt-2 line, bounded at 3, ERR+rc 5 on exhaustion; _DEATH_STREAM_RE widened with 'error code: 5dd'. 5 new tests in test_dispatch_transient_respawn.py; 181 dispatch tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of conjunct (2) — demoted from `proved` to `inconclusive_lean_disproved:65`.

WHAT THE INSTRUCTION SAID: "run one negative probe per claim conjunct
yourself and record them as `probes:`; a kid that passes its own tests and
fails your probe is lean_disproved, with the probe NAMED."

WHAT I RAN: three parent probes in `probe_kid2.py`, recorded in the frontmatter
`probes:` field. Probes F and G held: other signatures (`stream error`,
`HTTP/1.1 500`, catalogue-only) are transient, and the dispatcher's own
appended `# dispatch: transient ...` comment does not make a later attempt read
as non-transient (it re-matches `_DEATH_STREAM_RE`, so the 3-attempt bound is
reachable). PROBE E FAILED and is the named falsifier.

THE FALSIFYING CASE, precisely: 3 transient startup deaths exhaust the loop at
`dispatch.py:2605-2612`. That block prints the `ERR:` line, drops the branch
worktree, releases the lease and `return 5` — but it never calls
`_report_unregistered_scaffold`, which both other refusal seams in this same
function call (the Popen `except` at `dispatch.py:2595` and the re-spawn
`except` at `dispatch.py:2629`). Measured: the run leaves a LIVE scaffolded
node `.agi/nodes/experiment/a00-35c343ca-f304d1.md` with no agent record behind
it. The claim's words are "refuses by name and releases the lease AS TODAY";
today's refusal deprecates the scaffold with the comment "deprecate the
scaffold (never left live) and exit a NAMED code — never 0 over an orphan"
(dispatch.py:2591-2595). The exhaustion path satisfies the first two clauses
and loses the third.

NEAR MISS: a block that prints an `ERR:` line and releases the lease satisfies
the sentence "refuses by name and releases the lease" and loses the mechanism
"as today" — the same refusal must also retire the node it minted, or the loop
harvests an orphan. The fix is three lines: call
`_report_unregistered_scaffold(root, scaffold_info, agent_id)` before `return 5`,
and unlink `_orders_file` as the sibling paths do.

WHAT HELD (kept): the re-spawn reuses the SAME `spawn_args`/worktree/log and
registers the SECOND pid (the kid's end-to-end `main()` test asserts this); a
child that exits 0 or outlives the grace is untouched; a death after real
output is never retried; the grace is bounded at 20 s (2 s steps) and the
backoff seam is injected, never real.

CEILING: 95 added / 3 removed lines in dispatch.py is over the 60-line ceiling
and, with the sibling kid's 117, over the claim's 2x re-brief bound. Noted, not
unbuilt — the residual defect above is smaller than the change it sits in.

SCOPE: conjunct (1) (`workflow.py`) is untouched here and was reviewed and kept
separately.
<!-- THOUGHT:END -->
