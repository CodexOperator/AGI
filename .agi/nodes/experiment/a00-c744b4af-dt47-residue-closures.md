---
id: experiment:a00-c744b4af-dt47-residue-closures
mint_id: 1338c74e93c24152acb57508562d363d
type: experiment
parents:
  - hypothesis:a00-0166642c-546ee6
next_edges: []
edited_by: a00-c744b4af
line_ceiling: 40
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "grep -n 'write-log' .agi/nodes/hypothesis/a00-0166642c-546ee6.md", "expected": "no match on the node (R1)", "observed": "exit 1, no output", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "grep -n 'PROVENANCE_ACTOR\\] = actor\\|default=\"\")' extensions/agi/bin/write.py", "expected": "tip-visible no-actor stamp mechanism: 1932, 2455, 2272", "observed": "1932 set_fm[PROVENANCE_ACTOR] = actor or _default_actor(); 2455 --actor default \"\"; 2272 _default_actor()=AGI_ACTOR|USER|unknown", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "grep -n 'sessions/iter-\\|Raw capture' .agi/nodes/experiment/a00-0166642c-dt43-residues.md", "expected": "no match (R2 dangling session path deleted)", "observed": "exit 1, no output", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "grep -n '439cc9a0a\\|f3eef11ca' .agi/nodes/hypothesis/a00-46a1a38f-a7dc2a.md", "expected": "f3eef11ca is the deliverable tip; 439cc9a0a only as the DT.37 tip", "observed": ":35 testable_claim and :46-47 body name f3eef11ca; :68 names 439cc9a0a only as the DT.37 tip", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "git show f3eef11ca:.agi/nodes/experiment/a00-36a00a4c-code-residues.md | grep -n edited_by; git show 439cc9a0a:.agi/nodes/experiment/a00-36a00a4c-code-residues.md | grep -n edited_by", "expected": "f3eef11ca carries a00-0166642c; 439cc9a0a carries the DT.37-forced a00-bae1a692", "observed": "f3eef11ca:8 edited_by: a00-0166642c; 439cc9a0a:8 edited_by: a00-bae1a692", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_tmux_hold.py extensions/agi/tests/test_grok_bot_adapter.py extensions/agi/tests/test_adapters.py -q", "expected": "61 passed", "observed": "61 passed in 1.64s", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "python3 extensions/agi/bin/links.py links", "expected": "0 broken", "observed": "3862 resolved, 0 broken (18 retired payload(s), not damage)", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: c5d466c899804080
season: 2
testable_claim: "All three primary MUR residues on goal:g7.31.1.2 are closed on the deliverable tip f3eef11ca: (R1) hypothesis:a00-0166642c-546ee6 contains no session-log reference and its auth probe now cites the tip-visible write.py:1932/2455/2272 no-actor stamp mechanism; (R2) experiment:a00-0166642c-dt43-residues carries no dangling .agi/sessions/ raw-capture path; (R3) hypothesis:a00-46a1a38f-a7dc2a names f3eef11ca as the deliverable tip and 439cc9a0a only as the DT.37 tip; and the fixtures-only three-file suite yields 61 passed with 0 broken links."
title: "DT.47: three MUR residues closed on the f3eef11ca bytes (R1 session-log, R2 dangling capture, R3 tip naming)"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-c744b4af-dt47-residue-closures

## Experiment

DT.47 corrective round on goal:g7.31.1.2, parent a00-e5f2e8e3, under parent node
hypothesis:a00-0166642c-546ee6. Closes all three primary MUR residues from
mur-g7-31-1-2-dt-43-f3eef11ca-3 on the bytes, through
extensions/agi/bin/write.py only and with NO --actor, so each foreign node keeps
the honest stamp of its actual last writer. No production code changed
(production_lines: 0).

### R1 -- session-log evidence replaced by the tip-visible write.py mechanism

hypothesis:a00-0166642c-546ee6 no longer names .agi/sessions/write-log.jsonl
(gitignored and absent on the merged tip). Its auth probe and its THOUGHT P3
now cite the delivered mechanism: write.py:1932 sets edited_by to
`actor or _default_actor()`; write.py:2455 defaults --actor to ""; write.py:2272
returns AGI_ACTOR or USER or unknown. With no --actor the stamp is the process's
own actual writer, and an explicit --actor is the only way to force a different
one. grep write-log over the node returns nothing.

### R2 -- dangling session capture path deleted

experiment:a00-0166642c-dt43-residues no longer carries the Raw capture line
pointing at the gitignored .agi/sessions/iter-DT.43/... path. The fenced
commands and their observed outputs directly above are the tip-reachable
evidence.

### R3 -- deliverable tip named correctly

hypothesis:a00-46a1a38f-a7dc2a now names f3eef11ca as the deliverable tip (the
DT.43 corrections tip, where the experiment edited_by is a00-0166642c), and
names 439cc9a0a only as the DT.37 tip (where the experiment edited_by is the
DT.37-forced a00-bae1a692). 124af18f6 stays the base tip the DT.37 commands ran
against. The testable_claim, the body Hypothesis and the THOUGHT all agree.

## Evidence

Commands run in this checkout, with observed output:

```
grep -n 'write-log' .agi/nodes/hypothesis/a00-0166642c-546ee6.md   -> no match (exit 1)
grep -n 'sessions/iter-|Raw capture' .agi/nodes/experiment/a00-0166642c-dt43-residues.md -> no match (exit 1)
grep -n '439cc9a0a|f3eef11ca' .agi/nodes/hypothesis/a00-46a1a38f-a7dc2a.md
  -> :35 and :46-47 and :68 name f3eef11ca as deliverable tip; 439cc9a0a only as DT.37 tip
git show f3eef11ca:.agi/nodes/experiment/a00-36a00a4c-code-residues.md | grep edited_by
  -> 8:edited_by: a00-0166642c
git show 439cc9a0a:.agi/nodes/experiment/a00-36a00a4c-code-residues.md | grep edited_by
  -> 8:edited_by: a00-bae1a692
python3 -m pytest extensions/agi/tests/test_tmux_hold.py extensions/agi/tests/test_grok_bot_adapter.py extensions/agi/tests/test_adapters.py -q
  -> 61 passed in 1.64s
python3 extensions/agi/bin/links.py links
  -> 3862 resolved, 0 broken
```

## Agent Notes
Residual not in DT.47 scope: hypothesis:a00-0166642c-546ee6 (testable_claim and body Hypothesis) and experiment:a00-0166642c-dt43-residues (testable_claim) still name 439cc9a0a as the deliverable tip for hypothesis:a00-46a1a38f-a7dc2a; after the DT.47 R3 edit that node names f3eef11ca. The ordered R1/R3 scopes did not cover those lines, so this remains open for the next round.
