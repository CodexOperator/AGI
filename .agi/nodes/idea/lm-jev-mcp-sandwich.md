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

OWNER 2026-09-18 06:14Z (thought-master pane), verbatim: "Btw I was thinking for one ingest these and queue model downloads if it makes sense. https://arxiv.org/abs/2609.04010 https://arxiv.org/abs/2510.03215 But the kv cache comms protocol could be used to bridge multiple choice models like open jev with standard LLMs or diffusion augmented LLMs double augmented with our novel oscillator architecture via spike modeling. A magical stitching together of models and comms protocols maybe able to utilize the tiniest models. All seem to be qwen based which is nice. Or many at least." APPLY (thought-master): jev is a hosted API, so a literal KV bridge to it is not possible; the testable reading is a LOCAL multiple-choice model -- a tiny Qwen prompted (later fine-tuned) as the menu-answering model over the mirror-built choice set (hypothesis:lm-mirror-choices-for-act) -- whose KV a C2C fuser feeds into a standard receiver LLM (hypothesis:lm-c2c-kv-bridge-released-fusers, conjunct 3). Same Qwen tokenizer family on both ends is the constraint the owner notes; it holds for Qwen2.5/Qwen3 pairs the released fusers already target.

OWNER 2026-09-18 18:4xZ (thought-master pane), verbatim: "I figured out what was wrong, something is going on with the local power. Nothing on my end, we didnt break anything. As confirmed by our checks. Continue as you were outside of this, lets keep researching what we can using our own CPUs. We still have billions of transistors, I know we can keep developing our bitwise idea here and jev among others. I have $5 on two jev keys, idk if they got imported yet or not. If not I can import manually via safe SSH commands once I ssh into this box and cd into work/agi there are some import scripts already even I can call." KEY STATE (measured, names only, never values): the MAIN .env carries ONE TypeSafe row, TYPESAFE_KEY (envfile.py --check reads it); the TypeSafe SDK reads TYPESAFE_API_KEY (SM.103 brief line 27), so the SECOND key has a natural home: `python3 extensions/agi/bin/envfile.py --set TYPESAFE_API_KEY` from MAIN (prompts on the terminal, never echoed, never in argv or history) -- the owner path. BLOCKER for the jev rounds R1 (hypothesis:lm-jev-typed-acts-replay) and R2 (hypothesis:lm-jev-next-call-suggestion): the key does not reach a spawned kid yet -- the earlier replay measured TYPESAFE_KEY absent from the kid environment (typesafe/ledger.md, BLOCKED:no_key); the fix is SM.103 (config forward_env name list, hypothesis:l4-a-named-env-key-reaches-a-spawned-kid-...), briefed 09-18 02:2xZ, NOT landed as of 18:4xZ (no forward_env in config.json or dispatch.py on either trunk). Asked the SM for its status 18:4xZ. Both rounds are API-only ($1 OpenRouter + $0.50 / $0.30 TypeSafe ledger caps) and dispatch the moment the key reaches kids.
