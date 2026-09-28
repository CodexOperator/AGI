---
id: experiment:a00-92c392c7-000519
mint_id: c891ba7f0536474ba58357d9aad3aa3d
type: experiment
parents:
  - hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
next_edges: []
confidence: 0.85
edited_by: a00-92c392c7
evidence_runs:
  - experiment:a00-92c392c7-000519
loop: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f1765dc5cb889ccd
season: 2
title: "DH.EG.167 text-fix: six citation residues settled at f7294d13d"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-92c392c7-000519 — DH.EG.167 text-fix: six citation residues settled against f7294d13d

## Experiment
TEXT-FIX KID. All edits made with `write.py ... 'replace body N:M -'`, paragraph-scoped. Each cite was checked with
`sed -n <line>p` on the worktree, which is byte-identical to the CUT tip f7294d13d for every file read (only node files changed).

| # | Node:line | Settling output (at f7294d13d) | Fix |
|---|---|---|---|
| 1 | a00-310104ca:216 | `322: @pytest.mark.xfail(strict=True, ...` · `329: def test_known_residual_a_row_may_name_a_file_that_does_not_exist` · `489: def test_one_submit_reads_the_frontmatter_once` (321 is blank, 483 is an assert) | re-pointed to 322/329/489 |
| 2 | a00-b2b01c2b:36, :81, :94 | `361:     assert resolved.is_file(), (` · `363:         f"KNOWN RESIDUAL this xfail pins")` | all three now cite :361; :363 named as the message string; unverifiable dff3b6076 number dropped |
| 3 | a00-0a22ec6c:163-165, a00-fd3b2d8a:78 | `15: import contextlib` (one line); defs 381/528/561/572 (+6) vs marker/def 322/329 (+1) | cause WITHDRAWN (a single insertion can't produce two different shifts); numbers kept |
| 4 | a00-fd3b2d8a:76 | a00-0a22ec6c `205: ## Weakness of this node`, `215: EG.80 (a00-310104ca, corrective) — ...` | re-pointed to the EG.80 Agent Note's M4 item (:215) |
| 5 | hypothesis:44 | `3206: "&&&& (a doubled pair) separates exactly as it always did.")` · `3207: epilog_lines.append(` · `3211: "(\`set payload_ref --confirm-move new/dir/f.txt\`).")` | 3206-3210 -> 3207-3211 |
| 6 | hypothesis:24 | `grep -n os.replace node_writer.py` -> `608 · 1201 · 1277` | 1194/1270 -> 1201/1277 |

## Evidence
```
$ git diff --numstat f7294d13d      (worktree vs the CUT tip, measured before this node was filled)
4	4	.agi/nodes/experiment/a00-0a22ec6c-a7c352.md
2	2	.agi/nodes/experiment/a00-310104ca-7482ff.md
4	4	.agi/nodes/experiment/a00-b2b01c2b-3dc0c3.md
3	3	.agi/nodes/experiment/a00-fd3b2d8a-0d5a4d.md
3	3	.agi/nodes/hypothesis/a-payload-ref-change-renames-the-file-in-the-same-write.md
```
Production lines 0 and test lines 0 (node prose only). Each node's extra +1/-1 is the frontmatter stamp write.py adds.
After the edits, `sed -n '111p;205p;215p'` on a00-0a22ec6c still shows the marker/def line, the Weakness heading and the
EG.80 note, so the replaces did not shift any sibling anchor.

## Weakness of this node
- No commit: the kid contract forbids git, so the parent/loop must commit these edits (the corrective's KID line says the kid commits, which contradicts that).
- dff3b6076 numbers were NOT re-measured (that would need `git show`). They were removed, not verified.
- Item 3 names no replacement cause. None was reproduced, so none is stated.
- This body cites line numbers itself. They hold only at f7294d13d.

## Agent Notes
DH.EG.167 six citation residues fixed via write.py, each settled by sed at f7294d13d: 310104ca:216 ->322/329/489; b2b01c2b :363->:361 x3; import-contextlib cause withdrawn (0a22ec6c, fd3b2d8a:78); fd3b2d8a:76 M4 ->:215; hyp:44 3207-3211; hyp:24 os.replace 1201/1277. 0 production/test lines.
