---
id: task:t-033
mint_id: d68a7ad303d9439abb40f27c6467cab8
type: task
parents:
  - hyp:environment-indexers-r2
acceptance_criteria:
  - R2.1 (one node per dir + child node per file/subdir)
  - R2.2 (frontmatter conforms to filesystem-tree schema)
  - R2.3 (symlinks/unreadable entries skipped with per-entry warning
  - run continues)
  - R2.4 (re-running yields same ids and parent-child links)
blocked_by:
  - task:t-032
  - task:t-031
  - task:t-005
cavekit_req: environment-indexers/R2
edited_by: season.py
effort: M
origin: build-site
season: 1
status: deprecated
tags:
  - M
  - tier--1
thought_session: season
tier: -1
title: "T-033: Filesystem tree indexer"
---
**Description:** `filesystem_tree` indexer walks the target. Emits a `directory` node per dir and `file` node per file. Skips symlinks/unreadable with a per-entry warning. Determinism comes from sorted walking + T-005 id minting.

**Files:** `agi-tree/src/environment_indexers/filesystem_tree.py`, `agi-tree/src/environment_indexers/schemas/[filesystem_tree].md`, `agi-tree/tests/environment_indexers/test_filesystem_tree.py`

**Test Strategy:** Run indexer twice on a fixture (with one symlink and one chmod-000 file); assert id stability and that warnings list the skipped entries.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R2` under `hyp:environment-indexers-r2`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->