---
id: experiment:a00-10d3626e-28c992
mint_id: 9ecc26c9235543afb9096d6acdcc898f
type: experiment
parents:
  - hypothesis:l3w4-drafter-seat
next_edges: []
confidence: 0.65
edited_by: a00-122738d5
evidence_runs:
  - experiment:a00-10d3626e-28c992
loop: hypothesis:l3w4-drafter-seat@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7a95c264c263ae1e
season: 2
title: Drafter seat resolution gates false as-tested (mechanism landed, seat absent)
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-10d3626e-28c992

## Experiment

Tested whether the drafter seat resolves as the hypothesis claims: that `dispatch.py --role drafter --ladder-tier 1` resolves a `drafter` row (claude-sonnet-5 / max / ultracode) and that `brief.py assemble(tier="drafter")` is a real tier. Ran both directly on branch `loop/hypothesis-l3w4-drafter-seat-a00-122738d5@s2`.

### 1. dispatch.py seat resolution

```
$ python3 extensions/agi/bin/dispatch.py . L3.42 --role drafter --ladder-tier 1 --dry-run
roles: no ladder row for (tier=1, role=drafter); falling back to config harnesses.pi.models[kid]
[dry-run] slot=0 harness=pi tier=kid role=drafter ladder_tier=1 ...
  command: ... pi --provider openrouter --model '~deepseek/deepseek-v4-flash-latest' ...
```

`--list-rows` shows 8 ladder rows; **there is no `drafter` row.** The claim's resolution (sonnet/max/ultracode via a drafter row) does not happen — it falls back to a generic pi kid on deepseek. The fallback actually *hides* the missing row, resolving to a kid brief rather than refusing.

### 2. brief.py drafter tier

```
$ cd extensions/agi/bin && python3 -c "import brief; brief.assemble(tier='drafter', ...)"
assemble drafter raised: BriefError | no brief for tier 'drafter'; known tiers: kid, parent, advisor, director, prime_director, liaison
'drafter' in brief.TIERS: False
```

`TIERS = ("kid", "parent", "advisor", "director", "prime_director", "liaison")` — no `drafter`. Exactly the `test_brief_drafter_tier_in_TIERS (assemble raises today)` gate from the hypothesis.

### What IS landed (the mechanism half)

- `extensions/agi/workflows/agi-brief-drafting.js` — the drafting workflow (draft + critic), exists as workflow payload.
- `.agi/config.json` `workflows.drafting` row: `{model: sonnet, effort: max, provider: claude-code}` with `note` citing `hypothesis:l3w4-drafter-seat`, owner quote (6).
- `test_workflow.py:245` references a `"role": "drafter"` draft agent label.

So the config-maxxed drafting mechanism has largely landed, but the **seat**: the ladder `drafter` row, `brief.py` drafter tier, and dispatch resolution described by this hypothesis do not yet exist. Per the hypothesis's own notes (Belam V), the SEAT is superseded by `hypothesis:l3w4-plan-master`; the mechanism is built here, the seat there. This experiment records the current gap: the literal seat-resolution gates are false as-tested today.

## Evidence

- `dispatch.py --list-rows`: 8 rows (prime_director, parent×2, director×2, liaison, parent, kid) — no drafter.
- `dispatch.py --role drafter --ladder-tier 1 --dry-run`: `roles: no ladder row for (tier=1, role=drafter); falling back to ...pi.models[kid]`, resolves to `~deepseek/deepseek-v4-flash-latest` kid.
- `brief.py assemble(tier="drafter")`: raises `BriefError` (not in TIERS).
- `test_brief.py` asserts only kid/parent/director/prime_director/advisor/liaison in TIERS; no drafter test wired.
- Config `workflows.drafting` and `workflows.review` rows present and cite the relevant hypotheses.

Caveat: absence-of-implementation is not refutation of the design — the seat was deliberately redirected to plan-master. But the literal claim (dispatch resolves a drafter row, brief has a drafter tier) is false as-tested this run.

## Agent Notes
Ran dispatch/resolution gates: no drafter ladder row (falls back to pi kid/deepseek), brief.assemble(tier=drafter) raises BriefError. Mechanism (workflow js + config workflows.drafting) landed; seat absent as-tested.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-122738d5, accepted as-is): the experiment runs the two literal gates of hypothesis:l3w4-drafter-seat and both are false as-tested — no drafter ladder row (dispatch falls back to pi kid/deepseek, silently hiding the gap) and brief.TIERS lacks drafter (BriefError). The lean_disproved:65 is calibrated correctly: the mechanism half (workflows/agi-brief-drafting.js + config workflows.drafting) is landed and the seat was deliberately redirected to hypothesis:l3w4-plan-master (Belam V), so this is absence-of-implementation, not refutation of design. Evidence is live CLI output, not assertion; the silent-fallback finding is the most valuable part and worth an engine follow-up (unknown --role should hard-fail, not fall back).
<!-- THOUGHT:END -->

Parent review accepted: verdict calibrated, evidence real, parents resolve. Noted defect: dispatch silently falls back on unknown role instead of hard-failing.
