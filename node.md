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
testable_claim: "A SEAT'S ROTATION METER READ ANOTHER SESSION'S TRANSCRIPT FOR AN ENTIRE SESSION AND NEVER SAID SO. MEASURED, by me, on my own pin: `.agi/sessions/sanctuary-director.meter` contained `/home/ubuntu/.claude/projects/-home-ubuntu-work-agi/e367a3fc-….jsonl` -- **the PRIME's transcript**, 2,092,514 bytes -- while my own was `…/-home-ubuntu-work-agi--agi-worktrees-seat-sanctuary-director/46fcdfbf-….jsonl` at 5,965,855 bytes, in a DIFFERENT project dir. Every meter number I quoted across a full day -- 0.21, 0.27, 0.30, 0.32, 0.34 -- was the prime's, and they tracked its own readings to two decimals because they WERE its readings. Re-pinned with an explicit `--session-log`: **0.7854** against a 0.47 threshold, matching the owner's GUI at 78%. I ran 67% past my rotation line believing I was under it. THE MECHANISM -- CORRECTED 2026-09-10 by gen V, sandbox-proved, and it is NOT what this node first said. It is not the newest `.jsonl`; rule 4 (slug dir) NEVER RUNS while any pin exists, and 24 pins exist. A bare `--pin` resolves at rule 3 (`rotate.py:359`): `find_pin_log(root, seat=None)` returns the NEWEST `.meter` PIN **across every agent** in the shared sessions dir -- which `_sessions_dir` routes to the MAIN checkout -- so the caller reads ANOTHER AGENT'S PIN, and `cmd_meter:906` then writes that foreign transcript path into the caller's own pin file and RE-STAMPS IT WITH THE CALLER'S CURRENT GENERATION, destroying `seat_pin-stale`, the one guard built to catch precisely this. CONFIRMED BY ARTEFACT: `.agi/sessions/belam.meter` -- the prime's pin -- names `…/-home-ubuntu-work-agi/e367a3fc-87da-48b3-8175-4ecc9da1227e.jsonl`, byte-identical to the path found in this seat's pin. The foreign PIN, not a foreign jsonl, is how it arrived. **The defect is worst exactly when another agent re-pins most recently -- normally the prime, because it writes constantly -- and it is FAIL-OPEN, so it never announces itself.** 🔴 WHY THE CORRECTION CHANGES THE FIX AND NOT JUST THE STORY: the fix this node originally prescribed -- resolve from the seat's own worktree project dir -- targets RULE 4, the branch that never executes in production. It would have gone GREEN on tests and changed NOTHING live: the same disease as a mitigation that hides the symptom while the cause stands. REQUIRED, restated against the real mechanism: a bare `--pin` must never adopt a pin it did not write. `rotate.py meter` REFUSES rather than guesses when it cannot establish that the resolved transcript belongs to the caller. 🔴 FAIL-CLOSED, because a fail-open meter is a rotation discipline that silently stops existing -- which is what happened here. THE WORKING FIXTURE ALREADY EXISTS: the helper's pin correctly names its own worktree transcript, so worktree-local resolution is right and mine was the broken case; build from both. PROVED BY: (a) a test that a seat whose transcript lives in a worktree project dir resolves ITS OWN, with a prime-sized newer `.jsonl` present in the main project dir as the distractor -- that distractor IS the bug and a fixture without it proves nothing; (b) a test that an unresolvable or ambiguous transcript REFUSES rather than picking the newest; (c) a test that an explicit `--session-log` still wins; (d) the helper's correct pin used as a positive fixture; (e) `python3 -m pytest extensions/agi/tests/test_rotate.py -q` GREEN. DISPROVED IF: it still picks the newest on ambiguity; it fails open; `--session-log` stops winning; or any existing test is edited. 🔴 THE BIGGER SHAPE, the owner's framing adopted by the prime, and it is a SECOND round not this one: tracking your own context is a coin-flip action and needs a MONITOR plus an automated reminder that POPULATES INTO A TURN. This box already runs PreToolUse, PostToolUse and SessionStart hooks, so the plumbing is proven -- and a hook is HANDED its own transcript path, which means it structurally cannot capture another session's, and it can speak unprompted, which a meter command never can. It must ESCALATE rather than ping once (a single reminder is missed mid-round; re-emit at rising thresholds) and must name the exact next command INCLUDING the explicit `--session-log` path, because a reminder that only says \"you should rotate\" costs a turn just to work out how."
thought_session: sanctuary-director-genIV-L4
title: A fail-open meter is a rotation discipline that silently stops existing
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-meter-pinned-another-sessions-transcript

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE MECHANISM IN THE PREVIOUS VERSION OF THIS CLAIM WAS WRONG, AND WRONG IN THE DIRECTION THAT COSTS A ROUND. It said a bare `--pin` takes the newest `.jsonl` in the main project dir. It does not. `resolve_transcript` reaches rule 3 first and `find_pin_log(root, seat=None)` returns the newest `.meter` PIN across every agent in a shared dir; rule 4, the slug-dir heuristic the old text described, is unreachable while any pin exists -- and there are 24. So the fix the node asked for pointed at dead code.

I PROVED IT RATHER THAN REASONED IT, in a sandbox built from the real shape: two pins in one sessions dir, the foreign one written last, my own pin naming my own transcript and CORRECT. `resolve_transcript(seat=None)` returned the foreign transcript. That is the path a bare `--pin` then writes into the caller's pin file.

THE ARTEFACT AGREES AND IS STILL ON DISK. `belam.meter` names `e367a3fc-…jsonl` -- exactly the transcript my predecessor found in `sanctuary-director.meter`. Both accounts name the same file; only mine explains how it got there, and it is checkable by anyone in one `cat`.

THE PART THAT GENERALISES, and the reason this is worth a node edit rather than a footnote: **my predecessor's remedy failed because it reused the broken mechanism, and the FIX IT PRESCRIBED would have failed the same way for the same reason.** The old THOUGHT block already contains the sentence 'a remedy that reuses the broken mechanism is not a remedy' -- correctly, about re-pinning -- and then the REQUIRED clause fifteen lines above it prescribes a repair aimed at the wrong branch. Seeing the principle did not protect the prescription, because the prescription was written against an unverified mechanism. Root-cause to file:line BEFORE stating the required fix, not after.

AND THE RE-STAMP IS THE SHARPEST HALF. `cmd_meter:906` writes the caller's CURRENT generation onto whatever path it just resolved. `seat_pin-stale` -- the guard added by hypothesis:l3-seat-pin-not-repointed-on-rotation, which exists to catch a pin belonging to someone else -- is therefore SILENCED by the very command an operator runs to fix a suspect pin. A guard that the standard remedy disarms is worse than no guard: it certifies the state it failed to check.
<!-- THOUGHT:END -->

## Agent Notes
ROTATION POSTSCRIPT, gen IV -> gen V, recorded because it vindicates an inherited rule by failing exactly where that rule says not to look. `rotate.py rotate-self` exited 0 having run steps 1-3 of 5 and then STOPPED on purpose: *"warn: successor did not answer the single word `continue`; leaving the renamed window in place for inspection."* Step 4 is the read-back and step 5 is killing the old window; neither ran.

**THE SUCCESSOR WAS ALIVE THE WHOLE TIME.** I confirmed it two ways before the warning existed -- `tmux capture-pane` on `@241` showing a live prompt, and the `ListAgents` join giving `seat-sanctuary-director-11 [3d6888] · agi-rc:@241` against tmux `@241 sanctuary-director`. It has since committed its own work (`db9209f75`) and dispatched a round. **So the read-back is not evidence in either direction, and the brief this seat inherited already said so:** *"Confirm your successor by `tmux capture-pane`, not the read-back."* That rule was written by a predecessor, carried forward untested, and has now been earned -- a rotation that reports failure at step 4 may have fully succeeded at step 3.

CONSEQUENCE, and it needs a human or a successor to act: **step 5 never runs on this path, so the old window survives as `sanctuary-director.gen5` (@238) and needs an EXTERNAL kill.** There are now TWO such orphans -- `@237 sanctuary-helper.gen2` from the helper's rotation, which was killed mid-flight by the harness memory reaper at step 3, and `@238` from mine, which stopped at step 4 by design. **Different causes, identical residue.** A rotation that ends anywhere before step 5 leaves a window nobody owns, and nothing sweeps them.

THAT IS A ROUND FOR SOMEONE: the two failure paths already differ (`hazard 5` fixed the interrupted-rotation record so a rotation says which step it reached -- and it did, cleanly, which is why this postscript could be written at all). What is missing is the cleanup: an orphaned `<seat>.genN` window is a mechanically detectable state, and the seat that owns the name is the one that should reap it. Not shaped here; named, with two live instances to build a fixture from.
