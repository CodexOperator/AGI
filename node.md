---
id: experiment:a00-78053072-407094
mint_id: 91bab04ef8d54d3788898bdba760d44d
type: experiment
parents:
  - hypothesis:l3-workflow-model-crosses-harness-namespace
next_edges: []
confidence: 0.85
edited_by: a00-beca492e
evidence_runs:
  - experiment:a00-78053072-407094
loop: hypothesis:l3-workflow-model-crosses-harness-namespace@s2
model: claude-sonnet-5
profile: balanced
role: kid
scaffold_hash: 77908d73a3c94bee
season: 2
title: A00 78053072 407094
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-78053072-407094

## Experiment

Fixed `extensions/agi/bin/workflow.py` so the pi harness can never receive a
Claude Code subscription alias as `--model`.

1. **Per-harness model resolution.** Added `_resolve_pi_model(cfg, stage,
   args)`: for the pi harness, model comes from `harnesses.pi.models`, keyed
   by the stage's `role` (falling back to the `kid` entry for a role the
   block doesn't name, e.g. `global`/`reviewer`), and is resolved/applied in
   `run_workflow` right after `harness == "pi"` is known — never from
   `workflows.<name>.model`. `--args model` still wins (explicit override).
2. **FAIL CLOSED.** Added `_assert_model_in_provider_namespace(model,
   provider)`: an OpenRouter slug always has the shape `provider/name`
   (optionally `~`-prefixed); a Claude Code alias (`sonnet`, `opus`, ...)
   never contains `/`. Called for every pi stage before any dry-run print or
   spawn — raises `ValueError` naming both the model and the provider.
3. **Removed the cross-namespace default.** Deleted `_DEFAULT_MODEL =
   "sonnet"`. `_resolve_knobs` now raises if no model resolves from args,
   config row, or stage hint, instead of silently defaulting.
4. **Repaired `.agi/config.json`.** Dropped the (now-ignored, misleading)
   `"model": "sonnet"` from the `review` and `deep-search` rows (both
   `provider: pi`) and added notes explaining why; left `drafting.model =
   "sonnet"` untouched since its provider is `claude-code`, the correct
   namespace for that alias. No stage/prompt/schema content touched.

RED FIRST: before the fix, `workflow.py run review --harness pi --dry-run`
printed `model=sonnet` for every pi stage (the exact defect); the two tests
below encoded that literal string as the expected passing value. I flipped
both assertions to require an OpenRouter slug and confirmed they fail
against the pre-fix code (`k.get("model", _DEFAULT_MODEL)` still reading
`workflows.review.model`), then made them pass with the fix above.

Added `test_pi_model_refuses_claude_code_alias_before_spawn` — an explicit
red-first proof of the guard: config declares `harnesses.pi.models.kid =
"sonnet"` under `provider: openrouter`; asserts `run_workflow(...,
"pi", ..., dry_run=True)` raises `ValueError` naming `sonnet` and
`openrouter`, and that no `[dispatch]` line is printed (no spawn happens
after the refusal).

## Evidence

Real dry-run against the actual repo config, post-fix:

```
$ python3 extensions/agi/bin/workflow.py run review --harness pi --dry-run
[dispatch] global-checks :: role=global model=~deepseek/deepseek-v4-flash-latest effort=medium
[dispatch] review :: role=reviewer model=~deepseek/deepseek-v4-flash-latest effort=medium
[summary] workflow=review harness=pi stages=2 via dispatch.py kids when harness=pi

$ python3 extensions/agi/bin/workflow.py run deep-search --harness pi --args '{"question":"x","facts":[],"lenses":[]}' --dry-run
[dispatch] read :: role=reader model=~deepseek/deepseek-v4-flash-latest effort=high
[dispatch] refute :: role=critic model=~deepseek/deepseek-v4-flash-latest effort=high
[dispatch] synthesize :: role=reviewer model=~deepseek/deepseek-v4-flash-latest effort=high
[summary] workflow=deep-search harness=pi stages=3 via dispatch.py kids when harness=pi

$ python3 extensions/agi/bin/workflow.py run drafting --harness claude-code --dry-run
[dispatch] draft :: role=drafter model=sonnet effort=max
[dispatch] critic :: role=critic model=sonnet effort=max
[summary] workflow=drafting harness=claude-code stages=2 via dispatch.py kids when harness=pi
```

No `sonnet` (or any bare, slash-less alias) reaches a pi/openrouter stage;
`drafting` on claude-code correctly keeps `sonnet` — its namespace is
subscription aliases, not OpenRouter slugs.

Test suite, full repo, post-fix:

```
$ python3 -m pytest extensions/agi/tests/ -q
2094 passed, 1 skipped in 121.93s
```

`test_workflow.py` alone (20/20, including the two red-first flips and the
new refusal test):

```
$ python3 -m pytest extensions/agi/tests/test_workflow.py -q
....................
20 passed in 0.16s
```

`links.py links`: `1603 resolved, 0 broken (18 retired payload(s), not
damage)` — untouched by this change, confirming no new dangling references.

Diff touches `extensions/agi/bin/workflow.py` (model resolution + guard +
removed default), `.agi/config.json` (`workflows.review`/`workflows.
deep-search` drop the misleading `model` key), and `extensions/agi/tests/
test_workflow.py` (three assertions flipped/added to lock the fixed
behavior). `dispatch.py`, `brief.py`, `rotate.py`, `cli.py`, `zoom.py` and
`.agi/nodes/.geometry/seats.md` untouched, per the brief's scope fence.

Did NOT run a live paid workflow — the `.env` OpenRouter key is at its cap
and every call would 402; `--dry-run` output above is the proof, per the
brief's explicit instruction.

## Agent Notes
workflow.py pi harness now resolves --model from harnesses.pi.models by role (never workflows.NAME.model), refuses any non-slug model under provider=openrouter before spawn, and the sonnet default is deleted; red-first tests flip, dry-run proves ~deepseek slug on pi vs sonnet kept correctly on claude-code drafting, full suite 2094 passed/1 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Accepted at proved by parent a00-beca492e after independent re-verification, not on the report. Re-ran the artefact myself rather than reading the summary: workflow.py:610-611 resolves the pi model via _resolve_pi_model then passes it through _assert_model_in_provider_namespace before any spawn or dry-run print, _DEFAULT_MODEL is gone (line 56 is now a comment naming this hypothesis), harnesses.pi.models is read by stage role with a kid fallback, and .agi/config.json no longer carries a model key on the two provider:pi rows while drafting keeps sonnet under provider:claude-code. My own runs: workflow.py run review --harness pi --dry-run prints ~deepseek/deepseek-v4-flash-latest for both stages; test_workflow.py 20 passed; full suite 2096 passed 1 skipped (two more than the kid reported, from a sibling round, not from this diff). The verdict stands at proved and the self-citation in evidence_runs is legitimate here because this node IS the run it judges. One residual the node does not state: the guard fires AFTER the --args override, so a human deliberately passing --args model=sonnet on a pi stage is also refused. That is stricter than item 1 of the brief asked for and is the right default under an incident whose whole cost was silent spend, but it means the documented escape hatch is now shape-checked too, and a future round wanting a deliberate cross-namespace run must widen the guard rather than use --args. The guard also only checks slug SHAPE, not that the slug exists at OpenRouter; a typo inside a valid-looking provider/name still reaches the network. Neither weakens the claim as written.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-beca492e, L3.41): ACCEPTED as proved, no demotion. Parent link resolves to hypothesis:l3-workflow-model-crosses-harness-namespace. evidence_runs is a list of one real node id (itself, legitimate for an experiment). Independently re-verified by the parent: guard + per-role resolution present in workflow.py, config repaired, dry-run shows the OpenRouter slug on pi and sonnet retained only on claude-code drafting, test_workflow.py 20/20, full suite 2096 passed 1 skipped. Scope fence honoured: dispatch.py, brief.py, rotate.py, cli.py, zoom.py and seats.md untouched. Noted for a future round: the namespace guard runs after the --args model override, so an explicit human override into the other namespace is refused too.
