---
id: experiment:a00-ef5840bb-983e95
mint_id: 52c39fabe7ab4577bcee7927e1e17dcc
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.9
edited_by: a00-ef5840bb
evidence_runs:
  - experiment:a00-ef5840bb-983e95
  - experiment:a00-775fe9d4-ae8544
  - experiment:a00-0de7626f-4f8260
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 1602f48bacd4423f
season: 2
title: "EG.83 corrective: EG.70 node numstat now lists its own 84 lines, a00-0de7626f title and THOUGHT describe their EG.70 delta"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# EG.83 corrective: two node-text residues from EG.70, fixed with write.py

Closes mur-eg-22 EG.70-k1 accept_with_residue. Base: 49b7b899d. Text only: 0 production lines, 0 test lines, 0 USD.

| item | defect | fix, in the bytes | verb |
|---|---|---|---|
| 1 | `a00-775fe9d4-ae8544` numstat block (worktree vs cut, own node untracked) omits its own 84 lines | block replaced with the committed two-operand range `a402ceeb3 49b7b899d`, 3 files, the node included; stray scaffold line after THOUGHT:END removed; THOUGHT rewritten to this delta | `replace body --force` ×2, `thought` |
| 2 | `a00-0de7626f-4f8260` title (:19), H1 and THOUGHT (:82) described only EG.47 | title and H1 now name the EG.70 corrections; THOUGHT rewritten from scratch to the EG.70 + EG.83 delta | `set title`, `replace body 2:2 --force`, `thought` |

`a00-3d4e7707-9962d4` needs no edit (the review says its THOUGHT matches its diff).

## Evidence (pasted)

```
$ git diff --numstat a402ceeb3 49b7b899d      (EG.70 final committed range, item 1)
8	6	.agi/nodes/experiment/a00-0de7626f-4f8260.md
2	2	.agi/nodes/experiment/a00-3d4e7707-9962d4.md
84	0	.agi/nodes/experiment/a00-775fe9d4-ae8544.md

$ git diff --numstat 49b7b899d                (this round, worktree vs CUT tip; own node untracked)
4	4	.agi/nodes/experiment/a00-0de7626f-4f8260.md
4	4	.agi/nodes/experiment/a00-775fe9d4-ae8544.md
$ wc -l < .agi/nodes/experiment/a00-ef5840bb-983e95.md   (own node, before this body was filled)
26

$ grep -n "^title" .agi/nodes/experiment/a00-0de7626f-4f8260.md
19:title: EG.47 corrective (a00-3d4e7707 THOUGHT rewrite + a00-8e3104fe thought-verb claim fix), with EG.70 corrections to its own evidence and OUTSIDE rows

$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/eg83-a00-ef5840bb
72 passed, 6 skipped in 44.06s
```

The two-operand `<your tip>` form for THIS round can't be pasted by a kid: no commit exists until the loop commits, so the untracked node line is given as `wc -l`. Same gap as item 1 had.

## OUTSIDE (for the director's findings row; not touched)

- `extensions/agi/bin/write.py:602` -- still no `--force` prefix example; this round hit the guard twice before using `replace body N:M --force -`.
- `extensions/agi/bin/write.py` `set title` -- a value wrapped in double quotes is stored with the quotes escaped inside YAML quotes (`"\"...\""`); I had to re-set it bare.
- Kid contract vs corrective: a kid can't commit, so "numstat against your tip" always misses the kid's own untracked node. The harvest should paste the post-commit range, or the corrective should ask for `wc -l` of the new node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Both EG.70 residues were node text; fixed with write.py on the two nodes, each THOUGHT rewritten to its own delta so this round does not repeat item 2.
<!-- THOUGHT:END -->

## Agent Notes
EG.83 corrective: a00-775fe9d4 numstat now the committed a402ceeb3..49b7b899d range incl. its own 84 lines; a00-0de7626f title/H1/THOUGHT rewritten to EG.70 delta; 0 prod/test lines; help smoke 72 passed/6 skipped
