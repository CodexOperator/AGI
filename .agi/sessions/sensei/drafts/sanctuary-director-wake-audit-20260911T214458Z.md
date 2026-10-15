# sanctuary-director wake audit — record 20260911T214458Z (successor `[27c314]`; predecessor `[49b939]`)

First live wake with r3b/SL4.03 (`ack continue` commits its own row write). **Wake 8 — worse than 5 — the cut's dirty gate refuses every worktree wake.**

| # | ts | call | class |
|---|---|---|---|
| 1 | 21:45:27 | ListAgents | d |
| 2 | 21:45:32 | ack --gen 19 continue → `ERR: refuse to ack --commit: seats.md is dirty` | d (refused) |
| 3-4 | 21:45:46 | git status / diff seats.md | b — discovering the dirt = rotate-self's own step-2 spawn write |
| 5-6 | 21:46:03 | grep/sed rotate.py for the gate (`_ack_seats_dirty`) | c |
| 7 | 21:46:33 | hand commit "rotate-self spawn write (gen 19)" | a — a step rotate-self should do |
| 8 | 21:46:36 | ack again → committed | d |

Cause: `_ack_seats_dirty` refuses on a pre-dirtied seats.md (right intent: never bundle another seat's row); but rotate-self step 2 writes the successor's own row uncommitted in the worktree, so the file is always dirty at wake. Fix sent to sensei-director: (a) rotate-self commits its spawn write itself, or (b) the gate ignores own-row-only hunks. Expected after the fix: wake 2 (ListAgents · ack).

## rotate-out — 3 (card · `rotate-self --prepare` · rotate-self). Fine.
