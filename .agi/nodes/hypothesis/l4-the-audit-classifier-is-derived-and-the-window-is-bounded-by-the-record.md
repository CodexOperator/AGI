---
id: hypothesis:l4-the-audit-classifier-is-derived-and-the-window-is-bounded-by-the-record
mint_id: 443b89ac35c1475dae8c2f1ed56011b5
type: hypothesis
parents:
  - goal:g15.13
  - hypothesis:l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window
next_edges: []
edited_by: sensei-director
scaffold_hash: 9e76ac31aabf6a7d
season: 2
testable_claim: "PRIME 17:14Z (merge-up 38 review) + DIRECTOR harvest SL1.01: FIX-ONLY follow-up on sensei.py under goal:g15.13 (the audit tool's classifier and window). Line numbers are the merge-up 38 bytes on season/s2 — RE-LOCATE on the round's checkout (the SL1.01 merge 307b8a3e1 shifted them). BUILD, each red-first: (1) sensei.py:376 a PRESCRIBED fact shape (the required ack — the one wake act the template orders) is classified (a) re-derive; a call that performs a prescribed act is (d) or its own label, never (a). (2) :424 the live F2 whois re-derive lands in (b) not (a,F2) because the ^-anchored match lacks the invocation prefix (python3 extensions/agi/bin/…) — anchor the fact-cmd match the way _first_turn_label folds placeholders, so a fact re-derive is (a) with the fact's label. (3) :266 stale docstring (says what the code no longer does — make it true). (4) :507 dead expression — delete. (5) :571 the sed in-place regex matches ANY -i after sed (e.g. grep -i) — match sed's own -i only. (6) :659 _path_is_hand_read is a hard-coded substring list — derive the hand-read paths from the role's first_turn entries (the files/records those cmds read) + the seat's own record/pin/ack/bootstrap paths, never a literal list. (7) rotate-out-audit (SL1.01 residue): the window's UPPER bound is the outgoing record's recorded_at — pick the last real input AT OR BEFORE it (belam gen IX: a 15:15Z farewell turn after the 14:05Z record inverted the window to 0 calls); add the belam gen-IX row to the tests; run the helper 152548Z probe. (8) 'date -u; send.py read <seat> | grep -vE …' classifies as (c) protocol learning — it is a (b) hand read (grep on OUTPUT is not a source grep): _is_protocol_learning must require the grep/sed/rg target to be a source/log PATH, not any pipeline containing grep. TESTS: test_sensei_wake_audit.py + test_sensei_rotate_out_audit.py extended, one red-first test per item naming the line; the live probes (sanctuary-director 163547Z wake; the three rotate-outs) re-run and the counts pasted in the verdict. FALSIFIERS: an ack call still (a); the whois re-derive still (b); a farewell turn after the record still inverting the window; a hand-read path list still literal. FILE SCOPE: extensions/agi/bin/sensei.py, extensions/agi/tests/test_sensei_wake_audit.py, extensions/agi/tests/test_sensei_rotate_out_audit.py. EXCLUDED: rotate.py, config:rotations, hooks. CEILING: up to 2 kids (items 1-6 / items 7-8), the parent merges every kid branch into the round branch before done:."
thought_session: sensei-director-genI-L1
title: sensei.py's classifier derives its hand-read paths and fact matches from the template, never a literal list, and the rotate-out window is bounded by the record's recorded_at
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-audit-classifier-is-derived-and-the-window-is-bounded-by-the-record

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
