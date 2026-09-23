---
id: experiment:a00-fb190ecb-dh155-mur-verify
mint_id: 13d0d1523f244fc2aa7173f32494c273
type: experiment
parents:
  - hypothesis:a00-fb190ecb-1fe1ca
next_edges: []
edited_by: a00-fb190ecb
line_ceiling: 40
loop: goal:g7.31.2.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 886be88ff18073a0
season: 2
title: "DH.155 corrective: four MUR residues on goal:g7.31.2.2 closed — probes: list proven NOT inert via schema_registry (127->131)"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-fb190ecb-dh155-mur-verify

## Experiment

## Experiment

DH.155 corrective round on `goal:g7.31.2.2`: four MUR residues, text
corrections only, no production code and no schema change.

1. `experiment:a00-33653715-dh45-verify` — the conjunct-3 probe asserted the
   `probes: list` typing was "inert". It is not: through `schema_registry`
   the typing adds four `types:probes` errors on the live corpus. Probe result
   changed to `refused`; the Evidence fence and `## Result` were rewritten.
2. `hypothesis:a00-33653715-0d018f` — `## Result` and `## Agent Notes`
   rewritten from "all three residues closed" to partially closed (only
   residue 2 held); the title's "and inert" claim was removed.
3. `hypothesis:a00-3c0140ac-0fa4dd` — `## Result` and `## Agent Notes` no
   longer claim full closure; they name the committed predecessor
   `a00-afc164be`.
4. `hypothesis:a00-f4f7eb39-a27b6a` — `production_lines` corrected 2 -> 0
   (the two numstat lines are node markdown, not production code).

## Evidence

Probe script `registry_probe.py` and its output `registry_out.txt` live in this
session dir.

```
$ python3 .agi/sessions/iter-DH.155/a00-fb190ecb/registry_probe.py
BEFORE (schema as committed): total=127 by_schema={'hypothesis': 127} probes=0
AFTER  (+ probes: list in validation.types): total=131 by_schema={'hypothesis': 131} probes=4
    probes: ('a00-8ee9bdff-40419b.md', 'probes', 'expected list, got str')
    probes: ('a00-bfd0d94a-d67716.md', 'probes', 'expected list, got str')
    probes: ('a00-debf9c6e-a64baf.md', 'probes', 'expected list, got str')
    probes: ('lm-typesafe-replay-200.md', 'probes', 'expected list, got str')
```

The DH.45 parent's registry probe measured the same +4 at BEFORE 126 /
AFTER 130; this tip's corpus carries one more `required:testable_claim` node,
hence 127 / 131.

Grep evidence (rc=1 on the first two = no output):

```
$ grep -n "is inert" .agi/nodes/experiment/a00-33653715-dh45-verify.md
$ grep -n "all three residues closed\|All three residues closed\|and inert" \
    .agi/nodes/hypothesis/a00-33653715-0d018f.md \
    .agi/nodes/hypothesis/a00-3c0140ac-0fa4dd.md \
    .agi/nodes/hypothesis/a00-f4f7eb39-a27b6a.md
$ grep -n production_lines .agi/nodes/hypothesis/a00-f4f7eb39-a27b6a.md
22:production_lines: 0
```

Contrast: `links.py schema` never reads `validation.types` — it calls
`node_writer.required_fields` / `missing_required` only (links.py:394,402), so
it is blind to the exact rule the earlier round asked it to judge. Running it
on this worktree exceeded 300 s and was terminated (rc=124); the source lines
are cited instead.

The THOUGHT blocks on the three hypothesis nodes are unchanged, and the schema
file `.agi/context/schemas/[hypothesis].md` is unmodified (`git diff --numstat`
on it gives no output).

## Result

All four residues are corrected by edit/text only; no production line changed.
The load-bearing correction is residue 1: the `probes: list` typing is NOT
inert, and the reader that reported otherwise (`links.py schema`) is blind to
`validation.types`.
