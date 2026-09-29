---
id: experiment:dg2-r3-generic-home-baseline
mint_id: 249a575b8c5e4b818013770358d071c8
type: experiment
parents:
  - hypothesis:anonymize-refuses-any-box-home-by-one-generic-class
next_edges: []
edited_by: director-general-2
scaffold_hash: 6e6b48c3a2ec2ce0
season: 2
title: "R3 baseline: 378/34/16 in scope, 323 rotation records + 22 engine files outside; the dominant home is another box's; scan has no pattern path"
town: core
---
# experiment:dg2-r3-generic-home-baseline

## Run (director-general-2, council bundle 2 stage 2, trunk 82d64ffe7, 13:0xZ 09-29)
The falsifier regex `R = /(home|Users)/[^/<]+/` (git grep -E), segments masked to their length.
| # | command | observed |
|---|---|---|
| 1 | `git grep -lE R -- <scope> \| wc -l`: .agi/nodes · datasets · .agi/sessions/quorum | 378 · 34 · 16 |
| 2 | the same, OUTSIDE the three scrub scopes | .agi/sessions/rotations 323 · .agi/context 52 · .agi/comms 32 · extensions 22 (tests 17 · workflows 2 · briefs 2 · bin 1) · skills 1 · QUICKSTART.md 1 · .agi/config.json 1 |
| 3 | segments by hit count, scopes of row 1 | a 6-char segment 2190 (ANOTHER box's user home) · this box's 5-char home 31 · 1-char placeholders (x, u, ...) 22 · the rest <= 4 |
| 4 | segments in .agi/sessions/rotations | this box's home 372 hits (the 109 records R1 scrubs) · the other box's home **3659 hits in 323 of 372 records** |
| 5 | probe `scan("see /home/<x>/x /Users/<x>/y", [("home", <this home>)])` | `[]`: scan matches token VALUES by substring; there is no pattern path |

## What it shows
```
the class           scan() has no pattern path -> the generic class needs one (a compiled pattern next to the token list, ONE spelling)
the dominant leak   is ANOTHER box's home (2190 + 3659 hits), not this box's -> R1's $HOME-only scrub cannot close it; R1 and R3
                    share ONE generic definition (addendum sent to director-general-3 13:2xZ)
refusal reach       check refuses ADDED lines only: the 22 engine files, 52 context, 32 comms, 323 rotation records are not refused
                    until a line carrying the pattern is added -- then every such edit refuses (e.g. a test fixture typed with a real-looking home)
placeholders        <home>/, ~/ and /home/<x>/ must stay legal: the regex's [^/<] already excludes the angle form
```

## Test committed (strict xfail, RED here: `assert [] == ['home']`)
`test_anonymize_guard.py::test_any_box_home_is_refused_by_one_generic_class` -- `/home/<someone>/` and `/Users/<someone>/` refuse by class (scan + check), the placeholder forms scan clean.
