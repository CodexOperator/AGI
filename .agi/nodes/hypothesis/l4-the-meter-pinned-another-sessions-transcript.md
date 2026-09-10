---
id: hypothesis:l4-the-meter-pinned-another-sessions-transcript
mint_id: 8d2888bd1cfb4f65be698cfb7af6fe8f
type: hypothesis
parents:
  - hypothesis:l4-verification-counts-and-engine-root
  - goal:g17.1
next_edges: []
edited_by: sanctuary-director
scaffold_hash: c7dd36e1cc02115f
season: 2
status: pending
tags:
  - l4
  - g17.1
  - rotate
  - meter
  - seat
testable_claim: "A SEAT'S ROTATION METER READ ANOTHER SESSION'S TRANSCRIPT FOR AN ENTIRE SESSION AND NEVER SAID SO. MEASURED, by me, on my own pin: `.agi/sessions/sanctuary-director.meter` contained `/home/ubuntu/.claude/projects/-home-ubuntu-work-agi/e367a3fc-….jsonl` -- **the PRIME's transcript**, 2,092,514 bytes -- while my own was `…/-home-ubuntu-work-agi--agi-worktrees-seat-sanctuary-director/46fcdfbf-….jsonl` at 5,965,855 bytes, in a DIFFERENT project dir. Every meter number I quoted across a full day -- 0.21, 0.27, 0.30, 0.32, 0.34 -- was the prime's, and they tracked its own readings to two decimals because they WERE its readings. Re-pinned with an explicit `--session-log`: **0.7854** against a 0.47 threshold, matching the owner's GUI at 78%. I ran 67% past my rotation line believing I was under it. THE MECHANISM: meter pins are SHARED state routed to the MAIN checkout by `locations.git_common_root`, while a seat's TRANSCRIPT lives in its own worktree's project dir. A bare `--pin` resolves the MAIN project dir and takes the NEWEST `.jsonl` there -- which is almost always the PRIME, because the prime writes constantly. **So the defect is worst exactly when the prime is busiest, and it is FAIL-OPEN, so it never announces itself.** REQUIRED: `rotate.py meter` resolves a seat's transcript from the SEAT's OWN worktree project dir, and REFUSES rather than guesses when the resolved transcript is not the caller's. 🔴 FAIL-CLOSED, because a fail-open meter is a rotation discipline that silently stops existing -- which is what happened here. THE WORKING FIXTURE ALREADY EXISTS: the helper's pin correctly names its own worktree transcript, so worktree-local resolution is right and mine was the broken case; build from both. PROVED BY: (a) a test that a seat whose transcript lives in a worktree project dir resolves ITS OWN, with a prime-sized newer `.jsonl` present in the main project dir as the distractor -- that distractor IS the bug and a fixture without it proves nothing; (b) a test that an unresolvable or ambiguous transcript REFUSES rather than picking the newest; (c) a test that an explicit `--session-log` still wins; (d) the helper's correct pin used as a positive fixture; (e) `python3 -m pytest extensions/agi/tests/test_rotate.py -q` GREEN. DISPROVED IF: it still picks the newest on ambiguity; it fails open; `--session-log` stops winning; or any existing test is edited. 🔴 THE BIGGER SHAPE, the owner's framing adopted by the prime, and it is a SECOND round not this one: tracking your own context is a coin-flip action and needs a MONITOR plus an automated reminder that POPULATES INTO A TURN. This box already runs PreToolUse, PostToolUse and SessionStart hooks, so the plumbing is proven -- and a hook is HANDED its own transcript path, which means it structurally cannot capture another session's, and it can speak unprompted, which a meter command never can. It must ESCALATE rather than ping once (a single reminder is missed mid-round; re-emit at rising thresholds) and must name the exact next command INCLUDING the explicit `--session-log` path, because a reminder that only says \"you should rotate\" costs a turn just to work out how."
thought_session: sanctuary-director-genIV-L4
title: A fail-open meter is a rotation discipline that silently stops existing
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-meter-pinned-another-sessions-transcript

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
I FLAGGED THIS AND MY REMEDY WAS NOT STRONG ENOUGH, which is the part worth inheriting. Early in the session the meter read 0.4159 and then 0.1836 minutes apart; I wrote in my own successor brief that it 'can read a FOREIGN transcript' and that the fix was to re-pin before believing it. The instinct was right. The remedy was wrong: a BARE re-pin is exactly the operation that captures someone else's transcript, so I re-pinned all day and captured the prime every time. **A remedy that reuses the broken mechanism is not a remedy**, and I could not see it because the numbers it produced were plausible -- they moved slowly upward, the way a real meter would.

THE TELL I MISSED, and the one a successor can use: my readings tracked the PRIME's to two decimal places. Two independent sessions doing different work do not agree to two decimals. I never compared, because I had no reason to think I was reading anything but my own.

THE SHAPE IS THE SAME ONE THIS SEAT HAS BEEN CHASING ALL DAY, and that is why it belongs beside the others rather than as a one-off: shared state resolved through `git_common_root` versus per-worktree state resolved locally -- the agent record in three trees, the session dirs stranded in the worktree that ran them, the inbox written to a comms root the recipient never reads, and now the meter pin pointing at the main project dir while the transcript lives in the worktree. Four faces, one boundary. The reconciler fixed the corpus; this one is the same boundary showing its ROTATION-DISCIPLINE face.

AND IT IS FAIL-OPEN, WHICH IS WHY IT SURVIVED A WHOLE DAY. Nothing errored. A wrong number is worse than no number precisely because it does not ask to be checked -- the same disease as the instrument that reported four zero deltas while omitting the only figure that moves, and the command that refused every round with fifteen green tests behind it. The prime's ruling to make it REFUSE rather than guess is the right shape, and it is the third time today that the correct answer was to fail closed.
<!-- THOUGHT:END -->
