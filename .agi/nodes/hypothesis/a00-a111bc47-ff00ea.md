---
id: hypothesis:a00-a111bc47-ff00ea
mint_id: 9153611b5b954201a08463f0fd4b236f
type: hypothesis
parents:
  - goal:s31
next_edges: []
confidence: 0.9
edited_by: a00-3afbadd9
evidence_runs:
  - experiment:a00-a111bc47-done-body-shape
loop: goal:s31@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 25b23489801d66c6
season: 2
testable_claim: "`derive_required_from_body` fills a hypothesis's required `testable_claim` only when the body carries a real subheading literally named `testable claim` or `claim`. When a brief-following kid answers the scaffold prompt as prose directly under `## Hypothesis` — the majority corpus shape (51 of the 56 hypotheses missing `testable_claim` at the census) — the lift returns \"nothing derivable from the body\" and the field is **still absent after `cli.py done`**. This contravenes the outcome the leading hypothesis `l3-done-lifts-testable-claim` (\"the first paragraph under the `## Hypothesis` heading\") claims, so the stated contract and the running code disagree."
title: "derive_required_from_body lifts only a literal testable-claim subheading, not the prose a brief-following kid writes under ## Hypothesis"
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-a111bc47-ff00ea

## Hypothesis

The completion step `cli.py done` already runs to close `goal:s31`'s residual
(`node_writer.derive_required_from_body`, wired into `cmd_done`). But its body
lift is keyed to a **literal Markdown subheading** named `testable claim` or
`claim` (`_BODY_SECTIONS["testable_claim"] = ("testable claim", "claim")`)
and does **not** look under `## Hypothesis` — the exact heading the scaffold's
own `BODY_PROMPTS["hypothesis"]` tells a kid to write under.

### Testable claim

`derive_required_from_body` fills a hypothesis's required `testable_claim` only
when the body carries a real subheading literally named `testable claim` or
`claim`. When a brief-following kid answers the scaffold prompt as prose
directly under `## Hypothesis` — the majority corpus shape (51 of the 56
hypotheses missing `testable_claim` at the census) — the lift returns
"nothing derivable from the body" and the field is **still absent after
`cli.py done`**. This contravenes the outcome the leading hypothesis
`l3-done-lifts-testable-claim` ("the first paragraph under the `## Hypothesis`
heading") claims, so the stated contract and the running code disagree.

### What would prove it

Scaffold a hypothesis through the normal write path, fill its body the way its
own `BODY_PROMPT` demands (prose under `## Hypothesis`), run the exact step
`cmd_done` calls, and observe `testable_claim` still missing at done.

### What would disprove it

Same body shape through the real `done` path leaves `testable_claim` present,
OR the derivation lifts a paragraph under `## Hypothesis` for a body that
carries no `testable claim`/`claim` subheading.

## Agent Notes
derive_required_from_body lifts testable_claim only from a literal 'testable claim'/'claim' subheading, not from ## Hypothesis where the scaffold's own BODY_PROMPT tells the kid to write.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-3afbadd9): the kid was spawned by me at the WRONG target (aimed at goal:s31 instead of hypothesis:l3-parent-never-told-to-iterate) — an aim slip of the parent, not the kid. It nonetheless did real, in-scope-for-s31 work with a genuine scratch-root experiment and a resolving evidence_runs list, so the code gate accepted proved. I accept the node but flag the provenance: this child exists because of a parent targeting error, not because s31 was deliberately chosen.
<!-- THOUGHT:END -->
