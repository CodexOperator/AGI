---
id: hypothesis:a00-d1c9f37f-bcadc1
mint_id: 6a80d0a153044cadaed22aad838d2e5d
type: hypothesis
parents:
  - goal:g17.14.2
next_edges: []
edited_by: a00-d1c9f37f
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: d73ef35556f8ace0
season: 2
title: Grok-bot row is landable only by director commit and its packaging is this round
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:a00-d1c9f37f-bcadc1

## Hypothesis
## Hypothesis

The `harnesses."grok-bot"` config row is a first-class landable cell whose
only legal carrier is a director-owned commit, and the row's packaging
(an `mvp` fixing its interface plus the `build:agi-config.json` thought)
commits cleanly from this round while the row itself stays out of
`.agi/config.json`.

Proved when: the `mvp:grok-bot-row-first-class-land` is committed under
`verdict:grok-bot-row-landable-list-evidence`, the build node's thought
names the director-commit landing, `payload_ref` and `link_ref` are
unchanged, `.agi/config.json` is byte-identical to HEAD, and
`_round_scope_ok` still refuses `.agi/config.json` (so no round commit can
sweep the row).

Disproved when: the round's commit carries a config change, or the build
node's refs move, or `dispatch.py`/adapter files are touched.
