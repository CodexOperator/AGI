---
id: hypothesis:engine-tests-read-no-live-home-resource
mint_id: 76d99ccee97a46a79f76a2b69c9c780a
type: hypothesis
parents:
  - goal:g15.29.5
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 4896c3e131c0b524
season: 2
testable_claim: After the fix, test_migrate_channel.py's transcript-copy test (~853/~879) redirects rotate.CC_PROJECTS_DIR to a tmp fixture and asserts on that fixture instead of snapshotting the live ~/.claude/projects top level, which any concurrent Claude Code session can change mid-test; test_rolslice_rename.py resolves its graph ROOT through a path that exists (config:posts at .agi/nodes/.geometry/posts.md, or a fixture) instead of the absent seats.md; and rolslice.py's comment claiming a complement test (rolslice.py ~62-66) is made true by a committed test that every SKILL.md `## ` heading maps to CORE or ROLE_SECTIONS, or reworded to what is tested; no test in these files reads a path under the real home, and they stay green.
title: "Engine tests read no live home resource (assigned: director-engine)"
town: core
---
# hypothesis:engine-tests-read-no-live-home-resource

# hypothesis:engine-tests-read-no-live-home-resource

## Hypothesis

After the fix, test_migrate_channel.py's transcript-copy test (~853/~879) redirects rotate.CC_PROJECTS_DIR to a tmp fixture and asserts on that fixture instead of snapshotting the live ~/.claude/projects top level, which any concurrent Claude Code session can change mid-test; test_rolslice_rename.py resolves its graph ROOT through a path that exists (config:posts at .agi/nodes/.geometry/posts.md, or a fixture) instead of the absent seats.md; and rolslice.py's comment claiming a complement test (rolslice.py ~62-66) is made true by a committed test that every SKILL.md `## ` heading maps to CORE or ROLE_SECTIONS, or reworded to what is tested; no test in these files reads a path under the real home, and they stay green.

## Agent Notes
assigned: director-engine (leaf goal:g15.29.5; source R-EF41 D + M1 (live ~/.claude/projects read) · R-EF47 M1 (complement test claimed, absent) M2 (dead ROOT)); bytes verified by director-engine 18:2xZ 09-23 on the post tip f36cc2420 before minting.
