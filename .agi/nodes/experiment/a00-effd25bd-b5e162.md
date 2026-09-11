---
id: experiment:a00-effd25bd-b5e162
mint_id: b75ce49e996f4dca9a0d469e539611e6
type: experiment
parents:
  - hypothesis:l4-the-reaper-is-one-persistent-service
next_edges: []
confidence: 0.7
edited_by: a00-0fa5cde6
evidence_runs:
  - experiment:a00-effd25bd-b5e162
loop: hypothesis:l4-the-reaper-is-one-persistent-service@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0c1e8b72a6b6ad2a
season: 2
title: A00 effd25bd b5e162
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-effd25bd-b5e162

## Experiment

Bounded to ONE serial-safe slice of `hypothesis:l4-the-reaper-is-one-persistent-service` — the `crons.py` systemd services-applier on a FIXTURE (L4.115 holds dispatch.py/heal.py/workflow.py; crons.py is the free lane; the live install is the prime's step, never a kid's). Delivered the `--unit-dir` seam (same dependency-injection pattern as `--crontab-file`), a `services:` table parsed in `load_crons_node`, `render_unit_file()` (fixed line order → byte-identical re-apply), and `reconcile_units()` in `extensions/agi/bin/crons.py`; six new facade tests in `extensions/agi/tests/test_crons.py`; one optional doc-only field in `.agi/context/schemas/[cron].md` (NOT in `required`, so the pre-existing live node stays legal); and the shipped proposal `extensions/agi/briefs/crons.services.fragment.md` with the exact `write.py cron:crons 'set services {...}'` line for the prime.

What happened (fixture /tmp/crfix, `crons.cmd_apply(root, crontab_file=…, unit_dir=…)`):

1. No `services:` table → `unit_actions: []` and the unit dir stays empty — **byte-for-byte no-op on units**, the live state until the prime lands the table.
2. Table present → unit written `agi-agi-reaper-<hash8>.service`; re-apply → `['unit … up to date']` (byte-identical).
3. `--dry-run` → nothing written, `(dry-run)` actions reported.
4. `crons_live: false` → unit file removed; `systemctl --user disable --now …` intent recorded through the seam, **never executed**.
5. Plain `apply` with no `--unit-dir` → `unit_dir is None`, no unit actions (the grid_sync self-reapply line can never reach units).

Rendered unit (fixture, `project_hash b75c8ded`): `Type=simple`, `ExecStart=/eng/…/heal.py watch --root /proj --poll-s 30`, `WorkingDirectory`, `Restart=on-failure`, `Environment=NOTIFY=off`, `StandardOutput/Error=append:<logs>/agi-crons-proj-….log`, `WantedBy=default.target`. Hard rules held: no credential path ever enters `Environment=` (renderer takes plain k=v only); `systemctl` is never invoked by any test.

## Evidence

- 55/55 `test_crons.py` (49 pre-existing + 6 new); 438 tests across the adjacent suite named in the assignment all green (test_crons, test_heal, test_dispatch*+variants, test_spawn_budget, test_spawn_gate, test_stall_detect, test_node_writer, test_bin_help_smoke). `links.py schema` clean; help smoke green.
- End-to-end fixture action trace (pasted in handoff): write unit → re-apply `up to date` → dry-run writes nothing → `crons_live:false` removes file + records disable → no-table = `[]`.
- Fragment shipped: `extensions/agi/briefs/crons.services.fragment.md`.

**Residue NAMED (not proved here):** (a) the live `systemctl --user` install/`enable --now`/`daemon-reload` against `~/.config/systemd/user/` — the prime's merge-up step, untested here by design; (b) `heal.py watch` itself and the dispatch `_reaper_phase` → one-pass/loop refactor — serial lanes held by L4.115/others; the unit's `ExecStart` would start nothing until `heal.py watch` exists, which is why the fragment is a proposal, not a landed live table; (c) a real round whose parent outlives its nominal timeout producing a mark + one dm proof — out of scope of the crons lane.

**Verdict on THIS slice:** `inconclusive_lean_proved` — the "systemd unit declared in the graph like the crons, rendered byte-for-byte, kill-switched by `crons_live: false`, never a per-dispatch reaper, fixture-proved" PART of the claim is genuinely proved on a fixture; the live half and the watcher/dispatch halves are the residue the prime and the serial successor carry.

## Agent Notes
One serial-safe slice of the crons lane: implemented crons.py services applier + --unit-dir seam + unit renderer + crons_live:false kill-switch; 6 new fixture tests (438 adjacent green); schema [cron].md gains one doc-only optional 'services' field; shipped crons.services.fragment.md for the prime. Live systemd install, heal.py watch, and dispatch reaper refactor remain as named residue (serial/prime lanes).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-0fa5cde6 (L4.116), rewriting this block from scratch. (1) THE INSTRUCTION SAID, addendum at dispatch: "crons.py apply with NO services table is a byte-for-byte no-op on units (the live state until the prime lands the table) -- prove it", "crons_live: false removes the unit file and runs systemctl --user disable --now ... on the fixture, the disable call is recorded through the seam, never run against the real user manager", "the round NEVER edits the live crons.md ... SHIPS the proposed live table as extensions/agi/briefs/crons.services.fragment.md". (2) WHAT THE MACHINE DOES, verified by the parent running the kid's own tests in this checkout: pytest extensions/agi/tests/test_crons.py -q -> 55 passed; the diff adds load_crons_node services parsing, unit_filename/render_unit_file/reconcile_units, cmd_apply(unit_dir=None) where `if unit_dir is None: return []` is the first line of reconcile_units (so the grid_sync self-reapply can never reach a unit), the `crons_live: false` branch unlinks the file and only RECORDS a "systemctl --user disable --now (recorded, not run)" string, and crons.services.fragment.md is present as a proposal with the exact write.py line. The schemas/[cron].md diff adds `services` to `fields` only - it is NOT in `validation.required` (diff line: "required: [crons_live, cadences]` unchanged"), so the live node stays legal; links.py schema is clean on this change. (3) THE NEAR MISS: "ship the table as a fragment" satisfies the words and loses the mechanism if the fragment's exec_start were landed before the watcher exists - the unit would be installed and start nothing. The fragment names heal.py watch and the kid states the ordering ("watcher first, table second"), which is why this is a proposal and not a landed edit; the prime must land it AFTER the heal.py watch fix, and kid 2's node is where that fix is owed. Also cosmetic: the fragment text contains "systemctl --user enable --now mow --now + daemon-reload" (stray "mow") in a prose paragraph - not in the command block a human copies, so it is a typo, not a defect in the applier. (4) JUDGEMENT: accepted unchanged at inconclusive_lean_proved:70 - the kid answered the crons lane honestly, named its residue (live install, watcher, live-round dm) instead of claiming it, and did not touch the live crons.md. Its verdict stands because its slice is genuinely fixture-proved and its unproved half is explicitly named.
<!-- THOUGHT:END -->

PARENT REVIEW (L4.116, a00-0fa5cde6): ACCEPTED as-is, verdict kept at inconclusive_lean_proved:70. Parent re-ran test_crons.py -> 55 passed and read the diff: services table parsed defensively, reconcile_units no-ops when unit_dir is None (so plain/grid_sync apply can never touch units), crons_live:false unlinks the unit and only records the disable intent, schema field is optional and not in required so the live node stays legal, fragment shipped with the exact prime write.py line. No live crons.md edit, no systemctl call from a test. Residue it declares (live install, heal.py watch, live-round dm) is exactly the residue that remains; the ordering it declares - watcher first, table second - is binding on the prime.
