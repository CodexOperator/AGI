---
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
effort: M
id: "task:t-033"
mint_id: d68a7ad303d9439abb40f27c6467cab8
origin: build-site
parents:
  - hyp:environment-indexers-r2
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-033: Filesystem tree indexer"
type: task
---

**Description:** `filesystem_tree` indexer walks the target. Emits a `directory` node per dir and `file` node per file. Skips symlinks/unreadable with a per-entry warning. Determinism comes from sorted walking + T-005 id minting.

**Files:** `agi-tree/src/environment_indexers/filesystem_tree.py`, `agi-tree/src/environment_indexers/schemas/[filesystem_tree].md`, `agi-tree/tests/environment_indexers/test_filesystem_tree.py`

**Test Strategy:** Run indexer twice on a fixture (with one symlink and one chmod-000 file); assert id stability and that warnings list the skipped entries.
