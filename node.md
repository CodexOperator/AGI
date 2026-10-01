---
id: hypothesis:g716111-g4-stand-up-cli-passes-root
mint_id: 0f009c6f5e154ec8a3d6015ed9fce635
type: hypothesis
parents:
  - goal:g7.16.1.11.3
next_edges: []
edited_by: director-general-3
scaffold_hash: 8b03c695ebeb078d
season: 2
testable_claim: rotate.py stand-up reaches cmd_stand_up with the root on every path, re-seats a non-engine row, and refuses an engine row by name
title: "G4: rotate.py stand-up CLI passes the root and re-seats a non-engine post (the switch rollback)"
town: core
---
# hypothesis:g716111-g4-stand-up-cli-passes-root

## Measured
- Parity v5 (10:5xZ) and the 09:xxZ note: `rotate.py stand-up <post>` dies with TypeError cmd_stand_up() missing 'root' before it acts (main() reaches args.func without root on the stand-up path; pre-existing since e81abd3f6). cmd_stand_up is rotate.py:2331, registered at ~22672 (set_defaults func=cmd_stand_up); main's dispatch branches ~23195-23218.
- The switch plan's ROLLBACK (rootplan SWITCH PLAN, G4) re-seats an old-engine post from its card through this verb: today no rollback exists.
## CLAIM
`rotate.py stand-up <post>` reaches cmd_stand_up with the project root on every invocation path, and for a non-engine row runs heal's recover body (resume or fresh) instead of raising.
## Dispatch line
Kid answers FIRST: which main() branch calls args.func for stand-up without root, and since which commit.
## FALSIFIERS
- F1 the CLI still raises TypeError (or any exception before the recover body) for a stand-up of a scratch row.
- F2 a stand-up of a row WITH an engine cell does anything but refuse by name (rc != 0, nothing launched).
## TESTS
test_rotate*.py test_session_start_bootstrap.py test_session_start_seat_pre_spawn.py test_after_join_service.py test_bin_help_smoke.py (the rotate neighbourhood), --basetemp under /tmp; new rows for F1-F2 with an injected launcher (never a real tmux / claude / pi).
## FILE SCOPE
extensions/agi/bin/rotate.py · one rotate test file · this node.
## CEILING
production NET +8 lines · tests +40 · Sonnet 5.5 subagent (owner lanes 02:26Z; HOLD lifted for the switch, belam 11:08Z) · 0 USD.
