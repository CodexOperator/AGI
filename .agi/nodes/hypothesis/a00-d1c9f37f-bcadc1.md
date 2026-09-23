---
id: hypothesis:a00-d1c9f37f-bcadc1
mint_id: 6a80d0a153044cadaed22aad838d2e5d
type: hypothesis
parents:
  - goal:g7.25.2
next_edges: []
edited_by: belam
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: d73ef35556f8ace0
season: 2
testable_claim: "(1) The harnesses.grok-bot config row is a first-class landable cell: resolve(cfg,\"grok-bot\") returns (\"grok-bot\", row) with adapter==\"grok_bot\" (explicitly or via the dash-to-underscore default) and every existing harness (pi, pi-local, claude-code, copilot-cli) still resolves unchanged. (2) The row's only legal carrier is a director-owned commit: cli.py's _round_scope_ok returns False for .agi/config.json, so no kid/parent round commit can carry it, and the packaging (mvp + build:agi-config.json thought) commits cleanly while config stays byte-identical to HEAD. (3) Merge-up must not discard the row: the canonical landing on helper commit 76d141786 survives a clean `git merge-tree --write-tree HEAD 76d141786` with harnesses.grok-bot intact; a merge-up that drops it re-breaks resolve with AdapterError. dispatch.py and all adapter files stay untouched."
thought_session: parent-residue-g14-g17-remap
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
