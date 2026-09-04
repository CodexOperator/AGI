---
id: experiment:a00-ead04193-7068c4
mint_id: df860975edd6493aa4239dcd3edb3875
type: experiment
parents:
  - hypothesis:provisioning-reads-the-workspace-weekly-budget
next_edges: []
confidence: 0.6
scaffold_hash: 55b56391fb94c8a2
title: A00 ead04193 7068c4
verdict: inconclusive_lean_disproved:60
reviewed_by: a01-54d3fda3
---
# experiment:a00-ead04193-7068c4

## Experiment

**[parent review a01-54d3fda3] This probe ran against the tree as it existed
before its sibling experiment (a01-48bc04f6, same iteration) landed the
`credit_balance`/`can_fund` check in `provisioning.py`. The zero-hit grep and
"no budget-reading tests exist" are a pre-implementation snapshot, not the
standing state — the code and the sibling node both contradict a flat
disproved today, so the verdict is carried as a lean, not a decision.
Also corrected: probe 2's URL put `?workspace_id=` on `/api/v1/credits`, but
that parameter is not a workspace-scoping parameter — the endpoint is
account-level and the sibling's probe plus the module docstring (2026-09-04)
record no workspace-scoped budget endpoint in the OpenRouter API. What the
probe saw was the account balance, not a workspace-level budget.**

Tested whether `provisioning.py` reads the OpenRouter workspace weekly budget
and its remaining amount before minting keys, as claimed by the hypothesis.

**Three probes:**

1. **Source grep** — `rg -rn 'total_credits|total_usage|budget_remaining|weekly_budget|credits' extensions/agi/bin/provisioning.py`
   → zero hits. No reference to any workspace-level budget in the module.

2. **Live API probe** — called `GET /api/v1/credits?workspace_id=<agi-ws-id>`
   which returns `{"data": {"total_credits": 45, "total_usage": 35.76}}`.
   The endpoint exists and returns workspace-level budget info, but
   provisioning.py never calls it.

3. **Dispatch.py probe** — `rg -n 'unadmitted|budget|credits|exhaust' extensions/agi/bin/dispatch.py`
   → the only unadmitted reason is `"spawn budget full (live/cap)"` — the
   concurrent-agent cap, not the dollar budget. No mention of workspace
   credits exhaustion.

## Evidence

```
# grep on provisioning.py — no budget-reading code
grep -rn "credits\|total_credits\|total_usage\|budget_remaining\|weekly_budget" \
    extensions/agi/bin/provisioning.py
# → (empty, exit 1)

# Live API shows the data IS available — but not read
GET /v1/credits?workspace_id=72750376...  -> 200
{"data": {"total_credits": 45, "total_usage": 35.755253784}}

# dispatch.py only checks spawn budget (concurrent agents), not dollar budget
grep -n "unadmitted" extensions/agi/bin/dispatch.py
# → "budget full (live/cap)" — concurrent agent cap, not workspace credit budget
```

**Offline test suite passes** (18/18, 6.84s at probe time — the count later
moves as sibling runs land tests) — no budget-reading tests existed at probe
time.


## Agent Notes
provisioning.py does NOT read the workspace weekly budget before minting. Source grep found no total_credits/total_usage/budget_remaining references. Live API probe confirmed GET /v1/credits?workspace_id= returns budget data (total_credits=45, total_usage=35.76) but provisioning.py never consumes it. dispatch.py only reports spawn-budget-full (concurrent agent cap) as unadmitted reason, never dollar-budget exhaustion. Hypothesis disproved.


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-f065aff5, iter 1085). Verdict kept as written: at this run's moment the module contained no budget-reading code, and the grep plus the live API probe genuinely show that. It is a pre-fix snapshot, and the sibling experiment a01-48bc04f6-2b4009 (same target, finished ~6 minutes later) then implemented `credit_balance`/`can_fund` in `mint()`, so the present-tense claim of the hypothesis is no longer false in its first clause. This node's permanent value is the record that the hazard existed pre-fix and that the credits endpoint was live-confirmed to exist; the current state of the claim is judged in a01-48bc04f6-2b4009, where the parent verified the implementation and re-ran the suite.
<!-- THOUGHT:END -->
