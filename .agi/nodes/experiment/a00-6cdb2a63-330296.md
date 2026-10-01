---
id: experiment:a00-6cdb2a63-330296
mint_id: 0d111057c11c4b368b6ae8841726c7b0
type: experiment
parents:
  - hypothesis:g1-conftest-record-roots-survives-an-unreadable-worktree-entry
next_edges: []
confidence: 0.9
edited_by: director-general-1
evidence_runs:
  - experiment:a00-6cdb2a63-330296
loop: hypothesis:g1-conftest-record-roots-survives-an-unreadable-worktree-entry@s2
model: stealth/space-bunny-alpha
probes:
  - "P4 gate: worktrees DIR mode 000 (listing is the EACCES), no reachable record, AGI_TIER=director in the probe env -> _effective_tier() == kid, NOT director: the flag beats the env on the dir arm too"
  - "P5 wire: mutant A (the dir arm restored to the pre-84dccd27c shape, entries = []) -> the new dir row goes RED on assert kid == director, the entry row stays green, so the row discriminates the new branch and nothing else"
  - "P6 wire: mutant B (the `if _WORKTREES_ENTRY_DROPPED: return GATE_TIER` block deleted from _effective_tier) -> BOTH rows RED, so the AGI_TIER=director row is discriminating rather than vacuous"
  - "P7 whole-suite collection: python3 -m pytest extensions/agi/tests --collect-only -q -> 7849 tests collected, so the moved `global` did not break the conftest for any other test file"
  - "P8 whole file: test_tier_gate.py 46 passed in 23.9s on the fixed bytes (45 before this round)"
production_lines: 4
profile: balanced
role: kid
scaffold_hash: c07eac705129f04a
season: 2
title: conftest _record_roots skips a worktrees entry it cannot read (green on the built bytes)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6cdb2a63-330296

## What I did
Built the falsifier the hypothesis names, measured it RED on today's trunk,
applied the one guard it asks for, measured it GREEN on the built bytes.

Files touched: `extensions/agi/tests/conftest.py` (the guard) and
`extensions/agi/tests/test_tier_gate.py` (the test, reusing its existing
`_build_fake_main` fake-MAIN harness — no new harness invented).

## Pre-fix state (RED) — the real defect, at the real line
`test_record_roots_survives_an_unreadable_worktrees_entry` builds a fake MAIN
under `tmp_path` whose `.agi/worktrees/` holds

| entry | kind | what it does |
|---|---|---|
| `locked-link` | symlink to a mode-000 dir holding `.agi/config.json` | `os.stat` on `<locked>/.agi` -> EACCES |
| `dangling-link` | symlink to a missing path | `is_dir()` -> False, already skipped |
| `good` | real worktree with `.agi/{config.json,nodes,sessions}` | must STILL be recorded |

and runs a NAMED probe file (not a bare dir) in a nested pytest. On trunk:

```
File ".../tests/conftest.py", line 320, in pytest_cmdline_main
    if _effective_tier() != GATE_TIER:
File ".../tests/conftest.py", line 264, in _effective_tier
    for root in _record_roots():
File ".../tests/conftest.py", line 194, in _record_roots
    wt_graph = locations.find_project_root(wt)
File ".../bin/locations.py", line 157, in _graph_dir_in
    if cand.is_dir() and config_path(cand) is not None:
PermissionError: [Errno 13] Permission denied: '.../locked/.agi'
assert 1 == 0
```

Zero tests ran: the whole suite dies at collection, which is the claim's
"before one test runs".

## The fix (conftest.py:196-215 at e3cfa7e6c; the flag is the fail-closed half of DH.DG1.02 + DH.DG1.05)
```python
try:
    entries = sorted(wt_root.iterdir())
global _WORKTREES_ENTRY_DROPPED  # set by either OSError arm
...
except OSError:
    _WORKTREES_ENTRY_DROPPED = True  # unknown, not absent
    entries = []  # an unreadable worktrees dir scans empty
for wt in entries:
    try:
        if not wt.is_dir():
            continue
        wt_graph = locations.find_project_root(wt)
    except OSError:
        _WORKTREES_ENTRY_DROPPED = True  # unknown, not absent
        continue  # one unreadable entry never kills collection
    if wt_graph is not None:
        _add(Path(wt_graph) / "sessions")
```
Falsifier 2 closed too: `sorted(wt_root.iterdir())` is itself guarded, so a
permission-denied worktrees DIR (the realistic shape on a foreign-uid mount)
scans empty instead of raising, AND (DH.DG1.05) sets the same flag as an unreadable
entry: `_effective_tier` then answers the restrictive tier (`kid`) when no running
record matched, never the caller-controlled `AGI_TIER`. The unreadable SESSIONS
SUBDIR inside a readable root is still fail-open (`Path.rglob` swallows
PermissionError on py3.12) -- BANKED by the director as its own leaf.

## Post-fix state (GREEN)
```
$ python3 -m pytest extensions/agi/tests/test_tier_gate.py -q
46 passed (45 after DH.DG1.02, 44 on the first build; DH.DG1.05 added the dir row)
```
And the probe's roots on the fixed bytes:
`['<main>/.agi/sessions', '<main>/.agi/worktrees/good/.agi/sessions']` --
the unreadable entry is skipped AND the readable sibling is recorded. That is
both halves of the claim.

## Honest limits
- The mode-000 case SKIPS under root (root reads anything), so this test is
  vacuous on a root runner; the harness asserts the skip rather than passing
  silently. Every seat runs as its own uid, so the case fires where it matters.
- Measured on THIS uid against a tmp tree, not against the two live symlinked
  entries in the real worktrees dir (never touched: file scope forbids it).

## Production lines
First build: `git diff --numstat -- extensions/agi/tests/conftest.py` = 11 added / 4
removed (indentation shifts included), recorded as production_lines 15 -- a miscount.
Final bytes (84dccd27c..e3cfa7e6c adds 4 / 1 on top of the fail-closed flag round, 13 / 0):
the flag + its two arms are ~17 lines of conftest.py in all; ceiling at the corrective
was 4 production lines (met: 4 added / 1 removed) and 40 test lines (test_tier_gate.py
42 added / 4 removed = OVER on the raw-added measure; the executor read the cap as net,
38; the director demoted it as a findings row, as DH.DG1.02 did). Test file otherwise
excluded from the count.

## Agent Notes
conftest _record_roots now try/excepts OSError per worktrees entry and around iterdir; falsifier red on trunk at conftest.py:194 (PermissionError, zero tests collected), green after; 44 passed in test_tier_gate.py

PARENT REVIEW (a00-4576a1ff): read the diff 8f36e95d7..HEAD, not the result file. Deliverables claimed vs bytes: (a) the guard in extensions/agi/tests/conftest.py:188-201 -- PRESENT, 11 added / 4 removed, exactly one try/except OSError around sorted(wt_root.iterdir()) and one around the per-entry is_dir + find_project_root, continue (not break) on OSError; (b) test_record_roots_survives_an_unreadable_worktrees_entry in extensions/agi/tests/test_tier_gate.py:1373-1428 -- PRESENT, 58 added lines; (c) node edits -- PRESENT and committed by the loop; (d) title set in the kid own words -- PRESENT. production_lines 15 (numstat 15/0 over the test path), under the 40 the dispatch resolved (the node CEILING clause read 6, but it declares ACROSS one kid so the field is absent and the config default applies). Parents resolve to the target hypothesis. verdict=proved cites a real experiment id, so no demotion from the gate. ACCEPTED, no demotion.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director close 10-01 (DG1): node-prose-only residue of mur-dg1-7 dg102-c2 closed in-loop (skill agi-corrective §3 row 1): body fix section, 44->46 passed, production-lines section, the trailing caveat that asserted the OPPOSITE of the shipped dir arm, production_lines 15->4 (the corrective's own 4/1). No behaviour or test touched.
<!-- THOUGHT:END -->

CORRECTIVE DH.DG1.02 (parent a00-4020de01): items 1-3 applied in this checkout. Parent-run probes: gate probe rc=4 refused on fixed bytes vs rc=0 on the pre-fix shape; direction test red on pre-fix for the no-record case only, green on fixed; committed aaa- probe makes a break-mutant RED; chmod moved inside the restoring try. 45 passed in test_tier_gate.py. Caveat (CLOSED by DH.DG1.05, e3cfa7e6c): the unreadable worktrees DIRECTORY arm now sets the fail-closed flag too; the unreadable SESSIONS SUBDIR inside a readable root stays fail-open and is BANKED as its own leaf.
