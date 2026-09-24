---
id: hypothesis:a-kid-under-a-credential-none-parent-inherits-its-harness-not-the-ladder-row
mint_id: 22a198fb64f34ac98f30616eeb209c41
type: hypothesis
parents:
  - goal:g5.27
next_edges: []
edited_by: director-engine
scaffold_hash: b4901f1231be6330
season: 2
testable_claim: dispatch.py --tier kid --dry-run with no --harness and AGI_HARNESS naming a credential-none row reports that harness with the row's own provider and kid model, while AGI_HARNESS=pi still resolves the ladder's tier-0 kid row.
title: A kid dispatched with no --harness under a credential-none parent inherits that harness, not the ladder's tier-0 kid row (0-credit leaf 2/2 of open item (2))
town: local-maxxing
---
# hypothesis:a-kid-under-a-credential-none-parent-inherits-its-harness-not-the-ladder-row

## Measured
- brief.py:1930 -- the parent brief's kid-spawn line carries no --harness, so adapters/__init__.py:163 takes spawn.harness "pi"
  (config.json:135) and the tier-0 kid row (ladder.md:43: pi, deepseek) wins through dispatch.py:1955 (resolve_role_spec,
  :1111-1115) and :1963-1989 -- how MP02-G.01's kids ran on OpenRouter under a pi-local parent (TMM.41).
- dispatch.py:1971-1979 already lets an explicit --harness beat the ladder row and take that harness's own tier model; args.harness
  is read only at :1947 and :1961.
- "credential-none" is the harness ROW cell (config.json:68; pi_adapter.py:372); claude_code / copilot_cli / grok_bot adapters'
  needs_credential() always return False, so `not needs_credential()` would move every claude-code parent's kids off the ladder.
- no test spawns a kid without --harness under a credential-none parent (test_dispatch.py:796-945, test_dispatch_dry_run.py:274-321,
  test_credential_none_spawn.py:237-293, test_adapters.py:285-343); on 66e3dd68c7 test_dispatch_dry_run.py 27 passed,
  test_credential_none_spawn.py 12 passed.
## CLAIM
When args.harness is None, args.tier is "kid", and AGI_HARNESS names a cfg["harnesses"] row whose credential is "none", main()
sets args.harness to that name before :1946 and prints ONE line naming the inheritance; the existing explicit-flag branch then uses
that harness's own kid model and mints no key. An explicit --harness or --seat still wins; any other AGI_HARNESS changes nothing.
## Dispatch line
config-max: none (ladder.md, config.json untouched) / template-max: none (brief.py untouched) / code: dispatch.py main(), ~10
lines between :1940 and :1946 -- keyed on the row's credential cell, NEVER on a harness name (test_adapters.py:192-203)
## FALSIFIERS
- the pi-local dry run still prints harness=pi, or its command: line still carries a deepseek model
- AGI_HARNESS=pi or AGI_HARNESS=claude-code moves a kid off the ladder row
- test_adapters.py:192 red (a harness-name literal or `harness == ` in dispatch.py code)
## TESTS
test_dispatch_dry_run.py::test_kid_under_a_credential_none_parent_inherits_its_harness -- rewrite config.json as CONFIG plus a
"pi-local" row {adapter pi, provider local-town, credential none, models {kid: <the local model id>}, allowed_extra [same]}; (1)
`_run(--tier kid --target hypothesis:x --dry-run)` with AGI_HARNESS=pi-local: rc 0, "harness=pi-local" in stdout, the command:
line carries "--provider local-town" and the local model, no "deepseek" (red today); (2) AGI_HARNESS=pi: "harness=pi " and
"deepseek" on the command: line. Assert on the command: line only (the roles: line still names the ladder row).
Neighbours: test_adapters.py, test_credential_none_spawn.py, test_dispatch.py.
## FILE SCOPE
extensions/agi/bin/dispatch.py 1937-2004
extensions/agi/tests/test_dispatch_dry_run.py 29-96, 274-303
extensions/agi/tests/test_adapters.py 192-203
## CEILING
1 kid under a pi-free parent (STANDARD round: --tier parent --harness pi-free, --harness pi-free on every kid spawn; TMM.89) · 10 production lines · 0 USD · SECOND (after the AGI_HARNESS export leaf merges)
RESIDUE (named, not this leaf's): pi-free is NOT covered -- its row (config.json:78-91) has no credential cell, so it mints and this leaf's credential-"none" key skips it: a pi-free parent's kid spawned without --harness still resolves the ladder's tier-0 kid row (ladder.md:43, pi / deepseek, paid, held), and the orders' explicit --harness pi-free is the only guard; a parent started before the export leaf has no AGI_HARNESS; restart (pi_adapter.py:337) and heal
(heal.py:95-101, the ladder kid row) bypass both leaves; the dry-run report (dispatch.py:1383-1449) does not show AGI_HARNESS.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Measured re-checked against e7910a90ab before dispatch (02:5xZ 09-24): two citations drifted, content unchanged -- spawn.harness moved config.json:121 -> :135 (the pi-free row now sits at 78-91), and EF.90 added test_live_spawn_exports_its_own_harness_over_an_inherited_one at :261, so the no-bare-kid-spawn span is 237-293; that test passes --harness pi-local, so 'no test spawns a kid without --harness' still holds (13 tests in the file on this base, 12 on 66e3dd68c7). Claim, tests and file scope unchanged; the previous version's CEILING + pi-free RESIDUE stand.
<!-- THOUGHT:END -->
