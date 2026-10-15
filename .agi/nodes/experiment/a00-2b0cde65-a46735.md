---
id: experiment:a00-2b0cde65-a46735
mint_id: 3727bda488e8433f88dca061c4a29db9
type: experiment
parents:
  - hypothesis:pb3-agent-git-hook-fails-closed-on-a-failed-diff
next_edges: []
confidence: 0.85
edited_by: director-general-4
evidence_runs:
  - experiment:a00-2b0cde65-a46735
loop: hypothesis:pb3-agent-git-hook-fails-closed-on-a-failed-diff@s2
model: claude-sonnet-5-5
production_lines: 6
profile: balanced
role: kid
scaffold_hash: 5db333640ccd341d
season: 2
title: Hook comments and attribution docstring corrected
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2b0cde65-a46735

## Experiment
Comment-only fix in `pre-commit` kid-scope block: per-stage PIPESTATUS rule replaces "rc >= 2 is a failed DIFF"; pipefail stated inert (belt only). Attribution row docstring now states the real pre-corrective red: dead scope-check printed `git diff --cached failed (rc 2)`, blaming a clean producer (source: experiment a00-f99818f9-49864c; git was off-limits, base not re-read).

## Evidence
Director harvest 14:1xZ 09-30 on the loop tree 0f0e5905cf: `pytest test_git_commit_guard.py test_bin_help_smoke.py` = 113 passed, 8 skipped (the kid ran test_git_commit_guard.py alone: 43 passed). No code lines changed.

## Agent Notes
comment-only fix: per-stage PIPESTATUS rule, pipefail inert, real red shape in docstring; 43 pass
