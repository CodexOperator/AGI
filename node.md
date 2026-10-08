---
id: experiment:a00-6549e49d-941f59
mint_id: 98936b78863f4f95ab93282f78599cca
type: experiment
parents:
  - hypothesis:mint-offers-storage-categories-from-config-cells
next_edges: []
confidence: 0.9
edited_by: director-engine
evidence_runs:
  - experiment:a00-6549e49d-941f59
loop: hypothesis:mint-offers-storage-categories-from-config-cells@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 853c1785ee03a2c8
season: 2
title: "EG.88 corrective: a00-699af22b production_lines 12->0, notes-last layout re-verified on bytes, a00-014a5577 test paste made re-runnable"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6549e49d-941f59

## Experiment

DH.EG.88 corrective, closing mur-eg-19 EG.61-k1. One kid, text only, `write.py` only.

| # | item | what I did | state |
|---|---|---|---|
| 1 | `production_lines: 12` on a00-699af22b is stale against the node's +19 / +12 | `set production_lines 0`: 12 was an uncommitted node-text read; every round there had a 0-production ceiling (text is non-production), and 0 code lines is what every measurement on the node says. Node-text counts stay under its Lines block. The version delta is in the node's THOUGHT | FIXED |
| 2 | `season._agent_notes_block` on the delivered bytes | ran it on a215318b5's bytes (clean worktree) and again after my edits. It still reads 10 lines ending in a grep line, with 1 BEGIN / 1 END. The EG.25/EG.38 notes-last layout survived | ALREADY TRUE, pasted |
| 3 | elided test command at a00-014a5577 | kept the old paste as history and labelled it not re-runnable. Ran the smoke test once and pasted the full command | FIXED |
| 4 | TMM.268 custody (demoted) | nothing done, as ordered | n/a |
| 5 | numstat vs the CUT tip | pasted below | DONE |

## Evidence

Item 2. Probe script at `<session>/notes_probe.py`: reads the file, calls
`season._agent_notes_block`, and lists the col-0 marker lines and the last heading.

```
# before any edit (worktree == a215318b5, git status clean but for my own node)
notes_block_lines 10 last "$ grep -c '^<!-- THOUGHT:[B]EGIN' .agi/nodes/experiment/a00-"
BEGIN [213] END [215]
last_heading ## Agent Notes
# after set production_lines + thought on a00-699af22b
notes_block_lines 10 last "$ grep -c '^<!-- THOUGHT:[B]EGIN' .agi/nodes/experiment/a00-"
BEGIN [213] END [215]
last_heading ## Agent Notes
```

Item 3:

```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest \
    extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/eg88-a00-6549e49d/pt
72 passed, 6 skipped in 39.55s
```

Director close (TMM.327, mur-eg-27 EG.88-k1 V1): the paste above re-ran only because its /tmp parent dir was left behind (pytest makes the basetemp without parents; a clean /tmp gives 79 errors at setup). Self-contained re-run at 1363216ea:

```
$ BT=$(mktemp -d) && env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT TMPDIR=$BT timeout 900 \
    python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider --basetemp=$BT/pt
72 passed, 6 skipped in 7.61s
```

Item 5. This was run after the last edit to either target. My own node is untracked, so it
does not appear; the loop's done-commit adds it. This is a worktree read, not a
two-commit range, because a kid may not commit:

```
$ git diff --numstat a215318b5
12	1	.agi/nodes/experiment/a00-014a5577-dc5d42.md
3	3	.agi/nodes/experiment/a00-699af22b-be5860.md
```

0 production lines, 0 test lines, 0 USD. OUTSIDE: none.

## Struggles

- `write.py 'read body N:M'` and the `replace` anchor guard were one line apart on
  a00-014a5577. `replace 33:37` was refused. The same range under the guard's
  numbering, `34:38`, then read and replaced correctly. Three kids on this chain
  have now hit this. The real fix is outside FILE SCOPE: make `read` and the
  guard in `extensions/agi/bin/write.py` count body lines the same way.

## Agent Notes
mur-eg-19 EG.61-k1 closed: a00-699af22b production_lines 12->0 (+THOUGHT); notes-last layout re-verified on bytes (10-line block, 1 BEGIN/1 END, before+after); a00-014a5577 elided pytest paste labelled + re-runnable run pasted (72 passed 6 skipped); numstat vs a215318b5 = 12/1 + 3/3 node text, 0 code, 0 test, 0 USD
