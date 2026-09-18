---
id: hypothesis:lm-jev-docs-hunt
mint_id: b21fa765e96d4a8d833ea7a4b475af38
type: hypothesis
parents:
  - idea:lm-typed-decisions-in-the-loop
  - goal:g14
next_edges: []
ceiling: $2 OpenRouter for the rounds own tokens (parent + 3 kids, deepseek-v4-flash class); $0 compute; no GPU, no ssh, no Camber, no model download; kid line_ceiling 120, <= 40 tool calls per kid, <= 45 min wall per kid; nothing touches .env/Doppler/<keeper-dir>; no TypeSafe key used or needed for this round.
edited_by: director-thought
falsifier: Any digest visits fewer than 12 distinct pages with no stated reason, or contains a claim with no URL, no date, or no MEASURED/ESTIMATE tag -- demote of that kid. The synthesis names fewer than 8 loop sites, or any site in it lacks a falsifier, a dollar-per-1000-decisions figure, or a named engine seam -- demote of that row, and if fewer than 8 rows survive with all three, demote of the round.
file_scope: ".agi/nodes/hypothesis/lm-jev-docs-hunt.md (TM ordered, director mints; parent edits verdict + probes + review lines only) - .agi/nodes/experiment/<kid-id>.md x3 (kids write) - .agi/context/local-maxxing/troves/2026-09-18-typesafe/{concepts-api.md, recipes-integrations.md, pricing-legal.md, synthesis.md} (hunt_args.json is READ-ONLY input, already committed). Nothing else: no extensions/, skills/, src/, .env, Doppler, <keeper-dir>, config.json, no edit to hunt_args.json, no other node."
scaffold_hash: 60237f0bba1a2031
season: 2
testable_claim: "Three kids, each with the verbatim reader brief from .agi/context/local-maxxing/troves/2026-09-18-typesafe/hunt_args.json (sources[].prompt: concepts-api, recipes-integrations, pricing-legal; fetch by curl, no paid API, no key needed since the docs are public -- if a page needs auth, log the URL and skip), deliver .agi/context/local-maxxing/troves/2026-09-18-typesafe/<key>.md digests such that every claim carries a URL and a date and is tagged MEASURED or ESTIMATE, and each digest visits at least 12 distinct pages or states plainly which topics had fewer and why; and the parent synthesises the three digests into synthesis.md: a ranked list of at least 8 loop sites for typed decisions (the sites already named on idea:lm-typed-decisions-in-the-loop -- 6 as currently written there, not 7 -- plus any new ones the docs inspire), ranked by knowledge-per-token, each row carrying a falsifier, a dollar-per-1000-decisions figure derived from the quoted price, and the specific engine seam it would plug into (a write.py verb, a rotate.py step, a dispatch.py gate, or a review step) -- a row with no price or no named seam is a demote of that row, not a pass."
tests: "ONE pi parent, THREE kids (concepts-api, recipes-integrations, pricing-legal), READ-ONLY web + this box: fetch with curl -sL + python3 tag-stripping, no pip installs, no downloads, no ssh, no GPU, no paid API and no TypeSafe key needed (the docs are public; if a page requires auth, the kid logs the URL and skips it rather than trying to authenticate). API/curl class: this round is light enough on both network and CPU to run beside anything else live (off-box, A1-light or A1-heavy) with no loadavg gate. Each kid <= 40 tool calls, line_ceiling 120, <= 45 min wall. Kids write their digest plus an experiment node each. The parent spawns all three (spawn.json x3), authors no experiment node, writes synthesis.md from the three digests per the CLAIM above, re-probes one citation per digest by opening it directly, writes probes: per numbered conjunct, sets verdicts; proved needs the kids in evidence_runs. Mur (director-thought runs workflow.py run merge-up-review per the standing rule) BEFORE delivery to thought-master -- any red the mur finds gets fixed in-loop or the affected row or kid demoted before the merge-up line goes up, never sent up unresolved."
title: "Docs hunt for jev/TypeSafe: three kid readers (concepts+API, recipes+integrations, pricing+legal) synthesised by the parent into a ranked list of >= 8 typed-decision loop sites, each priced and mapped to an engine seam"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-docs-hunt

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-thought per direct order (TM.28) from thought-master, itself relaying the owner (02:1xZ 09-18): only a 19-line README digest exists for TypeSafe/jev (.agi/context/local-maxxing/papers/typesafe-ai.md), and the owner wants richer docs pulled in since they would likely inspire other applications beyond the 6 sites already named on idea:lm-typed-decisions-in-the-loop. Shape copied deliberately from hypothesis:lm-oscillator-research-hunt (TM.22): one parent, three reader kids, a hunt_args.json carrying the verbatim per-kid briefs (here at .agi/context/local-maxxing/troves/2026-09-18-typesafe/hunt_args.json), each kid producing a cited digest, the parent synthesising a ranked, priced, seam-mapped list. One correction against thought-master own order text: they said the idea node names 7 sites; reading it directly shows 6 (numbered list items 1-6) -- the node and TESTS section here say 6, not 7, so the parent synthesis does not chase a phantom 7th site. Mur (workflow.py run merge-up-review) is now standing policy for director-thought before any merge-up delivery, per thought-masters same-session rule -- noted here since this round is the first one minted entirely under that new policy.
<!-- THOUGHT:END -->
