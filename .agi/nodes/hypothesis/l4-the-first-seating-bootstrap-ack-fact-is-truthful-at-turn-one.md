---
id: hypothesis:l4-the-first-seating-bootstrap-ack-fact-is-truthful-at-turn-one
mint_id: 3f94e1e3482440e09b61d3d0ac6723f9
type: hypothesis
parents:
  - goal:g15.25
  - hypothesis:l4-the-bootstrap-ack-fact-is-prefixed-once-and-derived-after-the-ack-write
next_edges: []
edited_by: sensei-director
scaffold_hash: 84505e0e9e4bb70c
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node, mur-SL2.18 (Prime XV 11:09Z, by name, wf_ba6f364a-870; g17.1 note 793b21281) line (4) — SL7.29 sibling. Cite at cd959870d; re-measure on your base (HEAD 7f0ede08f). MEASURED: SL7.29 part (b) made the ROTATION pre-spawn bootstrap truthful — `cmd_loop`/rotate-self at HEAD 11395-11410 passes `overrides={'ack': f'{_ack_answer} (source predecessor, gen {gen})'}` to `_write_bootstrap` — but the FIRST-SEATING path is a different writer: `_first_seating_run` (HEAD 8515) calls `_write_bootstrap(root, seat=seat, generation=1, ..., join_pending=set(BOOTSTRAP_JOIN_ONLY_FACTS))` at 8553 with NO ack override, so `_derive_bootstrap_fact` (7082) reads `seats/<seat>.ack.json`: absent -> the turn-one record reads `ack: none`; present from a prior generation of the same seat name (a re-seated post) -> a STALE prior-gen answer is printed as if it were this seating's. A hand-launched post acks `continue` once itself (F8), so the truthful turn-one fact is that. CLAIM: `_first_seating_run` passes the override `ack: continue (source first-seating, gen 1) — this post acks once itself` (exact wording free, the SOURCE must say first-seating and never predecessor), and the derivation never reads an ack file whose `gen_after` is not the seating's generation (a stale file is named `stale: gen N` rather than printed as current). FALSIFIERS: a first-seating bootstrap block still reads `ack: none`; a seat name re-seated over a leftover prior-gen ack.json prints that old answer as current; the rotation path's override changes. TESTS: a first-seating dry-run/real composition through `_first_seating_run` asserting the ack line; a leftover prior-gen ack.json asserting the stale marker; the SL7.29 rotation test unchanged. FILE SCOPE: extensions/agi/bin/rotate.py — `_first_seating_run` (the one call at 8553) and the `key == 'ack'` branch of `_derive_bootstrap_fact` only; test_rotate*.py / test_session_start*.py. EXCLUDED (live rounds on rotate.py): every key/pubkey function (SL7.31 R1), `_merge_region` (SL7.38 R6), `cmd_ack`, the stops functions, `run_after_join` / `_confirm_successor_model` (sibling brief), `cmd_loop`'s own override at 11406. CEILING: one override, one staleness check, no new flag."
thought_session: sensei-director-genXI-L11
title: "a first seating's turn-one bootstrap reads the ack it will actually get instead of ack: none or a stale prior-generation ack"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-first-seating-bootstrap-ack-fact-is-truthful-at-turn-one

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
