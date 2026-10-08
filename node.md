---
id: experiment:a00-4b8b5e69-a4bdc7
mint_id: d44f91d105114c0f872c6469ec14a9ea
type: experiment
parents:
  - hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one
next_edges: []
confidence: 0.85
evidence_runs:
  - experiment:a00-4b8b5e69-a4bdc7
loop: hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 07893498b954d144
season: 2
title: A00 4b8b5e69 a4bdc7
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-4b8b5e69-a4bdc7

## Experiment

g15-7 FIX (hypothesis:l4-startup-first-turn-is-performed-by-the-service-
and-the-hook-fires-at-turn-one). IMPLEMENTED the pre-spawn seat identity /
bootstrap record claim on the built bytes, then proved it hermetically.

Defect (verified on today's bytes before edit): `rotate._shell_cmd()`
prepended only `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` (+ultracode)
and exported NO seat, so `AGI_SEAT` never reached the successor; the hook
COPY `cc-session-start.next.sh` reads `BOOTSTRAP_SEAT="${AGI_SEAT:-}"` and
is a silent no-op without it; and `_write_bootstrap` ran at s11 AFTER the
spawn, so no record existed at turn one regardless.

Changes (extensions/agi/bin/rotate.py):
1. `_shell_cmd(claude_cmd, settings, *, seat=None)` — when `seat` is given,
   prepend `export AGI_SEAT=<seat> && ` before the claude argv, composed
   the same way REAPER_ENV_EXPORT composes. No seat => byte-identical to
   today (proven by unit test). `spawn_window` gained `seat=None` keyword
   and passes it to `_shell_cmd`; `cmd_rotate_self` passes `seat=seat`,
   `cmd_seats_launch` passes `seat=name`. `cmd_spawn`/`cmd_loop` (no
   concrete seat) stay byte-identical.
2. `cmd_rotate_self`: moved verification computation + a NEW PRE-SPAWN
   `_write_bootstrap` to step 2.75, BEFORE the `spawn_window` call (step 3).
   Join-only facts (BOOTSTRAP_JOIN_ONLY_FACTS = successor_live_model,
   successor_address, model_refusal_fallback) are written with the explicit
   `"pending": "resolved after join"` marker (never blank, never a
   `SKIPPED: <predecessor owns>` reason). After the @id join, s11 REWRITES
   the SAME `<seat>.bootstrap.json` path in place with the resolved facts as
   `overrides` (successor_address from the window @id, successor_live_model
   from model_confirm) — verified: same path updated, join facts resolved.
3. New `_write_bootstrap` params `join_pending`/`overrides` (defaults keep
   every existing call byte-identical). Added BOOTSTRAP_JOIN_ONLY_FACTS.

Proof (extensions/agi/tests/test_session_start_seat_pre_spawn.py, 3 tests):
(a) `_shell_cmd` exports AGI_SEAT only when seat given; no-seat stays
    reaper+argv; export rides before the claude argv.
(b) a PRE-SPAWN record written by the PRODUCTION writer (the exact step-2.75
    call) is read back by the SAME reader the hook uses (`rotate.py
    bootstrap-block --seat --root` — path DERIVED, never hardcoded) and the
    hook COPY emits the block at "turn one" when AGI_SEAT is set; every
    join-only fact carries `pending: resolved after join`.
(d) FALSIFIER: the SAME hook, AGI_SEAT unset (the pre-fix artifact — no
    spawn path exported it), must NOT emit the block. Demonstrated: export
    present → block emitted; export absent → block absent (the guard fails
    to fire, so the injection genuinely depends on the export).

Real-tree dry-run proof of the export (requirement 1):
```
$ python3 extensions/agi/bin/rotate.py rotate-self --name sanctuary-director --dry-run
... export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 && export AGI_SEAT=sanctuary-director && claude --remote-control sanctuary-director ...
```

## Evidence

All suites passing (no git run):
- `python3 -m pytest tests/test_session_start_seat_pre_spawn.py -q` → 3 passed
- `... tests/test_session_start_bootstrap.py test_session_start_seat_pre_spawn.py test_rotate_startup.py test_rotate_templates.py -q` → 73 passed
- `... tests/test_rotate.py test_rotate_handover.py test_rotate_selfreap.py -q` → 155 passed
- `... tests/test_rotate_complete.py test_rotate_next.py test_rotate_tail.py test_seat_status.py test_rotation_alert.py -q` → 41 passed
- `... tests/test_cli.py test_commands.py -q` → 54 passed

Pre-spawn record + reader + hook differential (requirement 4 paste):
```
=== PRE-SPAWN record (production writer, path derived) ===
path: .../proj/sessions/seats/adv-alive.bootstrap.json
{ "commit": "1de799c", ..., "successor_live_model": "pending: resolved after join",
  "successor_address": "pending: resolved after join",
  "model_refusal_fallback": "pending: resolved after join", ... }
=== reader: rotate.py bootstrap-block (path the hook uses) ===
(rc=0) ## ⚓ bootstrap: adv-alive successor handover (shape v1 · gen 7 · HEAD@1de799c)
=== turn-one hook, AGI_SEAT exported === rc=0; block emitted: True
=== MUTATION, AGI_SEAT NOT exported === rc=0; block emitted: False   <-- guard depends on export
```

Post-join rewrite (same path updated):
```
SAME path updated after join: True
join-only facts after rewrite: {"successor_live_model": "claude-opus-5",
  "successor_address": "@295", "model_refusal_fallback": "pending: resolved after join"}
```

## Caveats
The live fresh-session turn-one verification is the PRIME's install step at
merge-up (proved on the COPY only per claim). The pre-spawn-vs-post-spawn
order is proven structurally (code position) + by the fixture firing, not by
an automated test that fails on a deliberately post-spawn write.

## Agent Notes
g15-7 FIX implemented+proved: spawn exports AGI_SEAT before claude (real-tree dry-run + unit); bootstrap record written PRE-spawn (step 2.75) with join-only facts marked 'pending: resolved after join', post-join rewrite updates same path; fixture test fires the hook COPY on the pre-spawn record (path derived via rotate.py bootstrap-block); falsifier shown (no-export => block absent). 323 tests green across rotate/session/cli suites.
