---
id: hypothesis:l3w4-director-kids-on-glm
mint_id: a453f79a838d4b3cbfd461a7a004b072
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-VII
scaffold_hash: 20cd81ef606c500a
season: 2
testable_claim: dispatch.py --seat dir-g1 --tier director --role director --ladder-tier 1 --dry-run resolves harness pi, model ~z-ai/glm-flash-latest and --thinking high (from config:seats and ladder:ladder's tier-1 director row, both changed), and brief.assemble(tier="director") contains a REASONING segment whose text includes the literal strings "write.py create goal", "--ladder-tier 0" and "season.py judge".
thought_session: 7af11157
title: Seat director-kids on GLM flash
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-director-kids-on-glm

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

`config:seats` rows dir-g1/dir-g15/dir-g16 (director-kid seats) move
`claude-code`/`claude-opus-5`/`high` to `pi`/`~z-ai/glm-flash-latest`/
`thinking: high`; `ladder:ladder`'s tier-1 `director` row becomes the same
DEFAULT for an unseated perpetual goal (L3.28's `--harness` flag already
wins; only the fallback changes). `brief.py`'s director
template gains a REASONING segment — a small ASCII goal-to-subgoal diagram,
then the literal `write.py create goal`, `dispatch.py --tier parent
--ladder-tier 0`, and `season.py judge` commands — so a one-shot GLM-flash
director with no native reasoning still knows how to decompose and drive
the loop.

## WHY

Owner, 20:14 UTC (HANDOFF §6 item 32, verbatim): "...glm flash parent model
for director-kids as well, just use with reasoning if available as api or
if not by manually prompting it to reason carefully including graphical
ascii diagram examples of reasoning as a process of breaking down goals
into subgoals and minting those as needed and getting parents to run
them." (director proposal) narrows correction (4) to director-kids only;
quorum (Opus 5 max) and liaison (Sonnet 5 high) stand — the quorum's
OpenRouter model stays open.

## FILES

- .agi/nodes/.geometry/seats.md :: seats — EDIT dir-g1/g15/g16 rows
- .agi/nodes/.geometry/ladder.md :: roles — EDIT tier=1 role=director row
- extensions/agi/bin/dispatch.py :: resolve_role_spec L396,
  resolve_seat_spec L441, print L782-784, apply L834-842
- extensions/agi/bin/adapters/pi_adapter.py :: model_args L47, `--thinking`
  L75-77 — already threads it
- extensions/agi/bin/brief.py :: _director L519, assemble L976
- extensions/agi/tests/test_dispatch.py, test_brief.py

## DESIGN

New `thinking` cell — pi's analogue of `effort` (pi has no `--effort`).
`resolve_role_spec`/`resolve_seat_spec` add
`"thinking": (row.get("thinking") or "").strip() or None`. L834-842 gains
`if _spec["thinking"]: dispatch_harness["thinking"] = _spec["thinking"]` —
flat, not tier-keyed, since `pi_adapter.model_args` reads `harness.get
("thinking")` directly (L75-77). Print notices gain `thinking={...}` too.
`[ladder]`/`[config]` validate rows as `list` only — no schema edit needed.

New `_director()` segment after step 2:

```
goal:g16 (no subgoal)
      | decompose
  +---+---+
  |       |
g16.a   g16.b    write.py create goal <slug> --parent goal:g16
  |       |
parent  parent   dispatch.py ... --tier parent --ladder-tier 0 --target <slug>
  |       |
outcome outcome
  +---+---+
      |
  season.py judge <outcome-id> --against goal:g16   # continue|adjust|done
```

Unconditional across tiers and models — `assemble()` has no model axis.

## TESTS (red-first)

`test_thinking_cell_wins_over_config_default`;
`test_resolve_seat_spec_thinking_is_none_when_blank` (test_dispatch.py);
`test_director_brief_carries_reasoning_section_with_ascii_diagram` — asserts
"write.py create goal", "--ladder-tier 0" and "season.py judge" all appear
(test_brief.py).

## GATE

`dispatch.py <root> <iter> --tier director --role director --ladder-tier 1
--target goal:g1 --seat dir-g1 --dry-run` prints `seats: seat dir-g1 ->
pi/~z-ai/glm-flash-latest/effort=-/thinking=high/settings=-` and
`--thinking high` on the `command:` line, before the 20-line cutoff;
brief line count grows over baseline. Suite green.

## NOT IN SCOPE

The per-turn loop holding a seat alive across rotations
(`l3w4-seat-rotation-loops`). Drafting through `workflow.py run drafting
--harness pi` — a stub today (`l3w4-workflows-config-maxxed`, MEASURED
20:22 UTC).

## SOURCE

HANDOFF.md §6 item 32 (2026-09-07 20:14 UTC, verbatim, quoted above); owner
correction (4) in `doc:l3-command-ladder-brief` (narrowed to
director-kids — see WHY).

PRIME NOTE (Belam VII at mint, 2026-09-07): the critic pass fixed one real violation before this landed — the draft had written the owner as SUPERSEDING correction (4) of the model table for director-kids, when owner item 32 says only "I am considering using my glm flash parent model for director-kids as well". That is a question put to the ladder, not a decision taken, so it is now labelled a director proposal and the OWNER STILL OWNS IT: do not treat GLM-flash director-kids as settled policy until the owner confirms. The quorum model is separately and explicitly still an open owner decision. Two line numbers in FILES have already drifted (brief.py _director is at L524 not L519, assemble at L992 not L976 — other agents were editing the file during the draft); trust the symbol names, re-grep the lines. Neighbours: l3w4-seat-rotation-loops owns the loop that keeps a seat alive, l3w4-workflows-config-maxxed owns the stub pi path of workflow.py run that must be fixed for any of this to be drafted without subscription tokens.
