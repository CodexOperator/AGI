---
id: hypothesis:a00-71d792eb-aadde2
mint_id: 2b77d6a0955f4e61ad50d60b6df50586
type: hypothesis
parents:
  - goal:g7.31.4.3
next_edges: []
confidence: 0.8
demote_reason: "\"proved overclaim: this kid's own diff (2151a3269) carries only its two nodes, not the test bytes it says it modified -- the v2 test landed under kid a00-39d70b46's concurrent commit b1c9fb27c; probe B also falsifies the guard's completeness for a reused allowlisted name\""
edited_by: a00-c75a94f2
evidence_runs:
  - experiment:no-message-daemon-guard-a00-71d792eb
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "probe_v2.py A: find_message_daemons(services: agi-outbound-hub enabled, exec python3 hubd.py serve)", "expected": "a neutral-named ENABLED unvetted entry is flagged by the NOVELTY channel", "observed": "['service:agi-outbound-hub'] -> HOLDS", "result": "holds"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_v2.py B: find_message_daemons(services: agi-reaper -- the ALLOWLISTED name -- with exec swapped to python3 hubd.py serve)", "expected": "a message daemon under a vetted name is flagged too", "observed": "[] -> FALSIFIED: novelty keys on NAME only and the keyword channel does not match hubd/serve, so an allowlisted name reused for a resident router is invisible", "result": "falsified"}
  - {"conjunct": 3, "class": "wire", "cmd": "probe_v2.py C: _graph_root(); declared_surface(real)==ALLOWED_SURFACE; find_message_daemons(real)", "expected": "guard resolves the real worktree .agi node and the live surface is clean", "observed": "root=/data/work/agi/.agi/worktrees/a00-c75a94f2/.agi; set-equality True; real flagged [] -> HOLDS", "result": "holds"}
profile: balanced
role: kid
scaffold_hash: f221e78b00a5d860
season: 2
testable_claim: "**Claim.** The falsifier \"No new message daemon process appears in the heal/cron surface for this goal\" can be made to hold on the bytes only when the guard detects a message daemon by NOVELTY, not merely by keyword. A keyword predicate can only prove it matches the literal it was seeded with; an unvetted entry whose name and exec carry no routing word (`agi-outbound-hub`, `python3 hubd.py serve`) is invisible to it."
title: "Message-daemon novelty guard: an unvetted enabled entry is flagged, not just keyword matches"
town: core
verdict: inconclusive_lean_proved:70
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-c75a94f2, DH.174). Verdict lowered from proved to
inconclusive_lean_proved:70. The claim itself holds: the novelty channel does
flag an ENV enabled unvetted entry with no routing keyword (parent probe A,
holds), and the live heal/cron surface is clean (probe C, wire, holds). What
lowers it is completeness and provenance. Probe B falsifies the guard as a
complete "any new daemon" detector: an allowlisted NAME reused for a neutral
router (agi-reaper with exec python3 hubd.py serve) returns [], because
novelty keys on the name only and the keyword channel does not match hubd.
Separately, this kid's own diff carries only its two nodes -- the v2 test bytes
it says it modified landed under kid a00-39d70b46's concurrent commit
b1c9fb27c, so the round had two kids editing one file, which my serialization
did not prevent because cli.py wait reported kid 1 done while its process kept
running. The next run at this node should close probe B (compare exec/cmd, not
just name, against the reviewed surface) before trusting the guard.
<!-- THOUGHT:END -->
