---
id: hypothesis:l2w2-telemetry-stamps
mint_id: a79e933316184c18a39da41db9929790
type: hypothesis
parents:
  - goal:g16
next_edges: []
edited_by: director
scaffold_hash: 994e4c49af9a45cc
testable_claim: At cli.py done the kid's node is stamped with tokens_in, tokens_out and cost_usd from a real source, and with accepted diff bytes at parent acceptance, or the node records which source was unavailable
thought_session: agi-master-2026-09-06
title: "L2 wave 2: l2w2-telemetry-stamps"
---
# hypothesis:l2w2-telemetry-stamps

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
INVESTIGATE FIRST, this is the owner's standing decision 5 (cost lookup is a hypothesis, not an assumption): determine where a pi kid's token usage and cost can be read after it finishes. Candidates in order: (a) pi's own session or usage log under ~/.pi (find it, read one real record from this run's kids); (b) OpenRouter's per-generation endpoint GET https://openrouter.ai/api/v1/generation?id=<generation id> using the kid's per-spawn key (provisioning.py issues it; the generation id must come from pi's log or response headers, check whether pi records it); (c) nothing available, in which case stamp source: unavailable and say why. Record the investigation in the experiment node before implementing. THEN FILES: extensions/agi/bin/post_wire.py or wherever cli.py done finalises the node, plus tests: stamp tokens_in, tokens_out, cost_usd (float, USD), telemetry_source (pi-log, openrouter-generation, unavailable) on the kid's node at done; accepted_bytes is the byte size of the node file plus its payload at the moment the parent accepts, stamped by the parent's done --owns path. Never read these fields anywhere to choose what to do; they are secondary (brief section 5). VERIFY: red-first tests with a fake source record; on this repo, show one real kid node from iter L2.04 or later carrying the stamps or the unavailable marker; suite green. REPORT: one experiment node under this hypothesis, verdict on the testable claim, evidence_runs as a list of node ids (pass --evidence-runs to cli.py done, your own experiment id counts), every verify command with its actual output in the body. Engine files are edited in place; suite via python3 extensions/agi/bin/commands.py run tests, green before you report; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md
