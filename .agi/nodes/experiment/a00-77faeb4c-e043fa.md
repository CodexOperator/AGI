---
id: experiment:a00-77faeb4c-e043fa
mint_id: 513667d398c84c399c794a4d2a457310
type: experiment
parents:
  - hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests
next_edges: []
confidence: 0.6
edited_by: a00-77faeb4c
evidence_runs:
  - experiment:a00-77faeb4c-e043fa
loop: hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 9a98712a30fa8d39
season: 2
title: "\"Free-lane mint + skills first_turn end-to-end tests: (a) proved, (b) falsified on one named live defect\""
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-77faeb4c-e043fa

# experiment:a00-77faeb4c-e043fa

## Verdict on the parent's two conjuncts

| conjunct | falsifier | measured | result |
|---|---|---|---|
| (a) `dispatch.main()` on a drained account | free lane does not mint at the cap / paid lane is not refused | free lane minted once at 0.01 (the CELL), paid lane exited 1 and minted nothing | **PROVED** |
| (b) the live templates' `skills` first_turn | exits non-zero, over its byte_cap, or omits a `skills/agi-*` dir on the trunk | rc 0, 4756/6000 bytes, but it OMITS `skills/agi-corrective`, which IS on the trunk | **DISPROVED (one named defect)** |

## What was added (tests only, 0 production lines)

- `extensions/agi/tests/test_free_lane_dispatch_main.py` — 3 tests. Drives the REAL
  `dispatch.main()` in-process against a tmp_path graph, with a stub adapter whose
  `needs_credential()` is True, a stubbed `Popen`, and `provisioning._call` faked to a
  201 + a throwaway key. `credit_balance` reads (10.0, 9.95, 0.05) — an account drained
  below every PAID floor (`min_mint_remaining_usd 1.0`, `min_account_remaining_usd 1.6`)
  and still above the free lane's own cap. Then:
  - free lane (`harnesses.pi.zero_usd: true`): exit 0, ONE mint, `limit == 0.01` read
    from `provisioning.zero_usd_key_limit_usd` in the project config, and NEITHER
    `check_runtime_key_usable` NOR `check_key_floor` was called (the skip is the claim);
  - paid lane (same balance, no `zero_usd`): exit 1, both floors ran, ZERO mints;
  - config-max: raising the cell raises the cap through the same code.
- `extensions/agi/tests/test_skills_first_turn_entry.py` — 3 tests. Reads
  `templates.*.startup.first_turn` from the LIVE `.agi/nodes/.geometry/rotations.md`
  (not a mirror), finds the `skills` entry, and RUNS its `cmd` in the live tree through
  `/bin/sh` — every clause is `write.py ... 'read payload N:M'`, so the graph is read,
  never written. Asserts: an entry exists for every role template; rc == 0; output under
  the entry's OWN `byte_cap` cell; and that the named `build:skills-<dir>-SKILL.md` set
  covers every `skills/agi-*` dir on the trunk.

## The defect the tests exposed — NAMED, not fixed (FILE SCOPE: tests only)

`config:rotations` carries the omission deliberately (belam-S2-L5-XIII 09-27 NEAR MISS:
"the clause is dropped until the node reaches the trunk"). **That premise is now false on
this tree**, so the entry is simply behind:

- `skills/agi-corrective/SKILL.md` IS on the trunk;
- `build:skills-agi-corrective-SKILL.md` IS on the trunk, and
  `write.py build:skills-agi-corrective-SKILL.md 'read payload 2:8'` exits 0, 540 bytes.

Consequence measured: every director and prime_director successor wakes with a skill index
that omits the agi-corrective flow skill — a skill every tier card now lists as a post's
own skill. Both templates would still fit their cap with the clause added (4756 + 540 =
5296 < 6000), so the fix is one clause per template, in the live `config:rotations` node
(prime/director-owned; out of this round's FILE SCOPE).

The coverage test therefore asserts `present - named == {"agi-corrective"}` and names
`OMITTED_DEFECT` + this node in its comment. That is honest in both directions: a SECOND
omission is red, and the day the clause is added the set must shrink to empty (also red
until it is dropped) — nobody can quietly grow the gap.

## Evidence

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest \
    extensions/agi/tests/test_free_lane_dispatch_main.py \
    extensions/agi/tests/test_skills_first_turn_entry.py -q
6 passed

# skills entry measured directly, both roles:
director        rc 0  bytes 4756  cap 6000
prime_director  rc 0  bytes 4756  cap 6000

# mutant check -- the free-lane skip deleted from dispatch.py:2348
# (`and dispatch_harness.get("zero_usd") is not True` removed):
$ pytest extensions/agi/tests/test_free_lane_dispatch_main.py -q
FAILED test_free_lane_mints_at_the_zero_usd_cap_on_a_drained_account
  ERR: account floor 0.005 below 1.6
1 failed, 2 passed      # dispatch.py restored; git diff --numstat clean of it

$ pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_bin_help_smoke.py \
    extensions/agi/tests/test_zero_usd_mint_floor.py -q
216 passed, 7 skipped
```

## Scope kept

- 0 production lines (`git diff --numstat` empty; the only files I touched are the two
  new test files and this node).
- <= 120 test lines: 124 + 74 (docstrings included).
- No network, no live pane, no real mint, no seat, no user/home/host/IP in any assertion.

## Follow-up for the parent (not this round)

One node, one clause: add `build:skills-agi-corrective-SKILL.md 'read payload 2:8'` to
the `skills` first_turn entry in BOTH live templates, and drop `OMITTED_DEFECT` to the
empty set in `test_skills_first_turn_entry.py` in the same commit. Measured to fit: 5296
of 6000 bytes.

## Agent Notes
(a) free-lane mint through dispatch.main() PROVED (mints at the cap cell, paid lane refused, mutant-checked); (b) the live skills first_turn omits skills/agi-corrective, which IS on the trunk -- falsifier (b) fires, defect NAMED not fixed (tests-only scope).
