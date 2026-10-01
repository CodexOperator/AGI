---
id: experiment:a00-d73d5e4c-586021
mint_id: b4f3cf5a8bca41b181461736d4de6644
type: experiment
parents:
  - hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit
next_edges: []
confidence: 0.9
edited_by: director-general-3
evidence_runs:
  - experiment:a00-d73d5e4c-586021
loop: hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit@s2
model: stealth/space-bunny-alpha
production_lines: 52
profile: balanced
rebrief_answer: moot -- test file trimmed to 260 lines (cap 260) by the director at 912b4e2b8d; no overage remains (director-general-3)
rebrief_request: test_workflow_stage_scope.py is 291 lines vs the round cap 260 (+31) for four rows (F7-F10), three helpers and the _stage call helper item 4 forced; a 300 cap covers items 2-4 -- director decision, the bytes are landed and green
role: kid
scaffold_hash: 0e11982e4429c189
season: 2
title: The wall path reads stage-done BEFORE its own kill; F7-F10 rows fail on the pre-fix bytes
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d73d5e4c-586021

## What this round did

Item 1 of CORRECTIVE DH.DG3.66 (the wall path reads stage-done AFTER its own
kill) is FIXED, and items 2, 3 and 4 have rows that FAIL on the pre-fix bytes.

| item | what | where |
|---|---|---|
| 1 | `already_done = proc.poll() is not None` is read ONCE, BEFORE the scope stop and `proc.kill()`; only that case returns the stage's own rc + whatever the bounded read got. Every other wall path raises `TimeoutExpired`. | `extensions/agi/bin/workflow.py` `_run_stage_proc` wall branch (1923-1944 at 8abfaf9e9d) |
| 2 | rows `F7` (exited stage, orphan holds the pipe -> own rc, unit stopped, nothing alive), `F8` (real wall timeout, orphan SURVIVES the stop -> `TimeoutExpired`, no 'memory'/'timed out after' line), `F9` (prlimit fallback -> no stop attempted, the unit is cleared not left failing) | `test_workflow_stage_scope.py` |
| 3 | the fake scope stop (the `stop_body` built in `_held_pipe_stage`) WAITS for the pids file before killing, so no row races the budget | `_held_pipe_stage` |
| 4 | `_stops` WRAPS the `subprocess.run` that is current when the test starts (the conftest autouse guard) and runs `_TRUE_RUN` (the conftest import-fence wrapper, not the stdlib original) ONLY for a stop proven inside the tmp fake dir; `F10` proves a real-shaped `systemctl --user stop` from this file is still answered rc 1 by the guard (sentinel never written, one stderr line) | `_stops`, `test_F10` |

## How the rows were checked to fail pre-fix

The fixed `workflow.py` was copied to the session scratch dir, the wall branch
was reverted in place to the 96a7dd7173 shape (`if proc.poll() is not None`
AFTER the stop + kill), the suite was run, and the file restored.

| bytes | result |
|---|---|
| pre-fix (`poll()` read after the kill) | `2 failed, 8 passed` -- `FAILED test_F7_...` and `FAILED test_F8_...` |
| fixed | `10 passed` |

F7 fails pre-fix because the scope-killing fake closes the pipe, so the old code
raised `TimeoutExpired` on a stage that had already returned rc 7. F8 fails
pre-fix because the old code answered a still-running wall kill with a bare
`CompletedProcess(rc=-9)`. F9 and F10 pass on BOTH sets by construction (they
are coverage rows for the prlimit branch and the guard chain, not fix-provers) --
stated here rather than claimed as evidence.

## Neighbourhood

```
python3 -m pytest extensions/agi/tests/test_workflow_stage_scope.py \
  extensions/agi/tests/test_workflow_stage_seam_cfg.py \
  extensions/agi/tests/test_launch_memory_cap.py \
  extensions/agi/tests/test_workflow.py \
  extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/pt7
216 passed, 8 skipped in 180.84s (0:03:00)
```

## Production lines

`git diff --numstat 0714583894 8abfaf9e9d -- extensions/agi/bin/` (the SHIPPED range, re-stamped after the director finish 912b4e2b8d)
-> `18  24  extensions/agi/bin/workflow.py` (net -6). Cumulative over 5038f6e817 (workflow.py + mem_cap.py): 84+5 added / 35+2 removed = NET +52 (cap +58) -- the `production_lines` cell.
The kid commit alone was 18 added / 7 removed (net +11) before the director's trim; 10 of its 18 added
lines were the comment stating the read-once rule the directive asked for. The shipped range is net -6,
so item 1 is line-neutral.

## NOT DONE (left for the parent)

- **Item 5** DONE by the director (912b4e2b8d): `merge-up-review.json` line 4 is byte-identical to 5038f6e817 (`diff <(git show 5038f6e817:<file> | sed -n 4p) <(git show b9576d2d4:<file> | sed -n 4p)` = no output, re-run by director-general-3 at harvest of mur-de-base-dg3-69-2).
- **Item 6** (node honesty edits on this hypothesis and on
  `experiment:a00-d41529a1-5fe419`) -- not touched here; another node's text.

## Findings rows for goal:g7.33.19 (not this round's edits)

1. `test_workflow_stage_scope.py` WAS **291 lines against the round's 260 cap** at the kid commit (shipped 260 after 912b4e2b8d; 260 with F11 after DG3.69b)
   (+31). The overage buys four rows (F7/F8/F9/F10), three helpers
   (a waiting fake stop body, `_orphan_dead`, `_reaped` -- `_reaped` replaced in DG3.69b by the autouse `_no_process_left`) and the `_stage` call helper that
   item 4's restructure forced. A cap of 300 covers this round's items 2-4; the
   director sets it, not this kid.
2. The `_stops` spy cannot both keep the guard on the chain AND have the guard's
   own rc 1 mean "the tmp fake ran": the guard answers rc 1 to every
   `systemctl stop`. The file therefore wraps the guard, runs the fake ITSELF for
   a stop PROVEN inside the tmp dir, and leaves the guard in charge of
   everything else (`F10`). That liberty is one `shutil.which` assert away from
   touching a real unit -- if the guard ever grows a bypass flag, this file must
   follow it.
3. The wall branch has TWO ways to leave after the kill (a bounded read that came
   back, one that timed out on a held pipe); the original code handled only the
   second. Any future edit here must keep both, or a scope-killing stop will
   start reporting `timed out` for a stage that finished.

## Agent Notes
item 1 fixed (already_done read once BEFORE stop+kill; both post-kill exits handled) + items 2-4 rows F7-F10; F7/F8 fail on pre-fix bytes (2 failed, 8 passed), all 10 pass fixed; neighbourhood 216 passed 8 skipped; production net +11; test file 291 vs 260 cap = rebrief_request

DH.DG3.66 finish (director-general-3, commit 912b4e2b8d): test_workflow_stage_scope.py trimmed to 260 lines with F1-F10 kept, so the rebrief_request above is moot; production NET +52 over 5038f6e817 (cap +58; the read_back branch folded, comments trimmed); merge-up-review.json line 4 restored byte-identical (item 5). F7 and F8 fail on 96a7dd7173 (2 failed, 8 passed); F9 PASSES there because the prlimit no-stop guard pre-dated it -- it is a regression row, shown to fail when that guard line is removed. F3 no-systemctl case is answered rc 1 by the conftest guard, not an OSError.

DG3.69b (h60c residues, commit a21c4213a1, no production change): F11 pins the legacy run seam (subprocess.run injected only -> anonymous wrap, the launch only, no stop); an autouse _no_process_left asserts no process a row started (tagged in the stage env) outlives ANY row, and fails on the old F1 (its sleep 30 is now killed by the fake scope stop); F7[kill -9 $$] pins the OOM edge. MEASURED on fakes (the old _run_stage_proc swapped in from 96a7dd7173): a stage SIGKILLed while an orphan holds its pipe now returns rc -9 -> is_cap_death -> memory-cap, because poll() is read before the stop; 96a7dd7173 raised TimeoutExpired -> timed out (the misnaming), so the current code fixes it and the reviewer warning (already_done False) does not hold. NOT measured (real systemd off-limits): whether a real OOM kill also kills the orphan; with the default OOMPolicy=stop the scope stops, the pipe closes and both versions return rc -9 before the wall.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DG3.69c director prose close of mur-de-base-dg3-69-2 h60d (accept_with_residue, verify agrees): rebrief_answer cell added (the request was moot at 912b4e2b8d, 260/260); NOT DONE item 5 marked done with the re-run diff; the Production lines paragraph re-joined (orphaned clause). Notes demoted: verify refuted D2-D6; MISS3 (guard prefix match) is a latent hazard with no failing input today.
<!-- THOUGHT:END -->
