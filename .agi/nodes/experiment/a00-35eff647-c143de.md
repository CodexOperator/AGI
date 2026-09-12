---
id: experiment:a00-35eff647-c143de
mint_id: bbfceedd9eba4bff8064eb6d473dc707
type: experiment
parents:
  - hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt
next_edges: []
confidence: 0.72
edited_by: a00-84f091be
evidence_runs:
  - experiment:a00-35eff647-c143de
loop: hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ccb8abe00b134807
season: 2
title: A00 35eff647 c143de
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-35eff647-c143de

## Experiment

SL7.70 close-of-loop for `hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt`. Kid 2 (`experiment:a00-83d5d0e0-bcf35b`) built the P7 carve-out tests and **named** the sentences that still tell a seat to read the meter by hand; the hypothesis authorized dropping them. This run did the DROP by reworking the single class-(a) instruction.

**T1 — CLASSIFY each of kid 2's four named hits (read the bytes in context):**

| hit | bytes in context | class | decision |
|---|---|---|---|
| `.agi/nodes/doc/l4-owner-decisions.md` body 446 (prime-'Banked' section, header 'prime recommendations, NOT owner text') — "Seats read the meter after every round close and before every dispatch, not only at pauses." | standing protocol order to a seat to read the meter BY HAND, per generation | **(a) instruction** | REWORD — the only one in scope |
| `skills/agi/SKILL.md:128` — "**Rotation:** `rotate.py meter` prints context-usage fraction against `director_rotate_at` (this project: 0.47 …)" | reference line describing what `rotate.py meter` does + the threshold | **(b) description** | LEAVE — not an instruction; the 0.47 `director_rotate_at` prose is expressly not mine to edit |
| `skills/agi/SKILL.md:140` — "**`agi:check-handoff`** → `rotate.py meter --check …`" | description of what the named `agi:` invocation does | **(b) description** | LEAVE |
| `extensions/agi/briefs/prime-director-successor.md:7` — "Pin your meter yourself: `rotate.py meter --pin …`" | inside the `IF THERE IS NO ## STARTUP OUTPUT BLOCK … you were seated by rotate.py spawn` RECOVERY wake shape, where nothing was pre-run and no auto line exists | **(c) recovery** | LEAVE — no auto line on that path; also outside the file scope |

**T2 — REWORD, do not delete (target shape):** applied via the sanctioned writer —
`python3 extensions/agi/bin/write.py doc:l4-owner-decisions 'replace body 446:446 -'` (< new text on stdin). New text keeps the measured gen-I fact (0.5185 past cap), states the hook auto-prints the meter line on every prompt inside a project with a readable transcript, removes the per-prompt hand call, and keeps `rotate.py meter` / `agi:check-handoff` documented as the fallback when the line is absent (outside a project, or P7 silence). No owner-verbatim passage touched. This was the ONLY class-(a) hit; the per-prompt hand call the hypothesis exists to remove is gone from the one standing instruction that demanded it.

**T3 — routes:** node edit went through `write.py` (`doc:l4-owner-decisions`, body 446); `skills/agi/SKILL.md` was NOT edited (both hits there are class-(b)), so no build-node thought and no SKILL test run was owed. No code changed.

## Evidence

- Pre-edit body 446 (verbatim): "Seats read the meter after every round close and before every dispatch, not only at pauses."
- Post-edit body 446, confirmed by re-read: "…The rotation-alert hook now prints `[meter] post=<post> <fraction> (<tokens>/<window>) line=<threshold>` as the last line of every prompt inside an agi project with a readable transcript, so seats no longer have to run `rotate.py meter` to read their own context. Run it (or `agi:check-handoff`) only when the line is absent — outside an agi project, or when the hook could not read the transcript (P7 silence)."
- `write.py` returned `updated: doc:l4-owner-decisions`; THOUGHT recorded on `experiment:a00-35eff647-c143de`.
- No code changed (only a node doc), so no pytest run was required.
- Bytes left untouched with reason (see row): `skills/agi/SKILL.md:128` (b), `skills/agi/SKILL.md:140` (b), `extensions/agi/briefs/prime-director-successor.md:7` (c).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW SL7.70 (a00-84f091be), accepted as proved at confidence 0.72 -- the round's lowest, and correctly so: this node is a DOCUMENTATION change with no test evidence, so its support is a re-read of the bytes rather than a suite, and 0.72 is the honest number for that. I verified the artifact myself and not the report: `git diff HEAD -- .agi/nodes/doc/l4-owner-decisions.md` shows exactly ONE line changed and `git diff HEAD -- skills/agi/SKILL.md` is EMPTY, so the "left it alone" claims are checkable and true, not paraphrase. I re-ran the rotation suite (43 passed) and the FULL engine suite (4110 passed, 8 skipped, 1 xfailed in 785.91s) after the edit, and `links.py links` reports 2744 resolved / 0 broken. ACCEPTED: the classification table is the right shape of work and its per-hit reasoning matches what I read in the bytes -- SKILL.md:128/:140 really are descriptions of what the commands do, and prime-director-successor.md:7 really does sit inside the `IF THERE IS NO ## STARTUP OUTPUT BLOCK` recovery wake shape where nothing was pre-run and no auto line exists. DEMOTION I REVERSED: this kid's verdict is proved but its node carried NO thought on `doc:l4-owner-decisions` itself -- the writer recorded the edit and this experiment node carried the reasoning, so a reader zooming into the doc node saw a changed sentence with no delta attached. I wrote that thought onto doc:l4-owner-decisions under my own name (SL7.70, parent), which is the review landing where the work is. NEAR MISS the round avoided by accident and should keep avoiding: "may then drop the sentence" read as licence to DELETE the clause would have satisfied the claim's words and removed the only escape hatch for the two paths where the hook is silent BY DESIGN (outside an agi project, and a transcript the hook could not read -- P7, pinned in experiment:a00-83d5d0e0-bcf35b). My brief said reword-not-delete before the kid ran, so this was a brief-level catch, not a kid-level one. Deviation from "a g15 claim is a build order, not a measurement" (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement): this one WAS a build -- it changed bytes a reader acts on -- but its deliverable is prose, so the build is complete when the sentence says the true thing, not when a test goes red. Property of this case that makes the rule not apply: the claim's own text scopes the deliverable to an EDIT ("may then drop the sentence"), and the only assertion available is that the new sentence matches the hook's measured behaviour, which experiments a00-7cee97dc and a00-83d5d0e0 already established.
<!-- THOUGHT:END -->

## Agent Notes
Closed the loop: classified kid 2's four named read-the-meter hits and dropped the single class-(a) standing instruction (doc:l4-owner-decisions body 446) via write.py replace body 446:446 — reworded to point at the auto [meter] hook with the P7/outside-project fallback, no hand call per prompt. Left SKILL.md:128 (b description + 0.47 prose not mine), SKILL.md:140 (b description), prime-director-successor.md:7 (c recovery-spawn path, no auto line, out of scope). No code changed.
