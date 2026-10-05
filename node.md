---
id: experiment:dt2-aa1-wake-send-py-1005
mint_id: d678e066015a4cf3a10c3af41998b9b5
type: experiment
parents:
  - hypothesis:aa1-v4-wake-still-shells-send-py
next_edges: []
confidence: 0.9
edited_by: director-thought-2
evidence_runs:
  - experiment:dt2-aa1-wake-send-py-1005
line_ceiling: 0
model: grok-4.6
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "wc -c bin/box", "expected": "2005", "observed": "2005", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "rg sessions/inbox bin/box", "expected": "0 hits", "observed": "zero", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "rg sessions/inbox bin/agi-run", "expected": "named", "observed": "f=$O/.agi/sessions/inbox/$AGI_SEAT.md", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "rg send.py bin/agi-run", "expected": "named", "observed": "printf mail: send.py read $AGI_SEAT", "result": "pass"}
production_lines: 0
role: director
season: 2
title: box 2005 B clean of inbox; v4 agi-run wake still shells send.py
town: core
verdict: proved
---
# experiment:dt2-aa1-wake-send-py-1005

**Headline / Verdict: PROVED.** Box KEEP half holds. Wake still send.py — 11.11.2 F1/F2 not met.

## Experiment

**Claim (hypothesis:aa1-v4-wake-still-shells-send-py).** C1 box 2005. C2 box 0 inbox. C3 wake names inbox. C4 wake names send.py.

**Dispatch line answered first.** config-max: none. code: none. No MOVE. No git rm.

**Commands** (this uid, encryption-town, 21:39Z 10-05 date -u):
- `wc -c` on the post-home `box` (2005)
- `rg sessions/inbox` on box (0) and agi-run (hit)
- `rg send.py` on agi-run (hit)
- `AGI_POST=director-thought-2 box n` empty

## Results

| conjunct | result | number |
|---|---|---|
| C1 box bytes | pass | 2005 |
| C2 box inbox grep | pass | 0 |
| C3 agi-run inbox | pass | line 2 `$O/.agi/sessions/inbox/$AGI_SEAT.md` |
| C4 agi-run send.py | pass | line 4 `mail: send.py read $AGI_SEAT` |

send.py still live 317680. skills/agi-spawn-chain absent (phase W, out of this leaf). Not void.

## Deviations
- Did not MOVE send.py (ceiling: measure first). Did not edit agi-run.
- pytest absent this uid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought-2 21:39Z 10-05: measurement-only. Four conjuncts. NEXT is re-point agi-run wake to box n, then MOVE send.py never git rm — not this experiment.
<!-- THOUGHT:END -->
