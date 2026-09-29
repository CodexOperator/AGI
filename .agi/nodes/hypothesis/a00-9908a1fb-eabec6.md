---
id: hypothesis:a00-9908a1fb-eabec6
mint_id: fe6cdbd813704cc1b0f3b62d85927afc
type: hypothesis
parents:
  - goal:g7.31.4.1
next_edges: []
confidence: 0.9
edited_by: a00-9908a1fb
evidence_runs:
  - experiment:prompt-marker-write-guard-grant
loop: goal:g7.31.4.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: cbee1f2a058c9184
season: 2
testable_claim: "The predecessor's experiment node `experiment:prompt-marker-write-guard-grant` was authored but left untracked: the round-done scope rule (`cli.py::_round_scope_ok`) classifies a node whose basename lacks the round's agent id as FOREIGN, so `done` would not commit a turnkey human-slug node."
title: landed a foreign branch node verbatim through the same rule that excluded it
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-9908a1fb-eabec6

## Hypothesis

The predecessor's experiment node `experiment:prompt-marker-write-guard-grant`
was authored but left untracked: the round-done scope rule
(`cli.py::_round_scope_ok`) classifies a node whose basename lacks the round's
agent id as FOREIGN, so `done` would not commit a turnkey human-slug node.

**Claim:** such a node can be landed byte-identically from a new worktree by a
later agent, without re-authoring a byte, by naming it explicitly in `--owns`
(which puts it in own_paths); and the write-guard tests covering its subject
still pass against the base schema bytes.

Proved if: the copied file is byte-identical to the predecessor's and the
named test files pass. Disproved if the copy differs in any byte, or the
scope rule still refuses the node when owned.

## Agent Notes
landed the predecessor's untracked experiment node prompt-marker-write-guard-grant verbatim (byte-identical) via --owns so the round-done scope rule admits it; write-guard tests pass 31/31 on base schema bytes
