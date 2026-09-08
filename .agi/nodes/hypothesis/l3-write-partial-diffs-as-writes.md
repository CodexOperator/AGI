---
id: hypothesis:l3-write-partial-diffs-as-writes
mint_id: d26321711f4b4cecb4c3eb294b2ec95a
type: hypothesis
parents:
  - goal:g13.1
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: 8f33da4044a59664
season: 2
testable_claim: "After the change, a node body or payload can be read by line range and written by applying a diff through write.py alone: a one-line change to a large module costs a one-line write rather than a whole-file re-emission, a patch that does not apply cleanly is refused loudly and changes nothing, and the partial write is stamped and grid-versioned exactly as a whole-file write is - proven red-first on a real engine module and on a real node body."
thought_session: belam-S1-L3-XI
title: "write.py can only replace a whole payload or a whole region, so every partial edit either bypasses the one sanctioned hand or costs a full re-emission: reads and writes should both be line-addressed, with a diff as the unit of write"
---
<!-- BODY:BEGIN -->
# hypothesis:l3-write-partial-diffs-as-writes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted from the owner's sentence the same turn it arrived. The framing deliberately leads with the fact that this hole is already written down in SKILL.md rather than presenting it as a new request, because the interesting part is not the feature but the evidence that the rule has been quietly unaffordable the whole time - the agents most required to use write.py are precisely the ones who cannot. The owner's piggyback-on-diffs instruction is taken literally and the brief forbids inventing a second patch format, since the grid already stores and renders exactly this delta.
<!-- THOUGHT:END -->

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF — and on this brief that sentence is also the design.

THE OWNER ASKED FOR THIS, 2026-09-08, verbatim: "We also need to implement partial write support so we can both read node bodies lines at a time and write to them the same. Maybe just piggyback it off the diff system and use diffs as writes".

THIS IS ALREADY A NAMED HOLE, NOT A NEW IDEA — which is why it should be closed rather than debated. `skills/agi/SKILL.md` records it verbatim: "Known gap: payload writes are whole-file only. There is no anchored or partial edit, so a one-line change to a large module still means emitting the whole file — which is why engine surgery across several modules is still done with ordinary tools plus a `thought` afterwards. That is a real hole in `goal:g13.1`, not a licence."

WHAT THAT HOLE ACTUALLY COSTS, in this project's own measurements. `write.py` is the ONE sanctioned hand: it stamps `edited_by` and `thought_session`, runs the spawn gate, warns on schema, and lands the payload and the reasoning in one submit. Every rule in this repo says use it. And every agent doing real engine work does not, because emitting a whole module to change one line is unaffordable — so the most careful writes in the system route around the mechanism built to make writes traceable. **A rule that is correct and unaffordable is a rule that gets skipped, and this one is skipped by exactly the agents whose edits matter most.** It also puts a hard floor under how cheap an agent can be: a kid on a flash model cannot re-emit a 2,000-line module at all, so whole-file writes silently reserve engine surgery for expensive models.

THE OWNER'S HANDLE IS THE RIGHT ONE AND IT IS ALREADY HALF-BUILT. The grid already stores every version and `grid.py diff` already renders the delta between them — the diff vocabulary, storage and rendering all exist. Do NOT invent a second patch format or a bespoke anchored-edit syntax. Piggyback, as the owner said.

WHAT TO BUILD.
1. READ BY RANGE. A node body or a payload can be read by line range through the same resolver `write.py` already uses for `payload_ref` and `location:`. Line-addressed, so a reader takes only the part it needs. Report the byte and token cost of a ranged read against the whole file in your node; a partial-read feature with no measurement is a claim, not a result.
2. WRITE BY DIFF. A new verb — `patch`, taking a unified diff on argv or on stdin the way `payload -` already does — applies to the node body or the payload and lands in the SAME submit as the `thought` that explains it, exactly as `payload` does today. Nothing about traceability may weaken: `edited_by`, `thought_session`, the schema warning, the grid version and the write-guard sanction all still happen, or the feature is a regression wearing a convenience.
3. FAIL CLOSED, TOTALLY. A hunk that does not apply refuses the WHOLE write and changes nothing on disk. There is no partial application, ever. A half-applied patch to a payload is a corrupted engine file that reports success, which is this loop's single most expensive failure shape and has now cost it four separate defects.
4. RESPECT THE EXISTING SHARP EDGES, one of which this brief hit while being written. The script form splits on a doubled ampersand, so no prose verb can contain one — the first attempt to save this very brief was REFUSED with `ERR: no verb` because the text quoted that operator. A diff will contain almost any character, so patch bytes must arrive by stdin, never inline; `payload -` is the precedent to copy. Preserve the destination's mode as `payload` does, so patching a script cannot disarm it. Refuse a source that does not exist rather than emptying a payload on a typo.

RELATED, DO NOT ABSORB IT: `hypothesis:l3w4-handoff-sections-claimable` is the same family one level up — addressing part of a document instead of the whole — but it is about claiming and locking named sections of `HANDOFF.md`, not about line ranges or patches. If your line-addressing turns out to be the natural substrate underneath it, say so in your node and leave the wiring to a later round.

PROVE IT, RED FIRST. A one-line change to a real engine module landed through `write.py patch`, with the diff shown and the resulting `grid.py diff` shown beside it. A ranged read of a real node body with the two size numbers. A malformed hunk refused with the file byte-identical afterwards, verified by checksum. A patched executable still executable. Verify the red half by stashing the fix. Paste actual output, not a description.

DO NOT touch `workflow.py`, `rotate.py`, `dispatch.py`, `brief.py` or `zoom.py`. Do not write `.agi/nodes/.geometry/seats.md`. Do not kill any `belam-*` tmux window. Do not weaken or bypass `write_guard.py` to make your tests pass — if the guard fires on your own writes, that is the guard working and your write is the thing to fix.
