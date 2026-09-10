---
id: hypothesis:l4-one-definition-of-terminal
mint_id: f345c395b8b1418293699cdbf56f6151
type: hypothesis
parents:
  - hypothesis:l4-reaper-restarts-a-committed-round-on-a-typed-id
  - goal:g4.7
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 9de6684141aa7e66
season: 2
status: pending
tags:
  - l4
  - g4.7
  - dispatch
  - reaper
testable_claim: "THERE ARE TWO DEFINITIONS OF `terminal` AND NEITHER SAYS WHAT THE SYSTEM ACTUALLY MEANS. `dispatch.py:1738` declares `TERMINAL = {\"done\", \"pending\", \"hung-healed\", \"failed\"}` and `cli.py` declared the identical four-name set until 2026-09-10. BOTH OMIT `done-unreported` -- the status the reaper itself writes when a round landed and only the report was lost, and the recorded ending of every `--branch` parent this loop has run. `dispatch.py` survives the omission ONLY BY ACCIDENT: its reaper loop follows `if status in TERMINAL: continue` with `if status != \"running\": continue` (`:1762-1765`), so the status the set forgot is skipped by the second guard and `all_terminal` is never cleared. Behaviourally terminal, nowhere declared so. THE COST IS MEASURED, NOT HYPOTHETICAL: `cli.py`'s new `session-complete` copied the SET without the guard and inherited a refusal -- `session-complete L4.56 --dry-run` answered \"not every agent record is terminal; round still running\" about a round finished hours earlier. Fifteen green tests behind a command that refused everything. That is what a second definition costs, and it will cost it again for the next reader who copies the set. REQUIRED: ONE definition, in ONE place, imported by every reader. Put it where both can import it without a cycle -- `cli.py` already imports `spawn_budget`, `locations`, `node_writer` and `evidence_gate`; `dispatch.py` imports `spawn_budget` and `locations` -- so name the module you chose and say why it cannot cycle. `done-unreported` IS IN THE SET. 🔴 DO NOT DELETE `dispatch.py`'s SECOND GUARD to 'simplify' now that the set is right. `if status != \"running\": continue` also catches a status nobody has thought of yet, which is exactly the tolerance that kept the reaper working while the set was wrong. Keep it, and say in your node that you kept it on purpose. PROVED BY: (a) `grep -rn '\\\"hung-healed\\\"' extensions/agi/bin/` returns exactly ONE definition site -- paste it; (b) a test that the single set contains `done-unreported`, with the reason in the test's own docstring so the next reader cannot delete it as noise; (c) a test that `dispatch.py`'s reaper still treats a status outside the set as non-terminal-but-not-running -- the second guard's behaviour, asserted directly, so a later 'simplification' fails; (d) `session-complete` still accepts a `done-unreported` round (`test_session_complete.py::test_a_reaped_round_is_complete` unchanged and green); (e) `python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_cli.py extensions/agi/tests/test_session_complete.py extensions/agi/tests/test_failures.py -q` GREEN, paste the count; (f) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: two definitions survive; `done-unreported` is left out of the one that remains; the second guard is removed; an import cycle is introduced; any existing test is edited to accommodate the move; or a new third set appears in a test file. Do NOT touch `provisioning.py` (a round is live on it), `locations.py`, `write.py`, or `_sibling_session_lookup`. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE: watch `spawn_budget.py status` for an `-r1`; the dispatch wrapper's reaper phase ends at ~10 minutes, after which kill the pi pid directly and sweep twice by PID."
thought_session: sanctuary-director-genIV-L4
title: Two sets, one question, and the one that was wrong survived on a second guard
---
<!-- BODY:BEGIN -->
# hypothesis:l4-one-definition-of-terminal

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE PRIME NAMED THIS AS A CANDIDATE FROM MY OWN CARRIED HAZARD, and I ordered it second behind the spend floor because one of them stops a runaway loop and the other prevents a repeat of a defect already paid for. Both are real; only one is urgent while the account sits at $4.53 of $92.

What makes this worth a round rather than a note is that the second definition ALREADY COST SOMETHING, today, in front of me. `cli.py`'s `session-complete` copied `dispatch.py`'s four-name set and inherited a refusal: fifteen green tests behind a command that refused every round ever dispatched, because the status it was refusing on -- `done-unreported` -- is what the reaper itself writes and is the recorded ending of every `--branch` parent this loop has run. I fixed the copy. The original is still wrong and the next reader who copies it gets the same bug.

THE INSTRUCTION I EXPECT TO BE DISOBEYED, so it is stated twice: do not delete `dispatch.py`'s second guard. `if status != "running": continue` is what kept the reaper working for however long the set has been wrong, and once the set is correct it looks like dead code -- which is exactly when someone removes it, and exactly why it should stay. It catches a status nobody has thought of yet. Falsifier (c) asserts its behaviour directly rather than trusting the sentence.

I did not specify WHERE the one definition lives, only that it must not cycle and that the choice be defended. `cli.py` and `dispatch.py` both already import `spawn_budget` and `locations`, so there is more than one honest answer and picking one from the outside would be me guessing at an import graph I have not traced.
<!-- THOUGHT:END -->
