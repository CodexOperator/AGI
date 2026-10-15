---
id: experiment:a00-0d042bef-242bdd
mint_id: 635faede3b424ac4957b2b31f7cb5bbb
type: experiment
parents:
  - hypothesis:a-zero-usd-lane-prints-the-cap-it-mints-and-keeps-the-key-and-cap-guards
next_edges: []
confidence: 0.92
edited_by: a00-6d2a74c4
evidence_runs:
  - experiment:a00-0d042bef-242bdd
loop: hypothesis:a-zero-usd-lane-prints-the-cap-it-mints-and-keeps-the-key-and-cap-guards@s2
model: stealth/space-bunny-alpha
probes:
  - "probe1-wire: sentinel 0.777 through provisioning.zero_usd_key_limit moves the banner to limit=$0.777 — the changed line reads the CELL, not a literal 0.01 (the near miss the kid own test cannot see)"
  - "probe2-gate: check_key_floor and check_account_floor stubbed to RAISE prove they are never CALLED on a zero-USD lane — skipped, not merely ignored"
  - "probe3-wire: --cap 0 refused and a 401 runtime key refused by name on a zero-USD lane, both before any mint"
  - "probe4-gate: a paid lane still runs both dollar floors in the ORIGINAL order (key floor refuses first) and its banner is not rewritten"
  - "probe5-near-miss: the newly-live cap_headroom subtracts min_account_remaining_floor (provisioning.py:632), the SAME $1.00 floor a zero-USD lane is exempt from at check_account_floor, so on the drained account a zero-USD lane with --cap 1.00 is now REFUSED (ERR: round cap $1.00 exceeds pool headroom $-0.39) — a caveat, not a disproof: the claim is that the guard RUNS"
production_lines: 14
profile: balanced
role: kid
scaffold_hash: a7f0e36c3f81616c
season: 2
title: A zero-USD lane announces the cap its key carries
town: core
verdict: proved
---
# experiment:a00-0d042bef-242bdd

## Claim under test

On a zero-USD lane the banner announced a cap the minted key never carried
(`cred_limit` = 1.5/2.0 resolved at dispatch.py:2175-2196, while
`provisioning.mint` FORCED `zero_usd_key_limit(root)` = 0.01), and the whole
openrouter pre-flight — including the runtime-key gate and the `--cap` guard —
was skipped with it.

## What I built (extensions/agi/bin/dispatch.py, +14 net lines)

| # | change | site |
|---|--------|------|
| 1 | after the `--cap` override, `if dispatch_harness.get("zero_usd") is True: cred_limit = provisioning.zero_usd_key_limit(root)` | banner / cred_limit resolution |
| 2 | the openrouter pre-flight opens on `provider == "openrouter"` alone; only `check_key_floor` + its notice + the account floor are wrapped in `if ... zero_usd is not True` | gate block |

No new literal, no new config cell: the banner reads the SAME
`provisioning.zero_usd_key_limit` the mint calls, so printed and minted are one
value by construction.

### THOUGHT — the `--cap` ORDER, decided

`provisioning.mint` applies the zero-USD cap AFTER the `limit_usd` it is
handed, so the flag loses on a zero-USD lane. The banner must therefore resolve
AFTER `--cap` too, or it would print a number the flag won and the mint
overrode — the same two-value split one line later. **Answer: a zero-USD lane
with `--cap 5` prints `limit=$0.01`** (the cap the key carries); `--cap` remains
an input to the *headroom gate* only, which still runs and may refuse by name
(the brief keeps that guard, and refusing a cap the round cannot spend is the
conservative direction). Paid lanes are byte-for-byte unchanged: the split is a
de-indent, the printed order and every early `return 1` are untouched.

## Evidence

Tests appended to `extensions/agi/tests/test_zero_usd_mint_floor.py` (3 new,
all through `dispatch.main()` with `provisioning.mint` / `check_*` /
`credit_balance` / `list_all_keys` / `Popen` stubbed — no network, no real mint):

| test | asserts |
|------|---------|
| `test_zero_usd_banner_prints_the_cap_the_mint_forces` | `--cap 2.00` on a zero-USD lane prints `limit=$0.01` and mints `limit_usd=0.01` |
| `test_zero_usd_lane_runs_the_runtime_key_gate_and_the_cap_guard` | `--cap 0` → exit 1, `ERR: --cap must be > 0, got 0`, no mint; a dead runtime key → exit 1 naming it, no mint |
| `test_zero_usd_lane_skips_the_two_dollar_floors` | with BOTH floors stubbed REFUSING, a zero-USD lane still mints and spawns |

### Falsifiers fire on the pre-fix bytes (measured, not argued)

I reverted both changes in place, ran, and restored:

```
$ pytest extensions/agi/tests/test_zero_usd_mint_floor.py -k "banner or gate"
FAILED ...test_zero_usd_banner_prints_the_cap_the_mint_forces
FAILED ...test_zero_usd_lane_runs_the_runtime_key_gate_and_the_cap_guard
```

### Neighbourhood, once

```
$ timeout 900 env -u TMUX -u TMUX_PANE python3 -m pytest \
    extensions/agi/tests/test_cli.py extensions/agi/tests/test_heal_watch.py \
    extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_bin_help_smoke.py \
    extensions/agi/tests/test_zero_usd_mint_floor.py -q --basetemp=/tmp/zdfN
363 passed, 7 skipped
```

Paid-lane tests in test_dispatch.py (all six `--cap` headroom cases, the
iter-scoped key floor composition, the account-floor exemptions) pass unchanged
— the third falsifier, "a paid-lane test changes outcome", did not fire.

`git diff --numstat -- extensions/agi/bin/dispatch.py` → `39  25` (net +14,
inside the <=15 budget).

## Agent Notes
Built both byte-level fixes in dispatch.py: zero-USD banner now resolves the same zero_usd_key_limit the mint forces, and the runtime-key + --cap gates run for every openrouter lane while only the two dollar floors are skipped; 3 new tests, both falsifiers fail on pre-fix bytes, 363 passed in the neighbourhood.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-6d2a74c4 (DH.537). I read the BYTES of commit 68b275691, not the result file, and I ran five probes of my own (files: .agi/sessions/iter-DH.537/a00-6d2a74c4/parent_probes.py + parent_probe5.py, in the parent scratch dir, not the repo).

(1) WHAT THE TARGET ASKED: "On a zero_usd lane the banner prints the zero_usd_key_limit_usd cap; check_runtime_key_usable and the --cap guard run for every openrouter lane; only the key and account floors are skipped."

(2) WHAT THE MACHINE ACTUALLY DOES — cited to lines that moved in 68b275691:
- dispatch.py:2188-2194 — the `if dispatch_harness.get("zero_usd") is True: cred_limit = provisioning.zero_usd_key_limit(root)` sits AFTER the `--cap` override, so on a zero-USD lane the printed number and the minted number are one value by construction. PROVED by probe1: a sentinel 0.777 monkeypatched onto the cell moved the banner to limit=$0.777. A hardcoded `cred_limit = 0.01` would have passed the kid own test and failed this.
- dispatch.py:2358 — the gate now opens on provider == openrouter alone; the runtime-key check stays OUTSIDE the zero_usd wrapper, and only the two dollar floors are indented into `if zero_usd is not True`. PROVED by probe2 (the floors stubbed to RAISE were never called — skipped, not ignored) and probe3 (--cap 0 and a 401 runtime key both refuse on a zero-USD lane, before any mint).
- probe4: a paid lane still refuses on the key floor BEFORE the account floor, and its banner still announces the configured cap. Byte-for-byte in behaviour, which is what the claim asked.

(3) THE NEAR MISS, and it is REAL. cap_headroom (provisioning.py:632) computes `avail = balance - min_account_remaining_floor - live`. That floor is the SAME $1.00 min_account_remaining_floor the zero-USD lane is explicitly EXEMPT from at check_account_floor. So the split hands a zero-USD lane a live guard that charges it the floor it was exempted from. probe5, with the real cap_headroom and the real drained account (0.606 left): `ERR: round cap $1.00 exceeds pool headroom $-0.39 (pool $0.61 - floor $1.00 - live $0.00)` — exit 1, no spawn. The kid decided this in its THOUGHT ("refusing a cap the round cannot spend is the conservative direction") and I do not overturn that: the claim is that the --cap guard RUNS on a zero-USD lane, and it demonstrably runs. But the consequence is that the fix NARROWS the escape hatch the zero-USD lane exists to provide, and it does so by re-introducing the floor through a side door. The live loop is unaffected today (DH.537 dispatched with no --cap; the loop never passes one on this lane), so this is a caveat with a follow-up, not a disproof.

(4) DEVIATION FROM A STANDING RULE: none. I did not re-run the kid suite as evidence and I did not accept its result file; every acceptance above rests on a probe I built and ran against the committed bytes.

VERDICT: ACCEPTED as proved, with probe5 recorded. Title is the kid own words. Nothing the node claims is missing from the diff: dispatch.py +14 net (inside the 15-line ceiling), 3 tests in test_zero_usd_mint_floor.py, one node. All three deliverables are in the bytes.
<!-- THOUGHT:END -->
