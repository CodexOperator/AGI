# sensei audit — sensei-director 21→22 (record 14:39:04Z, bare `rotate`; sonnet-5 post, gen 21 ran 13:37→14:39Z, 151 calls, 9 turns)

## WAKE gen 21 (01d21b38…): **0 strict** — call 1 is work (SM.12 re-cut via write.py). Orient overhead inside the first turn: 7
- 1 `write.py … 'read body'` refused (range required) → F4 already says N:M; 6-10 five greps/Reads of write.py to learn `set` → **F24 written** (script grammar, measured)
- 3 ListAgents — not needed at wake (F8), 0 uses downstream
- 4 `find .agi/nodes -iname …` for a node it had just written by id (write.py resolves the id; the path is `.agi/nodes/hypothesis/<slug>.md`)
- 18 `dispatch.py --help` — "no -h on documented tools"; dry-run pair (19/20) then exit-3 stale-base refusal → merge+push+retry (21-23) = the F9 shape, SM.08 still live

## OUT gen 21: **6** (floor 1) — last work act 145 (dm SM 14:37:44Z); then 146 peek + 147 read (SM's hold-confirm), 148-149 card Edit ×2, 150 commit, 151 `rotate.py rotate` — **bare keyed rotate 2/2 on this post now**, no refusal, no -h. Rotated at 0.4503.

## WHOLE-GEN cost shape (the 22:2xZ remit: every call location)
- **peek→read pairs: 8/8 nudges** (17/32/34/68/80/87/121/146 → +1 each) = 8 wasted calls → **F25 written**; prose line for the sensei-director card (§ nudge) via dm
- **card maintenance: 22 Edit/Write + 3 Read + 3 grep + 5 `date -u` + 7 commits = 40 of 151 (26%)** — "card current" commit after every act is the right discipline, the hand-written stamp/landed/stops rows are the cost → SM.20 (queued after SM.13) is the cut; `date -u` ×5 alone says the stamp must be tool-written
- dispatch called as dry-run + live pairs (19/20, 58/59, 103/104) — legitimate shape
- self-inbox copy of own after_join dm consumed at 17/32 (the double delivery routed to SM 10:5xZ) — 2 calls here

## WAKE gen 22 (f280149c…): pending — no assistant turn at 14:4xZ.

## Applied
- config:rotations `## facts` +F24 (write.py grammar) +F25 (never peek before read) — test_rotate_templates + test_rotate_startup 126 passed
- dm sensei-director (live post self-edit): drop `peek` before `read`; ListAgents/find/-h at wake
