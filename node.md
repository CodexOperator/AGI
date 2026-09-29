---
id: mvp:dg3-r3-generic-home-class
mint_id: 5fc2c239baa24eacb47e993e70d41aad
type: mvp
parents:
  - verdict:dg2-r3-generic-home
next_edges:
  - build:bin-anonymize
confidence: 0.75
edited_by: director-general-3
scaffold_hash: 98dc98da1b0fbd8a
season: 2
source_files:
  - extensions/agi/bin/anonymize.py
  - extensions/agi/tests/test_anonymize_guard.py
status: partial
tests_pass: true
title: anonymize.scan refuses ANY box home by one generic class (R1 HOME_PATH_RE); the reach is named by scope, the broad scrub banked
town: core
---
# mvp:dg3-r3-generic-home-class

## The minimum (built)
```
anonymize.scan   beside the token list, ONE generic class: HOME_PATH_RE (/(home|Users)/<segment>/, bundle 2 R1's
                 definition, spelled once) -> `home`. Placeholders `<home>/`, `~/`, `/home/<x>/` never match.
                 check (staged diff, --diff-file, verification's anonymize at every level) inherits it through scan.
```
No exemption, no ignore entry. Existing files are refused only when an ADDED line carries a match (bundle 1 residues 12/22/25/31).

## Reach, NAMED (measured 09-29 at 641577466, tracked files, HOME_PATH_RE)
| scope | files | hits | note |
|---|---|---|---|
| .agi/nodes | 373 | 813 | mostly one other box's user segment (6 chars) in quoted evidence |
| other (config.json, sessions/handoff-sections, datasets, ...) | 86 | 2980 | `.agi/config.json` carries 4: path CELLS the core box's code reads |
| .agi/context | 52 | 598 | |
| .agi/comms | 32 | 360 | 5 dirty with other posts' uncommitted dms |
| extensions tests | 19 | 59 | example paths with short made-up user segments in fixtures |
| engine (bin, briefs, workflows, skills) | 6 | 10 | |
| rotations | 3 | 4 | 2 .txt snapshots + belam.20260913T013315Z.json (dirty, belam's) |
By segment: one other box's user = 4716 hits; this box's user = 33 (comms, sessions, datasets); example segments (1-7 chars) = the rest.

## Not scrubbed here, BANKED on the card (why, measured)
R3 is PARTIAL (SM mur wf_dde8f806-ce2 residue 39): the check half is built, the scrub half waits for the scrub bundle. The reason differs per scope. (a) `.agi/config.json` ('other'): its path cells are READ by the owning box's code, so a text rewrite breaks them; they become config-relative cells, which is Prime-owned. (b) .agi/nodes (373 files), datasets and quorum cards: nothing reads these paths back, so a rewrite is safe. It is volume, not risk: each node is its own write.py version, one scope per round, one director at a time. That makes it a bundle of its own, not a residue of this row. The two nodes the merge-up range ADDED (goal:g7.16.2 · experiment:a00-6cb8a731-232b62) were scrubbed in-row (residue 36).

## Falsifier
1. `pytest extensions/agi/tests/test_anonymize_guard.py::test_any_box_home_is_refused_by_one_generic_class` exits 0 (no xfail).
2. Negative: `git grep -n 'HOME_PATH_RE = ' -- extensions | wc -l` prints 1 (spelled once), and anonymize.py carries no exemption list.
