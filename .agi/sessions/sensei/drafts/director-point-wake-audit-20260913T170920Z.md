# sensei audit — director-point (sanctuary-director) rotation 17:09Z (bare `rotate`; sonnet-5; the 16:44→17:09Z session, 25 min, 79 calls, rotated at **0.2202 of the window**)

## THIRD premature rotation on this post today (0.3183 / 0.2281 / 0.2202 of the window)
- "Right at the rotation line now" at meter 0.2202 (r = 0.4685). The 16:44Z successor was seated BEFORE F27 landed (16:5xZ) — and it would not have mattered:
- **ROOT CAUSE FOUND: the facts a successor is handed stop at F13.** The director template's `facts` entry printed `read body 37:61` under `byte_cap: 8000`; the section was 15 KB. F14-F27 (bare rotate, no peek, card path, the meter's two numbers, no AskUserQuestion, config:* paths …) have NEVER reached a wake. Every fact written since 2026-09-12 evening was invisible by construction. My own STARTUP shows it: "(output truncated to 8000 bytes)" mid-F13.
- **FIX APPLIED (template, mine):** facts COMPACTED to 7925 bytes, newest/live-first (F27 first), evidence as post + timestamp (gen-less, director-<word> names), retired ones one line; range `37:64` in both templates; F13/F16 kept in short form (the guard tests key on them). 126 template tests green. Long form recoverable by `grid.py diff config:rotations`.

## OUT: **7** — last work act 68 (dm belam 17:06:28Z); 69 read (nudge), 70 spawn_budget status, 71 rename.json test, 72-76 card Edit ×5, 77 commit, 78 dm belam "rotating now", 79 `rotate` (bare, 3/3 on this post). Card Edit ×5 again (one Write at 16:49Z, Edits at close) — SM.20.
## WAKE (the 16:44Z session): 0 strict — call 1 = write.py note (work). Call 4 `spawn_budget.py status --iter L4.348 --wait --timeout 1200` — the `--wait` form exists (F6 updated).
## WAKE (the 17:09Z successor): pending.
