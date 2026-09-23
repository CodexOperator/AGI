---
id: experiment:a00-2f9d30c1-grok-profiles-route-names
mint_id: 62299528ebcc48a7b3526f12ea2e0fd7
type: experiment
parents:
  - hypothesis:a00-2f9d30c1-c2af1e
next_edges: []
edited_by: a00-2f9d30c1
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 25bb6fb6ec70f2c8
season: 2
title: Reconcile grok cold-seat PROFILE briefs to the five contract route names
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-2f9d30c1-grok-profiles-route-names
# Experiment: reconciling the two grok cold-seat PROFILE briefs to the five contract route names

Run node for `hypothesis:a00-2f9d30c1-c2af1e` (falsifier 1 of `goal:g7.31.3.1`).

## What I did

1. Audited every surface carrying a route list with `grep -n`.
2. Made both cold-seat PROFILE SoTs carry the five `goal:g7.31.3` contract names
   and record the deliberate rename, via the sanctioned `write.py` route.
3. Re-grepped the built bytes and read the write log.

## Before (baseline grep)

```
.agi/nodes/doc/director-grok-internals.md:152:routes: write.py · read · send · dispatch/workflow · rotate/spawn
.agi/nodes/doc/belam-grok-internals.md        (no route line in ### SECTION:PROFILE)
.agi/nodes/doc/unified-director-brief.md:36:routes write·read·send·dispatch/workflow·rotate/spawn
extensions/agi/briefs/director-belam-duties.md:14:routes: write·read·send·dispatch/workflow·rotate/spawn
```

## Edits (write.py only)

```
$ printf 'routes: write·read·send·dispatch/workflow·rotate/spawn  (rename: route write → engine seam write.py)\n' \
  | python3 extensions/agi/bin/write.py doc:director-grok-internals 'replace body 131:131 -'
updated: doc:director-grok-internals

$ printf 'Golden: harness data ← write.py graph only\nroutes: write·read·send·dispatch/workflow·rotate/spawn  (rename: route write → engine seam write.py)\n' \
  | python3 extensions/agi/bin/write.py doc:belam-grok-internals 'replace body 35:35 -'
updated: doc:belam-grok-internals
```

## After (byte proof)

```
$ grep -n "write·read·send·dispatch/workflow·rotate/spawn" \
    .agi/nodes/doc/director-grok-internals.md .agi/nodes/doc/belam-grok-internals.md
.agi/nodes/doc/director-grok-internals.md:152:routes: write·read·send·dispatch/workflow·rotate/spawn  (rename: route write → engine seam write.py)
.agi/nodes/doc/belam-grok-internals.md:58:routes: write·read·send·dispatch/workflow·rotate/spawn  (rename: route write → engine seam write.py)
```

Wire: `director-grok-internals` line 152's nearest preceding section header is
`55:### SECTION:PROFILE (copy into agent description)`; `belam-grok-internals`
line 58 sits inside `### SECTION:PROFILE` (line 49), right under `Golden:`.

Auth: `.agi/sessions/write-log.jsonl` records two `update_node` entries with
`"actor": "a00-2f9d30c1"` (ts 00:49:37Z and 00:49:41Z); `belam-grok-internals`
frontmatter carries `edited_by: a00-2f9d30c1`.

## Result

Both cold-seat PROFILE SoTs list all five contract names and the rename note.
Falsifier 1 as stated holds on the built bytes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Minted as the experiment child of `hypothesis:a00-2f9d30c1-c2af1e`
because the evidence gate will not let a hypothesis self-cite: a proven claim
needs a distinct experiment node behind it. Differs from the parent's node only
in being the raw run record — before/after greps, the exact write.py verbs, the
write-log provenance — rather than the claim's body.
<!-- THOUGHT:END -->
