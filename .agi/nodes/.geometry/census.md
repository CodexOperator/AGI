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
    home-path-token-regex:
      home: extensions/agi/bin/anonymize.py
      pattern: 'roots = \["/home/", *"/Users/"\]'
    home-path-code-literal-regex:
      home: extensions/agi/bin/paths.py
      pattern: 're\.compile\(r?.[^)]*(/home/|\$HOME|expanduser)'
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

Home-path rules (goal:g7.16.1.1.6.2): TWO distinct named rules, not one def. `home-path-token-regex` pins anonymize.py's physical-token
root list (`roots = ["/home/", "/Users/"]`, the one home of the check, verdict:dg2g6-c conjunct 1); `home-path-code-literal-regex` pins paths.py
`HOME_RE`, a WIDER code-literal lint (it also matches `~/`, `$HOME` and `expanduser`, so it is not a byte copy of the token regex). A third
`re.compile` carrying `/home/`, `$HOME` or `expanduser`, or a second `["/home/", "/Users/"]` list, under the scanned paths FAILs naming file:line.
Both patterns are shapes, not names: a third regex spelled some other way is not caught until its shape gets a row.
