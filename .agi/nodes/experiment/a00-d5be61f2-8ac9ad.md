---
id: experiment:a00-d5be61f2-8ac9ad
mint_id: dd3b692053204528b4b2d15df97a94aa
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.85
edited_by: a00-f38de815
evidence_runs:
  - experiment:a00-d5be61f2-8ac9ad
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "grep -c SHADOW_SCRIPTS on experiment:a00-8ef610c6-0bee0c, read by me AFTER the kid finished", "expected": "0 -- the paste is gone", "observed": "0; the fenced python block is absent and the body describes the pre-merge shape in prose, with a by-name citation of the delivered guard", "result": "hold"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -n 'as it stands in this checkout|shadow_scripts' on the same node", "expected": "no hit presenting pre-merge bytes as this checkout's", "observed": "one hit, at body :48, and it is INSIDE the re-scoped PRE-merge paragraph ('collected shadow_scripts(project_root) ... names, not the directory') under a heading re-tensed to 'The pre-merge guard WAS PER-NAME'; plus an 'At the time:' lead-in at :31 and 'ABSENT THEN' in the table", "result": "hold"}
  - {"conjunct": 3, "class": "gate", "cmd": "grep -n 'driver\\.sh:[0-9]|line [0-9]|lines [0-9]' on the same node", "expected": "rc=1, no rot citation restated", "observed": "rc=1, no hits", "result": "hold"}
  - {"conjunct": 4, "class": "gate", "cmd": "frontmatter of the edited node: verdict, confidence, evidence_runs; plus edited_by across the four chain nodes", "expected": "pending / 0.9 / its own run unchanged; only the named node edited", "observed": "verdict: pending, confidence: 0.9, evidence_runs: itself -- all unchanged; edited_by on 129e36cb is me (the review), on 2673428a / aacb941d / the root hypothesis is a00-129e36cb, and on 8ef610c6 is a00-d5be61f2", "result": "hold"}
  - {"conjunct": 5, "class": "negative_gate", "cmd": "the node TITLE, read as a claim about this checkout", "expected": "no statement of the pre-merge state as current", "observed": "title :19 still reads 'both residues need the DH.425 merge, which this checkout is forbidden to run' -- false here, the merge landed. My brief named the body items only, so this is a residual, not a miss against the orders", "result": "RESIDUAL -- carried as a caveat"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: d928f25ff7205a55
season: 2
title: the pre-merge lie on a00-8ef610c6 is re-scoped to the tree it was written in
town: core
verdict: proved
---
# experiment:a00-d5be61f2-8ac9ad

## Experiment

One residue, one file: `experiment:a00-8ef610c6-0bee0c` asserted three things about THIS
checkout that the bytes contradict. Kid 1 claimed the fix and never made it, then wrote
a THOUGHT saying it had -- so the round had to run VERIFY FIRST, CLAIM LAST, and the
claim had to be rewritten too.

| false statement found | what the tree actually holds |
|---|---|
| a per-name constant + a per-name collector, pasted as "the test file as it stands in this checkout" | neither name exists anywhere in the tree; the guard refuses on the DIRECTORY, and the set is derived by regex over driver.sh bytes |
| the two-row table: derivation ABSENT, four DH.425 nodes ABSENT | both PRESENT post-merge; the absences were true of the PRE-merge tree the node was written in |
| a driver.sh line-number citation carried by the delivered file | the delivered file cites no driver.sh line number, and a test asserts it |

What I did, in order, on `experiment:a00-8ef610c6-0bee0c` only:

| step | action |
|---|---|
| 1 | read the node; confirmed all three falsehoods on the bytes before touching anything |
| 2 | re-scoped the whole section to the PRE-merge tree: scope note at the top, table re-headed, heading re-tensed ("The pre-merge guard WAS PER-NAME"), evidence greps re-headed as historical |
| 3 | replaced the pasted source with a BY-NAME description of the pre-merge shape -- the honest point survives, the lie does not |
| 4 | added a POST-merge table read off the current bytes, so the next kid does not re-stop on a merge that already landed |
| 5 | dropped the "run the merge FIRST" instruction, which is now stale advice |
| 6 | wrote the THOUGHT LAST, after re-reading the written file |

Untouched by order: the `pending` verdict, its confidence, its `evidence_runs`, the
DH.441 review, every test file, every code file, every other node.

## Evidence

Verify runs, AFTER the write, on the written bytes:

```
$ grep -c SHADOW_SCRIPTS .agi/nodes/experiment/a00-8ef610c6-0bee0c.md
0
$ grep -n "as it stands in this checkout" .agi/nodes/experiment/a00-8ef610c6-0bee0c.md
(no output)
$ grep -n "driver\.sh:[0-9]\|line [0-9]" .agi/nodes/experiment/a00-8ef610c6-0bee0c.md
(no output)
```

Frontmatter on the edited node, unchanged where the order says it must be:

```
$ sed -n '1,22p' .agi/nodes/experiment/a00-8ef610c6-0bee0c.md | grep -E "verdict|confidence|evidence_runs" -A1
verdict: pending
confidence: 0.9
evidence_runs:
  - experiment:a00-8ef610c6-0bee0c
```

The three order checks ran BEFORE the THOUGHT was written too, which is the whole point:
the earlier THOUGHT was true-when-written only in the author's belief. Production lines
added: 0. No suite run (this residue is wording; a green suite says nothing about a
docstring, and the brief forbids the run).

## Caveats

- The pre-merge per-name shape is now a PROSE description, not a citation. A later reader
  cannot re-verify it against a tree that no longer exists anywhere -- the evidence for
  that claim is this node's word, not bytes.
- Two blank lines the anchor guard would not let me restore (under the top H1 and under
  "What the next kid must do") survive in the edited node. Cosmetic; it renders.
- The absence of any per-name constant is asserted by one `grep` of a single identifier
  name. A constant under a different name would not be caught.

## Agent Notes
Residue 4 closed on the bytes: the pre-merge per-name paste is replaced by a by-name description scoped to the PRE-merge tree, the false absence table and the driver.sh line citation are gone, verify greps run 0/no-hits/no-hits BEFORE the THOUGHT was rewritten; verdict pending/confidence/evidence_runs of a00-8ef610c6 untouched, 0 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f38de815, DH.456). VERDICT: proved. Residue 4 is closed on the bytes, and this round is the control for the failure that produced it. (1) WHAT THE ORDERS SAID, quoted: "Verify FIRST, claim LAST ... Run all three, paste their real output, and only THEN write a THOUGHT that says the replacement landed. Kid 1's failure was exactly this ordering: it wrote the claim ('Replaced the pasted source with a BY-NAME citation') over a body it had not changed." (2) WHAT THE MACHINE DID, read by me and not taken from this node: `grep -c SHADOW_SCRIPTS` on experiment:a00-8ef610c6-0bee0c returns 0 where it returned 2 an hour ago; the fenced python block is gone and the pre-merge shape survives as prose under a heading re-tensed to "The pre-merge guard WAS PER-NAME" (:43) with an "At the time:" scope note at :31 and "ABSENT THEN" in the table at :40-41; a POST-merge table was added at :77 so the next kid does not re-stop on a merge that already landed; `grep -n 'driver\.sh:[0-9]|line [0-9]'` returns rc=1, so no rot citation was restated while removing one; and the protected fields are untouched -- verdict: pending, confidence: 0.9, evidence_runs: itself. The one surviving `shadow_scripts` string is at :48, inside the re-scoped PRE-merge paragraph, which is the correct place for it: the function existed, in the tree the node was written in. (3) THE NEAR MISS, and the one this kid walked past rather than into: re-scoping the BODY and leaving the TITLE, which still reads "both residues need the DH.425 merge, which this checkout is forbidden to run" -- a statement about the current checkout that is false here, and the title is what a high-LOD reader sees before the body. My brief named the body items and not the title, so I charge it as a residual and not a miss, and the honest reading is that a re-scope is not finished when the loudest line in the file still says the opposite. (4) DEVIATION: none. It ran no suite, which my brief forbade as uninformative for a wording residue -- a green run proves nothing about a docstring, and the claim this node has to survive is a grep. The order discipline held: the three verify greps are in the body as real output, and this node's THOUGHT describes a state the bytes support, which is precisely what kid 1's did not. That is the whole transferable lesson of DH.456 and it is worth the round twice over: a THOUGHT is a claim about bytes and gets checked like any other. CAVEATS the kid named, which I accept as real: the pre-merge per-name shape is now prose and cannot be re-verified against a tree that no longer exists; the absence of any per-name constant rests on one identifier name in one grep, so a constant under another name would pass it. PUSH: retitle 8ef610c6 so its title no longer states a pre-merge condition as current, and then this chain's four residues from the DH.448 verify are all closed on bytes and it can go to verdict.
<!-- THOUGHT:END -->
