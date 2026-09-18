---
id: idea:lm-typed-decisions-in-the-loop
mint_id: 3dcd4befc3014ccd953308af868342d0
type: idea
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
scaffold_hash: 0d3c7fefe4b8aa5d
scale: big
season: 2
tags:
  - local-maxxing
  - treasury
title: "\"Replace the loop small classifications (verdict class, evidence-present, defect severity, stops-slot state, inbox tag, brief-touches-real-resource, corpus labels) with TypeSafe typed decisions at ~$0.045/1M in and $0 out — measured first against 200 decisions the by-name reviews already made\""
town: local-maxxing
---
# idea:lm-typed-decisions-in-the-loop

## Source
doc:typesafe-ai-skill (+ the pane line quoted there). Siblings: idea:lm-kid-persona-lora (the corpus needs labels), hypothesis:l4-merge-up-gate-leaves-no-merge-in-progress and the g15 review lane (severity calls), config:rotations (stops-slot refusal: EMPTY / AMBIGUOUS refused, STALE not).

## Lever
The loop is full of small fixed-question decisions that today cost either a regex (brittle) or a prose LLM call (expensive, unstructured): they are exactly TypeSafe's shape — a state plus a question with named criteria, answered with a probability. At $0.045/1M input and $0 output (owner-stated), a 2k-token node costs ~$0.0001 to classify. Candidate sites, each a `choice`/`noul`/`score` with criteria we already write in prose:
1. Kid scaffold: verdict class of an experiment body (proved / disproved / inconclusive_lean_* / pending) as `choice`; "does the body carry a measured number with a source" as `noul`; confidence as `score` — a pre-check before the evidence gate, and a hint the small kid model does not have to reason out itself.
2. Merge-up review triage: per defect, severity demote / residue / note as `choice`; "does this diff touch the gate it must pass through" and "does any test reach a real pane/unit/crontab/process" as `noul` — the reviewer's own rules as criteria.
3. Rotation: stops-slot state EMPTY / AMBIGUOUS / STALE / CURRENT as `choice` (today a heuristic in rotate.py); "does the card name the exact next command" as `noul`.
4. Comms: the Prime tag ([merge-up] [decision] [rotation] [red] [rule] [complete] [owner]) for an untagged line as `choice`; urgency as `noul`.
5. Corpus labels for idea:lm-kid-persona-lora: accepted / rejected / unlabelled reason per example as `choice` over 354+ examples for ~$0.03.
6. Dispatch guard: "does this brief ask a kid to touch a real resource or a secret" as `noul` before spawn.

## What it buys the town
Decisions off the kid's token budget and off the CC subscription, with a probability the gate can threshold — and a uniform log of (state, question, answer, confidence) that is itself training data for the local kid.

## First falsifier
On 200 past decisions with known answers (verdicts set by name reviews; defect severities from the mur jsonl; stops-slot refusals from rotation records; Prime tags from comms), TypeSafe `choice` agrees with the recorded answer < 85% of the time, or its confidence does not separate right from wrong (AUROC < 0.7) — then it is no better than the regex it would replace and the idea is dropped. Second falsifier: a 422/429 profile that makes a 2k-token state unusable (limits are ABSENT from the docs).

## Cheapest test on our iron
ROUND 1 (needs the key — BANKED with the Prime; ~$0.02 of TypeSafe + $1 OpenRouter for the kid): one kid replays the 200 labelled decisions through `/v1/systemone` from this A1 (curl, no SDK install), records agreement, AUROC, latency p50/p95, the 422/429 profile and the exact input-token bill; writes the table. Nothing in the engine changes.
ROUND 2 (g15, kids write code): one adapter + one gate at the best-scoring site, behind a config flag, off by default.

## Numbers (owner-stated unless marked)
$0.045 / 1M input, $0 output (owner); a 2k-token node ≈ $0.0001 (arithmetic); 200-decision replay ≈ 0.4M tokens ≈ $0.02 (arithmetic); limits/latency ABSENT from the docs.

## Provenance
Minted by thought-master 2026-09-17 00:0xZ from the pane line in doc:typesafe-ai-skill. No install, no key, no provider added by the thought-master: the plugin install is the Prime's harness cell, the key is a provider secret for the Prime + encryption town; round 1 waits for that line.

## Agent Notes
LEDGER (pane line 2026-09-17 00:3xZ): the TypeSafe account holds $5.00 preloaded, more on request — "run it all out if needed". Round 1 (hypothesis:lm-typesafe-replay-200) is capped at $0.10 by design (a replay needs no more); later rounds size their TypeSafe cap against this $5, each round naming its own line in this ledger. Spend is on the owner TypeSafe account, never OpenRouter.

OWNER 2026-09-18 01:5xZ (relayed verbatim by director-thought, owner said "Relay to your master"): "Both TypeSafe keys landed, $5 each. There are lots of ways to apply it to minimize tool-calling requirements -- for example a live transcript view with call suggestions, a three-layer jev-MCP sandwich: jev in front of MCP reading intent and suggesting MCP actions, and jev after MCP reading the pre-MCP jev inputs and dispatching tool-call suggestions to be confirmed or modified, eventually just auto-dispatched with a delay to allow undo for something like 10 to 60 seconds." STATE: round 1 (TM.25, hypothesis:lm-typesafe-replay-200) went pending at $0 -- TYPESAFE_KEY cannot reach a kid (dispatch path never reads MAIN .env; pi child_env merges only config literals) -> g15 finding with sanctuary-master 02:0xZ; and the belam--* corpus holds 14 tagged decisions (41 across all dm), not the 100 the claim needs. ROUND 2 re-scope (after the key path lands): corpus = decision -> next-tool-call pairs mined from kid transcripts on this box (1,943 output.logs), N = 200 sampled, held-out; jev noul/choice/score predicts the next tool call from the pre-call context; metrics = top-1 agreement with the call actually made, USD per decision, latency; that IS the owner call-suggestion layer measured before any UI. The sandwich is minted beside this node as idea:lm-jev-mcp-sandwich.

OWNER 2026-09-18 02:0xZ (thought-master pane, verbatim): "Also jev can help with auto naming for things like NODE ids or especially session ids i think". LOOP SITE 7 = NAMING: today experiment ids are opaque mint hashes (experiment:a00-<hash>-<6hex>), session ids are uuids / registry names (agi-a2, d98fb21a), loop branches carry a truncated slug + agent hash; only hypothesis/idea slugs are authored. A typed name decision (jev noul over the node body / the session brief -> one slug under the schema+branch grammar) could give every minted thing a readable, unique, grammar-conformant name at mint time. ROUND SHAPE ($0.02-0.05, API-only, blocked with the rest on SM.103 forward_env): replay 100 existing nodes (bodies -> proposed slug) + 50 rotation records (brief -> proposed session name); metrics = collision rate against the live graph (must be 0 after a deterministic suffix), grammar conformance (branches.py parse + schema slug regex, must be 100%), gist coverage (slug contains the body top-2 TF-IDF terms, target >= 0.8), USD per name; ship = mint-time suggestion behind write.py create / rotate.py spawn with the hash kept as the immutable mint_id (address changes, mint id never -- G2.5).
