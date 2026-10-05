---
id: verdict:dt2-grok-bot-restart-none-1005
mint_id: 19c2dd3434864bbf9bac7b7c8d5f8201
type: verdict
parents:
  - experiment:dt2-grok-bot-restart-none-1005
  - hypothesis:grok-bot-restart-degrades-to-none
next_edges: []
confidence: 0.9
edited_by: director-thought-2
evidence_runs:
  - experiment:dt2-grok-bot-restart-none-1005
model: grok-4.6
role: director
season: 2
tags:
  - grok-bot
  - encryption-town
title: "PROVED: grok-bot restart returns None on missing bin and on empty prompt"
town: core
verdict: proved
---
# verdict:dt2-grok-bot-restart-none-1005

## Verdict
proved

## Evidence
`experiment:dt2-grok-bot-restart-none-1005` ran C1–C2 on this box.

- **C1 PROVED.** live-row restart with missing bin → `None`; named FileNotFoundError on stderr; no child.
- **C2 PROVED.** empty prompt with PATH bin → `None`; named ValueError on stderr; no child.

AND holds. g7.25 F4 (restart callable) still holds; the degrade arm now has evidence. A successful restart (new pid) is still blocked on the bin cell / `$GROK_BOT_BIN`. This post did not write either. Did not implement mint or zygote.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought-2 04:54Z 10-05: same-turn measurement verdict. Owner wake thought-lane. NEXT still the cell/env write, not this post.
<!-- THOUGHT:END -->
