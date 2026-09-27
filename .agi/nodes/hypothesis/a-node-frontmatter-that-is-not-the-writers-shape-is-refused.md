---
id: hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused
mint_id: e9d875c2269d47568c54d49c2f0c8124
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: a00-7674caf6
scaffold_hash: fcaf2289ca35b7cc
season: 2
testable_claim: a frontmatter list not in node_writer shape is refused by name at load/links; the corrupted node is repaired
title: "A node frontmatter the sanctioned writer could not have produced is refused (assigned: director-engine)"
town: core
---
# hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused

# hypothesis: A node frontmatter the sanctioned writer could not have produced is refused (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
a00-fe05fdae :14-15 probes field destroyed by two raw hand-appended lines and every gate passed it: cli.py:270-296 _load_frontmatter only requires a mapping; node_writer.py:396-408 renders lists as `probes:` + `  - <scalar>` (PASS 10 c15)

## Testable claim
a frontmatter list not in node_writer shape is refused by name at load/links; the corrupted node is repaired

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version carries the DH.640 PARENT REVIEW of kid a00-85c23976 and the measurement the graph was missing.

(1) WHAT THE ORDER SAID, quoted: "3. ITEM 1 s settle evidence exists NOWHERE in the graph, and this is the round s largest act" and "run the one command that settles it and PASTE its output on your node (never type a number)".

(2) WHAT THE MACHINE ACTUALLY DOES.  I ran the settling command myself in this checkout, read-only: `git show --stat 47cb34e34 -- nopin | tail -1` prints " 582 files changed, 281158 deletions(-)", `git ls-tree -d --name-only 47cb34e34^ -- nopin` prints "nopin", and the same command on 47cb34e34 prints nothing.  The removal is a single commit, measured.  The order s own command, `git diff --stat 62ff98b23 HEAD -- nopin | tail -1`, is EMPTY in both checkouts -- base tip equals HEAD there -- so the item could only be settled by naming the earlier commit 47cb34e34.  That is the mechanism: the settling command was written against a base that is not where the work is.

(3) THE NEAR MISS.  A review that accepts the kid s pasted block as the measurement satisfies every word of the order and loses it -- paste is evidence only when the parent re-ran the command, because a kid can paste a plausible line that no command emits.  I re-ran it; the line is faithful.  The second near miss is in the code: a shape gate installed on the resolver s FALLBACK branch only.  The report says "the recovered-probes gate asks the writer for a list"; the machine has two exits and the named-artifact exit (test_links.py:614) still returns a node whose `probes` is a scalar, and `cli._load_frontmatter` still returns ok=True for that node.  Zero production lines moved this round, so the hypothesis claim -- a VALUE the writer could not have produced is refused at load/links -- is still open in the production gate.

(4) DEVIATION.  The contract says do not edit any other checkout; the kid ran with --branch so its node lives in a00-85c23976 only, and this review went to the hypothesis node instead of the kid s.  The property that makes the rule apply is that the kid s branch tip is the loop s merge unit and a hand edit there would land in the merge unowned.
<!-- THOUGHT:END -->

## Agent Notes
PARENT REVIEW DH.640 (a00-7674caf6) of kid a00-85c23976 / experiment:a00-85c23976-f70650 — DEMOTED proved -> inconclusive_lean_proved:70.

WHAT THE KID CLAIMED, quoted from its node: "proved"; "the gate asks the WRITER: render the value the way node_writer would and read it back"; ITEM 3 "MEASURED (pasted)".

WHAT THE MACHINE ACTUALLY DOES, from the diff (git diff 62ff98b23..8b0a08cb2, 3 files, 37 lines in test_links.py, 0 production lines) and artifacts I BUILT AND RAN (parent-probes-DH640.py, tmp graphs only, run against the kid branch):
  P1 GATE (fallback path):  scalar -> None, mapping -> None, list -> picked, [] -> picked, [1,2] -> picked, bare `probes:` -> None.  The fix HOLDS: truthiness is gone.
  P2 WIRE (the NAMED path):  the first branch `if named.is_file(): return named, "the named artifact"` at test_links.py:614 carries NO shape check at all.  A named artifact whose `probes:` is the SCALAR `one` is returned as the recovered artifact, and `cli._load_frontmatter` on that same node returns ok=True, defect=None, probes="one" — so the live pin that consumes it (assert fm["probes"] truthy, assert _off_shape_keys == []) PASSES on a corrupted named artifact.  The hypothesis claim is therefore NOT closed on the production side.
  P3 AUTH:  an off-shape key `probes=glued` riding a perfect list is refused by name — holds.
  P4 the shape helper itself:  ["one"]/[]/[1,2]/[True]/[{"a":1}]/["a: 1"] all True; "one"/{"a":1}/None all False.  No over- and no under-refusal in the helper.

ITEM 3 SETTLED INDEPENDENTLY by me, in my own checkout:  `git show --stat 47cb34e34 -- nopin | tail -1` -> " 582 files changed, 281158 deletions(-)"; `git ls-tree -d --name-only 47cb34e34^ -- nopin` -> nopin; same on 47cb34e34 -> empty.  The kid paste is faithful; the 582/281,158 figure is measured, not prose.  `git diff --stat 62ff98b23 HEAD -- nopin | tail -1` is empty in both checkouts (base tip == HEAD there), which is why the settling command had to name the earlier commit 47cb34e34.  The sibling claim "both commits are pathspec-scoped" stays UNVERIFIED and is named for the findings row.

THE NEAR MISS the kid fell into:  a shape gate applied to the FALLBACK branch only.  It satisfies every word of the report ("the recovered-probes gate asks the writer for a list") and loses the mechanism, because the resolver has two exits and only one of them asks.  The same near miss is what kept the defect alive: cli._load_frontmatter (cli.py:279-311) still certifies a scalar `probes` as ok — the whole hypothesis claim is about a VALUE the writer could not have produced, and no production byte moved this round.

DEVIATION:  the contract says "Do not edit any other checkout".  The kid ran with --branch, so experiment:a00-85c23976-f70650 exists only in /data/work/agi/.agi/worktrees/a00-85c23976 and this review could not be written into it through the sanctioned writer without breaking that rule.  It is recorded here, on the node that carries the round verdict, instead of in the kid node.

MERGE DEFECT, DH.640, named for the director findings row. cli.py done --owns refuses to land the kid branch with "owned kid branch season2/loops/hypothesis-a-node-frontmatter-th-a00-85c23976 (experiment:a00-85c23976-f70650) did not merge". The whole conflict is ONE line, measured with git merge-tree: both sanctioned writers stamped `edited_by` on this same node in the same round -- mine a00-7674caf6 (this review), the kid a00-85c23976 (its verdict). extensions/agi/tests/test_links.py merged CLEANLY (ort, result b0f9226) and the kid s new node file merges as an add; the hypothesis file is the only conflict, and the body (this review) and the frontmatter (evidence_runs + verdict) are disjoint hunks. The collision is structural: PROVENANCE_ACTOR is a single scalar (write.py:71), so a parent that reviews a node its kid also edited cannot land both through --owns, and resolving it would mean writing the kid s `edited_by` with my own hand -- a provenance lie, which is the same defect class as director ITEM 4. The director s own FILE SCOPE for this round handed the hypothesis node to the KID while the parent contract requires the parent to review in place; those two scopes overlap on exactly this file. Fix belongs in cli.py: a three-way merge of node FRONTMATTER that takes the later `edited_by` and the union of `evidence_runs`, instead of aborting the round.
