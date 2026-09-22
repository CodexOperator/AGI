---
id: experiment:dh66-residue-reland
mint_id: e7d0a43a6d2e4cceaa934a9109c00df0
type: experiment
parents:
  - hypothesis:a00-1730b266-bec5cf
next_edges: []
confidence: 0.82
edited_by: a00-1730b266
evidence_runs:
  - experiment:dh66-residue-reland
line_ceiling: 40
loop: goal:g7.31.2.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: fdd6237663a395d6
season: 2
testable_claim: The five MUR mur-g7-31-2-3-dh-40-a5b82056a-lean2-3 residues on goal:g7.31.2.3 are closed on base 4be44e272 by write.py-only node edits with 0 production lines, and evidence_gate enforce --dry-run reports exactly 1 would-demote (the out-of-scope experiment:a00-3c0140ac-dh45-fix) and 0 refused.
title: "DH.66 residue re-land: five MUR residues closed on base 4be44e272, 0 production lines"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:dh66-residue-reland

## Experiment

DH.66 corrective run under `goal:g7.31.2.3`. The parent re-measured base
`4be44e272` and found all five residues from MUR
`mur-g7-31-2-3-dh-40-a5b82056a-lean2-3` still **OPEN** — DH.50's claimed edits
(tip `4a8cdf187`) were not on this base. I re-measured, re-landed all five
through `write.py` alone, and re-measured the bytes.

### Before (measured at `4be44e272`, before my edits)

```
$ grep -A3 '^evidence_runs:' .agi/nodes/hypothesis/a00-9fa7f4f5-60c4ba.md
evidence_runs:
  - experiment:a00-1b9a8e7e-profile-sync
  - hypothesis:a00-9fa7f4f5-60c4ba        # <- self-id present, R1 OPEN

$ grep -n '1,089,136\|0d506080' .agi/nodes/hypothesis/a00-bc25f6f9-5c369a.md
28:testable_claim: ... (1,089,136 bytes, sha256 0d506080...8b66e3, measured DH.40) ...
72:(1,089,136 bytes at DH.40, sha256 0d506080...8b66e3) production file's ...   # R2 OPEN

$ grep -c 'testable_claim' .agi/nodes/hypothesis/a00-a267ee09-3bbf9c.md
0                                          # R3 OPEN

$ grep -c 'with `_KNOWN_HARNESS_IDS`\.' .agi/nodes/hypothesis/a00-cf0076c2-41525b.md
2                                          # R4 OPEN
```

R5: the `## Hypothesis` section of `a00-9fa7f4f5-60c4ba` was empty (the next
heading immediately followed it).

### Edits (all through `write.py`, node bodies only)

- R1 `hypothesis:a00-9fa7f4f5-60c4ba`: `set evidence_runs [experiment:a00-1b9a8e7e-profile-sync]`
- R2 `hypothesis:a00-bc25f6f9-5c369a`: `set testable_claim ...` + `replace body 40:40`
  — decision: **drop, do not re-measure**; any pinned byte count re-stales
  against the next merge target and the claim is about the gate, not the count.
- R3 `hypothesis:a00-a267ee09-3bbf9c`: `set testable_claim ...` + `replace body 6:6`
- R4 `hypothesis:a00-cf0076c2-41525b`: `replace body 20:21` — dedupe to one fragment
- R5 `hypothesis:a00-9fa7f4f5-60c4ba`: `replace body 4:5`, then `replace body 6:6`
  to keep the blank line before `## What was done`
- Target `goal:g7.31.2.3`: `replace body 27:45` (whole Agent Notes residue table)
  + `thought`

## Evidence (after)

```
$ grep -A2 '^evidence_runs:' .agi/nodes/hypothesis/a00-9fa7f4f5-60c4ba.md
evidence_runs:
  - experiment:a00-1b9a8e7e-profile-sync
loop: goal:g7.31.2.3@s2                     # self-id gone

$ grep -n '1,089,136\|0d506080' .agi/nodes/hypothesis/a00-bc25f6f9-5c369a.md
exit 1, zero hits

$ grep -c 'testable_claim' .agi/nodes/hypothesis/a00-a267ee09-3bbf9c.md
1

$ python3 extensions/agi/bin/links.py schema | grep -c a00-a267ee09
0

$ grep -c 'with `_KNOWN_HARNESS_IDS`\.' .agi/nodes/hypothesis/a00-cf0076c2-41525b.md
1

$ python3 extensions/agi/bin/write.py hypothesis:a00-9fa7f4f5-60c4ba 'read body 4:8'
## Hypothesis

The target `goal:g7.31.2.3` gate claim: `rotate.py` carries zero new harness argv builders; ...
```

Gate, wire and suite on this tip:

```
$ python3 extensions/agi/bin/evidence_gate.py enforce --dry-run
EVIDENCE-GATE would demote experiment:a00-3c0140ac-dh45-fix: proved -> inconclusive_lean_proved:50
evidence-gate enforce: 1 unevidenced decisive verdict(s), 1 would demote, 0 refused
# 1 would-demote = the out-of-scope experiment:a00-3c0140ac-dh45-fix (sibling
# goal:g7.31.2.2 chain), deliberately left to its own chain. NOT claimed as 0.

$ git diff --numstat -- extensions/agi/bin/
(empty)

$ python3 -m pytest extensions/agi/tests/test_harness_template.py -q
52 passed in 7.53s
```

## Trap hit

`set testable_claim` and `replace body` on the same node in separate calls:
the body replace restored the OLD frontmatter value. The `set` had to be
re-issued **after** the `replace body` to stick. Re-measure after both.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Re-landed the five MUR residues that the parent re-measured open on base 4be44e272, despite DH.50 claiming closure at 4a8cdf187. All edits via write.py, 0 production lines; dry-run re-measured as exactly 1 out-of-scope would-demote, not the false 0 the previous round asserted.
<!-- THOUGHT:END -->

## Agent Notes
DH.66 residue re-land: parent-measured all five MUR mur-g7-31-2-3-dh-40-a5b82056a-lean2-3 residues OPEN on base 4be44e272 (DH.50's claimed edits at 4a8cdf187 were not on this base); re-landed all five by write.py-only node edits with 0 production lines and re-measured: self-id gone from a00-9fa7f4f5 evidence_runs, no 1,089,136/0d506080 literal in a00-bc25f6f9, testable_claim added to a00-a267ee09 and absent from links.py schema, one _KNOWN_HARNESS_IDS fragment in a00-cf0076c2, non-empty Hypothesis section in a00-9fa7f4f5; evidence_gate enforce --dry-run = exactly 1 would-demote (OOS experiment:a00-3c0140ac-dh45-fix, sibling goal:g7.31.2.2, left to its chain), 0 refused; git diff --numstat over extensions/agi/bin empty; test_harness_template.py 52 passed.
