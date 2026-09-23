---
id: experiment:dh137-non-persistent-spawn-regression
mint_id: a794fc4100c048be946073a207dd6963
type: experiment
parents:
  - hypothesis:a00-105e0c84-5e7222
next_edges: []
edited_by: a00-105e0c84
line_ceiling: 40
loop: goal:g7.28.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 548c6703cc512f72
season: 2
title: "DH.137 regression: --persistent is opt-in on supervision only; non-persistent kid/parent argv is unchanged"
town: core
---
<!-- BODY:BEGIN -->
# experiment:dh137-non-persistent-spawn-regression

## Experiment

**Claim under test (goal:g7.28.2):** `goal:g7.28.1`'s opt-in `--persistent`
mode did not change the non-persistent kid/parent spawn path — with the flag
ABSENT, argv, lifecycle and record stay fire-and-forget for BOTH tiers.

I extended `extensions/agi/tests/test_dispatch_persistent.py` (reusing its
`project` / `_fake_spawn` / `_argv` / `_manifest` harness) with one new test,
parameterized over `tier` in `{kid, parent}`:

`test_goal_g7_28_2_persistent_is_opt_in_on_supervision_only[kid|parent]`

Per tier it runs `dispatch.main()` twice against a scratch project through the
fake-spawn live path:

1. WITHOUT `--persistent` — asserts exactly ONE `Popen`, that
   `_supervise_persistent` was never entered (spied, calls == []), and that the
   manifest record carries neither `persistent` nor `restart_count`.
2. WITH `--persistent` (control, so the test cannot go green by the feature
   being deleted) — asserts the supervisor IS entered exactly once and the
   record IS stamped `persistent: true` / `restart_count: 0`.

Then ARGV PARITY: the two FULL child argv lists are compared for equality
after exactly two normalizations — the per-run session dir, and the minted
agent identity. Full-list equality, never a substring check.

Two harness facts the run forced out, both recorded rather than hidden:
* `tier=parent` needs a `parent` entry in the fixture's
  `harnesses.pi.models` (the live path refuses a tier with no model); the
  fixture now carries one.
* the scaffold node id embeds the agent id PLUS a per-mint
  `uuid4().hex[:6]` suffix (`a00-<8hex>-<6hex>`), so the agent-identity
  normalization is a regex over that whole token — otherwise the comparison
  reports a difference that is pure uuid noise, not the feature.

## Evidence

Command (exactly as the parent brief required):

```
python3 -m pytest extensions/agi/tests/test_dispatch_persistent.py \
    extensions/agi/tests/test_dispatch_dry_run.py -q
```

Observed (exit 0):

```
................................                                         [100%]
32 passed, 5 warnings in 1522.64s (0:25:22)
```

Per-tier confirmation earlier in the round:

```
-k "goal_g7_28_2 and kid"    -> 1 passed in 173.07s
-k "goal_g7_28_2 and parent" -> 1 passed in  18.58s
```

The new test fails on a real difference, not vacuously: the first version
asserted equality after normalizing only the agent id and the session dir, and
it correctly FAILED (the scaffold uuid suffix differed); the passing version
normalizes that same run-generated token. No production source was touched.
