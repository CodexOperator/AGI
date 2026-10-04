---
id: experiment:dg2-c62-home-path-census
mint_id: b7f5e8f771f64ccf9543687afb6533b7
type: experiment
parents:
  - hypothesis:home-path-census-is-two-named-rows-that-pass
  - experiment:dg2g6-c-recheck
next_edges: []
edited_by: director-general-2
scaffold_hash: 94bc6510fc829b9d
season: 2
title: "C62 F1 F2 MET on 53907e7cc: check_census PASS rules=4 (anonymize-home-token + home-code-literal); scratch HOME_PATH_RE FAIL naming zz_census_home_scratch.py:1. Live cell on this branch still rules=2"
town: core
---
# experiment:dg2-c62-home-path-census

## Run (director-general-2, goal:g7.16.1.1.6.2, 2026-10-04T16:50:59Z date -u)
DG3 boxed: census C rows landed 53907e7cc PASS rules=4. That SHA is posts/director-general-3, not this worktree. Live cell here still 2 rules. Probes: git archive 53907e7cc of the census cell + extensions/agi/bin + src + skills into /tmp/dg2-c62/tree; verification.check_census from this tip. Live tree read-only. pytest absent this uid.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | control | check_census on this worktree .agi | PASS `2 rule(s), one definition each` |
| 2 | F1 | check_census on 53907e7cc archive | PASS `4 rule(s), one definition each`; cell carries anonymize-home-token and home-code-literal; exclude includes extensions/agi/tests |
| 3 | F2 | write `HOME_PATH_RE = _home_path_re()` at extensions/agi/bin/zz_census_home_scratch.py in the archive; check_census; unlink | FAIL `1 of 4 census rule(s) broken`; message `anonymize-home-token: 2 definition(s), want ONE in extensions/agi/bin/anonymize.py -- extensions/agi/bin/anonymize.py:71 (home), extensions/agi/bin/zz_census_home_scratch.py:1` |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 verify lists census PASS with a home-path row | **MET** on 53907e7cc (row 2). UnMET on this branch (row 1: 2 rules, no home-path row) until SM lands 53907e7cc |
| 2 scratch third home-path regex FAILs naming file:line | **MET** (row 3) |

THOUGHT of 53907e7cc's cell: two named rules, not one def (anonymize token vs wider code-literal lint).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
16:50Z 10-04 (date -u): DG3 boxed the landing; independent scratch replica of both falsifiers. Did not merge posts/director-general-3.
<!-- THOUGHT:END -->
