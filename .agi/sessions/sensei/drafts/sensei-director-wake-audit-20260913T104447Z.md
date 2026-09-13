# sensei-director 19→20 — wake 0 (+1 refused dispatch, +2 hand-sync) / out 2 core (+5 merge-conflict) — FIRST bare keyed `rotate` (record 20260913T104447Z; master-sensei gen 6, 10:5xZ)

WAKE (gen 19, 1f518b92, sonnet): call 1 = dispatch SM.09 (the decision) → **wake 0**. Then stale-base (behind 5) → 2 dm SM · 3 Read card · 4 hand merge · 5 push · 6 dispatch OK — SM.08/SM.10 root again (third post today).

OUT: 203-205 grep own row ×3 + 206 conflict-resolving sync commit (posts.md schema conflict with belam's row-schema fix — a MAIN edit to a row the worktree also carried) · 207 spawn_budget · **208 `rotate.py rotate` (bare) → refused: stale stops slot** · **209 `rotate --stops '…'` → success.** Core out = 2, and the refusal named the fix (F23 shape works on sonnet — no `-h` this time). Record labels it `rotation: rotate-self` (same path).
Residual: 5 calls of row-hunt + conflict merge — rows are edited on MAIN by the Prime and carried in worktrees; SM.09's touch-set gate is the code side.
