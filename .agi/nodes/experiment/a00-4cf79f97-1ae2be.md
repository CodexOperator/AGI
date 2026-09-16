---
id: experiment:a00-4cf79f97-1ae2be
mint_id: a63fdea9a0544a598d8caa98c31b5a50
type: experiment
parents:
  - hypothesis:l4-a-kid-checkpoints-its-projected-lines-and-pauses-above-2x-for-a-parent-re-brief
next_edges: []
confidence: 0.85
edited_by: a00-7f9e013a
evidence_runs:
  - experiment:a00-4cf79f97-1ae2be
line_ceiling: 90
loop: hypothesis:l4-a-kid-checkpoints-its-projected-lines-and-pauses-above-2x-for-a-parent-re-brief@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 4, "class": "wire", "cmd": "cli._kid_measured_lines(.agi, real kid agent ids) and cli._parent_harvest_body over the real commits", "expected": "the real done-commits measure (a00-bcb2955a=64, a00-6df6d202=70, a00-4cf79f97=86) and the real harvest dm names the real over-2x kid", "observed": "PASS wire-measures-a-real-kid-commit (70); PASS wire-no-anchor-returns-none; PASS wire-real-over-2x-rebrief-named (rebrief=[experiment:a00-4cf79f97-1ae2be 86/40])", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "cli._parent_harvest_body with a kid node holding NO record fields at all, whose real done-commit measures 86 > 2*40", "expected": "the previously-failing falsifier state is now named: a kid past 2x with no record and no re-brief entry must NOT harvest clean", "observed": "PASS gate-no-record-but-measured-is-named -> overage=[experiment:k-norec 86/40 no-rebrief]", "result": "pass"}
  - {"conjunct": 4, "class": "auth", "cmd": "cli._parent_harvest_body with the same over-budget kid whose spawned_by_agent is a DIFFERENT parent", "expected": "no overage is named for a kid this parent did not spawn", "observed": "PASS auth-foreign-kid-not-named (kids=[])", "result": "pass"}
production_lines: 86
profile: balanced
rebrief_answer: proceed with ceiling 90 -- parent review accepted the node at proved; the 86 production lines are within the raised ceiling and no trim is required
rebrief_request: "cli.py 86 lines (2.15x of 40): conjunct (4) build complete, falsifier test green, nothing remains -- need a 90-line ceiling blessed or a trim directive"
role: kid
scaffold_hash: af0d49ad26e2b335
season: 2
title: A00 4cf79f97 1ae2be
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4cf79f97-1ae2be

## Conjunct owned: (4) — the harvest must measure the kid, not trust its self-report

The last kid (`experiment:a00-6df6d202-b8c020`) made the harvest READ each
kid's node frontmatter (`production_lines` / `line_ceiling`) and name
`overage=[id N/C no-rebrief]`. It works when the kid records; it FAILS OPEN
when the kid records nothing — no record, no defect, the over-budget kid
harvests clean. That is the hypothesis's own stated falsifier, and it is the
shape of the original SM.44 defect (3.4x, caught only by the parent reading
the diff).

## Pre-fix state (measured, not assumed)

Scratch probe `.agi/sessions/iter-SM.45/a00-4cf79f97/prefix_probe.py` on ONE
temp fixture — a bare kid node (no `production_lines`) plus a real git repo
whose newest commit is `a00-kid-1 done:` adding 90 production lines:

```
PRE-FIX  note for bare kid: [] (nothing -- kid harvests clean)
POST-FIX note for bare kid: ['overage=[experiment:k-bare 90/40 no-rebrief]']
measured lines: 90
no-anchor kid : None
```

The pre-fix predicate is empty for a bare node because `lines is None` ->
`continue`; the falsifier reproduces. Post-fix it names the defect.

## What was built (`extensions/agi/bin/cli.py`)

1. `_parent_harvest_body` now passes the kid RECORDS through (the anchor —
the record carries `id`, the `done`-commit key) instead of only node ids:
`notes = _kid_budget_notes(root, kids)`.
2. `_kid_measured_lines(root, agent_id)` — the measurement. Resolves
`main = locations.git_common_root(root) or root` the same way `_branch_tip`
does, reads `git log --all --format=%H --grep='^<id> done:'` (newest first)
and sums ADDED lines of production paths in that commit
(`git show --numstat --format=`). Production = a source suffix, never a
`tests/` path, never a node/markdown file. Read-only; every subprocess call
is wrapped for `TimeoutExpired`/`OSError` exactly like `_branch_tip`, and no
anchor resolving returns `None` rather than a fabricated 0.
3. `_kid_line_ceiling(root, fm)` — the node's own `line_ceiling` when present
and > 0, else `spawn_budget.production_line_ceiling(cfg)` read from the
graph's `config.json`. The number stays in ONE place (spawn_budget); no
second hardcoded 40.
4. Naming rules unchanged: measured (or, when no anchor resolved, recorded)
lines > 2 * ceiling with no `rebrief_request` -> `overage=[id N/C no-rebrief]`;
a `rebrief_request` -> `rebrief=[id N/C]`; at or under 2x -> nothing.

Judgement call, recorded: **the measured value wins over a contradicting
record** (record 30, git 200 -> `overage=[... 200/40 no-rebrief]`). Reason: the
record is the monitored agent's own claim; if the claim could override the
measurement, a stale or understated self-report would launder an over-budget
kid — exactly the failure this conjunct exists to close. Both directions of
the contradiction are tested.

## Tests (`extensions/agi/tests/test_kid_reports_to_parent.py`)

New: `test_harvest_measures_a_kid_that_records_nothing` (THE FALSIFIER: bare
kid, real git `done` commit of 90 lines -> `overage=[experiment:k-bare
90/40 no-rebrief]`); `test_measured_lines_beat_a_contradicting_record`
(record 30, git 200 -> measured wins); `test_measured_overage_still_honours_a
_rebrief` (measured 120 + `rebrief_request` -> `rebrief=`, no defect).
Updated, not deleted: `test_harvest_is_unchanged_under_2x_or_without_a
_resolvable_commit` — the old no-record assertion "adds nothing" is only true
when no commit resolves; it now says so, and the with-an-over-budget-commit
case is the new falsifier test above.

The git anchor is a REAL temp repo (`_git_done_commit`), so the MEASUREMENT
path is exercised, not the record path.

```
python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py -q
14 passed in 0.82s

python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py \
    extensions/agi/tests/test_cli.py extensions/agi/tests/test_brief.py -q
188 passed, 27 warnings in 6.95s
```

## Production lines vs the ceiling

One read-only `git diff --numstat` over the production path (never staged,
never committed):

```
86	21	extensions/agi/bin/cli.py
66	4	extensions/agi/tests/test_kid_reports_to_parent.py
```

**86 production lines against a 40-line ceiling = 2.15x**, above the 2x
checkpoint. Test-file lines do not count. A `rebrief_request` is recorded
below rather than an undeclared overage: the conjunct is built and green and
nothing remains — what the parent must decide is the ceiling, not the work.

## Caveat carried forward (not fixed — outside this conjunct's spec)

The production filter is the one the parent specified (source suffix, no
`tests/` segment, no markdown). A kid probe script written in its OWN session
dir (`.agi/sessions/.../probe.py`, which the brief mandates for probes) is a
non-test `.py` and would be counted as production if the `done` commit swept
it in. Excluding a `.agi/` path segment would close that false-positive
source; it is a one-line change but a deviation from the specified filter, so
it is reported rather than improvised.

## Evidence

- cli.py: `_kid_budget_notes` (records in), `_kid_measured_lines`,
  `_kid_line_ceiling`.
- Scratch probe: `.agi/sessions/iter-SM.45/a00-4cf79f97/prefix_probe.py`.
- 14/14 in the changed file; 188 passing across the three covering files.

## Agent Notes
conjunct (4) closed: harvest MEASURES each kid's production lines from its own '<id> done:' commit (git log --grep + show --numstat, read-only, _branch_tip-shaped guards) instead of trusting the node record; measured beats record on contradiction; node line_ceiling else spawn_budget default. 14/14 in test_kid_reports_to_parent.py (falsifier: bare kid with 90-line done commit -> overage=[... 90/40 no-rebrief]), 188 passed across the three covering files. 86 cli.py production lines = 2.15x of 40 -> rebrief_request filed on the node (work complete, ceiling decision is the parent's).

PARENT REVIEW (a00-7f9e013a, SM.45): ACCEPTED at proved. I read the bytes, not the result file: _kid_measured_lines resolves the kid done-commit via git log --all --grep and sums added PRODUCTION lines from git show --numstat, excluding tests and non-source suffixes; _kid_budget_notes now takes the kid RECORDS so the agent id is the measurement anchor, and the ceiling falls back to spawn_budget.production_line_ceiling, not a second hardcoded 40. My three probes hold against the REAL repo commits: measured 64/70/86 for the three kids, the real harvest names rebrief=[experiment:a00-4cf79f97-1ae2be 86/40], and -- the falsifier that demoted the previous node -- a kid node with NO record fields whose real commit measures 86 now harvests as overage=[experiment:k-norec 86/40 no-rebrief]. The fail-open is closed. Caveats: (a) the measurement is the scope of the done-commit, so a shared-tree auto-commit that sweeps another agent file would over-count; (b) conjunct 2 remains a brief instruction with no runtime enforcement -- a model that ignores it is only caught by this harvest check after the fact; (c) conjunct 3 is still unbuilt.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-7f9e013a, SM.45). The previous node failed open: harvest trusted the monitored agent self-report, so a kid that recorded nothing was never over budget and harvested clean -- the target hypothesis stated falsifier. This kid moves the measurement to the parent side: git log --all --grep '^<agent_id> done:' finds the kid own commit and git show --numstat sums its added production lines, with the node line_ceiling (or the config default) as the ceiling. The record is now only a fallback when no commit anchor resolves. I verified the mechanism on the REAL commits rather than a stub (64/70/86 measured for the three kids), confirmed the real harvest names the real over-2x kid, and reproduced the previously-failing falsifier state -- a no-record node with an 86-line commit -- now yielding overage=[experiment:k-norec 86/40 no-rebrief]. Verdict kept at proved because the conjunct as written is now satisfied independent of self-report. Two caveats survive on purpose: the count is the done-commit scope (a sweep would over-count) and conjunct 2 has no runtime enforcement, both recorded for the harvest rather than papered over.
<!-- THOUGHT:END -->
