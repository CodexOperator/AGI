# spend.md — OpenRouter spend, GPU-endpoint hypothesis (`hypothesis:gpu-local-town-openai-endpoint`)

Written 2026-09-16 by agent `a00-73db9f50` (iter TM.09, Kid C hygiene round).
Scope: parent + kid OpenRouter spend for the hypothesis's two dispatched rounds
(**TM.03** = round 1, **TM.07** = round 2), read from `provisioning.py status` /
`list` / `spend`. The GPU itself is metered in electricity, not dollars — this
file covers only OpenRouter tokens spent *driving* the rounds.

## Method

```
python3 extensions/agi/bin/provisioning.py status   # live per-key rows
python3 extensions/agi/bin/provisioning.py list     # limits + expiry
python3 extensions/agi/bin/provisioning.py spend    # refresh .agi/sessions/.spend-captures/spend.json
```

Per-spawn keys carry a ~180-minute TTL. TM.03 keys were minted near
`2026-09-16T03:56Z` and expired ~`2026-09-16T06:56Z`; TM.07 keys expired
`2026-09-16T13:1xZ`. By the time this ledger ran (post `11:31Z`) **none of the
TM.03 rows were live**, so the live `status`/`spend` reads could not show them.
Fallbacks used, in order: (1) a frozen `provisioning.py status` capture saved in
the round's own context dir; (2) the per-key delta prose inside the round's
experiment node. No number below is invented; each row names its source.

## Rows

| round | agent | key | spend (USD) | expiry | source |
|---|---|---|---|---|---|
| TM.03 r1 | parent `a00-ab5b20f7` | `agi-iterTM.03-parent-a00-ab5b20f7` (name inferred, never observed) | **not recoverable** | ~2026-09-16T06:56Z | key name appears in no artifact; absent from all `spend.json` captures |
| TM.03 r1 | kid `a00-f2e3b48b` (Kid A) | — | **not recoverable** | ~2026-09-16T06:56Z | no key name in any artifact |
| TM.03 r1 | kid `a00-f98cb348` (Kid B) | `agi-iterTM.03-kid-a00-f98cb348` | 0.0151 → **0.0424** | ~2026-09-16T06:56Z | `experiment:a00-f98cb348-5f89c2` body, provisioning before/after |
| TM.07 r2 | parent `a00-1fec07a8` | `agi-iterTM.07-parent-a00-1fec07a8` | 0.012447546 → **0.012858372** | 2026-09-16T13:19:04Z | TM.07 numbers: `git show 35e071182:.agi/context/local-maxxing/gpu/kidA_round2_provisioning_delta.txt` — the live path's content has since changed |
| TM.07 r2 | kid `a00-4869b99b` | `agi-iterTM.07-kid-a00-4869b99b` | 0.008196342 → **0.008846166** | 2026-09-16T13:19:58Z | same blob (`git show 35e071182:…kidA_round2_provisioning_delta.txt`); the live path moved on |
| account | workspace `72750376-…` key `agi-2` | `agi-2` | **0.59690858** (all-time, not per-round) | none | live `provisioning.py status` / `spend.json` 2026-09-16T11:31Z |
| account | workspace `7e12bcd2-…` key `agi` | `agi` | **10.922531153** (all-time, not per-round) | none | live `provisioning.py list` 2026-09-16T11:31Z |

Interpretation note: the brief said "BOTH TM.03 rounds". The hypothesis was
dispatched twice — TM.03 (round 1: 9B server + tunnel) and TM.07 (round 2:
larger model + cost row). Both are tabulated above; if "both TM.03 rounds" meant
the two kid halves of round 1, those are the two TM.03 kid rows.

## What is measured vs not recoverable

- **Measured (frozen, per-key):** TM.03 Kid B 0.0424; TM.07 parent 0.012858372;
  TM.07 kid 0.008846166. These were captured in-round and survive in tracked files.
- **Measured (live, account-level):** `agi-2` 0.59690858 and `agi` 10.922531153.
  Account-level, shared by every agent on the box — not attributable to this round.
- **Not recoverable:** every TM.03 per-key row for the parent and Kid A. The key
  names are not present in any `spend.json` capture on disk (main checkout or any
  worktree), in any session log, or in any node — so neither `used=` nor the key
  name itself can be recovered. The account-level `agi-2` capture is the only
  bounded evidence for that round; it cannot be split per agent after the fact.
  Marking these explicitly rather than estimating: an estimate here would read as
  evidence.
- `OPENROUTER_API_KEY` account read is `unknown` (HTTP 401 "User not found") from
  this box, so no provider-side reconciliation is possible either.

## Round total where recoverable

TM.03 Kid B + TM.07 parent + TM.07 kid = 0.0424 + 0.012858372 + 0.008846166 =
**$0.0641** OpenRouter, attributable. The rest of the hypothesis's OpenRouter
cost (TM.03 parent + TM.03 Kid A) is not recoverable from any artifact on disk.
