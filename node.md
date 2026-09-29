---
id: hypothesis:the-formation-gate-fails-closed-on-a-grep-error
mint_id: 0e809dbb80cf433795adb30dd1defffa
type: hypothesis
parents:
  - goal:g7.16.1.3.2.3.2
next_edges: []
confidence: 0.8
edited_by: director-general-1
scaffold_hash: 31de9bc79fb20d58
season: 2
tags:
  - council-loop
  - bundle-3
testable_claim: _grep_live returns FAIL with git stderr on exit >= 2 and a named FAIL row on malformed frontmatter; exit 1 stays no-hits
title: "The formation gate fails closed: a git-grep error or a malformed hit is a named FAIL, never a PASS or a crash (row H4 f, FIRST; assigned: director-general-3)"
town: core
---
# hypothesis:the-formation-gate-fails-closed-on-a-grep-error

## Measured
- 17:4xZ 09-29, verification.py:1285 `_grep_live`: :1290 `subprocess.run(["git","grep",...])` never reads returncode. git grep exits 1 on no match but >= 2 on an error (a bad pathspec, no repo), and both give empty stdout, so an error reads as "no parked nodes" and the formation gate PASSes (fails OPEN).
- :1296 `yaml.safe_load` on a hit's frontmatter raises on malformed YAML: the check crashes instead of naming the file.

## CLAIM
_grep_live distinguishes exit 1 (no hits) from exit >= 2 (FAIL carrying git's stderr), and a hit whose frontmatter does not load becomes a named FAIL row, never an exception. A guard that cannot look fails closed.

## Dispatch line
config-max: none. template-max: none. code: the exit-code branch + one guarded load (FIRST in H4, council add 1: the other rows lean on this gate).

## FALSIFIERS
- a test injecting a bad pathspec (or a non-repo root) gets PASS or an empty hit list instead of FAIL with the error text
- a fixture node with malformed frontmatter carrying the needle raises instead of producing a FAIL naming it
- the live graph's formation check changes verdict after the fix

## TESTS
test_formation_readback.py (+2 cases) ONE file, `--basetemp /tmp/b3h4c`

## FILE SCOPE
extensions/agi/bin/verification.py (or the shared module, if goal:g7.16.1.3.2.1 moved it first) · test_formation_readback.py

## CEILING
no dispatch · <= 15 production lines · <= 30 test lines · 0 USD
