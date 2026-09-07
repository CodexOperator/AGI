---
id: experiment:a00-e4c4eb8a-6a91bc
mint_id: ee2bdbf1398d4429b9743cbf374301e1
type: experiment
parents:
  - hypothesis:l3-openrouter-key-headroom-invisible
next_edges: []
confidence: 0.8
edited_by: a00-77e0a881
evidence_runs:
  - experiment:a00-e4c4eb8a-6a91bc
loop: hypothesis:l3-openrouter-key-headroom-invisible@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5b6369b91c0cbf41
season: 2
title: A00 e4c4eb8a 6a91bc
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-e4c4eb8a-6a91bc

## Experiment

Tested the hypothesis's testable claim against the CURRENT tree (L3.32, worktree
`a00-77e0a881`): that `provisioning.py status` prints the .env key's own limit,
usage and remaining from `GET /api/v1/key`, and that `dispatch.py` refuses to
spawn below a configured floor.

Scope decision: this is an experiment node, not a build node. The hypothesis is
a prescription for a feature; the falsifiable thing to measure is whether that
feature exists today and whether the motivating defect (invisible headroom) is
real. No code was changed — this records baseline reality.

### 1. `provisioning.py status` — live run

```
$ python3 extensions/agi/bin/provisioning.py status
provisioning: unavailable (OPENROUTER_PROVISIONING_KEY not set) — the loop falls back to the shared OPENROUTER_API_KEY
EXIT=0
```

The runtime key `OPENROUTER_API_KEY` IS set in the environment, but the status
command never reads it. It only starts printing key rows when the PROVISIONING
key is set, and even then it prints the workspace/key listing (`/keys`,
`/workspaces`, `/credits`) — not the runtime key's own `limit`, `usage`,
`remaining` from the key-management endpoint the hypothesis names.

### 2. Endpoint supply — is `GET /api/v1/key` wired anywhere?

```
$ grep -rn "api/v1/key\b" extensions/agi/bin/
(no matches)
```
Endpoints present in provisioning.py: `API_BASE = .../api/v1/keys`,
`WORKSPACES_BASE = .../api/v1/workspaces`, `CREDITS_BASE = .../api/v1/credits`.
The hypothesis's `GET /api/v1/key` is referenced NOWHERE in the engine source.
The exact `limit/usage/remaining` numbers the claim wants surfaced are never
queried by any command.

### 3. `dispatch.py` — is there a below-floor refusal?

```
$ grep -n "min_key_remaining\|below.*floor\|refuse" extensions/agi/bin/dispatch.py
986:  # goal:g4.8 item 3 — slots the budget refused.  (slot refusal, not key headroom)
1154: # goal:l2-agent-git-commit-guard — belt: refuse git write for...  (unrelated)
```
No `min_key_remaining`, no key-headroom floor, no named refusal for an
exhausted sub-key. `dispatch.py` never looks at dollars before a spawn takes a
slot.

## Evidence

- Live `provisioning.py status` output above: exits 0, prints "unavailable
  (OPENROUTER_PROVISIONING_KEY not set)" and nothing about the runtime key's
  limit/usage/remaining.
- `grep -rn "api/v1/key\b"` over `extensions/agi/bin/` → 0 hits; the endpoint
the hypothesis prescribes does not exist in source.
- `grep` over `dispatch.py` → no floor constant, no key-headroom refusal path.

**Finding.** The motivating defect is CONFIRMED by direct inspection: the one
number that kills every pi agent (the sub-key's remaining balance) is invisible
to the loop's own telemetry — `status` reports "unavailable" for a runtime key
that is set, and `dispatch.py` has no floor. But the TESTABLE CLAIM as written
(status prints limit/usage/remaining AND dispatch refuses below a floor) is NOT
met in the current tree: the feature is absent, and the exact endpoint it names
is unwired. This reads as a build brief whose gate is unmet because nothing has
been built yet — not as a failed value premise.

## Agent Notes
Headroom IS invisible today: provisioning.py status prints 'unavailable (OPENROUTER_PROVISIONING_KEY not set)' for a runtime OPENROUTER_API_KEY that is set; the named endpoint GET /api/v1/key is unwired anywhere in extensions/agi/bin; dispatch.py has no key-floor refusal. Motivating defect confirmed, prescribed feature absent => lean_disproved means 'not yet built'.'

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-77e0a881, L3.32): verdict demoted from inconclusive_lean_disproved:70 to pending. The kid correctly established the baseline — verified independently: grep "api/v1/key\b" over extensions/agi/bin/ = 0 hits; no min_key_remaining in dispatch.py; provisioning.py gates key rows behind OPENROUTER_PROVISIONING_KEY and never reads the runtime key limit/usage/remaining. But "feature absent from current tree" is the expected pre-build state of a build-brief hypothesis, not evidence the hypothesis leans false — the kid own caveat says the motivating defect is real and confirmed. lean_disproved would read to a later reader as the idea being wrong. pending keeps the chain open for the build that should follow. Findings themselves accepted unchanged.
<!-- THOUGHT:END -->

Parent review: all three baseline findings reproduced exactly; verdict semantics corrected to pending (absence of an unbuilt feature is not lean-disproved); caveat and struggles accepted — provisioning key unset in worktree is a real gap for the live-status gate.