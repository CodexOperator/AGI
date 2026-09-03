---
id: mvp:a-live-loop-on-minted-keys
mint_id: b30be1ab97d049c7bdbc91e38d76a9e4
type: mvp
parents:
  - verdict:per-spawn-beats-batching
next_edges: []
confidence: 0.8
edited_by: director
scaffold_hash: fe6f7690615aa0b4
status: open
thought_session: L1.01
title: A real loop where every agent authenticates with a key that did not exist before it
---
# mvp:a-live-loop-on-minted-keys

## What this must satisfy

`verdict:per-spawn-beats-batching` proved the credential path against a stub
that dumped its environment and exited. **No pi agent has ever authenticated
with a minted key.** That is `goal:g1.11`'s falsifier's first clause and the
one thing between "the mechanism works" and "the loop runs on it".

### The interfaces

Nothing new. `dispatch.py` already mints, injects and attaches; `spawn_budget`
already revokes on reclaim; `provisioning.py reap` already exists as the
backstop. This mvp is **execution, not construction** — which is itself the
finding, because a mechanism that needs no new code to go live is one whose
seam was drawn in the right place.

### The invariants

1. **Every spawned agent's key is one minted for it.** Verified from the
   OpenRouter dashboard by name — `agi-iter<N>-<tier>-<agent>` — not from the
   engine's own logs, which are the thing under test.
2. **Zero engine-minted keys survive the run.** `provisioning.py reap` reports
   0 orphans after the loop ends and after a deliberate mid-run kill of the
   director.
3. **Spend is attributable.** At least one key shows non-zero usage against
   its own name, which is the first time attribution is proved by a *bill*
   rather than by a naming convention.
4. **A `SIGSTOP`ped agent holds its slot.** Correct behaviour — it is alive to
   `os.kill(pid, 0)` — and worth observing once at cap 25 rather than
   discovering during an incident.

### The falsifier

One live iteration at `spawn.parallel: 5`, `spawn.max_live: 25`. Every agent
runs on a minted key; the run completes; `reap` finds nothing; at least one
key shows usage. Then repeat with `OPENROUTER_PROVISIONING_KEY` unset — the
loop still runs, on the shared key, with no code path changed. **Both halves
are required**: a hardening feature that becomes a hard dependency has made
the project more fragile while calling itself hardened.

### The risk this run actually carries

25 concurrent pi agents is well past the ~4 where rate-limit deaths were
measured. That is the point of the credit cap: a wave of failures costs at
most `25 x $0.25`, and the caps are what make running the experiment at all
a bounded decision rather than an open one.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The two open questions on this mvp are now settled, both by measurement rather than by argument. (1) WALL TIME: mint is 0.760s mean, 10 concurrent in 0.919s wall. The owner ruled this acceptable on 2026-09-03 on the ground that inference already faces 1-3s of latency, so an extra fraction of a second is inside the noise it hides in. The cost objection that motivated batching is therefore closed, not deferred. (2) WORKSPACE: keys now mint into the owner OpenRouter agi workspace (72750376-2d45-452e-8273-197fdaabae95), asserted against the live API before the code was written -- POST /keys accepts workspace_id, returns it on the created object, and a probe key landed there and was revoked. This is a SAFETY change, not tidiness: reap_orphans matched the name prefix agi- while the owner own long-lived key is named agi, so one character separated the reaper from the key the project runs on. The workspace filter is a second, independent ground on which that key is out of scope. Per-key cap raised 0.25 -> 5.00 USD at the owner direction. Measured account state at this edit: 20.00 total credits, 4.43 used, 15.57 remaining -- so the 5 USD cap is three keys deep, not twenty.
<!-- THOUGHT:END -->