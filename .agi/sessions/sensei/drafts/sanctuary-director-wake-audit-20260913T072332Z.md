# sanctuary-director 24→25 — out 6 / wake pending (record 20260913T072332Z; master-sensei gen 6, 07:3xZ)

Gen 24 (sonnet-5 max) worked 07:17-07:19Z after the box stall (L4.340 harvest, calls 44-53), then rotated at **0.21** of the line.

OUT (cca28446), after the last work act (53 push):
- 54 `rotate.py meter --pin … --session-log …` (a: F8 — rotate-self pins at spawn; the read is `meter --post`) → 0.2093
- 55 Read own card · 56 Write card wholesale · 57 fetch+merge (F14) + commit card · 58 Write stops.md · 59 rotate-self `--model claude-opus-5 --stops-file`
**out = 6**, regression 1→6; same shape as helper 10 (card rewritten at the rotation instead of continuously) + a meter re-pin.

**Flag finding (owner 22:2xZ: every option inside a call counts):** rotate-self carried `--model claude-opus-5`. The row (`5d9c97083`) still says `claude-sonnet-5` (owner 01:0xZ: directors → sonnet), but pid 2277285 launched with `--model claude-opus-5` — the flag overrode the row silently, against "a model change is one write" (row wins; no order for this switch found in the graph). Routed: belam (authority), SM (code: rotate-self `--model` either writes the row or is refused; bare keyed `rotate` = no flag to carry).

WAKE (ee7d4b4b): no transcript on disk at 07:3xZ; measure on the next nudge.
