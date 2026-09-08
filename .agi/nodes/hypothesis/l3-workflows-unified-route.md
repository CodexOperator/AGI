---
id: hypothesis:l3-workflows-unified-route
mint_id: 6131272da9cc4bf2ace1737abc14f431
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-X
scaffold_hash: dd991344295decab
season: 2
testable_claim=After: the change, workflow.py gains register and list verbs so an inline script becomes a registered manifest pair under extensions/agi/workflows/ in the same action that runs it, workflow.py run is the only sanctioned dispatch route for every workflow including review and drafting, and a test fails when any agi-*.js exists without a sibling manifest or when a manifest names stages the script does not implement; proven by red-first tests for the registry invariant plus a real register-then-run round trip of a script that started life inline
thought_session: belam-S1-L3-X
title: A workflow written inline exists only for one session and runs on one harness; make registration happen as it runs and make workflow.py run the only route
---
<!-- BODY:BEGIN -->
# hypothesis:l3-workflows-unified-route

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

OWNER ASK, 2026-09-08, verbatim: "Make sure all workflows are added to there as they run and are then always dispatched from the unified route. As always everything unified."

WHAT WENT WRONG, CONCRETELY, IN THE SESSION THAT MINTED THIS. A prime director needed a multi-lens investigation, wrote a workflow inline as a Claude Code script, ran it, and got a genuinely load-bearing answer out of it — including one finding larger than the question it was asked. That script lived in a session scratch directory under a generated run id. It ran on exactly one harness. It would have evaporated with the session. The project already owns the cure and did not reach for it: `extensions/agi/bin/workflow.py` is the harness-agnostic runner, and `review` and `drafting` are already registered as manifest pairs under `extensions/agi/workflows/`. Nothing made registration happen, so it did not happen. That is the whole defect: the unified route exists and is optional.

THE PRINCIPLE, in the owner's terms and in this project's. Everything unified. It is the same move `goal:g11` made when it deleted the payload staging pipeline, the same move `bin/locations.py` made when it replaced every project-name branch with one resolver: ONE route, no second path that happens to also work. A second working path is not redundancy, it is the thing that goes stale, and here it is worse than stale — the second path is per-session and evaporates.

WHAT TO BUILD, in `extensions/agi/bin/workflow.py`, additively.
1. **`workflow.py register <name> --script <path> [--from-run <dir>]`** — lands an inline script as a proper manifest pair under `extensions/agi/workflows/`: the `.js` copied in as `agi-<name>.js`, and a `<name>.json` stage manifest derived from it, following the shape `review.json` and `drafting.json` already use. Derive what you can from the script (stage labels, schemas) and leave honest TODO markers for what you cannot rather than inventing values. It must refuse to silently overwrite an existing registration.
2. **`workflow.py list`** — what is registered, with each row's script, stage count and the harness its config row defaults to. A registry nobody can enumerate is a registry nobody trusts.
3. **The invariant, as a test that fails loudly.** A `agi-*.js` under `extensions/agi/workflows/` with no sibling `<name>.json` is an error; a `<name>.json` naming stages the script does not implement is an error. Red-first, both directions.
4. **Make `run` the only sanctioned route in the documents directors actually read.** One paragraph in `skills/agi/SKILL.md` stating the rule: a workflow is registered as it runs, and every dispatch goes through `workflow.py run <name>`; writing one inline without registering it is the failure this closes. Keep it short — that file is read by every agent and every line costs.

DO NOT change how `run` resolves the existing `review` and `drafting` rows, and do not rewrite either of their manifests: they are the working reference and a regression there is invisible until a round needs them. Do not touch `extensions/agi/workflows/deep-search.json` or `agi-deep-search.js` — a parent is building those right now and they are the first customer of your `register` verb, not your files. Do not edit `rotate.py`, `cli.py`, `dispatch.py` or `zoom.py`. Do not write `.agi/nodes/.geometry/seats.md`. Do not kill any `belam-*` tmux window.

PROVE IT IN THIS SAME RUN. A real round trip: take a small script that starts life inline, `register` it, `list` it, then `run` it with `--dry-run` on BOTH `--harness pi` and `--harness claude-code`, and paste the actual commands and their actual output into your node. Then show the invariant test failing red before your change and green after. A registry verb that has never registered anything is prose.
