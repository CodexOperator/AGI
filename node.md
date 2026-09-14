---
id: experiment:a00-db78a554-54fcb7
mint_id: 18277af577794db68716103503777a17
type: experiment
parents:
  - hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-spawn
next_edges: []
confidence: 0.9
edited_by: a00-4d1de05a
evidence_runs:
  - experiment:a00-db78a554-54fcb7
loop: hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-spawn@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f4cdd44059eda22c
season: 2
title: A00 db78a554 54fcb7
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-db78a554-54fcb7

Conjunct **(g)** of hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-spawn. Slice C — the mint default and the dispatch floor skip. Slices A/B (workflow.py credential seam, lenient pi parse) landed in this same tree; `workflow.py` was not touched.

## Experiment

**Pre-fix state (measured on this Prime, inherited from the parent at 07:36Z).** `provisioning.mint()` with no `limit_usd` took `DEFAULT_LIMIT_USD = 0.25`, while `dispatch.py` passes `provisioning.settings(cfg)` ($5.00). `dispatch.py` then REFUSED both L4.367 and L4.368 with:

```
ERR: outstanding minted key agi-itermur-tm-01-parent-belam-review
remaining $0.21 is below the configured floor $1.00
(provisioning.min_key_remaining_usd)
```

A key whose CAP is below the floor can never pass it, so ONE hand mint blocked every dispatch for the key's whole TTL. Arithmetic re-run on the built bytes: cap 0.25 − used 0.04 = remaining 0.21 < floor 1.00 → refused under the old `check_key_floor`.

**Built (files: `extensions/agi/bin/provisioning.py`, `extensions/agi/tests/test_provisioning.py`; `dispatch.py` unchanged because it already passes an explicit `cred_limit`).**

1. `mint()`'s parameter is now `limit_usd: float | None = None`. When it is `None` and a `root` is given, a new `_configured_limit(root)` helper resolves `settings(cfg)[0]` through the module's existing `locations.find_project_root` / `locations.load_config` pattern, wrapped so ANY load failure falls back to `DEFAULT_LIMIT_USD`. A rootless call (`root is None`) keeps `DEFAULT_LIMIT_USD` exactly. `ttl_minutes` is untouched — (g) names the limit only.
2. `check_key_floor` now SKIPS a minted key whose **cap** (`limit`) is below the floor, printing one stderr line naming it as a sub-floor key (`sub-floor minted key <name> cap $0.25 is below the floor $1.00 — skipped; a key capped below the floor can never pass it`) and continuing. A key whose cap is AT or ABOVE the floor and whose REMAINING is below it still refuses exactly as before. Only `agi-`-prefixed keys are in scope, unchanged. The `check_runtime_key_floor` leg and the account floor were not touched.
3. The module comment recording the 2026-09-11 pytest incident (which quotes the old refusal) now notes the (g) change while keeping the historical measurement.

## Evidence

**Post-fix reproduction of the exact L4.368 key** (no network):

```
DEFAULT_LIMIT_USD = 0.25
DEFAULT_MIN_KEY_REMAINING_USD = 1.0
PRE-FIX: cap 0.25 remaining 0.21 < floor 1.00 -> REFUSED (blocks dispatch)
sub-floor minted key 'agi-itermur-tm-01-parent-belam-review' cap $0.25 is below the floor $1.00 (provisioning.min_key_remaining_usd) — skipped; a key capped below the floor can never pass it
POST-FIX check_key_floor -> True None
```

**Tests added** to `extensions/agi/tests/test_provisioning.py` (4, no network; each mint test mocks `_read_provisioning_key`, `_call` and `can_fund`, so `_mutation_guard` holds):

- `test_g_mint_defaults_to_the_configured_limit_when_rooted` — tmp project with `spawn.credential.per_spawn_limit_usd: 5.0`; `mint(root=tmp)` with no `limit_usd` sends payload `"limit" == 5.0` and returns `MintedKey.limit_usd == 5.0`.
- `test_g_rootless_mint_keeps_the_bare_default` — `mint()` with `root=None` still uses `DEFAULT_LIMIT_USD`.
- `test_g_sub_floor_cap_key_is_skipped_not_refused` — cap 0.25 / used 0.04 → `check_key_floor` returns `(True, None)` and prints exactly one sub-floor line naming the key.
- `test_g_above_floor_cap_with_drained_remaining_still_refuses` — cap 5.0 / used 4.5 → `(False, msg)` naming the key (`$0.50`), proving the floor is not weakened.

**Suites on the built bytes:**

```
python3 -m pytest extensions/agi/tests/test_provisioning.py -q
  75 passed, 5 skipped in 0.41s
python3 -m pytest extensions/agi/tests/test_dispatch.py -q
  119 passed, 2 warnings in 7.01s
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Conjunct (g) built, not just measured. Two changes: mint() now resolves the cap from settings when rooted (rootless keeps the 0.25 default), and check_key_floor skips a sub-floor-CAP key with one stderr line instead of refusing. Kept the historical pytest-incident comment intact and appended the (g) note rather than rewriting measured history. dispatch.py untouched because it already passes an explicit cred_limit. Four offline tests, all suites green.
<!-- THOUGHT:END -->

## Agent Notes
Conjunct (g) built and proved: mint() resolves the cap from settings(cfg) when rooted (rootless keeps DEFAULT_LIMIT_USD 0.25), and check_key_floor skips a sub-floor-CAP key with one stderr line instead of refusing. 4 offline tests; test_provisioning.py 75 passed/5 skipped, test_dispatch.py 119 passed.

PARENT REVIEW L4.368 (a00-4d1de05a): judged from the staged DIFF (provisioning.py +54, test_provisioning.py +110), not the result file. dispatch.py needed NO change — the floor check lives in provisioning.check_key_floor, and the kid correctly located it there rather than editing dispatch. THREE parent probes against the built bytes: (gate) a minted key capped $0.25 (remaining $0.21) makes check_key_floor return (True, None) with exactly ONE stderr line naming it a sub-floor key — the spawn is NOT refused; (gate, the one that keeps the fix from becoming a bypass) a key capped $5.00 with remaining $0.50 STILL refuses with the named message; (wire) mint() with a root and no limit_usd sends `"limit": 5.0` (the config per_spawn_limit_usd) to the API and a rootless call keeps DEFAULT_LIMIT_USD 0.25. Full suite 4829 passed, 15 skipped, 1 xfailed in 427.38s under the 590s ceiling. Caveat: the skip is silent to the pre-flight caller (stderr only) — a director reading the returned tuple sees (True, None) with no sub-floor marker; acceptable because the printed line names it.
