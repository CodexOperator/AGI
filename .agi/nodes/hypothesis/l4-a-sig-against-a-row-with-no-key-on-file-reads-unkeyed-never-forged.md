---
id: hypothesis:l4-a-sig-against-a-row-with-no-key-on-file-reads-unkeyed-never-forged
mint_id: dd9fb0938b4549c6a59ea73bc3360a22
type: hypothesis
parents:
  - goal:g15.26
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: a4ea2a7c88917929
season: 2
testable_claim: "goal:g15.26 fix-only (gate on the VALUE flip) — A SIG AGAINST A ROW WITH NO KEY ON FILE READS UNKEYED, NEVER FORGED (Prime XIII ask (b), 00:16Z grant dm, measured live on the sensei-director SL2#10 dm which read FORGED on MAIN; re-measured by sensei-director gen VI on seat tip 692dbec5c). MEASURED: send.py _label_for_sig (2036) LIVE path 2069-2073 — row_scheme = row.get('sig_scheme'), row_pub = row.get('pubkey'); if either is empty it returns the bare label FORGED, the same label a bad signature against a NAMED key returns (2075/2079/2081). _verify_block (2085) documents that a row with no pubkey/sig_scheme is FORGED (2092-2094). Under comms.verify == enforcing, read/peek (2265-2275) withhold a block whose label is EXACTLY FORGED into inbox/quarantine, and whois --sig (3023-3046) prints REFUSED FORGED. Consequence: fleet-wide 0 pubkey cells on MAIN until SL2#10 (now 1, sensei-director), and every freshly rotated worktree post's row is unkeyed on MAIN until its merge-up (SL6.01 fixes the write; the label stays wrong for any unkeyed row) — so flipping enforcing today would WITHHOLD every signed dm from an unkeyed sender at the one moment the channel matters. CLAIM: (1) _label_for_sig returns the label UNKEYED <seat> when the from-seat's row names NO pubkey or NO sig_scheme (2069-2073) — FORGED is reserved for a signature that fails against a key the row NAMES (scheme mismatch, bad hex, verify false) or a malformed/unknown-sender sig, nothing else; (2) _verify_block's docstring and every reader that switches on the label (read/peek enforcing withhold 2265-2275, whois --sig 3023-3046, the label regex at 2142) treat UNKEYED like UNSIGNED — printed in full, never withheld, never REFUSED — under BOTH informational and enforcing; (3) the RETIRED path (2057-2067) is unchanged: a key_history hit still reads RETIRED:<fp> before the live path is consulted. FALSIFIERS: a signed block from a row with pubkey empty reads FORGED; the same block under enforcing is withheld or REFUSED; a signed block from a row that NAMES a pubkey but whose sig does not verify reads anything but FORGED; a scheme the row does not name reads UNKEYED (it must stay FORGED — the row NAMES a key); whois --sig on an unkeyed row prints REFUSED. TESTS: test_send.py (grep _label_for_sig / _verify_block / test_forged / test_enforcing for the existing cases) + test_seatsig.py; one test per label under both verify values; fixture rows only, never the live seats.md. Neighbourhood: send (test_send.py test_seatsig.py test_sensei.py test_heal.py test_bin_help_smoke.py test_write_self_row.py). RULES: merge, never rebase; never lower a guard (FORGED against a NAMED key stays withheld under enforcing); comms.verify VALUE stays informational — this round changes no config node; experiment prose never quotes the literal THOUGHT marker, one THOUGHT region per node. FILE SCOPE: send.py _label_for_sig, _verify_block docstring, the enforcing switch in read/peek, whois --sig, the label regex; tests. EXCLUDED: rotate.py (SL6.01), heal.py (SL6.02), .agi/config.json, config nodes, seatsig package. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genVI-L6
title: a signature against a row that names no key reads UNKEYED (printed in full under enforcing), never FORGED
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-sig-against-a-row-with-no-key-on-file-reads-unkeyed-never-forged

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
