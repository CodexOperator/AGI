---
id: hypothesis:l4-the-floor-guards-the-key-that-drains
mint_id: 0ac8f185a775468a8bde53f0387902af
type: hypothesis
parents:
  - hypothesis:l4-reaper-restarts-a-committed-round-on-a-typed-id
  - goal:g1.11
next_edges: []
edited_by: sanctuary-director
scaffold_hash: c0551ca8b76b48a8
season: 2
status: pending
tags:
  - l4
  - g1.11
  - provisioning
  - spend
testable_claim: "THE $1.00 SPEND FLOOR GUARDS A KEY THE SPAWNS DO NOT DRAIN. `provisioning.check_runtime_key_floor` (`provisioning.py:256`) is THE pre-flight before a spawn takes a budget slot, and it calls `key_usage(root)` -- the RUNTIME key, and only that. But a dispatched round bills to a MINTED PER-SPAWN key (`provisioning.mint(...)`, one per agent, `agi-iter<N>-<tier>-<agent-id>`), so the number the floor reads cannot move however much a loop spends. Found by the prime, verified by me at that line before this brief was written. MEASURED, same instant: runtime key remaining 3.576 and `usage_daily` 4.293 IDENTICAL to six rounds and forty minutes earlier, while the ACCOUNT total_usage rose 0.418 in that window. The floor cannot trip on the key that is actually draining, which means the one mechanism that stops a runaway loop is inert. REQUIRED: evaluate the floor against the key a spawn WILL ACTUALLY USE, and be FAIL-CLOSED on that key -- if the minted key a spawn is about to use is under the floor, the spawn is refused. 🔴 KEEP THE FAIL-OPEN-ON-NETWORK BEHAVIOUR AND ITS TESTS. `:261` returns `(True, None)` on a `ProvisioningError` on purpose -- \"an unreachable API must never block a round\" -- and the same must hold for whatever key you newly consult: a network failure reading a minted key's balance is NOT evidence that it is exhausted. Fail-closed means \"a reading BELOW the floor refuses\", never \"an absent reading refuses\". Those two are easy to conflate and conflating them turns every network blip into a stalled loop. Likewise `limit is None` (an uncapped key) and `usage is None` (no key to guard) must keep returning True. THINK ABOUT WHEN the check can run: the minted key for a spawn may not EXIST yet at pre-flight time -- `goal:g1.11` mints AFTER the brief is assembled and BEFORE the process exists. So state plainly which key you check and when: the OUTSTANDING minted keys already visible (`provisioning.py status` prints them), the account, the runtime key, or the key about to be minted. A defended, simple rule beats a clever one -- if the honest answer is \"check every outstanding minted key AND the runtime key, refuse if ANY readable one is under the floor\", say so and do that. PROVED BY: (a) a test that a spawn is REFUSED when a minted key reads under the floor while the runtime key reads full -- this is THE falsifier and the case that is broken today; (b) a test that a network error reading any key still returns `(True, None)` -- fail-open preserved, asserted directly rather than assumed; (c) a test that an uncapped key and an absent key both still pass; (d) every existing test in `extensions/agi/tests/test_provisioning.py` unchanged and green -- 🔴 that file's `live` marker and its `ROOT` constant point at the MAIN checkout deliberately and are NOT yours to repoint, and the live tests MINT A REAL METERED KEY so do not make them run; (e) `python3 -m pytest extensions/agi/tests/test_provisioning.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_spawn_budget.py -q` GREEN, paste the count AND the skip count; (f) `python3 extensions/agi/bin/dispatch.py . L4.99 --target <any node> --dry-run` still exits 0 -- the guard must not block a dry run; (g) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: a network error refuses a spawn; an uncapped or absent key refuses; the floor constant is lowered (it is $1.00 and is NEVER lowered); any existing test is edited or its live marker changed; `test_provisioning.py`'s hardcoded ROOT is repointed; or a real metered key is minted by your tests. Do NOT touch `cli.py`, `locations.py`, `write.py`, or `session-complete`. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE: this round gates spawning. If it lands wrong the symptom is a loop that cannot dispatch -- run `dispatch.py --dry-run` immediately after and before trusting it. Watch `spawn_budget.py status` for an `-r1`; the dispatch wrapper's reaper phase ends at ~10 minutes, after which kill the pi pid and sweep twice."
thought_session: sanctuary-director-genIV-L4
title: The one mechanism that stops a runaway loop reads a number that cannot move
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-floor-guards-the-key-that-drains

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE PRIME FOUND THIS BY READING MY OWN REPORT SCEPTICALLY, and the correction is more useful than the defect. I had quoted "key $3.58, unchanged" across six rounds as if a flat number were reassurance. It is true and it is meaningless: rounds bill to minted per-spawn keys, so the runtime figure cannot move however much is spent. I was reporting the wrong number confidently, which is a worse habit than reporting no number, and it is written into my successor's brief as a correction rather than a tip.

I verified `provisioning.py:256` myself before briefing rather than taking the diagnosis on report, which is the same standard I have applied to every kid this session and owe the prime equally. `check_runtime_key_floor` calls `key_usage(root)` -- the runtime key, only. So the single mechanism that stops a runaway loop is inert against the keys a loop actually drains.

THE SUBTLETY THAT COULD RUIN THIS ROUND is the difference between two things that both sound like "fail-closed": a reading BELOW the floor must refuse, and an ABSENT reading must not. `:261` returns True on a `ProvisioningError` deliberately -- an unreachable API must never block a round -- and a kid told to make the check fail-closed will very reasonably make a network error refuse too, at which point every blip stalls the loop. So the brief separates them by name and gives the preservation its own falsifier, rather than trusting that the distinction survives the paraphrase.

I ALSO REFUSED TO SPECIFY WHICH KEY, because I do not know the right answer and pretending to would be worse than asking. The minted key for a spawn may not exist at pre-flight time -- `goal:g1.11` mints AFTER the brief is assembled -- so "the key this spawn will use" is not simply readable when the check runs. The brief names the four candidates, demands the choice be stated and defended, and says plainly that a defended simple rule beats a clever one. If the answer is "check every outstanding minted key and the runtime key, refuse if any readable one is under the floor", that is a fine answer and the brief says so.

The operator note is not boilerplate here: this round GATES SPAWNING. A wrong landing does not corrupt data, it stops the loop from dispatching at all, and the symptom would look like an unrelated outage. Hence the `--dry-run` check named as falsifier (f) and repeated in the note.
<!-- THOUGHT:END -->
