---
id: goal:g1.31.5.5.3
mint_id: 4f308d0b72fb4535996921881ef781ba
type: goal
parents:
  - goal:g1.31.5.5
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.5.3
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 6885065b31b965fd
season: 2
seeds: []
status: retired
tags:
  - engine
  - pass
  - residue
  - node-answer
  - scaffold
title: "G1.31.5.5.3: 6 hypotheses + 1 experiment carry a real title and ## Hypothesis claim, one H1 and one ## Agent Notes -- no creation scaffold left"
town: core
---
# goal:g1.31.5.5.3

## Why this exists
goal:g1.31.5.5: PASS B3 verify stages found 6 rows where a hypothesis/experiment body still holds its creation scaffold (id-echo title, the unfilled "What is the testable claim?" prompt) or repeats a heading. Triaged REAL at HEAD 8209a5813; 0 already fixed; 2 residue · 4 nit.
```
n   round                                                    verify file (.agi/sessions/workflows/runs/)
1   a00-4d063889-c4e95d                                      mur-pb3chunk10of20/verify_a00-4d063889-c4e95d.json
15  l3-grid-lock-doubled-path                                mur-pb3chunk12of20/verify_l3-grid-lock-doubled-path.json
32  l3w4-rotation-announces-itself                           mur-pb3chunk14of20/verify_l3w4-rotation-announces-itself.json
48  thought-verb-edits-only-the-top-level-thought-block      mur-pb3chunk16of20/verify_thought-verb-edits-only-the-top-level-thought-block.json
57  l4-test-zoom-unresolvable-tier-id-errors-only-...-ful    mur-pb3chunk18of20/verify_l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-ful.json
99  provisioning-reads-its-cells-through-one-import-route    mur-pb3chunk4of20/verify_provisioning-reads-its-cells-through-one-import-route.json
```

## Target end-state
- n1 `hypothesis/a00-4d063889-c4e95d.md:13` `title:` is a claim, not the id-echo "A00 4d063889 c4e95d".
- n15 `hypothesis/l3-grid-lock-doubled-path.md:20` `## Hypothesis` holds the claim (today only frontmatter `testable_claim` + Agent Notes do).
- n32 `hypothesis/l3w4-rotation-announces-itself.md:20` `## Hypothesis` holds the claim, amended for the routing-matrix narrowing of "every live seat" (rotate.py `_announce_rotation`, :6498).
- n57 `hypothesis/l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-full-suite.md:21` `## Hypothesis` holds the claim + falsifiers from `testable_claim`.
- n48 `hypothesis/thought-verb-edits-only-the-top-level-thought-block.md` has ONE H1 (today :21 and :23).
- n99 ONE H1 in `experiment/a00-4453045a-d9a866.md` (:23, :25) and `hypothesis/provisioning-reads-its-cells-through-one-import-route.md` (:17, :19); ONE `## Agent Notes` in a00-4453045a (:94, :101); the "no sanctioned write.py verb removes a heading" note (:112) is answered (`write.py … 'patch -'` exists at HEAD).

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Node answers go through `write.py` only (`set title`, `sub`, `patch -`); a heading is removed, never the section under it; retire, never delete.

## Falsifier
1. From the repo root:
```bash
bash -c 'H=.agi/nodes/hypothesis; E=.agi/nodes/experiment
! grep -qx "title: A00 4d063889 c4e95d" $H/a00-4d063889-c4e95d.md &&
! grep -q "What is the testable claim? What would prove it?" $H/l3-grid-lock-doubled-path.md $H/l3w4-rotation-announces-itself.md $H/l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-full-suite.md &&
sed -n "/^## Hypothesis/,/^## /p" $H/l3w4-rotation-announces-itself.md | grep -qi routing &&
[ $(grep -c "^# hypothesis:" $H/thought-verb-edits-only-the-top-level-thought-block.md) -eq 1 ] &&
[ $(grep -c "^# hypothesis:" $H/provisioning-reads-its-cells-through-one-import-route.md) -eq 1 ] &&
[ $(grep -c "^# experiment:" $E/a00-4453045a-d9a866.md) -eq 1 ] &&
[ $(grep -c "^## Agent Notes" $E/a00-4453045a-d9a866.md) -eq 1 ]'
```
   (exits 1 at HEAD 8209a5813; all 7 conjuncts open.)
2. Negative: `git grep -n 'What is the testable claim? What would prove it?' -- .agi/nodes/hypothesis/l3-grid-lock-doubled-path.md .agi/nodes/hypothesis/l3w4-rotation-announces-itself.md .agi/nodes/hypothesis/l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-full-suite.md` returns zero hits (3 at HEAD).

## Out of scope
goal:g1.31.3.1.1 (#1 a00-4d063889 claim :20-29 + verdict :14; #13 l4-test-zoom experiment verdict) · the systemic duplicate-H1 cause in the create path (DG3 lane, see notes) · goal:g1.31.5.5.1 · goal:g1.31.5.5.2 · goal:g1.31.5.5.4 · goal:g1.31.5.5.5 · goal:g1.31.5.5.6 (n98: a00-4453045a prose after THOUGHT:END) · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
