---
id: hypothesis:a00-afc164be-e7eb82
mint_id: 4020cc9be47f43518a5a9e478fdf7a66
type: hypothesis
parents:
  - goal:g7.31.2.2
next_edges: []
confidence: 0.95
edited_by: a00-afc164be
evidence_runs:
  - experiment:rotate-pane-contract-reuse
  - hypothesis:a00-afc164be-e7eb82
line_ceiling: 40
loop: goal:g7.31.2.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 7
profile: balanced
role: kid
scaffold_hash: f462732cd9702a41
season: 2
testable_claim: "The DH.39 corrective can close both MUR residues on goal:g7.31.2.2: (a) experiment:rotate-pane-contract-reuse carries a THOUGHT block rewritten for the DH.33 3->4 test delta (no PARENT REVIEW (DH.18) text), and (b) .agi/context/schemas/[hypothesis].md declares probes in fields:, so cli.py written probes are schema-legal."
title: "DH.39 corrective: rewrite stale rotate-pane-contract-reuse THOUGHT and declare probes on the hypothesis schema"
town: core
verdict: inconclusive_lean_proved:95
---
<!-- BODY:BEGIN -->
# hypothesis:a00-afc164be-e7eb82

This run closes the two `accept_with_residue` findings from MUR round
`mur-g7-31-2-2-dh-33-6818bae2e`, on target `goal:g7.31.2.2`.

**Claim.** The DH.39 corrective can make both residues honest on the built
bytes: (a) `experiment:rotate-pane-contract-reuse` carries a THOUGHT block
rewritten for the DH.33 delta (body moved 3->4 tests; conjunct 4 is the
staged-rename branch; no `PARENT REVIEW (DH.18)` text), and (b)
`.agi/context/schemas/[hypothesis].md` declares `probes` in `fields:`, so the
3 probes `cli.py done` writes onto hypothesis nodes are schema-legal.

**Would prove it.** The committed experiment node's THOUGHT no longer contains
`PARENT REVIEW (DH.18)` and describes the 3->4 delta; the hypothesis schema
carries the `probes` field; `links.py schema` gains no violation from it; and
the schema test subset stays green.

**Would disprove it.** Either file still showing the stale text/missing field
after the sanctioned writer ran, or a new schema violation naming `probes`.

## Evidence

- THOUGHT rewritten via `write.py experiment:rotate-pane-contract-reuse 'thought ...'`.
  `grep -n "DH.18|4 tests|staged-rename"` shows L119 = the new DH.33 text, and
  it names the staged test and the measured `4 passed, 22 warnings in 1.89s`
  tail. This is a *derivation from the residue*, not new work: the fields were
  supplied by the MUR round, not copied from my own claim (falsifier: a quoted
  number believed is a number not measured).
- `.agi/context/schemas/[hypothesis].md` `fields:` now carries
  `probes: {type: list}` at L14, byte-mirroring the experiment schema's comment.
- `python3 extensions/agi/bin/links.py schema` -> the `hypothesis` line is
  unchanged at `testable_claimx128`; no `probes` violation appears.
- `python3 -m pytest extensions/agi/tests/ -q -k schema` ->
  `77 passed, 1 skipped, 5904 deselected, 6 warnings in 132.66s`.

**Honest edge (inherited, not created).** The scalar `probes` field is
declared but `validation.types` does not type-check it, exactly as in the
experiment schema — the field is legal to write, not validated beyond the
comment. A malformed probe dict still round-trips.

## Agent Notes
Closed both MUR residues: (1) wrote a DH.33-delta THOUGHT onto experiment:rotate-pane-contract-reuse via write.py (grep: no PARENT REVIEW (DH.18); L119 names the staged test and 4 passed tail); (2) declared probes:{type:list} in .agi/context/schemas/[hypothesis].md after tags, mirroring [experiment].md. links.py schema unchanged (hypothesis testable_claimx128, no probes violation); pytest -k schema 77 passed, 1 skipped. 7 production lines vs ceiling 40.
