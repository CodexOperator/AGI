---
id: hypothesis:l3-seat-pin-not-repointed-on-rotation
mint_id: 47195e6025e84c42af06bc5a1a437904
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: e66434019d26b0cb
season: 2
testable_claim: "After the change, the meter read through a seat can never be another generation's: the successor's own transcript is pinned as part of rotation (or the pin carries the generation that wrote it and a mismatch is a loud refusal, never a silent stale read), proven red-first against a pin left pointing at a predecessor."
thought_session: belam-S1-L3-XI
title: A seat pin is written by the generation that claims it and never re-pointed on rotation, so rotate.py meter --seat reads the PREDECESSOR's context usage
---
<!-- BODY:BEGIN -->
# hypothesis:l3-seat-pin-not-repointed-on-rotation

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

MEASURED LIVE, 2026-09-08, by Belam XI in its first twenty minutes. `.agi/sessions/belam.meter` is the seat pin Belam X created — the first live pinned seat this box has ever had (HANDOFF §0.7, "FIRST LIVE PINNED SEAT"). Belam X wrote its OWN transcript path into it and rotated. Belam XI then ran the standard check the handoff instructs it to run:

    $ rotate.py meter --seat belam
    0.3312  331231/1000000 tokens  source=seat_pin  threshold=0.35

That is Belam X's usage. Belam XI's own was 0.1866. The seat pin still pointed at `49835b37-...jsonl`, the transcript of a session that had already ended.

WHY THIS IS A SAFETY DEFECT AND NOT A COSMETIC ONE. The prime rotates at 0.35. A successor that trusts `--seat` inherits a reading that has nothing to do with its own context and is wrong in BOTH directions:
- Predecessor rotated near its cap (the normal case, since rotating IS what empties a seat): the successor reads ~0.33 against a 0.35 threshold and rotates almost immediately, having done nothing. Each generation then burns a full spawn to accomplish one round of nothing, and the ladder degenerates into rotation with no work between the rotations. Belam XI was four hundredths away from exactly this.
- Predecessor rotated early (Belam VII at 0.2892, Belam IX at ~0.27 — both deliberate, both recorded): the successor reads LOW, keeps working past its real cap, and dies mid-round with no handoff written. That is the antifragility failure the ladder exists to prevent.

`source=seat_pin` is printed with total confidence in both cases. Nothing warns. This is the same family as the two defects that cost this loop three generations — `rotate.py loop` returning 0 unconditionally, and the grid refspec silently vanishing — and it is the third time this project has been bitten by a component that reports success while delivering the wrong thing.

WHAT TO BUILD. Decide the shape and say why you chose it; both of these are defensible and one may be strictly better:
1. ROTATION RE-POINTS. `rotate.py` writes the successor's transcript into the seat pin as part of rotating, so the pin follows the seat's live occupant. Note the ordering problem honestly: the successor's transcript does not exist until it starts, so this likely means the successor claims the pin on ITS first meter read, not the predecessor writing it on the way out.
2. THE PIN CARRIES ITS WRITER. The pin records which generation wrote it, and a read by a different generation is a LOUD REFUSAL naming both, never a silent stale number. This is weaker at fixing and stronger at never lying, which given the history above may be the more valuable half.
Build the refusal in any case. A wrong meter must not be able to print as a confident one.

ALSO CHECK, because the same shape probably repeats: `config:seats` declares eight seats and the L3.37 review found every one reading `no_pin`. Now that pins are real, every seat has this defect and not only the prime's. Say in your node whether the fix covers all eight or only the one you tested.

PROVE IT, RED FIRST. A test that pins seat S to generation A's transcript, reads the meter as generation B, and asserts the result is a refusal or B's own number — never A's. Verify it red by stashing the fix. Then a live read: `rotate.py meter --seat belam` from this session, with the output pasted into your node.

DO NOT touch `workflow.py` or `.agi/config.json` workflow rows (another parent holds them this round). Do not touch `dispatch.py`, `brief.py`, `cli.py` or `zoom.py`. Do not write `.agi/nodes/.geometry/seats.md` — seat rows are owner-sanctioned content and a kid appending to that file directly is a recorded violation (HANDOFF §6 item 44). Do not kill any `belam-*` tmux window; the predecessor chain lives in them.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted the moment the defect was measured rather than after the round, because it is the class of finding that gets carried in a handoff and never fixed. The framing deliberately refuses to treat it as a rotate.py bug: the pin is a per-seat artefact being written with per-generation data, so the fix is about ownership of the pin, not about the meter command. Recorded both failure directions because the dangerous one is the quiet one - a successor reading LOW works past its cap and dies without a handoff.
<!-- THOUGHT:END -->

HARNESS CONSTRAINT FOR THIS ROUND (Belam XI, 2026-09-08, operational — not part of the claim). The `.env` OpenRouter runtime key is at its cap (`remaining $-0.02`, floor $1.00), so `dispatch.py` refuses every pi spawn with `ERR: runtime key ... below the configured floor`. Spawn your kid on the subscription instead:

    python3 extensions/agi/bin/dispatch.py . L3.41 --target <this node> --level small --tier kid --harness claude-code

Measured: `--harness claude-code` on the PARENT invocation does not reach the kid — the parent's own `dispatch.py` call falls back to the ladder row (pi) and hits the key floor. Pass the flag explicitly on the kid dispatch. Do NOT raise the key limit or edit `.env` to get around this; that is the owner's decision and it is banked. Do NOT treat the blocked spawn as a reason to do the kid's work yourself.
