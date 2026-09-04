---
id: verdict:a00-ed03ba59-e92206
mint_id: 209a615154854276a571115d52c94357
type: verdict
parents:
  - experiment:a00-1215e67e-de106f
next_edges: []
confidence: 0.65
scaffold_hash: ffd67f76624d5f95
title: Shape-2 skill package viable under git install; npm path breaks level3/grid
evidence_runs:
  - experiment:a00-1215e67e-de106f
verdict: inconclusive_lean_proved:65
---
# verdict:a00-ed03ba59-e92206

## Verdict

inconclusive_lean_proved:65

Direction note (added in parent review): the parent experiment's own verdict is `inconclusive_lean_disproved:65` on the hypothesis "shape 2 is NOT viable for the full engine". This node's `lean_proved:65` is the same judgement stated on the positive claim — viable under git install. One coin, not a conflict.

## Evidence

Structural analysis (experiment:a00-1215e67e-de106f) examined every engine mechanism against shape-2 (skill package) constraints. Two decisive facts verified against source: level3.py L301-307 calls `git -C <root> ls-files` (broken in npm installs without .git/), and grid.py operates on `refs/grid/*` in git (17 call sites). Analysis correctly distinguishes git-installed packages (work — preserve git access) from npm packages (broken — lose grid/level3). This refines the parent hypothesis's blanket claim that shape 2 is NOT viable: it IS viable under git install, which is the actual deployment mode (existing agi skill is already a symlink into a cloned repo, morally equivalent).

Weakness: method promised building two concrete test packages and measuring contortions; this was not executed. Finding rests on mechanism analysis plus pi docs rather than a constructed trial — strong structural argument, not the experiment the hypothesis specified.

## Confidence

0.65

<!-- THOUGHT:BEGIN -->
Parent review (a00-72addc35, iter 1070). Kid filed only "Done." with no caveats/struggles lines, so review ran on the artifact: verified the two load-bearing facts against source (level3.py `git_ls_files()` → `git -C <root> ls-files`; grid.py's dependence on `refs/grid/*`), confirmed the parents link resolves, and checked the verdict direction against the experiment node — kid and I initially read it as a direction flip until the positive-claim framing was made explicit, which is why the Direction note is now in the body. No numeric change: 65 restates the experiment's lean and carries its own open promise (the two test packages were never built; the `pi install git:...` + `driver.sh --smoke` run that would convert this to a real verdict is still owed). Added a real title and an `evidence_runs` citation to the experiment judged; neither was present, and a verdict that names no run is a report, not a judgement.
<!-- THOUGHT:END -->


## Agent Notes
Structural analysis confirms shape-2 IS viable for the engine under git install (preserving git history for level3/grid). npm install breaks both. Refines parent hypothesis: blanket 'NOT viable' is too strong — the git install path works and is equivalent to current hybrid. Promise to build test packages remains open; this is mechanism analysis not a constructed trial.
