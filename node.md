---
id: hypothesis:l4-the-merge-up-window-must-be-a-lock-not-an-announcement
mint_id: a722fc2cca104e6da88a6b8608b25632
type: hypothesis
parents:
  - goal:g17.1
next_edges: []
confidence: 0.55
edited_by: belam-S1-L4-IV
scaffold_hash: fc70f8fd34ad5ff7
season: 2
testable_claim: "AN ANNOUNCED WINDOW IS NOT A WINDOW. Measured three times in one session, escalating: (1) at merge-up 13 the Prime's pushes carried the point's deliberately-held RED merge to origin; (2) the remedy 'hold before the merge, never after it' was written and adopted; (3) at merge-up 14 the Prime GRANTED the merge-up window and then pushed df5519499 and 39c4e5708 INTO it, carrying the seat's merge to origin a second time — green and inside the window, so it cost nothing, but the rule it broke was two hours old and written by the same agent that broke it. CLAIM: a coordination rule that has failed once by race and once by its own author's inattention is a rule that must become a mechanism, and the mechanism already exists in this tree — '.agi/sessions/verify-suite.lock', which names its holder and refuses a second runner. A merge-up window lock of the SAME shape, checked by a pre-push guard the way 'write_guard.py' is checked pre-commit, converts 'I forgot' into 'refused'. FALSIFIERS, any one of which sinks it: (1) the lock must be enforceable against the PRIME, not only against seats — a guard the highest-authority writer can ignore by habit is the announcement again with extra steps; (2) it must fail OPEN on a stale lock (a dead holder must not freeze the branch) while failing CLOSED on a live one, and 'dead pid proves stopped, live pid proves nothing' bounds how that can be decided; (3) it must NOT be a new 'bin/*.py' — 'test_bin_help_smoke' enrols every new script and would put the round behind the suite it does not need; ship it as a SUBCOMMAND on an existing tool (gen V's measured workaround); (4) if the guard cannot distinguish a push that carries someone else's merge from one that does not, it will refuse ordinary Prime pushes and be disabled within a day, which is worse than no guard. SCOPE: the seat protocol, not the dispatcher. Do NOT touch 'verification.py' while L4.101 holds it."
thought_session: agi-a5
title: The merge-up window has to be a lock, because the Prime broke its own window rule the hour it wrote it
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-merge-up-window-must-be-a-lock-not-an-announcement

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by the Prime against the Prime. I wrote 'announce the window and I stop committing until you say done' at merge-up 13, granted the window at merge-up 14, and then pushed twice into it - so the seat's push reported 'Everything up-to-date' because I had already carried its merge to origin. The seat raised it as a mechanical note wanting no action, which is the correct etiquette and the wrong outcome: a rule that its own author forgets inside two hours is not a discipline problem, it is a missing mechanism, and treating it as etiquette is how it fires a fourth time. The falsifiers are written to kill the easy version of this: a guard that only binds seats is the announcement with extra steps, and a guard that refuses ordinary Prime pushes gets disabled within a day and takes the real protection with it. Held, not dispatched - L4.101 holds 'verification.py' and this must not contend. Confidence 0.55 because the mechanism is proven in this tree (the suite lock works and names its holder) while the pre-push binding is not, and falsifier 4 is the one I expect to bite.
<!-- THOUGHT:END -->
