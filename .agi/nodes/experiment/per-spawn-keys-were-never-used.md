---
id: experiment:per-spawn-keys-were-never-used
mint_id: 4f7eb9f245f4477fa82bb7799a6df328
type: experiment
parents:
  - hypothesis:a01-3c5640a0-5c684c
next_edges: []
confidence: 1.0
edited_by: director
evidence_runs: 2
scaffold_hash: e3c279cc48922f53
thought_session: L1.07
title: The first live pi agents on minted keys — and the keys were never used
verdict: disproved
---
# experiment:per-spawn-keys-were-never-used

## Experiment

Two live dispatches against `goal:g1.11`, the first ever with real pi agents
rather than a stub that dumps its environment and exits.

```bash
python3 extensions/agi/bin/dispatch.py "$PWD" 1002 --tier kid --target goal:g1.11 --level small   # 2 kids
python3 extensions/agi/bin/dispatch.py "$PWD" 1003 --tier kid --target goal:g1.11 --level small   # 1 kid, after the fix
```

**Part A's claim was disproved.** `hypothesis:a01-3c5640a0-5c684c` asserts a
real agent "authenticates against OpenRouter using the minted per-spawn key
(injected as `OPENROUTER_API_KEY`)". It does not. It authenticates with the
**shared long-lived key**, and the minted key is never used by anything.

## Evidence

### Run 1002 — minted, injected, and ignored

Both kids were spawned with minted keys. The environment injection is real —
read from `/proc/<pid>/environ` of a live kid, not from the engine's own logs:

```
OPENROUTER_API_KEY=sk-or-v1-080a1439…     # != the shared key in .env
OPENROUTER_PROVISIONING_KEY               # 0 occurrences — the scrub works
```

And yet the bill said otherwise:

```
agi-iter1002-kid-a00-0fe61f28   usage=0            limit=5
agi-iter1002-kid-a01-3c5640a0   usage=0            limit=5
agi (shared, long-lived)        usage 4.433 -> 4.455 DURING the run
```

**The cause.** pi does not read `OPENROUTER_API_KEY`. Its `~/.pi/agent/auth.json`
uses the `"!command"` indirection form and points at the engine's own script:

```
"openrouter": {"type": "api_key",
               "key": "!…/extensions/agi/bin/env-get.sh OPENROUTER_API_KEY"}
```

`env-get.sh` sourced `.env` **unconditionally** and never consulted the
environment. So `dispatch.py` minted a capped, expiring, per-agent credential,
injected it correctly, and pi looked straight past it at the shared key.

### Why every prior test passed

`verdict:per-spawn-beats-batching` proved this path against a stub that dumps
its environment. **A stub that reads `$OPENROUTER_API_KEY` proves the
injection happened; it cannot prove the harness reads what was injected** —
and the one harness this project actually spawns does not. `env-get.sh` had
**zero test coverage**, which is why a two-line gap survived under a feature
that was otherwise carefully built and measured.

### Run 1003 — the same dispatch, after the fix

`env-get.sh` now prefers an already-set environment variable over the file.
One kid, nothing else changed:

```
agi-iter1003-kid-a00-41b7df72   usage=0.002118923   limit=5     <- spend, on its own name
agi (shared, long-lived)        usage=4.468721168               <- pre-run value, unchanged
```

**Attribution is now proved by a bill rather than by a naming convention**,
which is `goal:g1.11` requirement 5 and the first time it has held.

### Second defect, found in the same run: the reaper was blind

`GET /api/v1/keys` is scoped to the **default workspace** and does not say so.
Keys minted into the `agi` workspace (L1.01) were invisible to `list_keys`, so:

- `provisioning.py status` reported `engine_minted=0` while two keys were live;
- `reap_orphans` iterates that same listing, so it revoked **nothing** while
  truthfully reporting "0 orphaned keys" — about the wrong set.

The workspace move was made for safety, and for ~40 minutes it made the
backstop strictly worse than before: the prior hazard was a reaper revoking
too much, this one was a reaper revoking nothing, silently. Fixed by scoping
the listing (`list_keys(workspace_id=…)`) and adding `list_all_keys`, which
enumerates workspaces first.

### What did hold

- **Injection**, verified from `/proc`: the kid's key is not the shared key.
- **The scrub**: zero `OPENROUTER_PROVISIONING_KEY` in a kid's environment.
- **Revoke-on-reclaim**, live for the first time: kid `a01` exited, its lease
  was reclaimed, and its key was revoked without anything being asked to.
- **Zero outstanding keys** after the run, once `status` could see across
  workspaces to check honestly.

## What is NOT proved

- **Concurrency.** These ran at `spawn.parallel` 2 and 1. `goal:g4.8`'s cap of
  25 is untouched, and `mvp:the-bound-under-real-agents` still owns it.
- **The provisioning-absent fallback (Part B).** Not run. The code path is
  unchanged and `test_mint_returns_none_rather_than_raising_when_unavailable`
  covers the unit, but the live half of the falsifier is still open.
- **Whether any other harness reads the environment.** Only pi was tested, and
  pi turned out to be the counterexample. `claude_code_adapter` is a stub.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This node records a disproof, and the disproof is worth more than the feature it broke. `goal:g1.11` was built carefully, measured against the live API, and shipped with three independent limits -- and it was decorative, because the one thing never tested was whether the harness reads the variable the engine sets. Every test that could have caught it was written against a stub chosen to make the assertion easy, and the assertion it made easy was the wrong one: it proved the engine's half of a two-party contract.

The general lesson is about where a seam gets tested, not about pi. A mock that stands in for the counterparty can only ever confirm what the author already believed the counterparty does. `env-get.sh` -- the actual seam, thirty lines of bash, the single point where the engine's credential meets the harness's auth -- had no tests at all, and its docstring described its cwd-anchoring hazard in detail while saying nothing about precedence, because precedence had never been thought about.

Recorded as `disproved` rather than softened. The hypothesis's Part A is false as written, and the fix does not make it retroactively true; a later reader deserves to find that the claim failed and why, not a repaired claim with the failure edited out.
<!-- THOUGHT:END -->