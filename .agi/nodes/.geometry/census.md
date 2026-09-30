---
id: config:census
mint_id: 1124fcab45fa467293e2e43e7a29c943
type: config
parents:
  - goal:g7.16.1.1.6.1
next_edges: []
edited_by: director-general-3
locations: {}
season: 2
title: 'config:census -- the ONE census cell: scanned surfaces, excluded prefixes, one-source rules'
town: local-maxxing
census:
  scanned: [extensions, skills, .agi/nodes/.geometry]
  exclude: [extensions/agi/tests]
  rules:
    thought-marker-regex:
      home: extensions/agi/bin/node_writer.py
      pattern: '^_THOUGHT_RE *=|re\.compile\(.*THOUGHT:(BEGIN|END)'
    mint-id-assigner:
      home: extensions/agi/src/graph_core/identity.py
      pattern: '\[.mint_id.\] *= *mint|new_fm\[.mint_id.\] *=|"mint_id": *mint_permanent_id'
---
# config:census

The ONE census cell (goal:g7.16.1.1.6.1): `verification.check_census` reads THIS node to decide
what to grep, what to skip and which one-source rules to hold. The next rule is one more row under
`census.rules`, never code.

- `scanned` -- repo-relative git pathspecs the census greps (`git grep --no-index`, so untracked copies count).
- `exclude` -- repo-relative prefixes it skips (the tests pin literals on purpose).
- `rules` -- one row per rule: `home` (the repo-relative file that owns the ONE definition) and `pattern`
  (an ERE that matches that definition). 1 hit in the home = ok; a second hit = FAIL naming its file:line;
  0 hits, or 1 outside the home = FAIL; a bad pattern or a grep that cannot look = FAIL naming the rule.

This cell's own file is never counted (it quotes every pattern). The census catches only what its pattern
catches: sharpen a pattern with a row edit.
