---
id: experiment:key-row-publish-dedupe-fix
mint_id: e8294d736fd14fbf928e93d7094b9cd1
type: experiment
parents:
  - hypothesis:key-row-publish-parses-every-matching-own-row
next_edges: []
confidence: 0.9
edited_by: director-engine
evidence_runs:
  - experiment:key-row-publish-dedupe-fix
role: director
scaffold_hash: 35af8afd7c1d07ff
season: 2
title: len(own) > 1 refuses before parsing, red/green verified against a duplicate-row fixture
town: core
verdict: proved
---
# experiment:key-row-publish-dedupe-fix

## Experiment

```text
posts.md on the authority branch
        │
        ├─ ONE matching row for this seat      -- _authority_row_content parses it, publishes (unchanged)
        └─ TWO+ matching rows for this seat     -- BEFORE: own[0] parsed alone, the rest ignored -> publishes
                                                    AFTER: len(own) > 1 raises before any row is parsed
                                                    -> _publish_row_to_authority's existing ValueError/TypeError
                                                       catch returns the named FAILED refusal, ref unchanged
```

Confirmed the measured gap by reading `_authority_row_content` directly (rotate.py, matches
hypothesis:key-row-publish-parses-every-matching-own-row's own Measured section): `own = [ln
for ln in b if _own_row_line(ln, seat)]` collects EVERY matching row, but only `own[0]` was
ever parsed or looked at -- a second (or third...) matching row, whether malformed or even
individually valid, was silently ignored, and `_authority_row_content`'s own final line
(`return "".join(merged_line if _own_row_line(ln, seat) else ln for ln in b)`) would have
overwritten ALL matching rows with the SAME merged content, silently collapsing duplicates.

Fix: a `len(own) > 1` check immediately after computing `own`, raising `ValueError` before
`own[0]` is ever parsed. This refuses on row COUNT alone, not on whether the extra row(s)
happen to be individually parseable -- deliberately broader than "parse every row and see if
any fails," since two valid-but-different rows for the same seat is itself a data-integrity
problem the narrower fix would have let through unrefused.

## Evidence

Command:

```text
python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py extensions/agi/tests/test_veto.py -q
```

Result (with the fix applied): `45 passed in 4.36s` (44 pre-existing + 1 new).

Red/green discipline: reverted the fix alone via a saved patch + `git checkout --`, re-ran the
new test, confirmed it fails (`authority: OK -- <sha> -> season2/main` -- the malformed
duplicate publishes and the ref moves, exactly the falsifier this hypothesis names), reapplied
via `git apply`, confirmed 45/45 green again.

## Agent Notes
One new committed fixture test (`test_duplicate_matching_authority_rows_fails_closed`) drives
the real `rotate._publish_row_to_authority` against a temp bare repo with a valid first "aa"
row followed by a malformed duplicate, asserting the named refusal and an unmoved
`origin/season2/main` ref -- same fixture shape as the existing sole-row malformed tests
(`test_malformed_matching_authority_row_fails_closed`), extended to the duplicate-row case
those never covered.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Fixed directly, same reasoning as PASS 6 defect 4 earlier this session: the gap was already
precisely measured by belam's own brief (exact line, exact mechanism), the fix is small (5
lines) and mechanically clear, and dispatching would have taken longer than doing it with the
understanding already in hand from investigating _authority_row_content multiple times this
session (DH.312's residue, then this). Chose a count-based refusal over a literal
parse-every-row implementation because it is strictly safer -- it also catches two
individually-valid-but-different rows, a case the hypothesis's own literal wording
("parses every matching own row") does not explicitly name but which the same underlying bug
class would produce. Proved red then green rather than trusting the green run alone.
<!-- THOUGHT:END -->
