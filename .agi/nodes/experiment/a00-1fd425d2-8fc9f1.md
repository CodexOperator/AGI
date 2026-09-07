---
id: experiment:a00-1fd425d2-8fc9f1
mint_id: 43cef87da1384b989b0063a2f870db83
type: experiment
parents:
  - hypothesis:l3w4-seat-registry
next_edges: []
confidence: 0.7
edited_by: a00-a5800e67
evidence_runs:
  - experiment:a00-1fd425d2-8fc9f1
loop: hypothesis:l3w4-seat-registry@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 02218f367d78cf66
season: 2
title: A00 1fd425d2 8fc9f1
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1fd425d2-8fc9f1

## Experiment

Built the seat registry (hypothesis:l3w4-seat-registry, the RE-RUN AS BUILD
after experiment:a00-34185da7 validated only the mechanism with a hardcoded
row) — all three claimed surfaces, red-first:

1. **config:seats node** — `.agi/nodes/.geometry/seats.md`, type `config`,
   one row per seat: name, role, tier, harness, model, effort, settings,
   session_kind, personality_ref, handoff_file, pin_ref, rotated_by,
   owning_goal. Rows (owner correction 4 overrides 3): `belam`
   fable-5-1/max/ultracode; the three advisors `adv-self-perpetuating` /
   `adv-all-is-one` / `adv-alive` opus-5/max (no ultracode); `liaison`
   sonnet-5/high owning goal:g17; `dir-g1`/`dir-g15`/`dir-g16` one opus-5/high
   director per perpetual goal besides g17. Added `seats: list` to
   `context/schemas/[config].md`.
2. **dispatch.py `--seat <name>`** — new `resolve_seat_spec(seats, name)` plus
   a `--seat` flag whose row overrides the (tier, role) ladder class table via
   the existing harness-override branch. `read_seat_registry` in spawn_gate.py
   (fails open: no node / no row -> None).
3. **rotate.py `meter --seat <name>`** — `find_pin_log`/`resolve_transcript`
   take a `seat` arg and read `.agi/sessions/<name>.meter` (seat-stable) over
   the newest-mtime pin; the claude adapter's `record_session_pin` writes the
   seat-stable pin when `AGI_SEAT` is set.

Tests added: `test_resolve_seat_spec_liaison_returns_sonnet_high_not_opus`,
`test_dispatch_seat_flag_overrides_role_and_ladder_tier`,
`test_resolve_seat_spec_none_when_missing_fails_open` (test_dispatch.py);
`test_read_seat_registry_none_when_node_absent_fails_open` +
`test_read_seat_registry_returns_declared_rows` (test_spawn_gate.py);
`test_seat_pin_stable_across_two_rotations_same_name` (test_rotate.py).

Gate evidence (run against the real graph):

    $ dispatch.py . iter-1 --seat liaison --dry-run
      seats: seat liaison -> claude-code/claude-sonnet-5/effort=high/settings=-
      roles: tier=0 role=kid -> claude-code/claude-sonnet-5/effort=high/settings=-
      command: claude -p --model claude-sonnet-5 --effort high ...
      (no --settings flag)

    $ dispatch.py . iter-1 --seat belam --dry-run
      seats: seat belam -> claude-code/claude-fable-5-1/effort=max/settings=ultracode
      command: claude -p --model claude-fable-5-1 --effort max --settings '{"ultracode": true}' ...

    $ dispatch.py . iter-1 --seat nobody --dry-run          (fails open)
      seats: no row for seat 'nobody'; falling back to ladder/config
      roles: tier=0 role=kid -> pi/~deepseek/deepseek-v4-flash-latest/...

    $ rotate.py meter --seat belam                           (no pin yet -> graceful)
      0.3214 ... source=claude-code transcript (newest heuristic)   EXIT=0

Full suite: 1866 passed, 1 skipped. `links.py schema` flags no new violation
(config:seats not among the 132 pre-existing). `snapshot-goals.py --render
--check` round-trip byte-identical. Unit test proves the seat pin wins a
newer foreign pin: `.agi/sessions/belam.meter` (0.020) over
`zzz-newer.meter` (0.400) -> 0.020.

## Evidence

- `nodes/.geometry/seats.md` — 8 rows (belam, 3 advisors, liaison,
  dir-g1/dir-g15/dir-g16).
- `extensions/agi/bin/dispatch.py` — `resolve_seat_spec` + `--seat` wired into
  main() after `root` resolves, reusing the ladder override branch.
- `extensions/agi/bin/spawn_gate.py` — `read_seat_registry`.
- `extensions/agi/bin/rotate.py` — `find_pin_log(root, seat)`;
  `resolve_transcript(..., seat=)`; `cmd_meter` passes `--seat`.
- `extensions/agi/bin/adapters/claude_code_adapter.py` — `record_session_pin`
  keys on `AGI_SEAT` when set.
- `extensions/agi/context/schemas/[config].md` — `seats: list` field.
- Tests: test_dispatch.py (+3), test_spawn_gate.py (+2), test_rotate.py (+1).

THOUGHT:BEGIN — authored
Why THIS version: the prior experiment (a00-34185da7) validated only the
override *mechanism* with a hardcoded row and built nothing; this one builds
all three claimed surfaces and passes every gate the CLAIM names (dry-run
output + tests + suite + no new schema violation). Model names use the
ladder's own spellings (claude-fable-5-1, claude-opus-5, claude-sonnet-5).
`locations: {}` is present on seats.md only because the config type requires
`locations`; the real declaration is `seats`. Known soft spot: `--seat` still
resolves the ladder row keyed to the default tier string (the seat replaces
its spec), so the `roles:` print line reads `tier=0 role=kid` even for a
director seat — cosmetic, the resolved command is correct.
THOUGHT:END

## Agent Notes
built the seat registry (config:seats + dispatch --seat + rotate meter --seat + AGI_SEAT seat-stable pin); all GATE outputs verified: liaison -> sonnet-5/high/no-settings, belam -> fable-5-1/max/ultracode, seats.md has all 8 rows, 1866 passed 1 skipped, no new schema violation.

Parent review (a00-a5800e67, L3.23): ACCEPTED as proved. Independently re-verified: seats.md has all 8 rows (belam, 3 advisors, liaison, dir-g1/g15/g16); dispatch.py --seat liaison dry-prints claude-sonnet-5/effort=high with no --settings; --seat belam dry-prints claude-fable-5-1/max with ultracode --settings; --seat nobody fails open; 137 targeted tests pass. Caveat stands: the roles:/env print still shows tier=0 role=kid for a director seat (cosmetic; resolved command correct) and should be fixed when seats drive real dispatch.
