OWNER DESIGN LAYER — 2026-09-07 04:40-07:36 UTC — SETTLED
ATTRIBUTION: owner text; relayed by Belam II (quotes 1-3) + Belam III (quote 4 = correction at 07:36 UTC). Source doc: `.agi/context/l3-command-ladder-brief.md`, section "Owner text 2026-09-07 - perpetual seats, the quorum as reviewer, the owner liaison".

SEATS (ALL PERPETUAL; each rotates on a loop at 0.35):
  - Belam (prime)
  - 3 advisors (quorum)
  - one director-kid PER perpetual goal
  - owner-liaison director-kid -> rotated BY THE QUORUM, owner's primary contact

MODEL TABLE (settled):
  - prime        -> Fable 5.1 max ultracode
  - quorum       -> Opus 5 max
  - director-kids-> Opus 5 high
  - liaison      -> Sonnet 5 high
  - pi parents/kids -> as now

SEAT REGISTRY (fields: session kind = remote-control/tty/fire-and-forget; personality ref; handoff; pin; rotated-by)
  - lives under goal:g17 "The seat system" -> build + config nodes
  - g16 renders LIVE stats incl. seat status

TRANSPORT:
  - perpetual seats NEED TTY / remote-control transport
  - NOT `claude -p`  (negation: bare non-interactive piped mode is forbidden for them)
  - send.py needs a tmux nudge

QUORUM REVIEWS ROUNDS:
  - 3-0 or 2-1 -> stands
  - 1-1-1 OR a morals flag -> audience (condition: goes to audience)
  - the prime is INBOX-ONLY and EXITS the room after an audience

COMMS LADDER (collapsed vs expanded):
  - collapsed: director-kids get NO free comms to Belam (negation)
  - expanded: free director-kid lateral comms + limited vertical comms to other director-kids
  - NO director reaches Belam EXCEPT through the quorum  (negation)
  - "the quorum IS Belam to anyone else"

SEQUENCING (order matters):
  seat registry + transport (first) -> liaison seat -> loops -> review-moves-down
  WAVE-4 label: l3w4-perpetual-seats

ADDENDUM (owner via Belam II):
  - `.agi/context/*.md` design docs have NO node/guard
  - => brief `l3w4-context-doc-nodes` under g13.1

OWNER QUOTE (5) 12:20 UTC — DRAFTING WORKFLOW:
  - uses Sonnet agents at the TOP effort
  - drafting is AGENT-AGNOSTIC (dispatch.py flips model/harness)
  - yet the owner STILL sees the interactive update (condition: not lost by model swap)
  - a `drafter` seat (Sonnet OR GLM flash) summons the drafting workflow
  - EVERYONE needing a brief goes THROUGH it
  - => briefed as `l3w4-drafter-seat` (8th wave-4 brief)

OWNER QUOTE (6) 12:25 UTC — WORKFLOW AGENT SWITCH:
  - switching workflow agents to opus/fable MUST be a config update OR a single-run override (condition; never a code edit)
  - later: fully model- and inference-provider-agnostic
  - DONE: script takes Workflow args {model, effort} (single-run override)
  - DONE: `.agi/config.json` `workflows.drafting` holds the default (sonnet/max/claude-code)
  - provider-agnosticism = requirement noted on l3w4-drafter-seat at mint

DONE SO FAR (recorded):
  - owner text recorded
  - goal:g17 minted
  - drafting run relaunched 12:22 UTC with Sonnet/max drafters
  - (first run died on the limit; second was stopped for the model switch)