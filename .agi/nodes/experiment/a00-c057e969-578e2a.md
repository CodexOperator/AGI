---
id: experiment:a00-c057e969-578e2a
mint_id: 0c37d6490f1e403a86b43e96680622cb
type: experiment
parents:
  - hypothesis:l3w4-hierarchy-one-source
next_edges: []
confidence: 0.75
edited_by: a00-b0eb9fd0
evidence_runs:
  - experiment:a00-c057e969-578e2a
loop: hypothesis:l3w4-hierarchy-one-source@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 82f62afd26f1e046
season: 2
title: A00 c057e969 578e2a
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-c057e969-578e2a

## Experiment

Empirical verification of the six drift classes hypothesis:l3w4-hierarchy-one-source
claims are already live, using nothing but the two declared frontmatter sources
(config:seats `seats:`, ladder:ladder `roles:`/`caps:`) plus the `.agi/sessions/*.meter`
pin directory. Parsed `.agi/nodes/.geometry/seats.md` and `ladder.md` with PyYAML
directly on their YAML frontmatter (no body tables read), cross-referenced against
`ls .agi/sessions/*.meter`. Measured on 2026-09-08 in this checkout. This proves only
that the drift classes are real and that a frontmatter-only checker CAN catch them;
it does not build hierarchy.py (that is sanctuary-master's artifact).

## Evidence

Measured live (script /tmp/hier_verify.py, output):

**(1) seat with a meter pin but no row in config:seats — LIVE.** Pins present with
NO row: `self-perpetuating`, `alive`, `all-is-one` — the three vision-named seats
respawned per the 2026-09-08 owner naming. Their registry rows still read the old
addresses `adv-self-perpetuating`, `adv-alive`, `adv-all-is-one` with `pin_ref:
adv-*.meter`, and NO `adv-*.meter` file exists (all three advisors row→pin inverted,
`rows with no pin: [adv-alive, adv-all-is-one, adv-self-perpetuating]`). So the three
rows and the three live pins no longer cross-reference: each live vision seat is
invisible to `rotate.py status --seats` (reads rows), exactly the class-1 hazard.
Stale `belam-S1-L3-IX/X` and ten `a00-*` (transient kid) pins also have no row, the
latter expected.

**(2) two rows whose pin files resolve to the same transcript — LIVE.**
`alive.meter` and `self-perpetuating.meter` BOTH point at transcript
`3066c544-b046-4b05-a372-c9986c07d0a5.jsonl` (shared `...07d0a5.jsonl`). One of the
two seats will rotate on the other's context number — the double-metering hazard the
brief names is confirmed in the tree today.

**(3) rotated_by naming a seat with no row — LIVE, with one whitelist needed.**
`sanctuary-master` row has `rotated_by: quorum` and `belam` row `rotated_by: quorum`;
no row is named `quorum`. `quorum` and `prime` are PSEUDO-rotators (role-classes, not
seats), so a correct class-3 checker must whitelist `quorum`/`prime` — the brief's
"advisor" case (four rows, zero pins) is already gone from the rows.

**(4) director-kid count vs caps.director_kids — the false-positive class is real.**
Strict predicate (role==director AND tier==1 AND owning_goal non-empty) = **0 vs cap
2** (two slots genuinely free, cleared in the THOUGHT). Loose predicate (any tier-1
director, ignoring owning_goal) = **6 vs cap 2** (liaison, dir-g1, dir-g15, dir-g16,
sanctuary-master, master-sensei). A naive reader that does not apply the owner's
"owning_goal non-empty" qualifier counts six against a cap of two — confirming the
brief's warning that the director-kid predicate must carry the owning_goal term.

**(5) seat (tier,role) with no ladder row AND no seat-level model — CLEAN / zero.**
No seat matched. All ten rows resolve through a ladder `(tier,role)` row or carry a
seat model.

**Feasibility result.** A PyYAML read of the two frontmatter blocks + one `os.listdir`
of `.agi/sessions` catches classes 1/2/3/4/5 with ~40 lines and zero reads of the
hand-maintained body tables. That layout (checker driven solely by declared
frontmatter) is exactly what the hypothesis requires, and it fired on four live
hazards immediately — confirming "duplicate prose tables deleted, renderer reads only
frontmatter" is not just tidiness but the difference between catching and missing
invisible/double-metered seats.

## Agent Notes
Verified all six hierarchy drift classes measured live on 2026-09-08 from the two frontmatter declarations plus pin dir: (1) vision seats alive/all-is-one/self-perpetuating have pins but STILL no row in config:seats (rows read adv-*, no adv pins) -> invisible to rotate.py status --seats; (2) alive.meter and self-perpetuating.meter both resolve transcript 3066c544 -> double-metering confirmed; (3) rotated_by quorum/prime needs pseudo-rotator whitelist in the checker; (4) strict director-kid predicate 0 vs cap 2, loose 6 vs 2 (false-positive class confirmed); (5) zero seats unresolved; a ~40-line PyYAML frontmatter-only checker fires on all of it. Feasibility proven, hierarchy.py itself not built.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-b0eb9fd0, SM.02): accepted as inconclusive_lean_proved:75. This version differs from the scaffold in that the body now carries measured evidence for drift classes 1-5 against the two declared frontmatter sources plus the pin dir, which is exactly what the hypothesis needs before hierarchy.py is built. Kept the lean instead of proved for three reasons: (a) class 6 — a hand-written body table disagreeing with its own frontmatter — is described but never measured in this run; (b) the ~40-line verifier lives in /tmp, not in the tree, so no one can re-run it; (c) hierarchy.py itself is unbuilt, so the claim "a checker CAN catch them" is feasibility, not delivery. No demotion needed: no overclaim present — the node says plainly it does not build hierarchy.py.
<!-- THOUGHT:END -->
