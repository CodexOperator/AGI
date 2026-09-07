---
id: hypothesis:l3-openrouter-codex-spend
mint_id: 12c4e179ea65453a87c9216056044165
type: hypothesis
parents:
  - goal:g16
next_edges: []
edited_by: ubuntu
scaffold_hash: 3d6f1e426b8e7af0
season: 1
testable_claim: An identifiable caller on this box sends gpt-5.1-codex requests through the owner's OpenRouter key every day; naming it with matched timestamps and either removing the call or replacing it through the command structure drops the daily codex share of OpenRouter spend to zero
title: L3 openrouter codex spend
---
# hypothesis:l3-openrouter-codex-spend

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER ASK 2026-09-06 (verbatim, belam session): for some reason I keep seeing gpt5.1 codex being used and credits spent in my openrouter usage. Fairly significant proportion of calls consistently day after day. Investigate why and see if they can eliminate it or propose and implement viable alternatives using the command structure. Again do it only once that's live and you can hand it off to them to pursue as another test of the system. SCOPE: wave-3 slice 2, dispatched by the live ladder (a perpetual director owns it; g16 by default, a director may re-hang it under g15), never by the prime before wave 3 is live. WHERE TO LOOK (pointers, not findings): the OpenRouter activity page or generations API with the key in .env for the calling app name, times and model slug; every config on this box that names a codex or gpt model: .agi/config.json, ~/.pi/agent (settings, extensions, pi-autoresearch), ~/.claude plugins (ck and bp codex-review.sh, the ck:judge skill), ~/.codex, crontab -l, any OPENROUTER_API_KEY export outside this repo, and the crons the graph declares (crons.py show). DELIVERABLE: an experiment naming the caller with evidence (timestamps matched to OpenRouter generations) and the daily share of spend it takes, then either the config change that stops it or a viable alternative implemented through the command structure (write.py, dispatch.py roles), with the spend delta measured afterwards. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Do not commit, push, or run grid.py commit.

ADDENDUM 2026-09-07 (owner, verbatim pieces): I think models are using the ask a more powerful model feature; its in the openrouter api. Timing corrected by the owner: the gpt-5.1-codex calls happened at the end of or during loop L2 (2026-09-05 to 06), none on 2026-09-07; not urgent, fix it in the planned wave. Prime's evidence for the kid: on 2026-09-07 the OpenRouter usage counter moved 55.49 to 55.96 over four two-parent pi rounds (L3.01 to L3.04, 0.19 + 0.10 + 0.11 + 0.07), fully accounted, so today's runs make no codex calls. First place to look: whatever escalation or ask-a-stronger-model tool the pi harness or its extensions (pi-autoresearch under ~/.pi/agent) expose to GLM parents and DeepSeek kids, and the OpenRouter generations list for 2026-09-05/06 filtered by model gpt-5.1-codex with the app name and the referer each call carried.
