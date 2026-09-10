---
id: experiment:a00-36d8780a-61313e
mint_id: ad9f0d838b2f4eddabbfab936d764373
type: experiment
parents:
  - hypothesis:l4-dispatch-model-allowlist
next_edges: []
confidence: 0.9
edited_by: a00-fb25b8e9
evidence_runs:
  - experiment:a00-36d8780a-61313e
loop: hypothesis:l4-dispatch-model-allowlist@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ea110d822db0fe84
season: 2
title: dispatch.py refuses any AGI_MODEL outside a fail-closed allowed_models census
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-36d8780a-61313e

## Experiment

Implemented the fail-closed model allowlist gate in `dispatch.py`, seeded the
real `.agi/config.json` census, added a dedicated test file. Ran ONLY the two
named files (`test_dispatch_dry_run.py` + `test_dispatch_model_allowlist.py`),
not the full suite (hard-ceiling instruction).

### The gate (`extensions/agi/bin/dispatch.py`)

Added helper `_assert_allowed_model(harness_name, harness, model)`:

- model absent/None → allow (a tier with no resolved model exports no
  AGI_MODEL, so there is nothing to refuse).
- `allowed_models` absent or empty → raise `AdapterError` refusing EVERY model
  (fail-closed: a gate that opens on absence disappears the moment the key is
  deleted).
- model not in `allowed_models` → refuse, message names model, harness, and
  the allowed list.

Wired it directly after the existing `assert_model_in_provider_namespace`
namespace guard at the effective-model resolution point — the ONE line every
model source (ladder row, seat row, config fallback) has landed in
`dispatch_harness["models"]` by, and the exact value the live spawn env
(`:1423-1425`ish), the dry-run env mirror (`:725-727`ish) and the agent record
(`:1348`) all read. One refusal here is a refusal at all four check sites
without four copies of the rule — same position and same rationale as the
pre-existing namespace guard. A `--seat` override is not an exemption: its
model is in that same dict by this line and gets the same check.

### The seed (`.agi/config.json`)

Re-verified the model census across `.agi/config.json`, `.agi/nodes/.geometry/
seats.md` and `ladder.md` before seeding: exactly five models, no sixth —
pi: `~deepseek/deepseek-v4-flash-latest`, `~z-ai/glm-flash-latest`;
claude-code: `claude-sonnet-5`, `claude-opus-5`, `claude-fable-5-1`. Seeded
`allowed_models` on each harness with exactly those. Real-project `--dry-run`
smokes still resolve and exit 0 (no live seat broken).

## Evidence

`pytest extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_dispatch_model_allowlist.py -q` → **20 passed**.

- `test_allowed_model_still_spawns_and_carries_agi_model` — allowed model
  exits 0, dry env carries `AGI_MODEL=~z-ai/glm-flash-latest` (P1).
- `test_disallowed_model_refuses_naming_model_harness_and_list` — a model not
  in the list (via config fallback) refuses non-zero; stderr names the model,
  `pi`, the allowed list, `allowed_models` (P2).
- `test_seat_override_naming_disallowed_model_refuses` — a `--seat` row naming
  a disallowed model refuses the same way; seat row is not an exemption (P3).
- `test_empty_allowed_models_refuses_every_model` — empty list refuses every
  model with "absent or empty" (P4a).
- `test_absent_allowed_models_refuses_every_model` — key deleted refuses every
  model (P4b).

Real-project smoke: `dispatch.py . 1 --harness pi --tier parent --dry-run` and
`--harness claude-code --tier director --ladder-tier 3 --dry-run` both
resolve `AGI_MODEL` from the seeded list and exit 0.

`allowed_models` added to the test fixture CONFIG for both harnesses so the
pre-existing green cases stay green under fail-closed (no assertion removed or
weakened).

NOTE (hypothesis's own honesty clause): this gate is defence in depth and
instant attribution — it does NOT explain or stop the `openai/gpt-5.1-codex`
spend the owner reported, which is not on the engine's code path. The verdict
records that separation.
<!-- BODY:END -->

## Agent Notes
Fail-closed allowed_models gate in dispatch.py: absent/empty list refuses every model, not-in-list refuses by name (model/harness/list), --seat override is NOT an exemption, dry-run and live share the one checked value. Seeded .agi/config.json with exactly the census of 5 (pi x2 slugs, claude-code x3 aliases; re-verified, no sixth). 20/20 tests green (test_dispatch_dry_run.py + new test_dispatch_model_allowlist.py only, per hard ceiling). Real-project dry-runs still resolve+exit 0. Honesty: does NOT explain/stop the owner's gpt-5.1-codex spend (not on this path) — defence in depth + attribution only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-fb25b8e9, L4.43): ACCEPTED as written; no demotion. I re-verified the artifact rather than the report: (1) the gate sits at the single effective-model resolution point (dispatch.py:1096) so live env, dry-run mirror and agent record all share one check — a seat override cannot bypass it because its model lands in the same dict before this line; (2) fail-closed is real code, not prose: absent AND empty both raise AdapterError refusing every model (dispatch.py:508-516), only a tier with no resolved model passes (nothing to refuse); (3) the seed in .agi/config.json is exactly the five-model census (pi x2 slugs, claude-code x3 aliases), no sixth; (4) I ran the two named test files myself — 20 passed, no assertion retargeted, fixture gains allowed_models rather than weakening a check; (5) I ran a real-project dry-run myself and AGI_MODEL still resolves and exits 0. Honesty clause is preserved in the experiment body and notes: this is defence in depth and attribution, NOT the explanation for the owner's gpt-5.1-codex spend.
<!-- THOUGHT:END -->

Parent review L4.43: accepted, verdict proved upheld. Independently re-ran the 2-file pytest (20 passed) and a live dry-run (AGI_MODEL resolves, exit 0); code inspected at the one check site covering all four consumer points; census of 5 re-checked.
