---
id: hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused
mint_id: e9d875c2269d47568c54d49c2f0c8124
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: a00-7f86f36e
evidence_runs:
  - experiment:a00-84c9c98d-34018e
  - experiment:a00-1556127c-9fb395
  - experiment:a00-3e7b260e-2cce33
  - experiment:a00-879cb9e8-625883
  - experiment:a00-85c23976-f70650
  - experiment:a00-342e0860-956c66
scaffold_hash: fcaf2289ca35b7cc
season: 2
testable_claim: a frontmatter list not in node_writer shape is refused by name at load/links; the corrupted node is repaired
title: "A node frontmatter the sanctioned writer could not have produced is refused (assigned: director-engine)"
town: core
verdict: inconclusive_lean_proved:80
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
DH.656 PARENT REVIEW of kid a00-342e0860. The rule left the TEST HELPER and is in the load path.

(1) WHAT THE ORDER SAID, quoted: "1. C2 open in the production gate, 0 production lines -- cli.py:284 _load_frontmatter returns ok=True for `probes: one`; the shape gate is a test helper, not the load path".

(2) WHAT THE MACHINE ACTUALLY DOES. cli.py:341 `_load_frontmatter(text, root)` now refuses a declared-container value the sanctioned writer could not have written: `_off_shape_values` (cli.py:325) renders the whole block with `node_writer.render_frontmatter`, reads it back, and takes the required TYPE from the `fields:` block of `[<type>].md` via `_declared_types` (cli.py:289); a mismatch returns False with a defect NAMING the key. I re-ran the probe on the real graph root: `probes: one` -> ok=False naming probes; `probes: {a: 1}` -> ok=False; `probes: [one]`, `probes: []`, a bare `tags:` and `confidence: 1` -> ok=True; 4703 live nodes read, 95 refused. The repair path refuses rather than rebuilds (cli.py:461-467) and my tmp-graph run shows the file byte-identical after `_ensure_frontmatter` refuses.

(3) THE NEAR MISS. Two, both avoided by the kid and one nearly taken by ME. (a) A pure writer round-trip would have CERTIFIED `probes: one` -- `set probes one` renders and reads back perfectly -- so the whole claim would have been closed on a gate that cannot see it; the type had to come from the schema. (b) A reviewer's near miss, which cost me my first probe: I handed `_load_frontmatter` the REPO root instead of the GRAPH root, `root/context/schemas` did not exist, the broad `except Exception: return {}` swallowed the empty table, and the gate reported ok=True for the exact value the claim is about -- a clean falsification of the round, produced entirely by my own argument. cli.py:3403 says `_find_root()` is "the `.agi/` graph dir"; the fixture the kid's test uses and the root production hands it are DIFFERENT objects, and a probe that conflates them decides the round either way.

(4) DEVIATION. The claim reads "refused by name at load/links; the corrupted node is repaired" and this round closed only one conjunct on one side: `links.py:105 off_shape_keys` is still KEYS-only, and a value defect is now refused, never repaired. Both are named in the review, not fixed here: links.py is outside the round's FILE SCOPE, and refusal-instead-of-repair was a measured engine call, not a scope choice.

Verdict raised :70 -> :80, evidence_runs the kid's own run. The CEILING was breached (cli.py 78/3 net against a hard cap of 15; test_links 65/2 against 40) and the round is CUT on the overage: `rebrief_request` answered `cut` because a 40-line ceiling is not the parent's to grant. The two residues above and the uncommitted kid-owned edit to experiment:a00-85c23976-f70650 are named for the director's findings row.
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
