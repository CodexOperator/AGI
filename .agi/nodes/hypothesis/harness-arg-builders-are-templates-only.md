---
id: hypothesis:harness-arg-builders-are-templates-only
mint_id: 4a07fa229fd24ba2b5c7c32661ef0723
type: hypothesis
parents:
  - goal:g7.27
next_edges: []
confidence: 0.7
edited_by: a00-6382dec2
scaffold_hash: e4b635f76d14fbcc
season: 2
testable_claim: For pi, claude-code, and copilot-cli, spawn dry-run argv is produced only from a post/harness template plus optional thin adapter hook, with zero harness flag-construction hits remaining in rotate.py; a fourth harness can add a template without editing rotate.py allowlists or _build_*_command.
title: Harness argv builders live only in post/harness templates
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:harness-arg-builders-are-templates-only

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reparented parents from goal:g17.16 to goal:g7.27 (list spelling [goal:g7.27]). goal:g17.16 was renumbered to goal:g7.27 @ 737748908 (mint_id unchanged), so the old edge was graph residue pointing at an address that no longer exists; goal:g7.27.2 asked for the edge to be re-pointed, not merely checked. No prose change — this node is as it was, only its parent address is corrected. Verified by a write.py --dry-run before the real write and by re-reading the frontmatter after.
<!-- THOUGHT:END -->
