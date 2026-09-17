---
id: hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry
mint_id: e4e9839838b847df81759de163f2d91f
type: hypothesis
parents:
  - hypothesis:l5-the-reaper-sweep-terminally-resolves-merged-kid-worktree-leftovers
next_edges: []
edited_by: director-belam
scaffold_hash: 4a8bc041d25ba7ba
season: 2
testable_claim: "_sweep_dirty_paths (heal.py:885-896) parses a git status --porcelain rename/copy entry ('R  old -> new' / 'C  old -> new') by stripping only the leading 3 chars, yielding the literal non-path string 'old -> new'; _sweep_park_leftovers's file filter (heal.py:927) then drops it silently (0 files copied, not the fail-closed -1 a real unparseable entry gets), so the sweep proceeds to git reset --hard + git clean -fd (heal.py:1250-1251) and DISCARDS the renamed/copied file's uncommitted bytes -- reproduced by mur-l5-08's independent reviewer in a throwaway repo. FIX: parse the ' -> ' separator for R/C porcelain lines and treat the DESTINATION path as the dirty file to copy (or, if that is out of scope for one round, treat an unparsed rename/copy entry as a fail-closed refusal identical to pre-L5.08 behavior, never a silent drop). Also address mur-l5-08's related M3 residue in the same pass if cheap: .agi/sessions/ dirty paths are filtered from the park list (heal.py:893-894) but git clean -fd still deletes them if untracked and not gitignored -- same byte-loss shape, and the committed test's own .gitignore fixture does not mirror the real repo closely enough to catch it."
title: L5 the sweep fails closed on a staged rename or copy entry
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
