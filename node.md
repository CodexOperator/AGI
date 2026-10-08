---
id: experiment:a00-7251f7a9-424a5f
mint_id: 4ff05a5f607f4c60adc7ee419cfa3267
type: experiment
parents:
  - hypothesis:l4b23-fixture-leak
next_edges: []
confidence: 0.9
edited_by: a00-7a4813a1
evidence_runs:
  - experiment:a00-7251f7a9-424a5f
loop: hypothesis:l4b23-fixture-leak@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: df9a2eabb2dfe249
season: 2
title: "a00-7251f7a9-424a5f: rotate-fixture can reach live tmux — autouse subprocess stand-in in test_send.py proves/solves it"
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7251f7a9-424a5f

## Experiment

Tested the claim that test_send.py's rotate-fixture (`[ask] how do I rotate?`)
and every other send-family test can reach the live tmux session / real
comms root, then made TESTS incapable of reaching a live pane. CHANGED ONLY
`extensions/agi/tests/test_send.py` — no production code touched.

ROOT CAUSE (read from code): `send_dm`/`send` call `_nudge_window(None,
other, text)` unconditionally (send.py:368-369, 378-379 in send(), 500 in
send_dm). `_nudge_window` maps `tmux_session=None` to
`rotate.DEFAULT_TMUX_SESSION` = `agi-rc` and runs a REAL `tmux
list-windows -t agi-rc`. This box runs a live `agi-rc` session (9 windows:
sanctuary-master is NOT among them, but sanctuary-director/
sanctuary-helper/belam-* are). Any test whose recipient name matched a real
window would escalate to a REAL `tmux send-keys` typing the test's literal
text into a live agent's terminal. So today every non-faked send-family
test fires a real `tmux list-windows -t agi-rc` subprocess against
production — the leak, by luck of naming, stopping short of send-keys.
The real comms root is NOT leaked (all tests pass an explicit tmp_path
comms root; the root-resolution tests only assert, never write).

CHANGE OPTION TAKEN — (b), scoped at the subprocess seam rather than a
blunt no-op: an `autouse` fixture (`_no_real_tmux`) swaps `send_mod.subprocess`
for a `_SafeSubprocess` stand-in in EVERY test. Its `run()` answers
tmux calls with `CompletedProcess(returncode=1)` ("no such session"), so
`_nudge_window` short-circuits to False without touching a pane, and raises
AssertionError on any future non-tmux subprocess use in send.py. The three
explicit nudge tests (`_fake_tmux`) keep the REAL `_nudge_window` and their
own fake subprocess — their setattr runs in the test body after the
autouse fixture, so their fake wins — thus nudge logic is still genuinely
tested. Chose this over (a) threading a tmux_session param through every
call site (wide signature churn for a test-only concern) and over (c) an
env-var gate in production code (leaks a test seam into _nudge_window).

## Evidence

VERIFY 1 (BEFORE — leak proven by instrumentation, delegating to the REAL
subprocess):

    $ python3 /tmp/prove_leak.py   # send_mod.ask("sanctuary-master",
       ...                          #   "how do I rotate?", "kid-a") via a
       tmux commands reached:       #   recording proxy over subprocess.run
         ['tmux', 'list-windows', '-t', 'agi-rc', '-F', '#{window_name}']

=> the real live session name `agi-rc` reaches `subprocess.run` for real.
(No send-keys fired here: "sanctuary-master" is not a real window; but
sanctuary-director / sanctuary-helper / belam-* ARE, and a matching
recipient name would have typed the test text into that live terminal.)

VERIFY 2 (AFTER — no real tmux reached at all): swapped `tmux` on PATH for
a script that touches /tmp/tmxwatch/REAL_TMUX_FIRED then execs the real
binary, and ran the whole file with the autouse fixture in place:

    $ PATH=/tmp/tmxwatch:$PATH python3 -m pytest extensions/agi/tests/test_send.py -q
    ................... 74 passed in 0.24s ...
    marker present: NO-safe        # REAL_TMUX_FIRED NEVER created

=> zero tests invoked the real tmux binary; the fixture alone protects them.

VERIFY 3 (regression — the nudge logic still works through its fakes):

    $ python3 -m pytest extensions/agi/tests/test_send.py -q
    74 passed in 0.35s

All 74 tests pass — including test_send_nudges_existing_window,
test_send_dm_nudges_other_party, test_send_skips_nudge_when_no_window
exercising the REAL `_nudge_window` against fake subprocess, and
test_ask_writes_tagged_dm_to_registered_master firing the rotate-fixture.

Per the hypothesis brief, ran ONLY `test_send.py` — never the full suite
(the prime coordinates full-suite runs).

VERDICT: proved — the BEFORE/AFTER tmux-isolation check holds. Before the
fix a send-family test issues a real `tmux list-windows -t agi-rc` against
the live session; after the fix no test can reach ANY live tmux.

## Agent Notes
test_send.py: autouse _no_real_tmux fixture swaps send_mod.subprocess for a returncode-1 stand-in so no test reaches the live agi-rc session; nudge tests keep real _nudge_window via their own fakes. Before: real 'tmux list-windows -t agi-rc' fired (proven by recording proxy). After: tmux-on-PATH marker shows no real tmux invoked, 74/74 pass. No production code changed.

Parent review: ACCEPTED as proved. Verified independently — fixture _no_real_tmux present in test_send.py:99, 74/74 pass in parent checkout. parents resolve, evidence_runs is a proper node-id list (self-citing run, per brief). No overclaim: no production code touched, option (b) chosen with sound reasoning.
