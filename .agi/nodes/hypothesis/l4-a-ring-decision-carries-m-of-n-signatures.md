---
id: hypothesis:l4-a-ring-decision-carries-m-of-n-signatures
mint_id: 126d784390b44bf58c596c0028e715f9
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 604628cc33a6a05e
season: 2
testable_claim: "OWNER 2026-09-11 20:3x-21:4xZ (the eight rungs, verbatim in doc:l4-owner-decisions; vision:web-app-suite db436e1f1: 'Rungs 1-4 are live as goal lines under goal:g15 at the Sanctuary director'). Proposed by sanctuary-director 214458Z 01:33Z, ACCEPTED by Prime XIII 01:33Z: 'mint the three hypothesis nodes now (parents goal:g15, town all) but do NOT dispatch until rung 1's F1-F4 land at the sensei-director (rung 2 sits behind enforcing)'. HELD -- not dispatched. RUNG 2, owner verbatim: 'Multisig rings. m-of-n plain signatures on ring and decision records; the gates (dispatch, merge-up, the write guard) verify a quorum.' CLAIM: (1) a ring is a config row (`rings:` in config:posts or a sibling geometry node -- the Prime's cell) naming its members' post keys and its threshold m; (2) a decision record (a merge-up grant, a spawn over the budget, a config:posts row edit outside self_row) carries a `signatures:` list of `<post>:<sig_scheme>:<sig>` over the record's canonical bytes (rung 1's injective canonical form, ONE registry, the verify-side vector -- the gate for this rung); (3) the three gates -- dispatch.py (a round the ring must approve), the merge-up recipe (`verification.py --suite` refuses a merge whose grant record lacks m valid signatures), write.py `_enforce_written_by` (a non-self-row config write needs the ring's quorum) -- verify m-of-n through the SAME Verifier interface as `send.py` (seatsig), never their own crypto; a record short of m is REFUSED by name with the count; (4) tests on fixture keys: m-of-n satisfied / one short / one forged (rung-1 FORGED label) / a member outside the ring; (5) nothing changes for a record type no ring names (rings are opt-in per gate). Ceiling and file scope are set when the round is cut; serial behind rung-1 enforcing."
title: "RUNG 2 (held): multisig rings -- m-of-n plain signatures on ring and decision records; dispatch, merge-up and the write guard verify a quorum"
town: all
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-ring-decision-carries-m-of-n-signatures

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
