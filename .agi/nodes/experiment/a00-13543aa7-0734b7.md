---
id: experiment:a00-13543aa7-0734b7
mint_id: c85d1338df28494d9fba5fa03f3c0c67
type: experiment
parents:
  - hypothesis:l4-written-by-message-and-shape
next_edges: []
confidence: 0.9
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-13543aa7-0734b7
loop: hypothesis:l4-written-by-message-and-shape@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 88a0d1c59f1fd33f
season: 2
title: A00 13543aa7 0734b7
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-13543aa7-0734b7

## Experiment

Ran hypothesis:l4-written-by-message-and-shape. Changed the `_enforce_written_by`
refusal in `extensions/agi/bin/write.py` so the message names the node TYPE and
its admitted writers, and made `written_by` admit a LIST or a comma-separated
string. The comparator is UNCHANGED: still `actor not in admitted` — no role
resolution, which is L4.41. Added a shared parse, `links.parse_written_by`, in
`extensions/agi/bin/links.py` and refactored the report's `_admitted` to use it,
so the report and the enforcer can never disagree about what the field holds.

Commands run — the ONLY suite, respecting the claim's ceiling:
```
python3 -m pytest extensions/agi/tests/test_write.py \
    extensions/agi/tests/test_links.py \
    extensions/agi/tests/test_write_guard.py -q
```

## Evidence

GREEN: `115 passed in 1.28s`. The moral tests plus the THREE new written_by tests
pass in isolation: `8 passed in 0.92s`.

What changed in `test_write.py` — the ONE retargeted assertion, reviewable here:
- `test_create_moral_without_owner_is_refused` retargeted from
  `pytest.raises(..., match="owner only")` to `match="moral"` and asserts MORE
  than before: the message names the TYPE (`moral`) and the admitted writer
  (`owner`), and does NOT contain the old phrase `owner only`. It was not
  loosened to `match=""` and not deleted.
- No OTHER existing assertion in any of the three files was touched.
  `test_submit_moral_without_owner_is_refused` (match="owner") is unchanged and
  still passes because the new moral message still contains `owner`.
- Added three new tests on FIXTURE schemas (never the real `[moral].md`):
  (1) a non-moral type `variorum` with `written_by: scribe` refuses with
  `variorum` and `scribe` in the message and `moral` ABSENT;
  (2) a LIST `written_by: [scribe, corrector]` admits BOTH and refuses an
  unlisted writer; (3) the comma-string parses identically to the list
  (`parse_written_by("scribe, corrector") == parse_written_by(["scribe","corrector"])`)
  and gates the same.

Disprove conditions all checked and NOT triggered: comparator still on the actor;
no real schema gained a `written_by`; exactly one existing assertion retargeted
(and it asserts MORE, not less); scalar `written_by: owner` still REFUSES without
`--actor owner` and PASSES with it — `[moral]` behaviour byte-identical. Ran only
the three named test files, not the full suite.

## Agent Notes
message now names type+admitted writers via shared links.parse_written_by; list+comma forms admitted; single assertion retargeted stronger; 115 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director review (L4.40, a00-4d02cd79): proved ACCEPTED after independent verification, not on the kid report alone. I read the full diff in the worktree and re-ran the three named files myself: 115 passed. Checks against the claim: (1) the compare is still exactly `actor not in admitted` — no role resolution leaked in (L4.41 stays out); (2) the refusal now names node_type and the admitted writers; (3) `links.parse_written_by` is the one parse, and `_admitted` in links.py was refactored onto it, so report and enforcer cannot diverge; (4) git diff --stat shows ONLY write.py, links.py, test_write.py, the experiment node and autoresearch.jsonl — no real schema gained written_by, test_links/test_write_guard untouched; (5) the one retargeted assertion asserts MORE (type `moral`, writer `owner`, old phrase absent), matching the claim narrow exception; (6) empty/None `written_by` still gates nothing (falsy set), so undeclared types are unchanged. The kid reported a mid-run stall that produced a false first node and done call, then rewrote — final state is coherent. The caveat (no end-to-end assertion through the `links.py roles` report) is accepted: the claim requires only that the parses agree, and they now share one function.
<!-- THOUGHT:END -->
