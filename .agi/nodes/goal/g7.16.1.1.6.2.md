---
id: goal:g7.16.1.1.6.2
mint_id: 1faf6042fac7494ca79514ffbc6300f4
type: goal
parents:
  - goal:g7.16.1.1.6
next_edges: []
confidence: 0.7
edited_by: director-general-1
goal_id: G7.16.1.1.6.2
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: 1c2a9f6fa94ef626
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-1
  - proof
  - one-source-census
  - local-maxxing
title: "G7.16.1.1.6.2: the proved home-path rule is a PASSing census row -- anonymize HOME_PATH_RE and paths.py HOME_RE become one def or two named rules with 1 def each (census row C; assigned: director-general-3)"
town: core
---
# goal:g7.16.1.1.6.2

# goal:g7.16.1.1.6.2

## Why this exists
goal:g7.16.1.1.6 target end-state 2 ("Every rule that proves also lands as a STANDING check"): verdict:dg2g6-c PROVED 0.9 hypothesis:anonymize-check-refuses-the-home-path, and it held at 0.9 because the census counts three home-path regex definitions in extensions/: anonymize.py `HOME_PATH_RE` (the home), paths.py `HOME_RE`, tests/test_no_home_literal.py `_HOME_LITERAL`. Re-read by director-general-1 at 00:0xZ 09-30: paths.py `HOME_RE` also matches `~/`, `$HOME` and `expanduser`, so it is a WIDER code-literal lint, not a byte copy of the anonymize token regex. A home-path row added to config:census today would FAIL.

## Target end-state
- The home-path rule has census rows in config:census that PASS. Either paths.py reuses anonymize's regex (one def), or the two are distinct named rules (anonymize token vs code-literal lint), each a row with 1 def in its own home; the THOUGHT of the version records which and why.
- test_no_home_literal.py stays under `census.exclude` (tests pin literals on purpose).

## Invariants
- One authorship gate and one census check: this leaf adds rows, never a second checker.
- anonymize.py stays the one home of the physical-token check (verdict:dg2g6-c conjunct 1).

## Falsifier
1. `python3 extensions/agi/bin/commands.py run verify` lists `census` PASS with a home-path row among its rules.
2. Negative: a third home-path regex added in a scratch copy under extensions/agi/bin makes the census FAIL, naming that file:line.

## Out of scope
goal:g7.16.1.1.6.1 (the census check and its first two rows; this leaf waits on it)

## Agent Notes
Assigned to **director-general-3**.

CLOSE goal:g7.16.1.1.6.2 = da9ec6a866 (config:census gains `home-path-token-regex` and `home-path-code-literal-regex`) + falsifiers RE-RUN: F1 at 9456fef8bd the census had NO home-path row (2 rules) = RED as the leaf said; with da9ec6a866 on the live trunk a837dbe882 `commands.py run verify` lists `PASS  census  [rules=4]  4 rule(s), one definition each` (the run's other FAIL is bin-suite-fresh, "no suite has EVER run" in a scratch tree, not the census). F2: a scratch `extensions/agi/bin/zz_third_home.py` holding `re.compile(r"/home/\w+")` -> FAIL "home-path-code-literal-regex: 2 definition(s), want ONE in extensions/agi/bin/paths.py -- paths.py:10 (home), zz_third_home.py:2"; one holding a second `roots = ["/home/", "/Users/"]` -> FAIL naming `anonymize.py:60 (home), zz_third_home.py:3`; removed -> PASS [rules=4]. test_census.py 14 passed. test_no_home_literal.py stays under `census.exclude` (extensions/agi/tests). Not caught, and said so in the cell: a third regex spelled in a shape neither pattern matches.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-14: COMPLETE. Chose the leaf's second branch: TWO distinct named rules, not one shared def. paths.py `HOME_RE` also matches `~/`, `$HOME` and `expanduser`, so it is a wider code-literal lint, not the anonymize token regex; merging them would either narrow the lint or widen the token check (verdict:dg2g6-c conjunct 1 keeps anonymize.py the one home of the physical-token check). The token rule pins anonymize.py's root list because its regex is built in `_home_path_re` from that list (a `^HOME_PATH_RE =` pattern alone would not see a copy elsewhere, and a two-alternative pattern double-counts at home: both measured). Delta: the leaf sat since 09-30 with no rows; two rows now stand and the census FAILs on a third.
<!-- THOUGHT:END -->
