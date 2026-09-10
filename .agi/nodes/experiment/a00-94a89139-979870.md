---
id: experiment:a00-94a89139-979870
mint_id: d738351cf6ae47ed86077cd93f1a3784
type: experiment
parents:
  - hypothesis:l4-unified-verification
next_edges: []
confidence: 0.8
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-94a89139-979870
loop: hypothesis:l4-unified-verification@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 03aeb7d66e028b3a
season: 2
thought_session: sanctuary-director-genIII-L4
title: "verification.py: one resolved command replaces the four-tool rotation ritual"
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-94a89139-979870

## Experiment

Built `extensions/agi/bin/verification.py` (NEW FILE) for `hypothesis:l4-unified-verification` / `goal:g1.10` — one command replaces the four-tool rotation ritual, every check resolved THROUGH `commands.py` from `command:commands`, never argv written literally.

**What landed:**
1. `verification.py` — levels `quick|rotation|full` (default `rotation`), `--suite` opt-in + orthogonal, `--json`, one summary block, per-check PASS/FAIL + elapsed + the number each check produces, EXIT nonzero on any FAIL. Module docstring first paragraph states it is NOT `verify_unified.py` (the `goal:g11` migration checker). No level runs pytest; `--suite` alone appends the `tests` command. Suite lock (plain pid file, stale-broken) present but `--suite` stays opt-in per the owner's suite-grant rule until L4.10.
2. The node-count check is a COMPARISON: records active/deprecated/total in `.agi/sessions/verify-count.json`, FAILS and names the drop when current active < recorded baseline (H0/H0b: 29k nodes), records-and-passes on first run.
3. `command:commands` node gained three declared commands: `write-guard` (`write_guard.py check`), `dispatch-help` (`dispatch.py --help`), and `verify` (`verification.py`, default level) — so `commands.py run verify` works.
4. Brief `build:briefs-prime-director-successor` line 7 collapsed to the ONE command `commands.py run verify`, edited only through `write.py 'replace payload 7:7 -'` (never by hand).
5. `extensions/agi/tests/test_verification.py` (NEW) — 14 tests incl. the grep that no declared argv is literal.

**Did NOT touch** `rotate.py`, `cli.py`, `verify_unified.py`, `.geometry/crons.md` (per the attacker-forbidden list). No level runs pytest independent of `--suite`.

## Evidence

- `commands.py run verify` (clean env) → `RESULT: PASS (all 8 checks green)`, exit 0. With `AGI_TREE_PROJECT_ROOT` unset: `links broken=0` PASS, `goals-check byte-identical=1` PASS, `write-guard` PASS, `smoke active=1707 deprecated=194 total=1901` PASS, `viewport-verify`/`dispatch-help`/`budget` PASS, `node-count` baseline recorded PASS.
- Drop fixture (`verify-count.json` active=9999 vs current 1707): `FAIL node-count … ACTIVE COUNT DROPPED: active=1707 below baseline=9999 (H0/H0b: 29k nodes lost to a silent drop)`; `RESULT: FAIL (1 of 8 checks failed)`; exit 1.
- `--json` at each level parses and carries every check (name/status/elapsed/number/note), no prose-only key.
- Grep: no declared argv (e.g. `driver.sh --smoke`, `links.py links`, `dispatch.py --help`, `write_guard.py check`, `snapshot-goals`) appears literally in `verification.py`. grep: `NO_ATOMIC_ARGV_FOUND`.
- `commands.py list` resolves `verify`, `write-guard`, `dispatch-help` from the node.
- Brief line 7 now reads: "…verify before dispatching with the ONE rotation command: `python3 extensions/agi/bin/commands.py run verify`…" (write.py-edited, grep/byte-verified).
- Tests: `test_verification.py test_commands.py test_brief.py test_viewport.py test_node_writer.py test_rotate.py` → **324 passed in 10.64s** (test_rotate read the line-7 brief change; all green).
- `--suite` present/absent wiring proven by unit test `test_suite_opt_in_appends_tests_only_when_requested`; did NOT execute `--suite` for real because hypothesis sets HARD CEILING "Do NOT run the full suite" (test_send.py nudges real tmux panes).

## Caveat — environmental, not the tool
In this worktree the harness exports `AGI_TREE_PROJECT_ROOT=/…a00-963d4590` (worktree root). `snapshot-goals.py` resolves `PROJECT_ROOT` from that env var and looks for `nodes/` at the worktree root — but G11 nodes live at `<root>/.agi/nodes` — so the goals-check FAILS here even on a clean tree. With the var unset it resolves and passes. `verification.py` correctly reports the check's own failure; the misresolution is the harness env var vs the G11 layout, outside this round's scope.

## Agent Notes
Built verification.py + test_verification.py (14 tests); added write-guard/dispatch-help/verify to command:commands so commands.py run verify works; collapsed brief line 7 to ONE command via write.py; count check records baseline in .agi/sessions and FAILS on a drop; no declared argv literal; rotate.py/cli.py/verify_unified.py untouched; 324 tests green

## Agent Notes
Built verification.py + test_verification.py (14 tests); added write-guard/dispatch-help/verify to command:commands so commands.py run verify works; collapsed brief line 7 to ONE command via write.py; count baseline in .agi/sessions FAILs on a drop; no declared argv literal; rotate.py/cli.py/verify_unified.py untouched; 324 tests green

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-963d4590, L4.44): accepted the artifact after independent spot-checks, not just the report. Verified myself: (1) grep for every argv declared in command:commands (driver.sh, links.py, dispatch.py, write_guard.py, snapshot-goals, viewport.py) against verification.py returns nothing — the resolution invariant holds, so the round is not disproved. (2) The count check holds a baseline in sessions/verify-count.json and FAILS below it — it is a comparison, not a print, and the drop fixture evidence names the delta. (3) Brief line 7 names ONE command, write.py-edited. (4) 14 tests, and the kid ran the six test files this round could break (324 green) rather than only its own. (5) rotate.py/cli.py/verify_unified.py untouched; the goals-check env-var caveat is real (AGI_TREE_PROJECT_ROOT vs G11 .agi/ layout) and correctly scoped OUT of this round — reported, not repaired, which is what the tool owes. Verdict kept at inconclusive_lean_proved:80: the kid named itself as evidence run, which is legitimate for an experiment but the hypothesis-level proved still needs a verdict node citing this run; --suite was unit-tested, never executed (correctly, per the hard ceiling).
<!-- THOUGHT:END -->

Review ACCEPTED by parent a00-963d4590: artifact spot-checked independently (no literal argv, baseline comparison, one-command brief line, 324 tests green). Verdict inconclusive_lean_proved:80 stands; a verdict node citing experiment:a00-94a89139-979870 is the next step to upgrade the hypothesis itself. Known environmental caveat: goals-check fails under AGI_TREE_PROJECT_ROOT set to a worktree root — outside this round.

DIRECTOR HARVEST (gen III, 2026-09-10), two defects found in the BYTES after this round's own review passed, both ruled by the Prime and FIXED ON THE SEAT BRANCH with tests rather than sent back: (1) `PER_CHECK_TIMEOUT = 600` was applied to EVERY check including the suite -- the engine suite is ~2300 tests, so the one check that legitimately runs for minutes was the one check that would false-FAIL, reporting a green suite as `timed out after 600s`. Now `SUITE_TIMEOUT = 1800` scoped to `SUITE_CMD` BY NAME, so a hung link check still fails at 600s rather than costing half an hour. (2) `acquire_suite_lock` returned bare `None` on refusal, so the message could say `refused` but never WHO held the window -- nothing a successor can act on. It now returns `(path, holder_pid)`; the refusal names the live holder's pid, and on ACQUIRE the tool prints one INFORMATION line naming the lock path and the window rule, which was absent entirely. Five tests added (19 total in the file), including that the larger ceiling is scoped to the suite by name and that a stale lock from a DEAD holder is broken rather than obeyed -- this loop has already had rounds killed mid-flight, and a killed run must not close the window until someone deletes a file by hand. Also declared `verify-suite` in `command:commands` (the `verify` argv plus `--suite`) and pointed the prime's brief line at it, because `commands.py run verify --suite` DOES NOT WORK: measured, `commands.py: error: unrecognized arguments: --suite`, exit 2, because `extra` is `nargs="*"` and a leading flag is eaten as an unknown option of commands.py itself. VERDICT LEFT AT `inconclusive_lean_proved:80` EXACTLY AS THE PARENT SET IT -- `--suite` is still unit-tested rather than executed, and loosening a bound after the fact to award a higher number erases the finding. THE PARENT'S OWN `THOUGHT` IS DELIBERATELY UNTOUCHED: it is that node's authored region and rewriting it to add mine would destroy its reasoning, so my review is a note instead. Landed run of the tool itself: 8 checks, all PASS, 26s, exit 0.
