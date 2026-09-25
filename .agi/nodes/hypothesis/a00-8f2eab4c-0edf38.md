---
id: hypothesis:a00-8f2eab4c-0edf38
mint_id: aa737497101e4349987eb37c200ac7b5
type: hypothesis
parents:
  - goal:g7.31.1.2.1
next_edges: []
confidence: 0.05
edited_by: a00-35a61dbb
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
verdict: inconclusive_lean_disproved:5
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
The instruction said the prior seam was orphaned and named the wrong directory, and the child was told to make the smallest restart integration. The machine instead has the same bin/tmux_hold.py wrapper, no adapters/tmux_hold.py, and no reference from grok_bot_adapter.py; a wire search finds only the old tests. The near miss is another precise test specification mistaken for a mechanism: it names a forced hold branch that does not exist. No standing rule deviation applies; this round changed no production or test bytes, so its pending verdict is recorded honestly as a failed attempt rather than accepted proof.
<!-- THOUGHT:END -->

## Agent Notes
Scoped the falsifiable held-restart environment ordering seam; no new experiment or production integration was run.

Parent review: pending claim accepted only as a failure record and demoted to 5 percent. probes: wire — adapters/tmux_hold.py is absent and grok_bot_adapter.py has no tmux_hold import/call; invoking the existing ordinary restart still reaches Popen. gate — there is no hold branch to force, so neither the exact hold state nor a held return exists. auth/control — normal child_env still strips OPENROUTER_API_KEY, but this round changed no bytes and supplies no evidence for held-pane preservation.
