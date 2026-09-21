---
id: experiment:a00-3588e734-dc2df3
mint_id: bccf038a33ee4495a9a74c2086087803
type: experiment
parents:
  - hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-spawn
next_edges: []
confidence: 0.9
edited_by: a00-4d1de05a
evidence_runs:
  - experiment:a00-3588e734-dc2df3
loop: hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-spawn@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a94305845e95219c
season: 2
title: A00 3588e734 dc2df3
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-3588e734-dc2df3

## Experiment

Slice A of `hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-spawn` — conjuncts (a)-(f) only.

**Pre-fix state (the defect, measured by reading the pre-change bytes).** `_run_stage_pi` called `subprocess.run(cmd, ..., env=_pi_env(), timeout=600)`, and `_pi_env()` is `os.environ` minus `_SCRUB` — i.e. the pi stage inherited whatever `OPENROUTER_API_KEY` the caller shell carried (the deleted `.env` key on TM.2 / mur-tm-01, which 401'd at stage 1). No mint was ever attempted on the pi workflow path. The legacy/no-seam behaviour is preserved and still asserted by the existing `test_run_stage_pi_passes_resolved_model_and_rendered_prompt` (the child env is `_pi_env()`, `ANTHROPIC_API_KEY` scrubbed, no minted key).

**Built (in `extensions/agi/bin/workflow.py`):**

1. `import provisioning` — the ONE mint seam `dispatch.py` uses.
2. `_credential_decision(root, cfg, harness)` — reads-only: `provisioning.available(root)` and `adapters.needs_credential((cfg["harnesses"])[harness])`. Returns `(would_mint, reason|None)`. Shared by the dry-run print and the live mint so the two cannot disagree.
3. `_credential_line(would_mint, reason)` -> `[credential] mint per-run` | `[credential] inherited env (<reason>)`.
4. `_workflow_credential_tier(stages)` -> first stage's declared tier, else `_tier_for_role(role)`.
5. `_resolve_workflow_spawn_env(root, cfg, run_key, harness, stages)` — calls `_credential_decision`; when minting, `provisioning.mint(iter_n=run_key, agent_id=f"workflow:{run_key}", tier=..., limit_usd/ttl_minutes=provisioning.settings(cfg), workspace_id=provisioning.workspace(cfg), root=root)` and sets `env[provisioning.RUNTIME_KEY_VAR] = minted.secret`. On unavailable / needs-no-credential / `mint() is None` it returns `_pi_env()` with ONE stderr line. A `ProvisioningError` with the key present prints `ERR: could not mint a workflow credential: <exc>` then the one named fallback line.
6. `_run_stage_pi(..., spawn_env: dict | None = None)`; `None` falls back to `_pi_env()` (legacy callers unchanged).
7. `run_workflow` mints ONCE before the `for st in stages:` pi loop and threads `spawn_env` into every stage; `--dry-run` writes the `[credential]` line BEFORE the dispatch lines from the same helper, without minting.

The claude-code branch (`harness != "pi"`) is untouched.

## Evidence

`python3 -m pytest extensions/agi/tests/test_workflow.py -q` -> **55 passed in 0.79s**
`python3 -m pytest extensions/agi/tests/test_provisioning.py -q` -> **71 passed, 5 skipped in 0.41s**

New tests (all in `extensions/agi/tests/test_workflow.py`):

- `test_pi_run_mints_one_credential_for_all_stages` — (a)+(c): both pi stages' `env` carry `OPENROUTER_API_KEY == "sk-minted-run"`; the fake mint seam called exactly ONCE for a two-stage run; `agent_id == f"workflow:{iter_n}"`, `limit_usd == 5.0`, `ttl_minutes == 180`, `workspace_id` from `spawn.credential`.
- `test_pi_dry_run_prints_credential_line_before_dispatch` — (d): one `[credential] mint per-run` line, index before the first `[dispatch]` line, and `mint` NOT called.
- `test_dry_run_credential_line_matches_live_decision` — the shared helper's claude-code answer (`harness claude-code needs no credential`) is exactly the dry-run line printed.
- `test_pi_fallback_prints_one_named_line_when_provisioning_absent` — one stderr line `workflow.py: [credential] inherited env (provisioning unavailable)`, no mint.
- `test_pi_mint_error_is_named_then_falls_back` — `ERR: could not mint a workflow credential: HTTP 401 nope` then the named fallback line.
- `test_claude_code_path_mints_nothing` — (e): cc branch never touches the seam, no `[credential]` line, summary unchanged.
- `test_pi_stage_receives_minted_key_across_the_process` — (a) with a REAL fake pi bin (executable script that dumps `os.environ`): the child process actually sees `OPENROUTER_API_KEY == "sk-real-seam"`.

Live dry-run byte proof:
```
[run-key] review-18
[credential] mint per-run
[dispatch] global-checks :: role=global model=~deepseek/deepseek-v4-flash-latest effort=medium
[dispatch] review:t1 :: role=reviewer model=~deepseek/deepseek-v4-flash-latest effort=medium
[summary] workflow=review harness=pi stages=2 via dispatch.py kids when harness=pi
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Slice A only: conjuncts (g) (provisioning.mint default / dispatch floor skip) and (h) (lenient JSON parse) are other kids' work and were deliberately not touched. The mint-per-run decision is factored into `_credential_decision` precisely because the task warns that a dry-run line computed separately from the live choice is the trap; both call sites now read the same boolean. The tier is taken from the first stage's ladder declaration (`_tier_for_role` fallback) — a run has one key, so one tier, and the first stage is the run's entry point; this is recorded as a judgement call rather than reading the ladder row's own `tier` cell.
<!-- THOUGHT:END -->

## Agent Notes
Slice A conjuncts (a)-(f): added a per-RUN provisioning mint seam to workflow.py pi stages; 7 new tests green (test_workflow.py 55 passed, test_provisioning.py 71 passed/5 skipped). (g)/(h) untouched.

PARENT REVIEW L4.368 (a00-4d1de05a): judged from the staged DIFF (workflow.py +95, test_workflow.py +228), not the result file. Slice-A conjuncts (a),(c),(d),(e),(f) hold; (b) holds in substance (_credential_decision/`workflow:<run_key>` agent_id asserted; key_name derives the full agi-iter<run_key>-... name). THREE parent probes run against the built bytes: (auth) with the REAL provisioning seam live and no mint mock, `_resolve_workflow_spawn_env` is ARRESTED by the L4.155 `_mutation_guard` (mint refused under pytest) and falls back with exactly one named line, no key leaked; (gate) claude-code needs_credential=False -> mint never called, one named line; (wire) the env returned by the seam is the SAME mapping subprocess.run receives and carries the minted secret. (f) full suite 4822 passed, 15 skipped, 1 xfailed in 443.06s under the 590s ceiling. Probe fixtures were throwaway and deleted; the staged diff is the kid\x27s only. Caveat: (a) proven on the fixture fake-pi bin, not live on paper-digest -- the claim allows either.
