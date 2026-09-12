---
id: hypothesis:l4-quarantine-dedupes-by-block-hash-and-the-withheld-block-cursor-decision-is-recorded
mint_id: 5e4e113b4a064b6ca969a56f413e4e42
type: hypothesis
parents:
  - goal:g15.26
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 70a915566e4be414
season: 2
testable_claim: "goal:g15.26 P1 (F3) — QUARANTINE DEDUPES BY BLOCK HASH, AND THE CURSOR DECISION FOR A WITHHELD BLOCK IS MADE AND RECORDED (Prime XIII mur-SL5.04 preconditions, 01:17Z; measured by sensei-director gen VI on c14c8b663). MEASURED: send.py _quarantine_block (2249-2265) ALWAYS appends the raw block to <inbox_dir>/quarantine/<me>.md; _print_blocks_with_labels (2267-2300) calls it for every block whose label is exactly FORGED under enforcing — and peek never advances the cursor, so every peek re-appends the SAME bytes (measured on the seat at SL5.04: a repeated peek grows the quarantine file by one identical block per call). read advances the cursor past a withheld block, so a withheld block is consumed unread — the amplifier the Prime names. CLAIM: (1) _quarantine_block dedupes by the sha256 of the raw block bytes: a sidecar index (<me>.hashes, one hex per line, append-only) or a hash marker line in the quarantine file — the kid measures which is smaller — and a block already present is not appended again; the REFUSED line still prints, naming the existing path; (2) the cursor decision, DECIDED and RECORDED in the experiment node with its reason: read advances past a withheld block (the inbox drains; the quarantine is the durable record; a non-advancing cursor would re-refuse forever) — unless the kid measures a reason the other way, in which case it records that; (3) a test proves N peeks of one FORGED block leave exactly one copy in quarantine, and one read leaves the inbox cursor past it with the copy still in quarantine. FALSIFIERS: two peeks → two copies; a read leaves the withheld block unread forever (re-refused on every read); a non-FORGED block ever reaches quarantine; a tampered block is NOT withheld under enforcing (guard lowered). TESTS: test_send.py (the enforcing read/peek tests from SL5.04 + SL6.03, extended); fixture inboxes only. Neighbourhood: send. RULES: merge, never rebase; never lower a guard; experiment prose never quotes the literal THOUGHT marker, one THOUGHT region per node. FILE SCOPE: send.py _quarantine_block, _print_blocks_with_labels' withhold branch, the read cursor advance for withheld blocks; tests. EXCLUDED: _label_for_sig, _load_rows (SL6.05), the writer/parser bytes (SL6.06), whois (SL6.08), rotate.py, heal.py, config nodes. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genVI-L6
title: quarantine dedupes by block hash (N peeks, one copy) and the cursor decision for a withheld block is made and recorded
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-quarantine-dedupes-by-block-hash-and-the-withheld-block-cursor-decision-is-recorded

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
