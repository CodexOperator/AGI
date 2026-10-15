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
testable_claim: "dispatch.py --tier kid --dry-run with no --harness and AGI_HARNESS naming a harness row marked \"zero_usd\": true (pi-free, pi-local) reports that harness with its own kid model; an explicit --harness still wins; AGI_HARNESS=pi or claude-code (no zero_usd cell) still resolves the ladder's tier-0 kid row."
title: A kid dispatched with no --harness under a 0-USD parent (pi-free / pi-local) inherits that harness, not the ladder's tier-0 kid row (0-credit leaf 2/2 of open item (2))
town: local-maxxing
---
# hypothesis:a-kid-under-a-credential-none-parent-inherits-its-harness-not-the-ladder-row

## Measured
- TMM.107 (05:19Z 09-24): dispatch.py:2656 EXPORTS AGI_HARNESS (a00-0d0977d3 proved that half) and nothing READS it -- EF.104's
  kid a00-beccdfa1 ran harness=pi / deepseek because its pi-free parent's spawn line dropped --harness pi-free.
- no --harness: adapters.resolve(cfg, None) at dispatch.py:1947 takes spawn.harness "pi" (config.json:136), and the tier-0 kid
  row (ladder.md:43: pi, deepseek) wins through resolve_role_spec (:1955) and the from_ladder branch (:1963).
- an explicit --harness already beats the ladder row and takes that harness's own tier model (:1972-1983); args.harness is read
  only at :1947 and :1961.
- no row cell marks a 0-USD harness: pi-free (config.json:79) = openrouter + stealth/space-bunny-alpha with no credential cell
  (it mints); pi-local = credential "none"; pi = openrouter + deepseek (paid). A credential-"none" key misses pi-free, and a
  harness-name key is banned (test_adapters.py:205-216).
## CLAIM
When args.harness is None, args.tier is "kid", no --seat is given, and AGI_HARNESS names a cfg["harnesses"] row carrying
"zero_usd": true, main() sets args.harness to that name ahead of :1947 and prints ONE line naming the inheritance; the existing
explicit-flag branch (:1972-1983) then takes that harness's own kid model. An explicit --harness or --seat still wins; an
AGI_HARNESS row without the cell (pi, claude-code, copilot-cli, grok-bot) or an unknown name changes nothing -- no silent upgrade
to a pricier harness.
## Dispatch line
config-max: "zero_usd": true on the pi-free and pi-local rows of .agi/config.json (one cell each; the cell IS the key) /
template-max: none (brief.py untouched) / code: dispatch.py main(), ~8 lines ahead of :1947, keyed on the row's zero_usd cell,
NEVER on a harness name (test_adapters.py:205-216)
## FALSIFIERS
- AGI_HARNESS=pi-free with no --harness: the dry run prints harness=pi, or its command: line carries a deepseek model
- AGI_HARNESS=pi or AGI_HARNESS=claude-code moves a kid off the ladder row
- an explicit --harness under AGI_HARNESS=pi-free resolves anything but that flag
- test_adapters.py::test_dispatch_is_not_keyed_on_any_harness_name red, or grep -c '"pi-free": {' .agi/config.json != 1
## TESTS
test_dispatch_dry_run.py::test_a_kid_under_a_zero_usd_parent_inherits_its_harness -- ONE test, three arms (TMM.107: "one test pins
all three"); the file's CONFIG plus a zero_usd row; `_run(--tier kid --target hypothesis:x --dry-run)`: (1) AGI_HARNESS=<the
zero_usd row>, no --harness: rc 0, "harness=<row>" in stdout, the command: line carries the row's kid model and no "deepseek" (red
today); (2) the same env plus an explicit --harness: that flag wins; (3) AGI_HARNESS=pi, then AGI_HARNESS=claude-code: the ladder
kid row exactly as today (deepseek on the command: line). Assert on the command: line only (the roles: line still names the ladder
row). Neighbours: test_adapters.py, test_credential_none_spawn.py, test_dispatch.py.
## FILE SCOPE
.agi/config.json -- the pi-free and pi-local rows, +1 cell each, nothing else
extensions/agi/bin/dispatch.py 1940-1950
extensions/agi/tests/test_dispatch_dry_run.py -- the one new test and its fixture row
## CEILING
1 kid, dispatched DIRECTLY by the director (TMM.107 (3): no parent, the literal --tier kid --harness pi-free) · 10 production
lines + 2 config cells · 0 USD
RESIDUE (named, not this leaf's): a parent started before the export leaf has no AGI_HARNESS; restart (pi_adapter.py:337) and heal
(heal.py:95-101, the ladder kid row) bypass both leaves; the dry-run report (dispatch.py:1383-1449) does not show AGI_HARNESS.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
TMM.107 (05:19Z 09-24) released this held leaf (EF.92 LH-2) as the next batch's ONE item and widened it to "a parent whose AGI_HARNESS is a 0-USD harness (pi-free / pi-local)". The previous key (credential "none") covered pi-local only -- its own RESIDUE named pi-free uncovered, and EF.104's kid then ran paid under a pi-free parent. Measured: no row cell marks 0-USD (pi-free carries no credential cell) and a harness-name key is banned, so the key becomes a new zero_usd row cell (config-max) and the TESTS gain TMM.107's three arms in one test. Citations re-checked on 3272d4e001: config.json:135 -> :136; the name-literal guard test_adapters.py:192-203 -> :205-216 (EF.101-104 added argv tests above it). Dispatched as EF.105, a DIRECT kid per TMM.107 (3).
<!-- THOUGHT:END -->
