---
id: hypothesis:harness-arg-builders-are-templates-only
mint_id: 4a07fa229fd24ba2b5c7c32661ef0723
type: hypothesis
parents:
  - goal:g17.16
next_edges: []
confidence: 0.7
edited_by: director-helper
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
