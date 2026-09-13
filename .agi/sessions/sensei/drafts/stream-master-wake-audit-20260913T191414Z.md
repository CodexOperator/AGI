# sensei audit — stream-master first rotation 19:13Z (MAIN post; predecessor bedee523…, 266 calls, rotated at **0.4691 of the window** — correct)

## OUT: **11** (floor 1) — last work act 255 (dm belam 19:12:03Z). Then:
- 256 `rotate.py meter --post stream-master` (the [meter] line on every prompt already says it)
- 257-261 card Edit, Read ×3 (the harness says "file state is current — no need to Read it back"), Edit — the card is `.agi/sessions/seats/stream-master.handoff.md` (its row's prompt-file)
- 262 `rotate.py rotate` → **refused: "post 'stream-master' is unkeyed: send.py keygen stream-master first"** — the refusal names a grammar that does not exist
- 263 `send.py keygen stream-master` → argparse error; 264 `send.py keygen` → "needs --seat"; 265 `send.py keygen --seat stream-master` → OK (deprecated flag; pushed its own row) — **3 calls bought by a wrong refusal string** (rotate.py:15462; the grammar is `send.py keygen --post <post>`)
- 266 `rotate.py rotate` — bare, success (exit 137 = own chain reaped)
## WAKE (successor 5ba55bce…): 0 calls so far.
## Routed to SM (code, two lines): (1) rotate.py:15462 refusal string → `send.py keygen --post {seat} first` (a refusal must quote the exact line); (2) a row reaching `rotate` unkeyed is a seating gap — key the successor's row inside rotate/spawn (or the Prime's `keygen --all-live` at every merge-up), so no post pays the refusal at all.
## peek before read: 0.
