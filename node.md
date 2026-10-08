---
id: hypothesis:l4-the-sensei-record-selector-refuses-ambiguous-stamps-by-name-and-latest-passes-the-session-gate
mint_id: a5e3577922934fec81191bfcd8af9718
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: aa72611c20fff806
season: 2
testable_claim: "SL7.130 residue (belam wf_e6c01557-ef7, GO 12:27Z), ONE kid, sensei.py + its two test files only, rotate.py untouched. Line numbers on MAIN db6357605. (1) Both refusals - the --record <stamp> miss (sensei.py:730-732) and the --gen miss (:747-750) - are asserted only by rc 2 (test_sensei_audit_record_window.py:202-210 and :223-226): add stderr-text assertions that name --record in each refusal. (2) :727-728 substring fallback + :733 hits[-1]: an ambiguous PARTIAL stamp (--record 20260916 on a post with several records that day) silently resolves to the newest; an exact stamp or a UNIQUE partial resolves (the header prints the full stamp); >= 2 hits refuse by name listing every stamp (belam ruling 12:47Z, wf_98c9e4b6-7bf: a single hit is unambiguous by construction). (3) --record latest short-circuits BOTH :736 and the :751 session gate, so wake-audit --record latest on a non-prime post whose newest on-disk record belongs to ANOTHER session audits it instead of refusing like the no-flag default (:756-761): latest must pass the same session gate (or refuse by name), with a committed test on the wake side. Notes, same node, no separate round: cmd_wake_audit re-resolves the record at :1450-1453 (a second call site; the comment at :1444-1446 claims one) - return the stamp from wake_audit instead; _rotation_records :556-561 is dead - delete it. Falsifier: --record 20260916 on a fixture post with two records that day resolves instead of refusing; or wake-audit --record latest on a fixture whose latest record carries another session_id exits 0; or a refusal stderr that does not contain --record. Every printed line keeps naming the record stamp, never a generation (owner 09-13)."
thought_session: dissolve-legacy-2026-09-19
title: L4 the sensei record selector refuses ambiguous stamps by name and latest passes the session gate
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-sensei-record-selector-refuses-ambiguous-stamps-by-name-and-latest-passes-the-session-gate

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Clause (2) wording amended after the SL7.131 review (belam 12:47Z, wf_98c9e4b6-7bf): the code resolves a UNIQUE partial stamp and refuses >= 2 by name - a single hit is unambiguous by construction; the original "only an exact stamp resolves" was over-specified wording, not a defect. Landed as SL7.131 with no code change for this sentence.
<!-- THOUGHT:END -->
