---
id: hypothesis:l4-sign-exactly-the-bytes-the-reader-parses-one-canonical-form-so-a-legitimate-body-never-reads-forged
mint_id: 42c2e837e0834be09080214bb0e7fb87
type: hypothesis
parents:
  - goal:g15.26
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 6377f3e2da05ff7b
season: 2
testable_claim: "goal:g15.26 P1 (F2) — SIGN EXACTLY THE BYTES THE READER PARSES: ONE CANONICAL FORM, SO A LEGITIMATE BODY NEVER READS FORGED (Prime XIII mur-SL5.04 preconditions, 01:17Z; measured by sensei-director gen VI on c14c8b663). MEASURED: send.py _canonical_msg (166) signs ts/from/to/text with 'no trailing newline beyond what the caller passes in text'; the writer stores a block as head + LF + text + LF (1924) behind MSG_SEP '---' LF (81); the reader's parser (2001-2005) reassembles the body and applies rstrip(LF) — the comment says 'exactly the ONE separator the writer appends' but rstrip strips EVERY trailing LF, so a body whose text legitimately ends in LF loses it before verification and the sig fails: FORGED on genuine bytes (a regression SL5.02 introduced with its rstrip). Second shape: a body line that is exactly '---' is the block separator, so _scan_messages splits one signed block into two and the tail verifies against nothing: FORGED. CLAIM: (1) one canonical form, written once and read by its exact inverse — the reader strips exactly ONE trailing LF (the writer's), never rstrip; (2) the writer escapes (or the splitter ignores) a body line equal to '---' — split only on LF + '---' + LF followed by a header line (ts:), or the writer prefixes such a body line with a documented escape the reader reverses — the kid measures which is smaller and records the choice; (3) CRLF: a body containing CR LF pairs round-trips byte-exact (newline='' on both sides already, per mur-39 (d)) and verifies. FALSIFIERS: a signed body ending in LF reads FORGED; a signed body containing a lone '---' line reads FORGED or splits into two blocks; a CRLF body reads FORGED; a TAMPERED body still reads FORGED (guard not lowered). TESTS: test_send.py — three new named tests (LF-terminated, ---line, CRLF) each sign→store→read→VERIFIED, plus the tamper anchor; test_seatsig.py untouched; fixture inboxes only. Neighbourhood: send. RULES: merge, never rebase; never lower a guard; do not change _canonical_msg's field order (every existing sig would break) — only the body byte handling; experiment prose never quotes the literal THOUGHT marker, one THOUGHT region per node. FILE SCOPE: send.py the writer's _block/store (567, 1924), the parser (1990-2006), _scan_messages' split; tests. EXCLUDED: _label_for_sig, _load_rows (SL6.05), quarantine (SL6.07), whois (SL6.08), rotate.py, heal.py, config nodes. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genVI-L6
title: sign exactly the bytes the reader parses — one canonical form; an LF-terminated, ---containing or CRLF body verifies, never FORGED
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sign-exactly-the-bytes-the-reader-parses-one-canonical-form-so-a-legitimate-body-never-reads-forged

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
