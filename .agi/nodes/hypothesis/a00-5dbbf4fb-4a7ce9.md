---
id: hypothesis:a00-5dbbf4fb-4a7ce9
mint_id: 79028c2ac15845a9bee922211bf8ce47
type: hypothesis
parents:
  - goal:g7.31.3.1
next_edges: []
confidence: 0.9
edited_by: a00-5dbbf4fb
evidence_runs:
  - experiment:a00-5dbbf4fb-dt87-residual-verify
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "git show HEAD:.agi/nodes/hypothesis/a00-f46503aa-25f7eb.md | grep -A2 evidence_runs; git ls-tree HEAD .agi/nodes/experiment/ | grep f46503aa", "expected": "evidence_runs names a committed experiment, not the hypothesis itself", "observed": "evidence_runs: experiment:a00-f46503aa-note-writers-under-heading; blob 11523d6 in HEAD", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_completion.py -q -k trailing_thought; python3 -m pytest extensions/agi/tests/test_cli.py -q -k trailing_thought; python3 -m pytest extensions/agi/tests/test_write.py -q -k \"inline_mention or before_a_trailing\"", "expected": "all four named tests pass at HEAD", "observed": "1 passed; 1 passed; 2 passed", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 extensions/agi/bin/links.py links; python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .; git diff --numstat -- extensions/agi/bin/brief.py", "expected": "0 broken; 0 demote 0 refused; empty brief.py diff", "observed": "3862 resolved 0 broken; 0 demote 0 refused; empty", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "for f in .agi/nodes/goal/g7.31.3.1.md .agi/nodes/hypothesis/a00-f0d769b5-7a5ace.md .agi/nodes/hypothesis/a00-f46503aa-25f7eb.md; do grep -c \"^## Agent Notes\" $f; done", "expected": "exactly one line-anchored heading per touched node", "observed": "1; 1; 1", "result": "held"}
profile: balanced
role: kid
scaffold_hash: 9b54407239381c6f
season: 2
testable_claim: "DT.87 residual closure on goal:g7.31.3.1 holds at HEAD 5f9f47bac: the self-citation is already replaced by a committed experiment, all three note writers call one line-anchored node_writer.merge_agent_notes, the four regression tests pass, brief.py is byte-unchanged, links 0 broken, gate 0 demote, and the still-dirty node files are what this round --owns lands."
title: A00 5dbbf4fb 4a7ce9
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-5dbbf4fb-4a7ce9

## Hypothesis

The DT.87 residual closure on `goal:g7.31.3.1` is real on the bytes at HEAD
`5f9f47bac`, and the dispatch brief's D1 is stale:

1. **D1 already closed.** `hypothesis:a00-f46503aa-25f7eb` no longer cites
   itself: its `evidence_runs` is `[experiment:a00-f46503aa-note-writers-under-heading]`,
   a real experiment committed in `5f9f47bac` whose body carries the run. Only
   the stale `demote_reason: no experiment evidence (evidence_runs=0) for
   'proved'` / `demoted_from: proved` pair survives in the committed
   frontmatter; the working tree drops it and this round's scoped commit lands
   the drop. So the brief's "create an experiment under that hypothesis" is
   already done and duplicating it would only inflate the graph.
2. **The engine seam holds.** All three writers —
   `cli.py:2066`, `post_wire.py:486`, `write.py:2317` — call one shared
   `node_writer.merge_agent_notes` (`node_writer.py:915`), which inserts the
   note after the line-anchored `## Agent Notes` LINE and never at end of
   body. `NOTES_HEADING` is declared once (`node_writer.py:912`) and aliased
   by the other three.
3. **The four regression tests pass at HEAD**, named
   `test_the_note_lands_under_the_heading_not_after_a_trailing_thought`,
   `test_done_places_the_note_before_a_trailing_thought_block`,
   `test_an_inline_mention_of_the_heading_is_not_a_section`,
   `test_a_note_lands_before_a_trailing_thought_block`.
4. **R1/R4/R5 hold**: the gitignored MUR-JSON cite is replaced by committed
   `88da0784c`, `brief.py` is byte-unchanged, `links.py` is 0 broken,
   `evidence_gate --dry-run` is 0 demote / 0 refused, and every touched node
   carries exactly one `## Agent Notes` heading.
5. **D2 is the live work**: `goal:g7.31.3.1`,
   `hypothesis:a00-f0d769b5-7a5ace`,
   `experiment:a00-f0d769b5-residual-close` and the stale
   `hypothesis:a00-f46503aa-25f7eb` are still dirty at dispatch; passing them
   in `cli.py done --owns` is what lands R1/R4/R5 in this round's commit.

**Disprove:** `evidence_runs` is self-referential or empty; any of the four
tests fails at HEAD; `brief.py` differs; a broken link appears; the gate
demotes; a touched node has != 1 `## Agent Notes` heading; or the residue
table claims a residue closed that is not.

## Evidence

`experiment:a00-5dbbf4fb-dt87-residual-verify` re-ran every command above on
this worktree and carries the verbatim output. Production lines = 0: this
round changes no production file (the DT.87 engine fix is already committed in
`7539f79d4`). The one open residue remains the DT.36 schema-list note,
deliberately OOS for this leaf; no global `residues=0` is claimed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The dispatch brief claimed D1 was open (self-citation) and asked me to mint an experiment under hypothesis:a00-f46503aa-25f7eb. Checking HEAD first showed the last kid had already created experiment:a00-f46503aa-note-writers-under-heading and pointed evidence_runs at it in 5f9f47bac, so minting a second one would inflate the graph for nothing. Instead this node is a verification hypothesis backed by its own re-run, and the live work is D2: all four dirty node files go into --owns. Production lines 0.
<!-- THOUGHT:END -->

## Agent Notes
DT.87 verification: the brief's D1 was stale — HEAD 5f9f47bac already carries experiment:a00-f46503aa-note-writers-under-heading and hypothesis:a00-f46503aa-25f7eb evidence_runs points at it, not itself. I re-ran the four named regression tests (all pass), links 3863/0 broken, evidence_gate 0 demote/0 refused, brief.py numstat empty, one Agent Notes heading per touched node, and landed D2 by passing all four dirty node files plus my two nodes in --owns.
