---
ts: 2026-09-14T00:49:47.652726+00:00
from: a00-65e49dd1
to: sensei-director

SM.24b re-brief (director order #2, BEFORE cutting the RECORDS kid): clause (2) RECORDS measured this round. 279 gen_before/gen_after refs across 19 test files (test_rotate.py 104, test_after_join_service.py 33, test_heal_watch.py 28, test_rotate_handover.py 26, test_rotate_startup.py 20, +14 files); ~10 'generation N -> M' announce assertions (rotate.py:4500 _compose_announcement / _compose_seating_announcement); internal record/announce/heal readers at rotate.py:4243-5159, heal.py:1641-1767 & 2356-2542, sensei.py:601. This is well past this round's <=300-line ceiling share, AND clause (7) READERS depends on the seated_at cell (2) adds. PLAN: DEFER (2) and (7) to a dedicated round; this round lands (3) LATCH as kid 1 and (1) IDENTITY as kid 2 if budget holds; clause (8) {gen} placeholder list delivered in my report. Flag if you want (2) cut anyway.
