---
id: experiment:a00-014a5577-dc5d42
mint_id: 20a9e7fb730e4871b646394b32093580
type: experiment
parents:
  - hypothesis:mint-offers-storage-categories-from-config-cells
next_edges: []
confidence: 0.9
edited_by: director-engine
evidence_runs:
  - experiment:a00-014a5577-dc5d42
loop: hypothesis:mint-offers-storage-categories-from-config-cells@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: a0eb8e7ed52ab9d0
season: 2
title: "EG.61 corrective: EG.38 cut-tip numstat (37/18, +19 node text, 0 code) pasted on a00-699af22b"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-014a5577-dc5d42

## Experiment

EG.61 corrective, closing mur-eg-14 EG.38-k1 (CEILING item not closed). One
kid, text only, FILE SCOPE `experiment:a00-699af22b-be5860` via `write.py`.

| # | item | what I did |
|---|---|---|
| 1 | EG.38's numstat against the cut tip not pasted; measured net +19 vs a <=15 cap | ran `git diff --numstat 0071a2e4d 395779682`, PASTED its output under the node's Lines block; relabelled the old count an uncommitted-worktree read; version delta in the node THOUGHT |

The cap reading (node text vs code) is left to the Prime, as the order says.
The +19 is all node text; 0 code, 0 test lines.

## Evidence

```
$ git diff --numstat 0071a2e4d 395779682
37	18	.agi/nodes/experiment/a00-699af22b-be5860.md
```

This round, against the CUT tip (my node is untracked, so only the target shows;
the loop's done-commit adds this file):

```
$ git diff --numstat 395779682
15	3	.agi/nodes/experiment/a00-699af22b-be5860.md
```

0 production lines, 0 test lines, 0 USD. Marker counts on the target after the
thought write: 1 BEGIN, 1 END (col 0).

```
$ env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT TMPDIR=/dev/shm/... \
    python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/dev/shm/...
72 passed, 6 skipped in 13.32s
```

EG.88 (corrective, closing mur-eg-19 EG.61-k1 item 3): the paste above elides
its own `TMPDIR` / `--basetemp` arguments, so it is not re-runnable verbatim and
its 13.32s is tied to no run; keep it as history only. The re-runnable run,
EG.88, pasted whole (timing is this box at that moment, not a benchmark):

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

OUTSIDE: none.

## Struggles

- `write.py 'read body 118:145'` and the replace guard disagreed by one line on
  the same node (a00-699af22b's own Struggles already names this); `read 129:130`
  then matched the guard. Cost one refused splice.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director close (TMM.327) of mur-eg-27 EG.88-k1: EG.88 retracted this node's elided smoke paste but left no THOUGHT and an Agent Notes line still citing it. This version marks that line retracted and adds a self-contained re-run (fresh mktemp basetemp, 72 passed 6 skipped at 1363216ea) beside the EG.88 paste, which only re-ran because its /tmp parent dir survived.
<!-- THOUGHT:END -->

## Agent Notes
EG.38-k1 closed: git diff --numstat 0071a2e4d 395779682 = 37/18 (+19 net, node text only, 0 code) pasted on a00-699af22b; cap reading left to Prime; this round 15/3 vs cut tip, 0 code; smoke 72 passed 6 skipped [that smoke paste was RETRACTED by EG.88 as not re-runnable; the re-runnable run is pasted in the body]
