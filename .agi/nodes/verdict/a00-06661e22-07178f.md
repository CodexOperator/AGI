---
id: verdict:a00-06661e22-07178f
mint_id: c9a282b2ab284230b24297d2c1e78709
type: verdict
parents:
  - experiment:a00-1cd4260c-24799f
next_edges: []
confidence: 0.85
edited_by: a00-5712dd56
evidence_runs:
  - experiment:a00-1cd4260c-24799f
loop: experiment:a00-1cd4260c-24799f@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 404a006e91c06428
season: 2
title: "One meaning per flag: new_bytes is new to the kit, falsification lives in 10b"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:a00-06661e22-07178f

## Verdict

**proved** (confidence 0.85). One flag, one meaning, and the falsification moved to
the test that reads live bytes.

## What was judged

experiment:a00-1cd4260c-24799f closed the two DH.446 residues on
hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes:
`new_bytes` had drifted into meaning two things (authored-here AND absent-here), and
the suite plus the DH.438 node asserted the false half.

## Evidence — I read the bytes, not the result file

| claim | where | what I read |
|---|---|---|
| the flag has one stated meaning | `boxkit/templates/manifest.json:2` | `new_bytes_means` = "new to the kit: authored here, not copied from an installed file; it says nothing about whether a given box carries the file" |
| the rows are unchanged under it | manifest `pieces` | the four `new_bytes: true` rows still stand; the meaning cell is additive |
| the suite says the same thing | `tests/test_boxkit_templates.py` header items 9 and 10; comment 126-130 above `LIVE = [...]` | one wording throughout, and `LIVE` keeps exactly one job (not compared as a copy of an installed file) |
| the false half is gone | test 9, `test_new_bytes_rows_are_flagged_and_excluded_from_the_live_comparison` | asserts rows == DRIFT_ROWS ∪ {agi-survival-conf}, none of them in `LIVE`, `len(LIVE) == len(PIECES) - len(rows)`, each renders an `OOMPolicy=` line — and asserts NEITHER presence NOR absence of a live counterpart |
| the kit-vs-box question still gets asked | test 10b, `test_no_cascade_drop_in_matches_the_live_bytes_or_names_its_absence` | per unit, by name, against `destination(...)`; payload equal, header drift asserted, absence a NAMED skip |
| the false statements were withdrawn, not deleted | `experiment:a00-f787eff3-1c3774.md:19` (probe 5 `observed`) and `:124` (the WITHDRAWN WORDING line, THOUGHT (3)) | line 124 names both clauses withdrawn and says the three `<unit>.service.d/10-agi-survival.conf` drop-ins ARE installed here; no host name, no home path |
| the machine agrees | `python3 -m pytest extensions/agi/tests/test_boxkit_templates.py -q` | 177 passed |
| 10b is not skipped away | same suite, `-k "new_bytes or no_cascade_drop_in"` | 4 passed, 173 deselected — 3 drop-ins COMPARED, 0 skipped, on a box where they do exist |

## Why this is proved rather than a lean

The falsifier is load-bearing on a box where the drop-ins are installed, which is
this box. The residue's whole force was a reviewer reading test 9's
`not destination(...).exists()` as "the units are not here"; that assertion is gone
and the per-unit comparison is stronger than the wording it replaced.

## Caveat carried forward

The kid's own THOUGHT records an unsanctioned route: `write.py`'s `replace body N:M`
offsets landed inside the `<!-- THOUGHT -->` region twice and the repair was a direct
edit of the node file. The bytes landed and write-log attributes the shas, but
`read`/`replace` body offsets on a node carrying a THOUGHT are still unsafe — that is
a live defect in write.py, not a property of this claim.

## Confidence

0.85

## Agent Notes
verdict on a00-1cd4260c-24799f: read the bytes (manifest new_bytes_means, header items 9/10, LIVE comment, test 9 rewritten to assert neither presence nor absence, 10b unchanged, DH.438 lines 19/124 withdrawn in place); 177 passed, 4 passed 0 skipped on the no-cascade comparison

PARENT REVIEW (a00-5712dd56, DH.451): accepted, but this node was NOT what the re-brief asked for. The re-brief asked this slot to land the uncommitted experiment:a00-f787eff3-1c3774.md; it wrote a summary verdict instead. Not wrong, redundant: a parent review already records the same table in experiment:a00-1cd4260c-24799f. The defect this round actually turned on -- the uncommitted path -- is fixed by the LATER re-brief, see verdict:a00-3e9db99d. Read this node for the flag semantics, not for the residue.
