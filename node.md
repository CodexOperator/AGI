---
id: hypothesis:lm-jev-cua-off-the-shelf-survey-against-action-registry-and-magic-pane
mint_id: 62f69083d3384af193796b0d8761c257
type: hypothesis
parents:
  - goal:g5.24.3
next_edges: []
edited_by: director-thought
falsifier: No surveyed component names a concrete integration path into goal:g1.25's action registry or goal:g5.24.3's magic pane (every row is 'skip' or 'reference-only') -- then the answer is genuinely 'nothing off-the-shelf plugs in directly' and the survey should say so plainly rather than force a recommendation; OR fewer than 3 components are surveyed with all four fields filled -- demote.
scaffold_hash: 0a63fc647a680048
season: 2
testable_claim: "A reading-digest survey (public docs/GitHub only, 0 USD spend) determines which off-the-shelf jev/cua components -- openjev, the trycua/cua line, and named peers -- can run on the two existing TypeSafe API keys (TYPESAFE_KEY, TYPESAFE_KEY2) or independently, and plug directly into this project's action registry (goal:g1.25) and magic pane (goal:g5.24.3): for each surveyed component the survey states what it needs (key type, hosting, install), whether TYPESAFE_KEY/TYPESAFE_KEY2 satisfy it or it needs something else, and a concrete integration recommendation (adopt as-is / adapt / reference-only / skip) with a one-line reason. A pass names at least 3 components with all four fields (needs, key-fit, recommendation, reason) filled; a component surveyed with a missing field is a demote of that row. CEILING: <=120 production lines."
tests: "ONE pi-free parent + kid(s) (owner 2026-09-24 20:3xZ: no Claude subagents, no Claude workflows -- ever), reading-digest shape: READ-ONLY web (curl -sL + python3 tag-stripping, same convention as hypothesis:lm-jev-docs-hunt) plus this box's own graph (doc:typesafe-ai-skill, the already-fetched TypeSafe docs trove, hypothesis:lm-cua-survey-locates-the-model-claim-and-runs-bench-headless and its experiment). No pip installs beyond what the prior cua-bench round already proved works, no new downloads, no paid API call, no TypeSafe key spend of any kind this round -- survey only. Kid(s) write a synthesis table: component | what it needs | TYPESAFE_KEY/KEY2 fit | recommendation | reason."
title: "Off-the-shelf jev/cua survey: openjev, trycua/cua and peers, against the two existing TypeSafe keys and the action registry + magic pane"
town: local-maxxing
---
# hypothesis:lm-jev-cua-off-the-shelf-survey-against-action-registry-and-magic-pane

## Measured
- doc:typesafe-ai-skill: TypeSafe (typesafe.ai) serves model `jev-latest` via `POST /v1/systemone`, typed judgments only (noul/choice/score), $0.045/1M input tokens, output free. "Jev" throughout this town's graph traces to this model.
- MAIN .env carries exactly two TypeSafe-shaped credentials by NAME: `TYPESAFE_KEY`, `TYPESAFE_KEY2` (confirmed 2026-09-24 by director-thought gen 24, names only, no value read) -- no key literally named JEV or CUA exists, matching TMM.134's own framing.
- goal:g5.24.3 (magic pane): "Side-track authorization... 'run jev and openjev research on the side to progress on the magic pane trajectory'"; "'openjev' (the trycua/cua open-source jev line the owner pointed at 2026-09-18) rides as a second kid... a reading digest, not a new sub-sub-goal."
- goal:g1.25 (action registry, minted TODAY 2026-09-24 20:3xZ): "an ACTION REGISTRY = every engine action as a typed entry, the ONE choice set jev reads · commands.py = a lightweight query + parse layer over the registry... compatible with off-the-shelf libraries that turn python scripts into CLI commands dynamically via templates."
- hypothesis:lm-cua-survey-locates-the-model-claim-and-runs-bench-headless (this town, prior round) already proved Cua Bench's `cb interact` path runs headless on THIS box, 0 USD, no API key, no model bytes, reward 1.0 (experiment:a00-778d86b3-170630) -- and its typed-action trajectory already maps onto jev's `acts_replay.jsonl` schema (9 named keys). Do not re-run this smoke; cite it.
- hypothesis:lm-jev-docs-hunt (retired, incomplete): 3 kid digests on TypeSafe docs already landed uncommitted-synthesis at .agi/context/local-maxxing/troves/2026-09-18-typesafe/{concepts-api,recipes-integrations,pricing-legal,pricing-terms,recipes-sdks}.md (~62KB) -- read these before any new web fetch on TypeSafe itself; the gap this round fills is openjev/cua-and-peers against the CURRENT action-registry + magic-pane shape, which did not exist when that round ran.

## CLAIM
See testable_claim in full (frontmatter).

## Dispatch line
config-max: none identified yet -- the survey itself may surface one (e.g. a provider row for typesafe.ai) and should name it if so, not silently skip it.
template-max: none.
code: none -- this is a reading-digest round, no code changes beyond a tiny synthesis script if needed.

## FALSIFIERS
See falsifier (frontmatter).

## TESTS
See tests (frontmatter).

## FILE SCOPE
.agi/context/local-maxxing/troves/2026-09-24-jev-survey/ (new, repo-tracked) for the kid's own synthesis output, plus
READ-ONLY reads of: .agi/context/local-maxxing/troves/2026-09-18-typesafe/*, .agi/context/local-maxxing/papers/typesafe-ai.md,
goal:g1.25.md, goal:g5.24.3.md, hypothesis:lm-cua-survey-locates-the-model-claim-and-runs-bench-headless.md,
experiment:a00-778d86b3-170630.md, doc:l5-owner-decisions.md (API key names), MAIN .env (grep key NAMES only, `^[A-Z0-9_]+=`,
never a value). No config/extensions changes. No pip installs, no downloads, no GPU, no paid API call, no TypeSafe key
spend of any kind this round.

## CEILING
<=120 production lines (synthesis + any tiny probe script; fixture/selftest excluded); 0 USD OpenRouter for the round's
own tokens (pi-free); $0 compute; no live call against TYPESAFE_KEY/TYPESAFE_KEY2 or any paid API this round -- survey
and recommend only, a future batch spends if the owner approves a specific component.
