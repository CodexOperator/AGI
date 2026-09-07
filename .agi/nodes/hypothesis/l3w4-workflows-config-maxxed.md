---
id: hypothesis:l3w4-workflows-config-maxxed
mint_id: fc8d4e4151da4891bfd05fdff1005de4
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-IV
scaffold_hash: 459d689411983b9f
season: 2
testable_claim: Both workflow scripts are build nodes under extensions/agi/workflows/ symlinked from .claude/workflows/, read model/effort/provider from .agi/config.json workflows.<name> with args overriding, and workflow.py run <name> --harness pi executes the same stages through dispatch.py kids; proved by a dry run on both harnesses and red-first tests.
thought_session: L3.24
title: Workflows live in the graph, config-maxxed, on any harness
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-workflows-config-maxxed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CLAIM
Both workflow scripts live in the graph as build nodes — `extensions/agi/workflows/agi-round-review.js` and `extensions/agi/workflows/agi-brief-drafting.js`, symlinked from `.claude/workflows/` so `Workflow({name})` resolves them — read every knob from `.agi/config.json` `workflows.<name>` (model, effort, provider/harness, minion count) with per-run args overriding, and a harness-agnostic runner `extensions/agi/bin/workflow.py run <name> [--harness claude-code|pi] --args JSON` executes the same stages (fan-out, schema-validated returns, critic or global-checks step) through `dispatch.py` kids when the harness is not Claude Code. Proved by a dry run on both harnesses and red-first tests.

WHY
Owner to Belam IV, 2026-09-07 15:10 UTC, verbatim: "that workflow script needs to be in graph. All workflows need to be symlinked to agi repo workflow directory. This is a clear "graph has everything you need" violation" and "it also needs to be config-maxxed so it can be ran on other harnesses as well". Belam IV moved both scripts into the repo at 15:12 UTC (the review script verbatim from Belam II's session dir; the drafting script from Belam III's, parameterized so briefs, scratch dir, owner-section pointer, model and effort come from args) and symlinked them from `.claude/workflows/`. The config row `workflows.drafting` exists (owner quote 6) but neither script reads it, and both run only as Claude Code Workflow scripts — a Bug Master or drafter seat on pi cannot run them at all.

FILES
extensions/agi/workflows/agi-round-review.js, extensions/agi/workflows/agi-brief-drafting.js (in the repo since 15:12 UTC; build nodes minted by the next smoke)
.claude/workflows/agi-round-review.js, .claude/workflows/agi-brief-drafting.js (relative symlinks)
.agi/config.json :: workflows (add `review`; every row {model, effort, provider, minions})
extensions/agi/bin/dispatch.py :: kid fan-out (a brief plus a JSON return contract)
extensions/agi/bin/workflow.py NEW, extensions/agi/tests/test_workflow.py NEW
QUICKSTART.md install table (a `.claude/workflows` symlink row beside the skill and CLI symlinks), skills/agi/SKILL.md CLI table

DESIGN (director proposal)
A workflow is a list of stages {label, prompt template, JSON schema, role: drafter|critic|reviewer|global}. Keep the stage definitions in one form both runners read — `extensions/agi/workflows/<name>.json` — so the .js script (Claude Code: `agent()` per stage) and `workflow.py` (any harness: one `dispatch.py` kid per stage whose brief is the prompt and whose done-contract returns the JSON, validated by the runner) execute identical stages. Model/effort/provider resolve config row → args override, never a literal in the script. Concurrency and the read-only rules stay in the prompt text.

TESTS (red-first)
test_workflow_config_row_overrides_script_defaults; test_named_workflow_symlinks_resolve_to_repo_files; test_runner_pi_harness_dry_run_prints_one_dispatch_per_stage; test_stage_return_is_schema_validated; test_review_and_drafting_stage_json_matches_js_prompts.

GATE
`Workflow({name: 'agi-round-review'})` resolves through the symlink; `workflow.py run review --harness pi --dry-run` prints one dispatch per stage with the configured model; changing the config row flips the model with no script edit; full suite green; no live spawn.

NOT IN SCOPE
The Bug Master and drafter SEATS that summon these (`l3w4-bug-master-seat`, `l3w4-drafter-seat`); the review content rules; per-parent branches (`l3w4-parent-branch-merge-up`).

SOURCE
Owner messages to Belam IV, 15:10 UTC (HANDOFF §6 item 22); owner quote (6) in `doc:l3-command-ladder-brief`; vision:alive addendum (quote 8: atomic, reusable, composable, config maxxing).

MEASURED (Belam IV, 2026-09-07 15:58 UTC): with the relative symlinks .claude/workflows/agi-round-review.js and agi-brief-drafting.js in place (commit b7f591371), Workflow({name: 'agi-round-review'}) returned 'Workflow agi-round-review not found. Available: deep-research' — the name registry did not see them (possibilities to test: the registry is read once at session start; symlinks are not followed; a different filename or a .md manifest is expected; the user-level ~/.claude/workflows/ dir is the one scanned). Running by scriptPath from the repo works. The kid must find the real resolution rule and make the install row match it; until then callers pass scriptPath=extensions/agi/workflows/<name>.js.
