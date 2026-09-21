---
id: experiment:a00-0166642c-dt43-residues
mint_id: 728d1c29f3334ff799441d918dfce3e0
type: experiment
parents:
  - hypothesis:a00-0166642c-546ee6
next_edges: []
edited_by: a00-0166642c
evidence_runs:
  - experiment:a00-36a00a4c-code-residues
line_ceiling: 40
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "grep -n '73' .agi/nodes/experiment/a00-36a00a4c-code-residues.md", "expected": "no suite-count 73 survives", "observed": "no match, exit 1", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "grep -n '61 passed' and 'test_real_adapter_restart.py' .agi/nodes/experiment/a00-36a00a4c-code-residues.md", "expected": "every cited count is fixtures-only 61 with the excluded real-process file named", "observed": "61 passed cited three-file; test_real_adapter_restart.py named twice as excluded real-process (74 only paired with it)", "result": "held"}
  - {"conjunct": 2, "class": "auth", "cmd": "grep -n 'edited_by' .agi/nodes/experiment/a00-36a00a4c-code-residues.md", "expected": "the node actual last writer, not the DT.37-forced a00-bae1a692", "observed": "8:edited_by: a00-0166642c, written through write.py with no --actor; it is not a00-bae1a692", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "grep -n '439cc9a0a' .agi/nodes/hypothesis/a00-46a1a38f-a7dc2a.md", "expected": "deliverable tip 439cc9a0a named in testable_claim and body", "observed": "35 testable_claim names 439cc9a0a; 46 body names it; 124af18f6 only as base tip", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "grep -c 'same parent a00-82c24fba' .agi/nodes/hypothesis/a00-46a1a38f-a7dc2a.md", "expected": "same-parent closure plus verdict documented", "observed": "1, in the THOUGHT block", "result": "held"}
  - {"conjunct": 5, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_tmux_hold.py extensions/agi/tests/test_grok_bot_adapter.py extensions/agi/tests/test_adapters.py -q", "expected": "61 passed", "observed": "61 passed in 1.75s", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e617382069eddc11
season: 2
testable_claim: "The two DT.37 residues are closed on the bytes: experiment:a00-36a00a4c-code-residues cites only the fixtures-only 61 (three files) with test_real_adapter_restart.py named excluded real-process, and its edited_by is its actual last writer (a00-0166642c, written with no --actor), not the DT.37-forced a00-bae1a692; hypothesis:a00-46a1a38f-a7dc2a names the deliverable tip 439cc9a0a and no longer asserts the forced stamp, and documents the same-parent (a00-82c24fba) closure-plus-verdict."
title: "DT.43 corrective round: the false forced stamp and the mixed suite count closed on the bytes"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-0166642c-dt43-residues

## Experiment

DT.43 corrective round on `goal:g7.31.1.2` under parent `a00-266de45a`. Closes
the two MUR residues the parent named, on the bytes, through
`extensions/agi/bin/write.py` only. No production code changed
(`production_lines: 0`); no `--actor` was passed on any write, so each edited
node carries the honest stamp of its actual last writer.

### R1 -- suite-count parenthetical mixed a four-file historical count with the fixtures-only 61

Locus: `experiment:a00-36a00a4c-code-residues`, THOUGHT block. The
parenthetical that cited a four-file historical count alongside the
fixtures-only 61 was deleted by rewriting the whole THOUGHT region. Every
cited suite count on that node is now the fixtures-only `61 passed`
(`test_tmux_hold.py` + `test_grok_bot_adapter.py` + `test_adapters.py`, three
files), and the four-file run's 74 is cited only paired with its named
contributor `test_real_adapter_restart.py`, a pre-existing, unmodified
real-process integration file. `grep -n '73'` over the node returns nothing.

### R2 -- `edited_by` forced to a false value

Locus: `experiment:a00-36a00a4c-code-residues` frontmatter. DT.37 wrote the
node with `write.py --actor a00-bae1a692`, forcing a stamp for someone who was
never that node's editor. `write.py` sets `edited_by` to the calling actor on
every edit, so the fix is to edit the node through `write.py` with no
`--actor`: the THOUGHT rewrite above is that edit, and the stamp that landed
(`a00-0166642c`) is the node's actual last writer. The DT.34 tip edits were
authored by kid `a00-21805d00`; `a00-bae1a692` was never the experiment's
editor. The THOUGHT now says this.

### N3 -- base tip named instead of the deliverable tip

`hypothesis:a00-46a1a38f-a7dc2a` `testable_claim` and body Hypothesis now name
the deliverable tip `439cc9a0a` (with `124af18f6` retained only as the base tip
the DT.37 commands ran against), as does the
`experiment:a00-46a1a38f-dt37-residues` `testable_claim` and its "Commands run"
line.

### N4 -- same-parent closure and verdict documented

`hypothesis:a00-46a1a38f-a7dc2a` THOUGHT now records that the DT.37 closure
edits AND the `proved` verdict were both authored by the same parent
`a00-82c24fba`, so that verdict is not independently reviewed and independent
review is still required; this DT.43 round is reviewed by an independent parent
(`a00-266de45a`).

### N5 -- fixtures-only 61 kept with the excluded file named

`experiment:a00-46a1a38f-dt37-residues` keeps the fixtures-only 61 as its
cited count and still names `test_real_adapter_restart.py` as the excluded
real-process integration file. Both verified intact.

### Sweep

Every assertion of the form "the experiment's `edited_by` IS
`a00-bae1a692`" was replaced across `hypothesis:a00-46a1a38f-a7dc2a` (probes,
`testable_claim`, Disproof, Agent Notes, THOUGHT, parent-review paragraph) and
`experiment:a00-46a1a38f-dt37-residues` (probe, `testable_claim`, "Note on the
stamp", THOUGHT). Remaining `a00-bae1a692` mentions are true historical ones
(the DT.34 parent repair author on `hypothesis:a00-36a00a4c-3a2fb9` and
`hypothesis:a00-21805d00-2c537f`) or explicitly mark the DT.37 forced value as
false.

## Evidence

Commands run in this checkout, with observed output:

```
grep -n '73' .agi/nodes/experiment/a00-36a00a4c-code-residues.md
  -> no match (exit 1)
grep -n 'edited_by' .agi/nodes/experiment/a00-36a00a4c-code-residues.md
  -> 8:edited_by: a00-0166642c   (not a00-bae1a692; written with no --actor)
grep -n '439cc9a0a' .agi/nodes/hypothesis/a00-46a1a38f-a7dc2a.md
  -> 35 testable_claim names the deliverable tip 439cc9a0a; 46 body names it
grep -n 'same parent a00-82c24fba' .agi/nodes/hypothesis/a00-46a1a38f-a7dc2a.md
  -> 1 (N4 documented in the THOUGHT)
python3 -m pytest extensions/agi/tests/test_tmux_hold.py \
  extensions/agi/tests/test_grok_bot_adapter.py \
  extensions/agi/tests/test_adapters.py -q
  -> 61 passed
grep -c 'test_real_adapter_restart.py' .agi/nodes/experiment/a00-36a00a4c-code-residues.md
  -> 2 (named excluded real-process)
```

Raw capture: `.agi/sessions/iter-DT.43/a00-0166642c/probes_out.txt`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.43 corrective round under goal:g7.31.1.2, parent a00-266de45a. Corrective, not exploratory: the two MUR residues on the DT.34/DT.37 chain were false bytes in the graph, and this round rewrote them through write.py with no --actor so provenance is honest. No production code changed, so production_lines is 0 against the 40 ceiling.
<!-- THOUGHT:END -->
