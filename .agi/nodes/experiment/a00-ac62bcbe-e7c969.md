---
id: experiment:a00-ac62bcbe-e7c969
mint_id: a275b99323ca4a268e3811ea9d4e4e0f
type: experiment
parents:
  - hypothesis:lm-jev-cua-off-the-shelf-survey-against-action-registry-and-magic-pane
next_edges: []
confidence: 0.78
evidence_runs:
  - experiment:a00-ac62bcbe-e7c969
loop: hypothesis:lm-jev-cua-off-the-shelf-survey-against-action-registry-and-magic-pane@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: e7a1efe2fa56f2ea
season: 2
title: JEV/CUA public-docs integration survey
town: local-maxxing
verdict: inconclusive_lean_proved:78
---
<!-- BODY:BEGIN -->
# experiment:a00-ac62bcbe-e7c969

## Experiment

Reading-digest survey of public CUA/JEV-related components against the two existing TypeSafe credentials, with no key spend, model call, package install, container, VM, or GPU. The already-fetched TypeSafe trove was read before this round. The prior headless Cua Bench smoke is cited from `experiment:a00-778d86b3-170630` and was not rerun: `cb interact` produced reward 1.0 without VM/Docker/API key; `cb run task` still requires an unpublished `cua-bench:latest` image.

The synthesis is stored at `.agi/context/local-maxxing/troves/2026-09-24-jev-survey/synthesis.md`.

| component | needs | key-fit | recommendation | reason |
|---|---|---|---|---|
| trycua/cua | Python SDK; real agent needs an LLM provider; VM/container is optional/deployment choice (README, 2026-09-24) | No: TypeSafe authenticates only its typed-decision endpoint; normal provider key or local OpenAI-compatible endpoint needed | adapt | Its action/observation trace maps to the registry, but its agent loop would bypass propose-validate-execute. |
| Browser Use | Python + browser runtime + LLM provider (normally OpenAI-compatible; local endpoint possible) (README, 2026-09-24) | Partial: Jev could rank a fixed action set, but is not a drop-in chat/tool loop; another key/local endpoint needed | adapt | Reference for action arguments, not an autonomous executor under the magic pane. |
| LangGraph | Python graph runtime; model access is application-supplied (provider key or local endpoint) (README, 2026-09-24) | Partial: Jev can be a decision node, but does not satisfy the graph's model calls | reference-only | State graph resembles pane top-k plus validation, but duplicates the action registry. |
| openjev / owner-named line | DEMOTE: reachable public landing did not yield a stable README/dependency contract (attempt, 2026-09-24) | Unknown; do not assume TypeSafe compatibility | reference-only | Name alone supplies no concrete action surface. |

**Result:** three concrete components have all four fields; openjev is demoted rather than padded. No surveyed component plugs directly into TYPESAFE_KEY/KEY2 as a complete computer-use agent. The viable architecture is provider-neutral: Cua as substrate, TypeSafe for bounded typed ranking/validation, a normal provider or local model for general prose/computer-use reasoning, and goal:g1.25 as the sole propose-validate-execute registry. This also matches the magic-pane order: Jev proposes, registry validates, execution remains guarded.

## Evidence

- Synthesis: `.agi/context/local-maxxing/troves/2026-09-24-jev-survey/synthesis.md`.
- Context read: `hypothesis:lm-jev-cua-off-the-shelf-survey-against-action-registry-and-magic-pane`, `goal:g1.25`, `goal:g5.24.3`, `hypothesis:lm-cua-survey-locates-the-model-claim-and-runs-bench-headless`, `experiment:a00-778d86b3-170630`, `hypothesis:lm-jev-docs-hunt`, and the 2026-09-18 TypeSafe trove.
- No new live evidence: this is a public-doc reading digest; the cited prior Cua run is the only runtime evidence.

## Agent Notes
Public-docs digest covers three concrete components with all four fields; Cua, Browser Use, and LangGraph are adapt/reference-only, while openjev is demoted because its reachable public landing lacked a stable dependency contract. No live key or model call.
