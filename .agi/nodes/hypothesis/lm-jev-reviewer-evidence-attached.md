---
id: hypothesis:lm-jev-reviewer-evidence-attached
mint_id: d24aeae92e3748a788daf91fc5cd8da3
type: hypothesis
parents:
  - idea:lm-why-jev-echoes-leaked-verdicts
  - goal:g5.24
next_edges: []
ceiling: <= 1 USD total (OpenRouter parent+kid); TypeSafe jev calls (2220 = 370 acts x 3 repeats x 2 arms) at the measured 1.645k mean input tokens (~3.7M tokens, ~0.15 USD at the JEV.01-measured $0.042/Mtok) inside the existing account; 0 compute; no downloads on ARM4C without an owner yes; runs <= 10 min
edited_by: thought-master
falsifier: Neither arm lifts the verdict subgroup above its 0.710 body-blind kind-prior (reviewer evidence is not what the bodies lack) OR leak_after is greater than 0 in any arm (the fixture, not jev, is broken) OR q2 does not exceed 0.776 in any arm (the accept-vs-demote failure is not an evidence-availability problem and cause 3 closes).
scaffold_hash: ba8da975fc229f04
season: 2
testable_claim: "Reuse the TM.42 pinned 370-act corpus and acts_replay_scrub.py (experiment:a00-0a6eb1a5-c0cf5c), jev-1.13.0, same seeds. ONE new variable: before each call append to the SCRUBBED body (a) the node structured frontmatter fields probes/evidence_runs/confidence/model (NOT verdict/status/demoted_from, which would leak the label) and (b) when the act maps to a round, the mur review text for that round from .agi/sessions/workflows/. Arms: ARM-E evidence-only, ARM-EM evidence+mur. Claim: on the verdict-node subgroup (n=169, jev scrubbed 0.479, kind-prior 0.710) ARM-E or ARM-EM q1 agreement rises ABOVE 0.710; and on the experiment subgroup (n=200, scrubbed 0.695) it holds or rises. Rows: per act arm, q1 agreement by subgroup, q2 accept-vs-demote agreement (target above its 0.776 baseline), ECE, cost USD, leak_after must stay 0."
tests: ONE pi parent + ONE kid, API slot; SM.103 forward_env is LANDED (adapters/__init__.py injects harnesses.<h>.forward_env from the MAIN-root .env; extensions/agi/tests/test_dispatch_forward_env.py 9 passed; config.json lists TYPESAFE_KEY/TYPESAFE_API_KEY; TYPESAFE_KEY is present in MAIN .env), so this is runnable now; re-using the TM.42 scrubbed cache and acts_replay_scrub.py; steps (1) build the evidence dict per act from node frontmatter, drop verdict/status/demoted_from, log the field list; (2) run ARM-E (1110 calls) then ARM-EM (1110 calls) with separate caches, leak_after asserted 0; (3) score q1 by subgroup and pooled, q2, ECE, cost; rows to bench/<utc>.jsonl, kid persists rows after every probe, parent commits promptly, FILE SCOPE .agi/context/local-maxxing/typesafe/, anonymization rule (hosts/IPs/GPU models/locations/key ids never; aliases ARM4C GPU2070S CPU8G EDGE), kid line_ceiling 120
title: "WHY jev echoes, hop 3 (cause 3, INPUT): the review call needs the reviewer evidence the bodies lack -- attach the structured probes frontmatter plus the round mur review text to the scrubbed body and the verdict-node subgroup rises above its 0.710 kind-prior"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-reviewer-evidence-attached

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
REVIEW (brainstorm adversarial, 2026-09-18): corrected the budget -- 2220 calls at the corpus measured 1.645k mean input tokens is ~3.7M tokens (~0.15 USD), not the claimed ~0.2k tokens per call (~0.02 USD); total still under the 1 USD ceiling. Confirmed runnable now: SM.103 forward_env landed in code (adapters/__init__.py), config declares TYPESAFE_KEY/TYPESAFE_API_KEY, test_dispatch_forward_env.py passes 9/9, and TYPESAFE_KEY is present in the MAIN .env, so the API arm is not blocked (the sibling single-axis node still says BLOCKED, which is stale).
