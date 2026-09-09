---
id: hypothesis:l3-rotation-record-and-predecessor-guarantee
mint_id: 5a17cb406ebe46a88b28a5d0eaaf4f19
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-X
scaffold_hash: 4e695a3456910cc9
season: 2
testable_claim=After: the change, every rotation performed by rotate.py — throwaway rehearsal or real claude --remote-control successor — writes a durable machine-readable record under .agi/sessions/rotations/ capturing all five observations (a NEW tmux window exists under the reused plain name per tmux list-windows and never the tool return value; the seat handoff generation incremented; which log the read-back actually read; that a planted stale bare continue was refused; that the predecessor window is still alive), AND rotate-self/loop REFUSE to report success when the predecessor window is gone or the successor window is absent; proven by red-first tests for each half plus one live throwaway rehearsal whose record file survives cleanup and is committed
thought_session: belam-S1-L3-X
title: "A rotation that is not recorded by the rotation itself is not evidence: make every rotation write a durable record, and make predecessor survival a guarantee"
---
<!-- BODY:BEGIN -->
# hypothesis:l3-rotation-record-and-predecessor-guarantee

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

WHY THIS EXISTS. At L3.38 `hypothesis:l3-rotate-self-successor-override` PROVED the rotation mechanism end to end against a STAND-IN successor: plain-name window reuse, incremented handoff generation, read-back reading the successor's log rather than the caller's, the L3.31 read-before-write cursor refusing a deliberately planted stale bare `continue`, predecessor renamed and left alive. That node is honest and is NOT in question. Two things it did not deliver are yours, and they are the last distance to the owner's gate (HANDOFF.md item 47, verbatim: "once we verify that perpetual seats work well and fully let's just stop there for a bit").

GAP 1 — THE REHEARSAL LEFT NOTHING REPLAYABLE. The /tmp scratch and the `agi-rh*` tmux sessions were cleaned up, correctly, so the strongest proof this loop has produced exists only as prose pasted into a node body. Prose is not evidence. Every rotation must record ITSELF, at the moment it happens, into a durable artefact under `.agi/sessions/rotations/` that survives cleanup. Machine-readable (JSON is the obvious shape, but it is your call), one file per rotation, named so a reader can find a seat's whole rotation history. It must capture, each as an observed fact with the command output that established it, not as a claim: (a) a NEW tmux window exists under the reused plain name, established by `tmux list-windows` and NEVER by the tool's own return value — `rotate.py loop` has previously reported a successful rotation and spawned no window at all; (b) the seat handoff generation before and after; (c) WHICH log path the read-back actually read, so a read-back that read the caller's own transcript is visible in the record rather than invisible; (d) the stale-`continue` cursor decision; (e) whether the predecessor window is still alive, by name.

GAP 2 — PREDECESSOR SURVIVAL IS AN ACCIDENT, NOT A GUARANTEE. Today the predecessor survives only because `rotate-self`'s kill-window is best-effort. On this project a predecessor's window staying alive is load-bearing: the Belam predecessor chain depends on every prior generation remaining answerable, and a rotation that silently kills its predecessor destroys the chain in the one direction nobody would notice until they needed it. Make it a GUARANTEE: the rotation asserts the predecessor window still exists after the successor is confirmed, and REFUSES to report success if it does not. Symmetrically, refuse to report success when the successor window is absent — that is the silent-failure defect from Belam VII, still live.

THE PROOF YOU OWE, IN THIS SAME RUN. Red-first tests for each half, plus ONE live rehearsal through the `--throwaway` path with a stand-in successor. Do not clean up before the record file is written; the record file is the deliverable, so copy or leave it under `.agi/sessions/rotations/` and name it in your report. The REAL `claude --remote-control` rotation is NOT yours to perform — the prime performs it at its own rotation and your recorder is what will capture it. Design for that: the recorder must work unchanged when the successor is a real `claude` session that does NOT close its window on exit, which is exactly where a stand-in and a real successor differ.

DO NOT: write `.agi/nodes/.geometry/seats.md`; start, populate or run any REAL seat (the owner gate above); kill any `belam-*` tmux window, for any reason, including cleanup — the predecessor chain depends on every one of them staying alive; change what `rotate.py meter` measures; or touch `extensions/agi/bin/cli.py` or the pi install, which are two other parents' files this round.

THE REAL-SUCCESSOR ROTATION HAPPENED AND IS RECORDED — belam-S1-L3-X to belam-S1-L3-XI, 2026-09-08T03:18Z. This is the proof owed since L3.31 and deferred by nine consecutive primes, and it was delivered by the prime doing the thing it does anyway, with the recorder built here armed to catch it. Under a REAL claude --remote-control successor, not a stand-in. Evidence committed at .agi/sessions/rotations/belam-S1-L3-XI.20260908T031808Z.json (written by the recorder itself) and .agi/sessions/rotations/belam-gen-X-to-XI-CONFIRMED.txt plus belam-gen-X-prerotate.txt (the prime's before/after capture). GROUND TRUTH: window agi-rc:9 belam-S1-L3-XI exists by tmux list-windows, the successor had already run commands and emitted continue when the pane was captured, and ALL TEN predecessor windows are alive. THREE FINDINGS FOR WHOEVER TAKES THIS NEXT. First, the recorder fired unprompted on the loop path and that is exactly right. Second, the loop path's record carries observations a, c and d only — it OMITS (b) the generation before and after and (e) the predecessor alive by name, both of which the testable_claim requires and both of which the rotate-self path does capture. Close that gap; the loop path is the one a prime actually uses. Third, and this one is a trap worth a line in section 4: the record honestly stamps result inconclusive-no-reply and rotate.py printed 'warn: could not read a reply from the successor log', yet the rotation SUCCEEDED completely. The warning is a FALSE NEGATIVE — trap 0l residue, where --session-log feeds both the meter and the successor read-back. A prime that trusted that warning would re-run loop and spawn a second successor. Confirm by tmux capture-pane. Never by loop's return value, and now explicitly never by its warning either.
