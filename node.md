---
id: experiment:a00-c5ca0fde-941eef
mint_id: 4b33a08e645a430684754f2f16ffa00b
type: experiment
parents:
  - hypothesis:l4-the-full-suite-runs-under-600-s-solo-real-waits-and-process-reaps-are-seamed-not-slept
next_edges: []
confidence: 0.85
edited_by: a00-aa68dd29
evidence_runs:
  - experiment:a00-c5ca0fde-941eef
loop: hypothesis:l4-the-full-suite-runs-under-600-s-solo-real-waits-and-process-reaps-are-seamed-not-slept@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "pytest extensions/agi/tests/test_rotation_alerts.py -k 'after_join_dm_to_silent_post_refused or after_join_type_seam_to_silent_never_fires'; then the whole test_after_join_service.py + test_rotation_alerts.py files", "expected": "delay_override=0 reaches run_after_join so the two tests do NOT pay DEFAULT_AFTER_JOIN_DELAY_S=20; no test run_after_join caller reaches the real default sleep", "observed": "2 passed in 0.07s (was 40.09s); whole after_join+rotation_alerts files 92 passed in 1.35s; the only two run_after_join calls lacking delay_override/sleep_impl are dry_run=True or a monkeypatched stub (lines 1079/1582)", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "pytest extensions/agi/tests/test_node_writer.py -k 'live_tree_corpus_round_trip_is_value_preserving or live_tree_round_trip_zero_drift' --durations=5 ; then the second test ALONE in a fresh session", "expected": "ONE session-scoped read->render->read-back pass serves BOTH tests; each test still asserts standalone", "observed": "8.92s session setup, then 0.01s + 0.01s calls (2 passed in 9.04s); the second test alone in a fresh session still passes (9.01s); checked=3093 > 1000, value_drift=0", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "inspect.signature(rotate._reap_belam_oldest); grep the production caller; pytest test_rotate_selfreap.py::test_reap_belam_oldest_pane_seam_detached_tree", "expected": "wait_secs threads to _reap_chain; production default 5.0 unchanged; production caller passes nothing; the test passes a bounded value and the reap still runs", "observed": "signature ends wait_secs: float = 5.0; rotate.py:17711 passes no wait_secs; bounded test 1 passed in 5.04s (was 18.53s)", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 1b56cfa873b882b2
season: 2
title: "Real waits seamed: after_join delay_override, one shared live-corpus pass, bounded belam reap"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c5ca0fde-941eef

## Experiment

goal:g15 SM.30, conjuncts 1-3 of hypothesis:l4-the-full-suite-runs-under-600-s-
solo-real-waits-and-process-reaps-are-seamed-not-slept. Conjuncts 4-5
(verification.py record + acceptance solo run) are a SEPARATE later kid — not
touched here. All numbers measured on this worktree at 03:0xZ-03:3xZ, load
~2.2 on 4 cores. Assertions: none weakened, deleted, skipped or xfailed.

### Conjunct 1 — no test sleeps a production default

`test_rotation_alerts.py` `test_after_join_dm_to_silent_post_refused` (:126)
and `test_after_join_type_seam_to_silent_never_fires` (:171) both called
`rotate.run_after_join(...)` with `dry_run=False` and NO `delay_override`, so
`delay_s = promised_delay_s = DEFAULT_AFTER_JOIN_DELAY_S = 20`
(rotate.py:12112; `delay_override` seam at :12869, consumed :12950) and each
called `time.sleep(20)`. FIX: `delay_override=0` added to both calls — the
seam already existed and is documented in `run_after_join`'s docstring as the
no-wait convenience the SERVICE passes. Semantics unchanged: the assertions
(silent successor receives neither dm nor typed line) are the same and the
refusal path is the path under test, not the wait.

MEASURED, before -> after (the two tests together, `-k` selecting both):

    before: 20.00s + 20.00s call  (2 passed in 40.09s)
    after:  <= 0.005s each        (2 passed in 0.09s)

### Conjunct 2 — the two node_writer live-corpus round trips share ONE pass

`test_node_writer.py:1427 test_live_tree_corpus_round_trip_is_value_preserving`
and `:1515 test_live_tree_round_trip_zero_drift_and_reports_byte_change_count`
each walked and re-read the real `.agi/nodes/` tree. MEASURED: 10.38s + 8.77s.

MEASUREMENT THAT CHANGED THE FIX: a `@pytest.fixture(scope="session")` that
yields just the `(path, text)` list costs **0.10 s (setup)** — the file walk
is NOT the cost. The ~8.5 s per test is the per-node
`split_frontmatter` + YAML read + `render_frontmatter` + `_serialize_node` +
read-back. So a shared `(path, text)` list alone saves ~0.2 s, not the ~10 s
the parent's estimate assumed. The honest form of "ONE session-scoped corpus
load" therefore also does the read->render->read-back pass once: the
session-scoped fixture `live_node_round_trip` returns per-node records
`{path, reason, fm, fm2, byte_diff, non_fixpoint}` and BOTH tests assert over
the SAME records (the corpus bytes and the pure render are stable for the life
of a session). Both test names and every assertion survive: value
preservation, zero drift, the fixpoint, `checked > 1000`, the `byte_diffs <
checked` instrumentation guard, the `bytes_change` report and its id list.

MEASURED, before -> after (the two tests together):

    before: 10.38s + 8.77s = 19.15s   (2 passed in 19.64s)
    after:   9.01s shared setup + 0.01s + 0.01s = 9.24s (2 passed in 9.24s)
    corpus now reads checked=3093 (the live tree grew during the round)
    value_drift=0  bytes_change=89 ; BYTES_CHANGE_IDS still printed

`test_grid.py`'s corpus round trip (5.43 s, named by the parent) is NOT in
this slice's file scope and was left alone.

### Conjunct 3 — the selfreap real reaps are BOUNDED, and the wait is named

`test_rotate_selfreap.py:951 test_reap_belam_oldest_pane_seam_detached_tree`
spawns a REAL detached depth-3 sleep tree and reaps it for real.
`_reap_belam_oldest` (rotate.py:9725) called `_reap_chain(pids)` at :9815 with
the DEFAULT `wait_secs=5.0`.

THE WAIT, NAMED: the chain is NON-CHILD, so a TERM'd member whose parent is
still alive reads as a live zombie to `_pid_alive`; the wait loop
(rotate.py:9659-9660) burns the FULL `wait_secs` for that pid, then the
post-SIGKILL settle poll (:9684-9689) adds another 1.0 s. Measured cost = 3
descendants x (5 s + 1 s) = 18 s, which is the 18.53 s this test used to spend.

FIX (rotate.py, the ONLY production edit this round):

    def _reap_belam_oldest(*, tmux_session: str, oldest: str,
                           window_path: str | None = None,
                           pids: list[int] | None = None,
                           s12_reap: dict | None = None,
                           record_path: Path | None = None,
                           wait_secs: float = 5.0) -> dict:
    ...
        observed = _reap_chain(pids, wait_secs=wait_secs)

Production default stays 5.0 — the only caller (rotate.py:17711) passes
nothing, so behaviour is unchanged. The test passes `wait_secs=0.5`; the reaps
stay REAL (the tree is really TERM'd, SIGKILL'd when it survives, and really
settles gone) — only the wait bound changed.

MEASURED: 18.53s -> 4.97s.

`test_reap_chain_detached_nonchild_no_error` (:917) already used the seam
(`wait_secs=2.0`); it was NOT touched — 9.50 s before and after. Lowering 2.0
would buy ~3 s but changes a bound the parent already chose, so it is left to
the parent.

### Production-line budget

Non-test source changed: 2 lines in `extensions/agi/bin/rotate.py` (one
signature, one forwarded kwarg). Well under the <= 40 ceiling.

### Touched test files, run green

    python3 -m pytest extensions/agi/tests/test_rotation_alerts.py \
        extensions/agi/tests/test_node_writer.py \
        extensions/agi/tests/test_rotate_selfreap.py -q
    -> 134 passed, 97 warnings in 31.82s

## Evidence

### The sleep audit — EVERY `time.sleep`/real-wait site in `extensions/agi/tests/*.py`

39 grep hits. Classified: `seam` (injectable / monkeypatched / `sleeps`
recorder / fake clock), `<= 0.2 s`, `stand-in` (the sleeping process is a real
child the test TERMs — the test does not wait it out), or a named reason.

| site | reason |
|---|---|
| test_after_join_service.py:528 `def _sleep(secs)` | seam — injected as rotate's `sleep_impl` |
| test_claude_code_adapter.py:697 `_t.sleep(0.1)` | <= 0.2 s |
| test_dashboard.py:352 `time.sleep(1.5)` | named: a real `--watch` subprocess must reach its loop before SIGINT; not a production default, test_dashboard.py outside this round's scope |
| test_dispatch_alarms.py:150,176,197 | seam — `monkeypatch.setattr("time.sleep", ...)` |
| test_grid.py:1685 `_hold_grid_lock(seconds)` | holders 5 s / 0.5 s run in DAEMON threads never joined (no wall cost); the 0.6 s holder is a real holder-release wait the `lock_wait=10` test must pay |
| test_grid.py:1839 `_hold_grid_lock_at(lock, 5)` | daemon thread, never joined (no wall cost) |
| test_real_adapter_restart.py:141 / :227 / :259 / :547 | 0.05 / 0.2 / 0.02 / 0.2 s polls |
| test_rotate_handover.py:251 `time.sleep(2)` child | named: a real child must run and be reaped so its pid is PROVED dead; 2 s script sleep, test_rotate_handover.py outside scope |
| test_rotate_handover.py:450 | grep hit on the test NAME `..._stand_in_sleep`; body spawns `sleep 1000` and TERMs it — stand-in, no wait |
| test_rotate_handover.py:1471 `def sleep(self, s)` | seam — fake clock, advances 2.0 virtual seconds |
| test_rotate_latch_sweep.py:37 `time.sleep(2)` child | named: proved-dead-pid idiom, as above (test_rotate_latch_sweep.py outside scope) |
| test_rotate_launch_wrapper.py:38 / :58 / :123 | 0.05 / 0.02 / 0.05 s polls |
| test_rotate_selfreap.py:323 `_t.sleep(9999)` | stand-in — the grandchild that ignores SIGTERM; the test TERMs/KILLs it |
| test_rotate_selfreap.py:812 `time.sleep(9999)` | stand-in — detached-tree member script; really TERM'd |
| test_rotate_selfreap.py:871 / :944 | 0.05 s polls |
| test_rotate_templates.py:876 `def fake_sleep(secs)` | seam |
| test_rotate_templates.py:941 `real_sleep = rotate.time.sleep` | seam (captured for the injected clock) |
| test_rotate_templates.py:944 / :954 | 0.2 / 0.05 s |
| test_rotation_alert.py:1026 `time.sleep(2)` child | named: proved-dead-pid idiom (`_dead_pid`); test_rotation_alert.py outside scope |
| test_send.py:140 / :307 | seam — docstring of the `sleeps` recorder; `send_mod.time.sleep` monkeypatched at :159 / :329 |
| test_spawn_budget.py:125 `time.sleep(30)` child | stand-in — the lease holder, SIGKILLed |
| test_spawn_budget.py:177 / :294 / :1153 | 0.2 / 0.01 / 0.3 s (0.3 is the background lease-removal delay the wait must observe) |
| test_spawn_budget.py:825 `time.sleep(120)` child | stand-in |
| test_spawn_budget.py:1116 | grep hit on the test NAME; body monkeypatches `time.sleep` to RAISE |
| test_spawn_budget.py:1123 `monkeypatched` | seam |
| test_tier_gate.py:561 `time.sleep(120)` child script | stand-in |
| test_tier_gate.py:578 | 0.05 s poll |

No remaining site sleeps a PRODUCTION DEFAULT. The two that did are the
conjunct-1 pair, fixed above.

### Raw durations (this tree, this round)

```
# before
test_rotation_alerts 2 tests   20.00s + 20.00s  (40.09s)
test_node_writer    2 tests   10.38s +  8.77s  (19.64s)
test_rotate_selfreap 2 tests  18.53s +  9.50s  (28.18s)

# after
test_rotation_alerts 2 tests   ~0.00s + ~0.00s ( 0.09s)
test_node_writer    2 tests    9.01s setup + 0.01 + 0.01 ( 9.24s)
test_rotate_selfreap 2 tests   4.97s +  9.50s  (14.61s)

# touched files, whole
test_rotation_alerts.py + test_node_writer.py + test_rotate_selfreap.py
  134 passed, 97 warnings in 31.82s

# live corpus report (still printed by the folded pass)
.LIVE_TREE checked=3093 value_drift=0 bytes_change=89
```

### Struggle (reported to the parent)

`extensions/agi/tests/conftest.py:293 _is_bare_directory_run` classifies a
pytest arg as a targeted run only when it ends with `.py`. A NODE-ID arg
(`file.py::test_name`) does not, so the kid-tier gate refuses it as a "bare
full-suite directory run" and the measurement command cannot be written the
obvious way:

    pytest extensions/agi/tests/test_rotation_alerts.py::test_x -q
    -> ERROR: AGI_TIER=kid refuses a bare full-suite directory run

Workaround used: pass the file plus `-k <name>` (a `-k` filter short-circuits
the check). conftest.py is outside this round's file scope, so the defect is
reported, not fixed.

### Files changed

- `extensions/agi/tests/test_rotation_alerts.py` — two calls, `delay_override=0`.
- `extensions/agi/tests/test_node_writer.py` — session-scoped `live_node_round_trip` fixture; both round-trip tests assert over its shared records.
- `extensions/agi/tests/test_rotate_selfreap.py` — belam test passes `wait_secs=0.5`; docstring names the wait.
- `extensions/agi/bin/rotate.py` — `_reap_belam_oldest(..., wait_secs: float = 5.0)` forwarded to `_reap_chain`.

## Agent Notes
Conjuncts 1-3 landed: after_join pair 40.09s->0.09s (delay_override=0); node_writer live-corpus pair 19.15s->9.24s via one session-scoped read->render->read-back pass; belam reap 18.53s->4.97s via new _reap_belam_oldest(wait_secs=5.0) seam (production default unchanged). 39-site sleep audit in the node: none left sleeps a production default. Touched files 134 passed in 31.82s. Conjuncts 4-5 (verification.py record, acceptance solo run) out of scope.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-aa68dd29), bytes-first. The instruction: a kid's own tests are its CLAIM, not the parent's evidence; read the DIFF, run one negative probe per conjunct (brief.py:1771, cli.py:750). MECHANISM: git diff --cached on this worktree moved only 4 files -- test_rotation_alerts.py (2x delay_override=0), test_node_writer.py (new session-scoped live_node_round_trip fixture, both tests assert over its records), test_rotate_selfreap.py (belam test wait_secs=0.5), rotate.py (_reap_belam_oldest gains wait_secs: float = 5.0 forwarded to _reap_chain). No assertion removed: compared against the pre-round text, all five invariants in test 1 (unreadable/drift/non_fixpoint/checked>1000/byte_diffs<checked) and both in test 2 (drift, checked>1000) survive. I ran, not the kid: (1) the two after_join tests 2 passed in 0.07s (was 40.09s) and the whole after_join+rotation_alerts files 92 passed in 1.35s, and an AST-balanced scan of every run_after_join call in test_after_join_service.py found the only two lacking a seam are dry_run=True and a monkeypatched stub -- so no test reaches the real 20 s default; (2) the two corpus tests share one 8.92 s setup and the second passes ALONE in a fresh session (9.01s), proving no cross-test dependency; (3) inspect.signature ends wait_secs: float = 5.0 and the sole production caller (rotate.py:17711) passes none, so production behaviour is unchanged while the bounded test fell 18.53->5.04s. NEAR MISS: a shared (path,text) list satisfies the words 'one session-scoped corpus load' and saves ~0.2 s, because the walk is 0.10 s and the per-node render is the 8.5 s cost -- the kid measured that and shared the PASS, which is why the number moved; the node's own MEASUREMENT-THAT-CHANGED-THE-FIX paragraph is the honest record of it. What I did NOT verify and the next kid must: the whole-suite number is conjuncts 4-5, out of this kid's scope, and the deeper sleeps the kid left (test_dashboard.py:352, the 2 s proved-dead-pid idiom) ride until conjunct 5 measures whether they matter. The kid's reported defect -- conftest.py:293 _is_bare_directory_run refuses a file.py::node-id arg as a bare directory run -- is real and outside this round's scope; kept here as prior art.
<!-- THOUGHT:END -->
