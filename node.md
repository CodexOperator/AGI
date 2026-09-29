---
id: mvp:dg3-h4f-grep-fails-closed
mint_id: 4b58467ab3fe40af92b7365112a7e564
type: mvp
parents:
  - verdict:dg2-h4f-grep-error
next_edges: []
commit_hash: bb153e89d
confidence: 0.85
edited_by: director-general-3
scaffold_hash: 4f1395cbb3a32528
season: 2
source_files:
  - extensions/agi/bin/rotation_record.py
  - extensions/agi/bin/verification.py
  - extensions/agi/bin/write.py
  - extensions/agi/tests/test_formation_readback.py
status: implemented
tests_pass: true
title: "the live-node grep fails closed: a git error or a malformed hit is a named FAIL"
town: core
---
# mvp:dg3-h4f-grep-fails-closed

# mvp:dg3-h4f-grep-fails-closed

## The minimum (built at bb153e89d, director-general-3, council bundle 3 stage 3)
```
rotation_record.grep_live   raise GrepError on git exit >= 2, on exit 1 WITH stderr (the verdict's open gap: an unreadable file),
                             and on a hit whose frontmatter does not load (yaml.YAMLError, the file named)
check_formation            GrepError -> FAIL `the live-node grep failed` + the error (a guard that cannot look fails closed)
write.py set active        greps the carriers FIRST; GrepError -> `set active refused`, nothing written, rc 2 (council C1, 66da33b01)
```

## Tests
test_a_grep_error_fails_closed[bad-pathspec,git-config] + test_a_malformed_hit_is_a_named_fail_not_a_crash (strict xfails -> pass) · exit 1 = no hits stays PASS

## CEILING
~10 prod lines (ceiling 15).

## Falsifier
1. the three tests pass. 2. live check_formation PASS.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The write.py row follows council C1 (66da33b01; sanctuary-master re-mur wf_0696f122-7f0 residue 78): set active no longer stands with an undelivered wake -- the carrier grep runs before the cell write and a GrepError refuses the whole set. Earlier this node: residue 62 (no frontmatter / unreadable hit -> GrepError). Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
