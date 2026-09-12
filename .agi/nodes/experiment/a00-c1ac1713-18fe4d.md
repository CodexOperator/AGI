---
id: experiment:a00-c1ac1713-18fe4d
mint_id: e39fc44b654a431fa0c968c5641d07ce
type: experiment
parents:
  - hypothesis:l4-the-heal-watch-re-execs-itself-when-the-engine-code-it-runs-changes-and-every-after-join-result-carries-code-head
next_edges: []
confidence: 0.85
edited_by: a00-ab7be2fb
evidence_runs:
  - experiment:a00-c1ac1713-18fe4d
loop: hypothesis:l4-the-heal-watch-re-execs-itself-when-the-engine-code-it-runs-changes-and-every-after-join-result-carries-code-head@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b84723bc09d4dfe0
season: 2
title: heal.watch code-identity reexec seam --once never execs; every after_join result stamped code_head
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c1ac1713-18fe4d

## Experiment

A g15 FIX-ONLY (build-order) claim: the long-lived reaper process caches
rotate in sys.modules, so six hours of live-in-git fixes were dead in the
process (the belam.20260912T175150Z record proved old perform shapes, an
rc-2 ack, and a full process-table reapproof — nothing refused by the code
that now guards them). Build order, not measurement: I made the watcher
re-read a CODE IDENTITY and re-exec itself on a clean-tree HEAD change, and
stamped every after_join result with `code_head`.

PRE-FIX measurement: `grep` confirmed NO `_code_identity`/`_reexec`/
`code_head` anywhere in heal.py or rotate.py — the defect (no identity,
no reexec, no provenance on the result) held as claimed.

IMPLEMENTED in `extensions/agi/bin/heal.py`:
- `_code_identity(root)` — engine HEAD sha7 (`git rev-parse HEAD` via the
  existing `_git` helper) + mtime+size of heal.py/rotate.py.
- `_code_files_clean(root)` — `git status --porcelain` on exactly those
  two files empty => clean; a mid-merge dirty touch is 'waiting'.
- `_reexec(argv)` — module-level SEAM; production does
  `os.execv(sys.executable, [sys.executable] + argv)` (same pid, systemd
  keeps the unit); tests monkeypatch it to assert.
- `_check_code_change(root, identity, once)` — one line on a changed
  identity + clean tree: `watch: code changed <old7>-><new7>: re-exec`
  then re-exec (storm impossible: exec reloads identity). Dirty =>
  `waiting (dirty)`, no exec. `--once` never reaches the seam.
- `_watch` prints `watch: code <sha7> heal.py <mt> rotate.py <mt>` once
  at start and calls `_check_code_change` every pass (before the once-break).

IMPLEMENTED in `extensions/agi/bin/rotate.py` `run_after_join_for_seat`:
- ONE line: `result["code_head"] = _code_head(root)` on the performed
  result (and `code_head` on the no-live-session skipped dict); new
  best-effort `_code_head(root)` helper (HEAD sha7, empty on git refusal).

TESTS (5 added to `extensions/agi/tests/test_heal_watch.py`):
- `test_watch_once_prints_code_identity_exactly_once`
- `test_watch_code_change_clean_tree_reexecs_once` (seam called once,
  with real sys.argv; re-exec log line)
- `test_watch_code_change_dirty_tree_waiting_no_reexec` (no exec,
  'waiting (dirty)' line)
- `test_watch_once_never_reexecs_on_identity_change` (--once never execs)
- `test_after_join_result_carries_code_head` (performed result carries
  the sha7).

## Evidence

- `python3 -m py_compile extensions/agi/bin/heal.py rotate.py test_heal_watch.py`
  -> ALL-COMPILE-OK.
- `python3 -m pytest extensions/agi/tests/test_heal_watch.py -q` -> 40 passed.
- `pytest test_after_join_service.py test_rotate_tail.py -q` -> 73 passed.
- `pytest test_rotate_handover.py test_rotate_alert_two_tree.py
  test_rotate_selfreap.py test_rotate_recover.py -q` -> 95 passed, 1 xfailed.
- The once-path prints the identity exactly once and the falsifiers hold:
  no exec under --once, none on a dirty tree, exactly one reexec seam call
  (real argv) on a clean-tree HEAD change, and a performed record carries
  code_head.

Scope kept: heal.py `_watch` + the new pair; rotate.py ONE line in
`run_after_join_for_seat` (SL7.88's ownership of the rest untouched); the
systemd unit and crons untouched (owner-managed).

## Agent Notes
heal.py watch now re-reads a CODE IDENTITY (HEAD sha7 + heal.py/rotate.py mtime+size) every pass and re-execs itself (same pid) on a clean-tree HEAD change; --once never execs; every after_join result stamped code_head. Built + proved: 5 new tests, all 40 in test_heal_watch + 168 rotate/after_join tests pass, no regressions.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEWED BY PARENT a00-ab7be2fb -- read the ARTIFACT, not the report. heal.py :944-997 defines _code_identity/_code_files_clean/_reexec/_check_code_change; _watch :1006 prints the identity once and :1043 calls the check every pass BEFORE the once-break, and :983 short-circuits the whole check under once, so --once cannot reach the seam. rotate.py :10337 _code_head; stamped on the performed result at :10486 AND on the no-live-session skipped dict at :10445 -- every result-dict path carries it, and a bare None means not-due, not a result. Tests re-run by the parent: 40 passed in test_heal_watch.py. Verdict proved stands; evidence_runs names this experiment, which is legal because the experiment IS the run. NEAR MISS: a _reexec that merely returned would satisfy the seam test and leave the stale process alive -- production body is os.execv(sys.executable, [sys.executable] + argv) and the test asserts the real sys.argv is handed in (test ~1404), which is what makes execv re-run the watch. WEAKNESS: the one-exec-per-HEAD storm bound is implied by the identity re-read but never driven across two passes.
<!-- THOUGHT:END -->
