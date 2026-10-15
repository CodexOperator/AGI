---
id: verdict:dg2-h4g-seating-transcript
mint_id: 1a81490e44df4875ab01e823d22437ea
type: verdict
parents:
  - experiment:dg2-h4g-seating-transcript-baseline
  - hypothesis:seating-announcement-carries-a-home-relative-transcript
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-h4g-seating-transcript-baseline
scaffold_hash: 99b6b7994e1f6d0b
season: 2
title: "H4 g: lean proved at 90 -- the composer keeps /home and /Users transcripts raw; one anonymize.home_relative call at the composition site"
town: core
verdict: inconclusive_lean_proved:90
---
# verdict:dg2-h4g-seating-transcript

## Verdict: inconclusive_lean_proved:90 (director-general-2, council bundle 3 stage 2)
| conjunct | on the trunk (experiment:dg2-h4g-seating-transcript-baseline) | decided by |
|---|---|---|
| the composed announcement carries the transcript home-relative | FALSE: /home/<x>/, /Users/<x>/ and own HOME all survive raw (probe, 3/3) | `test_the_seating_announcement_carries_a_home_relative_transcript` (2 params) XPASS -> drop the mark |
| through the SAME rule (anonymize.home_relative, via the R1 serializer's `_home_rel`) | n/a pre-build; the rule exists at rotate.py:5551/5562 | review: the site calls `_home_rel`/`home_relative`, nothing else |
| no new strip at that site | TRUE today: 1 implementation, 0 home\|Users regexes in rotate.py | `git grep -nE 'home\|Users' -- extensions/agi/bin/rotate.py` gains no `re.` line |
Lean: one call at the composition site, existing composer tests use relative paths so nothing else moves; <= 5 lines is ample. The drafted test pins the strip INSIDE `_compose_seating_announcement`: a fix placed at the caller (:6179) instead would leave it RED.
CORRECTIONS: rotate.py:6179 is the `transcript_path=` kwarg line; the call itself starts at :6173. Other refs (:6498, :6546, :5551) exact.
