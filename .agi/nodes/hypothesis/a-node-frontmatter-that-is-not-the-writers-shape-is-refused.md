---
id: hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused
mint_id: e9d875c2269d47568c54d49c2f0c8124
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: director-engine
evidence_runs:
  - experiment:a00-84c9c98d-34018e
  - experiment:a00-1556127c-9fb395
  - experiment:a00-3e7b260e-2cce33
  - experiment:a00-879cb9e8-625883
  - experiment:a00-85c23976-f70650
  - experiment:a00-342e0860-956c66
  - experiment:a00-3e239d1d-9407b0
  - experiment:a00-7a12aad2-6a3a17
scaffold_hash: fcaf2289ca35b7cc
season: 2
testable_claim: a frontmatter list not in node_writer shape is refused by name at load/links; the corrupted node is repaired
title: "A node frontmatter the sanctioned writer could not have produced is refused (assigned: director-engine)"
town: core
verdict: inconclusive_lean_proved:75
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
PARENT, EG.133, a00-98a14a87 -- this block is REWRITTEN WHOLE, carrying ONE round's delta (the rule AGENTS.md quotes from G2.11: body is state, thought is delta, rewritten whole). The previous block carried two: the EG.28 header (a00-7a69e3ca) plus a COUNT CORRECTION paragraph accreted under it at :51. What that shape traded away: a THOUGHT that is append-only in practice, so every later round reads a delta written against a version of the node that no longer exists, and a reader cannot tell which sentences this node believes from which a prior round believed on its behalf. The count record itself is NOT lost -- the wrong counts and their four measured replacements live in the Agent Notes paragraph of this node, which is body, which is state.

(1) WHAT THE INSTRUCTION SAID, quoted: "3. The THOUGHT was appended to, not rewritten whole ... against the G2.11 rule quoted in AGENTS.md ('body is state, thought is delta ... rewritten whole'). The round declared the method ('counts corrected in place; old counts kept in quotes as the record') but did not name the convention it traded away". And item 2, on the number: "The falsified ground of a standing demotion was recorded but the number was left ... The hypothesis then lists that demoted node as evidence (hypothesis:17) while its own verdict sits at :23 ... 'verdict is the number a later reader reads first'. Parent action, not a demote of this round."

(2) WHAT THE MACHINE ACTUALLY DOES. Item 2 is fixed in the bytes: experiment:a00-7a12aad2-6a3a17.md now reads `verdict: inconclusive_lean_proved:80` (was `inconclusive_lean_disproved:65`) with `confidence: 0.8`, written through write.py. The demotion's sole stated ground was its probes[2] P3 -- the corrected bytes of a00-3e239d1d-9407b0.md sitting uncommitted in the working tree. That ground is false of the bytes on disk today: a00-3e239d1d-9407b0.md:16 carries the CORRECTION to P2 (the false "ap=None, where a rebuild was never possible" reason) and :20 carries the CORRECTED NUMBER for P4b, and this node's body records the falsification against the parent's own done commit 850091463. The delivery fault closed; a verdict demoted for a delivery fault and never re-judged is the drift the order names as fatal, so the number moves back. The number on THIS node does not move: still :75, because nothing this round touched a production byte.

Item 1 is SETTLED, not fixed, and the settling measurement is the whole last line of the file the counts came from, run by me today: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_links.py -q --basetemp=/tmp/eg133-parent-links` -> "36 passed, 9 warnings in 0.30s". There is no `skipped` token on that line at all -- the file collects no skips -- so a summary of a test_links.py run on these bytes has nothing to omit, and the order's `1 skipped` cannot belong to those lines. The only published summaries that DO carry a skipped count carry it: a00-16a744c6-447f40.md:62 and a00-7a12aad2-6a3a17.md:152 both read "1 failed, 72 passed, 6 skipped" and ":152" also "1 failed, 108 passed, 6 skipped". Item 1 is therefore refuted by the bytes for every line this chain publishes, and the node text is left as it stands rather than edited to match a count that does not exist.

Item 4 is RECORDED, NO ACTION (g7.33.19 row 13): this chain's deliverable did not ride its done commit -- the 850091463 message names experiment:a00-1556127c-9fb395 while the EG.44 parent verdict actually lives on a00-7a12aad2-6a3a17. History is not rewritten and nothing is re-landed; it is named here once.

(3) THE NEAR MISS. One, and this round did not take it: fixing item 1 by editing a `1 skipped` into a published line -- that would satisfy the order's words and lose the mechanism, because the count is a property of what pytest collected, not a property of the sentence; a typed-in skip count is prose wearing a measurement's clothes. The re-judge of a00-7a12aad2 to inconclusive_lean_proved:80 is NOT a near miss: it is the action this round TOOK (item 2, in (2) above). Where the number stops: this claim is "refused by name at load/links; the corrupted node is repaired", and a fourth round has MEASURED the links half to be keys-only rather than assumed it -- :80, not higher, is the verdict those conjuncts carry. (Director close, TMM.327, mur-eg-x552735-fc285a EG.133-k1: an earlier wording listed the taken re-judge as a declined near miss.)

(4) DEVIATION. The order's item 2 said "Parent action, not a demote of this round", and the one-kid ceiling meant the corrective items 1 and 3 had a single kid slot that this round's kid spent on a measurement instead. I fixed items 1, 3 and 4 on this node myself through the sanctioned writer rather than re-dispatching: the work is text, the cap is one kid, and a re-brief for text I can write in one call costs a round to no end. That is a property of THIS case -- the residue is prose on the target node, not a mechanism anywhere -- and not a general licence for a parent to do a kid's work.
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

THIS ROUND'S NET MOVEMENT ON THE CLAIM, from the corrective kid experiment:a00-3e239d1d-9407b0 (its diff, and my own re-run of its deletions): the load-path half is no longer deletable-with-no-red -- deleting the no-rebuild guard turns test_links.py red, deleting only the writer round-trip clause turns it red -- and the fail-open multi-root cache is closed and my probe discriminates old bytes from new. COUNT CORRECTED by experiment:a00-7a12aad2-6a3a17 (EG.44): the counts written here before that correction, '1 failed, 33 passed' and '2 failed, 32 passed', do NOT reproduce on tip 2d5c5a81c. Re-measured on a clean /tmp copy of that tip, test_links.py only: guard deleted -> 1 failed, 34 passed (test_an_off_shape_value_is_REFUSED_and_the_file_is_left_alone, 'AssertionError: frontmatter repaired'); round-trip CLAUSE deleted -> 1 failed, 34 passed (test_the_writer_ROUND_TRIP_is_load_bearing_not_just_the_declared_type); round-trip COMPUTATION deleted -> 1 failed, 34 passed (the pre-existing test_a_declared_container_field_off_the_writers_shape_is_refused_by_name); both deleted -> 1 failed, 34 passed. Every natural deletion takes exactly ONE test red, never two. The load-bearing claim reproduces under all four; only the arithmetic did not. Both were pin-tests, not mechanism, which is why the number moves only 5 points and not to `proved`. The claim's other two halves are untouched: `links` and `repair`.

EG.133 parent round (a00-98a14a87) — CORRECTIVE DH.EG.133 closed on this node.

| item | disposition | evidence |
|---|---|---|
| 1 · published pytest summaries omit `1 skipped` | SETTLED, no edit | `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_links.py -q --basetemp=/tmp/eg133-parent-links` -> "36 passed, 9 warnings in 0.30s" (whole last line). No `skipped` token exists to omit; the only published lines on this chain that carry one already carry it (a00-16a744c6-447f40.md:62 "1 failed, 72 passed, 6 skipped"; a00-7a12aad2-6a3a17.md:152 "1 failed, 108 passed, 6 skipped"). |
| 2 · a falsified demotion ground with the number left | FIXED | experiment:a00-7a12aad2-6a3a17.md:25 now `verdict: inconclusive_lean_proved:80`, `confidence: 0.8`. The demotion's sole ground (its probes[2] P3, "the file is still ` M`") is false of the bytes on disk: a00-3e239d1d-9407b0.md:16 carries the CORRECTION to P2 and :20 the CORRECTED NUMBER for P4b, in text, committed. |
| 3 · THOUGHT accreted, not rewritten | FIXED | the THOUGHT block on this node is rewritten whole and carries one round's delta; the count record it dropped is in the Agent Notes paragraph of this node, which is body. |
| 4 · deliverable did not ride its done commit | RECORDED, NO ACTION (g7.33.19 row 13) | commit 850091463 names experiment:a00-1556127c-9fb395; the EG.44 parent verdict lives on a00-7a12aad2-6a3a17. History is not rewritten, nothing re-landed. |

THIS ROUND'S NET MOVEMENT ON THE CLAIM: none, and the number says so (:75 held). The one kid (a00-381638dd, experiment:a00-381638dd-55286c) spent its round on a measurement instead of the corrective text, and its measurement is the fourth round in a row to find the `links` half untouched. I re-ran it myself in a tmp graph (four probes recorded on that node): `cli._load_frontmatter` refuses the scalar `probes` by name (ok=False, "frontmatter value(s) not in the sanctioned writer's shape ...: probes"); `cli._off_shape_values` -> `['probes']`; `links.off_shape_keys` -> `[]` because links.py:103-106 never reads a value; and `cli._declared_types` -> `{}` for any root with no `context/schemas`, which turns the whole value gate off with no message (cli.py:300-302, bare except). That last one is latent -- cli.py:376/464/471/1981 all pass the graph root -- and it is the smallest live mechanism left on this claim.
