---
id: hypothesis:l4-no-gen-0-ack-file-the-stale-ack-prepare-check-names-its-evidence-and-a-continue-ack-at-the-current-gen-is-consumed
mint_id: 16335938b83d4a8c8670d4fe656c7271
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: d20ed5655073ae80
season: 2
testable_claim: "goal:g15.25 FIX-ONLY (Prime XVI 17:55Z 'a gen-0 belam.ack.json written 16:09Z by the after_join service BLOCKED rotate-self (stale ack, cur=16) until removed by hand' + master-sensei belam XVI->XVII audit line (1) 'the spawn-time continue ack is never consumed... the prepare gate refuses stale ack until a hand rm; sanctuary-helper.ack.json (12:11Z) and stream-master.ack.json are queued to hit the same gate'; cite at post tip, re-measure on your base). MEASURED: extensions/agi/bin/rotate.py:11168-11184 _prepare_checks check 6: stale_ack = ack.exists() and gen_after is not None and gen_measured and gen_after != cur_gen; the refusal line is 'stale ack (<seat>.ack.json) <gen_note>' with the hint 'rm <path>' — it names neither the file's gen_after, its answer, its source nor when it was written, so the Prime paid 2 calls to learn it was a gen-0 file. cmd_ack writes gen_after: args.gen (:2162) with no lower bound — a --gen 0 (the stale service ran exactly 'ack --post belam --gen 0 --ref  continue', record belam.20260912T175150Z, rc 2 only because that old code lacked --post) would write a gen-0 ack that check 6 then refuses at the next rotate-out. F19/SL7.06: rotate-self writes the successor's continue ack at spawn with gen_after = the new gen (ack_written_at_spawn on the record), so at that seat's NEXT rotate-out cur_gen == gen_after and check 6 passes today — but nothing states or tests that a continue ack at cur_gen is CONSUMED, and the two queued files are unmeasured (which gate, why). CLAIM: (1) cmd_ack refuses --gen < 1 by name before any write ('--gen 0: a generation is never 0 (SL7.74); the row reads gen N') — no ack file, no row write; (2) check 6's refusal line carries the evidence: 'stale ack (<seat>.ack.json): gen_after=<g> answer=<continue|diff> source=<the file's source field or unknown> written=<file mtime UTC HH:MMZ>, row gen=<cur> — rm <path>'; (3) a continue ack whose gen_after == cur_gen is CONSUMED: check 6 passes and prints 'ack consumed (gen <cur> continue)'; a pending diff ack at cur_gen halts exactly as today; (4) the kid reads sanctuary-helper.ack.json and stream-master.ack.json in MAIN's .agi/sessions/seats/ and states in its node which gate each would hit and why (gen_after vs the row's gen), touching neither file. FALSIFIERS: a gen-0 ack still writable through cmd_ack; a check-6 refusal without gen_after/answer/written; a continue ack at cur_gen refusing; the diff-ack halt semantics changed; check 5 or any other prepare check touched. TESTS (≤4, test_rotate.py prepare-check tests — this file is shared with SL7.86's cmd_ack tests: append, union at harvest): --gen 0 refused with nothing written; stale gen-0 file → the evidence line; continue at cur_gen → consumed line and no refusal; diff at cur_gen → still refused. FILE SCOPE: rotate.py cmd_ack's --gen handling (:2050-2080, :2162) + _prepare_checks check 6 (:11168-11184) + test_rotate.py. EXCLUDED (by function, never rebase): cmd_ack's --ref validation and step 6.4 (SL7.86); run_after_join_for_seat and heal.py (SL7.88/89); the ack file's schema beyond reading its existing fields. CEILING: ~25 lines + 4 tests; land SL2#25/26."
thought_session: sensei-director-genXV-L15
title: cmd_ack refuses --gen < 1 by name; prepare check 6's stale-ack refusal carries gen_after, answer, source and written-time; a continue ack whose gen_after equals the row's gen is CONSUMED (says so), a diff ack halts as today; the two queued ack files are measured, not touched
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-no-gen-0-ack-file-the-stale-ack-prepare-check-names-its-evidence-and-a-continue-ack-at-the-current-gen-is-consumed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
