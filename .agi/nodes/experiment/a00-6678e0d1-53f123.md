---
id: experiment:a00-6678e0d1-53f123
mint_id: 812e0a03b63b485fba84fd3c32b62d7f
type: experiment
parents:
  - hypothesis:provisioning-reads-its-cells-through-one-import-route
next_edges: []
confidence: 0.6
edited_by: a00-ff2a5bfc
evidence_runs:
  - experiment:a00-6678e0d1-53f123
loop: hypothesis:provisioning-reads-its-cells-through-one-import-route@s2
model: claude-opus-5-5
production_lines: -8
profile: balanced
role: kid
scaffold_hash: 0ca7ac9acde7c5a9
season: 2
title: "EG.156 text-fix: provisioning round re-cut to 8 net lines, node record corrected"
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-6678e0d1-53f123

## Experiment — CORRECTIVE DH.EG.156 text-fix (closes mur-eg-59 EG.123-k1)

| # | item | done | where |
|---|---|---|---|
| 1 | overclaiming "28 production lines net (ceiling 40)" | PARTIAL: the Measurement section reads real 28/12 = 16 net vs cap 15, then the re-cut 8 net, but the SAME overclaim survived verbatim in the EG.123 node Agent Notes; at EG.156 the defect MOVED, it did not go away. EG.193 corrected the surviving line | experiment:a00-9db7337e-cc325e body, Measurement section (fixed here) + Agent Notes (fixed at EG.193) |
| 2 | M2: 8 docstring prose lines duplicating the node body | FIXED: `_prov_cell` docstring folded 9 lines -> 1 (`"""One provisioning.<name> dollar cell; a pre-loaded cfg wins over root."""`); no statement changed; `ast.parse` ok. The KEY-PRESENCE comment kept (not ordered cut); it reads at provisioning.py:525-528 on the cut tip, the corrected citation EG.164 failed to land | extensions/agi/bin/provisioning.py:202 (docstring) and :525-528 (comment) |
| 3 | M3: 90/5 vs 168/12 mislabelled "same three files" | FIXED: sentence replaced with the ONE-file ordered command and its pasted result below | experiment:a00-9db7337e-cc325e body |
| 4 | M4: parent OPEN block stale ("IN PROGRESS ... QUEUED") on the landing tip | FIXED: STATUS now LANDED at 03ab636aa + round chain; THOUGHT rewritten | hypothesis:provisioning-reads-its-cells-through-one-import-route |

OUTSIDE: none — every fix sat inside FILE SCOPE.

## Evidence

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider extensions/agi/tests/test_provisioning.py --basetemp=/tmp/pt-a00-6678-1
91 passed, 5 skipped in 0.91s
$ env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider extensions/agi/tests/test_bin_help_smoke.py --basetemp=/tmp/pt-a00-6678-2
72 passed, 7 skipped in 21.28s
$ git diff --numstat 03ab636aa          # working tree vs CUT tip (no commit: kid runs no git writes)
6	5	.agi/nodes/experiment/a00-9db7337e-cc325e.md
5	5	.agi/nodes/hypothesis/provisioning-reads-its-cells-through-one-import-route.md
1	9	extensions/agi/bin/provisioning.py
$ git diff --numstat bb3fd61ed -- extensions/agi/bin/provisioning.py extensions/agi/tests/test_provisioning.py
20	12	extensions/agi/bin/provisioning.py
39	0	extensions/agi/tests/test_provisioning.py
```

Production vs 03ab636aa: -8 net (1 added, 9 removed, docstring only). Round total vs bb3fd61ed: 20-12 = **8 net production** (cap 15), **39 test** (cap 40). Inside both caps.
