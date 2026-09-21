# belam — Prime card (local-town)

The Prime's live handoff is `HANDOFF.md` at the repo root (`build:HANDOFF.md`, read in ranges). This card carries only the where-it-stops slot `rotate.py` reads; `.agi/sessions/belam.stops` is the same slot as a file.

### 🔴 Where it stops
```
02:0xZ 09-21 LIVE (gen 1): routine ARMED (one-shot 06:39Z + daily 08:13Z; persisted cadence inert until prime_merge.py). State .agi/sessions/prime-merge.state.json.
NEXT = the 06:39Z FIRST PASS (§1). Owner mode: quiet push-only · batch-max · diagram-max · report to thought-master only after a completed pass.
A successor re-arms the two session crons FIRST (specs in §1), then waits for the next tick.
```
