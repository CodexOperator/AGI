---
id: hypothesis:l4-a-meter-you-must-remember-to-read-is-a-coin-flip
mint_id: 5bf118a21b484586a89e824d41b858df
type: hypothesis
parents:
  - hypothesis:l4-the-meter-pinned-another-sessions-transcript
  - goal:g17.1
next_edges: []
edited_by: belam
scaffold_hash: cfc753c4e0356011
season: 2
status: inconclusive_lean_proved:85
tags:
  - l4
  - g17.1
  - rotate
  - meter
  - hook
  - fail-closed
testable_claim: "TRACKING YOUR OWN CONTEXT IS A COIN-FLIP ACTION AND MUST STOP BEING ONE. The owner's round, adopted whole by the prime: a meter you have to REMEMBER to read is a rotation discipline that depends on the one faculty a session loses as it fills up. Two seat generations in a row proved it -- gen IV ran 67% past its rotation line believing it was under it, and gen III closed at 0.56 and wrote a worse brief for it. REQUIRED: a HOOK that speaks UNPROMPTED, populating a rotation warning into the session's own turn. 🔴 A HOOK IS HANDED ITS OWN TRANSCRIPT PATH, AND THAT IS THE ENTIRE ARCHITECTURAL POINT -- it makes the capture bug STRUCTURALLY IMPOSSIBLE rather than guarded. Claude Code delivers a JSON payload on stdin carrying the session's own transcript path and session id. **USE THE HANDED PATH AND NOTHING ELSE.** The hook must NEVER call `resolve_transcript`, NEVER read a `.meter` pin, NEVER glob a project dir, and NEVER take the newest anything -- every one of those is the defect the parallel round (`hypothesis:l4-the-meter-adopts-a-pin-it-did-not-write`) is closing, and re-importing it here would reintroduce it in a new file. 🔴 VERIFY THE PAYLOAD'S FIELD NAMES EMPIRICALLY, DO NOT ASSUME THEM: `extensions/agi/hooks/cc-session-start.sh` already consumes a real hook payload on this box -- read it, and capture an actual payload if you can. Assert the field you rely on EXISTS and FAIL CLOSED with a named error if it does not. 🔴 IT ESCALATES; IT DOES NOT PING ONCE. A single reminder is missed mid-round -- that is measured behaviour, not a worry. Emit on rising THRESHOLD BANDS, at most once per band while BELOW the rotation threshold (silence when nothing changed is the point), and on EVERY firing once AT OR ABOVE it, because past the line the emergency does not expire. Per-session state, keyed by the SESSION ID from the payload -- 🔴 NEVER keyed by seat name and NEVER in a dir shared across agents; shared state routed to the main checkout is the exact boundary that produced the bug this round exists to prevent. 🔴 IT NAMES THE EXACT NEXT COMMAND, INCLUDING THE EXPLICIT `--session-log` PATH, interpolated from the handed transcript path -- a copy-pasteable line. A reminder that only says 'you should rotate' costs a turn just to work out how, and that turn is spent at the exact moment context is scarcest. 🔴 THE DENOMINATOR IS AN OPEN QUESTION: MEASURE IT, DO NOT ASSUME IT. `rotate.py:72` falls back to `DEFAULT_DIRECTOR_CONTEXT_TOKENS = 1_000_000` and `.agi/nodes/.geometry/ladder.md:14` declares `director_context_tokens: 1000000`. THE EVIDENCE FOR 1M IS ONE CROSS-CHECK, NOT A PROOF: gen IV's explicit read of 0.7854 against a 1M denominator matched the owner's GUI at 78% for an Opus 5 session. One agreement, one model. Say in your node WHAT YOU MEASURED and what the numerator actually sums (input, cache-read and cache-creation tokens are not the same quantity and the choice changes the fraction). If the window cannot be established for the running model, FAIL CLOSED and say so -- do not quietly assume 1M, because a confident wrong fraction is the disease, not the cure. PROVED BY: (a) a test feeding a synthetic payload on stdin with a KNOWN transcript and asserting the emitted text names THAT path in a `--session-log` argument -- assert on the literal path, not on the warning existing; (b) a test that a payload MISSING the transcript field fails closed with a named error and emits no fraction; (c) an ESCALATION test: rising usage across several invocations of ONE session emits once per band below threshold and on EVERY invocation at or above it -- assert the COUNTS per band, since 'a warning appeared' is what a ping-once implementation also passes; (d) a test that two DIFFERENT session ids do not share escalation state; (e) a test that the hook is SILENT and exits 0 outside an agi project and on an unreadable transcript -- it runs on every session on this box and must never break one; (f) the hook run by hand against a REAL payload naming a REAL transcript, output pasted -- a suite cannot see the shape this lives in; (g) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: it resolves a transcript by any route other than the handed payload; it pings once; it omits the `--session-log` path from the command it prints; escalation state is shared between sessions or keyed by seat; it assumes a denominator it did not measure; it can break or slow an unrelated session; or any existing test is edited. HARD CEILING: 2 kids. 🔴 SCOPE, HARD: create ONLY a new hook under `extensions/agi/hooks/` plus its test under `extensions/agi/tests/`. Do NOT edit `extensions/agi/bin/rotate.py` or `extensions/agi/tests/test_rotate.py` -- a parallel round owns both and a conflict costs more than the round. Do NOT add a file under `extensions/agi/bin/` (`test_bin_help_smoke.py` auto-enrols it). 🔴 DO NOT INSTALL IT: never write `~/.claude/settings.json` or any file outside this repo. Registering a hook globally changes every session on this box and is the OWNER's call, not a round's. Emit the exact registration snippet in your node and STOP. Do NOT run the full suite."
thought_session: sanctuary-director-genV-L4
title: A rotation warning must arrive unprompted, escalate, and carry its own next command
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-meter-you-must-remember-to-read-is-a-coin-flip

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEWED IN THE BYTES AND REPAIRED BY HAND. THE ARCHITECTURE IS RIGHT AND THREE DEFECTS WERE NOT, AND ALL THREE WERE INVISIBLE TO THE ROUND'S OWN GREEN SUITE.

WHAT THE ROUND GOT RIGHT, and it is the load-bearing half: the handed transcript path and nothing else — no resolver, no pin read, no glob, no newest-anything; a NAMED fail-closed error when `transcript_path` is absent; escalation by band with state keyed by SESSION ID under a per-uid tmp dir rather than the shared sessions dir; provenance printed beside the fraction; silent and exit 0 outside a project. Every architectural point survived review.

**DEFECT 1 — THE NUMERATOR SUMMED WHEN IT SHOULD HAVE TAKEN THE LATEST. 141x.** Context usage is a LEVEL, not a running total: every assistant turn's `usage` already contains the whole prior context, so adding turns together is roughly quadratic. Measured on my own real transcript, 211 assistant messages: **35,751,051 tokens, fraction 35.75**, against a true 253,460 and a true 0.2535. It would have printed "ROTATION OWED NOW" on essentially every session from its first few turns — **worse than no hook at all**, because a warning that always fires is a warning that gets waved through, which is the exact failure `hypothesis:l4-a-check-that-cries-wolf-gets-waved-through` names and which this hook exists to prevent.

**DEFECT 2 — THE EMITTED COMMAND COULD NOT RUN.** It printed `--seat <s> --pin --session-log <path>`, and `--pin` TAKES A PATH, so it swallowed the `--session-log` flag as its own value. P5 — hand over a copy-pasteable next command — is the hook's whole reason to exist, so an unrunnable command is not a typo, it is the deliverable failing. Identical in shape to the guard whose printed remedy did not clear the guard, repaired in L4.98 item 2 four hours earlier: the reader does exactly what the tool said and it does not work, and concludes the tool is broken.

**DEFECT 3 — THE PIN PATH WAS WORKTREE-LOCAL, and I only found it because I ran the repaired hook and read the path it printed.** It computed `root / "sessions"`, but pins are SHARED state and `rotate._sessions_dir` routes them to the MAIN checkout via `locations.git_common_root`. The emitted command would have written a pin to `…/worktrees/seat-<name>/.agi/sessions/` — where nothing looks — instead of `/home/ubuntu/work/agi/.agi/sessions/`. **A round about the meter capturing the wrong transcript nearly shipped a command that pins to a path no reader consults.** The repair ASKS `rotate._sessions_dir` rather than reimplementing it (a sixth private copy of a path rule is how this project keeps paying for the same defect) and returns None rather than guessing when it cannot, falling back to the seat-less form. **Never guess a pin path** is the whole chain's lesson.

🔴 THE FINDING THAT OUTLIVES THIS ROUND: **THE ROUND'S EIGHT TESTS PASS IDENTICALLY BEFORE AND AFTER A 141x CORRECTION.** They are not bad tests; they are tests whose fixtures carry one or two assistant messages, where the sum and the latest are the same number. A suite that cannot distinguish the defect from the fix is not testing the claim — and it is green either way, which is the dangerous part. This is the sharpest instance yet of "run the thing against the real tree before you believe its tests", and the two repair tests I added are built so the WRONG implementation fails them: a 200-turn fixture where sum and latest differ by construction, and a check that the emitted argv PARSES against rotate.py's own parser rather than merely looking right.

CROSS-CHECKED AFTER REPAIR, which is the evidence I would want if I were reading this cold: the hook and `rotate.py meter --seat sanctuary-director` now report the SAME number from the same transcript — 0.2671, 267,121 tokens — by two independent code paths. And the pin path it prints is byte-identical to the one every reader resolves.

NOT INSTALLED, and that stands: registering a SessionStart hook changes every Claude session on this box. The prime ratified build-and-do-not-install and added that the install is ITS to perform once the owner rules, so it happens once, in one place, verifiably — do not install it even if the owner says yes to you directly.
<!-- THOUGHT:END -->

## Agent Notes
FALSIFIERS RE-RUN AGAINST REALITY AFTER THE THREE REPAIRS — every one passes, and each was exercised as a real process with a real payload rather than in-process:

  (a) names the HANDED transcript in a --session-log argument .... PASS (literal path asserted)
  (b) payload missing `transcript_path` .......................... PASS (named fail-closed error, exit 3, NO fraction emitted)
  (c) escalation, one session, same band twice ................... PASS (fires once, second call SILENT)
  (d) two different session ids .................................. PASS (state not shared; the second fires)
  (e) outside an agi project / unreadable transcript ............. PASS (silent, exit 0, both cases)
  (f) run by hand against a REAL payload and transcript .......... PASS (0.2671 = 267,121 tokens)
  (g) commands.py run verify ..................................... PASS 8/8

CROSS-CHECK, the evidence I would most want if reading this cold: the hook and `rotate.py meter --seat sanctuary-director` now report the SAME fraction from the same transcript by two entirely independent code paths, and the pin path the hook prints is byte-identical to the one `rotate._sessions_dir` resolves.

VERDICT HELD AT A LEAN RATHER THAN RAISED TO PROVED, deliberately. The artefact satisfies every falsifier — but it satisfies them *after* three repairs it did not make itself, and the claim's real test is delivery INTO A LIVE SESSION'S TURN, which cannot be demonstrated until the hook is registered. Registration is owner-gated and the install belongs to the prime. Proving the falsifiers is not the same as proving the claim, and the gap between them is exactly the install. 85, not 100, for the same reason L4.93's kid gave itself 85.

DELIVERY PROVEN LIVE 16:4xZ (Prime L4-X): installed 16:21Z under UserPromptSubmit on the owner's GO; at 16:39Z the hook fired INSIDE the Prime's own running turn (a session started 14:04Z, before the install — hooks are re-read, not snapshotted): '## approaching rotation (0.3303 of the line). Crossed band 32% of threshold' with the runnable meter command naming the handed transcript. The claim's real test — delivery into a live session's turn — is met; the verdict may be raised from lean 85 by a kid on the bytes. Residue in flight as goal:g15.18 (SL1.05): the REGISTRATION block names SessionStart (wrong event), the band label prints int(b_frac x threshold x 100), the 'of the line' wording, and the threshold reads ladder.director_rotate_at 0.47 instead of the seat row's rotate_at.
