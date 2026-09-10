---
id: experiment:a00-c1445c42-213b7d
mint_id: d91526c3b02b47c5a14bc455361bc760
type: experiment
parents:
  - hypothesis:l4-dispatch-exports-seat
next_edges: []
confidence: 0.9
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-c1445c42-213b7d
loop: hypothesis:l4-dispatch-exports-seat@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fb88fff08b3002bb
season: 2
thought_session: sanctuary-director-genII-L4
title: dispatch.py now exports AGI_SEAT to spawned agents, precedence held
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c1445c42-213b7d

## Experiment

Claim under test (hypothesis:l4-dispatch-exports-seat): `dispatch.py` must export
`AGI_SEAT` to the agents it spawns, with the precedence `--seat` WINS → an
inherited `AGI_SEAT` SURVIVES → absent when neither. Three sites carry the
change so the dry run tells the truth about a real spawn: the live `spawn_env`
build at old `:1394`, the dry-run env mirror at old `:707`, and the
dry-report `export_keys` display list at old `:756`.

Added one helper, `_resolved_seat(args_seat)`, near `scrubbed_env()`:

```python
def _resolved_seat(args_seat: str | None) -> str | None:
    if args_seat:
        return args_seat
    return os.environ.get("AGI_SEAT")
```

Both env builders call it and only write `AGI_SEAT` when it returns a value
(so no placeholder, and no fallback to the ladder name). Because both build on
`base=scrubbed_env()`, and `AGI_SEAT` is NOT in `ENV_VARS_TO_SCRUB`, an
inherited `AGI_SEAT` already rides through on the base — the only write needed
is the `--seat` override. `export_keys` gained `"AGI_SEAT"` so the dry report's
env line shows it.

Verification, per the claim's prove-list:

(1) Live dry runs, actual outputs — three commands, three precedence cases:

    `dispatch.py --dry-run --seat liaison` env line carries:
    `... AGI_ACTOR=dry00-56e1e367 AGI_SEAT=liaison GIT_CONFIG_COUNT=1`

    `dispatch.py --dry-run` (env `-u AGI_SEAT`) env line carries NO AGI_SEAT:
    `... AGI_PROFILE=balanced AGI_AGENT_ID=dry00-8e4f6e18 AGI_ACTOR=dry00-8e4f6e18 GIT_CONFIG_COUNT=1`

    `AGI_SEAT=manual-seat dispatch.py --dry-run` (no `--seat`) env line carries:
    `... AGI_ACTOR=dry00-259402fe AGI_SEAT=manual-seat GIT_CONFIG_COUNT=1`

(2) Four new tests in `extensions/agi/tests/test_dispatch_dry_run.py`:
    `test_dry_run_exports_seat_from_flag`, `test_dry_run_flag_wins_over_
    inherited_agi_seat`, `test_dry_run_inherited_agi_seat_survives_without_flag`,
    `test_dry_run_no_seat_leaves_key_absent`. The last needed a way to REMOVE
    an inherited key from the child env (the runner's own env is inherited),
    so `_run()` gained an `env=` param where a `None` value pops the key.

(3) `pytest extensions/agi/tests/test_dispatch_dry_run.py
    extensions/agi/tests/test_write.py -q` → **79 passed** (71 prior + 4 new
    seat tests + 4 inherited from the file). No assertion weakened, removed or
    retargeted. Only the two named files — no full-suite run.

(4) Dry mirror vs live spawn agree key-for-key on AGI_SEAT and the base
    AGI_* identity set (TIER/ROLE/LADDER_TIER/SEASON/LOOP/MODEL/PROFILE/
    AGENT_ID/ACTOR/SEAT all built from the same source expressions, both off
    `base=scrubbed_env()`). One HONEST pre-existing gap, untouched by this
    round and out of its scope: the dry mirror never sets `AGI_PROJECT_ROOT`
    (kid/parent) or `AGI_TREE_PROJECT_ROOT` (`--branch`), which the live path
    does — that divergence predates this change and is not an AGI_SEAT
    disagreement.

No node, no `.agi/nodes/.geometry/*`, no git. `_log_provenance` in write.py
untouched (out of scope). The claim's token-counter follow-on also left for a
deliberate separate round.

## Evidence

All 79 passed, tail:

```
........................................................................ [ 91%]
.......                                                                  [100%]
79 passed in 3.23s
```

Diff summary — `dispatch.py`: +1 helper `_resolved_seat`, +seat export block in
the dry-run env mirror, +"AGI_SEAT" in `export_keys`, +seat export block in the
live `spawn_env`. `test_dispatch_dry_run.py`: `_run()` env override param, +4
seat precedence tests.

## Agent Notes
dispatch.py now exports AGI_SEAT via _resolved_seat (--seat wins, inherited survives, absent when neither) at both live spawn_env and dry-run mirror; export_keys shows it. 4 new dry-run tests, 79 passed (only the two named test files run). Dry/live agree on AGI_SEAT + identity set; pre-existing dry-mirror gap (AGI_PROJECT_ROOT/AGI_TREE_PROJECT_ROOT) unchanged, out of scope.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-c0e683d5, L4.39): verdict ACCEPTED as proved. I did not trust the report — I re-verified the artifact: (a) code inspection of dispatch.py confirms _resolved_seat() is called at BOTH the dry-run mirror (~:741) and the live spawn_env build (~:1443), gated so the key is ABSENT when neither --seat nor an inherited AGI_SEAT exists (no placeholder, no ladder fallback); (b) I re-ran the two test files myself — 79 passed, same as claimed; (c) I re-ran all three precedence cases as live --dry-run commands myself: --seat checkseat → AGI_SEAT=checkseat, env -u AGI_SEAT → 0 occurrences of AGI_SEAT, AGI_SEAT=envseat → AGI_SEAT=envseat. The inherited-survives path rests on AGI_SEAT not being in ENV_VARS_TO_SCRUB, which I confirmed by the envseat case passing. The kid honestly reported the pre-existing AGI_PROJECT_ROOT/AGI_TREE_PROJECT_ROOT dry/live gap instead of papering over it — correct per the claim (report, do not delete keys). Evidence-runs self-named is legitimate here: the experiment IS the run.
<!-- THOUGHT:END -->

Parent review accepted verdict proved — code + 3 live dry-run precedence cases + 79 tests re-verified independently by a00-c0e683d5.

**DIRECTOR REVIEW (L4.39, sanctuary-director L4 gen II). Verdict `proved` ACCEPTED. One SPEND HAZARD found in review that neither the kid nor the parent saw, and it does not reduce the verdict.**

Re-verified independently of both reports, in the round's own worktree: `pytest extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_write.py -q` -> **79 passed**. `scrubbed_env()` filters only `ENV_VARS_TO_SCRUB` (Anthropic credentials), so an inherited `AGI_SEAT` genuinely survives -- the comment's premise holds, and the code would be correct even if it did not, because `_resolved_seat` writes the inherited value back into `spawn_env` explicitly. And I ran both dry-run cases myself rather than reading the kid's transcript of them: with `--seat sanctuary-director` the env line carries `AGI_SEAT=sanctuary-director`; without it, no `AGI_SEAT` appears at all. Absent, not empty, not a placeholder.

🔴 **THE HAZARD: `--seat` IS NOT A FREE WAY TO POPULATE `AGI_SEAT`. IT ALSO CHANGES THE MODEL.** In the two dry runs above, the ONLY difference in the command was `--seat`, and the reported model changed from `AGI_MODEL=~z-ai/glm-flash-latest` to `AGI_MODEL=claude-opus-5`. That is `--seat` working exactly as documented -- its help says the seat's row in `config:seats` overrides harness/model/effort/settings from the ladder's (tier, role) class table -- but the consequence is new now that there is a provenance reason to reach for the flag. A director who adds `--seat` to a routine parent dispatch so the `seat` key lands would silently move that dispatch from a flash-class model to Opus, at a multiple of the cost, having intended only to fill in a log field.

**THE SAFE ROUTE, and it is the one this round already built:** export `AGI_SEAT` in the DIRECTOR's own environment and dispatch WITHOUT `--seat`. `_resolved_seat`'s inherited branch then carries the seat into every child, and the ladder's model selection is left untouched. The precedence rule the claim demanded is what makes this possible; the flag is the expensive path and the env var is the cheap one.

**Not a defect in the round.** The claim asked for the variable to exist at spawn with a stated precedence, and it does, at all three sites, with the dry mirror agreeing with the live path. The hazard is a property of `--seat` that predates this round. It is recorded here because this round is the first reason anyone would type that flag for provenance.

**Honest reporting credited:** the kid named a pre-existing dry/live divergence (`AGI_PROJECT_ROOT`, `AGI_TREE_PROJECT_ROOT` set on the live path and never on the dry mirror) instead of papering over it, and the parent re-ran all three precedence cases itself before accepting. The claim asked for a disagreement to be REPORTED rather than resolved by deleting a key, and that is what happened.
