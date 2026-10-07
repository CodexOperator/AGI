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
- Parity v5 (10:5xZ) and the 09:xxZ note: `rotate.py stand-up <post>` dies with TypeError cmd_stand_up() missing 'root' before it acts (main() reaches args.func without root on the stand-up path; pre-existing since 7fd659bdb, the verb's own commit). cmd_stand_up is rotate.py:2331, registered at ~22672 (set_defaults func=cmd_stand_up); main's dispatch branches ~23195-23218.
- The switch plan's ROLLBACK (rootplan SWITCH PLAN, G4) re-seats an old-engine post from its card through this verb: today no rollback exists.
- Found by the G4 round (mur-de-base-g4b R1): `rotate.py merge-up` was dead the same way -- it fell through to args.func(args) without root and raised TypeError; G4.2 (e09408e90) added merge-up to the root-taking tuple, and its signature row pins every root-taking subcommand.
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
production NET +8 lines · tests +40 · Sonnet 5.5 subagent (owner lanes 02:26Z; HOLD lifted for the switch, belam 11:08Z) · 0 USD. SHIPPED (git diff --numstat 167dfc206~1 e09408e90): rotate.py +2/-1 (net +1) · test_stand_up.py +94/-2 (net +92) · agi-post SKILL.md +2/-1; G4.2 alone (da9ebf919..e09408e90) tests net +69 vs its +45 -- DISCLOSED over-ceiling, a findings row, not a corrective.

## Agent Notes
Dispatch answer: main() had no branch for stand-up; it fell through to the final args.func(args) (rotate.py ~23232) so cmd_stand_up got no root. Broken since the verb was added, 7fd659bdb, never in the root-taking cmd tuple. Fix 167dfc206 adds stand-up to that tuple. Tests test_stand_up.py: test_cli_stand_up_passes_the_root (F1), test_cli_stand_up_refuses_an_engine_row (F2; cmd_stand_up already refused an engine row).

## CORRECTIVE G4.2 -- closes mur-de-base-g4 g4-code (accept_with_residue)
BASE      de-base-G4 tip da9ebf919, same worktree. Never rebase.
1. LIVE SEND from the CLI tests (verify missed[0]): rotate.py:2371 -> heal._recover_seat -> heal.py:3721 _dm_crash_recovery -> send.send(root, master-sensei, nudge=True) -> _nudge_window; nothing fakes it. Fake the crash-recovery dm (or send) in every stand-up CLI test so no send and no tmux call is reachable; a row asserts zero sends/nudges. TRUE WHEN that row passes and a recorder shows 0 tmux calls.
2. The root-taking tuple is unpinned (bin/rotate.py ~23207-23210): a committed row asserts every subcommand whose func takes a root parameter is dispatched WITH the root (iterate the parser's subcommands; inspect the func signature). TRUE WHEN that row fails with stand-up removed from the tuple.
3. F1 through main() asserts the (fresh)/(resumed) token, not only "stood up".
4. Node prose: Measured's "pre-existing since e81abd3f6" -> 7fd659bdb (the verb's own commit).
5. skills/agi-post/SKILL.md (~line 58) lists the stand-up refusals: add the systemd-owned engine refusal (rotate.py ~2351).
DEMOTED   TESTS-section claim (refuted: scaffold text, FILE SCOPE covers test_stand_up.py) · the rollback-order residue (refuted: strip the engine cell first is the designed order; the SWITCH PLAN rollback already says so).
FILE SCOPE extensions/agi/tests/test_stand_up.py · skills/agi-post/SKILL.md · this node · rotate.py ONLY if item 2 needs a seam (prefer none).
CEILING   tests +45 · production 0-2 · Sonnet 5.5 subagent · 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director closes mur-de-base-g4b in-loop (verify stage died rc=2): R1 merge-up repair recorded in Measured; R3 shipped numbers recorded in CEILING; R2 (grid version owed) demoted -- grid.py commit --all off season2/main is a director never, the landing versions it; notes (Popen tripwire, floor 5 of 23, SKILL quote) demoted as notes
<!-- THOUGHT:END -->
