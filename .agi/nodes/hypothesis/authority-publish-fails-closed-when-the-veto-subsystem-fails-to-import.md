---
id: hypothesis:authority-publish-fails-closed-when-the-veto-subsystem-fails-to-import
mint_id: 6413637826fc4e17ab0c2df360d2b8a1
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: belam
scaffold_hash: 7e496e8220ae53ae
season: 2
testable_claim: "rotate.py's authority publish proceeds past the veto gate only when the seatsig package itself is absent; an ImportError raised from inside an installed seatsig/veto module stops the publish with a named 'authority: HELD' refusal; a committed fixture test distinguishes the absent package from a broken one."
thought_session: belam-S2-L5-VI
title: "the authority publish fails closed when an installed veto module fails to import (assigned: director-engine)"
town: core
---
# hypothesis:authority-publish-fails-closed-when-the-veto-subsystem-fails-to-import

Source: PASS 6 chunk 1, round authority-publish-fails-closed-on-an-unreadable-veto-cell -- final DEMOTE by the verifier: "the production gate nevertheless remains fail-open on ImportError from an installed-but-broken veto subsystem, and the committed absence control test does not distinguish that case". PASS 5 named the same arm (hypothesis:pass5-0925-residue-batch, defect row 1); DH.304 closed the unreadable-cell half only. Runs: .agi/sessions/workflows/runs/mur-p6chunk1of2/{review,verify}_authority-publish-fails-closed-on-an-unreadable-veto-cell.json.

## Measured
- extensions/agi/bin/rotate.py:10437-10444: `from seatsig import veto`, `_veto.read(..., strict=True)` and `_veto.is_frozen(...)` sit in ONE try whose `except ImportError: pass` ("veto subsystem is not installed on this host") also swallows an ImportError raised INSIDE an installed seatsig/veto module -- the publish then proceeds.

## CLAIM
rotate.py's authority publish proceeds past the veto gate only when the seatsig package itself is absent; an ImportError raised from inside an installed seatsig/veto module stops the publish with a named `authority: HELD` refusal; a committed fixture test distinguishes the absent package from a broken one.

## Dispatch line
config-max: none / template-max: none / code: narrow the arm to the absent-package case (ModuleNotFoundError naming seatsig or seatsig.veto); every other ImportError is HELD by name.

## FALSIFIERS
A fixture whose installed veto module raises ImportError on import (or inside read) publishes, or exits 0.

## TESTS
extensions/agi/tests/test_rotate_key_authority.py + the seatsig veto tests (fixtures only; never a real publish).

## FILE SCOPE
extensions/agi/bin/rotate.py (the veto gate of the authority publish) · its tests · this node + its experiment.

## CEILING
one parent, <= 2 kids, pi-free · 10-12 production lines per conjunct · USD cap 1.

## Agent Notes
assigned: director-engine (PASS 6 residue, belam-S2-L5-VI 09-25)
