---
id: config:key-authority
mint_id: ea60a26fbf784a0eafb1c3e292f2f1fc
type: config
parents:
  - hypothesis:rotation-publishes-a-reminted-seat-key-to-the-key-authority
authority_ref: origin/season2/main
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
