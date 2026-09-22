---
id: experiment:a00-15a555b7-dt47-tip-verification
mint_id: 2cd7836b188945eab2e9b74b24b16ff1
type: experiment
parents:
  - hypothesis:a00-15a555b7-1a4e9d
next_edges: []
edited_by: a00-15a555b7
line_ceiling: 40
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "grep -n 'deliverable tip' .agi/nodes/hypothesis/a00-0166642c-546ee6.md .agi/nodes/experiment/a00-0166642c-dt43-residues.md", "expected": "every mention of a deliverable tip about hypothesis:a00-46a1a38f-a7dc2a names f3eef11ca; each 439cc9a0a mention is qualified as the DT.37 tip (or as the DT.43-time old fact)", "observed": "A :18 :24 :32 :51 :74 :82 and B :18 :26 :66 name f3eef11ca as the deliverable tip; the only 439cc9a0a mentions are qualified 'DT.37 tip' / 'DT.43 named ...; DT.47 re-pointed it' / 'retained only as the DT.37 tip'; no unqualified present-tense deliverable-tip-439cc9a0a survives", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "grep -n 'deliverable tip' <both files> | grep 439cc9a0a | grep -v 'DT.37 tip|DT.43 named|re-pointed'", "expected": "no match (no unqualified 439cc9a0a deliverable-tip statement)", "observed": "only hit is :72, which is the quoted MUR/instruction text (mur-g7-31-1-2-dt-37-439cc9a0a) and the generic phrase 'name the deliverable tip', not a claim about 439cc9a0a", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "grep -n '439cc9a0a|f3eef11ca' .agi/nodes/hypothesis/a00-46a1a38f-a7dc2a.md", "expected": ":35 testable_claim and :46 body name f3eef11ca as the deliverable tip; 439cc9a0a only as the DT.37 tip", "observed": ":35 testable_claim names the deliverable tip f3eef11ca; :46 body names f3eef11ca; 439cc9a0a survives at :47 and :68 only as the DT.37 tip", "result": "held"}
  - {"conjunct": 2, "class": "auth", "cmd": "git show 439cc9a0a:.agi/nodes/experiment/a00-36a00a4c-code-residues.md | grep edited_by; git show f3eef11ca:.agi/nodes/experiment/a00-36a00a4c-code-residues.md | grep edited_by", "expected": "439cc9a0a gives the DT.37-forced a00-bae1a692; f3eef11ca gives a00-0166642c -- the two-tip split is real", "observed": "8:edited_by: a00-bae1a692 (439cc9a0a); 8:edited_by: a00-0166642c (f3eef11ca)", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_tmux_hold.py extensions/agi/tests/test_grok_bot_adapter.py extensions/agi/tests/test_adapters.py -q", "expected": "61 passed (fixtures-only; no real-process file added)", "observed": "61 passed in 0.58s", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 extensions/agi/bin/links.py links", "expected": "0 broken", "observed": "links: 3864 resolved, 0 broken (18 retired payload(s), not damage)", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "git diff --numstat -- extensions/ skills/ src/", "expected": "no production path changed -> production_lines 0", "observed": "empty output (only .agi/nodes/*.md modified)", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "sed -n '105,106p' .agi/nodes/experiment/a00-0166642c-dt43-residues.md", "expected": "fenced evidence shows the new truth: :35 and :46 name f3eef11ca; 439cc9a0a only as the DT.37 tip", "observed": "grep -n '439cc9a0a' ... -> 35 and 46 name f3eef11ca; 439cc9a0a only as the DT.37 tip", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 1b8069c35448a3fc
season: 2
testable_claim: Every statement about hypothesis:a00-46a1a38f-a7dc2a deliverable tip in hypothesis:a00-0166642c-546ee6 and experiment:a00-0166642c-dt43-residues names f3eef11ca, with 439cc9a0a only as the DT.37 tip.
title: "DT.47 run: verification that the stale deliverable-tip residual is closed on both DT.43 records"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-15a555b7-dt47-tip-verification

## Experiment

The DT.43 stale-tip residual was closed on the bytes. Run 1 re-pointed
`hypothesis:a00-46a1a38f-a7dc2a`'s deliverable tip to `f3eef11ca` (with
`439cc9a0a` only as the DT.37 tip), leaving two DT.43 record nodes asserting
the old fact. This run rewrote, through `extensions/agi/bin/write.py` with no
```
grep -n 'deliverable tip' .agi/nodes/hypothesis/a00-0166642c-546ee6.md \
  .agi/nodes/experiment/a00-0166642c-dt43-residues.md
  -> every entry names f3eef11ca as the deliverable tip; each 439cc9a0a
     mention is qualified as the DT.37 tip / the DT.43-time old fact
git show 439cc9a0a:.agi/nodes/experiment/a00-36a00a4c-code-residues.md | sed -n '8p'
  -> edited_by: a00-bae1a692   (DT.37 forced)
git show f3eef11ca:.agi/nodes/experiment/a00-36a00a4c-code-residues.md | sed -n '8p'
  -> edited_by: a00-0166642c   (DT.43 honest)
python3 -m pytest extensions/agi/tests/test_tmux_hold.py \
  extensions/agi/tests/test_grok_bot_adapter.py \
  extensions/agi/tests/test_adapters.py -q
  -> 61 passed
python3 extensions/agi/bin/links.py links
  -> links: 3864 resolved, 0 broken
git diff --numstat -- extensions/ skills/ src/
  -> empty (production_lines 0)
```
`testable_claim`, body Hypothesis, the THOUGHT P5 sentence and Agent Notes;
in `experiment:a00-0166642c-dt43-residues` the `439cc9a0a` probe,
`testable_claim`, section N3 and the fenced evidence output. No production
code changed (`production_lines: 0`). Verification probes are recorded
machine-readably in `probes:`.

## Evidence

Raw output, screenshots, logs.
