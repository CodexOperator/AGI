---
id: doc:l4-five-unstaffed-seats
mint_id: 44f265ffc66f41bf8a6a0c7cc16a854b
type: doc
parents:
  - goal:g17.1
next_edges: []
confidence: 0.5
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-852433f1-2975a8
loop: hypothesis:l4-five-unstaffed-seats-specified-none-created@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b9f4ab1c6bd1b31c
season: 2
tags:
  - l4
  - seats
  - spec
  - g17.1
thought_session: sanctuary-director-genIV-L4
title: The five unstaffed seats get cards and no chairs; the owner's holes stay holes
verdict: inconclusive_lean_proved:85
---
# doc:l4-five-unstaffed-seats

## Five seats get cards and no chairs

Spec for the five roles the owner named but has NOT yet set up live. NOT ONE is
created, launched or given a row here — this writes a `.doc` card for each and
stops. `config:seats` (`.agi/nodes/.geometry/seats.md`) is untouched and no
`config` node is minted. The card grammar is COPIED from the owner's own role
cards at `l4-owner-decisions.md:345-361` — `NAME: answers-to=... | pulls=... |
tells=... | Q="..." -> {answer set}`, then a `NOT:` line — not invented. Every
field carries a `file:line` citation to the owner text it comes from; where the
owner never said, the literal token `UNSPECIFIED` appears with the one question
that would settle it. Inventing a plausible field is the failure mode of this
round.

## The five cards

**GOAL KEEPER (Sage)** — a keeper, IN the Keep (`l4-owner-decisions.md:340`, "Sanctuary Keep ('the Keep') = Sanctuary Keeper (Mistress), Role Keeper (Sensei, teacher), Goal Keeper (Sage)"; the Keep's shared card is `:352`). *[Citation corrected by sanctuary-director on merge: this line cited `.agi/nodes/.geometry/seats.md:2`, which is the line `id: config:seats` and supports nothing about the Keep. The other fifteen refs in this document were sampled and all land on the text they claim.]*

`GOAL KEEPER (Sage): answers-to=the Council (a keeper does not answer to the Keep it sits on; the Keep answers to the Council) [l4-owner-decisions.md:352] | pulls=channel A — every director comm lands on the Sage as the internal liaison — seat nodes vs live processes + spend [l4-owner-decisions.md:352,:355,:257] | tells=the routed recipient — the master or director who needs to know (the Keep tells "* Masters (assign a workflow), directors (routed answers)") [l4-owner-decisions.md:352,:355] | Q="Who needs to know this?" -> {route:<recipient> | nobody} [l4-owner-decisions.md:355,:257]`

`NOT: UNSPECIFIED — the owner gave a NOT line to the Prime, the Council and the * Masters [l4-owner-decisions.md:349,:351,:357] but never to a keeper in the Keep; the one question that settles it: is the Goal Keeper route-only, or may it also build / dispatch a workflow?`

**DRAFT MASTER** — the brief-drafting Master; "Policy Master" is the superseded name [l4-owner-decisions.md:387,:389].

`DRAFT MASTER: answers-to=the Keep (assignment), the Council (acceptance) [l4-owner-decisions.md:356] | pulls=the assignment, its own workflow's output — the brief-drafting workflow [l4-owner-decisions.md:356,:341,:329] | tells=the Council (channel B: the drafted brief), the Keep (done / blocked) [l4-owner-decisions.md:356] | Q="What brief gets this done?" -> {a drafted brief, the brief-drafting workflow's output} [l4-owner-decisions.md:356,:341,:379]`

`NOT: address a director or the Prime · work outside its workflow [l4-owner-decisions.md:357]`

**GLITCH MASTER** — the round-review Master [l4-owner-decisions.md:341,:329].

`GLITCH MASTER: answers-to=the Keep (assignment), the Council (acceptance) [l4-owner-decisions.md:356] | pulls=the assignment, its own workflow's output — the round-review workflow [l4-owner-decisions.md:356,:329] | tells=the Council (channel B: the review), the Keep (done / blocked) [l4-owner-decisions.md:356] | Q="What is wrong with this?" -> {the review, the round-review workflow's output} [l4-owner-decisions.md:356,:341]`

`NOT: address a director or the Prime · work outside its workflow [l4-owner-decisions.md:357]`

**RESEARCH MASTER** — deep, exploratory research on things that need more in-depth exploration; grows with local-maxxing [l4-owner-decisions.md:370].

`RESEARCH MASTER: answers-to=the Keep (assignment), the Council (acceptance) [l4-owner-decisions.md:356] | pulls=the assignment, its own workflow's output — the deep-exploration research workflow [l4-owner-decisions.md:356,:370] | tells=the Council (channel B), the Keep (done / blocked) [l4-owner-decisions.md:356] | Q=UNSPECIFIED — the owner introduced the Research Master at :370 and gave it NO question anywhere in the text; the one question that settles it: what is the Research Master's main question (e.g. what needs deeper exploration, and who should explore it)?`

`NOT: address a director or the Prime · work outside its workflow [l4-owner-decisions.md:357]`

**SHAEL** — the owner's voice / liaison, takes the owner's preferred name [l4-owner-decisions.md:253,:379].

`SHAEL: answers-to=the Keep (assignment), the Council (acceptance) like any * Master — with the owner as the standing audience it serves, "maximally available for owner questions and to deliver answers/reports above all else" [l4-owner-decisions.md:356,:372] | pulls=the assignment, its own workflow's output, and equally the owner's questions [l4-owner-decisions.md:356,:372] | tells=the Council (channel B), the Keep (done / blocked), and delivers the relevant info to the role that most cares about knowing it [l4-owner-decisions.md:356,:372] | Q="Who cares the most about knowing this?" -> {deliver:<role>} — the owner's LATER question, called by him "Shael's main question"; SEE THE TWO-Q CONFLICT BELOW [l4-owner-decisions.md:372,:380]`

`NOT: address a director or the Prime · work outside its workflow [l4-owner-decisions.md:357]`

## The three holes, left open on purpose

1. **The Research Master has NO question.** Introduced at `:370` as "responsible for doing deep, exploratory research on things that need more in-depth exploration", given no `Q`. Its card above carries `Q=UNSPECIFIED` with the question that would settle it. Not closed.

2. **Shael has TWO questions.** `:356` gives `Q="What would the owner say?"`; `:372` gives "Shael's main question is 'Who cares the most about knowing this?'". BOTH are recorded; `:372` is LATER (part 6, 22:48Z, vs part 5, 22:31Z) and the owner called it "main". Which one governs is the owner's to confirm — not this round's to pick. Not resolved.

3. **The `policy-master` row fate is unsettled.** `config:seats` `.agi/nodes/.geometry/seats.md:15` carries a `policy-master` row (sonnet-5/high); part 7 finalises the title as **Draft Master** and the owner calls "Policy Master" the superseded name (`l4-owner-decisions.md:387,:389`). Whether that row IS the Draft Master renamed or a stale row to deprecate is banked as **Q27** (`l4-owner-decisions.md:435`) — the Sanctuary Keeper rules it in one pass. Changing it is NOT this round. The row is untouched here.

## What is also recorded, from the owner's own sentences

- **Chambers — which assigns and which receives.** The * Masters answer to the **Keep** for assignment and the **Council** for acceptance, returning on channel B (`l4-owner-decisions.md:356`). The Goal Keeper is IN the Keep, so the Keep's card governs it instead: it answers to the **Council**, not to a chamber above it (`l4-owner-decisions.md:352`).
- **Tooling route.** "If a master or keeper needs more tooling, they draft a brief of what they need using the Draft Master and submit to Council for review" (`l4-owner-decisions.md:370`).
- **Council-to-Keep propagation.** "Once a master returns their results to the Council, the Council can choose to propagate some things to the Keep instead as needed if it's something that falls under a keeper's jurisdiction (so modifications to role arrangement, individual role parameters, or otherwise a new unforeseen need for more briefs or reviews)" (`l4-owner-decisions.md:370`).

## Why this is a doc, not a seat

These cards become `seat` node bodies when **L4.13** lands the `[seat]` type.
They are a `.doc` today because that type does not yet exist — this spec is
written against the LIVE vocabulary (goal, doc), not a future one, and says
out loud that it retargets to `seat` bodies when L4.13 lands.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version stands as the kid wrote it; the parent review (L4.57, a00-41c4e898) accepted it without edits and added only a review note flagging that the Masters answer-sets are inferred rather than verbatim owner text — the retarget to seat node bodies under L4.13 should re-derive them from the owner text, not carry the inference forward.
<!-- THOUGHT:END -->
# doc:l4-five-unstaffed-seats

## Agent Notes
REVIEW (parent a00-41c4e898): ACCEPTED. Five cards verified against owner-decisions 345-392; grammar copied, three holes intact (Research Master Q=UNSPECIFIED, Shael two-Q conflict recorded with timestamps, policy-master/Q27 untouched); seats.md policy row unchanged; no config node; links.py 1910 resolved 0 broken. Caveat recorded: the four Masters answer-set braces (-> {a drafted brief ...}) are inferred from the owner workflow-output phrasing at :356,:329,:341,:370, not verbatim owner tokens — cited but flagged for the L4.13 retarget to seat bodies.

## Agent Notes
Spec doc written: five role cards in owner grammar, three holes preserved, no seat/config created, links 0 broken