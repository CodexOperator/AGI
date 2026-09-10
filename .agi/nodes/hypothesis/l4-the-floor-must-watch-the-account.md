---
id: hypothesis:l4-the-floor-must-watch-the-account
mint_id: f0e6922f863846c29c57f313bd8821d5
type: hypothesis
parents:
  - hypothesis:l4-an-estimate-wearing-a-measurements-clothes
  - goal:g1.11
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 3fc0e2dfae97689f
season: 2
status: pending
tags:
  - l4
  - g1.11
  - provisioning
  - spend
testable_claim: "THE SPEND PRE-FLIGHT MUST CONSULT THE ACCOUNT, BECAUSE THE ACCOUNT IS THE ONLY NUMBER THAT MOVES. MEASURED, do NOT re-derive it: I captured before dispatching one round, ran it to completion (parent + one kid, committed and exited cleanly), and diffed -- `account.used` $87.9269 -> $88.0246, delta **$+0.0977**, while ALL THREE keys and the runtime key moved **$0.0000 exactly**. One dispatched round costs about ten cents and bills to the ACCOUNT and to no key this project manages; `dispatch.py` names no `OPENROUTER_API_KEY` and pi resolves its own auth, so the code and the measurement agree. CONSEQUENCE, and it is why this round exists: `check_key_floor` was widened in L4.69 from the runtime key to every outstanding engine-minted key -- a CORRECT fix to a REAL defect, and it still cannot see one cent of a round. **The guard is not weak, it is looking somewhere else.** REQUIRED, and this is the prime's spec, not mine to redesign: a configured `provisioning.min_account_remaining_usd`, checked in the same pre-flight, **ADDITIVE to the key floor and never replacing it**. FAIL-CLOSED when the account reading is PRESENT and BELOW the floor; FAIL-OPEN on a network error or an unreadable reading. 🔴 THOSE ARE TWO DIFFERENT THINGS AND CONFLATING THEM STALLS THE LOOP ON EVERY BLIP -- 'a reading below the floor refuses' is not 'an absent reading refuses'. `check_key_floor`'s existing shape already gets this right; match it rather than inventing a second idiom, and reuse `min_key_remaining_floor`'s config-reading pattern so there is one way to declare a floor, not two. 🔴 THE $1.00 KEY FLOOR IS NEVER LOWERED and this round does not touch it. QUOTE THE RUNWAY IN YOUR NODE so the owner can pick the number against a real rate rather than a feeling: at the measured $0.0977 per round and $3.98 remaining on the account ($88.02 used of $92 at the time of writing), that is **roughly 40 rounds of runway**. State that arithmetic explicitly and note that the DEFAULT is the owner's to set -- propose one, defend it, and say plainly that it is a proposal. PROVED BY: (a) a test that a spawn is REFUSED when the account remaining reads below the floor while every key reads full -- THE falsifier, and the case that is unguarded today; (b) a test that a network error or an unreadable account reading still returns `(True, None)` -- fail-open, asserted directly rather than assumed; (c) a test that the KEY floor still refuses exactly what it refuses today, unchanged -- additive, not replacing; (d) a test that an absent `min_account_remaining_usd` config leaves behaviour identical to today, so a project that has not declared one is not suddenly gated; (e) `python3 -m pytest extensions/agi/tests/test_provisioning.py extensions/agi/tests/test_dispatch.py -q` GREEN, paste the count AND the skip count -- `test_provisioning.py`'s `live` marker MINTS A REAL METERED KEY and must stay skipped; (f) `python3 extensions/agi/bin/dispatch.py . L4.99 --target <any node> --dry-run` exits 0 -- the guard must not block a dry run; (g) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: a network error or absent reading refuses; the key floor's behaviour changes; the $1.00 constant is lowered; a second config idiom for declaring a floor is introduced; an existing test is edited (🔴 and if one MUST be, the replacement asserts the SPECIFIC fact the old one obscured IN ADDITION to whatever it counted -- never merely relaxes the constraint; that is the prime's standing standard as of today); or a real metered key is minted. Do NOT touch `capture`/`diff` (L4.74, the instrument that produced this measurement), `cli.py`, or the parent brief. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE: this round gates spawning -- run `dispatch.py --dry-run` immediately after and before trusting it. Watch `spawn_budget.py status` for `-r1`; the wrapper's reaper phase ends at ~10 minutes, after which kill the pi pid and sweep twice by PID. A parent that goes idle at ~0.4% CPU with the work staged and does not commit has happened twice this loop -- kill it, review the bytes, land the round on its own branch."
thought_session: sanctuary-director-genIV-L4
title: Ten cents a round, none of it on a key any guard can read
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-floor-must-watch-the-account

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE PRIME'S SPEC, AND I AM NOT REDESIGNING IT. It ruled the shape -- a configured `min_account_remaining_usd`, additive to the key floor, fail-closed on a present reading below and fail-open on a network error -- and the brief carries that verbatim rather than my improvement of it. What is mine is the measurement underneath: I built the instrument, captured before a round, ran it, and read $+0.0977 on `account.used` against $0.0000 on every key. Without that number this round would be another opinion about spend, and this loop has had three of those, two of them mine.

THE UNCOMFORTABLE PART IS THAT L4.69 WAS RIGHT AND IS STILL BLIND. It widened the floor from the runtime key to every outstanding minted key, fixed a real defect, kept fail-open properly, and cannot see one cent of what a round costs. I want that stated in the node rather than quietly superseded, because the tempting story is that the earlier round was wrong. It was not. It fixed what it could see. The instrument is what changed what could be seen.

I SPENT THE BRIEF'S SHARPEST WORDS ON THE FAIL-OPEN DISTINCTION AGAIN, for the second round running, because it is the one thing here that turns a guard into an outage: 'a reading below the floor refuses' and 'an absent reading refuses' sound alike and only one is safe. `check_key_floor` already gets it right, so the instruction is to MATCH it rather than to be careful -- copying a working idiom is more reliable than restating its principle.

THE RUNWAY IS IN THE CLAIM ON PURPOSE. $0.0977 a round, $3.98 left, about forty rounds. A floor chosen against that arithmetic is a decision; one chosen against a feeling is a number someone will quietly lower later. The default is the owner's, the round proposes and defends one, and the brief says out loud that it is a proposal -- which is the difference between offering a judgement and taking one.
<!-- THOUGHT:END -->
