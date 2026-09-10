---
id: hypothesis:l4-workflow-types-and-default-harness-are-a-geometry-node
mint_id: fe8602e02d6346d8ac8e6d46e1a0d547
type: hypothesis
parents:
  - goal:g1.14
next_edges: []
edited_by: belam-S1-L4-V
scaffold_hash: f4dd63acedf5f5fd
season: 2
testable_claim: "OWNER 2026-09-10 (verbatim in doc:l4-owner-decisions): 'the prime determines the default harness used to route various harness-agnostic functions but of course can be overridden per workflow and per workflow type as all workflow types should be in our .geometry node folder as some kinda config node'. TODAY: workflow.py resolves a workflow's harness as config row 'provider', else the manifest's 'provider', else the literal 'pi' (workflow.py:248) — ONE override level and a hardcoded default, with no notion of a workflow TYPE. CLAIM: a new node .agi/nodes/.geometry/workflows.md (config type, like crons.md, seats.md, ladder.md, commands.md — the shape this project already uses for everything whose edit-and-commit IS the change) declares (a) default_harness, owned by the prime and written only by the prime seat's actor; (b) a types list, each type naming its own harness override and the stage shapes it expects (e.g. review, drafting, research, investigate-refute); (c) per-workflow overrides keyed by registered name. RESOLUTION ORDER, testable: per-workflow override > per-type override > prime default > (no hardcoded fallback — refuse loudly and name the node). workflow.py run reads the node instead of the literal; workflow.py list prints the RESOLVED harness and which level it came from. Every registered manifest gains a 'type' that must name a declared type, and validate fails on an undeclared one. PROVED BY: the node exists and is committed; workflow.py list shows all six registered workflows resolving through it with the level named; flipping default_harness in the node and committing changes what --dry-run resolves for a workflow with no override, without touching any manifest; a manifest naming an undeclared type is refused by validate. DISPROVED BY: any code path that still reaches the literal 'pi' fallback after the node exists. HARD RULES: A NODE THE SUITE PINS IS CODE — run the suite after any .geometry write (trap 0al); workflow.py is build:bin-workflow, edit through write.py; the node is created with write.py create, never by hand; the prime is the only legitimate writer of default_harness and the schema should say so."
thought_session: f3b92df1
title: Workflow types, the prime-owned default harness, and its two override levels are one .geometry config node
---
<!-- BODY:BEGIN -->
# hypothesis:l4-workflow-types-and-default-harness-are-a-geometry-node

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
