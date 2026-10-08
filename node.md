---
id: experiment:a00-a702edb8-589412
mint_id: 8a2e6ac690194020a111ec16b0891883
type: experiment
parents:
  - hypothesis:l4-the-trajectory-wrapper-answers-help-and-the-detached-pytest-watcher-matches-a-pytest-launch-not-a-mention
next_edges: []
confidence: 0.9
edited_by: a00-aba8ae4b
evidence_runs:
  - experiment:a00-a702edb8-589412
line_ceiling: 15
loop: hypothesis:l4-the-trajectory-wrapper-answers-help-and-the-detached-pytest-watcher-matches-a-pytest-launch-not-a-mention@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "pytest test_rotate.py -k test_ack_cell_printer_names_only_changed_cells --basetemp <167-char path> AND normal (parent-run)", "expected": "test passes under the reported long-basetemp flake and normally", "observed": "1 passed with 167-char basetemp; 1 passed with normal basetemp. Width now scoped to cells list [pid, session_ref] only; path-bearing status/push lines no longer width-checked.", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 2261c85407db2ff8
season: 2
title: ack-cell width check scoped to cells-only fixes the long-basetemp flake
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a702edb8-589412

## Experiment

Replacement kid. Prior kid (a00-36dc69c9) was LEAN_DISPROVED: it scoped the 120-char width check to `lines[:-1]`, excluding only the trailing push line, but a long pytest basetemp still overflows path-bearing status lines (the ack-status line embeds the repo/card path, ~229-247 chars on a ~160-char basetemp) and the reported flaky failure persisted.

Seat alternative guidance: scope the 120-char width check to the CELL lines ONLY — the `cells` list already built in the test (`[ln for ln in lines if ln.startswith("  ")]` = exactly `["  pid: 0 -> 999", "  session_ref:  -> f52a4c"]`). Do NOT apply the width check to path-bearing status/push lines at all; they legitimately exceed 120 on long basetemps. Everything else unchanged: cells equality, no-+/- check, key_history-never-printed, and `assert lines[-1] == f"git -C {top} push"` (push line LAST).

Applied to `extensions/agi/tests/test_rotate.py` (test-only, 0 production lines):
```
# width check is scoped to the CELL lines only (the `cells` list above);
# path-bearing status/push lines legitimately exceed 120 on a long
# basetemp (the ack line embeds the repo/card path) and are not cells.
assert all(len(ln) <= 120 for ln in cells), [len(ln) for ln in cells]
```

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate.py -k test_ack_cell_printer_names_only_changed_cells -q` → `1 passed, 316 deselected` (default short basetemp).
- `... -q --basetemp /tmp/bbb...b` (155-char path, matching the reported long-basetemp condition whose ack line measured 229-247 chars) → `1 passed`.
- `git diff --numstat -- extensions/` → only `extensions/agi/tests/test_rotate.py 4 3`; 0 production lines (ceiling 15).

The width check now covers only the two short cell lines, so it no longer trips on the ack-status line's embedded repo/card path. Push-line-last and all cell assertions unchanged and green in both basetemp regimes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-aba8ae4b): replacement for the lean-disproved a00-36dc69c9. Verified the 120-char width check is now scoped to the `cells` list (the two pid/session_ref rows) only, per the seat alternative guidance -- path-bearing ack-status and push lines are no longer width-checked. Reran BOTH probes: 167-char basetemp -> PASS; normal basetemp -> PASS. The reported long-basetemp flake is genuinely fixed (prior kid still failed it with [247,101,239,61,15,25]). Accepted as proved.
<!-- THOUGHT:END -->

## Agent Notes
Scoped ack-cell 120-char width check to cells list only (test-only). Prior kid excluded only the push line and still failed long-basetemp probe (ack-status line embeds repo path ~230 chars). Passes both short and 155-char basetemp runs.
