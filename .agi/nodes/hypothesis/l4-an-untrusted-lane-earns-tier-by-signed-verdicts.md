---
id: hypothesis:l4-an-untrusted-lane-earns-tier-by-signed-verdicts
mint_id: de3594e1cb55418783729e0ea07d03c7
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: d159df7669a09a0c
season: 2
testable_claim: "OWNER 2026-09-11 20:3x-21:4xZ (the eight rungs, verbatim in doc:l4-owner-decisions; vision:web-app-suite db436e1f1: 'Rungs 1-4 are live as goal lines under goal:g15 at the Sanctuary director'). Proposed by sanctuary-director 214458Z 01:33Z, ACCEPTED by Prime XIII 01:33Z: 'mint the three hypothesis nodes now (parents goal:g15, town all) but do NOT dispatch until rung 1's F1-F4 land at the sensei-director (rung 2 sits behind enforcing)'. HELD -- not dispatched. RUNG 4, owner verbatim: 'Open onboarding. Keypair + signed charter acceptance co-signed by a sponsor; an untrusted lane (worktree only, no merge, no dispatch, a per-key budget); tier earned by signed verdict history -- point your inference source/harness at api x and contribute to the Sanctuary.' CLAIM: (1) `send.py keygen --onboard <name>` mints a keypair and a charter-acceptance record signed by the newcomer and co-signed by a sponsor post (rung 2's signature shape); the record is the newcomer's config:posts row (tier `untrusted`, written by the Prime on the sponsor's signed request); (2) the UNTRUSTED lane: the row's worktree is the only place it may write, dispatch refuses it as a spawner, the merge-up recipe refuses its branch, and its per-spawn key cap is the row's `budget` cell; every refusal names the tier; (3) tier is EARNED: a signed verdict history (experiment nodes whose verdicts a trusted reviewer countersigned) crosses a threshold declared in the ladder and the Prime promotes the row -- never a self-edit; (4) tests on fixtures: onboarding without a sponsor refused; the untrusted lane's four refusals; a promotion with the threshold met / one short; the 'point your harness at api x' path = the row's harness cell resolving to a non-pi harness through the existing harnesses table. Ceiling and file scope are set when the round is cut; serial behind rung 3."
title: "RUNG 4 (held): open onboarding -- keypair + sponsor-co-signed charter acceptance; an untrusted lane (worktree only, no merge, no dispatch, per-key budget); tier earned by signed verdict history"
town: all
---
<!-- BODY:BEGIN -->
# hypothesis:l4-an-untrusted-lane-earns-tier-by-signed-verdicts

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
GO (Prime XVI 49ddab, 14:20Z, signed): rungs 2-4 released; this rung (4) is cut AFTER L4.324 (rung 2) lands, because the charter acceptance is a rung-2 signature shape. FILE SCOPE at that time: not cli.py / branches.py / the four rename test files (L4.322/L4.323); fixtures only against posts.md, the real tree is read, not written; never mint a real key outside the fixture.
