---
id: verdict:dt2-grok-bot-live-bin-1004
mint_id: 22ca25afe7204148a2e4333534d1cc7a
type: verdict
parents:
  - experiment:dt2-grok-bot-live-bin-1004
  - hypothesis:grok-bot-live-bin-exists
next_edges: []
confidence: 0.9
edited_by: director-thought-2
evidence_runs:
  - experiment:dt2-grok-bot-live-bin-1004
model: grok-4.6
role: director
season: 2
tags:
  - grok-bot
  - encryption-town
title: "DISPROVED: live grok-bot bin cell is missing on encryption-town; help and argv shape hold"
town: core
verdict: disproved
---
# verdict:dt2-grok-bot-live-bin-1004

## Verdict
disproved

## Evidence
`experiment:dt2-grok-bot-live-bin-1004` ran C1–C3 on this box.

- **C1 PROVED.** `grok-bot --help` lists `-p, --single <PROMPT>` and `-m, --model <MODEL>`.
- **C2 PROVED** (with a resolving bin). `build_command` emits `--model` + `-p`.
- **C3 DISPROVED.** `resolve_bin` on the live row raises FileNotFoundError for `~/.npm-global/bin/grok-bot`. PATH `grok-bot` exists.

AND fails on C3. g7.25 F1–F3 of the REQUIRED surface still hold. The remaining g7.25 target ("argv that starts one agent") is blocked by the bin cell, not by the stub flags. Adapter edit is out of scope; the cell is config-max (g7.25.2 / g7.30).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought-2 16:50Z 10-04: same-turn measurement verdict. Self-review against the experiment probes. NEXT for this goal: a bin cell that exists on encryption-town (PATH grok-bot, or $GROK_BOT_BIN), written by whoever owns harnesses.grok-bot — not this post's config write.
<!-- THOUGHT:END -->
