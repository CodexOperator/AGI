---
id: experiment:a00-f5692f23-b86b61
mint_id: 9bd87a57680b4ba1aed335d3cc9beaab
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.75
edited_by: a00-465d4567
evidence_runs:
  - experiment:a00-f5692f23-b86b61
  - experiment:a00-ef130285-1b046b
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": "residue 3a(1) -- the node carries a REAL title, not the derived `A00 ef130285 1b046b`", "class": "gate", "probe": "read the title cell and compare it to the derived slug; then grep the whole file for the string 'A00 ef130285' (a title left derived is harvested as untitled)", "expected": "a title in the kid's own words naming what the round did, and zero hits for the derived form", "observed": "title: 'DH.458 round moved the two live-bytes tests onto committed fixtures, declared each no-cascade drift per row, and kept the live comparison as a parent probe -- mechanism accepted, claim short of proved because its own falsifier was vacuous'; the derived form appears nowhere in the file", "result": "holds"}
  - {"conjunct": "residue 3a(2) -- the verdict matches the PARENT REVIEW (short of proved), not the round's later success", "class": "auth", "probe": "read verdict and confidence, and check them against the lean the parent actually holds after its own probes (test 7 was vacuous when this evidence was gathered; DH.463 closed that in a LATER round)", "expected": "inconclusive_lean_proved:75 with confidence 0.75 as a FRACTION, never proved and never 75 as the confidence", "observed": "verdict: inconclusive_lean_proved:75, confidence: 0.75 -- the percent in the verdict, the fraction in the confidence, which is the common error done in reverse. The THOUGHT names both residues and says the mechanism 'became real AFTER this node was written, which is exactly why proved would be a lie about the round that produced it'", "result": "holds"}
  - {"conjunct": "residue 3a(3) -- the THOUGHT carries the parse proof, with output the kid RAN, not output I dictated", "class": "wire", "probe": "read the THOUGHT block and re-run the parse command it quotes against the node on disk NOW", "expected": "the four-part shape (1) instruction / (2) machine cited to file:line / (3) near miss / (4) deviations, plus a command whose output I can reproduce", "observed": "the block has (1) WHAT THE ORDER SAID, (2) WHAT THE MACHINE NOW DOES citing test_boxkit_templates.py:356 / :243 / :253 / :409 and '24 manifest rows', (3) THE NEAR MISS I AVOIDED (setting proved on the strength of the DH.463 acceptance), (4) RULES I DEVIATED FROM: none. Its quoted command is the one from the brief and the output is list 5 ['class','conjunct','expected','observed','probe','result']; I re-ran it and got exactly that", "result": "holds"}
  - {"conjunct": "the kid touched nothing it was told not to touch -- the closed bytes, and the three fields that are not its own", "class": "gate", "probe": "find extensions -newermt '2026-09-27 00:40' (after kid 1 finished); re-run the suite; read the parent's probes list and rebrief_answer on the node; read .agi/sessions/write-log.jsonl for today's rows on this node and their ACTOR", "expected": "no engine file newer than the hand-off, the suite unchanged at 179 passed, the parent's five probes and the rebrief_answer still present, and every edit row under a00-f5692f23 (never a hand edit)", "observed": "find returned NOTHING under extensions; 179 passed in 1.30s; probes is still a 5-row list and rebrief_answer still carries the parent's cut; four update_node rows under actor a00-f5692f23 role kid, three under a00-465d4567 role parent. The kid's own claim 'I touched nothing under extensions/agi/**' is TRUE, checked against mtimes and not against its word", "result": "holds"}
production_lines: 30
profile: balanced
role: kid
scaffold_hash: a4ab84e08550d6ec
season: 2
title: "DH.463 residue 3a: rewrote the ef130285 record in place -- real title, verdict downgraded to inconclusive_lean_proved:75 because its own falsifier was vacuous, THOUGHT with the probes parse proof"
town: core
verdict: inconclusive_lean_proved:75
---
# experiment:a00-f5692f23-b86b61

## Experiment

RESIDUE 3a: the node ef130285 carried a DERIVED title and a verdict of proved for a
claim whose own falsifier was vacuous. This round edited that node in place, through
write.py only, and changed nothing else. No code was touched: the two live-bytes
residues were already closed in the bytes by a00-b04fa632, and a second hand on a
settled falsifier would re-open it.

```
before (ef130285)                         after
  title:  A00 ef130285 1b046b     -->    a real sentence naming the round
  verdict: proved                -->    inconclusive_lean_proved:75
  confidence: 0.85               -->    0.75
  THOUGHT: absent                -->    (1)(2)(3)(4) shape + parse proof
  probes / rebrief_* / review    UNCHANGED (parent-authored, read first)
```

## Evidence

```
$ python3 extensions/agi/bin/write.py experiment:a00-ef130285-1b046b 'set title ...'
updated: experiment:a00-ef130285-1b046b
$ ... 'set verdict inconclusive_lean_proved:75 && set confidence 0.75'
updated: experiment:a00-ef130285-1b046b
$ ... 'thought ...'   (twice; the second pass corrected one over-claimed clause)
updated: experiment:a00-ef130285-1b046b

$ python3 -c "... read_frontmatter(...); print(d['verdict'], d['confidence'])"
inconclusive_lean_proved:75 0.75
```

Parse proof for the parent-rewritten probes list, run here, not taken from the brief:

```
$ python3 -c "import importlib.util;spec=importlib.util.spec_from_file_location('fm','extensions/agi/bin/frontmatter.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);d=m.read_frontmatter(open('.agi/nodes/experiment/a00-ef130285-1b046b.md').read());print(type(d['probes']).__name__,len(d['probes']),sorted(d['probes'][0]))"
list 5 ['class', 'conjunct', 'expected', 'observed', 'probe', 'result']
```

## What this node claims

Only that the ef130285 record now tells the truth about its own round: the mechanism
was accepted, the claim it makes was not proved at the time it was written, and both
residues it left were named and closed in a later round. No test file was run, because
no test file was changed.
Raw output, screenshots, logs.

## Agent Notes
Residue 3a: ef130285 record rewritten in place via write.py -- real title, verdict proved -> inconclusive_lean_proved:75 (its falsifier was vacuous at the time it was written), THOUGHT in the (1)-(4) shape carrying the probes parse proof I re-ran (list 5). No code touched; 179 passed unchanged; production lines 30.

PARENT REVIEW (DH.463, a00-465d4567) -- ACCEPTED on four probes I ran myself (probes:). (1) WHAT THE INSTRUCTION SAID: 'experiment:a00-ef130285-1b046b: a real title (what it did); its verdict must match its parent review (the review says it stays short of proved -> set the verdict the review states, with the reason in THOUGHT)'. (2) WHAT THE MACHINE ACTUALLY DOES: the target node now reads verdict: inconclusive_lean_proved:75, confidence: 0.75, a real 200-char title, and a THOUGHT whose (2) cites test_boxkit_templates.py:356/:243/:253/:409 -- line numbers I confirmed against the file, and whose parse proof I re-ran and reproduced. (3) THE NEAR MISS: setting verdict: proved because the bytes are good NOW (DH.463 closed the vacuity in a later round) -- it satisfies 'the verdict must match the review' in letter and loses the reason, because it dates the proof to a round that did not exist when the evidence was gathered. The kid named that miss itself and refused it. (4) NO RULE DEVIATED. One weakness, in prose only: the title is 200+ characters, which is a full-sentence title rather than a title -- legible, but a reader scanning a node list pays for it. Not a reason to re-brief a round whose every other deliverable checks out.
