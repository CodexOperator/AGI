---
id: config:census
mint_id: 1124fcab45fa467293e2e43e7a29c943
type: config
parents:
  - goal:g7.16.1.1.6.1
  - goal:g7.16.1.1.6.2
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
    anonymize-home-token:
      home: extensions/agi/bin/anonymize.py
      pattern: '^HOME_PATH_RE *= *_home_path_re\('
    home-code-literal:
      home: extensions/agi/bin/paths.py
      pattern: '^HOME_RE *= *re\.compile'
---
# config:census

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 08:4xZ 10-04, goal:g7.16.1.1.6.2. Two named rules, not one def: anonymize.HOME_PATH_RE is the physical-token check (any-box home path); paths.HOME_RE is a wider code-literal lint (~/, $HOME, expanduser). They are not a byte copy, so one row would FAIL. test_no_home_literal.py _HOME_LITERAL stays under census.exclude.
<!-- THOUGHT:END -->

The ONE census cell (goal:g7.16.1.1.6.1 + goal:g7.16.1.1.6.2): `verification.check_census` reads THIS node to decide
what to grep, what to skip and which one-source rules to hold. The next rule is one more row under
`census.rules`, never code.

- `scanned` -- repo-relative git pathspecs the census greps (`git grep --no-index`, so untracked copies count).
- `exclude` -- repo-relative prefixes it skips (the tests pin literals on purpose).
- `rules` -- one row per rule: `home` (the repo-relative file that owns the ONE definition) and `pattern`
  (an ERE that matches that definition). 1 hit in the home = ok; a second hit = FAIL naming its file:line;
  0 hits, or 1 outside the home = FAIL; a bad pattern or a grep that cannot look = FAIL naming the rule.

This cell's own file is never counted (it quotes every pattern). The census catches only what its pattern
catches: sharpen a pattern with a row edit.
