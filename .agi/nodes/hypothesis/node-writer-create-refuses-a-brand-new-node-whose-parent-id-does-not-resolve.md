---
id: hypothesis:node-writer-create-refuses-a-brand-new-node-whose-parent-id-does-not-resolve
mint_id: 6eb909e2ca1541c498689e50743c1fe9
type: hypothesis
parents:
  - goal:g7.33
next_edges: []
confidence: 0.85
edited_by: director-engine
scaffold_hash: ac990a45c78befca
season: 2
testable_claim: write.py create <type> <slug> --parent <id> is REJECTED, no file written, when <id> resolves to no node -- mirroring the existing no-active-schema-for-type branch at node_writer.py:703-709 -- while a pre-existing file with an already-unresolved parent stays UNVERIFIED/fail-open per G7.1
title: A brand-new node_writer.py create refuses a parent id that resolves to no node
town: core
---
# hypothesis:node-writer-create-refuses-a-brand-new-node-whose-parent-id-does-not-resolve

## Measured
- node_writer.py:689-702 (comment) + :703-709 (code): a fail-open exception already exists,
  carved out for CREATE-only, no-active-schema-for-type (hypothesis:l4-create-refuses-a-
  genuinely-unknown-type-before-any-file-is-written, landed) -- proving the "REJECTED instead
  of UNVERIFIED, for a brand-new create only" shape already exists and already works for one
  UNVERIFIED cause.
- spawn_gate.py:1092: `res.reason = f"parent id(s) resolve to no node: {unresolved}"` is the
  OTHER UNVERIFIED cause the module's own docstring (spawn_gate.py:48-52) names as fail-OPEN by
  design: "a parent id that resolves to no node ... Fail OPEN: warn, allow, stamp."
- Real, measured harm from this exact gap, today: 3 swarm parents (DH.364/365/366, room
  swarm-g73314, goal:g7.33.14) each ran `write.py create hypothesis <slug> --parent
  goal:<intended-subgoal-id>` against a subgoal id none of them had actually committed yet --
  each meant to mint its own subgoal first, but the mint never landed on any of the 3 branches
  (3 different intended ids, 0 of 3 exist anywhere in the merged tree, confirmed by grep, not
  assumed). All 9 kid `create` calls SUCCEEDED anyway, minting 9 real nodes with a
  `parents:`/`loop:` pointing at nothing. Fixed by hand this session (commit fb2e0ca6ec,
  director-engine) by re-pointing all 9 to the real existing ancestor goal:g7.33.14 -- a repair
  that was only possible because a human-directed session happened to read the INTEGRITY
  warnings `snapshot-goals.py --render` prints (it does not fail the check on them); an
  unattended loop would not have caught it.

## CLAIM
`write.py create <type> <slug> --parent <id>` REFUSES (REJECTED, no file, no directory -- the
same shape as the `not gate.ok` branch) when `<id>` resolves to no node in the index, for a
brand-new create specifically. A pre-existing file whose CURRENT parent already fails to resolve
(e.g. an old node predating a renumbering) is UNCHANGED by this -- that path still reads
UNVERIFIED and fails open, exactly as G7.1 requires: never invent a missing edge on something
already alive. This mirrors the shape node_writer.py:703-709 already uses for the
no-active-schema-for-type cause; it does not touch that branch.

## Dispatch line
code: node_writer.py's create path gains a second discriminator beside the existing
no-active-schema-for-type branch at ~line 703: `gate.status == spawn_gate.UNVERIFIED and
gate.reason.startswith("parent id(s) resolve to no node") and not node_file.exists()` ->
REJECTED, same shape as the existing branch. No config cell, no template -- a resolver branch
that does not exist yet, added beside one that already does.

## FALSIFIERS
1. `write.py create hypothesis <fresh-slug> --parent goal:this-id-does-not-exist-anywhere`
   exits non-zero, writes no file, and the reason names the unresolved id.
2. A node that already exists with an unresolved parent (planted by a test fixture, never by
   this code) and is later re-written by some verb OTHER than `create` is untouched -- only the
   create path gains the new branch; UNVERIFIED-fail-open is unchanged for every other reader.
3. `hypothesis:l4-create-refuses-a-genuinely-unknown-type-before-any-file-is-written`'s own
   tests still pass unchanged -- this is an ADDITIONAL discriminator, not a replacement of it.
4. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/ -q` still passes in full.

## TESTS
Whichever committed test file already covers the no-active-schema-for-type branch (check
test_node_writer.py and test_spawn_gate.py first) -- mirror its fixture shape for the new
branch rather than inventing a new file if one of these already exists and fits.

## FILE SCOPE
extensions/agi/bin/node_writer.py (the new branch), extensions/agi/bin/spawn_gate.py (read
only -- the UNVERIFIED reason string already lives there, unchanged), and whichever test file
FILE SCOPE / TESTS above resolves to. Nothing else.

## CEILING
1 kid · ~10-12 production lines (one new discriminator branch, mirroring the existing one
almost verbatim) · pi-free · 0 USD.
