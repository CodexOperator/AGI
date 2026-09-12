---
id: hypothesis:l4-the-meter-telemetry-key-resolves-to-a-measured-fraction-or-a-labelled-estimate-never-blank
mint_id: 2ea3cee9d67b4b43b662c644030f618e
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 57854e9c0b4bdb03
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (master-sensei gen 4 dm 15:56Z relaying owner 15:5xZ (third order; verbatim at doc:l4-owner-decisions); cite at seat tip 92563a7f5, re-measure on your base. — owner: 'each role should have a template that includes what calls are done at wake for it'; the Sensei added 'meter' as a telemetry key to BOTH templates, director and prime_director, at 4bad592ec + fb9e86652, 98 template tests green). MEASURED: every bootstrap block now renders 'SKIPPED: no handover derivation for meter' because _derive_bootstrap_fact (rotate.py:7416) has no 'meter' branch; the pin write in rotate-self precedes the bootstrap write (the Sensei measured :12271 before :12491 at fb9e86652), so at bootstrap time the successor's transcript exists but usually carries no assistant usage yet. CLAIM: the switch gains a 'meter' branch: when the pinned successor transcript has assistant usage, the measured fraction exactly as rotate.py meter prints it ('0.NNNN (tokens/window) line=threshold'); else 'est. N tokens = composed first input bytes/4 (head + brief + STARTUP)' computed from the bytes rotate-self composed for the successor — never blank, never an unlabelled number (P6); if the pre-spawn record cannot know either, the key is marked join-only and filled by _fill_bootstrap_join_facts at the join (SL7.54's seam) — the kid measures which and says so. This is the WAKE half; the per-prompt hook line (hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt, SL7.70) is the between-turn half. FALSIFIERS: a bootstrap block still reads SKIPPED for meter; a fresh spawn prints a bare number without est.; a transcript with usage prints an estimate; the join-only path leaves the pending marker after the join. TESTS: test_rotate_startup.py (or the bootstrap tests) — measured case, est. case, join-only fill. FILE SCOPE: extensions/agi/bin/rotate.py — _derive_bootstrap_fact's switch + the join-fact list if join-only; its test file. EXCLUDED: the templates (already declared), rotate.py meter itself, the hook. CEILING: one branch, three tests."
thought_session: sensei-director-genXIII-L13
title: the 'meter' telemetry key both templates now declare resolves in rotate.py's telemetry switch — the measured fraction from the pinned successor transcript when it has usage, else 'est. N tokens' from the composed first input bytes/4 — never blank, never a confident wrong number; join-only if the pre-spawn record cannot know it
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-meter-telemetry-key-resolves-to-a-measured-fraction-or-a-labelled-estimate-never-blank

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
