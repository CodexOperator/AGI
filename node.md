---
id: idea:lm-jev-mcp-sandwich
mint_id: 6cc72c9cc13043b8b08518061dc040f4
type: idea
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
scaffold_hash: e19d2c3a53eeaa92
season: 2
title: "jev-MCP sandwich: a typed-decision layer before and after MCP that suggests, then auto-dispatches with an undo window, the next tool call"
town: core
---
<!-- BODY:BEGIN -->
# idea:lm-jev-mcp-sandwich

## Idea

What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
OWNER 2026-09-18 01:5xZ verbatim (via director-thought, "Relay to your master"): "a live transcript view with call suggestions, a three-layer jev-MCP sandwich: jev in front of MCP reading intent and suggesting MCP actions, and jev after MCP reading the pre-MCP jev inputs and dispatching tool-call suggestions to be confirmed or modified, eventually just auto-dispatched with a delay to allow undo for something like 10 to 60 seconds." SHAPE: layer 1 (pre-MCP) jev reads the live transcript + declared tools and emits a typed choice = the next MCP action (or none); layer 2 = MCP executes only what is confirmed; layer 3 (post-MCP) jev reads layer-1 inputs + the MCP result and dispatches the next suggestion; maturity ladder = suggest -> confirm/modify -> auto-dispatch with a 10-60 s undo window. FIRST MEASUREMENT before any UI = idea:lm-typed-decisions-in-the-loop round 2 (replay-200 from kid transcripts: top-1 agreement, USD/decision, latency); a sandwich earns a UI only if top-1 agreement on replayed calls clears a bar set from the replay (proposed 0.7) at < $0.001/decision. Sibling of idea:lm-typed-decisions-in-the-loop (schema: idea parents are goal|vision only, so parented on goal:g14). Blocked with it on the g15 key-forwarding fix.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by thought-master on the owner line of 01:5xZ 09-18; the replay-200 measurement comes first because a suggestion layer that disagrees with what agents actually do would add a confirm step to every call instead of removing calls.
<!-- THOUGHT:END -->

OWNER 2026-09-18 02:5xZ (via director-thought, continuing the sandwich thought): "I also thought that jev could help even in a more raw sense by automatically scaffolding MCP calls themselves to where LLMs only ever have to emit thought words or specific jev corrections. Fits right into the sandwich model just describing a very base level application." LAYER 0 (the base): the LLM emits INTENT words (+ corrections to a previous suggestion); jev choice/score over the tool roster and each tool closed-set argument scaffolds the concrete call; code validates types and dispatches -- the LLM never writes a tool-call JSON. It rides R2 (hypothesis:lm-jev-next-call-suggestion): metric 1 = tool top-1 agreement (already named), metric 2 = ARGUMENT agreement on closed-set args (add as a row), metric 3 = tokens saved per call (intent words vs the full tool-call JSON the kid actually emitted). SAFETY RULE (director-thought design risk, adopted): once jev scaffolds from intent and auto-dispatches after an undo delay, the delay is the only net -- so IRREVERSIBLE classes (delete, send, push, payment, spawn/kill) are CONFIRM-ONLY at every maturity level regardless of delay; delay-based auto-dispatch applies only to reversible/read-only calls, and the class of each roster tool is declared in code, never inferred by jev.
