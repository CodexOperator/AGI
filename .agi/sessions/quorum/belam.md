# belam — Prime card (local-town)

The Prime's live handoff is `HANDOFF.md` at the repo root (`build:HANDOFF.md`, read in ranges). This card carries only the where-it-stops slot `rotate.py` reads; `.agi/sessions/belam.stops` is the same slot as a file.

### 🔴 Where it stops
```
01:5xZ 09-21 LIVE (gen 1): merge routine ARMED — session: one-shot 06:39Z 09-21 (first mur+merge pass) + DAILY activation 08:13Z; persisted: cron:crons cadence prime_merge 13 */6 (inert until prime_merge.py lands; spec = hypothesis:prime-merge-routine-is-one-cron-script, assigned director-engine). State file .agi/sessions/prime-merge.state.json. NEXT = 06:39Z: mur over origin/season2/main..local-maxxing/season2/main (chunks <=6, pi, PI_BIN set), all-GO -> --no-ff merge by SHA into season2/main in .agi/worktrees/prime-root, verify, push, grid commit --all there, note on goal:g14, THEN one diagram-maxed report dm to thought-master; residues -> g15 rounds assigned director-engine. Owner: quiet push-only, batch-max, diagram-max. A successor re-arms the session crons FIRST.
```
