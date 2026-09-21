---
id: hypothesis:l4-cmd-spawn-with-a-seat-takes-the-rows-model-effort-and-settings-never-the-tier-default
mint_id: 6401de481164400ebfd5c2aa10cb6ffc
type: hypothesis
parents:
  - goal:g15.15
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 007d31a934962357
season: 2
testable_claim: "goal:g15.15 fix-only — CMD_SPAWN --SEAT TAKES THE ROW'S MODEL, EFFORT AND SETTINGS (Prime XIII 00:33Z, P2 after SL6.01-03; owner order verbatim in doc:l4-owner-decisions: 'No surprise fable please.'; measured by sensei-director gen VI on seat tip 0058b5207). MEASURED: rotate.py cmd_spawn (1485) resolves the seat row at 1561 (_srow = _find_seat(root, seat)) and uses it for role (1562-1563) and generation (1564-1566) only; the spawn itself at 1570-1580 calls spawn_window(model=args.model, effort=args.effort, settings=json.loads(args.settings) if args.settings else None) — the row is IGNORED, so a --seat spawn with no --model gets spawn_window's tier default (1376): the dry-run for the new stream-master row (model claude-sonnet-5) built --model claude-fable-5-1. The three other spawn paths take the row: cmd_seats_launch 2694-2696 (model=row.get('model'), effort=row.get('effort'), settings=settings from the row), cmd_rotate_self 9518-9521 (args.model or row.get('model'), args.effort or row.get('effort'), settings from args else _normalize_settings(row.get('settings'))), heal._recover_seat's respawn 1715-1717 (model/effort/settings = row.get). CLAIM: (1) cmd_spawn, when --seat resolves a registry row, passes model = args.model or row.model, effort = args.effort or row.effort, settings = json.loads(args.settings) if args.settings else _normalize_settings(row.settings) — the rotate-self shape at 9518-9521, reused not copied (one helper, e.g. _row_launch_cells(row, args), called from cmd_spawn and cmd_rotate_self; seats-launch and heal may adopt it only if their behaviour is byte-identical after); an explicit flag still wins; a --seat that resolves NO row (throwaway) keeps today's args-only path. (2) the dry-run line names the model it WOULD launch and its source (flag | row | tier-default) so a wrong model is visible before a window exists. FALSIFIERS: a fixture row with model X and no --model spawns anything but X (dry-run output asserted); --model Y on that row spawns X (the flag must win); a row with effort E and no --effort spawns the tier default; a row with settings spawns without them; a throwaway --seat changes behaviour. TESTS: grep cmd_spawn / spawn_window in extensions/agi/tests (test_rotate_spawn*.py, test_rotate.py) and extend: one fixture row per cell (model, effort, settings), flag-wins, no-row; dry-run only, fake tmux only, never the live registry. Neighbourhood: rotate (test_rotate*.py test_session_start*.py test_after_join_service.py test_bin_help_smoke.py). RULES: merge, never rebase; never lower a guard; do not touch doc:l4-owner-decisions; experiment prose never quotes the literal THOUGHT marker, one THOUGHT region per node. FILE SCOPE: rotate.py cmd_spawn (the spawn_window call + dry-run line) and one shared helper; tests. EXCLUDED: spawn_window's own defaults (1376), cmd_seats_launch, heal.py, the ack/spawn-row/key paths (SL6.01 — this round is dispatched only after SL6.01 lands), send.py, config nodes. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genVI-L6
title: cmd_spawn --seat launches the row's model, effort and settings (a flag still wins), never the tier default — no surprise fable
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-cmd-spawn-with-a-seat-takes-the-rows-model-effort-and-settings-never-the-tier-default

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
