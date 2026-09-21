---
id: experiment:a00-2a6402d0-9d9033
mint_id: 982d81eccd28498aad19eba4ff5c3039
type: experiment
parents:
  - hypothesis:l4-an-unchanged-since-rotate-out-stops-slot-is-refused-by-that-name-never-called-stale
next_edges: []
confidence: 0.95
edited_by: a00-abf18d88
evidence_runs:
  - experiment:a00-2a6402d0-9d9033
line_ceiling: 10
loop: hypothesis:l4-an-unchanged-since-rotate-out-stops-slot-is-refused-by-that-name-never-called-stale@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe1.py on live rotate.py: git init, card slot text 'run the suite and report', commit 'prime rotate-out gen 4->5', cmd_rotate bare", "expected": "exit 2; refusal says UNCHANGED since your predecessor; NO STALE; nothing delegated", "observed": "exit 2: 'rotate refused: where-it-stops slot UNCHANGED since your predecessor's prime rotate-out gen 4->5 @ 15302c03 2026-09-17 ... it is their card, not yours -- write the slot, or pass --stops (nothing delegated)'; no STALE anywhere; called=[]", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe2.py: commit rotate-out with text A, rewrite slot to text B, force year-2001 mtime (age irrelevant via os.utime), cmd_rotate bare", "expected": "delegates exit 0 with stops=B regardless of mtime", "observed": "exit 0 stops=['hand off the round'] err=''", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "parent probe1.py // the same live run whose stderr proves the new message bytes reach the real cmd_rotate call site (not a stub); probe2 proves a changed slot never reaches the refusal", "expected": "new UNCHANGED wording flows out of _stops_slot_is_stale through cmd_rotate to a caller; the single stripped-slot compare is the only gate", "observed": "p1 stderr shows the new wording from the gate via cmd_rotate; p2 delegates on changed", "result": "pass"}
production_lines: 4
profile: balanced
role: kid
scaffold_hash: 3653df2a3448096e
season: 2
thought_session: SM.95
title: stops-slot refusal names UNCHANGED never STALE
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2a6402d0-9d9033

## Experiment

Goal:g15 BUILD ORDER — reword the derived-stops-slot refusal so it names the
slot UNCHANGED since the predecessor's rotate-out and never calls it STALE
(F23's vocabulary), keeping the mechanism (single stripped-text comparison
vs. the predecessor's rotate-out commit slot via one locator) and the
delegate-on-changed behaviour intact.

Conjunct 1 (the wording): rewrote the refusal in
`extensions/agi/bin/rotate.py` `_stops_slot_is_stale` (orig ~L17497).

  BEFORE: `where-it-stops slot is STALE (unchanged since {seat} rotate-out... )`
  AFTER:  `where-it-stops slot UNCHANGED since your predecessor's {seat} rotate-out gen N->N+1 @ <sha> <date>; newest work act <act> from <src>: it is their card, not yours -- write the slot, or pass --stops`

The useful detail is preserved: gen pair (from the commit subject's
`gen N->N+1`), short sha + date, and the newest-work-act stamp + its source.
The word STALE no longer appears anywhere in the refusal.

Conjunct 2 (changed-delegates): untouched by the change. The gate only fires
when `committed == text.strip()`; any diff, however old, returns None and
delegates (test 11 `test_rewritten_slot_delegates` and 12b `test_retry_after_blocked_rotate_out_not_stale` still green — age is not the test).

Conjunct 3 (single comparison): untouched. One locator
(`_stops_body_text`/`_default_stops_text`), one byte compare of the stripped
slot text vs the predecessor rotate-out slot; no mtime/age reader, no second
slot reader (test 11 still asserts the sha256 on the delegated namespace).

Tests: updated test 10 (`test_stale_stops_slot_refuses_by_name_not_delegated`)
and test 17 (`test_stale_refusal_names_both_stamps_and_source`) to assert the
UNCHANGED wording, assert "STALE" NOT in err, and assert the new fix line
"it is their card, not yours -- write the slot, or pass --stops".

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate_verb.py -q`
-> 21 passed, 3 warnings (DeprecationWarning datetime.utcnow, pre-existing).

The stale-gate cohort (10/11/12/12b/13/16/17) flips as claimed:
- 10: exit 2, UNCHANGED wording present, STALE absent -> FALSIFIER dead.
- 11: rewritten/changed (old) slot delegates -> changed-though-old passes.
- 12/13: first seating / explicit --stops delegates.
- 17: both stamps named, STALE absent.

FALSIFIERS all dead:
- "STALE" in refusal: gone (asserted not-in on 10 & 17).
- changed-since-rotate-out refused: test 11 & 12b still delegate.
- unchanged-since-rotate-out passing: test 10 / 17 still exit 2.

Production-line ceiling: `git diff --numstat` -> 4/4 on rotate.py (<=10);
tests 5/4 on test_rotate_verb.py (test files excluded from ceiling).

## Agent Notes
Reworded the derived-stops refusal in rotate.py _stops_slot_is_stale to 'UNCHANGED since your predecessor's {seat} rotate-out gen N->N+1 ... it is their card, not yours -- write the slot, or pass --stops'; STALE gone from the refusal. Mechanism untouched: single stripped-slot compare vs predecessor rotate-out commit, changed-delegates intact. Updated test 10 & 17 to assert UNCHANGED + STALE NOT in err; full test_rotate_verb.py 21 passed. 4 prod lines.

PARENT REVIEW (SM.95 a00-abf18d88): read the kid diff 7f3d77cb2..85ea38c68, not its result file. The changed bytes are only the refusal wording in _stops_slot_is_stale (rotate.py) + two test asserts; mechanism untouched. Ran 3 independent negative probes on LIVE rotate.py (not the kid suite): (1) unchanged slot -> exit 2, refusal says UNCHANGED since your predecessor, no STALE, nothing delegated; (2) changed-but-year-2001-mtime slot -> delegates exit 0 with stops set; (3) wire: the new wording reaches the real cmd_rotate call site. All falsifiers dead; accepted verdict=proved, 4/10 prod lines, real title.
