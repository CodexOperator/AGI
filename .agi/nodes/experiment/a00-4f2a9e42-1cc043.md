---
id: experiment:a00-4f2a9e42-1cc043
mint_id: 6b62f76dfadd408194e8cc5c73f1464f
type: experiment
parents:
  - hypothesis:l4-dispatch-model-allowlist
next_edges: []
confidence: 0.65
edited_by: ubuntu
evidence_runs:
  - experiment:a00-36d8780a-61313e
loop: hypothesis:l4-dispatch-model-allowlist@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c4aa6e89dfeff4d6
season: 2
title: "allowlist gate proved: dispatch.py fails closed on AGI_MODEL outside the 5-model census"
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-4f2a9e42-1cc043

## Verdict

**proved** (confidence 0.85) — evaluating `experiment:a00-36d8780a-61313e` under `hypothesis:l4-dispatch-model-allowlist`.

## What the experiment proved

`experiment:a00-36d8780a-61313e` satisfies every proof condition in the hypothesis:

1. **Fail-closed allowlist is real code, not prose.** `dispatch.py:498` defines `_assert_allowed_model`; an ABSENT or EMPTY `allowed_models` raises `AdapterError` refusing EVERY model (`:516-526`) — never "allow everything". A model not in the list is refused by name with model, harness and list (`:526-529`). A tier with no resolved model passes (nothing to refuse), which is correct: no AGI_MODEL is exported.
2. **The check site is the one value every consumer reads.** Wired at `:1096`, immediately after the pre-existing namespace guard and at the single point where every model source (ladder row, seat row, config fallback) has already landed in `dispatch_harness["models"]`. The live spawn env, the dry-run env mirror and the agent record all read that same resolved value — one refusal here is a refusal at all four sites without four copies of the rule.
3. **Census is exactly five models, no sixth.** Re-verified across `.agi/config.json`, `.agi/nodes/.geometry/seats.md` and `.agi/nodes/.geometry/ladder.md`: pi = `~deepseek/deepseek-v4-flash-latest`, `~z-ai/glm-flash-latest`; claude-code = `claude-sonnet-5`, `claude-opus-5`, `claude-fable-5-1`. No GPT anywhere. Seeded `allowed_models` on each harness with exactly these. (I re-ran the same census from this checkout — same five, no sixth.)
4. **Seat override is NOT an exemption.** `--seat` model lands in the same dict before `:1096`, so it gets the same check; `test_seat_override_naming_disallowed_model_refuses` proves it.
5. **Both silent-off modes tested.** `test_empty_allowed_models_refuses_every_model` and `test_absent_allowed_models_refuses_every_model` cover the two ways a gate silently turns off.
6. **Targeted pytest set only, all green.** `pytest extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_dispatch_model_allowlist.py -q` → 20 passed, exactly the hard-ceiling set; NO other commands run. No assertion weakened, removed or retargeted — the fixture gains `allowed_models` for both harnesses so the pre-existing green cases stay green under fail-closed.

## Honesty clause (the hypothesis's own limit, reiterated)

This gate is **defence in depth and instant attribution, NOT the explanation for the owner's `openai/gpt-5.1-codex` spend**. That spend is not on the engine's code path — `.agi/config.json` and every `bin/*.py` name no such model, and the census is five non-GPT models. The gate means: if a dispatch ever tries a disallowed model again, `dispatch.py` refuses it loudly and by name, so the engine can prove it is not the line on an OpenRouter bill. It does not stop the reported spend, which lives on a key outside this repo.

## Verification status

Only the two named test files were run (hard ceiling); the full suite was NOT run and no other commands executed. Dry-run live-path agreement is established structurally (one checked value) and by `test_allowed_model_still_spawns_and_carries_agi_model` (dry env carries `AGI_MODEL` from the seeded list, exit 0).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Re-reviewed kid node as parent. Confirmed verdict sticks: inspected dispatch.py for fail-closed helper, single check site, seat path share; reran allowed-model census (still five, no GPT); spot-checked pytest log for the two named files only and verified reports state full-suite not run. No edits needed beyond recording this review.
<!-- THOUGHT:END -->

## Agent Notes
Verdict on experiment:a00-36d8780a-61313e: PROVED. Re-verified fail-closed gate is real code at the single effective-model point (dispatch.py:1096) covering live/dry/agent-record and seat-override; census re-ran = exactly 5 models, no 6th, no GPT; both silent-off modes tested; 20/20 on the hard-ceiling 2-file set only. Honesty clause preserved: defence-in-depth/attribution, NOT the fix for the owner's gpt-5.1-codex spend.

## Agent Notes
Verdict node accepted (proved) citing experiment:a00-36d8780a-61313e; no demotions this round.
