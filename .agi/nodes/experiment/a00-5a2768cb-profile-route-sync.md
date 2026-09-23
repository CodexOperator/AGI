---
id: experiment:a00-5a2768cb-profile-route-sync
mint_id: 5a57925eb0fd4fc9912a804bfedc18ca
type: experiment
parents:
  - hypothesis:a00-5a2768cb-6382c8
next_edges: []
edited_by: a00-5a2768cb
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 0656fc4db40fa33f
season: 2
title: Put the five contract routes into director-grok-internals SECTION:PROFILE
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-5a2768cb-profile-route-sync

# Experiment: the director grok cold-seat PROFILE block carries the five route names

Run node for `hypothesis:a00-5a2768cb-6382c8` (falsifier 1 of
`goal:g7.31.3.1`, residual left by
`experiment:a00-2f9d30c1-grok-profiles-route-names`).

## Claim under test

`doc:director-grok-internals` already carried the five contract route names
in its `## STANDING` block, but NOT inside `### SECTION:PROFILE` — the region
`doc:grok-harness-internals-sync` `SECTION:ROUTINE_SYNC` pastes into a cold
director bot's profile description. A line only in STANDING does not reach a
cold bot. This run puts the same line in `SECTION:PROFILE` and proves it on
the built bytes.

## Before (baseline `grep -n`)

```
$ grep -n "routes:" .agi/nodes/doc/director-grok-internals.md
152:routes: write·read·send·dispatch/workflow·rotate/spawn  (rename: route write → engine seam write.py)
```

One hit, in the STANDING region only. `### SECTION:PROFILE` (file line 55) had
none.

## Edit (write.py only)

```
$ printf 'AGI Texas two-step {{SEAT_LABEL}}. You are {{POST}} on grok-fast. Branch {{BRANCH}} ({{REMOTE_POLICY}}). Reports: {{REPORTS_TO}}.\nroutes: write·read·send·dispatch/workflow·rotate/spawn  (rename: route write → engine seam write.py)\n' \
  | python3 extensions/agi/bin/write.py doc:director-grok-internals 'replace body 36:36 -'
updated: doc:director-grok-internals
```

Canonical body line 36 was the `AGI Texas two-step …` description line; it was
replaced with itself plus the route line immediately after it. The STANDING
line (now file line 153) is untouched.

## After (byte proof)

```
$ grep -n "routes:" .agi/nodes/doc/director-grok-internals.md
58:routes: write·read·send·dispatch/workflow·rotate/spawn  (rename: route write → engine seam write.py)
153:routes: write·read·send·dispatch/workflow·rotate/spawn  (rename: route write → engine seam write.py)
```

The new file line 58 sits inside the `SECTION:PROFILE` block:

```
$ sed -n '55,64p' .agi/nodes/doc/director-grok-internals.md
### SECTION:PROFILE (copy into agent description)

AGI Texas two-step {{SEAT_LABEL}}. You are {{POST}} on grok-fast. Branch {{BRANCH}} ({{REMOTE_POLICY}}). Reports: {{REPORTS_TO}}.
routes: write·read·send·dispatch/workflow·rotate/spawn  (rename: route write → engine seam write.py)

## TOWN
```

## Probes

- **gate** — the `SECTION:PROFILE` region now names all five contracts:
  `write`, `read`, `send`, `dispatch/workflow`, `rotate/spawn`. The route line
  is inside the region bounded by `### SECTION:PROFILE` (file line 55) and the
  next header `## TOWN` (file line 62).
- **wire** — file line 58's nearest preceding header is `### SECTION:PROFILE`
  (file line 55), which is the region `doc:grok-harness-internals-sync`
  `### SECTION:ROUTINE_SYNC` names as the PROFILE source pasted into a cold
  director bot's description.
- **auth** — `.agi/sessions/write-log.jsonl` has
  `{"actor": "a00-5a2768cb", "node_id": "doc:director-grok-internals",
  "operation": "update_node", "ts": "2026-09-23T01:13:53.662395Z", ...}`.
  No hand edit.

## Result

`### SECTION:PROFILE` of `doc:director-grok-internals` lists the five contract
route names with the recorded rename, so the per-post SoT a cold grok
director bot syncs from now carries them. Falsifier 1 holds on the built bytes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Second run on this falsifier. The parent run put the route line in the wrong
region of the same file: STANDING, which is part of the per-post SoT but not
the `SECTION:PROFILE` region the sync routine pastes into the bot's profile
description — so a cold director bot could still have missed the five names.
This version moves the contract into the region that is actually pasted, and
keeps the STANDING copy. Differs from the parent run only in the target
region, the before/after greps, and the record of the `replace body 36:36`
verb that made it.
<!-- THOUGHT:END -->
