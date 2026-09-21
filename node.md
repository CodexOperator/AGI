---
id: hypothesis:l4-the-viewport-theme-literal-is-renamed-keep-so-the-ladder-may-declare-the-sanctuary-town-in-the-same-merge-up
mint_id: 9baa5054161d4243a776fd043ba5d2f0
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 9603121557763dfe
season: 2
testable_claim: "goal:g15.25 SM.29 (OWNER ORDER 01:06Z via belam XX, verbatim in doc:l4-owner-decisions L773-775: sanctuary is a town of its own, the original town; Prime 01:09Z: the declaration was reverted @a7de3da13 because test_no_literal_town.py (goal:g8.2 guard) went red — MAIN red 2 min). MEASURED on season2/main @4bd02c74c: the guard (test_no_literal_town.py:67-108) flags any RUNNABLE string literal equal to a non-core ladder town; viewport.py:1052 `choices=(\"graph\", \"sanctuary\")` and :1076 `if args.theme == \"sanctuary\":` are both runnable literals — and :1076 IS a branch on the name, so the guard is right by mechanism and must not be taught an argparse exemption (the exemption would have to cover the branch too, which is exactly what the guard exists to refuse). The theme is a VIEW of the keep (viewport.py:422 hypothesis:l3w4-sanctuary-theme; :564 _render_sanctuary; :580 status line; seat_status.py:14 docstring). No caller in cards, templates, geometry or tests passes --theme sanctuary (grep 01:2xZ). CLAIM: (1) the theme is renamed `keep`: choices (\"graph\",\"keep\"), the branch at :1076 compares to \"keep\", _render_sanctuary -> _render_keep, the :580 status line prints theme=keep, the :422 comment and seat_status.py:14 docstring follow; NO alias keeps the old literal (an alias is the literal again); (2) in the SAME round the kid adds `sanctuary` to ladder.md `towns:` (the ONE declaration site; town_branches follows the existing shape) and the guard stays green on the whole engine (the test is run singly in the round: test_no_literal_town.py + test_viewport.py + test_seat_status.py); (3) the Prime re-mints town:sanctuary + vision:sanctuary + the council-sanctuary row from the local-maxxing create-script shape once this round is on MAIN — the kid ships that script with the names swapped (.agi/sessions/quorum/sanctuary.create.sh), dry-run clean, NOT run (schema written_by owner/prime). FALSIFIERS: any remaining runnable literal \"sanctuary\" in extensions/agi/bin after the round (grep = 0 outside docstrings/comments per the guard AST); the guard red with sanctuary declared; a --theme sanctuary that still resolves. TESTS (<= 3): test_viewport --theme keep renders (rename the existing theme test); guard green with a fixture ladder declaring sanctuary; --theme sanctuary is an argparse error. FILE SCOPE: viewport.py, seat_status.py docstring, ladder.md towns list, the create script, test_viewport.py. CEILING: <= 15 production lines, ONE kid."
title: L4 the viewport theme literal is renamed keep so the ladder may declare the sanctuary town in the same merge up
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-viewport-theme-literal-is-renamed-keep-so-the-ladder-may-declare-the-sanctuary-town-in-the-same-merge-up

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.29 reviewed by name (mur-sl2-33, wf_9cedfafb-a6e, reviewer+refuter agree): ACCEPT with residue. Rename is clean by mechanism (viewport.py:1053 choices graph/keep, :1077 branch, _render_keep :565, seat_status.py:14; zero runnable sanctuary literal in bin/ at f3f618efd), ladder declares sanctuary, guard stays green and reaches the new town. Residue 1: sanctuary.create.sh:12 has no council-sanctuary posts-row step - run before the row exists it mints the town then towns.load_towns raises and set -e aborts before git add; Prime order = ladder on MAIN, write the council-sanctuary row, then run the script. Residue 2: test_viewport.py:474 reaches the real tmux server via rotate._existing_windows (read-only, no dependence) - plumb the window_path seam through _render_keep in a follow-on.
