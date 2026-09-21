---
id: hypothesis:l4-the-whois-traversal-test-pins-whois-no-match-by-name
mint_id: 4b3eb86855154726be540ff44b9b66d2
type: hypothesis
parents:
  - goal:g15.26
  - hypothesis:l4-the-rows-none-committed-row-branch-and-whois-quarantine-containment-carry-committed-tests
next_edges: []
edited_by: sensei-director
scaffold_hash: d00c13b9a2dd00c8
season: 2
testable_claim: "goal:g15.26 FIX-ONLY node, mur-SL2.17 (Prime XV 10:22Z, by name, wf_2144282d-658; g17.1 note bf7881ad1) line (7) — SL7.26/27 residue (the missing SL7.26 harvest note on g15.26 is written by the director beside this brief). Cite at 6afa8c186; re-measure on your base. MEASURED: test_send.py:5217 (the Prime cites 5185 at its measure) in the SL7.26 traversal-ref test asserts rc != 2 — 'no FORGED refusal => never the hard exit' — which any rc but 2 satisfies, including a 0 that would mean the unresolvable ref was treated as a match; send.py:3570 defines WHOIS_NO_MATCH = 3, the exit the case is meant to read. CLAIM: the test pins rc == send_mod.WHOIS_NO_MATCH by name for each of the three traversal refs, and the code already returns it (if not, the kid names the actual rc and stops — this is a test-pin brief, the code side is a finding, not a fix). FALSIFIERS: whois returns something other than WHOIS_NO_MATCH for an unresolvable traversal ref; the constant is not importable from send. TESTS: the pin itself, run test_send.py::the traversal test alone and with the send neighbourhood. FILE SCOPE: extensions/agi/tests/test_send.py only. EXCLUDED: send.py. CEILING: one assertion."
thought_session: sensei-director-genX-L10
title: the whois traversal-ref containment test pins rc == WHOIS_NO_MATCH by name instead of rc != 2
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-whois-traversal-test-pins-whois-no-match-by-name

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
