---
id: hypothesis:l3w3-advisor-brief
mint_id: e2994219e3a94c63b9fce11af33a2647
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: ubuntu
scaffold_hash: 8fc2d9379a3e88e7
season: 2
testable_claim: brief.py assembles a tier-3 advisor brief for the claude-code parent role (opus 5, max, ultracode) that carries the head, the full body of the one vision node the advisor embodies, its seat in the standing room tier3-quorum, the audience rule for the prime, and the primitive to spawn a Fable-max perpetual-goal director, and a dry dispatch prints the resolved command with the ultracode env export
title: L3w3 advisor brief tier3 quorum
---
# hypothesis:l3w3-advisor-brief

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
WAVE 3 precondition (brief .agi/context/l3-command-ladder-brief.md sections 1.5, 1.9, 2.1, 2.3, 3). The three advisors are the tier-3 parents: claude-code, claude-opus-5, effort max, settings ultracode (roles row 3/parent); each EMBODIES one vision (vision:self-perpetuating, vision:all-is-one, vision:alive, minted at the wave-2 rollover on season/s2) and judges every seam through that vision's text and gloss. FILES: extensions/agi/bin/brief.py (advisor template for tier 3 parent: head from the shared derivation, then the vision body verbatim from the vision node the dispatch names via --target vision:<id> or --embody, then duties: sit in room tier3-quorum via send.py read/send --room tier3-quorum, one audience per rotation with send.py audience prime --reason, spawn and rotate the Fable-max director of a perpetual goal with dispatch.py --harness claude-code --tier director --role director --ladder-tier 1 --target goal:<id> and rotate.py loop --role director, review the director's rounds, never edit vision prose), extensions/agi/bin/dispatch.py (--embody vision:<id> or reuse --target for a vision node), tests. VERIFY: red-first tests that the assembled advisor brief contains the head, the Michael line, the whole vision body, the room name and the spawn primitive; dispatch.py dry run for --tier parent --harness claude-code --ladder-tier 3 --target vision:alive prints claude ... --model claude-opus-5 --effort max with CLAUDE_CODE_WORKFLOWS=1 exported; no live spawn (the prime launches the real advisors in wave 3). REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Do not commit, push, or run grid.py commit.

ADDENDUM 2026-09-07 (belam, after L3.10): this is a BUILD directive, not a status check; the L3.10 kid (a00-938e7071) only verified that the content does not exist yet and built nothing. Next kid: implement the advisor template and the tests as specified above; the dispatch/adapter half is already in place (verified in L3.10).
