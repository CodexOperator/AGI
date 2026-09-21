---
id: experiment:a00-bb925977-20a90e
mint_id: 2c3f4692e3ab4afea8175b93f7aef6bb
type: experiment
parents:
  - hypothesis:lm-jev-docs-hunt
next_edges: []
edited_by: director-thought
line_ceiling: 120
loop: hypothesis:lm-jev-docs-hunt@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: f96d345f2ac11365
season: 2
title: "recipes-integrations kid: 44 pages, no MCP server or LangChain adapter exists, batched noul calls measured 12x cheaper and 10x faster, streaming absent"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# experiment:a00-bb925977-20a90e

## Experiment

Executed the `recipes-integrations` reader brief verbatim from `.agi/context/local-maxxing/troves/2026-09-18-typesafe/hunt_args.json`: fetch TypeSafe/jev docs with `curl -sL` (no key, no paid API), strip tags with python3, every claim URL + MEASURED/ESTIMATE tagged, >=12 distinct pages or state why fewer.

Pages opened (all HTTP 200): 44 distinct URLs, 71 requests to the live site and raw.githubusercontent.com. Discovery came from `https://docs.typesafe.ai/llms.txt` (115-line index) plus the 18 cookbook entries; raw markdown fetched by appending `.md` to each docs path (Mintlify). Raw copies of all fetched pages are in the session scratch dir `.agi/sessions/iter-TM.28/a00-bb925977/raw/` (scratch, not committed).

Deliverable written: `.agi/context/local-maxxing/troves/2026-09-18-typesafe/recipes-integrations.md` (82 lines) with the required sections Sources read / Recipes and worked examples / SDKs / Agent and MCP integrations / Streaming / Latency numbers / Fit for the town.

## Evidence

Answers to the four hunt questions:
1. Worked examples: 4 named patterns (`/patterns.md`) + 18 cookbooks + smart-home demo, each quoted with its actual JSON/code shape and its published measured numbers (e.g. `parallel_questions`: 13 q in one call $0.000497/0.27s vs 13 calls $0.006090/2.71s = 12.2x cheaper/10.0x faster; `rerank_typesafe`: top-1 5%->18%, top-10 38%->62%).
2. SDK surface beyond HTTP: Python `TypeSafeClient.system_one/models.list/close` + async mirror; JS `TypeSafeClient.systemOne/models.list` + `noul()/choice()/score()` helpers, ESM/CJS/TS, Node >=20. No batching helper exists in either SDK; batching = one `questions` map per call.
3. MCP server / agent-framework adapter: NO MCP server anywhere in `llms.txt` or the pages read; NO LangChain/LlamaIndex/CrewAI adapter. YES to an agent skill (`/agent-skill.md`: `claude plugin install typesafe@typesafe-ai`, `npx skills add typesafe-ai/skills --skill typesafe-ai`).
4. Streaming: ABSENT (`/api.md` returns one complete JSON; no stream method in either SDK reference).
5. Latency: measured 111 ms (consistency_noul), 114 ms (consistency_choice), 0.27s for 13 batched questions; no p50/p95 published (ABSENT).

Fresh findings the 19-line paper did not have: docs price is $42/Btok = $0.042/Mtok input with output free (`/models.md`) vs the owner-stated $0.045; rate limit 250,000 tok/s + 1,200 req/min; 64k context (32k state+longest question); SDKs are 3 days old (v0.5.7 on 2026-09-14).

## Metering

production_lines 82 (the digest; the experiment node is not production), line_ceiling 120 (the parent hypothesis `ceiling:` declares `kid line_ceiling 120`). 82 <= 120, so no re-brief needed. Note: the harness DEFAULT ceiling is 40, whose 2x is 80 — the round-level 120 was used as binding because the dispatching hypothesis declares it explicitly.
