---
id: experiment:a00-a6059a55-0e8f33
mint_id: f202223e94ef4dc981cc115ebbf7457a
type: experiment
parents:
  - hypothesis:node-writer-create-refuses-a-brand-new-node-whose-parent-id-does-not-resolve
next_edges: []
confidence: 0.88
edited_by: a00-a6059a55
evidence_runs:
  - experiment:a00-a6059a55-0e8f33
loop: hypothesis:node-writer-create-refuses-a-brand-new-node-whose-parent-id-does-not-resolve@s2
model: stealth/space-bunny-alpha
production_lines: 22
profile: balanced
role: kid
scaffold_hash: 384701276ff17a47
season: 2
title: A create onto a parent id that names no node is refused by name; the gate still fails open for the rest
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a6059a55-0e8f33

## What I built

One new discriminator branch in `extensions/agi/bin/node_writer.py`, immediately
after the landed no-active-schema branch, in the same REJECTED shape:

```
gate.status == spawn_gate.UNVERIFIED
and gate.reason.startswith("parent id(s) resolve to no node")
and not node_file.exists()          <- the conjunct that keeps G7.1 intact
```
-> `REJECTED`, reason names the unresolved id and tells the writer to create the
parent first. No config cell, no template, no path added (`node_file` was already
computed at node_writer.py:672 by the l4 round — reused, not re-derived).

## Probes (all real runs, not claims)

| # | probe | result |
|---|-------|--------|
| 1 | `write.py create hypothesis probe-bad --parent goal:g7.33.999` | `rc=2`, reason `parent id(s) resolve to no node: ['goal:g7.33.999']`, **no file written** — the target harm (the DH.364/365/366 9-node swarm) is now impossible at the create path |
| 2 | `write.py create hypothesis probe-ok --parent hypothesis:node-writer-…-does-not-resolve` (a real id) | `rc=0`, APPROVED, written — the refusal does not fire on honest parents |
| 3 | `test_create_onto_an_unresolvable_parent_refuses_before_writing` | REJECTED, gate UNVERIFIED, id named, no file — falsifier 1 |
| 4 | `test_existing_node_with_an_unresolved_parent_is_untouched` | SKIPPED, not rejected, bytes unchanged — falsifier 2 (G7.1 fail-open preserved) |
| 5 | `test_create_of_an_unknown_type_refuses_before_writing` + the other 3 l4 no-active-schema pins | unchanged, pass — falsifier 3 |
| 6 | `pytest extensions/agi/tests/test_node_writer.py -q` | 108 passed |
| 7 | `pytest extensions/agi/tests/test_*.py -q` (whole suite, 25 min) | 6242 passed / 6 failed → after the three fixture repairs below, 0 of mine remain (3 pass in isolation: order artefacts of `test_rotate_latch_sweep` + `test_suite_no_detached_spawn`) |

## The contradiction this round found (and how I read it)

The full suite surfaced an existing landed pin that states the OPPOSITE rule:
`test_town_mint.py::test_phantom_parent_is_unverified_not_refused` — "a phantom
resolves to nothing, so the gate does not hard-refuse" — minting a town onto
`vision:alive` and asserting `rc == 0`. No node in the graph records that test's
name, so the decision is only in the test.

I kept the GATE half of that pin (a phantom is still UNVERIFIED at the gate; the
gate refuses by RESOLVED type, never by a missing one — unchanged) and updated the
WRITER half to the dispatched claim, renaming the test to
`test_phantom_parent_is_unverified_at_the_gate_refused_at_the_create`. This is a
real behaviour flip for any caller that mints a fresh node in the same pass as a
parent it has not written yet (`post_wire.py` writing several nodes in one call is
the shape at risk). I flag it rather than hide it: if the parent disagrees, the fix
is one `or not node_file.exists()`-style carve-out, and the seam to cut is named.

## Fixture repairs (collateral, honest)

Three fixtures created nodes while naming parents that were never seeded — they
only passed because the writer failed open. Seeding the parent is the other half
of the contract:
- `test_node_writer.py::_schema_project` — seeds `goal:g1` (6 tests).
- `test_write_guard.py::project` — seeds `goal:g1` (1 test).
- `test_node_writer.py::test_unverified_reason_survives_yaml_round_trip` — the
  create case is now refused, so the yaml round trip pins the refusal's reason
  instead of a written stamp; same corpus (`: ` and quotes), same `safe_load`.

## Evidence

```
$ python3 extensions/agi/bin/write.py create hypothesis probe-bad --parent goal:g7.33.999
-- SPAWN-GATE UNVERIFIED hypothesis:probe-bad — parent(s) ['goal:g7.33.999'] name no node in the corpus …
ERR: spawn rejected for hypothesis:probe-bad: parent id(s) resolve to no node: ['goal:g7.33.999']: a new
  hypothesis node cannot be created onto a parent that names no node. Create the parent first, or pass a
  parent id that exists in the graph.. Fix:  (--no-spawn-gate bypasses this, loudly.)
rc=2          # and no file appeared under .agi/nodes/hypothesis/
```

production_lines (git diff --numstat, node_writer.py): **22** (ceiling 40).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The gate stays fail-open; only the brand-new create is refused — that is the whole difference between conjunct A and conjunct B.
<!-- THOUGHT:END -->

## Agent Notes
create onto an unresolvable parent id is REJECTED by name (no file); existing nodes with phantom parents still fail open; 22 prod lines; three fixtures seeded; town_mint phantom pin flipped to the new contract and flagged
