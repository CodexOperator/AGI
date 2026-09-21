---
id: experiment:a00-1ea8c652-dh16-verdict-cites-measuring-node
mint_id: f2dbaeb945a8446d9a9452a3038361a2
type: experiment
parents:
  - hypothesis:a00-1ea8c652-91eca1
next_edges: []
confidence: 0.95
edited_by: a00-c173f33b
evidence_runs:
  - experiment:a00-1ea8c652-dh16-verdict-cites-measuring-node
line_ceiling: 40
loop: goal:g7.27@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "read raw frontmatter of verdict:g7.27-harness-templates-falsifiers-hold + normalize_evidence_runs(build_corpus)", "expected": "evidence_runs parses back as a YAML list of 3 ids and each resolves in the corpus", "observed": "raw type list, is_list=True; entries=the 3 ids; counted (resolvable, non-self)=3", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "apply_gate(proved, pre/post evidence_runs, corpus=nodes, node_type=verdict)", "expected": "PRE-fix list counts 2 and passes (the gate cannot see this provenance defect); POST-fix counts 3 and passes", "observed": "PRE-fix counted=2 demoted=False ok=True; POST-fix counted=3 demoted=False ok=True", "result": "pass"}
  - {"conjunct": 2, "class": "source", "cmd": "grep -n d48eb062a|1.31s on experiment:a00-feb73f39-dh13-falsifier-remeasurement", "expected": "no d48eb062a/1.31s in that node (it pins 8b0234685/1.12s), so the corrected attribution to experiment:dh-15-close-g7-27-evidence-gate-residue is true", "observed": "only 8b0234685 / 1.12s present; the d48eb062a / 1.31s run lives in experiment:dh-15-close-g7-27-evidence-gate-residue", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "read raw frontmatter of verdict:g7.27-harness-templates-falsifiers-hold; build_corpus(.agi/nodes); normalize_evidence_runs(raw, self_id=verdict id, allow_self=False)", "expected": "evidence_runs is a LIST equal to the 3 expected ids, all 3 resolve in the corpus, counted==3", "observed": "is_list=True; equal expected=True; resolvable 3/3; counted=3", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "apply_gate('proved', <scalar evidence_runs>); apply_gate('proved', ['experiment:does-not-exist-0000']); apply_gate('proved', <post-fix 3-id list>)", "expected": "scalar -> demoted inconclusive_lean_proved:50; nonexistent -> demoted; post-fix list -> NOT demoted", "observed": "scalar demoted=True runs=0; nonexistent demoted=True runs=0; post-fix demoted=False runs=3", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "apply_gate('proved', [verdict-id], self_id=verdict-id, node_type=verdict) vs apply_gate('proved', [experiment id], self_id=that id, node_type=experiment)", "expected": "verdict self-cite refused/demoted; experiment self-cite allowed, not demoted", "observed": "verdict self-cite demoted=True runs=0; experiment self-cite demoted=False runs=1", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: edbdcfe048ffc3d8
season: 2
title: "DH.16: append the measuring experiment to the g7.27 verdict evidence_runs"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1ea8c652-dh16-verdict-cites-measuring-node

## Experiment

DH.16 residue lane under `goal:g7.27`. The DH.15 MUR
(`mur-g7-27-dh-15-evidence-gate-71b38fcc0`, `accept_with_residue`) left one
provenance defect: `verdict:g7.27-harness-templates-falsifiers-hold` claimed in
its body a re-measurement at tip `d48eb062a` with tail `70 passed in 1.31s`,
but its `evidence_runs` LIST named only
`hypothesis:harness-arg-builders-are-templates-only` and
`experiment:a00-feb73f39-dh13-falsifier-remeasurement` — the latter still pins
the OLDER tip `8b0234685` / `1.12s`. The node that actually measured
`d48eb062a` is `experiment:dh-15-close-g7-27-evidence-gate-residue`. So the
verdict's tip/count claim was unreachable through its own evidence list — a
provenance defect the gate could not see, because the remaining cites still
resolved.

### Primary fix — the measuring node joins the LIST

Before (raw frontmatter,
`.agi/nodes/verdict/g7.27-harness-templates-falsifiers-hold.md`):

    evidence_runs:
      - hypothesis:harness-arg-builders-are-templates-only
      - experiment:a00-feb73f39-dh13-falsifier-remeasurement

Fix, through the sanctioned writer (no hand edit):

    python3 extensions/agi/bin/write.py verdict:g7.27-harness-templates-falsifiers-hold \
      "set evidence_runs [hypothesis:harness-arg-builders-are-templates-only, experiment:a00-feb73f39-dh13-falsifier-remeasurement, experiment:dh-15-close-g7-27-evidence-gate-residue]"

After:

    evidence_runs:
      - hypothesis:harness-arg-builders-are-templates-only
      - experiment:a00-feb73f39-dh13-falsifier-remeasurement
      - experiment:dh-15-close-g7-27-evidence-gate-residue

### Secondary fix — the mis-attributed prose

`hypothesis:a00-7f6f1f95-b253cb` body said the `d48eb062a` re-measurement was
done by `experiment:a00-feb73f39-dh13-falsifier-remeasurement`; that node's
body still pins `8b0234685` / `1.12s` (`grep -n` hits at body lines 29, 45,
107, 113). Corrected via `replace body 24:26 -` to name
`experiment:dh-15-close-g7-27-evidence-gate-residue`.

## Evidence

Gate (exact output, current tree):

    $ python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .agi
    evidence-gate enforce: 0 unevidenced decisive verdict(s), 0 would demote, 0 refused

Links:

    $ python3 extensions/agi/bin/links.py links | grep -i broken
    links: 3821 resolved, 0 broken (18 retired payload(s), not damage)

Wire probe — the raw frontmatter parses back as a LIST and every cited id
resolves, so the count is 3 (not 2, not 0):

    raw value type: list is_list: True
    entries: ['hypothesis:harness-arg-builders-are-templates-only',
              'experiment:a00-feb73f39-dh13-falsifier-remeasurement',
              'experiment:dh-15-close-g7-27-evidence-gate-residue']
    counted (resolvable, non-self): 3

Gate probe — the gate is unchanged by this round and could NOT have caught the
provenance defect: handed the PRE-fix two-id list it counts 2 and does not
demote; handed the POST-fix list it counts 3. Both pass, which is exactly why
this is a provenance repair, not a gate-demotion repair.

Production (non-test) lines changed: 0 — node data only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.16 residue round, kid a00-1ea8c652, reviewed by parent a00-c173f33b. WHAT THE INSTRUCTION SAID (dispatch orders, verbatim): "add the measuring node to evidence_runs LIST via write.py ... Keep existing cites; do not drop feb73f39. Proof: evidence_gate.py enforce --dry-run --root .agi still 0/0/0; the verdict's tip claim is reachable via evidence_runs." WHAT THE MACHINE ACTUALLY DOES (bytes, not summary): the diff on verdict:g7.27-harness-templates-falsifiers-hold adds exactly one line, `  - experiment:dh-15-close-g7-27-evidence-gate-residue`, below the two kept cites, and changes edited_by to a00-1ea8c652; the diff on hypothesis:a00-7f6f1f95-b253cb rewrites the d48eb062a mis-attribution to name the DH.15 experiment; both new kid nodes exist with real titles and testable_claim. Parent probes (run by me, recorded on this node as probes 4-6) all pass: WIRE the raw frontmatter reparses as a 3-id LIST, all 3 ids resolve in build_corpus, normalize counts 3; GATE apply_gate still demotes a scalar and a non-existent id to inconclusive_lean_proved:50 and leaves the 3-id list alone; AUTH a verdict self-cite still demotes while an experiment self-cite is allowed -- the fix did not weaken the gate. Re-ran gate dry-run 0/0/0 and links 3822 resolved / 0 broken. THE NEAR MISS: three plausible implementations satisfy the words and lose the mechanism -- (a) hand-editing the node file instead of write.py, which moves the write outside the write log and defeats the review surface; (b) setting evidence_runs to a scalar or a list that does not reparse, which the DH.15 round already proved the gate counts as zero; (c) re-labelling the verdict tip d48eb062a -> f66e984c7 without re-running, a fabricated measurement. The kid did none of these. DEVIATION ACCEPTED: the kid left the tip label at d48eb062a (the historical pre-fold tip) because it did not re-run; refreshing without a run would be fabrication, so the honest choice is to keep the measured label and the newer tip is recorded in this round. Not done and not required this round: the note-only off-by-one cite (evidence_gate.py:393-397 vs :398) and the optional label refresh, both deferred by the dispatch orders. Verdict: ACCEPTED, kid claim proved, evidence_runs now reachable to its measurer.
<!-- THOUGHT:END -->
