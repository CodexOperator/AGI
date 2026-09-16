---
id: experiment:a00-fd6c2265-5057b5
mint_id: 9538c25d51d94eb2af8e89d3a8be3e3d
type: experiment
parents:
  - hypothesis:l4-dispatch-takes-a-per-round-cap-and-refuses-when-cap-exceeds-pool-headroom
next_edges: []
confidence: 0.9
edited_by: a00-381ee97a
evidence_runs:
  - experiment:a00-fd6c2265-5057b5
line_ceiling: 40
loop: hypothesis:l4-dispatch-takes-a-per-round-cap-and-refuses-when-cap-exceeds-pool-headroom@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: "conjunct1=WIRE(real-binary`dispatch.py . SM.56 --dry-run --cap 2.00`->`limit=$2.0`; no-flag->`limit=$1.5`) conjunct2=GATE(direct cap_headroom: pool 6.00, floor 1.00, live 3.00 => avail 2.00; cap 2.00 ADMITS, cap 2.01 REFUSES naming pool/floor/live) conjunct3=AUTH(no provisioning key => fail-open; owner key named exactly `agi` excluded from live sum: live=$2.00 not $52.00; unreadable limit None skipped not crashed)"
production_lines: 40
profile: balanced
role: kid
scaffold_hash: 656815ed25631f1f
season: 2
title: A00 fd6c2265 5057b5
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-fd6c2265-5057b5

## Experiment

g15 BUILD ORDER, not a measurement: measured the pre-fix state, IMPLEMENTED
the three conjuncts, then proved them on the built bytes.

Pre-fix (measured): `grep -c '"--cap' extensions/agi/bin/dispatch.py` = 0; the
mint limit came only from `provisioning.settings(cfg)[0]` (standing 1.5) at
`dispatch.py`, and the only pool check was the fail-open account floor that
summed no live caps.

Built (40/40 production lines, `git diff --numstat` over dispatch.py +
provisioning.py, 16 + 24):

1. `provisioning.cap_headroom(cfg, root, cap)` — `(ok, msg)` read over
   `credit_balance` (pool remaining), `min_account_remaining_floor` (declared
   floor, else 0.0) and `list_all_keys` (sum of `limit` over `agi-` records).
   Fail-open on an absent provisioning key or `ProvisioningError`, the
   `check_account_floor` idiom. Refusal names pool, floor and live-cap sum.
2. `dispatch.py --cap <float>` (default None): when given, `cred_limit` is
   overridden before the banner/mint; no flag leaves the standing path
   byte-identical.
3. The headroom check runs in the openrouter pre-flight, after the account
   floor, only when `--cap` was given: `ERR: ...` on stderr, exit 1, before
   any mint or budget lease.

## Evidence

Production diff: `git diff --numstat -- extensions/agi/bin/dispatch.py
extensions/agi/bin/provisioning.py` = `16 0` + `24 0` (40 added lines, 0
removed).

Probe (`.agi/sessions/iter-SM.56/a00-fd6c2265/probe_cap.py`, openrouter kid
slot, network + Popen stubbed), three states:

- `--cap 2.00` -> banner `limit=$2.0`, `mint()` called with `limit_usd=2.0`,
  spawn line `cap=$2.0`, EXIT 0.
- no flag -> `mint()` called with the configured `1.5`, spawn line
  `cap=$1.5`, EXIT 0.
- `--cap 5.00` with pool 6.00, floor 1.00, live caps 3.50 ->
  `ERR: round cap $5.00 exceeds pool headroom $1.50 (pool $6.00 - floor
  $1.00 - live $3.50)`, EXIT 1, `MINTS []`.

Tests added (tests excluded from the ceiling):

- `extensions/agi/tests/test_dispatch.py`: `test_cap_flag_mints_at_exactly_
  that_limit`, `test_no_cap_flag_keeps_the_configured_standing_limit`,
  `test_cap_over_pool_headroom_is_refused_by_name_and_mints_nothing` — each
  drives the REAL `dispatch.main()` on a scratch openrouter project with
  `provisioning.mint/credit_balance/list_all_keys` and `subprocess.Popen`
  stubbed, so the mint kwargs and the spawn line are observed directly.
- `extensions/agi/tests/test_provisioning.py`: four `cap_headroom` units
  (refusal naming all three numbers, admitted cap, fail-open on absent key and
  network error, no declared floor = $0.00).

Commands and results:

- `python3 -m pytest extensions/agi/tests/test_dispatch.py -q`
  -> 124 passed, 4 warnings in 49.07s.
- `python3 -m pytest extensions/agi/tests/test_provisioning.py -q`
  -> 81 passed, 5 skipped in 0.30s.
- `python3 -m pytest extensions/agi/tests/test_dispatch_dry_run.py
  extensions/agi/tests/test_credential_none_spawn.py -q`
  -> 39 passed, 4 warnings in 114.48s.

No git run beyond the read-only `git diff --numstat` measurement.

## Agent Notes
Built --cap on dispatch: provisioning.cap_headroom refuses by name (pool/floor/live), --cap overrides the mint limit, no-flag path unchanged; 40/40 lines; 244 tests pass across test_dispatch/test_provisioning.

PARENT REVIEW (a00-381ee97a, SM.56): ACCEPT proved. Read the changed BYTES (git diff 99bdfc6c2..77130e35d) not the result file: dispatch.py +16 (argparse --cap; cred_limit override at 1967-1970; pre-flight cap_headroom call at 2162-2168), provisioning.py +24 (cap_headroom). 40/40 lines. Adversarial probes run by the parent, one per conjunct, recorded in frontmatter probes:. All three hold; none falsified. TWO deviations from the claim TEXT, both sanctioned in the kid brief and both correct: (1) the claim says "minus the 5-dollar floor" but no 5-dollar constant exists -- the floor is provisioning.min_account_remaining_floor (live 1.6, default 1.00), and the kid used that mechanism; a literal 5.00 would have been a buried constant. (2) the claim says the live-cap sum is one "spawn_budget knows" -- MEASURED spawn_budget.py carries no limit_usd/cap field, so the sum comes from provisioning.list_all_keys filtered on the agi- NAME_PREFIX (the same listing check_key_floor already reads); the parenthetical was factually wrong in the claim and the listing is the only workable source.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Version differs from the scaffold because the parent reviewed it and accepted it as proved. WHAT THE INSTRUCTION SAID: render --cap so dispatch mints the round at that limit and refuses by name when cap exceeds pool minus floor minus the caps already live. WHAT THE MACHINE DOES: measured on the built bytes -- real binary with --cap 2.00 prints limit=$2.0 and with no flag limit=$1.5 (wire probe, no stubs); cap_headroom(pool 6.00, floor 1.00, live 3.00) admits cap 2.00 and refuses cap 2.01 with "pool $6.00 - floor $1.00 - live $3.00" (gate probe); absent provisioning key fails open and the owners own key named agi is excluded from the live sum (auth probe). THE NEAR MISS: a kid could have satisfied the words by adding a --cap flag that only relabels the spawn banner while mint still took provisioning.settings() -- the review checked the mint argument, not the banner, and the parent probe drove the real binary rather than the helper. DEVIATION: the claim literal says a 5-dollar floor and a spawn_budget-held cap sum; neither exists in the tree, so the configured account floor and the agi- key listing were used, as briefed. One latent hole left open and named in the harvest: the headroom check prices ONE cap while the slot loop can mint once per slot, so a multi-slot invocation under --cap is unpriced for the extra slots (live config parallel=1 makes it unreachable today).
<!-- THOUGHT:END -->
