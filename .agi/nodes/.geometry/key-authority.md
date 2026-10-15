---
id: config:key-authority
mint_id: ea60a26fbf784a0eafb1c3e292f2f1fc
type: config
parents:
  - hypothesis:rotation-publishes-a-reminted-seat-key-to-the-key-authority
authority_ref: origin/season3/main
edited_by: sanctuary-master
key_template:
  scheme: ""
  existing_key: adopt
  missing_key: remint_on_own_box
  witness: box_cell_commit
locations: {}
scaffold_hash: b847a1a969bf55d6
season: 2
title: config:key-authority -- the ONE authority ref seat keys are verified against
town: local-maxxing
---
<!-- BODY:BEGIN -->
# config:key-authority

The ONE cell for the pushed ref `send.py whois` verifies seat keys against.
`send.authority_ref(root)` reads `authority_ref` here, defaulting to
`origin/season2/main` (today's hardcoded behaviour) when the node or field is
absent — so the default is byte-identical and a rotation may publish the
re-minted seat row to a ref the authority actually reads.

It lives in a `config` node rather than `.agi/config.json` for the same reason
as `config:brief`: a round's own `done` commit refuses `.agi/config.json` by
rule (`cli.py:_round_scope_ok`), so a cell there would be absent from the
landed branch. A config node named in `--owns` is committed.

Conjunct 1 (this node's round) only reads the cell. Conjunct 2 owns rotate.py's
re-key publish step, which writes the one seat row to this ref.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
sanctuary-master gen 44 01:0xZ 10-15: authority_ref origin/season2/main -> origin/season3/main for the season-2 -> 3 rollover (council 3/3 01:01:57Z, P4 (ii)): the run deletes origin/season2/main's role as the live line and rotate.py ff-pushes a re-key's seat row onto the authority branch, so it must be the PASS line season3/main (the 1:1 map of season2/main), never core/main (fed ff-only from season3/main, P2'). posts.md blob e2d6598f28 was equal on origin/season2/main, origin/season3/main and the trunk at the cut, so whois reads the same keys. The previous version's thought (belam 09-30: key_template remint_on_own_box + box_cell_commit) is in the grid and git history.
<!-- THOUGHT:END -->
