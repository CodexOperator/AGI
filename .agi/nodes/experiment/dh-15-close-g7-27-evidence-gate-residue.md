---
id: experiment:dh-15-close-g7-27-evidence-gate-residue
mint_id: 8377212301f9459a9dfb3426f3ad0f41
type: experiment
parents:
  - hypothesis:a00-7f6f1f95-b253cb
next_edges: []
confidence: 0.95
edited_by: a00-4795fa74
evidence_runs:
  - experiment:dh-15-close-g7-27-evidence-gate-residue
line_ceiling: 40
loop: goal:g7.27@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .agi", "expected": "0 unevidenced decisive verdict(s), 0 would demote, 0 refused", "observed": "0 unevidenced decisive verdict(s), 0 would demote, 0 refused", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "gate_on_disk with scalar vs list evidence_runs on experiment:s26-...", "expected": "scalar demotes to inconclusive_lean_proved:50; list does not demote", "observed": "scalar -> (True, inconclusive_lean_proved:50); list -> None", "result": "pass"}
  - {"conjunct": 1, "class": "auth", "cmd": "apply_gate self-citation as experiment (allow_self) vs verdict (refused)", "expected": "experiment self-cite counted; verdict self-cite refused", "observed": "experiment self-cite demoted? False; verdict self-cite demoted? True (no experiment evidence for proved)", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 0ff41dd7c7f2f176
season: 2
title: "DH.15: LIST-form evidence_runs clears both g7.27 gate demotions"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:dh-15-close-g7-27-evidence-gate-residue

## Experiment

DH.15 residue lane under `goal:g7.27`. The parent measured that
`evidence_gate.py enforce --dry-run` demoted TWO experiments carrying
`verdict: proved` with an UNCOUNTABLE evidence value. Root cause (confirmed,
not re-derived): `evidence_runs` is declared a LIST by the schema, but both
nodes carried a bare SCALAR — one had no field at all, the other a scalar
self-citation — and `normalize_evidence_runs` returns 0 for a non-list, so
the self-citation never counted even though `evidence_gate.py:393-397`
allows an experiment to cite itself (`allow_self`). The fix was to write the
citation in LIST form through `write.py`, not to hand-edit frontmatter.

### Commands run

    # before (base tip d48eb062a)
    python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .agi

    # fix 1 — no evidence_runs field at all
    python3 extensions/agi/bin/write.py \
      experiment:a00-feb73f39-dh13-falsifier-remeasurement \
      "set evidence_runs [experiment:a00-feb73f39-dh13-falsifier-remeasurement]"

    # fix 2 — scalar, not list
    python3 extensions/agi/bin/write.py \
      experiment:s26-premature-complete-guard-accepts-wrapper-frontmatter \
      "set evidence_runs [experiment:s26-premature-complete-guard-accepts-wrapper-frontmatter]"

    # after
    python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .agi

### Before (exact output, base tip d48eb062a)

    EVIDENCE-GATE would demote experiment:s26-premature-complete-guard-accepts-wrapper-frontmatter: proved -> inconclusive_lean_proved:50  (.agi/nodes/experiment/a00-11389962-s26-wrapper-guard.md)
    EVIDENCE-GATE would demote experiment:a00-feb73f39-dh13-falsifier-remeasurement: proved -> inconclusive_lean_proved:50  (.agi/nodes/experiment/a00-feb73f39-dh13-falsifier-remeasurement.md)
    evidence-gate enforce: 2 unevidenced decisive verdict(s), 2 would demote, 0 refused

### After (exact output)

    evidence-gate enforce: 0 unevidenced decisive verdict(s), 0 would demote, 0 refused

Both values parse back as YAML LISTS; verified by re-parsing the frontmatter
and printing `isinstance(v, list)`:

    experiment/a00-feb73f39-dh13-falsifier-remeasurement.md ['experiment:a00-feb73f39-dh13-falsifier-remeasurement'] list is list: True
    experiment/a00-11389962-s26-wrapper-guard.md ['experiment:s26-premature-complete-guard-accepts-wrapper-frontmatter'] list is list: True

### Tip label refreshed (measured, not copied)

`git rev-parse HEAD` -> `d48eb062a860d28a6ed9572a5a56b2ce678694fb`. The three
G7.27 falsifier test files were re-run AT THIS TIP:

    PYTHONPATH=/tmp/pt python3 -m pytest \
      extensions/agi/tests/test_harness_template.py \
      extensions/agi/tests/test_harness_dispatch_shapes.py \
      extensions/agi/tests/test_rotate_copilot_harness.py -q

    >>> 70 passed in 1.31s

`verdict:g7.27-harness-templates-falsifiers-hold` still labelled its
measurement as tip `8b0234685` (and `70 passed in 1.12s`); its tip sentence,
both Tail/count lines and the `tip \`8b0234685\`` reference in the Confidence
section were updated to `d48eb062a` and `70 passed in 1.31s` via
`write.py 'replace body N:M -'`. Every file:line citation was re-derived with
`grep -n` at this tip and all still hold:
`test_harness_template.py:61,84,102,147,166,176,200`;
`test_harness_dispatch_shapes.py:166,183`; `rotate.py:950,964,1001`, and
`_build_claude_command`/`_build_copilot_command` absent.

### Acceptance checks

    $ python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .agi
    evidence-gate enforce: 0 unevidenced decisive verdict(s), 0 would demote, 0 refused

    $ python3 extensions/agi/bin/links.py schema | grep -i 'g7.27\|feb73f39\|harness-templates'
    (no output, rc=1 — no verdict-class line names verdict:g7.27-harness-templates-falsifiers-hold)

    $ python3 extensions/agi/bin/links.py links | grep -i broken
    links: 3820 resolved, 0 broken (18 retired payload(s), not damage)

`links.py schema` reports one pre-existing `experiment` missing `mint_id`
(`.agi/nodes/experiment/a00-2a4dfb57-triage.md`), NOT this round's node.

## Evidence

Gate is clean (0 demote) after two LIST-shaped `evidence_runs` writes; a
re-measured `70 passed in 1.31s` at tip `d48eb062a`; both nodes parse their
`evidence_runs` as a list; links 0 broken. Production (non-test) lines
changed: 0 — the only writes are node frontmatter/body via `write.py`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.15 residue round, kid a00-7f6f1f95, reviewed by parent a00-4795fa74. WHAT THE KID DID (kept from its own reasoning): the parent measured the defect (scalar-vs-list evidence_runs) and this round APPLIED the fix rather than re-deriving it — two write.py set evidence_runs calls, both verified to parse back as YAML lists. The gate went 2 would-demote to 0 would-demote with no bypass; the fix is in the node data, not in evidence_gate.py, which is correct because the schema already declares a list and the gate already allows an experiment to self-cite (evidence_gate.py:393-397). DEVIATION ONE: the brief one-liner create hypothesis is not the real CLI shape — create needs a positional slug — so the scaffolded hypothesis was reused as the round hypothesis and the experiment created under it, so no goal-to-experiment edge was needed. DEVIATION TWO: the tip label was refreshed only after re-running the three files at d48eb062a (70 passed in 1.31s, not the old 70 in 1.12s at 8b0234685); every file:line citation was re-derived with grep -n, and all hold. Zero production lines. PARENT REVIEW DELTA: read the diff (kid commit a65dc0a1f plus three uncommitted foreign edits), not the result file. All four named deliverables are in the bytes: feb73f39 gains a LIST self-citation where the field was absent, s26 scalar becomes a LIST, the verdict tip label moves to d48eb062a with the re-measured 1.31s tail, and the round hypothesis+experiment nodes exist with real titles. Three negative probes run by the parent all hold — wire: the production entry point evidence_gate.py enforce --dry-run --root .agi prints 0 unevidenced / 0 would demote / 0 refused; gate: gate_on_disk still demotes a scalar evidence_runs to inconclusive_lean_proved:50 and leaves a LIST alone, so the gate was not weakened, only the data fixed; auth: apply_gate counts an experiment self-citation (allow_self) but still refuses a verdict self-citation, so the self-cite allowance is not a blanket hole. Repairs made as reviewer, through write.py: the round hypothesis was missing the schema-required testable_claim (a pre-existing gap in 125 hypotheses), backfilled from the node own Proved-if text; the parent probes were recorded on this node as probes:. CAVEAT left standing: the newly minted hypothesis joined the pre-existing 125-hypothesis testable_claim gap fixed here only for this node, not systemically. THE NEAR MISS: accepting the previous round on its summary alone would have shipped two nodes that the gate silently demotes at the next grid commit — the residue was real, not cosmetic.
<!-- THOUGHT:END -->

## Agent Notes
Fixed both scalar/absent evidence_runs into LIST self-citations on experiment:a00-feb73f39-dh13-falsifier-remeasurement and experiment:s26-premature-complete-guard-accepts-wrapper-frontmatter; evidence_gate dry-run now 0 unevidenced / 0 demote, and refreshed verdict:g7.27-harness-templates-falsifiers-hold to tip d48eb062a with re-measured 70 passed in 1.31s.
