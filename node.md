---
id: experiment:a00-75246953-b332a8
mint_id: 2fd162b600ae4222bd4568d750da64c1
type: experiment
parents:
  - hypothesis:l3w4-director-kids-on-glm
next_edges: []
confidence: 0.8
edited_by: a00-31205148
evidence_runs:
  - experiment:a00-75246953-b332a8
loop: hypothesis:l3w4-director-kids-on-glm@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b01ae6a73197187a
season: 2
title: A00 75246953 b332a8
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-75246953-b332a8

## Experiment

Tested `hypothesis:l3w4-director-kids-on-glm` (seat director-kids on GLM
flash): (a) the `thinking` cell threads `--thinking high` through
dispatch, and (b) the director brief carries a REASONING segment with the
three literal strings `write.py create goal`, `--ladder-tier 0`,
`season.py judge`.

The mechanism was NOT implemented in the tree, so the experiment built it
first, then verified it two ways — unit tests, then the exact gate dry-run.

Implemented:
- `dispatch.py` — added the `thinking` cell to `resolve_role_spec` and
  `resolve_seat_spec` (blank → None), threaded it onto `dispatch_harness`
  in the apply block (flat, `pi_adapter.model_args` reads it directly), and
  added `thinking=...` to the `seats:` and `roles:` print notices.
  `pi_adapter.model_args` already emitted `--thinking` (L75-77), so no
  adapter change was needed.
- `brief.py` — new `_director()` segment 3, "REASON BEFORE YOU ACT", with
  the ASCII goal→subgoal→parent→outcome diagram and the three commands.
- 3 red-first tests: `test_resolve_seat_spec_thinking_is_none_when_blank`,
  `test_thinking_cell_wins_over_config_default` (test_dispatch.py),
  `test_director_brief_carries_reasoning_section_with_ascii_diagram`
  (test_brief.py).

Gate run (data temporarily applied, then reverted):

    python3 extensions/agi/bin/dispatch.py . 1 --tier director \
      --role director --ladder-tier 1 --target goal:g1 --seat dir-g1 \
      --dry-run

Output (exit 0):

    seats: seat dir-g1 -> pi/~z-ai/glm-flash-latest/effort=-/thinking=high/settings=-
    roles: tier=1 role=director -> pi/~z-ai/glm-flash-latest/effort=-/thinking=high/settings=-
    command: ... --provider openrouter --model '~z-ai/glm-flash-latest' --thinking high ...
    brief: tier=director 150 lines; first 20:

The assembled director brief (150 non-empty lines, grown over baseline)
contained all of `write.py create goal`, `--ladder-tier 0`, `season.py
judge`, and `REASON BEFORE YOU ACT` (verified on the real assembled text).

Verification: full suite `python3 -m pytest extensions/agi/tests/ -q` →
**1995 passed, 1 skipped**. The three new tests pass.

## Evidence

- Gate dry-run exit 0; `seats:` line matches the claim verbatim
  (`pi/~z-ai/glm-flash-latest/effort=-/thinking=high/settings=-`);
  `--thinking high` and `--model ~z-ai/glm-flash-latest` on the command.
- Real assembled director brief contains all three literal strings +
  `REASON BEFORE YOU ACT`; 150 lines.
- Mechanism unit tests green (`test_thinking_cell_wins_over_config_default`,
  `test_resolve_seat_spec_thinking_is_none_when_blank`,
  `test_director_brief_carries_reasoning_section_with_ascii_diagram`); full
  suite 1995 passed, 1 skipped.

## Caveat (why the gate needs the data — already reverted)

The claim's mechanism half is PROVEN, but its data half — flipping live dir
seats dir-g1/g15/g16 + the ladder tier-1 director row to GLM/thinking high —
is OWNER-OWNED policy. `hypothesis:l3w4-director-kids-on-glm` PRIME NOTE
itself says "do not treat GLM-flash director-kids as settled policy until the
owner confirms". The experiment therefore applied the data only to run the
gate and reverted it: the live tree still resolves dir-g1 to opus/high, only
the mechanism (thinking cell + REASONING brief) is landed. Applying the data
later is a one-cell edit per row — the mechanism is proven ready.

## Agent Notes
Mechanism PROVEN (gate passes exactly: seat dir-g1->pi/glm/effort=-/thinking=high, --thinking high on command, director brief 150 lines carries write.py create goal / --ladder-tier 0 / season.py judge). Data half (flipping live dir seats g1/g15/g16 + ladder t1 director row to GLM) deliberately REVERTED — owner-owned policy per hypothesis PRIME NOTE; mechanism is landed and one-cell-edit per row ready. Suite 1995 passed, 1 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-31205148): ACCEPTED at inconclusive_lean_proved:80. Read the artifact, not the report: reran test_dispatch.py + test_brief.py (137 passed) and re-read the diffs. The thinking cell lands exactly as the hypothesis DESIGN specified — flat on dispatch_harness (pi_adapter reads it tierless), blank->None in all three resolvers, no config fallback, print notices updated. The REASONING segment carries the ASCII diagram plus all three literal strings. The lean is right, not timid: the MECHANISM is proven (gate dry-run verbatim, full suite 1995 passed) but the hypothesis is about seating director-kids on GLM, and the data half was deliberately reverted as owner-owned policy per its own PRIME NOTE — so the full claim cannot read proved until the owner flips the rows. Self-cited evidence_runs is legitimate here: this experiment IS the run.
<!-- THOUGHT:END -->

Parent review PASS: parents link resolves (hypothesis:l3w4-director-kids-on-glm exists); verdict format valid; evidence_runs is a real node-id list. Diffs re-read, tests rerun locally (137 passed). No demotion — no overclaim: the data half is explicitly not landed, owner-owned.
