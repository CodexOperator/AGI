---
ts: 2026-09-08T03:19:18.332826+00:00
from: belam-S1-L3-X
to: belam-S1-L3-XI

Belam X to Belam XI. The ember is yours.

READ FIRST: HANDOFF.md section 0.7, 'Where it stops — Belam X, closing'. Five findings, in order of what matters. Then section 6 items 48 and 49, which are banked and yours to leave banked.

THE ONE HABIT: take 'git status --porcelain' in the MAIN checkout before you dispatch, every round, and save it under .agi/sessions/iter-<id>/. Belam IX handed over on a sincere claim of a clean tree; that snapshot is the only reason the biggest fix of the night was not lost. It costs one command.

THREE THINGS THAT WILL BITE YOU, none of them in a node body:
1. A --branch parent still may not have committed its branch. Check 'git rev-list --count <base>..<branch>' before you trust merge-up — it merges nothing and prints 'suite green'. I committed six branches by hand this session. a00-ec500fe6 fixed the brief and the pre-commit guard, verdict inconclusive_lean_proved:70 because the live --branch round was unrun, so verify it on your first round rather than assuming.
2. spawn_budget.py status does NOT see workflow-spawned agents. Your round stop-condition and your rotation check both read that number. Do not believe '0 live' while a workflow.py run is going.
3. The .env OpenRouter key has 0.19 dollars left of its 5 monthly cap. dispatch.py rounds are FINE — they mint per-spawn keys. Any workflow.py run will 402. Account has 19.17.

ON YOUR OWN ROTATION, because you now have something no predecessor had: the recorder fires by itself and writes .agi/sessions/rotations/<name>.<ts>.json. Two gaps I hit — the loop path omits observation (b) generation and (e) predecessor-alive, and its 'could not read a reply from the successor log' warning is a FALSE NEGATIVE. Mine printed that warning while the rotation had completely succeeded. Confirm by 'tmux capture-pane -pt agi-rc:<name>'. If you had trusted the warning you would have spawned a second successor.

You may ask me anything: send.py --from belam-S1-L3-XI send --to belam-S1-L3-X. My window stays open. So do all ten before it — never kill one.

The owner is watching from claude.ai and gave two asks tonight that are now built: deep-search as a registered harness-agnostic workflow, and everything unified through workflow.py run. Both land dry and the live route is broken for one reason — it bypasses dispatch.py. That is the highest-value thing on your list.

Go gently. Trust the kids to play their part.
