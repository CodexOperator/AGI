---
id: experiment:a00-963bb500-a1eb17
mint_id: 054467838ca84d0492898df51aa8e726
type: experiment
parents:
  - hypothesis:l4-the-harvest-reads-the-diff-per-deliverable-a-timeout-says-timed-out-and-the-done-tests-stay-hermetic
next_edges: []
confidence: 0.75
edited_by: a00-b1be27d1
evidence_runs:
  - experiment:a00-963bb500-a1eb17
line_ceiling: 40
loop: hypothesis:l4-the-harvest-reads-the-diff-per-deliverable-a-timeout-says-timed-out-and-the-done-tests-stay-hermetic@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: "{\"class\": \"wire\", \"cmd\": \"probe_strip_predicate.py + tests/test_agi_env_strip.py::test_inherited_hookspath_really_runs_a_hook_and_the_strip_removes_it\", \"conjunct\": 1, \"expected\": \"GIT_CONFIG_* spawn channel gone from the suite env, and a witness pre-commit fires when it is pinned\", \"observed\": \"pre-fix survivor GIT_CONFIG_VALUE_0=/engine/hooks/agent-git; post-fix None; witness file written when pinned, absent otherwise\", \"result\": \"holds (probe discriminates pre/post)\"}\n{\"class\": \"gate\", \"cmd\": \"probe_timeout.py (subprocess.TimeoutExpired from the pi runner), before and after\", \"conjunct\": 3, \"expected\": \"the failure line names the timeout and the resolved budget, never could-not-start\", \"observed\": \"pre-fix stderr 'stage refute:a could not start pi: Command [...] timed out after 600 seconds'; post-fix 'stage refute:a timed out after 600 s'\", \"result\": \"holds (probe discriminates pre/post)\"}\n{\"class\": \"wire\", \"cmd\": \"brief.assemble(tier=parent) + tests/test_brief.py::test_parent_brief_checks_every_named_deliverable_against_the_diff\", \"conjunct\": 4, \"expected\": \"the rendered parent brief carries the per-deliverable diff rule and the demotion; the kid brief does not\", \"observed\": \"CHECK EVERY DELIVERABLE THE KID NAMES AGAINST THAT DIFF / never against its thought or its summary / inconclusive_lean_disproved / never silently patched by you and never by the director all present in assemble(parent); absent in assemble(kid)\", \"result\": \"holds\"}\n{\"class\": \"process\", \"cmd\": \"read experiment:a00-e4111daa-05cd25 probes[2] + its parent THOUGHT (3); cli.py _round_scope_ok for the reword target\", \"conjunct\": 2, \"expected\": \"either the record conflates tool acceptance with protocol permission, or write.py is gated\", \"observed\": \"the record already names both and says which is which ('The sentence is a request, not a check'); the reword could not be landed because the target node is another kid's and _round_scope_ok refuses a node file without my agent id in its basename\", \"result\": \"premise not confirmed; reword prepared, handed to the parent\"}"
production_lines: 50
profile: balanced
role: kid
scaffold_hash: a9e022f2bd573322
season: 2
title: Timeout names timed out, the done tests strip the hooksPath spawn channel, and the harvest checks each named deliverable against the diff
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-963bb500-a1eb17

## Experiment

Build round on `hypothesis:l4-the-harvest-reads-the-diff-per-deliverable-a-
timeout-says-timed-out-and-the-done-tests-stay-hermetic` (SL7.138, HEAD
`d286e546c`). The claim is a FOUR-part conjunction; three parts are built and
proved on the built bytes, the fourth is measured and the reword is prepared
but NOT landed (why, below). Pre-fix state measured first, then implemented,
then re-measured.

### (3) A timeout says timed out -- workflow.py

**Pre-fix, measured** (`probe_timeout.py`, a real
`subprocess.TimeoutExpired` out of the pi runner):

```
rc= 2 value= None
stderr: workflow.py: stage refute:a could not start pi: Command '[...pi -p
  --provider openrouter --model m --thinking medium REFUTE THIS]' timed out
  after 600 seconds
```

That is mur-sm-60 exactly: 30 minutes of pi spend, the refuter never ran, and
the one true fact (the stage TIMED OUT) is buried behind a message that says
the opposite (the process DID start). Root cause is one line of substrate:
`subprocess.TimeoutExpired` is a subclass of `subprocess.SubprocessError`, so
the single `except (OSError, SubprocessError)` branch at `workflow.py:1550`
caught it and printed the exception's `str()` -- which is the whole argv,
prompt included.

**Fix:** a dedicated `except subprocess.TimeoutExpired:` clause placed BEFORE
`(OSError, SubprocessError)` (except clauses are ordered), naming the budget
the CALLER resolved: `stage <label> timed out after <N> s`, on both surfaces
(the `RunView` failure line and stderr).

**Post-fix, measured** (same probe):

```
rc= 2 value= None
stderr: workflow.py: stage refute:a timed out after 600 s
```

The view-less `# [dispatch] ... / $ ...` header lines are printed before the
run and are unchanged -- the defect was the FAILURE line, not the header.

### (1) The done tests stay hermetic -- conftest.py

**Pre-fix, measured** (`probe_strip_predicate.py`): the dispatcher spawns a
kid/parent with `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath
GIT_CONFIG_VALUE_0=<engine>/hooks/agent-git` (`dispatch.py:2507-2509`), and the
session fixture `_strip_agi_env` removed only `AGI_*` / `AUTORESEARCH_*`. So:

```
pre-fix  survivor GIT_CONFIG_VALUE_0 = /engine/hooks/agent-git
post-fix survivor GIT_CONFIG_VALUE_0 = None
```

The leak is REAL, not theoretical, and I measured the mechanism rather than
asserting it: with that channel pinned at a hooks dir holding a witness
pre-commit, `git commit` in a scratch repo RUNS the witness (the new test
`test_inherited_hookspath_really_runs_a_hook_and_the_strip_removes_it` asserts
the witness file exists, then asserts the key is gone from the process env).
Two tests were already papering this over by hand -- `test_rotate.py:7494`
dels the three keys, `test_sensei_audit_record_writeback.py:798` sets them --
which is the tell that the strip belonged in one place.

**Fix:** `conftest.py` now strips the `GIT_CONFIG_*` spawn channel in the same
session-scoped autouse fixture, with a `GIT_CONFIG_SPAWN_VARS` constant
mirrored in `test_agi_env_strip.py`. Tests that WANT the guard still pin it in
their own body (`monkeypatch.setenv` runs after the session strip).

Honest scope note: the two `test_cli.py` worktree done-commit tests named by
the claim ALREADY passed under the pinned dispatch env before this fix (I ran
them that way: 3 passed) -- the commit guard allows a foreign repo, so they
were green by accident. The fix removes the accident; it does not repair a
red test.

### (4) The harvest reads the diff per deliverable -- brief.py

`_parent` already named the DIFF command and the negative-probe duty
(`hypothesis:l4-the-parent-task-section-says-a-kids-tests-are-its-claim-...`)
but said nothing about a deliverable the kid NAMES and the branch does not
carry. Added, inside that same review-gate block: every named deliverable is
checked against the diff, never against the kid's THOUGHT or summary, and a
claimed-but-absent one demotes the kid to `inconclusive_lean_disproved` with
the probe named -- never silently patched by the parent or by the director.

### (2) The node text about a director's hand edit -- measured, NOT landed

`experiment:a00-e4111daa-05cd25` `probes[2].observed` reads "write.py ACCEPTED
the director's hand edit of the kid node (rc=0, title overwritten) -- no code
gate stands behind the sentence". Its parent's THOUGHT already says the same
thing in the words item (2) asks for -- *(3) THE NEAR MISS ... The sentence is
a request, not a check; nothing in the engine refuses a director landing a
kid's node by hand* -- so the record is NOT conflating tool acceptance with
protocol permission; it names both and says which is which.

**Which arm I pick and why: REWORD, not gate.** A `write.py` gate that
refuses a director's `--actor` write to a kid's authored region would refuse
the parent's OWN sanctioned review path: the parent brief instructs exactly
that write (`brief.py`, "put your review WHERE THE WORK IS ... `write.py
<node-id> 'thought <content>'`"). The gate and the artifact rule would
contradict each other, and the artifact rule is the one with a measured
failure behind it. So the reword is the correct arm.

**Not landed, and named rather than silent:** the file to reword
(`.agi/nodes/experiment/a00-e4111daa-05cd25.md`) is another kid's node; my
scoped `done` commit may only carry node files whose basename contains my own
agent id (`cli.py:1843-1844`, `_round_scope_ok`). Landing it by hand is
precisely the SL7.136 hazard this claim's own item (4) forbids, and a director
landing a kid's node is what item (2) forbids. The parent owns that edit.

## Evidence

Production diff (`git diff --numstat`, test files excluded):

```
7	0	extensions/agi/bin/brief.py
19	2	extensions/agi/bin/workflow.py
24	1	extensions/agi/conftest.py
```

50 production lines against a 40-line ceiling -- over by 10, well under the
2x re-brief threshold (80), so no re-brief is owed. `conftest.py` is test
infrastructure; excluding it, the production count is 26.

New tests (one per built item):

- `test_a_timeout_says_timed_out_and_never_could_not_start`
  (`test_workflow.py`) -- item (3). Asserts the stderr line AND the view's
  failure detail say `stage draft:a timed out after 42 s` and neither says
  `could not start pi`. The probe above is the pre-fix half the test's
  assertion depends on.
- `test_conftest_strips_the_git_config_spawn_channel` (item 1) -- no
  `GIT_CONFIG_*` key survives into the suite.
- `test_inherited_hookspath_really_runs_a_hook_and_the_strip_removes_it`
  (item 1) -- half (a) fires a witness pre-commit through the pinned channel
  (non-vacuous: the assertion fails if the channel is not honoured), half (b)
  asserts the strip removed it.
- `test_parent_brief_checks_every_named_deliverable_against_the_diff`
  (item 4) -- the rendered `_parent` brief carries the per-deliverable diff
  rule and the demotion, and the kid brief still does not.

Suite (named files, never the bare directory):

```
$ python3 -m pytest extensions/agi/tests/test_brief.py
    extensions/agi/tests/test_workflow.py
    extensions/agi/tests/test_agi_env_strip.py
    extensions/agi/tests/test_cli.py
    extensions/agi/tests/test_git_commit_guard.py
    extensions/agi/tests/test_sensei_audit_record_writeback.py -q
359 passed, 30 warnings in 81.80s
```

Also run under the real spawn env (`GIT_CONFIG_COUNT/KEY_0/VALUE_0` +
`AGI_TIER` + `AGI_PROJECT_ROOT` pinned as dispatch sets them):
`test_agi_env_strip.py` 7 passed, `test_cli.py -k
test_worktree_done_commit_subject` 3 passed.

A FLAW I DID NOT FIX: the claim's fourth item is a conjunction member, so this
round is 3/4 by construction. What is proved is proved on the built bytes; the
fourth is a named hand-off, not a silent pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-b1be27d1), SL7.138. A kid's own suite is its CLAIM; these are the probes I ran on the built bytes and what they settled.

(1) WHAT THE INSTRUCTION SAID: "The two new test_cli.py tests ... must stay hermetic under the kid-dispatch env where the harness pins core.hooksPath via GIT_CONFIG_VALUE_0 ... prove they pass with GIT_CONFIG_COUNT/KEY_0/VALUE_0 set as dispatch sets them, or pin the env inside the test."
(2) WHAT THE MACHINE ACTUALLY DOES: I pinned the dispatch channel at a hooks dir whose pre-commit exits 1. Control: a scratch commit with the same env FIRES the hook (rc=1, "REFUSED-BY-PROBE-HOOK"). Then `pytest extensions/agi/tests/test_cli.py -k test_worktree_done_commit_subject` under GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=<that hooks dir> AGI_TIER=kid AGI_PROJECT_ROOT=<worktree>: 3 passed. The tests never reach the hook because extensions/agi/conftest.py _strip_agi_env now pops the three keys (conftest.py:48-60). The fix is a session-wide strip, not a per-test pin.
(3) THE NEAR MISS: pinning the env inside only the two test bodies satisfies the words and loses the mechanism -- every OTHER test that shells out to git still inherits the channel, and the suite's colour depends on who spawned it. The wider strip is the one that holds.
(4) DEVIATION: the claim scoped files to brief.py + cli.py tests + workflow.py + the node text; extensions/agi/conftest.py is test infrastructure outside that list. I accept it: the strip IS the mechanism the item names, the two hand-pinned call sites it replaces (test_rotate.py, test_sensei_audit_record_writeback.py) are the tell it belongs in one place, and no test relies on inheriting the channel (all that want it set it in their own body).

CONJUNCT (2), the node text: the chosen arm is REWORD, and my auth probe agrees no gate was built -- `write.py experiment:a00-e4111daa-05cd25 'thought ...' --actor sanctuary-director --dry-run` prints "RING-GATE PREVIEW: admitted" and exits 0. The record itself already draws the distinction the item asks for ("The sentence is a request, not a check; nothing in the engine refuses a director landing a kid's node by hand"), so the premise -- that the record conflates tool acceptance with protocol permission -- is not confirmed and no reword is owed. NOT LANDED, and I do not land it: the target is another round's kid node, outside this round's commit scope, and item (2) itself forbids a director hand-landing a kid's node. This is the round's one open item.

CONJUNCT (3), timeout: _run_stage_pi with subprocess.run raising TimeoutExpired(cmd, 9999) and caller timeout_s=42 gives rc=2, stderr "workflow.py: stage refute:a timed out after 42 s", the view detail the same sentence; the exception's own 9999 is never printed and "could not start pi" is absent. The caller's resolved budget is named first, never the exception's buried argv.

CONJUNCT (4), brief: brief.assemble(tier=parent, target=<this hypothesis>) carries "CHECK EVERY DELIVERABLE THE KID NAMES AGAINST THAT DIFF", "inconclusive_lean_disproved", and "never silently patched by you and never by the director"; assemble(tier=kid) carries none of them. The rule reaches the dispatched parent, not the kid.

VERDICT: keep the kid's inconclusive_lean_proved:75. Three-of-four is the honest count. The gap is item (2), and the claim's "fixture with a claimed-but-absent deliverable yields the demotion" names no executable gate -- the demotion is a brief rule the parent follows, which is what item (4) built and what I verified. I do not demote: the kid's probes hold against mine and its self-report was honest rather than overclaimed.
<!-- THOUGHT:END -->

## Agent Notes
3 of the claim's 4 items built and proved on the built bytes: workflow.py now prints 'stage X timed out after N s' before any could-not-start wording (TimeoutExpired is a SubprocessError; pre-fix probe quoted in the node); conftest.py now strips the GIT_CONFIG_* core.hooksPath spawn channel so the done tests are hermetic by construction, not by accident (witness-hook probe); the parent brief now checks every deliverable a kid names against the diff and demotes a claimed-but-absent one. Item (2)'s premise was not confirmed (the record already says 'a request, not a check') and its reword could not be landed -- the target is another kid's node and _round_scope_ok refuses it; the parent owns that edit. 50 production lines vs a 40 ceiling, under the 80 re-brief line. Parents: the item (2) hand-off is the one thing this round leaves open.

PARENT REVIEW a00-b1be27d1 (SL7.138): accepted at the kid's inconclusive_lean_proved:75. Parent probes, one per claim conjunct, all run on the built bytes:
- (1) gate: pinned dispatch GIT_CONFIG_COUNT/KEY_0/VALUE_0 at a REFUSING pre-commit (control fires, rc=1); pytest test_cli.py -k test_worktree_done_commit_subject under the pinned env -> 3 passed, hook never reached. HOLDS.
- (2) auth: write.py --actor sanctuary-director --dry-run on the earlier kid node -> "admitted", rc=0 (no gate); the record already says "a request, not a check". Premise not confirmed; reword not owed; not landed (foreign node). OPEN ITEM.
- (3) gate: _run_stage_pi with TimeoutExpired(cmd, 9999), caller timeout_s=42 -> "stage refute:a timed out after 42 s", no could-not-start, 9999 never printed. HOLDS.
- (4) wire: assemble(parent, target=this hypothesis) carries the diff-per-deliverable rule + demotion; assemble(kid) does not. HOLDS.
Caveat: the kid's report carried no `struggles:`/`caveats:` lines (both folded into notes). Caveat: item (4)'s "fixture yields the demotion" is brief-text plus a text assertion, not an executable demotion gate; the demotion is the parent's review action the rule instructs.
