---
id: experiment:a00-3cccf2e3-09031d
mint_id: 4cca59418ed546c8be1384936ed6a847
type: experiment
parents:
  - hypothesis:l4-a-parents-zoom-is-its-target-goal-chain-claim-conjuncts-and-own-kids-never-the-sibling-hypothesis-dump
next_edges: []
confidence: 0.9
edited_by: a00-00ab0971
evidence_runs:
  - experiment:a00-3cccf2e3-09031d
loop: hypothesis:l4-a-parents-zoom-is-its-target-goal-chain-claim-conjuncts-and-own-kids-never-the-sibling-hypothesis-dump@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b1a15c220682a6a5
season: 2
title: A00 3cccf2e3 09031d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3cccf2e3-09031d

## Experiment — SL7.109 round 2, build order under
`hypothesis:l4-a-parents-zoom-is-its-target-goal-chain-claim-conjuncts-and-own-kids-never-the-sibling-hypothesis-dump`

Parent measured before this round (round-1 residue): `zoom.py . SL7.109 a00-zz
--level 3 --runtime pi --tier parent --target <id>` returned rc=0 with no
stderr and rendered the ordinary level-3 Code view (4,792 B); `--level big
--tier parent` behaved the same. The `--tier parent` flag was accepted and
dropped off the small path (same defect class as `hypothesis:l4b23-
promptfile-drop`).

**Defect 1 — honest refusal for `--tier parent` off the small path.**
Chosen fix (a): refuse by name. Added a guard in `zoom.py main()` before the
level dispatch:
- when `raw_level != "small" and args.tier == "parent"`, print one stderr line
  naming the tier and the level and return 1, before any context is written.
- `kid`/`director` were deliberately left unguarded: they are byte-identical
  to the default shape on every level, so serving the numeric view under them
  is not a dropped grain (the requested shape IS served).
- The file already refuses a wrong grain rather than serving one
  (`_unavailable_message`), so this is consistent house style. Keeping the
  numeric-level view for `--tier kid`/`director` preserves the live pipeline
  and every existing caller byte-identically.
- `--level small --tier parent` is untouched and re-verified below.

Measured after (on the live tree):
```
$ zoom.py . SL7.109 a00-check --level 3 --tier parent --target <id>
ERR: --tier parent has no shape at --level 3; the parent shape only exists
on the --level small path. Refusing to serve the level-3 view under the
parent tier label instead of the requested shape.
rc=1
$ zoom.py . SL7.109 a00-check --level big --tier parent
ERR: --tier parent has no shape at --level big; ... (same shape)
rc=1
```
No context file written on the refusal (the guard returns before
`out_path.write_text`).

**Defect 2 — dangling node citation in two comments.**
`zoom.py:767` and `dispatch.py:203` cited `hypothesis:l4-a-parents-zoom-is-a-
per-tier-shape` (invented shorthand, does not resolve). Replaced both with the
real id `hypothesis:l4-a-parents-zoom-is-its-target-goal-chain-claim-`
`conjuncts-and-own-kids-never-the-sibling-hypothesis-dump`, verified to
resolve on the live tree (`ls .agi/nodes/hypothesis/ | grep`).

## Evidence

- Tests: `python3 -m pytest extensions/agi/tests/test_zoom.py
extensions/agi/tests/test_dispatch.py -q` → **146 passed** (145 in round 1 +
  the 3 added/refined assertions; baseline 143 → 146 net of this round's 3
  new tests).
- New tests added (in `test_zoom.py`):
  1. `test_parent_tier_refuses_by_name_off_the_small_path` — `--tier parent`
     at levels `3`, `big`, `1` returns non-zero, the stderr names both tier
     and level, and no context path is printed.
  2. `test_small_path_parent_shape_still_renders_after_guard` — the round-1
     parent shape (target full, conjuncts, goal chain, own kids, no
     siblings) still renders post-guard.
  3. `test_no_source_comment_cites_an_unresolvable_tier_node_id` — the
     invented `a-parents-zoom-is-a-per-tier-shape` is gone from both
     `zoom.py` and `dispatch.py`, and the corrected id prefix is present.
- Round-1 golden holds: `test_kid_and_director_tiers_byte_identical_to_default`
  and the small parent-size/kid tests still pass — kid/director/default stay
  byte-identical, and the small `parent` path is unchanged.
- Line budget: change is ~14 production lines (one guard + cascading level 
  checks), well under the 60-line ceiling. I did not attempt the optional
  120-line docstring fold: the round-1 185-line count is dominated by the
  three helpers' documented reasoning, and folding them would touch rendered
  bytes that the golden test pins byte-identical. Left as-is on purpose.
- The `--level 4/5` refusal for `--tier parent` arrives via
  `_unavailable_message` (level truly unavailable) before the tier guard —
  still an honest refusal, and the live `3`/`big`/`1` cases (the silent-drop
  defects) are the guard's own job.
- No git was run; edits and tests only.

## Agent Notes
Fixed both SL7.109 defects: (1) --tier parent now refuses by name (rc=1, stderr names tier+level, no context written) on any level without a parent shape (3/big/1 verified live; kid/director left unguarded as byte-identical to default); (2) replaced invented comment id hypothesis:l4-a-parents-zoom-is-a-per-tier-shape with the real resolvable id in zoom.py and dispatch.py. Added 3 tests; suite 146 passed; round-1 small-parent shape and kid/director golden unaffected.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-00ab0971, SL7.109 round 2) — kept at proved, both named defects independently reproduced fixed. WHAT THE INSTRUCTION SAID: (Defect 1) "in zoom.py, when --tier parent is combined with a level that has no parent shape ... either (a) refuse by name — non-zero exit, one stderr line naming the tier and the level, no context written ... or (b) emit a named skip line"; (Defect 2) "zoom.py:767 and dispatch.py:200 cite hypothesis:l4-a-parents-zoom-is-a-per-tier-shape; no such node exists. Replace both with the real id". WHAT THE MACHINE ACTUALLY DOES (measured by me, not read from the kid report): zoom.py . SL7.109 a00-zz --level {3,big,1} --runtime pi --tier parent --target <id> each returns rc=1, writes NO context file, and stderr names both the tier and the level ("ERR: --tier parent has no shape at --level 3; the parent shape only exists on the --level small path"); --level small --tier parent still renders (8,296 B) and shows the kids section; grep per-tier-shape in zoom.py/dispatch.py returns nothing while the real id resolves. pytest test_zoom.py test_dispatch.py = 146 passed. NEAR MISS: the cheap implementation of Defect 1 is to make the guard fire on tier alone, which would also refuse --level small --tier parent and break the only shape the round-1 work produced; the guard keys on raw_level != "small" so the served shape is untouched, and the round-1 golden (kid/director byte-identical, small-parent renders) is re-run to prove it. RESIDUE, accepted: (a) the 8,224 B parent render I measured in round 1 is now 8,296 B — NOT a shape regression: the target gained this experiment as a second child and the kids section prints one line per child, verified by reading the section; a future reader comparing the two numbers should know the delta is the graph, not the renderer. (b) the optional 120-line docstring fold was declined on purpose with the reason that it would touch bytes the golden pins; correct call. (c) this node title is the scaffold default ("A00 3cccf2e3 09031d") — cosmetic, the body carries the work. (d) --level 4/5 --tier parent is refused by _unavailable_message before the tier guard, which is still an honest refusal but a different line than the guard own; a reader grepping for the guard message will not find it on those levels.
<!-- THOUGHT:END -->
