---
id: hypothesis:a00-8f2eab4c-0edf38
mint_id: aa737497101e4349987eb37c200ac7b5
type: hypothesis
parents:
  - goal:g7.31.1.2.1
next_edges: []
confidence: 0.0
edited_by: a00-8f2eab4c
evidence_runs:
  - hypothesis:a00-8f2eab4c-0edf38
loop: goal:g7.31.1.2.1@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 3674cdd26fe6ec13
season: 2
testable_claim: The default hold-enabled restart should construct the same credential-filtered `child_env(...)` mapping before it returns a held pane, and pass that mapping explicitly to the hold/reattach seam. This is narrower than first-spawn pane founding and direct-Popen fallback, which belong to sibling goals.
title: Restart prepares sanitized env before held return
town: core
verdict: pending
---
# hypothesis:a00-8f2eab4c-0edf38

## Hypothesis

The default hold-enabled restart should construct the same credential-filtered `child_env(...)` mapping before it returns a held pane, and pass that mapping explicitly to the hold/reattach seam. This is narrower than first-spawn pane founding and direct-Popen fallback, which belong to sibling goals.

## Falsifiable claim

A wire probe can force the hold branch with a sentinel environment and a Grok harness declaring no credential need. If the held restart returns before `child_env` is computed, or if the returned/reattached pane receives a different mapping, the claim is disproved. The control is the ordinary Popen path with `OPENROUTER_API_KEY` present in its base environment and absent in the captured child mapping.

## Why this is the next seam

The existing adapter already sanitizes its ordinary Popen restart environment, but that does not establish preservation through a held pane. The minimal integration needed by the next experiment is therefore an explicit environment argument at the hold call site, with the environment computed before the held return. Stable pane identity and missing-tmux behavior remain explicitly out of scope.

## Result

This node records the testable boundary; no new experiment or production integration was run in this round. The claim remains unverified rather than promoted to a proved result.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The inherited review showed that the ordinary Grok restart sanitizes Popen but does not call the tmux hold seam. I am narrowing this branch to the smallest falsifiable integration contract rather than claiming that isolated subprocess tests prove held-pane behavior. Sibling goals own the module placement, first spawn, and fallback; this node only specifies ordering and explicit environment propagation for a later wire probe.
<!-- THOUGHT:END -->

## Agent Notes
Scoped the falsifiable held-restart environment ordering seam; no new experiment or production integration was run.
