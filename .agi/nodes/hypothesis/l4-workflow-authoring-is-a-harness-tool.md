---
id: hypothesis:l4-workflow-authoring-is-a-harness-tool
mint_id: 5681dafb92b44f4a96f45f66475a7fbd
type: hypothesis
parents:
  - goal:g1.14
next_edges: []
edited_by: belam-S1-L4-V
scaffold_hash: 9ed3db18b65ba36c
season: 2
testable_claim: "OWNER 2026-09-10 (verbatim in doc:l4-owner-decisions): 'do you create workflows on the fly? If so that needs to be a harness tool as well that is dynamically routed across whatever harness is used by the prime.' The answer was yes and the instance was the Prime's own: workflow prime-open-questions was authored inline through the Claude Code Workflow tool, ran six agents, and was registered only afterwards — and register wrote a manifest whose four stage prompts are literally '<TODO: author the stage prompt...>' with a '<TODO>' repeat key, so the pair exists but CANNOT run on pi. CLAIM: workflow.py gains an 'author' verb that takes a stage list (JSON, path or stdin) and writes BOTH halves of a runnable pair in one action — the <name>.json manifest with real prompts AND the agi-<name>.js script generated FROM the manifest, not the other way round — so that the manifest is the source and the script is derived, and a pi parent with no Claude Code tool can author a workflow that a Claude Code session can then run unchanged. PROVED BY: (1) prime-open-questions rewritten through the new verb into ONE repeated 'investigate' stage over an args list of questions plus ONE repeated 'refute' stage, workflow.py validate green, and workflow.py run prime-open-questions --harness pi --dry-run resolving every stage with a non-TODO prompt; (2) the same manifest driving --harness claude-code --dry-run; (3) register's TODO skeleton path either removed or made to refuse with a message naming the author verb, because a skeleton that lists as registered is a registry that lies about what it can run. DISPROVED BY: any registered pair after this round whose manifest still carries a <TODO> prompt, or a script whose stage labels disagree with its manifest. HARD RULES: workflow.py is build:bin-workflow — edit it through write.py; a new bin/*.py enrols in test_bin_help_smoke, so this is a VERB not a file; keep validate's invariant exactly as strong as it is."
thought_session: f3b92df1
title: Authoring a workflow on the fly is a harness tool, routed like any other — not a Claude Code privilege
---
<!-- BODY:BEGIN -->
# hypothesis:l4-workflow-authoring-is-a-harness-tool

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER CONSTRAINT ADDED 2026-09-10 ~21:0xZ (verbatim in doc:l4-owner-decisions): 'If it's to Claude code it should render the same as native workflows so basically use the native tooling of whatever harness the workflow gets routed through.' This is a hard constraint on the claim, not a preference: the generated agi-<name>.js MUST be a real Claude Code Workflow script — meta block, phase() calls, agent()/pipeline() — so that workflow.py run <name> --harness claude-code lands in the native Workflow tool and renders in /workflows exactly like a natively authored one, with its journal and resume intact. On pi the same manifest drives dispatch.py kids as today. A runner that executes the manifest itself on Claude Code instead of handing it to the native tool FAILS this round even if every stage completes.
