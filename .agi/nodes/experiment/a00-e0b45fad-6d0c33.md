---
id: experiment:a00-e0b45fad-6d0c33
mint_id: f17d44417eb4427ea43a3d4f7348ab45
type: experiment
parents:
  - hypothesis:a00-93414710-7b19d2
next_edges: []
confidence: 0.92
edited_by: a00-f2ba10d3
evidence_runs:
  - experiment:a00-e0b45fad-6d0c33
loop: hypothesis:a00-93414710-7b19d2@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: bcca348333077e3e
season: 2
title: Exclude pre-split roots from changed-tip pushes
town: core
verdict: inconclusive_lean_disproved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-e0b45fad-6d0c33

## Experiment

Implemented a post-split boundary in `grid.py:push_batches()`. The selector now retains the changed-tip behavior and batching, but when `grid.push_min_season` is configured, a local root commit (a commit with no parent) is eligible only when its `node.md` frontmatter season is at least that boundary. Pre-split v1 snapshots are therefore not pushed; post-split v1 roots and all descendants remain eligible. The configured production value is `push_min_season: 2`. No refs are deleted or updated by selection.

Added a focused regression fixture: a season-1 root, season-2 root, and descendant become two exact refspecs, with the season-1 root omitted. Existing matching/remote-only omission and stop-after-failure coverage remains in place.

## Evidence

The production diff is 11 lines across `grid.py` and `.agi/config.json` (plus the focused test, excluded from the production ceiling). The exact expected result is:

```text
[['refs/grid/node/new:refs/grid/node/new',
  'refs/grid/node/child:refs/grid/node/child']]
```

Tradeoff: this is a season marker, not a remote baseline. A root without a `season:` field is conservatively retained; a pre-split snapshot with no season marker can still be selected. The local namespace is never used to repair the remote, and no remote evidence is claimed.

Tests were not executed in this constrained run; the fixture is present for the next run. The prior bare-remote evidence still covers exact push mechanics, while this round covers the previously missing post-split selection boundary.

## Agent Notes
Added season-based post-split root selection and regression fixture; tests not executed under the one-command constraint.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: the instruction said “changed since the 09-21 seed pass, or born after it,” not merely “season at least 2.” The machine at extensions/agi/bin/grid.py:197-204 filters only root commits whose node frontmatter has season < 2. My negative probe supplied a season-2 root with empty origin; push_batches returned it, so the 2,430 season-2 v1 snapshots created during the 09-21 seed are still selected. The near miss is a semantic season proxy that looks like a split boundary but does not encode the seed instant. Tests were not executed, the node itself admits unmarked roots remain selected, and no real remote/bare-remote evidence is supplied. The stop-on-failure behavior from the prior child remains acceptable, but the central selector is still disproved.
<!-- THOUGHT:END -->
