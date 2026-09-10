---
id: hypothesis:l4b23-fixture-leak
mint_id: e039064d38144ad082c7adf5929c9bd0
type: hypothesis
parents:
  - idea:l4b23-fixture-leak
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
scaffold_hash: b2a6ef931e4b8476
season: 2
tags:
  - hypothesis
testable_claim: "test_send.py's `[ask] how do I rotate?` fixture cannot reach a live tmux pane or the real comms root -- today it fires by accident (owner, l4-plan A:32: \"The test fixture is firing by accident I think\")."
thought_session: sanctuary-helper-05
title: The rotate-fixture cannot reach a live tmux pane or the real comms root
---
<!-- BODY:BEGIN -->
# hypothesis:l4b23-fixture-leak

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.10 brief -- test_send.py's rotate-fixture reaches the REAL tmux session

ROOT CAUSE, confirmed by reading the code (not guessed): `send_dm()` in
`extensions/agi/bin/send.py:507` calls `_nudge_window(None, other, text)`
UNCONDITIONALLY on every DM -- there is no test-mode guard and no parameter
a caller can use to suppress it. `_nudge_window` (send.py:352-386) treats
`tmux_session=None` as "use the REAL default": `tmux_session =
rotate.DEFAULT_TMUX_SESSION` (send.py:364-366), then runs a real `tmux
list-windows -t <that session>` and, if `window` (the `other` recipient
name, e.g. `"sanctuary-master"`) is a REAL window in that REAL session,
runs `tmux send-keys -t <session>:<window> <text> Enter` -- typing the
test's literal text into a live agent's terminal. `ask()` (send.py:531-547)
and `report()` both route through `send_dm`/`send_room`, so EVERY test in
`test_send.py` that calls them -- including `test_ask_writes_tagged_dm_to_
registered_master` (line 751-760, recipient `"sanctuary-master"`) and
`test_report_refuses_without_matching_ask_from_named_asker` (line 790-800+,
via the `comms` fixture at line 296-297) -- reaches this same unconditional
nudge. On THIS box, where a real `agi-rc` tmux session runs live seats
during test runs, any test whose recipient name happens to match a live
window name will inject text into that agent's real terminal. That is
what the owner's "The test fixture is firing by accident I think" means.

FILE: extensions/agi/bin/send.py (send_dm, send_room, _nudge_window and
their call sites in ask/report), plus extensions/agi/tests/test_send.py
(the fixtures/tests that exercise them).

CHANGE (you choose the cleanest of these, or a better one you find --
this is the actual engineering decision, not pre-made for you):
(a) thread an explicit `tmux_session` override through `send_dm` /
    `send_room` / `ask` / `report` so callers (including tests) can pass a
    guaranteed-non-live session name instead of relying on the `None` ->
    real-default path, or
(b) add a module-level test seam (e.g. an autouse fixture in
    test_send.py, or a `conftest.py`) that monkeypatches `_nudge_window` (or
    the `subprocess.run` calls inside it) to a no-op for the whole test
    file, or
(c) make `_nudge_window` refuse to touch `rotate.DEFAULT_TMUX_SESSION`
    when a recognized test-mode env var is set.
Whichever you pick, the fix must not change `_nudge_window`'s real,
intentional production behaviour (best-effort nudge into a live seat's
window) -- only make TESTS incapable of reaching it.

VERIFY: before your fix, show (by temporarily instrumenting or by
reasoning from a passing/failing assertion) that running
`test_ask_writes_tagged_dm_to_registered_master` today calls
`subprocess.run(["tmux", "list-windows", ...])` against the REAL
`rotate.DEFAULT_TMUX_SESSION` name. After your fix, show the same test
run touches NO real tmux session at all (mock/monkeypatch asserts zero
real subprocess calls, or asserts calls only against an injected fake
session name). Run ONLY `python3 -m pytest extensions/agi/tests/test_send.py -q`
-- never the full suite (the prime is coordinating full-suite runs this
round; ask first if you think you need it, don't run it).

KID CEILING: 2. This is a small, single-concern fix in one file plus its
test file; a second kid is for review/cleanup only if the first kid's
diff needs it, not for parallel exploration.

DO NOT: touch any other file. Do not add a build node -- this round mints
chain + evidence only, no build. Do not run `git add -A`; stage only the
files you actually changed. Do not run `grid.py commit --all` on this
seat branch (branch-blind refusal by design) -- your worktree's protocol
ends at `git commit` + `git push` on your own branch/worktree, the parent
director merges upward.

REPORT: write one `experiment` node whose `parents` is this hypothesis,
with a verdict on the testable claim (`proved` only if you actually ran
the before/after tmux-isolation check above and it holds; otherwise
`inconclusive_lean_proved`/`disproved` with your reasoning).
`evidence_runs` must be a list of node ids that resolve in the corpus;
your own experiment node counts once it exists. List every verify command
you ran and its actual output in the body. Say plainly which of the three
CHANGE options you took and why.
