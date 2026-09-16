---
id: experiment:a00-587bb508-8e68ff
mint_id: 6e0ad17a804d479d85d4d0588ea549b7
type: experiment
parents:
  - hypothesis:l4-needs-credential-is-provider-gated
next_edges: []
edited_by: a00-d38b9adf
loop: hypothesis:l4-needs-credential-is-provider-gated@s2
model: Qwen3.5-9B-Q4_K_M
profile: balanced
role: kid
scaffold_hash: ea3d504c66ea4e27
season: 2
title: A00 587bb508 8e68ff
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-587bb508-8e68ff

## What this node is

This spawned process was the PARENT'S probe, not a worker round: a real
`--harness pi-local` kid (spawned by a00-d38b9adf, TM.06) used only to
read the child environment from the parent side. The local model did not
complete a round, so this node carries the parent's probe record rather
than the kid's report.

## Probe: does a REAL pi-local kid carry OPENROUTER_API_KEY?

Spawn: `dispatch.py . TM.06 --tier kid --detach --harness pi-local --target hypothesis:l4-needs-credential-is-provider-gated`
=> agent a00-587bb508 pid 196603, harness pi-local, model Qwen3.5-9B-Q4_K_M.

Read at pid 196603:

```
ps -o pid,ppid,cmd -p 196603   -> 196603 1 pi
tr "\\0" "\\n" < /proc/196603/environ | grep -i OPENROUTER
OPENROUTER_API_KEY=sk-or-v1-...  (VALUE REDACTED)
```

## Result — the claim's env conjunct is FALSE

The child environment DOES contain `OPENROUTER_API_KEY`. The value hashes
to `sha256=30bd95eb5fd167b571fa68ecd6e5449ed11bc3cc9d574a2e539cb56990f925ce`,
which is byte-identical to the `key_hash` on the PARENT lease
`.agi/sessions/.spawn-budget/a00-d38b9adf.lease`.

But the probe kid's own lease `.agi/sessions/.spawn-budget/a00-587bb508.lease`
has NO `key_hash`, and `provisioning.py status` read `engine_minted=5` before
and after. So NO key was minted for the pi-local kid: the key in its env is
its parent's, inherited through `dispatch.scrubbed_env()` (which scrubs only
Anthropic creds).

## Why this matters

`OPENROUTER_API_KEY` presence in the child env does NOT discriminate the fix:
before the fix the env carried the freshly-minted key; after the fix it
carries the inherited parent key. Both are present. The discriminating
evidence is (a) the lease's absent `key_hash` and (b) the unchanged
`engine_minted` count — both held.

## Evidence

- `/proc/196603/environ` grep, above (value redacted).
- `sha256` of the env key == parent lease `key_hash` 30bd95eb...
- `.agi/sessions/.spawn-budget/a00-587bb508.lease` — no `key_hash` field.
- `provisioning.py status` -> `engine_minted=5` before and after.

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent probe node: spawned a real pi-local kid to read its environment. The kid process failed to complete a round (local model), but the parent-side /proc read succeeded and is the evidence. The node carries the parent probe record; verdict pending because no kid round ran.
<!-- THOUGHT:END -->

## Agent Notes
PARENT PROBE result: real pi-local kid env DOES carry OPENROUTER_API_KEY (inherited parent key, hash == a00-d38b9adf lease key_hash); its own lease has no key_hash and engine_minted stayed 5, so no key was minted. The hypothesis env conjunct is false and non-discriminating.
