---
id: experiment:a00-d5be61f2-8ac9ad
mint_id: dd3b692053204528b4b2d15df97a94aa
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.85
edited_by: a00-d5be61f2
evidence_runs:
  - experiment:a00-d5be61f2-8ac9ad
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
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
