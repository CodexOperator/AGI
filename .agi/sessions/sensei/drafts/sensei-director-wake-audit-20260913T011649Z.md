# sensei-director 17→18 — wake 4 (+2 refused, +3 hand-sync) / out 1 (record 20260913T011649Z; first sonnet-5 max wake; master-sensei gen 6, 01:3xZ)

OUT (gen 17, eb33e73a): 216 read dm · 217 F14 fetch+merge · 218 push + harvest-table · 219-220 SM.05 harvest (work) · 221-222 SM.03b dispatch (work) · 223 fetch+merge+push again · 224-225 stale-base grep + 3-try retry loop · 226 dm SM (last work act) · 227 rotate-self. **out = 1** (floor, 4th time). Inline cost 217/223/224/225 = 4 calls of F14/stale-base = SM.08.

WAKE (gen 18, aece205e, 01:21-01:24Z), first (d) = call 5:
- 1-3 `grep -rl <slug> .agi/nodes/hypothesis/` ×2 + `cat` the files (a: SM's dm carried the node ids; `write.py hypothesis:<slug> "read body 1:40"` is one call per node, by address — owner 22:3xZ: graph addresses, never fs paths)
- 4 `dispatch.py --help | head -60` (c: no -h on documented tools; the dispatch line is in the card §1b)
- 5-6 dispatch `--dry-run` ×2, 7-8 dispatch real ×2 → **both REFUSED `stale-base behind=4`** (2 failed calls): the worktree was cut at 01:16Z and MAIN took 4 commits (three after_join records + SM card) by 01:22Z
- 9-11 hand `git fetch` / `merge origin/season2/main` / `push` (3 calls) = the SM.08 root exactly — rotate-self counted behind against the stale local ref; and the refusal names the merge as text instead of performing it
- 12-13 dispatch OK · 14-16 quorum wc + Read + `date` (a: date is in every dm ts)
Regression 0 → 4 on the model switch; failed-call axis (owner 22:3xZ) = 2; the dry-run pair doubles every dispatch (2 → 4 calls per pair).
