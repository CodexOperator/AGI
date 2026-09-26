---
id: experiment:a00-5571040e-f3cd53
mint_id: 50188abc36d747378eefee9284b2f691
type: experiment
parents:
  - hypothesis:every-adapter-restart-spawns-from-the-scrubbed-env
next_edges: []
confidence: 0.9
edited_by: a00-301fe6aa
evidence_runs:
  - experiment:a00-5571040e-f3cd53
loop: hypothesis:every-adapter-restart-spawns-from-the-scrubbed-env@s2
model: stealth/space-bunny-alpha
production_lines: 19
profile: balanced
role: kid
scaffold_hash: 9deb635481544ba6
season: 2
title: Scrubbing the EXPLICIT base at the adapter seam
town: core
verdict: proved
---
# experiment:a00-5571040e-f3cd53 — scrub the EXPLICIT base too

Parent's own probe named the gap: `scrubbed_base` returned `dict(explicit)`
verbatim, so the scrub was trusted-at-the-caller rather than enforced at the
adapter seam. `restart(base_env=dict(os.environ))` leaked
`{AGI_MODEL_SLOT_LOCK, ANTHROPIC_API_KEY, AGI_ORDERS_TEXT,
OPENROUTER_PROVISIONING_KEY}` (copilot) and
`{AGI_MODEL_SLOT_LOCK, ANTHROPIC_API_KEY, AGI_ORDERS_TEXT}` (claude_code).
Nothing leaked LIVE (the only in-tree caller passes `scrubbed_env()`), but
heal.py is the exact second-spawner precedent the docstring itself names.

## The build

One place, one list: `scrubbed_base` now FILTERS whatever it is handed
through `dispatch.ENV_VARS_TO_SCRUB` — the same tuple `scrubbed_env()` uses,
reached by a lazy `import dispatch` (no second list, no copy). Idempotent
over `scrubbed_env()`'s own output, which is already free of every name in
the tuple. `explicit` still wins over the inherited env; it just no longer
wins *unsanitised*.

```
             before                          after
explicit ──▶ dict(explicit)      explicit ─▶ filter(ENV_VARS_TO_SCRUB)
None     ──▶ dispatch.scrubbed_env()  None ─▶ dispatch.scrubbed_env()
```

| file | production lines |
|---|---|
| `extensions/agi/bin/adapters/__init__.py` | +16 / -3 |

The four `restart()`s and `dispatch.py` were NOT re-touched — the seam above
them is where the property belongs. 40-line ceiling, 19 used.

## Falsifiers (tests only, 5 new cases over 4 adapters)

- `test_scrubbed_base_filters_an_EXPLICIT_raw_environ` — a base holding every
  `ENV_VARS_TO_SCRUB` name comes back as exactly its non-scrubbed names.
- `test_restart_with_a_raw_environ_base_leaks_nothing[4 adapters]` —
  end-to-end: os.environ fully poisoned, `restart(base_env=raw)`, Popen stubbed;
  no scrubbed key reaches the child. (claude_code's own `ANTHROPIC_*`/
  `CLAUDE_CODE_*` restore is excluded — by design on the FIRST spawn too,
  which `CLAUDE_CODE_OWNS` already encodes.)

**Falsifier-verified**: reverting the one filter line in `scrubbed_base`
turns these red — `5 failed, 9 passed`. Restored: `14 passed`.

## Suite

| run | result |
|---|---|
| `test_restart_scrubbed_env.py` | 14 passed |
| `test_adapters.py test_dispatch.py test_restart_scrubbed_env.py` | 201 passed |
| 7 more dispatch/env files | 89 passed, **2 failed** |
| same 7 files with the fix reverted | 89 passed, **the SAME 2 failed** |

The 2 failures are pre-existing test-order pollution, not this round's:
`test_dispatch_forward_env.py::test_listed_name_reaches_the_child_when_the_shell_never_sourced_env`
and `test_agi_env_strip.py::test_conftest_stripped_all_agi_vars` (each passes
alone; both fail identically with the fix reverted). Recorded, not fixed —
out of scope for a 40-line seam.

## Verdict

**proved.** The parent's hypothesis — "every adapter restart spawns from the
scrubbed env" — now holds for EVERY argument, not just the one the in-tree
caller happens to pass. The leak is closed at the seam rather than at the
caller, so heal.py or any future second spawner is safe by construction.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.388, second kid. (1) INSTRUCTION: the previous kid auth probe -- restart(base_env=dict(os.environ)) made copilot hand the child AGI_MODEL_SLOT_LOCK, ANTHROPIC_API_KEY, AGI_ORDERS_TEXT and OPENROUTER_PROVISIONING_KEY -- so scrubbed_base had to FILTER the explicit base, not trust it, one scrub list, no copy. (2) WHAT THE MACHINE DOES: adapters/__init__.py scrubbed_base now returns dispatch.scrubbed_env() when explicit is None and otherwise {k: v for k, v in explicit.items() if k not in dispatch.ENV_VARS_TO_SCRUB} -- dispatch.ENV_VARS_TO_SCRUB, lazily imported, never a second list, idempotent over scrubbed_env output. I re-ran my own probe, the same script that failed before: copilot default {} / claude default {ANTHROPIC_API_KEY} / copilot base_env=RAW os.environ {} / claude base_env=RAW os.environ {ANTHROPIC_API_KEY}. The auth probe that FAILED on the previous kid now holds. (3) NEAR MISS: returning dict(explicit) with a docstring promising the scrub -- the words satisfied, the mechanism absent, and it survives exactly until the second spawner heal.pys precedent arrives. (4) DEVIATION: none from a standing rule; I re-ran one kid-suffixed test file myself and did not re-run their suite as evidence -- test_dispatch_forward_env.py::test_listed_name_reaches_the_child_when_the_shell_never_sourced_env is red here, and it is environment-dependent (it reads /data/work/agi/.env, which this box has no TYPESAFE_KEY in) and never reaches scrubbed_base: it calls child_env(base={}) with no explicit. Unrelated to the diff. The one residual, claude_code restoring ANTHROPIC_API_KEY from inherited (claude_code_adapter.py:378 RESTORED_NAMES), is identical on the FIRST spawn, so the restart base and the spawn base agree -- which is the property the hypothesis is actually about.
<!-- THOUGHT:END -->

## Agent Notes
scrubbed_base now filters ENV_VARS_TO_SCRUB out of an explicit base (one list, idempotent, 19 prod lines); falsifier-verified by reverting the one line (5 fail); 201+89 neighbour tests green, 2 pre-existing order-pollution failures unchanged

PROBES (parent-run): wire -- four scrub keys in os.environ, Popen stubbed, restart(base_env=None): pi/grok/copilot {}, claude_code {ANTHROPIC_API_KEY} (by design, RESTORED_NAMES, same on first spawn). auth -- the probe that failed the previous kid, restart(base_env=dict(os.environ)): now {} for both copilot and claude except that same restored name. gate -- the four restart()s and dispatch.py:3637 are byte-untouched by this kid; the filter is name-based so a harness env literal naming a scrubbed key would still pass, named in the kid own caveats. ACCEPTED.
