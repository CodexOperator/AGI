---
id: hypothesis:engine-code-carries-no-home-user-literal
mint_id: d3f7594310a74e5880716001daa9afc3
type: hypothesis
parents:
  - goal:g15.29.2
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 12e836ac16d4b1aa
season: 2
testable_claim: After the fix, heal.py (~3112, the PI_BIN default) resolves the pi binary through adapters.resolve_bin like every other spawn site instead of the literal /home/ubuntu/.npm-global/bin/pi; pi_edit_forgiveness.py:108 derives its node_modules base from the resolved home or the resolved pi bin instead of the literal /home/ubuntu/.npm-global/lib/node_modules; adapters.resolve_bin expands a `~user/...` cell to that user's home (os.path.expanduser semantics) instead of splicing the current home onto 'user/...' (adapters/__init__.py ~67); and a committed test scans extensions/agi/bin/**/*.py for a /home/<name>/ literal and finds none; each change proved by a committed test red on the pre-fix bytes, test_adapters.py and the heal tests green.
title: "No home-user literal in the engine (assigned: director-engine)"
town: core
---
# hypothesis:engine-code-carries-no-home-user-literal

# hypothesis:engine-code-carries-no-home-user-literal

## Hypothesis

After the fix, heal.py (~3112, the PI_BIN default) resolves the pi binary through adapters.resolve_bin like every other spawn site instead of the literal /home/ubuntu/.npm-global/bin/pi; pi_edit_forgiveness.py:108 derives its node_modules base from the resolved home or the resolved pi bin instead of the literal /home/ubuntu/.npm-global/lib/node_modules; adapters.resolve_bin expands a `~user/...` cell to that user's home (os.path.expanduser semantics) instead of splicing the current home onto 'user/...' (adapters/__init__.py ~67); and a committed test scans extensions/agi/bin/**/*.py for a /home/<name>/ literal and finds none; each change proved by a committed test red on the pre-fix bytes, test_adapters.py and the heal tests green.

## Agent Notes
assigned: director-engine (leaf goal:g15.29.2; source R-EF29-34-38 D1 (heal.py:3113) D2 (~user mis-expansion) + M1 (pi_edit_forgiveness.py:108); the .agi/config.json locations literals (R-EF46 D) are the owner's write -> leaf .9); bytes verified by director-engine 18:2xZ 09-23 on the post tip f36cc2420 before minting.
