---
id: hypothesis:l4-sd06-residue-renumber-notice-fixture-dry-run-parity-refused-run-key
mint_id: 72c6443bba074559be1f26ba7d327ec9
type: hypothesis
parents:
  - goal:g6.16
next_edges: []
edited_by: belam
scaffold_hash: e9e58ba242e4b152
season: 2
testable_claim: "goal:g15 (residue of SD.06/L4.373, Prime review 12:12Z, mur wf_a2e23548-c20 -- ACCEPT WITH RESIDUE, accepted round untouched; belam XXIII noted line numbers may have drifted under upstream merges since the review -- re-measure on the current bytes, every named location still exists): (1) the conjunct ordinals in dispatch.py, provisioning.py and workflow.py's inline comments/docstrings, and in experiment a00-c2613ff6-31b78c's probes list, are shifted +1 against the parent hypothesis's own (1)-(5) numbering -- renumber all of them (code comments by hand, the experiment node ONLY through write.py); (2) the notice surface (dispatch.py's 'notice: {msg}' line preceding the account-floor ERR when check_key_floor returns (True, <marker>)) has no COMMITTED fixture test -- add one to test_dispatch.py that mocks check_key_floor->(True,'M') and check_account_floor->(False,'X') and asserts 'notice: M' appears before the ERR line with zero spawns (today only the parent's own in-process probe exercises this, nothing in the tree); (3) workflow.py's --dry-run path returns before _resolve_stage_timeout runs, so --dry-run can OK a manifest whose timeout_s the live run would refuse (0/negative/non-numeric) -- extend the existing credential-decision principle (dry-run already reflects credential decisions) to the timeout budget too, so --dry-run and the live run agree; (4) a run refused for an invalid timeout_s (rc 4) still consumes a minted per-run key with no tracking row recording why, and rc 4 collides with the stage JSON-parse-error return code -- give the timeout refusal its own distinct return code and either a tracking row or skip the mint entirely for a manifest that will be refused before any stage runs. Fixture-proven; suite green. FALSIFIERS: any conjunct's ordinal still disagrees with the parent hypothesis's numbering anywhere it appears; the notice-surface fixture test is absent from the tracked suite or doesn't fail on the pre-fix bytes; --dry-run still approves a manifest the live run would refuse on timeout_s; a timeout-refused run still consumes a key with nothing recording it, or its return code is still indistinguishable from a stage parse error."
thought_session: dissolve-legacy-2026-09-19
title: "SD.06 residue: conjunct renumbering, notice-surface fixture, dry-run/timeout_s parity, refused-run key tracking (belam review 12:12Z)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sd06-residue-renumber-notice-fixture-dry-run-parity-refused-run-key

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
