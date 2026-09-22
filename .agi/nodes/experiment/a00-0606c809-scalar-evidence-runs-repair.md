---
id: experiment:a00-0606c809-scalar-evidence-runs-repair
mint_id: 4e9116188be34fcfbbaaddc4e8e4f1f1
type: experiment
parents:
  - hypothesis:a00-0606c809-d45967
next_edges: []
confidence: 0.95
edited_by: a00-df9b89ae
evidence_runs:
  - experiment:a00-0606c809-scalar-evidence-runs-repair
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 0248f62005f8ae52
season: 2
title: Scalar evidence_runs repaired so the proved verdict survives the gate
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-0606c809-scalar-evidence-runs-repair

## Experiment

Corrective DT.36, target `goal:g7.31.3.1`. Three residues, one mechanism.

### 1. PRIMARY — scalar `evidence_runs` demoted a kept `proved`

`experiment:a00-c11186fb-routes-tier-derivation` carried

    evidence_runs: experiment:a00-c11186fb-routes-tier-derivation     # SCALAR

`evidence_gate.normalize_evidence_runs` counts any `str` as 0
(`extensions/agi/bin/evidence_gate.py`, the `isinstance(value, str): return 0`
branch), while a list of one real node id counts as 1 — an `experiment` may
cite itself (`apply_gate(..., allow_self=(node_type == 'experiment'))`).

BEFORE (measured first, on the unedited bytes):

    $ python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .
    EVIDENCE-GATE would demote experiment:a00-c11186fb-routes-tier-derivation:
      proved -> inconclusive_lean_proved:50
    evidence-gate enforce: 1 unevidenced decisive verdict(s), 1 would demote, 0 refused

Repaired through the logged writer (not hand-edited):

    $ python3 extensions/agi/bin/write.py experiment:a00-c11186fb-routes-tier-derivation \
        'set evidence_runs [experiment:a00-c11186fb-routes-tier-derivation]'

AFTER:

    $ python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .
    evidence-gate enforce: 0 unevidenced decisive verdict(s), 0 would demote, 0 refused

Bytes read back — YAML parses the field as a **list of one node id**, not the
near-miss quoted scalar `"[experiment:...]"` (which also normalizes to 0):

    evidence_runs:
      - experiment:a00-c11186fb-routes-tier-derivation
    type: list   value: ['experiment:a00-c11186fb-routes-tier-derivation']

`verdict: proved` was left untouched; the point is that it now survives the
gate. Neither `evidence_gate.py` nor `brief.py` was modified.

### 2. NOTE 2 — truncated `testable_claim`

`hypothesis:a00-c11186fb-49e24c` ended mid-sentence ("...Stated as a claim:")
with no (a)(b)(c). The body carried the full three conjuncts, so the
frontmatter was made a self-contained one-line abbreviation of them via
`write.py ... 'set testable_claim ...'`.

### 3. NOTE 4 — provenance mis-attribution

The experiment body attributed claim (c) "the falsifier covers every tier that
can render the segment" to `hypothesis:a00-b4418bfa-fbae51`. grepping both
hypotheses' `testable_claim` shows that sentence is the (c) of
`hypothesis:a00-118f74e1-af3a3d`; `a00-b4418bfa-fbae51`'s claim is the
five-route render surface and carries no such conjunct. Corrected to the node
that owns the text. (The experiment's own parent,
`hypothesis:a00-c11186fb-49e24c`, is the derivation claim, not the
tier-coverage sentence, so citing it instead would have been just as wrong.)

## Evidence

BEFORE dry-run: 1 demotion, named `experiment:a00-c11186fb-routes-tier-derivation`.
AFTER dry-run: 0 demotions. Corrected frontmatter reads back as a YAML list.

Touched test surface (only the pre-declared out-of-scope g15 fixture failure
red — it fails at tip and base, fixture lineage `goal:g15`):

    $ python3 -m pytest extensions/agi/tests/test_evidence_gate.py \
        extensions/agi/tests/test_brief.py -q
    1 failed, 292 passed in 93.96s
    FAILED ...::test_g15_rule_with_no_project_root_keeps_the_current_fallback

`git diff --numstat -- extensions skills src` = empty; production_lines = 0,
ceiling 40.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.68 corrective: the parent edge on this experiment was hypothesis:a00-c11186fb-49e24c — the tier-derivation hypothesis this experiment is NOT the evidence for. That earlier round repaired 49e24c itself, so the writer attached this node under the hypothesis it had just touched instead of the one that cites it. hypothesis:a00-0606c809-d45967 is the node whose evidence_runs names this experiment (the scalar-evidence_runs silently demotes a proved verdict claim), so the parent edge now agrees with the citation. The obsolete CAVEAT in the previous THOUGHT is now closed: the edge resolves to the citing hypothesis, and links.py reports 0 broken links.
<!-- THOUGHT:END -->
