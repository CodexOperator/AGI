---
id: hypothesis:l3-dispatch-harness-flag-overridden
mint_id: cee0122553c8485aaac3acd9ba175fb4
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-V
scaffold_hash: 6424c41aac22ffdf
season: 2
testable_claim: After the fix, dispatch.py . X --tier parent --harness claude-code --dry-run prints harness=claude-code with a claude command and a claude-code model for the tier (the ladder row's pi model is NOT applied), a red-first test pins that an explicit --harness wins over the ladder row's harness, and a second test pins that without --harness the ladder row still wins; a --seat row keeps winning over both.
thought_session: L3.28
title: Explicit --harness is silently overridden by the ladder row
---
<!-- BODY:BEGIN -->
# hypothesis:l3-dispatch-harness-flag-overridden

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
MEASURED (Belam V, 2026-09-07 17:40 UTC): L3.26 p-pinpath2 was dispatched with --harness claude-code (Belam IV's intent, HANDOFF L3.26 row: the sonnet-kid fallback after two pi probes) yet the manifest shows all six L3.26 agents harness: pi. Reproduced dry: dispatch.py . L3.27 --target hypothesis:l3-rotate-pin-path-readback --level small --tier parent --harness claude-code --dry-run prints 'roles: tier=1 role=parent -> pi/~z-ai/glm-flash-latest' then '[dry-run] slot=0 harness=pi'. CAUSE: dispatch.py main(), the block after adapters.resolve(cfg, args.harness) (about L699-708, hypothesis:l3w0-ladder-roles-table): when the ladder row names a harness that differs from the resolved one, the row's harness replaces the CLI harness unconditionally, so an explicit flag is lost with no message. FIX SHAPE (explicit beats declared): when args.harness is given, keep it, take the harness's own models for the tier and drop the ladder row's model/effort/settings (they belong to the other harness), print one notice line naming both; without the flag the ladder row keeps winning; a --seat row (also explicit) keeps winning over both. Red-first tests in tests/test_dispatch*.py through --dry-run. WHY IT MATTERS: owner rule HANDOFF section 6 item 14 makes --harness claude-code (opus parents / sonnet kids, lowest effort) the fallback when OpenRouter runs to its reserve; today that fallback cannot be selected from the CLI at all, and a third pi probe ran where a claude-code kid was intended. Files: extensions/agi/bin/dispatch.py, extensions/agi/tests/test_dispatch.py (or the dry-run test file). Output must be atomic and reusable: one resolution function harness_for(args, spec, cfg) that every spawn path calls.

L3.28 review (Belam V, 19:30 UTC): experiment:a00-db75bb99-6d7472 proved 0.9 accepted — red-first flip reproduced by stashing dispatch.py; seat > flag > ladder order pinned. GAP left open: the fix is inlined in main()'s block; the brief asked for one atomic harness_for(args, spec, cfg) that every spawn path calls — extract it when dispatch.py is next touched (parent-branch --branch path and the kid re-dispatch path should route through it too).
