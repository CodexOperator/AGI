---
id: goal:g5.24.3
mint_id: a9e21b78a2c045f5bd0e66fb32bfa0c8
type: goal
parents:
  - goal:g5.24
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G5.24.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 7d6b42fcd1519fbc
season: 2
seeds:
  - hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens
status: active
tags:
  - local-maxxing
  - track-iii
  - magic-pane
title: "G5.24.3: THE MAGIC PANE -- a passive detector on the resident 9B predicts the structured form from the first prose tokens of a recorded agent stream, before the read-only tmux surface or the interruption protocol are attempted (owner 21:4xZ 09-20)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g5.24.3

## Agent Notes
**Owner source (2026-09-20 21:4xZ, verbatim on goal:g14):** "See if we can come up with a 'magic pane' that is a tmux pane surface that reads the raw prose tokens an LLM streams into it and suggests structured outputs it should use as instantaneous mid stream interruptions like autocorrect ... Call it the magic pane. A true LLM autocorrect and autofill that could genuinely save tokens. Just have link to it via cli." Side-track authorization (owner 01:2xZ 09-21, relayed TMM.16): "run jev and openjev research on the side to progress on the magic pane trajectory" — allowed alongside G5.27 (the switch), not blocking on it.

**Commits to.** The magic-pane half of G5.24, built in the three chunks G5.24 itself names: (1) an offline, passive detector that predicts which structured form (a `write.py note`, `write.py create <type>`, a tagged dm, an experiment node, a bench jsonl row, a `[merge-up]` line, a dispatch line) a recorded agent stream is about to produce, from only its first N prose tokens, using the resident local model — no engine code, no interruption of a live stream yet. (2) A read-only tmux surface that shows the suggestion beside a live stream, once chunk 1 clears its bar. (3) The interruption protocol itself (a CLI the streaming agent calls to hand tokens straight into the form's fields), measured for real token savings, only after chunks 1-2 hold.

**Invariants.** Every chunk reports precision/recall or accuracy against a majority-class baseline and latency per event; chunk 3 additionally reports tokens saved per form versus the same form written out normally, on >= 20 real events; nothing here touches `extensions/` (a script lives under `.agi/context/local-maxxing/magic-pane/`, the eventual CLI link is a one-line wrapper); the detector must run at <= 1.5s median on a local model or it cannot usably sit mid-stream regardless of accuracy.

**Falsifiers.** (a) Chunk 1 is falsified if top-1 form accuracy stays below 0.6 at 40 prose tokens AND still below 0.6 at 80 — then the next step is a form-specific prompt or a tiny fine-tuned classifier on the same labelled corpus, not a bigger model. (b) The whole goal is falsified if, once the interruption protocol chunk is reached, it saves less than 15% of the tokens of the forms it intercepts across >= 20 real events — an autocorrect that costs more than it saves is not kept.

**Done when.** A round's parent runs with the pane linked end to end, its forms are filled through the pane, the saving is measured on real events, and the pane is either handed to G5.27's eventual build as a component or retired with its numbers recorded.

**First chunk (minted):** `hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens` (MP.01) — the passive detector, chunk 1 only; chunks 2-3 (the tmux surface, the interruption protocol) wait on this one clearing its own bar. `openjev` (the trycua/cua open-source jev line the owner pointed at 2026-09-18) rides as a second kid of the same round if budget allows, or the next MP chunk otherwise — a reading digest, not a new sub-sub-goal of its own.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
owner ask 2026-09-21: renumber local-maxxing research g5.24.3 → g5.24.3 (g5 continuation after g5.21; mint_id preserved; town:local-maxxing kept); no director assignment
<!-- THOUGHT:END -->
