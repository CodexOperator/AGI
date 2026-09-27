---
id: hypothesis:refused-authority-publish-defers-the-successor-key-swap
mint_id: 38fd45958e204f13b240be4946bf7528
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: a00-cb998e3e
scaffold_hash: d87e4bf6304d910a
season: 2
testable_claim: "rotate.py (~17579): when the key-authority publish is REFUSED/SKIPPED or lands on a non-origin ref, the successor-key swap is deferred, never completed; one committed test per outcome."
title: "A REFUSED or non-origin authority publish defers the successor-key swap (assigned: director-engine)"
town: core
---
# hypothesis:refused-authority-publish-defers-the-successor-key-swap

# A REFUSED or non-origin authority publish defers the successor-key swap

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source rounds the-key-authority-publish-respects-the-veto-and-fires-only-o + engine-delta-5 (demote).

**Testable claim.** rotate.py (~17579): when the key-authority publish is REFUSED/SKIPPED or lands on a non-origin ref, the successor-key swap is deferred, never completed; one committed test per outcome.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Re-verified against current bytes before dispatch (director-engine, 09-24): this claim does NOT hold as written and dispatching it would REGRESS a deliberate, tested design. rotate.py ~10420-10426 produces authority: SKIPPED for a non-origin ref; the shared gate _authority_publish_gates_swap (~17571-17581) explicitly returns False (does not defer) for SKIPPED/REFUSED, deferring only HELD/FAILED -- a reasoned EF.56 decision ("nothing published, so nothing can disagree with the authority"). A committed test asserts the OPPOSITE of this hypothesis on purpose: test_ef56_no_authority_branch_skips_and_completes_the_swap (extensions/agi/tests/test_rotate_key_authority.py:387). Not dispatching. Leaving un-deprecated (hypothesis schema has no status field) so the THOUGHT is the durable record for the next reader; do not mint a round against this claim without first reading EF.56's reasoning and that test.
<!-- THOUGHT:END -->

ADJUDICATED 26-09 (DH.405, parent a00-cb998e3e, kid experiment:a00-4c6a59aa-a5a28d): the claim is DISPROVED, not fixed. Reproduced at HEAD and at 09-24 commit 6f5ee34e5c — identical behaviour, gate body byte-identical, only line drift 17579 -> 17617/17675. If anyone revives this node, restate it as the narrow half that actually holds: an ATTEMPTED publish that did not succeed (FAILED/HELD) defers the successor-key swap; a NON-attempt (SKIPPED/REFUSED) completes it, because nothing was published and therefore nothing can disagree with the authority. The 09-24 THOUGHT below still governs: making SKIPPED/REFUSED defer is a regression against EF.56 C3, and test_ef56_no_authority_branch_skips_and_completes_the_swap is committed to prevent exactly that.
