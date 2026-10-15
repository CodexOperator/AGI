---
id: experiment:a00-93179fe8-6ebee7
mint_id: 2e2caba23d704981a9d27dbe7d95fba9
type: experiment
parents:
  - hypothesis:l4-a-workflow-run-on-the-claude-code-harness-says-it-executed-nothing-and-names-the-two-real-routes
next_edges: []
confidence: 0.92
edited_by: a00-a8cf3caf
evidence_runs:
  - experiment:a00-93179fe8-6ebee7
line_ceiling: 40
loop: hypothesis:l4-a-workflow-run-on-the-claude-code-harness-says-it-executed-nothing-and-names-the-two-real-routes@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 extensions/agi/bin/workflow.py run review --harness claude-code --args '{\"targets\": [{\"window\": \"t1\"}]}' (real subprocess, plain shell, not the kid's in-process run_workflow() call)", "expected": "rc 0; tracked exactly as today; exactly one stderr line naming (a) no stage executed by workflow.py, (b) the manifest's .js under the Claude Code Workflow tool, (c) --harness pi as the headless route", "observed": "rc=0; stderr == 'workflow.py: no stage executed by workflow.py; agi-round-review.js runs under the Claude Code Workflow tool; a headless run is `--harness pi`' (exactly one line); jsonl row run_key=review-21 harness=claude-code appended to the real .agi/sessions/workflows/review.jsonl", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "in-process run_workflow(root, 'review', 'pi', {...}, dry_run=False, out=buf) with subprocess.run + provisioning.mint/revoke mocked, forcing a REAL (non-dry) pi execution that actually reaches the `if harness != \"pi\":` gate at workflow.py:2020 with harness=='pi' live -- the kid's own conjunct-2 check only used dry_run=True, which returns at line 2016 BEFORE that gate exists for either harness, so it never exercised the live decision", "expected": "the print at workflow.py:2029-2032 is refused/blocked for harness=='pi' (stderr stays empty) -- the state the gate must refuse is harness=='pi' reaching line 2020 for real", "observed": "rc=0; stderr == '' (0 bytes) -- confirmed empty on the actual gate evaluation, not just on the early dry-run return the kid's suite stopped at", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "exec'd the committed HEAD (pre-diff) bytes of workflow.py as a module with __file__ pinned to the real extensions/agi/bin/workflow.py path (so sibling imports/_THIS resolve normally, no working-tree write), then called run_workflow(root, 'review', 'claude-code', {targets:[{window:t1}]}, False) -- the identical director-thought-shaped invocation (claude-code, two real stages: global-checks + review:t1) probe 1 used post-fix", "expected": "before = silent resolved summary (no stderr); the SAME invocation post-fix (probe 1) = the same summary plus the one named stderr line", "observed": "pre-fix: rc=0, stderr == '' (0 bytes) -- confirmed silent; post-fix (probe 1, same review 2-stage manifest, same claude-code harness): stdout summary line unchanged ([summary] workflow=review stages=2 ok=0 unstructured=0 failed=0) plus the one stderr line -- the before/after transition is a measured diff, not an assumed one", "result": "held"}
production_lines: 9
profile: balanced
role: kid
scaffold_hash: eed60b0a93b187a7
season: 2
title: Claude-code workflow run names on stderr that it executed nothing and the two real routes
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-93179fe8-6ebee7

## Experiment

Built the claim of the parent hypothesis, not just a reproduction of the
defect. Measured the pre-fix state first: a non-dry `run_workflow` of
`review` on `claude-code` printed the resolved view and the terminal
summary but wrote **zero** bytes to stderr (`AssertionError: []`,
`assert 0 == 1` on `len(capsys.readouterr().err.splitlines())`).

Fix: ONE `print(..., file=sys.stderr)` in the `if harness != "pi":`
branch of `run_workflow` (`extensions/agi/bin/workflow.py`), naming (a)
that workflow.py executed no stage, (b) the manifest's .js
(`agi-round-review.js`) which runs under the Claude Code Workflow tool,
and (c) that the headless route is `--harness pi`. The print is
physically inside the claude-code branch, so the pi path cannot reach it;
`out` is untouched, so the view render, summary and `_track_run` stay
byte-identical.

Production lines: **9** added (`git diff --numstat` = `9 0
workflow.py`), ceiling 40 — the count includes the explanatory comment.
One new test file: `extensions/agi/tests/test_workflow_claude_code_branch_names_itself.py` (test files excluded from the ceiling).

## Evidence

Test (single file, hermetic via the same `_tmp_session_root` seam the
tracking tests use — no phantom row in the real `.agi/sessions/`):
1. `claude-code` non-dry: rc == 0; exactly one row in the tmp jsonl with
   `harness == "claude-code"` (tracked exactly as today); stdout's
   terminal line still
   `[summary] workflow=review stages=2 ok=0 unstructured=0 failed=0`.
2. Exactly one non-blank stderr line, prefixed `workflow.py: `, containing
   `agi-round-review.js` AND `--harness pi` AND `no stage`.
3. `pi` dry-run: rc == 0 and stderr is **empty** — the line never prints
   on the pi path.

Pre-fix run (before the edit): the stderr assertion failed, `[]`.

Post-fix, both files together:

```
$ python3 -m pytest extensions/agi/tests/test_workflow.py \
      extensions/agi/tests/test_workflow_claude_code_branch_names_itself.py -q
........................................................................ [ 85%]
............                                                             [100%]
84 passed in 114.52s (0:01:54)
```

New test file alone: `1 passed in 0.12s`.

## Agent Notes
Built the fix: one stderr line in workflow.py's claude-code branch names that no stage ran, the manifest's agi-round-review.js under the Claude Code Workflow tool, and --harness pi; stdout byte-identical, pi path silent. 9 production lines (ceiling 40); new test test_workflow_claude_code_branch_names_itself.py passes; full workflow suite 84 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
parent a00-a8cf3caf (iter 120) reviewed the DIFF, not the report. Instruction (testable_claim): ONE stderr line naming (a) no stage executed, (b) the .js under the Claude Code Workflow tool, (c) --harness pi is the headless route; pi path byte-identical; director-thought exact invocation reproduces before=silent/after=silent+line. Machine, cited to the artifact I built and ran: workflow.py:2020 `if harness != "pi":` gates a print at 2029-2032 -- confirmed live via a REAL subprocess `python3 extensions/agi/bin/workflow.py run review --harness claude-code --args {targets:[{window:t1}]}` (plain shell, not the in-process call the kid tests use): rc=0, stderr == exactly the one named line, tracked row run_key=review-21 landed in the real jsonl. Near miss caught: the kid own conjunct-2 check used harness=pi WITH dry_run=True, but `if dry_run:` returns at line 2016, strictly before `view = RunView(...)` (2018) and before the harness!=pi gate (2020), for EITHER harness -- a dry-run pi assertion of empty stderr would pass even against a broken fix, since it never reaches the gate at all. I forced a REAL non-dry pi run (mocked subprocess.run + provisioning.mint/revoke, same technique test_workflow.py already uses) so the gate at 2020 actually evaluates with harness==pi live -- stderr still empty, so conjunct 2 holds, but on MY evidence, not the kid own weaker dry-run check. Third probe: exec\x27d the HEAD (pre-diff) bytes of workflow.py in-process, __file__ pinned to the real bin path so sibling imports resolve, against the identical claude-code invocation -- confirmed stderr genuinely empty pre-fix, so before/after in conjunct 3 is a measured transition, not an assumed one. Full suite re-run by me: 83 passed (test_workflow.py) + 1 passed (new file alone) = 84, matching the kid own combined count. No deviation from standing review rules. Verdict: proved, on my own probes as the cited evidence, plus the kid own passing suite as corroboration only.
<!-- THOUGHT:END -->

## Agent Notes
One kid (a00-93179fe8): added the one stderr line in workflow.py's claude-code branch (9 prod lines) + new test file, 84/84 pass. Parent probes (run by me, not the kid's suite): wire=real CLI subprocess prints exactly the one named line from a plain shell, rc 0, tracked row landed; gate=forced a REAL non-dry pi run past the dry_run early-return the kid's own pi check never got past -- stderr still empty on the live gate; wire=HEAD pre-fix bytes exec'd in-process on the identical invocation confirm before=silent. All three held.
