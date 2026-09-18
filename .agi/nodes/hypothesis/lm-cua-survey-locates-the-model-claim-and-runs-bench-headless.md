---
id: hypothesis:lm-cua-survey-locates-the-model-claim-and-runs-bench-headless
mint_id: abd1a541b55241f7b67854643147cde5
type: hypothesis
parents:
  - idea:lm-cua-bench-as-typed-acts-source
next_edges: []
ceiling: <= 1 USD OpenRouter total; 0 USD compute; no VM, no Docker, no cloud desktop (Cua Fleets = spend, never without a Prime line)
edited_by: thought-master
falsifier: "(a) the model claim is found NOWHERE in cua docs, cua blog or the TypeSafe update (the premise came from elsewhere: ask the owner for the link, the idea stays as a bench/trajectory source only) OR (b) Cua Bench does not run headless on ARM4C without a VM/Docker/API key (record the exact failure; then it runs on the rig only) OR (c) the exported trajectory lacks typed action records (screenshots + clicks only -- not a typed-acts source; the idea narrows to a kid environment)."
scaffold_hash: 8a1c08c3ab66d541
season: 2
testable_claim: "(a) SURVEY (pi trove-survey read stage, judged by hand): sources = the cua README + cua.ai/docs (concepts: what-is-computer-use; bench; driver/connect-your-agent) + the TypeSafe changelog/blog for the update the owner saw; angles = which open model, which benchmark, which closed-source baseline, exact numbers + URL + date; what Cua Bench measures (reward, tasks, KiCad set, the Gemini 3.5 Flash 0.267 line); trajectory export format. Claim: the model + numbers are located and quoted, or the survey states that no such claim exists in those sources. (b) SMOKE on ARM4C: `uv` + Python 3.12/3.13, the Cua Bench simulated task from the README runs headless, one trajectory exported; its record carries per-step action type + target + args + observation. (c) MAPPING: a 20-line table maps those fields onto .agi/context/local-maxxing/typesafe/acts_replay.jsonl (jev typed acts) with the gaps named."
tests: "OWNER 22:5xZ: the survey half (a) is NOT a graph round -- it is the trove-survey workflow the thought-master runs after the SM fixes (SM.111/SM.112); this node keeps (b) the headless smoke + (c) the mapping: ONE pi parent + ONE kid, CPU-only -> CPU8G when routed else the rig spare threads (owner placement rule 22:4xZ), 0 USD compute, <= 10 min, uv venv under the round worktree deleted at round end, no model bytes; rows to file after every probe; land on the director post branch, push to refs/agi/posts/director-thought."
title: "cua hop 1 (survey read + one headless smoke): the trove-survey on trycua/cua docs + the TypeSafe update locates the exact open model and its numbers vs closed-source (quoted with URL + date), Cua Bench runs a simulated task headless on ARM4C with no VM/Docker/API key, and its exported trajectory is a typed-acts record (action type, target, args, observation) mappable onto the jev acts_replay schema"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-cua-survey-locates-the-model-claim-and-runs-bench-headless

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
thought-master 22:5xZ: narrowed per the owner -- survey = my workflow after the SM fixes; graph round = smoke + mapping only.
