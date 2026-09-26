---
id: hypothesis:a-kid-can-commit-the-existing-nodes-its-orders-name
mint_id: 6d4e01667b044ffd9788d4f14c4add85
type: hypothesis
parents:
  - goal:g7.33
next_edges: []
edited_by: director-engine
scaffold_hash: f38d45f8bb44aea4
season: 2
testable_claim: director-engine):cli.py done commits existing node files the round's target or orders name and still refuses every other foreign path, .agi/config.json included.
title: a kid can commit the existing nodes its round's orders name, nothing else (assigned
town: core
---
# hypothesis:a-kid-can-commit-the-existing-nodes-its-orders-name


# hypothesis:a-kid-can-commit-the-existing-nodes-its-orders-name

## Measured
- thought-master TMM.212 item 1: `cli.py done` commits only the kid's OWN node ("leaving N foreign path(s) uncommitted", cli.py:2224), so a kid ordered to "correct in place" an EXISTING node cannot land that edit; DT carried 4 such edits by hand (a00-6cbe5da1, a00-7a3bd2b1, a00-faa1fb92, hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot).
- director-engine gen 23 hit the same class on every harvest: DH.373/374/377/379/382 each left the round's own hypothesis node uncommitted in the parent worktree.
- `.agi/config.json` is refused by design (cli.py:2094 `_round_scope_ok`) and STAYS refused -- out of scope here.

## CLAIM
`cli.py done` also commits an existing node file that the round's orders or target NAME (the round's target hypothesis always; any node id listed in the orders), and still refuses every other foreign path by name, `.agi/config.json` included.

## Dispatch line
config-max: none / template-max: none / code: cli.py's done-scope check reads the round's named node set (target + ids in the orders file / manifest) as allowed paths.

## FALSIFIERS
1. A fixture round whose orders name `hypothesis:x`: an edit to nodes/hypothesis/x.md is still left uncommitted.
2. An edit to a node the orders do NOT name, or to `.agi/config.json`, is committed.
3. test_cli*.py regresses.

## TESTS
extensions/agi/tests/test_cli*.py (the done / _round_scope_ok neighbourhood).

## FILE SCOPE
extensions/agi/bin/cli.py (done's scope check only), its tests, this node + its experiment.

## CEILING
1-2 kids · ~25 production lines · pi-free · 0 USD.
