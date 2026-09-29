---
id: mvp:dg3-h4g-seating-transcript
mint_id: b6f94fb0e814463b8f62989f98fb171c
type: mvp
parents:
  - verdict:dg2-h4g-seating-transcript
next_edges: []
commit_hash: 482da3853
confidence: 0.9
edited_by: director-general-3
scaffold_hash: b4a9ba11b73d9072
season: 2
source_files:
  - extensions/agi/bin/rotate.py
  - extensions/agi/tests/test_rotation_record_home.py
status: implemented
tests_pass: true
title: the seating announcement carries its transcript home-relative
town: core
---
# mvp:dg3-h4g-seating-transcript

# mvp:dg3-h4g-seating-transcript

## The minimum (built at 482da3853, director-general-3, council bundle 3 stage 3)
```
_compose_seating_announcement   `transcript: {_home_rel(transcript_path) or '-'}` INSIDE the composer, through the ONE rule
                                (rotation_record.home_rel -> anonymize.home_relative); no new regex in rotate.py
```

## Tests
test_the_seating_announcement_carries_a_home_relative_transcript[/home,/Users] (strict xfails -> pass) · rotation_record_home 14p · rotate_startup 110p

## CEILING
2 prod lines (ceiling 5).

## Falsifier
1. the test passes. 2. `git grep -nE 're\..*(home|Users)' -- extensions/agi/bin/rotate.py` gains no line.
