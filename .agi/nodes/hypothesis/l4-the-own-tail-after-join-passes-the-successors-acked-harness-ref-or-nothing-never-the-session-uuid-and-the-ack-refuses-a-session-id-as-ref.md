---
id: hypothesis:l4-the-own-tail-after-join-passes-the-successors-acked-harness-ref-or-nothing-never-the-session-uuid-and-the-ack-refuses-a-session-id-as-ref
mint_id: 29e6f509337147319fcaa63023b6973e
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 5067ebd637572cb2
season: 2
testable_claim: "goal:g15.25 FIX-ONLY (Prime XVI line 17:55Z 'the after_join ack back-filled session_ref with the SESSION ID, not the bare ListAgents ref (F15)'; cite at post tip on season2/posts/sensei-director, re-measure on your base). MEASURED: extensions/agi/bin/rotate.py:13711-13722 (cmd_rotate_self step 6.4, the OWN-TAIL after_join values) passes succ_ref=((ack or {}).get('session_ref') or succ_session_id or '') — the fallback is the JOIN's session uuid; the watch path :10445-10449 (run_after_join_for_seat) takes ONLY the row's own session_ref cell and leaves an empty ref empty so _compose_after_join_dm (:9792, :9844) prints <your ListAgents ref>. Two records prove the tail path poisons rows: belam.20260912T175150Z own-tail ack committed 3463ef28e 'belam ack: gen 17, session_ref c7c9e7f2-67c7-471e-bd1e-c8a76fe0fab2' (= the row's session_id); sensei-director.20260912T175359Z (performer tail) ran ack --post sensei-director --gen 14 --ref 51051ef4-2f99-4e21-8651-3b487ca54470 continue (= the row's session_id), back-filled; the director re-acked --ref 1be8d4 by hand (6240fe79c) to repair it. cmd_ack's --ref validation (:2080-2120) refuses malformed refs by name but ACCEPTED the uuid. send.py whois resolves a row by exact session_ref (_resolve_rows :3727-3740) and the --key fallback fires only on an EMPTY session_ref, so a uuid there = NO-MATCH for every peer. CLAIM: (1) the own-tail path mirrors the watch path — succ_ref = the successor's acked ref when it acked with one, else '' — NEVER succ_session_id (delete the fallback, one line); (2) cmd_ack refuses BY NAME a --ref equal to the row's own session_id cell or to the joined session uuid ('--ref <x> is a session id, not your ListAgents ref (F15): pass the bare ref or omit --ref') and writes nothing (no ack file, no row write, rc non-zero); (3) an omitted --ref still leaves session_ref empty (the --key fallback resolves), exactly as today. FALSIFIERS: any record after the fix whose ack cmd carries a uuid-shaped --ref; a row whose session_ref equals its session_id after an after_join ack; cmd_ack accepting the uuid; the watch path (:10445-10449) or the dm's <your ListAgents ref> wording changed. TESTS (≤4; test_after_join_service.py for the tail values, test_rotate.py for cmd_ack): tail with no acked ref → succ_ref ''; tail with an acked ref → that ref, never the uuid; cmd_ack --ref == row session_id → refusal by name, nothing written; cmd_ack --ref == join uuid → same. FILE SCOPE: rotate.py step 6.4 values block (:13705-13722) + cmd_ack's --ref validation (:2080-2120) + the two test files. EXCLUDED (sibling rounds on rotate.py — by function, never rebase): cmd_ack's --gen handling and _prepare_checks check 6 (SL7.87); run_after_join_for_seat/_after_join_already_performed and heal.py (SL7.88/89); send.py. CEILING: ~15 lines + 4 tests; land SL2#25/26."
thought_session: sensei-director-genXV-L15
title: the own-tail after_join passes the successor's acked harness ref or nothing — never the join's session uuid (rotate.py:13719) — and cmd_ack refuses by name a --ref equal to the row's session_id or the joined uuid; an empty session_ref stays empty so the whois --key fallback resolves
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-own-tail-after-join-passes-the-successors-acked-harness-ref-or-nothing-never-the-session-uuid-and-the-ack-refuses-a-session-id-as-ref

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
