---
id: hypothesis:l3-deep-search-workflow-harness-agnostic
mint_id: 4973aeac875c41ecb74677c92e92cc63
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-X
scaffold_hash: 4dcad74a9b8c5878
season: 2
testable_claim=After: the change, extensions/agi/workflows/deep-search.json and extensions/agi/workflows/agi-deep-search.js exist and are driven entirely by --args (question, facts, lenses, refute_n), with NO investigation-specific text baked into either file; python3 extensions/agi/bin/workflow.py run deep-search --dry-run prints one resolved dispatch per stage under BOTH --harness pi and --harness claude-code; and one real end-to-end run through the pi harness returns a ranked mechanism list for a question supplied purely through --args. Proven by red-first tests for the manifest contract plus the two dry-runs and the one live run captured as output
thought_session: belam-S1-L3-X
title: The deep-search investigation loop exists only as an ad-hoc Claude-Code script bound to one question; register it as a parameterized workflow both harnesses can run
---
<!-- BODY:BEGIN -->
# hypothesis:l3-deep-search-workflow-harness-agnostic

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

OWNER ASK, 2026-09-08, verbatim: "Add the deep search workflow as part of the improved deep research loop to be made harness agnostic."

WHY THIS EXISTS. The multi-lens investigation loop works and has already paid for itself, but it exists only as a one-off Claude Code script written inline by a prime director to answer ONE question (why a `--branch` kid writes source into the main checkout). Its shape is: fan out N independent readers, each given a DIFFERENT lens on the same ground truth; hand every finding that claims to explain the phenomenon to an adversarial refuter told to default to refuted; then synthesize the survivors into a ranked list with a fix and a red-first test. That shape is general. Its current implementation is not: the question, the ground truth and the five lenses are hardcoded in the script, and it can only run through the Claude Code Workflow tool, which means it cannot run on a pi round, cannot run when the subscription is at its limit, and disappears the moment the session that wrote it ends.

THE INFRASTRUCTURE IS ALREADY THERE — DO NOT BUILD A SECOND ONE. `extensions/agi/bin/workflow.py` is the harness-agnostic runner (`hypothesis:l3w4-workflows-config-maxxed`). It already resolves a stage manifest by path — `extensions/agi/workflows/<name>.json` — reads model and effort knobs from `.agi/config.json` under `workflows.<name>`, and takes `--harness {pi,claude-code}`, `--args JSON` and `--dry-run`. Two workflows are registered this way already: `review` (`review.json` + `agi-round-review.js`) and `drafting` (`drafting.json` + `agi-brief-drafting.js`). READ BOTH before you write anything. Your job is a third registration in exactly that idiom, not a new mechanism.

WHAT TO BUILD.
1. `extensions/agi/workflows/deep-search.json` — the stage manifest. Stages: a READ stage that fans out one agent per lens; a REFUTE stage that takes each finding claiming to explain the phenomenon and tries to kill it; a SYNTHESIZE stage that ranks survivors. Each stage carries its `label`, `role`, `model_hint`, `effort_hint`, `prompt` and inline JSON `schema`, the same as `review.json`.
2. `extensions/agi/workflows/agi-deep-search.js` — the Claude Code script for the claude-code harness, matching the manifest stage for stage.
3. Whatever minimal `.agi/config.json` key the runner needs under `workflows.deep-search`, following the existing rows.

THE ONE PROPERTY THAT MATTERS MOST: **NO investigation-specific text may appear in either file.** The question, the ground-truth facts, the lens list and the number of refuters all arrive through `--args`. Concretely, `--args` should carry at least `question` (what is being investigated), `facts` (measured ground truth the agents must explain rather than re-litigate), `lenses` (a list of named reading angles, each with its own instruction) and `refute_n`. A reader must be able to point this at a completely unrelated question — a performance regression, a flaky test, a security question — without editing a single file. If you find yourself typing the word "worktree" or "isolation" into either artefact, you have hardcoded the example instead of building the tool.

TWO DESIGN NOTES FROM THE INSTANCE THAT PROVED THE SHAPE, both worth preserving because each caught something. First, the refuter is told to DEFAULT TO REFUTED when uncertain — an agent asked to "check" a finding confirms it, and an agent asked to kill it does the work. Second, the readers are deliberately given DIFFERENT lenses rather than the same prompt N times: redundancy finds the same thing N times, diversity finds N different things. Preserve both as manifest defaults, and let `--args` override.

THEN PROVE IT, IN THIS SAME RUN, ON BOTH HARNESSES — this is the whole point of the brief and a proof on one harness is not a proof.
(a) `python3 extensions/agi/bin/workflow.py run deep-search --dry-run --harness pi --args '<a small question of your choosing with two lenses>'` prints one resolved dispatch per stage, with the model each stage resolved to, and spawns nothing.
(b) The same command with `--harness claude-code`.
(c) ONE real end-to-end run through the pi harness, on a question supplied entirely through `--args`, returning a ranked list. Pick something small and genuinely unknown so the run means something; do not re-run the branch-isolation question, which is already being answered elsewhere.
Paste the commands and their real output into your node. A dry-run that was never executed is prose.

DO NOT: edit `extensions/agi/bin/rotate.py`, `cli.py`, `dispatch.py` or `zoom.py` — three other agents hold those files this round and two of them are mid-flight; write `.agi/nodes/.geometry/seats.md`; kill any `belam-*` tmux window; or change how `workflow.py` resolves the existing `review` and `drafting` rows. Additive only.
