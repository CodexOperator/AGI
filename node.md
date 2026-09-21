---
id: hypothesis:l3-rotate-self-successor-override
mint_id: 959115dc057a45ccac15eb0502f6b1fc
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-IX
scaffold_hash: 15062e785a9128eb
season: 2
testable_claim: After the change, rotate.py rotate-self accepts an explicit successor-command override and a throwaway-seat registration path that never writes seats.md, with the default path byte-identical to today's real claude spawn; proven by a red-first test for each half, and measured live by one rehearsed rotation in which a NEW tmux window exists under the reused plain name (checked with tmux list-windows, not the tool's return value), the seat handoff generation increments, the read-back reads the successor's log, a deliberately planted stale bare continue does NOT falsely confirm the new generation, and the predecessor's window is renamed and left alive.
thought_session: belam-S1-L3-IX
title: "The live rotation proof is blocked by rotate-self itself: the successor argv is hardwired to real claude, so no kid can ever exercise it"
---
<!-- BODY:BEGIN -->
# hypothesis:l3-rotate-self-successor-override

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

WHY THIS EXISTS, AND WHY IT IS THE HIGHEST-PRIORITY UNBLOCK IN WAVE 4. The live tmux rotation proof has been owed since L3.31 and has never once been observed across nine prime generations. At L3.37 a kid was dispatched to deliver it and could NOT — not through unwillingness, and not through any fault of its own. It reported the blocker precisely and honestly rather than faking the proof, and its report is the specification for this brief: "rotate-self's stand-in TTY override does NOT exist (successor argv is hardwired `claude --remote-control`), so the brief's 'use a stand-in command' hint is not achievable through the tool itself". The brief asked for a proof its own tool made impossible. That is a TOOL gap, not a kid gap, and no amount of re-briefing will close it.

WHY IT MATTERS BEYOND ITSELF: the owner's standing gate (HANDOFF.md §6 item 47, verbatim "once we verify that perpetual seats work well and fully let's just stop there for a bit before we start them running") requires perpetual seats to be verified FULLY. A seat is perpetual only because it rotates. So every seat in `goal:g17` is gated behind a rotation nobody can currently exercise without spending a real Claude subscription session on every attempt — which is why nine directors in a row have deferred it.

WHAT TO BUILD. `rotate.py rotate-self` (and `rotate.py spawn`/`loop` where they share the path) gains an explicit successor-command override so the mechanism can be exercised end to end without launching a real `claude` session. Shape it however the code wants, but it must satisfy all four: (1) the DEFAULT is exactly today's behaviour, byte for byte — a real `claude --remote-control` successor — so no existing caller changes; (2) the override is explicit and impossible to trip into accidentally; (3) EVERY step downstream of the spawn still runs for real against the stand-in — window creation, the plain-name reuse, the read-before-write cursor, the single-word read-back, the predecessor rename — because a proof that stubs the interesting half proves nothing; (4) it is safe to run on a box that is about to be livestreamed: no secret reaches the pane, and no real seat is started.

SECOND HALF, EQUALLY REQUIRED: a sanctioned way to register a THROWAWAY seat for a rotation rehearsal, so the exercise does not need `seats.md` — which the Sanctuary Master owns and which no other seat may write. An ephemeral registry overlay, a `--throwaway` flag, an in-memory row: your call, but it must NOT write the real registry, and the L3.37 kid confirmed the registry gate correctly refuses an unregistered seat today, so this half is genuinely load-bearing and not a convenience.

THEN PROVE IT, LIVE, IN THIS SAME RUN. Rotate a throwaway seat with a stand-in successor and record the observation with commands and their output: (a) a NEW tmux window exists afterwards under the reused plain name — check `tmux list-windows`, NEVER the tool's own return value, because `rotate.py loop` once reported a successful rotation and spawned no window at all; (b) the seat handoff is written with an INCREMENTED generation; (c) the read-back reads the SUCCESSOR's log and not the caller's; (d) a deliberately planted stale bare `continue` in the reused plain-name log does NOT falsely confirm the new generation — the L3.31 read-before-write cursor exists precisely for this and has never been exercised live, so plant the stale line and confirm the refusal; (e) the predecessor's window is RENAMED and left ALIVE.

DO NOT: write `.agi/nodes/.geometry/seats.md`; start, populate or run any REAL seat (the owner gate above); kill any `belam-*` tmux window (the predecessor chain depends on every one of them staying alive); or change what `rotate.py meter` measures.
