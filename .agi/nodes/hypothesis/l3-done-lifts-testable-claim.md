---
id: hypothesis:l3-done-lifts-testable-claim
mint_id: acd4549263394558bb6418c9974d38e7
type: hypothesis
parents:
  - goal:g7.33.10.1
  - hypothesis:born-valid-without-touching-frontmatter
next_edges: []
edited_by: belam
evidence_runs:
  - experiment:dg2close-l3-done-lifts-testable-claim-check
loop: goal:g15@s2
model: claude-fable-5-1
profile: balanced
role: director
scaffold_hash: 17b8397fc019c09f
season: 2
testable_claim: "A hypothesis is scaffolded without testable_claim (not derivable at scaffold, goal:s31) and the kid brief forbids frontmatter edits, so the field is only ever filled by an attentive parent or director. If cli.py done, on a hypothesis node, lifts the first paragraph under the ## Hypothesis heading (or a Claim: line the kid brief now tells it to write) into testable_claim through node_writer, and refuses loudly when neither exists, then a hypothesis finished by a standard DeepSeek kid passes links.py schema at done. Proved by a red-first test on cli.py done plus one live kid whose node is schema-valid without a parent backfill; disproved if the standard kid path still leaves the field empty or the lift invents text."
thought_session: iter-L3.14
title: cli.py done lifts testable_claim from the kid body, so a scaffolded hypothesis is schema-valid at done if not at birth
verdict: proved
---
# hypothesis:l3-done-lifts-testable-claim

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Parent brief (a00-3f745c2f, after two concordant disproved probes experiment:a00-8547e564-df7969 and experiment:a00-da23eefb-64a6f1): the claim is DISPROVED as the tree stands. Root cause: node_writer.py _BODY_SECTIONS["testable_claim"]=("testable claim","claim") does not match the scaffold body heading ## Hypothesis, and derive_required_from_body returns UNCHANGED silently. Next kid: (1) add "hypothesis" and "the claim" to _BODY_SECTIONS["testable_claim"] in extensions/agi/bin/node_writer.py; (2) make cmd_done in cli.py print a loud SCHEMA-WARNING to stderr when missing_required is still non-empty after the lift attempt (no rc change — keep never-fatal); (3) run pytest extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_cli.py; (4) red-first end-to-end: scaffold a hypothesis in a temp project, fill only ## Hypothesis, run real cmd_done, assert testable_claim lifted and missing_required empty; (5) report.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Moved from goal:s31 to goal:g7.33.10.1 because its proved lift (cli.py done lifts testable_claim from the body) is the one deriver g7.33.10.1's links.py schema --fix must reuse; the hypothesis parent is kept. goal:g7.33.10.1 is the live leaf the council re-homed retired s31 into, and its body cites this node by id. Owner, verbatim: "Move all hypotheses under all retired s goals to be patented by appropriate nested g-goals". Parenthood only (owner: "The regime doesn't need a goal. We're just adjusting parenthood"): mint_id, body and verdict unchanged.
<!-- THOUGHT:END -->
