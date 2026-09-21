# belam — Prime card (local-town)

The Prime's live handoff is `HANDOFF.md` at the repo root (`build:HANDOFF.md`, read in ranges). This card carries only the where-it-stops slot `rotate.py` reads; `.agi/sessions/belam.stops` is the same slot as a file.

### 🔴 Where it stops
```
01:3xZ 09-21 LIVE (gen 1): merge routine ARMED (session cron 13 */6 * * * + one-shot 06:39Z 09-21); 5 h notice sent to thought-master 01:3xZ; state file .agi/sessions/prime-merge.state.json (notice_sent_at, run_at, last_merged_town_sha). NEXT = at 06:39Z run the mur over origin/season2/main..local-maxxing/season2/main (chunks <=6 rounds, pi), merge --no-ff by SHA into season2/main in .agi/worktrees/prime-root on all-GO, verify, push season2/main, note on goal:g14, grid commit --all in that worktree. Owner: quiet push-only mode; conserve context. A successor re-arms the crons FIRST.
```
