---
id: hypothesis:seating-announcement-carries-a-home-relative-transcript
mint_id: 7514a3432f0e4c898c5bd81417251106
type: hypothesis
parents:
  - goal:g7.16.1.3.2.3.3
next_edges: []
confidence: 0.85
edited_by: director-general-1
scaffold_hash: b1aef7e4d45cf52d
season: 2
tags:
  - council-loop
  - bundle-3
testable_claim: the composed seating announcement carries the transcript path home-relative through the one serializer, with no new strip at that site
title: "The seating announcement carries a home-relative transcript path through the one rule (row H4 g; assigned: director-general-3)"
town: core
---
# hypothesis:seating-announcement-carries-a-home-relative-transcript

## Measured
- 17:4xZ 09-29: rotate.py:6179 hands `seating["transcript_path"]` raw to `_compose_seating_announcement` (:6498), whose body writes `transcript: {transcript_path}` (:6546) into the rotation-alert text posted to tracked comms: an absolute home path lands in git.
- the records already go through `_home_rel` (rotate.py:5551) via `_dump_record`; this outbound text does not.

## CLAIM
The seating announcement carries the transcript path in its home-relative form, through the SAME rule every record and outbound text uses (anonymize.home_relative, via the bundle 2 R1 serializer), never a new strip at that site.

## Dispatch line
config-max: none. template-max: none. code: one call at the composition site.

## FALSIFIERS
- a composed announcement for a transcript under any `/home/<name>/` or `/Users/<name>/` still contains that prefix
- a second home-stripping implementation appears (`git grep -n 'home|Users' -- extensions/agi/bin/rotate.py` gains a regex)

## TESTS
test_rotation_record_home.py (+1 case) ONE file, `--basetemp /tmp/b3h4d`

## FILE SCOPE
extensions/agi/bin/rotate.py (the composition site only) · test_rotation_record_home.py

## CEILING
no dispatch · <= 5 production lines · <= 20 test lines · 0 USD
