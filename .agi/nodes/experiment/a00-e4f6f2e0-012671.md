---
id: experiment:a00-e4f6f2e0-012671
mint_id: a69ab6989812410ca262b61a924a4a8d
type: experiment
parents:
  - hypothesis:l4-the-floor-must-watch-the-account
next_edges: []
confidence: 0.85
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-e4f6f2e0-012671
loop: hypothesis:l4-the-floor-must-watch-the-account@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0b3de38e10b5c441
season: 2
thought_session: sanctuary-director-genIV-L4
title: "Account floor preflight: fail-closed on account, fail-open on absence"
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e4f6f2e0-012671

## Experiment

Implemented the account leg of the pre-flight so the spend floor reads the number
that actually moves, per `hypothesis:l4-the-floor-must-watch-the-account`.

**Code (2 files + a proposed config default):**

1. `extensions/agi/bin/provisioning.py` — added `DEFAULT_MIN_ACCOUNT_REMAINING_USD
   = 1.00`, `min_account_remaining_floor(cfg)` (reads
   `provisioning.min_account_remaining_usd`; **returns None when absent** — the
   account floor is OPT-IN so a project that has not declared one keeps today's
   behaviour, and the short-circuit happens BEFORE the account is read), and
   `check_account_floor(cfg, root) -> (ok, msg)`:
   - floor present + `credit_balance(root)` present and remaining `<= floor` →
     `(False, msg)` — **fail-closed**, the guard's whole point.
   - `ProvisioningError` from `credit_balance` (network error) → `(True, None)`
     — **fail-open**, an unreachable API is not evidence of exhaustion.
   - `credit_balance` returns None (no provisioning key) → `(True, None)` —
     fail-open, absence is a supported state.
   - absent config → `(True, None)` before touching the network.
   Matches `check_key_floor`'s existing idiom rather than inventing a second.
2. `extensions/agi/bin/dispatch.py` — the openrouter pre-flight now calls
   `check_account_floor` right AFTER `check_key_floor`, ADDITIVE and never
   replacing it: a refusal on either ground returns 1.
3. `.agi/config.json` — proposed `provisioning.min_account_remaining_usd: 1.00`
   (the brief says the default is the owner's to set; I propose 1.00 and defend
   it in Evidence).

**Verification runs:**

- New tests (6) in `extensions/agi/tests/test_provisioning.py`, one per
  falsifier (a)(b)(d) plus the stays-healthy and key-floor-unchanged (c) cases:
  `python3 -m pytest extensions/agi/tests/test_provisioning.py -k l4a -q` →
  **6 passed**.
- Both files, minting live tests explicitly excluded (see Evidence for why):
  `python3 -m pytest extensions/agi/tests/test_provisioning.py
  extensions/agi/tests/test_dispatch.py -q -k "not live and not capped_and_expires
  and not expires_in_seconds and not no_ttl"` → **136 passed, 5 deselected**.
- `python3 extensions/agi/bin/dispatch.py . L4.99 --target
  hypothesis:l4-the-floor-must-watch-the-account --dry-run` → **exit 0**, guard
  did not block the dry run (account $3.92 > floor $1.00).
- `python3 extensions/agi/bin/commands.py run verify` → **exit 0, all 8 checks
  GREEN** (links broken=0, goals byte-identical=1, smoke active=1765 /
  deprecated=194 / total=1959, dispatch-help, budget, node-count).

## Evidence

Account read live before the run: `credit_balance(/home/ubuntu/work/agi)` →
`(92.0, 88.080512108, 3.92)`. A floor of $1.00 therefore does not gate the live
loop today — safe to make active as a proposal.

Proposed default defence: $1.00 equals the key-floor default and
`MIN_REMAINING_CREDITS`, so a refused account can still guarantee one more mint
remains fundable. At the measured $0.0977/round it refuses only at the final
~10 rounds. **This is a proposal, not a ruling** — the owner picks the number
against the real rate.

The six falsifier tests, in one pass:

```
$ python3 -m pytest extensions/agi/tests/test_provisioning.py -k l4a -q
......   6 passed
```

Falsifier coverage mapped to tests:
- (a) THE falsifier — `test_l4a_below_floor_named_config_refuses_a_spawn`:
  account at $0.50, every key full → `check_account_floor` refuses, names
  `account` and `$0.50`.
- (b) fail-open — `test_l4a_fails_open_on_a_network_error` (ProvisioningError →
  `(True, None)`) and `test_l4a_fails_open_on_an_unreadable_account_reading`
  (credit_balance → None → `(True, None)`).
- (d) absent config no-op — `test_l4a_absent_config_leaves_behaviour_identical_to_today`:
  asserts the account is NOT even read when `min_account_remaining_usd` is
  absent (network untouched).
- (c) key floor unchanged — `test_l4a_the_key_floor_still_refuses_exactly_what_it_refuses`:
  a drained minted key still refuses via the untouched `check_key_floor`; a
  drained account is a second, additive refusal ground.
- healthy — `test_l4a_account_above_the_floor_passes`.

No existing test was edited; the `live` marker and ROOT were not repointed.

`verify` exit 0 (tail):

```
PASS  links        [broken=0]
PASS  goals-check  [byte-identical=1]
PASS  write-guard
PASS  smoke        [active=1765, deprecated=194, total=1959]
PASS  viewport-verify
PASS  dispatch-help
PASS  budget
PASS  node-count
RESULT: PASS (all 8 checks green)
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The brief warned the `test_provisioning.py` live tests "must stay skipped" — but
in THIS environment the provisioning key is live in `/home/ubuntu/work/agi/.env`
(or the worktree's), so `provisioning.available()` is True and the five `@live`
tests are NOT skipped: they mint and revoke REAL metered keys against the API.
`-m "not live"` does NOT deselect them, because `@live` is a `pytest.mark.skipif`
marker, not a selectable `live` tag — so I excluded the five by name with `-k`
for the clean green count, rather than minting real keys a second time.
<!-- THOUGHT:END -->

## Agent Notes
Implemented the account floor pre-flight (fail-closed on a present reading at/below min_account_remaining_usd, fail-open on network error or absent reading, OPT-IN on absent config) additive to check_key_floor in the dispatch pre-flight; proposed min_account_remaining_usd=1.00 in config; 6 new tests all green, live-minting tests excluded by name, dry-run exit 0, verify all 8 PASS.

PARENT REVIEW (a00-775f0734) — ACCEPTED, verdict proved stands. Checked bytes, not report: check_account_floor present in provisioning.py (fail-closed on present reading at/below floor, fail-open on ProvisioningError and on None reading, short-circuits BEFORE network when config absent — opt-in as specified); dispatch.py call is additive, placed immediately after check_key_floor, either ground refuses; 6 l4a tests re-run by me, 6 passed; dry-run exit 0 re-confirmed; config proposal min_account_remaining_usd=1.0 present and defended as a proposal per brief. Evidence self-named (experiment IS the run) — legal. No existing test edited, no key floor lowered, one config idiom reused. Runway arithmetic quoted as required.

DIRECTOR REVIEW, sanctuary-director, on merge. VERDICT `proved` STANDS. Additive and opt-in by construction, which is the part that makes it safe to land on a live loop: `min_account_remaining_floor` returns None when the project has not declared the key, so a project without one keeps exactly today's behaviour. The default is DEFENDED rather than picked -- set equal to the key floor and to `MIN_REMAINING_CREDITS`, so a refused account can still guarantee one more mint remains fundable. The fail-open distinction that has now been the sharpest line in three consecutive briefs held again: a present reading below the floor refuses, an absent or unreadable one passes, and the round matched `check_key_floor`'s existing idiom instead of inventing a second. No existing test edited; the `provisioning.py` diff is purely additive.

VERIFIED LIVE, because this round gates spawning and a wrong landing presents as a loop that cannot dispatch rather than as bad data: `min_account_remaining_floor` reads 1.0 from the live config, `check_key_floor` returns `(True, None)` against the real account, and `dispatch.py --dry-run` exits 0. The floor is now ARMED at $1.00, which is exactly the prime's standing stopping rule expressed in code rather than in a brief.

ONE HYGIENE FIX ON MERGE: the round's `.agi/config.json` edit dropped the file's trailing newline. Restored, JSON re-validated. Its incidental rewrite of two `\u2014` escapes to literal em-dashes in unrelated `note` fields is semantically identical JSON and I left it rather than add churn reverting churn.

SECOND MEASURED ROUND, and the rate is now two readings rather than one: this round itself cost **$0.0749** on `account.used` ($88.0246 -> $88.0995), against **$0.0977** for L4.75. So a dispatched round with one kid runs roughly $0.075-$0.10, the account stands at $88.10 of $92, and the runway is about **40-50 rounds**. Both numbers were taken with the instrument this chain built, before and after, rather than estimated.
