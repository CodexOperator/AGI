---
id: goal:g14.8
mint_id: 1172f17d357148e4825aed8fcf27530e
type: goal
parents:
  - goal:g14
next_edges: []
confidence: 0.6
edited_by: thought-master
goal_id: G14.8
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 55ddc92f0bde4f69
season: 2
seeds:
  - idea:lm-magic-pane-llm-autocorrect-and-autofill
  - doc:typesafe-ai-skill
  - hypothesis:lm-jev-docs-hunt
  - hypothesis:lm-jev-ece-is-a-pooling-artifact
  - hypothesis:lm-jev-next-call-suggestion
  - hypothesis:lm-jev-q1-label-is-ambiguous
  - hypothesis:lm-jev-residual-is-corpus-composition
  - hypothesis:lm-jev-reviewer-evidence-attached
  - hypothesis:lm-jev-surface-lexical-beats-jev
  - hypothesis:lm-jev-typed-acts-replay
  - hypothesis:lm-mirror-choices-for-act
  - hypothesis:lm-typesafe-replay-200
  - idea:lm-cua-bench-as-typed-acts-source
  - idea:lm-jev-mcp-sandwich
  - idea:lm-typed-decisions-in-the-loop
status: active
tags:
  - local-maxxing
  - track-iii
  - jev
  - magic-pane
title: "G14.8: TRACK III — jev optimisations: local jev first, the API-key side, and the MAGIC PANE (a tmux surface that reads an LLM stream, detects the structured form, interrupts like autocorrect, fills the fields, confirms the final form; CLI-linked; token savings measured) (owner 21:4xZ 09-20)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.8

## Agent Notes
**Owner source (2026-09-20 21:4xZ, verbatim on goal:g14):** "I also wanna pursue more jev optimizations: Local jev stuff especially but also the api key stuff. See if we can come up with a 'magic pane' that is a tmux pane surface that reads the raw prose tokens an LLM streams into it and suggests structured outputs it should use as instantaneous mid stream interruptions like autocorrect like oh you want this structured form rescaled and the next tokens you stream will go straight in the body or whatever appropriate fields just fire them all off I'll distribute and confirm final form. Call it the magic pane. A true LLM autocorrect and autofill that could genuinely save tokens. Just have link to it via cli."

**Commits to.** The jev line (the local judge of typed engine acts) continues on the local models first; the API-key side (per-kid endpoint keys, G14.4's consumer) is kept measurable; and the **magic pane** is built in small chunks as a research tool, not engine code: (1) an offline detector that predicts the structured form from the first prose tokens of a recorded stream; (2) a read-only tmux surface that shows the suggestion beside a live stream; (3) the interruption protocol — a CLI the streaming agent calls to hand the next tokens straight into the form's fields, with the pane distributing and confirming the final form; (4) measured token savings on real rounds. Local models only (the 9B on `:8080` or smaller); the pane never edits a node itself — it proposes, the agent confirms through `write.py` / `send.py`.

**Invariants.** Every chunk reports precision/recall or accuracy against a majority baseline, latency per event, and — from chunk 3 — tokens saved per form versus the same form written out by the agent, on ≥ 20 real events; no chunk touches `extensions/` (a kid may write a script under `.agi/context/local-maxxing/magic-pane/`; the CLI link is a one-line wrapper); the detector runs on a local model at ≤ 1.5 s median or it is not usable mid-stream.

**Falsifiers.** (a) The detector is falsified if top-1 form accuracy stays < 0.6 at 80 prose tokens (then a form-specific prompt or a tiny classifier is the next chunk, and if that also fails the pane is retired). (b) The goal is falsified if the interruption protocol saves < 15 % of the tokens of the structured forms it intercepts on ≥ 20 real events — an autocorrect that costs more than it saves is not kept.

**Done when.** A round's parent runs with the pane linked, its forms are filled through the pane, the saving is measured, and the pane is handed to G14.11's build as a component or retired with its numbers.

**First chunk (minted):** `idea:lm-magic-pane-llm-autocorrect-and-autofill` → `hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens`. Sub-sub-goals are the director's to mint (G14.8.1 local jev, G14.8.2 API-key side, G14.8.3 the magic pane), same format, before any chunk runs.
