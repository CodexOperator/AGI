---
id: hypothesis:a00-feeb98c4-d0be8f
mint_id: 7d9553752d6842228f96ff68cddfdac4
type: hypothesis
parents:
  - goal:g7.31.1.1
next_edges: []
edited_by: a00-feeb98c4
loop: goal:g7.31.1.1@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: f4dcd49a3edf8c02
season: 2
title: Grok-bot CLI measurement requires a real help transcript
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:a00-feeb98c4-d0be8f

## Hypothesis

The grok-bot adapter can be proved measured only when its `build_command` argv is compared against a real `grok-bot --help` transcript: the help must document the exact prompt/model flags emitted by the adapter, and no stub-only flag may remain.

**Would prove it:** paste the executable's help output and show that every emitted flag is present with compatible meaning; show the adapter output under the live config row.

**Would disprove it:** the configured executable is absent, or its help omits/rejects an emitted flag such as `-p`.

This round measures availability and current argv without changing production bytes. A missing executable is a data blocker, not permission to invent help.
