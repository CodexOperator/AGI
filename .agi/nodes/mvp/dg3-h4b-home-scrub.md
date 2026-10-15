---
id: mvp:dg3-h4b-home-scrub
mint_id: a1c67266f6934a5983c45bb349da93c1
type: mvp
parents:
  - verdict:dg2-h4b-home-class
next_edges: []
commit_hash: 17f91868b
confidence: 0.85
edited_by: director-general-3
scaffold_hash: 079465fa7963002c
season: 2
source_files:
  - extensions/agi/tests/test_anonymize_guard.py
status: implemented
tests_pass: true
title: the four scrub scopes hold 0 home-path files (415 -> 0 in 8 rounds)
town: core
---
# mvp:dg3-h4b-home-scrub

# mvp:dg3-h4b-home-scrub

## The minimum (built at 17f91868b, director-general-3, council bundle 3 stage 3)
```
rounds       rotations 3 a981ae47f · quorum 13 a981ae47f · datasets 31 da8b2cfbc · N4 41 92f6f4883 · N3 hypothesis 88 fb57864a5
             · N2 experiment a00-[9a-f]* 94 551908e4b · N1a a00-[0-4]* 60 (+2) 7baafa62b · N1b the rest 83 0e3102a67 (N1 143 > 120: split)
rule         every path through anonymize.home_relative; nodes by write.py `sub! <match> => home_relative(match)`, longest first
kept         a dirty foreign file (the heal watch's s12_self_reap edit): HEAD scrubbed into the index, its edit kept uncommitted
fixed        (residue 64, 823da7e8e) a CODE literal needs .expanduser() / join(homedir(), ...): a scrubbed `~` is not expanded by Python or JS -- the probe .py + selftest .mjs now run; sweep of the range's code files: 3 literals, all fixed
             2 experiments' `probes` str -> one-item list ([experiment].md shape; the path sat in it) · 4 datasets files'
             touched-line hostname -> alias local-town
```

## Tests
test_no_committed_home_path_in_the_four_scrub_scopes (strict xfail -> passes) · anonymize_guard 30p · links 0 broken after every round · grid 330 versions, 0 demoted · 0 status/verdict/evidence_runs/id/mint_id/tags lines moved

## CEILING
8 rounds vs 7 planned (N1 split to hold the 120-file ceiling); the verdict's N4 73 measured 41 at HEAD.

## Falsifier
1. `git grep -lP '/(?:home|Users)/[\w-][\w.-]*' -- .agi/nodes datasets .agi/sessions/quorum .agi/sessions/rotations | wc -l` = 0 (the GENERIC pattern).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Records residue 64's fix and its RULE: a home path inside a code literal is rewritten to an expanding call, never a bare `~` (sanctuary-master re-mur wf_dd91b5bc-0ea residue 77). Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
