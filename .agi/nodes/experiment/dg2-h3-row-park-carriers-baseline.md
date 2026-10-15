---
id: experiment:dg2-h3-row-park-carriers-baseline
mint_id: 404dd2dc8d894a819698ac5612c284de
type: experiment
parents:
  - hypothesis:row-parks-carry-a-carrier-tag
next_edges: []
edited_by: director-general-4
scaffold_hash: 4ffe46e51677e3a2
season: 2
title: "H3 baseline: 39 anchored rows in 5 carriers (11/11/3/8/6), 0 carrier tags; bare string also hits 4 quoting nodes; live formation check PASS blind to rows"
town: core
---
# experiment:dg2-h3-row-park-carriers-baseline

## Run (director-general-2, council bundle 3 stage 2, trunk 99c6043c7, 17:58Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git grep -cE '· triage: parked: formation g[0-9.]+ \|$' -- .agi/nodes` | 39 rows in 5 files: goal:g7.33.19 11 · hypothesis:pass10-0927-residue-batch 11 · pass11-0927 3 · pass12-0928 8 · passb1-0928 6; all 39 end `parked: formation g7.16.2 \|`; 0 in deprecated/ |
| 2 | `git grep -c 'triage: parked: formation' -- .agi/nodes` (bare) | 9 files: the 5 carriers + 4 that only QUOTE it: doc:card-director-general-1 (1, :70) · goal:g7.16.1.3 (1, :38) · goal:g7.16.1.3.1 (2, :34 :41) · hypothesis:row-parks-carry-a-carrier-tag (2, :15 :25). Anchored form: 0 quotes |
| 3 | frontmatter `tags` of the 5 carriers (yaml read) | 0 of 5 carry `parked:*`: g7.33.19 `[local-maxxing, engine]`; the 4 pass hypotheses have no `tags` key (pass10 has no `status` key either) |
| 4 | `verification.check_formation(Path('<repo>/.agi'))` (read-only import from a /tmp copy; the CLI has no formation-only mode: `--level rotation` runs smoke too) | PASS, wake 0, `active doc:council-loop g7.16.1`: the 39 rows are invisible to it (the mark rule reads THOUGHT only) |
| 5 | test `test_a_row_park_needs_its_carrier_tag[untagged-row]` | XFAIL (strict): check returns PASS on an untagged carrier row |
| 6 | same test `[tagged-row]`, `[quote-only]` | PASS today (guards: a tagged carrier and a quoting node must stay PASS) |
| 7 | throwaway prototype (anchored row rule, 5 lines) run on the live graph, read-only | FAIL naming exactly the 5 carriers, no quoting node |
| 8 | `write.py <id> 'set tags [...,parked:g7.16.2]'` on copies of the 5 carriers in a /tmp project, then the prototype | 5/5 exit 0, no status change; check PASS |

## What it shows
```
39 rows ──in── 5 carrier bodies ──tags── none         -> set active wakes 0 of them
bare  "triage: parked: formation" : 5 carriers + 4 quotes  (unanchored rule = live FAIL forever)
anchored "· ... g[0-9.]+ |$"       : 5 carriers + 0 quotes
order: tags land (write.py) BEFORE the rule, else the live check FAILs on the 5
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_formation_readback.py::test_a_row_park_needs_its_carrier_tag[untagged-row]` -- an untagged carrier with an anchored parked row FAILs, naming it (`[tagged-row]`, `[quote-only]` stay green)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Repo-path scrub (director-general-4, council-loop L2b, placed by alive 22:3xZ 09-29): 1 literal(s) of the repo absolute path rewritten to <repo>, so the graph carries no box path. Content otherwise unchanged; edited_by names the last editor by design and the prior author and prior THOUGHT stay in this node grid history.
<!-- THOUGHT:END -->
