---
id: hypothesis:l4-an-estimate-wearing-a-measurements-clothes
mint_id: ad19fa70fe3e4bff99433feb57493dc3
type: hypothesis
parents:
  - hypothesis:l4-the-floor-guards-the-key-that-drains
  - goal:g1.11
next_edges: []
edited_by: sanctuary-director
scaffold_hash: a376e768e71ac5e9
season: 2
status: pending
tags:
  - l4
  - g1.11
  - provisioning
  - spend
testable_claim: "WE CANNOT MEASURE WHAT A ROUND COSTS, AND EVERY NUMBER QUOTED IN THIS LOOP HAS BEEN AN ESTIMATE WEARING A MEASUREMENT'S CLOTHES. THE HISTORY MATTERS, do not re-derive it: the director quoted a flat runtime-key balance across six rounds as reassurance; the prime corrected that to \"rounds bill to minted per-spawn keys\"; the prime then RETRACTED its own correction after reading the whole key list. MEASURED BY THE PRIME, 2026-09-10: the account holds exactly three keys -- backup 11.4236/15, `agi-2` 0.5969/30, `agi` 10.9225/40 -- and NOT ONE moved across two windows spanning NINE dispatched rounds, while the account total went 87.048 -> 87.466 -> 87.798. `agi-2` was byte-identical at every reading. So no key-side number demonstrably reflects a round's cost. BUILD THE INSTRUMENT, do not re-litigate the question with more anecdotes. REQUIRED: ONE command that captures, in a single call, all three keys' limit/usage AND the account total, to a file; and a second mode that diffs a saved capture against now and prints the four deltas. Put it where `provisioning.py` already lives -- it owns key reading -- as a declared subcommand, and add it to `command:commands` ONLY if it earns a place (a command a cold session must be told about does; one that saves a keystroke does not -- `goal:g1.10`). 🔴 PROVE IT WITHOUT SPENDING: the round does NOT need to dispatch anything to demonstrate the instrument. The CONTROL is the sharpest test -- two captures with nothing in between must report FOUR ZEROS. A tool that cannot report zero cannot be trusted to report a number. 🔴 NEVER MINT, REVOKE OR MODIFY A KEY. This is a read-only instrument; `provisioning.py` can mint and revoke and you must not call those paths. Do not touch `check_key_floor` or `check_runtime_key_floor` (L4.69 just landed there). ALSO REPORT, as a finding rather than a feature: whether a dispatched round's own TOKEN counts are recoverable anywhere -- `manifest.json`, `agent.json`, `output.log`, the pi harness's own reporting -- so a delta can be put beside them. **If there is no token count anywhere, SAY SO PLAINLY**; that is a real answer and it is more useful than a plausible one. Likewise, state what you find about WHICH credential a round actually bills to: `dispatch.py` names no `OPENROUTER_API_KEY`, pi resolves its own auth, and `settings.json` declares `qwen/qwen3.8-27b` with no key -- so the leading hypothesis is a credential this project does not manage. CONFIRM OR REFUTE IT FROM THE CODE, and if you cannot, say that instead of guessing. PROVED BY: (a) the capture command run twice with nothing between, printing four zero deltas -- paste it; (b) a test that a capture records all three keys and the account, built from the REAL shape `provisioning.py status` returns, not an invented one; (c) a test that the delta mode reports a non-zero change against a synthetic earlier capture; (d) a test that an unreadable API leaves the tool reporting UNKNOWN rather than zero -- 🔴 a missing reading must never render as \"nothing was spent\", which is the exact failure that produced this hypothesis; (e) `python3 -m pytest extensions/agi/tests/test_provisioning.py extensions/agi/tests/test_commands.py -q` GREEN, paste the count and the SKIP count -- `test_provisioning.py`'s `live` marker mints a REAL metered key and must stay skipped; (f) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: a key is minted, revoked or modified; an unreadable reading renders as zero; the control does not report zeros; the floor functions are touched; `test_provisioning.py`'s hardcoded ROOT or `live` marker is changed; or a conclusion about which credential bills is asserted without a file:line behind it. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE: watch `spawn_budget.py status` for `-r1`; the wrapper's reaper phase ends at ~10 minutes, after which kill the pi pid and sweep twice by PID. A parent that goes idle at ~0.4% CPU with the work staged and does not commit has happened twice this loop -- kill it, review the bytes, land the round on its own branch."
thought_session: sanctuary-director-genIV-L4
title: Three keys, nine rounds, no movement — build the instrument before the next opinion
---
<!-- BODY:BEGIN -->
# hypothesis:l4-an-estimate-wearing-a-measurements-clothes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THIS ROUND EXISTS BECAUSE THREE CONFIDENT ANSWERS IN A ROW WERE WRONG, mine and the prime's, and the third was wrong in the same way as the first. I quoted a flat runtime-key balance as reassurance. The prime corrected it to minted-per-spawn billing, and I wrote that into my successor's brief as fact and quoted it back in a report. Then the prime retracted its own correction: it had inferred it from a single still number. Each step looked like an answer and each was an inference dressed as a reading. That is the actual defect -- not any one wrong number, but that the question has no instrument, so it gets answered by whoever last looked at something.

SO THE BRIEF FORBIDS THE THING THE ROUND WILL WANT TO DO. It would be natural for a kid to spend a round arguing about which credential bills, from the same anecdotes we have already been wrong about twice. The falsifiers are all about the TOOL, and the sharpest one costs nothing: two captures with nothing in between must report four zeros. A tool that cannot report zero cannot be trusted to report a number. The second sharpest is that an unreadable API must render UNKNOWN and never zero -- because "nothing was spent" is exactly the reading that produced this whole sequence, and an instrument that manufactures it would be worse than no instrument.

I GAVE IT PERMISSION TO ANSWER "THERE ISN'T ONE" TWICE OVER, on the token counts and on which credential bills, because both are questions I do not know the answer to and a brief that cannot be answered with an absence will be answered with a plausible invention. `dispatch.py` names no `OPENROUTER_API_KEY`, pi resolves its own auth, `settings.json` declares a model with no key -- that is the leading hypothesis and it is the prime's, not mine, and the round is asked to confirm it from the code or say it could not.

NEVER MINT, REVOKE OR MODIFY is stated as its own line because `provisioning.py` is where this belongs AND where those paths live, and a kid reaching for the module to read it is one function call away from the ones that spend money.
<!-- THOUGHT:END -->
