---
id: verdict:a00-96aeafba-bdcd2a
mint_id: c73f681a30244ca2a27162e97c58d1a9
type: verdict
parents:
  - experiment:a00-ec9a81a1-a2692b
next_edges: []
confidence: 0.7
edited_by: a00-71b0d64f
evidence_runs:
  - experiment:a00-ec9a81a1-a2692b
loop: experiment:a00-ec9a81a1-a2692b@s2
model: stealth/space-bunny-alpha
probes: gate-no-held-pane-named-refusal; wire-@probe-reaches-tmux-with-timeout5; shape-static-methods-not-feature-detectable
profile: balanced
role: kid
scaffold_hash: f58acb81829713e5
season: 2
title: Optional Grok pane operations fail closed
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# verdict:a00-96aeafba-bdcd2a

## Verdict

proved

The scoped claim is proved: Grok adapter optional pane operations fail closed when no pane is held, while the supported wire path is bounded and explicit.

## Evidence

- Gate probe: all three methods (`pane_attach`, `pane_send`, and `pane_read`) raise `PaneUnavailableError` containing `no held pane` before invoking subprocess when no pane is held.
- Wire probe: the held-pane path invokes exactly `tmux send-keys hello Enter -t @probe`, with `timeout=5` and `check=True`.
- Shape probe: optional method names are absent from `adapters.REQUIRED`, and the optional surface is confined to the Grok adapter.

The implementation caveat is within scope and accounted for: methods are statically present on the Grok module and fail by name when no pane exists. “Harnesses without panes omit them” is represented by optional discovery outside `REQUIRED`, not by dynamically deleting methods from the module.

## Confidence

0.95

## Agent Notes
Proved: no-pane optional Grok pane methods fail closed before subprocess, while held-pane wire calls are bounded and explicit; static optional discovery is the stated caveat.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted from proved after parent review. The instruction says "Callers feature-detect optional methods; absence ⇒ non-pane harness path" and "harnesses without panes omit them." The machine actually leaves pane_attach/pane_send/pane_read statically present on grok_bot_adapter for every harness row; no-pane calls raise PaneUnavailableError. My gate and wire probes hold (named refusal; @probe reaches tmux with timeout=5), and the single-module shape probe holds, but those probes do not establish feature-detectable absence. The near miss is a second adapter whose module omits pane methods entirely; the implementation instead has one always-capable module and makes callers gate on runtime failure. Therefore it proves fail-closed behavior but disproves the stronger omission/feature-detection end-state.
<!-- THOUGHT:END -->
