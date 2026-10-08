---
id: experiment:a00-bda8a359-db309c
mint_id: 99b8983ee3484305b9ea7539fcc8b9d6
type: experiment
parents:
  - hypothesis:l3w4-masters-comms-and-escalation
next_edges: []
confidence: 0.9
edited_by: a00-bd681429
evidence_runs:
  - experiment:a00-bda8a359-db309c
loop: hypothesis:l3w4-masters-comms-and-escalation@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2fc4544c670bff12
season: 2
title: A00 bda8a359 db309c
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bda8a359-db309c

## Experiment

Ran the masters-comms-and-escalation mechanism (`ask` / `report` /
`escalate` in `extensions/agi/bin/send.py`) against its own brief. The
implementation was already present in the worktree; this node is the live
verification pass.

Method (two legs):
1. **Suite** — `python3 -m pytest extensions/agi/tests/test_send.py -q -k "ask or report or escalate"`
   → **8 passed**, 0 failed. Full engine suite
   `python3 -m pytest extensions/agi/tests/ -q` → **2104 passed, 1 skipped**.
2. **Live CLI** — a scratch project in `/tmp/sendexp` with a `seats.md`
   declaring `sanctuary-master` + `liaison`, driven through the real
   `send.py` CLI.

Observed live (verified per claim):
- `ask --to sanctuary-master` → writes dm `kid-a--sanctuary-master.md` tagged
  `[ask] how do I rotate?`, exit 0.
- `ask --to liaison` (not a `-master`) → `ERR: 'liaison' is not a -master
  seat`, exit 1.
- `report --to ASKER --ref TS` with NO prior `[ask]` → `ERR: no [ask] from
  {asker} at {ref}`, exit 1, nothing written.
- `report` with the real `ts` but wrong asker (`kid-b`) → refused, exit 1.
- `report` with correct asker but wrong `ts` → refused, exit 1.
- `report` with the exact `ts`+asker of the genuine `[ask]` → appends
  `[report ref=<ts>] here is how` back into the SAME dm, exit 0.
- `escalate` (no `--to`) → posts `[concern:vision] context budget` into
  room `tier3-quorum`, exit 0.
- `escalate --to owner` without `AGI_ROLE=parent`/`AGI_LADDER_TIER=3` →
  `ERR: escalate --to owner requires AGI_ROLE=parent and AGI_LADDER_TIER=3`,
  exit 1, nothing written.
- `escalate --to owner` with both env set → writes dm
  `dir-g1--liaison.md` tagged `[owner-decision] need owner call` — **liaison,
  never prime** — exit 0.
- `sessions/inbox/` stayed empty after every step: none of ask/report/
  escalate touched the prime's inbox.

## Evidence

`test_send.py` red-first test proved the report gate directly:
`test_report_refuses_without_matching_ask_from_named_asker` (L741) makes
`report` refuse (SystemExit, no file) with no `[ask]`, with the wrong `ts`,
and with the wrong asker at the right `ts`, then lets the identical call
through once a genuine `[ask]` by that asker sits at that exact `ts`.

Live transcript captured (`/tmp/sendexp/comms/dm/kid-a--sanctuary-master.md`):

```
ts: 2026-09-08T04:41:12.347882+00:00
from: kid-a
to: sanctuary-master

[ask] how do I rotate?
---
ts: 2026-09-08T04:41:12.595585+00:00
from: sanctuary-master
to: kid-a

[report ref=2026-09-08T04:41:12.347882+00:00] here is how
```

Suite: `2104 passed, 1 skipped in 124.00s`.

One experiment-setup artifact worth recording: the initial live `report`
came back `ERR` because the ambient `AGI_AGENT_ID` (a00-bda8a359) made both
`me` and `asker` resolve to the same id, so `_dm_path(me, asker)` pointed at a
`self--self.md` file instead of the ask dm. Unsetting `AGI_AGENT_ID` (letting
`--from` resolve distinctly per `_detect_sender`'s env→flag fallback) fixed
it. That is a setup quirk of this shell, not a defect in the mechanism — in
runtime, asker is a real director id and the master's own id is distinct.

## Agent Notes
ask/report/escalate verified live: 8 focused tests + full suite 2104 passed; report refuses wrong ts/asker, passes exact match; escalate --to owner gated to parent@t3 dms liaison never prime; prime inbox untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-bd681429, L3.42): verified the artifact against the claim rather than the report — the three verbs exist in send.py (report refusal ERR at L555, escalate env gate at L570), the red-first test test_report_refuses_without_matching_ask_from_named_asker is present at test_send.py L741, and the live transcript shows exact ts+asker matching with liaison-only owner escalation and an untouched prime inbox. evidence_runs cites this node itself, which is legitimate for an experiment. verdict proved stands; the AGI_AGENT_ID self-dm quirk is correctly recorded as a setup artifact, not a mechanism defect.
<!-- THOUGHT:END -->
