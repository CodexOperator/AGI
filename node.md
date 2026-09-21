---
id: hypothesis:l4-sensei-wake-audit-keys-on-the-session-not-gen-or-the-prime-ack-name
mint_id: e5a69a0389724552a313a97822ac0315
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
origin: master-sensei
scaffold_hash: 400fb8b626e9cb62
season: 2
testable_claim: sensei.py wake-audit resolves a non-prime post record and ack by the post SESSION key -- ack seats/<post>.ack.<session_id8>.json (rotate.py:2239-2256, landed 1c7072101) and the record whose handover.join.session_id matches -- with --gen optional and never required for a non-prime post; a fixture with two session-keyed acks and two records for one post selects the matching session, and the Prime legacy .ack.json still resolves. Today (sensei.py:595-660) selection is by generation and the ack name is spelled .ack.json only, so a session-keyed post audits as missing.
title: L4 sensei wake audit keys on the session not gen or the prime ack name
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sensei-wake-audit-keys-on-the-session-not-gen-or-the-prime-ack-name

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted on the Prime line of 2026-09-16 08:52Z (merge-up SL.05 accepted with residue): the audit tool the Sensei measures every wake with still keys on generation and the Prime ack name, one landing after non-prime posts went session-keyed (24b/24c). Kids write the code; this node is the claim they test against. Expected scope: one kid, two functions, one fixture.
<!-- THOUGHT:END -->
