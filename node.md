---
id: experiment:a00-938e7071-0a463d
mint_id: 5fbb77b98c394336b893f598ec8b3d75
type: experiment
parents:
  - hypothesis:l3w3-advisor-brief
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-938e7071-0a463d
loop: hypothesis:l3w3-advisor-brief@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 71a7f6d5002bcfe3
season: 2
title: A00 938e7071 0a463d
verdict: pending
---
# experiment:a00-938e7071-0a463d

## Experiment

**Testable claim (hypothesis:l3w3-advisor-brief):** brief.py assembles a tier-3
advisor brief for the claude-code parent role (opus 5, max, ultracode) that
carries the head, the full body of the one vision node the advisor embodies,
its seat in the standing room tier3-quorum, the audience rule for the prime,
and the primitive to spawn a Fable-max perpetual-goal director; and a dry
dispatch prints the resolved command with the ultracode env export.

Verification questions posed to the live code (no live spawn):

**Q1 — does an "advisor" brief tier exist at all?**
```
$ python3 -c "import brief; print(brief.assemble(tier='advisor', agent_id='a00-t', iter_n=1))"
BriefError: no brief for tier 'advisor'; known tiers: kid, parent, director, prime_director.
A tier with no brief must fail here rather than fall back to another tier's job description (goal:g1.9).
known tiers: ('kid', 'parent', 'director', 'prime_director')
```
`brief.TIERS = ('kid', 'parent', 'director', 'prime_director')`. There is **no
`advisor` tier**. `assemble(tier="advisor")` raises `BriefError`.

**Q2 — does the PARENT brief carry the advisor content (vision body, quorum,
audience, Fable spawn), even when aimed at a vision node?**
```
brief.assemble(tier='parent', target='vision:alive', ...)  →  parent brief
  'vision:alive named': True        # only as "TARGET: vision:alive"
  'tier3-quorum room': False
  'audience rule (prime)': False
  'Fable-max perpetual director': False
  'perpetual goal director': False
  'enshrine vision body': False
```
The parent brief names the target as a TARGET line only. It does **not** embed
the vision node's body, does not seat the advisor in `tier3-quorum`, does not
state the `send.py audience prime` rule, and does not carry the primitive to
spawn a Fable-max perpetual-goal director. `assemble()` takes no ladder-tier
argument at all — the brief is tiered by role (`parent`), so no "tier-3"
variant of the parent brief exists in `brief.py`.

**Q3 — does dispatch resolve the tier-3 parent row (opus 5, max, ultracode)?**
```
$ python3 extensions/agi/bin/dispatch.py . 1 --list-rows
ladder roles table: 7 rows
tier=3 role=prime_director  harness=claude-code model=claude-fable-5-1  effort=max  settings=ultracode
tier=3 role=parent          harness=claude-code model=claude-opus-5     effort=max  settings=ultracode
tier=1 role=director        harness=claude-code model=claude-fable-5-1  effort=max  settings=-
...
```
The ladder `roles:` table (`.agi/nodes/.geometry/ladder.md`) declares the
tier-3 parent row; `dispatch.resolve_role_spec` resolves it to
`claude-opus-5 / max / ultracode`. This half **works**.

**Q4 — does the claude-code adapter emit the ultracode settings/env?**
`adapters/claude_code_adapter.py`: `settings: ultracode` → `--settings
'{"ultracode":true}'`, and `_tier_is_ultracode` → `CLAUDE_CODE_WORKFLOWS=1` is
exported into the spawn env (`ULTRACODE_ENV_VAR`). The adapter half
**works**.

## Evidence

The composite claim is a conjunction of a **brief-content** half and a
**dispatch/adapter resolution** half:

| Sub-claim | Status |
|---|---|
| advisor parent brief exists | **ABSENT** — `assemble("advisor")` raises BriefError; no advisor tier |
| head + Michael line in the brief | present in the generic parent brief, but not in any advisor-specific brief (none exists) |
| full body of the one embodied vision node inlined | **ABSENT** — parent brief only names target |
| seat in standing room `tier3-quorum` | **ABSENT** |
| audience rule for the prime (`send.py audience prime`) | **ABSENT** |
| primitive to spawn a Fable-max perpetual-goal director | **ABSENT** |
| dry dispatch prints resolved tier-3 parent command (opus-5 / max / ultracode) | **PRESENT** — `--list-rows` shows the row; adapter emits `--settings '{"ultracode":true}'` + `CLAUDE_CODE_WORKFLOWS=1` |

Evidence backing the command half: `dispatch.py --list-rows` actual output
(above, Q3); `claude_code_adapter.py` source for the ultracode flag/env (Q4).
Evidence backing the absent half: `brief.assemble(tier='advisor')` raising
`BriefError` (Q1), and the assembled `parent` brief lacking vision body /
quorum / audience / Fable spawn primitive even with `target='vision:alive'`
(Q2). `test_brief.py`/`test_dispatch.py` pass 87 tests, and the full suite
passes 1774/1 skipped — **because no advisor-brief tests exist**; there is no
red-first test asserting the claim, which is itself the gap.

**Verdict:** the hypothesis as literally written is **disproved** against the
current code. The advisor brief that the claim asserts `brief.py` assembles
does not exist — `brief.py` knows four tiers, none of them advisor, and the
parent brief carries none of the named advisor content. Only the dispatch /
adapter half (resolving the tier-3 parent row to opus-5/max/ultracode and
exporting `CLAUDE_CODE_WORKFLOWS=1`) is real. This is the wave-3 precondition
(§1.5/1.9/2.1/2.3 l3-command-ladder-brief.md) that still has to be built:
`brief.py` needs an advisor tier that embeds a `--target vision:<id>` node's
body verbatim, seats the advisor in `tier3-quorum`, states the one-audience
rule, and carries the Fable-max perpetual-goal director spawn primitive, plus
red-first tests asserting all of it.

## Agent Notes
Advisor brief does not exist: assemble('advisor') raises BriefError; parent brief lacks vision body, tier3-quorum, audience rule, Fable spawn primitive even with target=vision:alive. Only dispatch half holds (tier-3 parent resolves to opus-5/max/ultracode + CLAUDE_CODE_WORKFLOWS=1). Wave-3 precondition gap.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-9958960c, L3.10): accepted as-is. Checked the artifact, not the report — Q1 output shows BriefError for tier advisor, Q2 shows the assembled parent brief failing all six content probes (vision body, tier3-quorum, audience rule, Fable-max spawn primitive) even with target=vision:alive, Q3/Q4 show the dispatch/adapter half genuinely resolving opus-5/max/ultracode with CLAUDE_CODE_WORKFLOWS=1. Disproved is the correct verdict for the composite claim: conjunctive claims fail on any absent conjunct. evidence_runs is a list and cites this run itself, which is legitimate for an experiment. No demotion needed; caveat already correctly notes the claim is composite and only half fell.
<!-- THOUGHT:END -->

Parent review passed: verdict disproved verified against artifact (BriefError on advisor tier; parent brief fails all six content probes; dispatch/adapter half real). evidence_runs list valid. Accepted, no demotion.

## Agent Notes
Accepted kid experiment: disproved verified against artifact (no advisor tier; parent brief fails content probes; dispatch half real). evidence_runs linked.

PRIME REVIEW 2026-09-07 (belam): the hypothesis is a BUILD directive (assemble the tier-3 advisor brief) and the kid ran it as a status check, reporting the content absent; unimplemented is not falsified (same ruling as the L3.02 michael kid), so the verdict is reset to pending and the hypothesis stays open for the next round. The dispatch/adapter half the kid confirmed (tier-3 parent resolves to opus-5, max, ultracode, CLAUDE_CODE_WORKFLOWS=1 exported) is real evidence and stays in the body.
