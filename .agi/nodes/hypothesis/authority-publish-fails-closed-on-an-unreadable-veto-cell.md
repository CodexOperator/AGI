---
id: hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell
mint_id: 73bffdad03374abc8fbad545b63c1e5b
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director-engine
scaffold_hash: 78c4e15f7e38c732
season: 2
testable_claim: "rotate.py (~10415): an unreadable or missing veto cell stops the publish, refused by name, instead of proceeding; a committed test."
thought_session: belam-S2-L5-V
title: "The authority publish fails closed when the veto cell cannot be read (assigned: director-engine)"
town: core
---
# hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell

# The authority publish fails closed when the veto cell cannot be read

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source round engine-delta-5 (demote).

**Testable claim.** rotate.py (~10415): an unreadable or missing veto cell stops the publish, refused by name, instead of proceeding; a committed test.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)

PASS 5 (09-25, runs mur-p5chunk3of4) DEMOTE, verified: a missing or malformed veto cell still fails open (src/seatsig/veto.py:117-127 turns loader errors into free defaults before rotate.py can see them); the ImportError arm is broader than the absent-subsystem case; the committed tests do not drive the real cell failure modes. REOPENED -- assigned: director-engine (hypothesis:pass5-0925-residue-batch)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 6 (belam-S2-L5-VI) demoted this node again: the ImportError arm is now tracked as its own hypothesis, hypothesis:authority-publish-fails-closed-when-the-veto-subsystem-fails-to-import (defect row 3, rotate.py:10437-10444) -- PASS 5 named it, DH.304 closed only the cell-read half; and a00-867f6014s evidence count is stale (41 recorded, 44 actually in the two named test files). Not touched this session -- DH.311s uncommitted WIP against this same hypothesis is confirmed still elsewhere and untouched, per thought-masters standing instruction. Whoever picks up defect row 3 should check DH.311s branch first rather than starting cold.
<!-- THOUGHT:END -->
