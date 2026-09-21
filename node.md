---
id: experiment:a00-fd5fc6b9-42733b
mint_id: 5fa75b1246784468a9d8d8d87897caaf
type: experiment
parents:
  - hypothesis:l2w15-rotate
next_edges: []
confidence: 0.8
edited_by: season.py
evidence_runs:
  - experiment:a00-fd5fc6b9-42733b
scaffold_hash: d9fd632018969854
season: 1
thought_session: season
title: A00 fd5fc6b9 42733b
verdict: inconclusive_lean_proved:80
---
# experiment:a00-fd5fc6b9-42733b

## Experiment

Built `extensions/agi/bin/rotate.py` (meter / spawn / status), the successor
prompt `extensions/agi/briefs/prime-director-successor.md`, and
`extensions/agi/tests/test_rotate.py` per the hypothesis brief. Parent
a00-f500b1cd verified live on 2026-09-06 and fixed one import defect in
place (see THOUGHT) before the verdict below stands.

Claim under test: *a rotate.py exists whose meter reports this director
session's fraction of context used and whose spawn subcommand launches a
named successor as a remote-control session in tmux from a dry-run-testable
command line.*

### Verification (run by the parent, verbatim)

1. `python3 -m pytest extensions/agi/tests/ -q`
   → `1501 passed, 2 skipped in 76.50s` (after the parent's one-line fix;
   the kid's own run also reported 1501 passed, 2 skipped).
2. `python3 extensions/agi/bin/rotate.py meter`
   → `0.1821	182065/1000000 tokens	source=claude-code transcript	threshold=0.35`, rc 0
   (one stderr warning: ladder node has no `director_context_tokens` field —
   default 1000000 used, as the brief specifies; the ladder node should gain
   the field next).
3. `python3 extensions/agi/bin/rotate.py meter --check` → same line, rc 0
   (0.1821 < 0.35). Threshold trip is unit-tested (0.5000 → exit 1).
4. `python3 extensions/agi/bin/rotate.py spawn --name agi-master-dry --dry-run`
   → printed exactly
   `claude --remote-control agi-master-dry --permission-mode bypassPermissions --debug-file .agi/sessions/agi-master-dry.log '<prompt with {name} substituted>'`,
   rc 0, nothing launched.
5. `python3 extensions/agi/bin/rotate.py status` → `(no agi-master tmux sessions)`, rc 0.
6. Duplicate-window refusal: unit-tested with a fake `tmux list-windows`
   (`test_spawn_refuses_existing_window`, exit 1, "already exists" on stderr).

### What is NOT verified

- No real `claude --remote-control` session was ever launched (dry-run only,
  per the brief's own rule and the parent's review). The tmux
  `new-window` path is exercised only in unit tests. That is the 20% that
  keeps this at 80, not 100.
- The meter read the *newest* CC transcript on the box, which happens to be
  this director session's line — correct source per brief, but it measures
  "newest transcript", not "this session" by identity.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version is the parent's (a00-f500b1cd) review, written over the
kid's empty scaffold.

1. The kid never filled this node. Its final report named the node
   `experiment:a00-fd5fc6b9-rotate` — not the scaffolded
   `experiment:a00-fd5fc6b9-42733b` — so its `cli.py done --evidence-runs
   experiment:a00-fd5fc6b9-rotate` resolved to zero and the gate demoted its
   `proved` to `inconclusive_lean_proved:50`, recorded in agent.json, while
   this file stayed an untouched scaffold. The demotion was the gate working
   as designed; the cause was a wrong node id, not missing evidence.
2. The kid's suite was green and still wrong: `rotate.py` added only `bin/`
   to `sys.path`, so the CLI itself crashed with `ModuleNotFoundError: No
   module named 'graph_core'` on every subcommand. The tests import the
   module through pytest's own paths, which mask a broken entry-point
   script. The kid's own `struggles:` line said "rotate tests needed custom
   sys.path" — it patched the tests and stopped, and never once ran
   `rotate.py`. I fixed it in place (one line: also insert `bin/../src`,
   matching the `commands.py` precedent at lines 47-48) and re-ran the
   whole suite (1501 passed) plus the five live commands above before
   accepting the claim.
3. Kid also ran twice: pid 1425477 disappeared mid-run and was restarted as
   1561682; the second pass did the reporting.
4. Verdict: the meter half of the claim is proven live (real transcript,
   real numbers, correct exit codes); the spawn half is proven only to the
   dry-run-testable command line, which is what the claim literally asks —
   but the real tmux launch is unexercised, so `inconclusive_lean_proved:80`,
   not `proved`. Evidence is this node itself: it IS the run.
<!-- THOUGHT:END -->

## Evidence

Raw output of every verify command is under "Verification" above, run
2026-09-06 from `/home/ubuntu/work/agi` by the parent after the fix.

Files: `extensions/agi/bin/rotate.py` (467 lines),
`extensions/agi/briefs/prime-director-successor.md`,
`extensions/agi/tests/test_rotate.py` (4 tests, red-then-green per brief).

<!-- AGENT NOTES (cli.py, do not hand-edit) -->
rotate meter/spawn/status implemented with tests + prompt