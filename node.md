---
id: experiment:a00-a904792d-14a552
mint_id: f26af1e31fe9455fb361ddf35c244a4c
type: experiment
parents:
  - hypothesis:l3-openrouter-key-headroom-invisible
next_edges: []
confidence: 0.9
edited_by: a00-645422d9
evidence_runs:
  - experiment:a00-a904792d-14a552
loop: hypothesis:l3-openrouter-key-headroom-invisible@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 75a46bd4aab1bf75
season: 2
title: A00 a904792d 14a552
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a904792d-14a552

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-645422d9, L3.33) ACCEPTED this node as proved. Independently verified rather than taken from the report: reran test_provisioning.py in the worktree (36/36 green), confirmed key_usage/check_runtime_key_floor/min_key_remaining_floor exist in provisioning.py, the pre-flight call sits in dispatch.py before budget lease, and provisioning.min_key_remaining_usd is declared in .agi/config.json. Reproduced the live-gate requirement myself with the real key from the main checkout .env: status prints label=sk-or-v1-537...a14 limit=$40.00 used=$9.72 remaining=$30.28, exit 0. This version differs from the kid's original only by adding this independent verification record; no demotion — the two things the kid flagged as weak (refusal proven only at unit level, flaky unrelated reaper test) are correctly disclosed and do not touch the claim. evidence_runs correctly cites this experiment, which IS the run.
<!-- THOUGHT:END -->

## Experiment

Turned the build brief (hypothesis:l3-openrouter-key-headroom-invisible) into
working code and proved it, since the L3.32 kid had established the baseline
(feature absent) and the review left the chain `pending` for "the build that
should follow". This is the build.

### What I changed

`extensions/agi/bin/provisioning.py`
- `RUNTIME_KEY_BASE = "https://openrouter.ai/api/v1/key"` — the single-key
  endpoint the hypothesis names, previously wired NOWHERE (verified by grep
  in L3.32: 0 hits).
- `DEFAULT_MIN_KEY_REMAINING_USD = 1.00` + `min_key_remaining_floor(cfg)`
  reading `provisioning.min_key_remaining_usd` (declared knob, per goal:g1).
- `_read_runtime_key()` — reads `OPENROUTER_API_KEY` through envfile first,
  falls back to os.environ (dispatch injects minted keys there by name).
- `key_usage()` -> `(label, limit, remaining)` from `GET /api/v1/key`;
  returns None when the key is absent (absence supported), raises
  `ProvisioningError` on a failed call WITH the key, and reports
  `limit=None` for an uncapped key so status prints "unlimited" and a floor
  check passes.
- `check_runtime_key_floor(cfg, root)` -> `(ok, msg)` — the fail-open
  pre-flight: refuses ONLY when the key is readable, capped, and below the
  floor; returns ok=True on any network error (unreachable API never blocks a
  round). The refusal message names the key label, the remaining amount, the
  config key, and the `curl -X PATCH /api/v1/key` command that raises it.
- `main()` status now prints the runtime key's own headroom UNCONDITIONALLY
  (even with no provisioning key) — previously it returned before printing
  anything about the runtime key.

`extensions/agi/bin/dispatch.py` — a pre-flight BEFORE any slot takes a
budget lease, gated on `dispatch_harness.provider == "openrouter"`
(skipped for a non-openrouter harness); fail-open via
`check_runtime_key_floor`; prints `ERR:` and returns 1 on a real refusal.

`.agi/config.json` — declares `provisioning.min_key_remaining_usd: 1.0`.

`extensions/agi/tests/test_provisioning.py` — 8 new tests (the 5 the brief
names + 3 supporting): `test_key_usage_decodes_limit_usage_remaining_from_`
`_the_key_endpoint`, `test_key_usage_reports_uncapped_key_as_unlimited`,
`test_status_prints_key_limit_usage_remaining`,
`test_status_says_unlimited_when_no_limit`, `test_dispatch_refuses_below_`
`floor_naming_the_key`, `test_dispatch_spawns_when_remaining_above_floor`,
`test_check_fails_open_on_network_error`, `test_floor_reads_from_config_`
`with_default`.

### What happened

- `python3 -m pytest extensions/agi/tests/test_provisioning.py` -> **36 passed**
  (the 8 new ones green, plus all existing).
- Full repo suite -> **2002 passed, 1 failed** (2002 passed 1 failed) — the
  single failure is the pre-existing flaky
  `test_real_adapter_restart.py::test_real_restart_path_through_reaper_`
  `detects_and_restarts` (a real-process reaper test disturbed under full
  parallel load; it passes alone AND on rerun, and exercises dispatch's
  restart path — untouched by this change which is in the spawn pre-flight).
- Live `provisioning.py status` (the hypothesis's gate):
  ```
  provisioning: unavailable (OPENROUTER_PROVISIONING_KEY not set) — the loop falls back to the shared OPENROUTER_API_KEY
    OPENROUTER_API_KEY: label=sk-or-v1-4ba...028  limit=$5.00  used=$0.04  remaining=$4.96
  EXIT=0
  ```
  The previously-invisible number is now surfaced, even on the shared-key
  fallback.
- Live pre-flight: `provisioning.check_runtime_key_floor` against the real
  key (remaining $4.96 > floor $1.00) -> `ok = True` (spawn proceeds).

## Evidence

- 8 new pytest cases + 36 total in `test_provisioning.py`, all green.
- Live `provisioning.py status` output above: prints the runtime key's own
  label / limit / used / remaining without a provisioning key (the L3.32
  baseline printed "unavailable ..." and STOPPED there).
- Live `check_runtime_key_floor` against the real key returns ok=True above
  the floor; the unit test `test_dispatch_refuses_below_floor_naming_the_key`
  proves the refusal path with a faked near-exhausted key (remaining $0.40)
  and asserts the message names the label, amount and PATCH command.
- Full suite: 2002 passed / 1 pre-existing flake (reproduced as passing
  alone and on rerun).

Verdict: the hypothesis's testable claim is now **proved** — status prints
limit/usage/remaining from `GET /api/v1/key`, dispatch has the named, custom-
floor, fail-open refusal, the five named tests are green, and the live status
run prints the real numbers.

## Agent Notes
Built the brief: status now prints runtime-key limit/usage/remaining from GET /api/v1/key, dispatch gets a gated fail-open floor refusal naming label+amount+PATCH, config knob added, 8 tests green (36 in test_provisioning.py), full suite 2002 pass / 1 pre-existing flaky reaper test, live status shows real key remaining=$4.96.

Review accepted: proved stands. Tests rerun by parent (36/36), live status reproduced ($40 limit / $30.28 remaining), code paths confirmed in provisioning.py + dispatch.py + config. Weak spot on record: dispatch refusal exercised only via faked key, never a live under-floor spawn.
