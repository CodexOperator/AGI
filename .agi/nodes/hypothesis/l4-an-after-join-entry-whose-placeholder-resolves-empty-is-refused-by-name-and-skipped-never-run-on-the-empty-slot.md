---
id: hypothesis:l4-an-after-join-entry-whose-placeholder-resolves-empty-is-refused-by-name-and-skipped-never-run-on-the-empty-slot
mint_id: 2dd2fb74b0cc431c8dff431ac84f0edc
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 9535d05818cc2679
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (Prime XVI dm 16:10Z line (1) + master-sensei gen 4 dm 16:12Z line (2), both measured on the first two LIVE after_join dms after the reaper restart 16:09Z onto SL7.54 bytes; cite at seat tip 1dc9f96b2, re-measure on your base). MEASURED: the template's reap-proof entry is `ps -e -o pid=,ppid=,tty=,args= | grep -E '{pred_pids}'` (config:rotations frontmatter, rotations.md:69 and :111); `_run_after_join_command` (rotate.py:9261) resolves it with `_resolve_startup_placeholders(cmd, values, refuse_empty=False)` (:9276) — the first_turn path refuses an EMPTY used placeholder by name (`placeholder {key} empty at spawn`, :8685-8689) but the after_join path does not, so a MAIN post with no chain (belam: {pred_pids} = '') ran `grep -E ''`, matched every line, and 40 KB of process table went into the record and the dm (the per-command cap DEFAULT_STARTUP_BYTE_CAP 4000, :7884, truncated it — a truncated ps table is still a wrong output, not a refusal); the docstring at :8922-8925 already promises 'an EMPTY pred_pids is the L4.179 named refusal' for a real rotation. CLAIM: (a) `_run_after_join_command` refuses an entry that USES a placeholder whose value is empty: the result is `{label, cmd, refused: 'placeholder {pred_pids} empty: no predecessor chain — skipped by name'}` (the refusal names the placeholder AND the reason, mapped per placeholder: pred_pids → no predecessor chain, succ_ref → row session_ref empty, gen → no generation resolved), nothing is executed, and the dm prints `[reap-proof] REFUSED` + that line through the existing refused branch of `_compose_after_join_dm`; (b) this is generic to every after_join entry, not a reap-proof special case — the ack entry with {succ_ref} empty is refused the same way (the sibling node on gen/ref decides how they are RESOLVED; this node decides that an unresolved empty slot never runs); (c) a first seating's named value 'none: first seating' (:8960) is a non-empty string and still runs (its grep matches nothing, exit 1 — expected, not a refusal). FALSIFIERS: an empty {pred_pids} still produces a command with an empty grep pattern or any executed command; the refusal is missing from the record's results or from the dm; a non-empty pred_pids is refused; the first-seating value is refused. TESTS: test_after_join_service.py — empty pred_pids → refused entry (no rc, no output) and the dm carries REFUSED + the placeholder name; non-empty pred_pids runs; the first-seating value runs; empty succ_ref on the ack entry is refused by name. FILE SCOPE: extensions/agi/bin/rotate.py `_run_after_join_command` (:9261-9305) only; extensions/agi/tests/test_after_join_service.py. EXCLUDED: `_resolve_startup_placeholders` itself and its first_turn callers; `run_after_join_for_seat` and `_first_turn_values` (the gen/ref sibling); `_compose_after_join_dm` (the gen/ref sibling); the templates (rotations.md is owner/prime-written); the tail and liveness (SL7.72 in flight); the catch-up loop (the dead-seat sibling); the sender (the signing sibling). CEILING: one flag flip + one per-placeholder refusal map, four tests."
thought_session: sensei-director-genXIV-L14
title: an after_join entry whose placeholder resolves EMPTY is refused by name and skipped — reap-proof never runs grep -E '' over the whole process table on a MAIN post with no predecessor chain
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-an-after-join-entry-whose-placeholder-resolves-empty-is-refused-by-name-and-skipped-never-run-on-the-empty-slot

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
