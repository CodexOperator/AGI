---
id: config:brief
mint_id: 6a1f2c3d4e5b60718a9b0c1d2e3f4051
type: config
parents:
  - hypothesis:brief-py-assembles-every-first-turn-from-config
next_edges: []
edited_by: a00-3ca5e37d
locations: {}
season: 2
title: "config:brief — the ONE brief cell: parts per role + harness, the harness block per harness, the trajectory town"
town: local-maxxing
brief:
  parts: {"kid": ["head", "card", "extras"], "parent": ["head", "card", "extras"], "director": ["head", "card"], "prime_director": ["head", "card", "trajectory"], "master": ["head", "card", "trajectory"]}
  harnesses: {"claude-code": ["harness"]}
  harness_blocks: {"claude-code": "CLAUDE.md"}
  trajectory: {"town": "local-maxxing"}
---
<!-- BODY:BEGIN -->
# config:brief

The ONE `brief` cell (`hypothesis:brief-py-assembles-every-first-turn-from-config`):
`brief.py render` resolves a first user turn from THIS node — the parts list per
role, what each harness adds, the harness block per harness, and the town
trajectory. Adding or removing a part is one line here, never a code change.

It lives in a `config` node rather than `.agi/config.json` on purpose: a round's
own `done` commit refuses `.agi/config.json` by rule (`cli.py:_round_scope_ok`),
so a cell there is absent from the landed branch and a fresh checkout of the
branch cannot render. A config node the round names in `--owns` is committed.

`head` is the HEAD region of `doc:unified-head` (the same bytes for every role);
`card` is `.agi/sessions/quorum/<post>.md`; `harness` is the block named in
`harness_blocks`; `trajectory` is `town:<town>`; `extras` names further node
refs. The sort order is the list order, joined with a blank line.
