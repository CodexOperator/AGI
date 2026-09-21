---
id: hypothesis:a00-afc164be-e7eb82
mint_id: 4020cc9be47f43518a5a9e478fdf7a66
type: hypothesis
parents:
  - goal:g7.31.2.2
next_edges: []
confidence: 0.95
edited_by: a00-ef6f8809
evidence_runs:
  - experiment:rotate-pane-contract-reuse
  - hypothesis:a00-afc164be-e7eb82
line_ceiling: 40
loop: goal:g7.31.2.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "git show season2/loops/goal-g7.31.2.2-a00-afc164be:.agi/nodes/experiment/rotate-pane-contract-reuse.md | grep -n 'PARENT REVIEW (DH.18)'; and sed -n '29p;43p;75p' on the same committed blob", "expected": "the COMMITTED experiment node carries NO stale 'PARENT REVIEW (DH.18)' text, and the THOUGHT's cited facts match the committed body: L29 '(4 tests,', L43 '4 passed, 22 warnings in 1.89s', L75 the staged-rename test name", "observed": "grep 'PARENT REVIEW (DH.18)' -> no output (rc=1, absent); L29 'New file ... (4 tests,'; L43 '4 passed, 22 warnings in 1.89s'; L75 '(`test_staged_rename_spawns_successor_under_new_name_and_prev`: a real'; edited_by now a00-afc164be", "result": "holds"}
  - {"conjunct": 2, "class": "gate", "cmd": "git show season2/loops/goal-g7.31.2.2-a00-afc164be:.agi/context/schemas/[hypothesis].md > /tmp/hyp.md; load it through schema_registry.load_schemas_from_dir and assert 'probes' in hypothesis schema fields; same load for the loop-branch baseline 9de4c6ab2", "expected": "the COMMITTED kid-branch schema declares probes and the registry loads it as {type: list}; the loop-branch baseline does NOT -- a worktree-only edit fails this", "observed": "committed blob carries 'probes: {type: list}'; registry fields include 'probes' -> {'type': 'list'}; baseline 9de4c6ab2 fields lack 'probes' -> None; links.py schema hypothesis stays testable_claimx127 (no probes violation) before and after", "result": "holds"}
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

## Agent Notes
Closed both MUR residues: (1) wrote a DH.33-delta THOUGHT onto experiment:rotate-pane-contract-reuse via write.py, named as an owned path in this same done call (--owns) so the human-slug node lands in the round commit -- the mechanism whose absence caused the DH.33 residue; grep: no PARENT REVIEW (DH.18), L119 names the staged test and 4 passed tail; (2) declared probes:{type:list} in .agi/context/schemas/[hypothesis].md after tags, mirroring [experiment].md. links.py schema unchanged (hypothesis testable_claimx128, no probes violation); pytest -k schema 77 passed, 1 skipped. 7 production lines vs ceiling 40.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (DH.39, a00-ef6f8809). Corrective round ACCEPTED; verdict kept at the kid's own inconclusive_lean_proved:95.
(1) WHAT THE INSTRUCTION SAID: the DH.39 dispatch orders required 'Rewrit[e] THOUGHT for the DH.33 delta' on experiment:rotate-pane-contract-reuse, and 'Add probes: {type: list} to the hypothesis schema fields (mirror experiment schema)'; the parent task says a kid's tests are its CLAIM, read the DIFF, and run one negative probe per claim conjunct.
(2) WHAT THE MACHINE ACTUALLY DOES: `git diff 9de4c6ab2..season2/loops/goal-g7.31.2.2-a00-afc164be` carries exactly the two named deliverables plus this node -- .agi/context/schemas/[hypothesis].md (+5, probes after tags), .agi/nodes/experiment/rotate-pane-contract-reuse.md (edited_by -> a00-afc164be; THOUGHT replaced with 'DH.33 DELTA ...'), and the kid node. On the COMMITTED blob, grep 'PARENT REVIEW (DH.18)' is absent (rc=1) and the new THOUGHT's cited facts match the body byte-for-byte (L29 '(4 tests,'; L43 '4 passed, 22 warnings in 1.89s'; L75 the staged-rename test). Loading the committed [hypothesis].md through schema_registry gives fields including 'probes' -> {'type': 'list'}; the loop-branch baseline lacks it. Probes: (A wire) no stale text, cited facts match the committed body; (B gate) the committed schema blob loads probes as a list, baseline does not.
(3) THE NEAR MISS: accepting a worktree-only edit as closing the residue -- the schema field could have sat uncommitted in the kid worktree, and the THOUGHT could have described the delta from the kid's own summary without matching the body. Both probes read the COMMITTED blob (git show), and probe A re-checks the exact cited line content, not that a THOUGHT exists. Also: a reviewer grepping the bare token 'DH.18' would falsely flag the new THOUGHT, which names 'the DH.18 parent-review text' while describing the delta; the residue is the stale PARENT REVIEW text, not the token.
(4) DEVIATION / BOUNDARY: conjunct 2 is a DECLARATION, not enforcement -- schema_registry.validation validates only required/types/regex and never rejects undeclared frontmatter keys (measured: links.py schema shows hypothesis testable_claimx127 unchanged, no probes violation before or after). Declaring the field is registry/fingerprint/meta-node visibility, exactly as the experiment schema already declares it. This is the honest boundary, not a demotion: the residue asked for the declaration. Deviation: none.
<!-- THOUGHT:END -->

REVIEW DH.39: ACCEPTED, inconclusive_lean_proved:95 (kid's own). Both MUR residues CLOSED. (1) experiment:rotate-pane-contract-reuse's COMMITTED THOUGHT is the DH.33 delta -- grep 'PARENT REVIEW (DH.18)' absent, and the cited L29 '(4 tests,', L43 '4 passed, 22 warnings in 1.89s', L75 staged-rename test all match the body. (2) .agi/context/schemas/[hypothesis].md declares probes:{type:list}; the committed blob loads through schema_registry with 'probes' in fields as a list, while the loop-branch baseline lacks it. Probes: wire (committed bytes, no stale text, cited facts match) and gate (committed schema blob vs baseline). Named boundary: the field DECLARES, it does not enforce -- validation checks required/types/regex only, same as the experiment schema.
