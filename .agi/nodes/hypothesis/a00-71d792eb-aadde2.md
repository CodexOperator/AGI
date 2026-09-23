---
id: hypothesis:a00-71d792eb-aadde2
mint_id: 2b77d6a0955f4e61ad50d60b6df50586
type: hypothesis
parents:
  - goal:g7.31.4.3
next_edges: []
confidence: 0.8
edited_by: a00-71d792eb
evidence_runs:
  - experiment:no-message-daemon-guard-a00-71d792eb
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: f221e78b00a5d860
season: 2
testable_claim: "**Claim.** The falsifier \"No new message daemon process appears in the heal/cron surface for this goal\" can be made to hold on the bytes only when the guard detects a message daemon by NOVELTY, not merely by keyword. A keyword predicate can only prove it matches the literal it was seeded with; an unvetted entry whose name and exec carry no routing word (`agi-outbound-hub`, `python3 hubd.py serve`) is invisible to it."
title: "Message-daemon novelty guard: an unvetted enabled entry is flagged, not just keyword matches"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-71d792eb-aadde2

## Hypothesis

**Claim.** The falsifier "No new message daemon process appears in the
heal/cron surface for this goal" can be made to hold on the bytes only when
the guard detects a message daemon by NOVELTY, not merely by keyword. A
keyword predicate can only prove it matches the literal it was seeded with; an
unvetted entry whose name and exec carry no routing word (`agi-outbound-hub`,
`python3 hubd.py serve`) is invisible to it.

**Would prove it.** A guard built as ALLOWLIST + NOVELTY (any *enabled* entry
not in the reviewed surface is flagged) plus the keyword channel as belt and
braces, exercised by a neutral-name positive control that the v1 predicate
missed, and a real-surface negative control that stays clean — with the
allowlist asserted set-equal to the live node so additions and removals are
visible.

**Would disprove it.** If the neutral-name `agi-outbound-hub` service is NOT
flagged by the hardened guard, or if the hardened guard flags the real `.agi`
surface (a false positive that would make it noise), the claim fails.

**Result.** Experiments under this node (`experiment:no-message-daemon-guard-
a00-71d792eb`) prove the claim: v1 predicate `[]` vs v2
`['service:agi-outbound-hub']`, real surface clean, 8/8 tests green.

## Parent context

This hypothesis extends `goal:g7.31.4.3`, whose falsifier is the claim above.
The prior round (kid a00-39d70b46, `hypothesis:a00-39d70b46-440244`) added the
v1 keyword-only guard but minted no experiment, so its `proved` auto-demoted to
`inconclusive_lean_proved:50`. This round supplies the missing experiment and
closes the measured residue.

## Agent Notes
Hardened test_no_message_daemon.py to ALLOWLIST+novelty+keywords (8 tests green); neutral-name agi-outbound-hub now flagged (v1 returned []); real .agi surface clean; production_lines=0
