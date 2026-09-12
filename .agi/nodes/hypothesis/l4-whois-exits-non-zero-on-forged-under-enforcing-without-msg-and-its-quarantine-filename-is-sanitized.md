---
id: hypothesis:l4-whois-exits-non-zero-on-forged-under-enforcing-without-msg-and-its-quarantine-filename-is-sanitized
mint_id: dc77e4496fd4452099fd533ef04cde93
type: hypothesis
parents:
  - goal:g15.26
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: ea93d6c82df8798e
season: 2
testable_claim: "goal:g15.26 P1 (F4) — WHOIS EXITS NON-ZERO ON A FORGED LABEL UNDER ENFORCING EVEN WITHOUT --MSG, AND THE WHOIS QUARANTINE FILENAME IS SANITIZED (Prime XIII mur-SL5.04 preconditions, 01:17Z; measured by sensei-director gen VI on c14c8b663). MEASURED: send.py whois (3090+): clause (3) refuses with WHOIS_NOT_AUTHORIZED only when the label is exactly FORGED AND a --msg was handed to withhold; its docstring (line ~18 of the function) says an absent --msg 'returns today's bytes and exit' 0 — so under enforcing a FORGED --sig with no --msg answers the authority question with exit 0, the clause-3 deviation. _quarantine_whois (3006-3020) writes qdir / f'{session_ref}.md' straight from the unvalidated CLI session_ref — a ref like ../../x or a path with separators writes outside the quarantine dir. CLAIM: (1) under enforcing, a label exactly FORGED returns WHOIS_NOT_AUTHORIZED (exit 2, the same code the --msg path uses) with the REFUSED FORGED line even when --msg is absent (nothing to quarantine; the refusal names 'no --msg to withhold'); informational verify keeps today's exit; (2) _quarantine_whois derives its filename from a sanitized ref — only [A-Za-z0-9._-] kept, empty or all-stripped → 'invalid-ref', and the raw ref is written INSIDE the record's first line — so no CLI value can choose a path; (3) tests for both under enforcing and informational, plus a traversal-shaped ref that lands inside quarantine/. FALSIFIERS: FORGED + enforcing + no --msg exits 0; a ref containing '/' or '..' writes outside <inbox_dir>/quarantine; VERIFIED/UNSIGNED/RETIRED/UNKEYED labels change exit code (guard lowered the other way); the --msg path's behaviour changes. TESTS: test_send.py whois tests (SL5.04's clause-3 tests, extended); fixture rows only. Neighbourhood: send. RULES: merge, never rebase; never lower a guard; experiment prose never quotes the literal THOUGHT marker, one THOUGHT region per node. FILE SCOPE: send.py whois (the enforcing branch), _whois_enforced_refusal, _quarantine_whois; tests. EXCLUDED: _label_for_sig, _load_rows (SL6.05), the writer/parser (SL6.06), _quarantine_block (SL6.07), rotate.py, heal.py, config nodes. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genVI-L6
title: whois exits non-zero on a FORGED label under enforcing even without --msg, and its quarantine filename is sanitized
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-whois-exits-non-zero-on-forged-under-enforcing-without-msg-and-its-quarantine-filename-is-sanitized

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
