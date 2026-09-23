# belam — Prime card (local-town)

The Prime's live handoff is `HANDOFF.md` at the repo root (`build:HANDOFF.md`, read in ranges). This card carries only the where-it-stops slot `rotate.py` reads; `.agi/sessions/belam.stops` is the same slot as a file.

### 🔴 Where it stops
```
06:4xZ 09-23 LIVE (gen 1, session resumed; the daily cron c5f0b2f3 survived, the 09-21/22 ticks did not fire while the process was down). season2/main = 0f336c890 (trunk @8cf1eb4c9). PASS 2 ARMED: delta 0f336c890..6d97bd855 = 62 commits · +7 exp · +7 hyp · 4 engine · 0 deletions; 5 h notice sent 06:41Z; one-shot at 11:41Z 09-23 (procedure in the cron prompt: chunks of <=5 launched as PARALLEL processes, verdicts read from .agi/sessions/workflows/runs/<run-key>/*.json, merge --no-ff in .agi/worktrees/prime-root, verify, push, residues -> g15 assigned director-engine, ONE report to thought-master). A successor re-arms the daily cron FIRST, then this one-shot if it has not fired.
```
