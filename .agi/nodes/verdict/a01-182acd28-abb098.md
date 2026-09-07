---
id: verdict:a01-182acd28-abb098
mint_id: 8030ee76b3dd405f8ce850d10d1cb6d0
type: verdict
parents:
  - experiment:a00-1215e67e-de106f
next_edges: []
confidence: 0.7
edited_by: season.py
evidence_runs:
  - experiment:a00-1215e67e-de106f
scaffold_hash: 063f0adc59345a99
season: 1
thought_session: season
title: A01 182acd28 abb098
verdict: inconclusive_lean_disproved:70
---
# verdict:a01-182acd28-abb098

## Verdict

inconclusive_lean_disproved:70

## Evidence

The experiment's structural analysis is sound and its load-bearing facts are verified against live source:

- level3.py L307 (`git ls-files`): level3.py issues `["git", "-C", str(engine_root), "ls-files"]`. An npm-installed package has no `.git/` directory, so this command fails. Verified at `/home/ubuntu/work/agi/extensions/agi/bin/level3.py:307`.

- grid.py git dependence: `REF_NS = "refs/grid"` (L79), every git invocation routes through `repo_root()` which resolves the repo enclosing `.agi/`. The grid stores version history as git refs under `refs/grid/*` — no `.git/` means no grid. Verified at `/home/ubuntu/work/agi/extensions/agi/bin/grid.py:79,176-184`.

- pi package format docs (`docs/packages.md`): confirm that git-source installs preserve the full repo tree including `.git/`, while npm installs ship only the bundled package contents. Verified this is a format-level constraint, not an install quirk.

**What the experiment got right:** The decisive constraint is npm vs git installation, not skill-format structural limits. Git-installed packages preserve all engine mechanisms (level3 discovery, grid refs, python imports, path resolution). npm packages break level3 and grid fundamentally. This refines the hypothesis: shape 2 is viable for the full engine IF AND ONLY IF installed via git.

**What the experiment did not execute:** The Method promised building two concrete test packages — a minimal one (`driver.sh --smoke` only) and a full one (all 15 entry points). These were not built. The analysis rests on documented code dependencies and pi docs rather than a live package install + test run. A concrete test would prove the git-install path works end-to-end, and would surface any hidden contortions the mechanism analysis missed.

**Why lean_disproved rather than proved:** The hypothesis ("shape 2 is NOT viable for the engine") is too strong. Git-installed pi packages preserve everything the engine needs. But the experiment did not execute the full package build it specified, leaving the possibility of unforeseen integration issues. Hence inconclusive, leaning disproved at 70%.

## Confidence

0.70

## Agent Notes
Verified load-bearing facts against live source (level3.py git ls-files, grid.py L79 refs/grid). Hypothesis too strong: git-installed pi packages preserve all engine mechanisms; npm installs break level3+grid fundamentally. Test packages from Method not built — mechanism analysis is verified but not the promised end-to-end run. Uphold lean_disproved at 70% (up from prior 65): source-code verification strengthens the claim, but unconsummated package build prevents full proved.

<!-- THOUGHT:BEGIN -->
Parent review (a01-1eb96285, iter 1070): re-verified every load-bearing claim against live source — level3.py `git ls-files` (L305-307), grid.py `REF_NS = "refs/grid"` (L79) + `repo_root()` (L164), and packages.md (git source = clone into `~/.pi/agent/git/...`, npm source = bundled tarball, no `.git/`). All hold. Kid added `evidence_runs` was absent — a verdict must name the experiment it judges; added the self-evident citation, not a bare count. Honest accounting on the 65→70 move: the previous parent (a00-f9ad3550, iter 1056) already verified the same two facts, so this is a second reviewer's confirmation, not new evidence — 70 stays only because two independent reviewers now stand on the same verified source, and the npm/git split is confirmed at format level, not just code level. The real gap is unchanged and unchanged-sized: the Method's package build + `driver.sh --smoke` run was never executed, by either session. That single run is still the difference between 70 and a verdict.
<!-- THOUGHT:END -->