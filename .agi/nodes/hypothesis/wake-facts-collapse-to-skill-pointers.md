---
id: hypothesis:wake-facts-collapse-to-skill-pointers
mint_id: 2a67da86c6424979801d44473a0484a0
type: hypothesis
parents:
  - goal:g4.18.2
next_edges: []
edited_by: belam
scaffold_hash: 1bd0bc68051b4ea8
season: 2
testable_claim: config:rotations facts region = one pointer line per F-number to skills/agi-*/SKILL.md, <= 2000 bytes (from 7164), first_turn range re-derived, pinned rotate tests updated in the same commit, suite green; rotate.py DEFAULT_CC_ROLES carries no ultracode
title: "The wake facts collapse to skill pointers under 2000 bytes, tests re-pinned in the same commit (assigned: director-engine)"
town: core
---
# hypothesis:wake-facts-collapse-to-skill-pointers

# hypothesis: the wake facts collapse to skill pointers (assigned: director-engine)

## Why this exists
**Parent `goal:g4.18.2`** (owner 01:1xZ 09-27: "a lot of your And other posts card f rules go into those and everyone's card just lists all the relevant skills"). The Prime landed eight flow skills (`skills/agi-*/SKILL.md`, build nodes `build:skills-agi-*-SKILL.md`) that now carry every F-rule the `config:rotations` facts block prints at each wake. The facts block itself was NOT trimmed by the Prime because it is an engine contract pinned by tests:
- `test_rotate_templates.py:387-450` resolves the wake-read region from the templates' own `facts` first_turn cmd (`read body 37:64`, `rotations.md:76` + `:114`) and `:534` asserts the live region still holds a hand-vocab hit (F16);
- a 7200-byte guard on the region (rotations.md steps note, 09-25);
- ten rotate test files read `config:rotations`, and rotate test files are never run from a post's pane.

## Testable claim
The facts region becomes one line per live F-number of the form `F<n> -> skill agi-<flow> (§<k>)` (plus any fact no skill carries, verbatim), the `facts` first_turn cmd's range is re-derived to match, the pinned tests are updated to the new contract in the same commit, and the region measures <= 2000 bytes (from 7164 at 01:0xZ 09-27) with the full suite green.

## Also (same round, one line each)
- `rotate.py:120` DEFAULT_CC_ROLES still carries `"settings": {"ultracode": True}` (and `effort: max`) for prime_director; the owner dropped ultracode from everyone and set effort high (c72b01fb5). Fallback only, but it contradicts the rows.

## Falsifier
1. `write.py config:rotations 'read body <new range>' | wc -c` <= 2000 AND every F-number cited in `extensions/agi/briefs/*.md` resolves either in the region or in a `skills/agi-*/SKILL.md`.
2. `git grep -n '"ultracode": True' -- extensions/agi/bin/rotate.py` = 0 hits.

## Agent Notes
2026-09-27 04:1xZ belam: DRAFT HELD BY THE DIRECTOR (owner 04:1xZ: it should be referenced) = loop branch season2/loops/hypothesis-wake-facts-collapse-t-a00-759e6b60 @3fb4c6199 (kid a00-759e6b60, DH.501, worktree .agi/worktrees/a00-759e6b60). The Prime's ONE config:rotations write takes the facts region from that branch (TMM.281 route: config:rotations facts are prime/owner-only); DE's red-first test lands after it.
